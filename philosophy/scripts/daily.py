"""Publish the next exact reading, at most once per Europe/London date."""

import argparse
import html
import json
import os
import tempfile
from datetime import date, datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

import corpus
from models import Passage, ProgressState

START_MARKER = b"<!-- DAILY-PHILOSOPHY:START -->"
END_MARKER = b"<!-- DAILY-PHILOSOPHY:END -->"
PROGRESS_PATH = "philosophy/state/progress.json"
INITIAL_READING = b"The first reading will appear here."
PUBLICATION_TIMEZONE = ZoneInfo("Europe/London")


def find_reading_region(readme: bytes) -> tuple[int, int]:
    """Return the byte offsets between the README's unique reading markers.

    Args:
        readme: Complete README contents, without newline conversion.

    Returns:
        Start-inclusive/end-exclusive offsets for the replaceable region.

    Raises:
        ValueError: Markers are missing, repeated, or reversed.
    """
    if readme.count(START_MARKER) != 1 or readme.count(END_MARKER) != 1:
        raise ValueError("README needs exactly one pair of reading markers")

    start_offset = readme.index(START_MARKER) + len(START_MARKER)
    end_offset = readme.index(END_MARKER)
    if start_offset >= end_offset:
        raise ValueError("README reading markers are reversed")
    return start_offset, end_offset


def render_reading(
    source: bytes,
    passage: Passage,
    publication_date: str,
    reading_number: int,
    reading_count: int,
) -> bytes:
    """Format a reading while preserving the source payload exactly.

    Args:
        source: Frozen source bytes.
        passage: Reviewed section boundaries and source offsets.
        publication_date: Publication date in ISO format.
        reading_number: One-based position in the reading sequence.
        reading_count: Total number of readings in the catalog.

    Returns:
        README content for the region between the reading markers.

    Raises:
        ValueError: HTML escaping does not reverse to the original bytes.
    """
    section_reference = str(passage["first"])
    if passage["last"] != passage["first"]:
        section_reference += f"–{passage['last']}"
    book_numeral = corpus.BOOK_NUMERALS[passage["book"] - 1]
    title = (
        f"**Marcus Aurelius — Meditations {book_numeral}.{section_reference}**"
        "  \n"
        f"George Long translation · {publication_date} · "
        f"Reading {reading_number} of {reading_count}\n\n"
    )

    original_text = source[passage["start"] : passage["end"]]
    escaped_text = html.escape(original_text.decode("utf-8"), quote=False)
    restored_text = html.unescape(escaped_text).encode("utf-8")
    if restored_text != original_text:
        raise ValueError("Rendering changed source text")

    # Prevent Markdown from interpreting section numbers, underscores or verse.
    reading = title + f"<pre>{escaped_text}</pre>\n\n"
    reading += (
        "[Source edition](https://www.gutenberg.org/ebooks/15877)"
        " · [Reading archive](philosophy/README.md)\n\n"
        "*The edition's translator notes and text markings are preserved.*"
    )
    if reading_number == reading_count:
        reading += (
            "\n\n**Meditations is complete. "
            "All readings remain available in the archive.**"
        )
    return ("\n\n" + reading + "\n\n").encode("utf-8")


def _validate_state(
    state: ProgressState,
    passages: list[Passage],
    catalog_checksum: str,
) -> int:
    """Check saved progress and return the next unpublished passage index."""
    expected_fields = {
        "catalog_sha256",
        "next_index",
        "last_published_date",
        "passage_id",
    }
    if set(state) != expected_fields:
        raise ValueError("Unexpected progress fields")
    if state["catalog_sha256"] != catalog_checksum:
        raise ValueError(
            "The catalog changed; review progress before continuing"
        )

    next_index = state["next_index"]
    if type(next_index) is not int or not 0 <= next_index <= len(passages):
        raise ValueError("Invalid progress index")

    publication_date = state["last_published_date"]
    if next_index == 0:
        if publication_date is not None or state["passage_id"] is not None:
            raise ValueError("Invalid initial progress")
        return next_index

    if not isinstance(publication_date, str):
        raise ValueError("Missing publication date")
    if date.fromisoformat(publication_date).isoformat() != publication_date:
        raise ValueError("Invalid publication date")
    if state["passage_id"] != passages[next_index - 1]["id"]:
        raise ValueError("Progress passage does not match its index")
    return next_index


