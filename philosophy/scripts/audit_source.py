"""Compare source formats and check that reading footnotes stay attached.

Comparison normalization is used only for this audit. Published readings
always come directly from the unmodified plain-text snapshot.
"""

import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional

import corpus
from models import Passage

HTML_SOURCE_PATH = "philosophy/sources/meditations-george-long-gutenberg.html"
COMPARISON_PATH = "philosophy/data/source-comparison.json"


class HtmlBookParser(HTMLParser):
    """Collect book text, excluding translator notes and illustration captions.

    Attributes:
        book_parts: Text fragments for each book, keyed by Roman numeral.
    """

    def __init__(self) -> None:
        """Initialize the parser's book, heading, and container state."""
        super().__init__(convert_charrefs=True)
        self.book_parts: dict[str, list[str]] = {}
        self._current_book: Optional[str] = None
        self._heading_parts: Optional[list[str]] = None
        self._div_classes: list[list[str]] = []

    def handle_starttag(
        self, tag: str, attributes: list[tuple[str, Optional[str]]]
    ) -> None:
        """Track excluded containers and preserve paragraph or verse breaks."""
        if tag == "div":
            class_names = dict(attributes).get("class") or ""
            self._div_classes.append(class_names.split())
        if tag == "h2":
            self._heading_parts = []
        if self._current_book is not None and tag in ("p", "br"):
            self.book_parts[self._current_book].append("\n")

    def handle_endtag(self, tag: str) -> None:
        """Finish a heading, paragraph, or container."""
        if tag == "div":
            self._div_classes.pop()
        if tag == "h2" and self._heading_parts is not None:
            heading = "".join(self._heading_parts).strip()
            self._heading_parts = None
            self._current_book = None
            if heading.endswith(".") and heading[:-1] in corpus.BOOK_NUMERALS:
                self._current_book = heading[:-1]
                if self._current_book in self.book_parts:
                    raise ValueError(f"Repeated HTML book heading: {heading}")
                self.book_parts[self._current_book] = []
        elif self._current_book is not None and tag == "p":
            self.book_parts[self._current_book].append("\n")

    def handle_data(self, text: str) -> None:
        """Capture heading text or body text outside excluded containers."""
        if self._heading_parts is not None:
            self._heading_parts.append(text)
            return
        if self._current_book is None:
            return

        excluded_classes = {"footnote", "ctr"}
        inside_excluded_container = any(
            excluded_classes.intersection(class_names)
            for class_names in self._div_classes
        )
        if not inside_excluded_container:
            self.book_parts[self._current_book].append(text)


def parse_html_sections(html_source: str) -> dict[tuple[int, int], str]:
    """Independently extract the edition's numbered sections from HTML.

    Args:
        html_source: The complete frozen HTML download.

    Returns:
        Section bodies keyed by book number and section number.

    Raises:
        ValueError: Book order or section numbering differs from the edition.
    """
    parser = HtmlBookParser()
    parser.feed(html_source)
    parser.close()
    if list(parser.book_parts) != list(corpus.BOOK_NUMERALS):
        raise ValueError("HTML does not contain all twelve books in order")

    sections = {}
    for book_number, numeral in enumerate(corpus.BOOK_NUMERALS, start=1):
        book_text = "".join(parser.book_parts[numeral])
        # Sections have at most two digits. A wrapped verse citation in V.33
        # starts with '197.' and is not a section heading.
        headings = list(re.finditer(r"(?m)^(\d{1,2})\.\s", book_text))
        section_numbers = [int(heading.group(1)) for heading in headings]
        expected_count = corpus.BOOK_SECTION_COUNTS[book_number - 1]
        if section_numbers != list(range(2, expected_count + 1)):
            raise ValueError(
                f"Unexpected HTML section numbers in Book {numeral}"
            )

        start_offsets = [0] + [heading.start() for heading in headings]
        end_offsets = start_offsets[1:] + [len(book_text)]
        for section_number, offsets in enumerate(
            zip(start_offsets, end_offsets), start=1
        ):
            start_offset, end_offset = offsets
            sections[(book_number, section_number)] = book_text[
                start_offset:end_offset
            ]
    return sections


