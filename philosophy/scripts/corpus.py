"""Extract and validate readings without changing the frozen source text."""

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from models import Catalog, Passage, ReadingPlan, Section

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = "philosophy/sources/meditations-george-long-gutenberg.txt"
CATALOG_PATH = "philosophy/data/passages.json"
READING_PLAN_PATH = "philosophy/data/reading-plan.json"
BOOK_NUMERALS = (
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
    "XI",
    "XII",
)
BOOK_SECTION_COUNTS = (17, 17, 16, 51, 36, 59, 75, 61, 42, 38, 39, 36)
SOURCE_FILENAMES = {
    "meditations-george-long-gutenberg.txt",
    "meditations-george-long-gutenberg.html",
}


def calculate_checksum(content: bytes) -> str:
    """Return the SHA-256 checksum of the exact supplied bytes."""
    return hashlib.sha256(content).hexdigest()


def read_json_file(path: Path) -> Any:
    """Read a UTF-8 JSON document without altering its line endings."""
    return json.loads(path.read_bytes())


def verify_sources(root: Path = REPOSITORY_ROOT) -> None:
    """Verify every frozen source against the committed checksum manifest.

    Args:
        root: Repository root containing the source files.

    Raises:
        ValueError: A source changed or a manifest entry is invalid.
        OSError: A source or the manifest cannot be read.
    """
    source_directory = root / "philosophy/sources"
    manifest_path = source_directory / "SHA256SUMS"
    manifest_lines = manifest_path.read_text(encoding="ascii").splitlines()
    verified_filenames = set()

    for line in manifest_lines:
        expected_checksum, filename = line.split("  ", 1)
        if filename not in SOURCE_FILENAMES:
            raise ValueError(f"Unexpected source checksum: {filename}")
        if filename in verified_filenames:
            raise ValueError(f"Duplicate source checksum: {filename}")

        source_content = (source_directory / filename).read_bytes()
        if calculate_checksum(source_content) != expected_checksum:
            raise ValueError(f"Source checksum mismatch: {filename}")
        verified_filenames.add(filename)

    if verified_filenames != SOURCE_FILENAMES:
        raise ValueError("Missing source checksum")


def _find_book_ranges(source: bytes) -> list[tuple[int, int]]:
    """Locate book bodies, excluding headings and surrounding blank lines."""
    headings = list(re.finditer(rb"(?m)^([IVX]+)\.\r\n", source))
    found_numerals = [heading.group(1).decode("ascii") for heading in headings]
    if found_numerals != list(BOOK_NUMERALS):
        raise ValueError("Expected the twelve book headings in order")

    book_ranges = []
    for book_index, heading in enumerate(headings):
        start_offset = heading.end()
        if book_index + 1 < len(headings):
            end_offset = headings[book_index + 1].start()
        else:
            end_offset = source.index(b"\r\nINDEXES.", start_offset)

        while source[start_offset : start_offset + 1] in (b"\r", b"\n"):
            start_offset += 1
        while source[end_offset - 1 : end_offset] in (b"\r", b"\n"):
            end_offset -= 1
        book_ranges.append((start_offset, end_offset))

    return book_ranges


def parse_sections(source: bytes) -> list[Section]:
    """Locate sections using the edition's existing numbering.

    Notes and publisher material remain in their original positions. The
    first section of each book is unnumbered in this edition.

    Args:
        source: Unmodified UTF-8 bytes of the Gutenberg text download.

    Returns:
        Ordered sections, with start-inclusive/end-exclusive offsets.

    Raises:
        ValueError: Book headings or section numbering are inconsistent.
    """
    sections = []
    for book_index, offsets in enumerate(_find_book_ranges(source)):
        book_start, book_end = offsets
        book_body = source[book_start:book_end]
        numbered_sections = list(re.finditer(rb"(?m)^(\d+)\. ", book_body))
        found_numbers = [
            int(section.group(1)) for section in numbered_sections
        ]
        expected_count = BOOK_SECTION_COUNTS[book_index]
        if found_numbers != list(range(2, expected_count + 1)):
            numeral = BOOK_NUMERALS[book_index]
            raise ValueError(f"Unexpected section numbering in Book {numeral}")

        start_offsets = [book_start]
        start_offsets.extend(
            book_start + section.start() for section in numbered_sections
        )
        end_offsets = start_offsets[1:] + [book_end]

        for section_number, offsets in enumerate(
            zip(start_offsets, end_offsets), start=1
        ):
            start_offset, end_offset = offsets
            sections.append(
                {
                    "book": book_index + 1,
                    "section": section_number,
                    "start": start_offset,
                    "end": end_offset,
                }
            )

    return sections