def validate_progress(
    state: ProgressState,
    passages: list[Passage],
    catalog_checksum: str,
    readme: bytes,
    source: bytes,
) -> int:
    """Verify that saved progress and the displayed reading agree.

    Args:
        state: Saved publication state.
        passages: Validated readings in their original order.
        catalog_checksum: Checksum of the current catalog file.
        readme: Complete README contents.
        source: Frozen source bytes.

    Returns:
        The zero-based index of the next unpublished reading.

    Raises:
        ValueError: State is invalid or the displayed reading has changed.
    """
    next_index = _validate_state(state, passages, catalog_checksum)
    if next_index == 0:
        expected_reading = b"\n\n" + INITIAL_READING + b"\n\n"
    else:
        expected_reading = render_reading(
            source,
            passages[next_index - 1],
            state["last_published_date"],
            next_index,
            len(passages),
        )

    start_offset, end_offset = find_reading_region(readme)
    if readme[start_offset:end_offset] != expected_reading:
        raise ValueError("README reading does not match the saved progress")
    return next_index


def _atomic_write(path: Path, content: bytes) -> None:
    """Replace one local file atomically; Git publishes the pair together."""
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(content)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def publish_daily_reading(
    root: Path = corpus.REPOSITORY_ROOT,
    today: Optional[date] = None,
    check_only: bool = False,
) -> str:
    """Validate the repository and publish at most one reading for the date.

    Args:
        root: Repository root containing the README, corpus and progress.
        today: Date override for tests. Defaults to today's London date.
        check_only: Validate without writing or advancing progress.

    Returns:
        A short status message describing publication or the reason to stop.

    Raises:
        ValueError: Validation fails or the supplied date moves backwards.
        OSError: A required file cannot be read or written.
    """
    source, passages, catalog_checksum = corpus.load_corpus(root)
    state: ProgressState = corpus.read_json_file(root / PROGRESS_PATH)
    readme = (root / "README.md").read_bytes()
    next_index = validate_progress(
        state, passages, catalog_checksum, readme, source
    )
    if check_only:
        return "Source, all passages, progress and README verified."

    publication_date = today or datetime.now(PUBLICATION_TIMEZONE).date()
    last_publication_date = state["last_published_date"]
    if last_publication_date is not None:
        if publication_date < date.fromisoformat(last_publication_date):
            raise ValueError("Cannot publish before the last publication date")
        if last_publication_date == publication_date.isoformat():
            return f"Already published for {publication_date}. No changes."
    if next_index == len(passages):
        return "Meditations is complete. No changes."

    passage = passages[next_index]
    new_reading = render_reading(
        source,
        passage,
        publication_date.isoformat(),
        next_index + 1,
        len(passages),
    )
    start_offset, end_offset = find_reading_region(readme)
    new_readme = readme[:start_offset] + new_reading + readme[end_offset:]
    new_state: ProgressState = {
        "catalog_sha256": catalog_checksum,
        "next_index": next_index + 1,
        "last_published_date": publication_date.isoformat(),
        "passage_id": passage["id"],
    }

    # Validate the proposed pair before either local file is replaced.
    validate_progress(
        new_state, passages, catalog_checksum, new_readme, source
    )
    new_state_bytes = (json.dumps(new_state, indent=2) + "\n").encode("utf-8")
    _atomic_write(root / "README.md", new_readme)
    _atomic_write(root / PROGRESS_PATH, new_state_bytes)
    return f"Published {passage['id']} for {publication_date}."


def main() -> None:
    """Run publication or a read-only validation from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate without advancing the reading.",
    )
    arguments = parser.parse_args()
    try:
        print(publish_daily_reading(check_only=arguments.check))
    except (ValueError, KeyError, OSError, TypeError) as error:
        parser.exit(1, f"Daily reading stopped: {error}\n")


if __name__ == "__main__":
    main()