def _plain_text_body(section_text: str) -> str:
    """Exclude printed notes and illustration placeholders for comparison."""
    body_paragraphs = []
    inside_note = False
    for paragraph in section_text.split("\r\n\r\n"):
        if re.match(r"^ {0,4}\[[A-Z]\] ", paragraph):
            inside_note = True
            continue
        if inside_note and paragraph.startswith("    "):
            continue
        if not paragraph.strip():
            continue

        inside_note = False
        paragraph = re.sub(r"\[Illustration:[^\]]*\]", "", paragraph)
        body_paragraphs.append(paragraph)
    return "\n".join(body_paragraphs)


def _normalize_comparison_text(text: str) -> str:
    """Ignore only wrapping, emphasis markers, and dash representation."""
    text = text.replace("_", "").replace("--", "—")
    return " ".join(text.split())


def compare_source_formats(
    source: bytes, html_source: str
) -> list[dict[str, object]]:
    """Identify remaining body-text differences between the frozen formats.

    This comparison excludes translator notes and illustrations. Those bytes
    are still covered by source checksums and exact reading reconstruction.

    Args:
        source: Unmodified plain-text download.
        html_source: Unmodified HTML download decoded as UTF-8.

    Returns:
        Book/section identifiers and checksums for every differing text pair.
    """
    html_sections = parse_html_sections(html_source)
    differences = []
    for section in corpus.parse_sections(source):
        section_key = (section["book"], section["section"])
        plain_text = source[section["start"] : section["end"]].decode("utf-8")
        plain_body = _normalize_comparison_text(_plain_text_body(plain_text))
        html_body = _normalize_comparison_text(html_sections[section_key])
        if plain_body != html_body:
            differences.append(
                {
                    "book": section["book"],
                    "section": section["section"],
                    "text_sha256": corpus.calculate_checksum(
                        plain_body.encode()
                    ),
                    "html_sha256": corpus.calculate_checksum(
                        html_body.encode()
                    ),
                }
            )
    return differences


def verify_footnotes(source: bytes, passages: list[Passage]) -> None:
    """Require local footnote references and definitions in the same reading.

    Args:
        source: Frozen plain-text download.
        passages: Reviewed contiguous reading ranges.

    Raises:
        ValueError: A reading separates a note from its reference.
    """
    for passage in passages:
        reading = source[passage["start"] : passage["end"]]
        all_markers = Counter(re.findall(rb"\[([A-Z])\]", reading))
        definitions = Counter(re.findall(rb"(?m)^ {0,4}\[([A-Z])\] ", reading))
        expected_markers = Counter(
            {marker: count * 2 for marker, count in definitions.items()}
        )
        if all_markers != expected_markers:
            raise ValueError(f"Detached footnote in {passage['id']}")


def audit_source(root: Path = corpus.REPOSITORY_ROOT) -> str:
    """Verify source structure, reviewed format differences, and footnotes.

    Args:
        root: Repository root containing frozen sources and review metadata.

    Returns:
        A summary of the validated sections, differences, and readings.

    Raises:
        ValueError: A check fails or an unreviewed format difference appears.
    """
    source, passages, _ = corpus.load_corpus(root)
    html_source = (root / HTML_SOURCE_PATH).read_bytes().decode("utf-8")
    differences = compare_source_formats(source, html_source)
    comparison_review = corpus.read_json_file(root / COMPARISON_PATH)
    reviewed_differences = [
        {key: value for key, value in difference.items() if key != "reason"}
        for difference in comparison_review["differences"]
    ]
    if differences != reviewed_differences:
        raise ValueError(
            "Source format differences do not match the AI review"
        )
    if any(
        not item.get("reason") for item in comparison_review["differences"]
    ):
        raise ValueError(
            "Every source format difference needs a review reason"
        )

    verify_footnotes(source, passages)
    return (
        f"Audited 487 sections in both formats; {len(differences)} documented "
        f"differences; footnotes attached across {len(passages)} readings."
    )


if __name__ == "__main__":
    print(audit_source())