def _validate_groups(plan: ReadingPlan) -> dict[tuple[int, int], int]:
    """Map each reviewed group's opening section to its final section."""
    group_endings = {}
    grouped_sections = set()

    for group in plan["groups"]:
        book = group["book"]
        first_section = group["first"]
        last_section = group["last"]
        boundaries = (book, first_section, last_section)
        if any(type(value) is not int for value in boundaries):
            raise ValueError("Reading boundaries must be integers")
        if not 1 <= book <= len(BOOK_NUMERALS):
            raise ValueError(f"Invalid book number: {book}")
        section_count = BOOK_SECTION_COUNTS[book - 1]
        if not 1 <= first_section < last_section <= section_count:
            raise ValueError(f"Invalid reading boundary in Book {book}")
        if not isinstance(group["reason"], str) or not group["reason"].strip():
            raise ValueError("Merged readings need a review reason")

        section_keys = {
            (book, number) for number in range(first_section, last_section + 1)
        }
        if grouped_sections.intersection(section_keys):
            raise ValueError(f"Overlapping reading groups in Book {book}")
        grouped_sections.update(section_keys)
        group_endings[(book, first_section)] = last_section

    return group_endings


def _verify_book_coverage(source: bytes, passages: list[Passage]) -> None:
    """Reassemble every book to detect gaps, duplication, and reordering."""
    for book_number, offsets in enumerate(_find_book_ranges(source), start=1):
        start_offset, end_offset = offsets
        book_passages = [
            passage for passage in passages if passage["book"] == book_number
        ]
        reconstructed_book = b"".join(
            source[passage["start"] : passage["end"]]
            for passage in book_passages
        )
        if reconstructed_book != source[start_offset:end_offset]:
            raise ValueError(
                f"Reading coverage mismatch in Book {book_number}"
            )


def build_catalog(source: bytes, plan: ReadingPlan) -> Catalog:
    """Build passage metadata from source sections and reviewed boundaries.

    Args:
        source: Original source bytes. This function never changes them.
        plan: Contiguous section groups selected during editorial review.

    Returns:
        Offsets and checksums for every reading, with no copied passage text.

    Raises:
        ValueError: A group is invalid or book coverage is incomplete.
    """
    sections = parse_sections(source)
    sections_by_number = {
        (section["book"], section["section"]): section for section in sections
    }
    group_endings = _validate_groups(plan)
    passages = []
    section_index = 0

    while section_index < len(sections):
        section = sections[section_index]
        book = section["book"]
        first_section = section["section"]
        last_section = group_endings.get((book, first_section), first_section)
        start_offset = section["start"]
        end_offset = sections_by_number[(book, last_section)]["end"]
        passage_id = (
            f"meditations-long-{book:02d}-"
            f"{first_section:03d}-{last_section:03d}"
        )

        passages.append(
            {
                "id": passage_id,
                "book": book,
                "first": first_section,
                "last": last_section,
                "start": start_offset,
                "end": end_offset,
                "sha256": calculate_checksum(source[start_offset:end_offset]),
            }
        )
        section_index += last_section - first_section + 1

    _verify_book_coverage(source, passages)
    return {
        "source": SOURCE_PATH,
        "source_sha256": calculate_checksum(source),
        "passages": passages,
    }


def load_corpus(
    root: Path = REPOSITORY_ROOT,
) -> tuple[bytes, list[Passage], str]:
    """Load a catalog only after verifying it against the frozen source.

    Args:
        root: Repository root containing sources, plan, and catalog.

    Returns:
        The source bytes, ordered passages, and catalog file's checksum.

    Raises:
        ValueError: A checksum or the reconstructed catalog does not match.
    """
    verify_sources(root)
    source = (root / SOURCE_PATH).read_bytes()
    saved_catalog: Catalog = read_json_file(root / CATALOG_PATH)
    reading_plan: ReadingPlan = read_json_file(root / READING_PLAN_PATH)
    expected_catalog = build_catalog(source, reading_plan)
    if saved_catalog != expected_catalog:
        raise ValueError(
            "Passage catalog does not match the source and reading plan"
        )

    catalog_checksum = calculate_checksum((root / CATALOG_PATH).read_bytes())
    return source, saved_catalog["passages"], catalog_checksum
