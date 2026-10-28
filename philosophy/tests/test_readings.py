"""Check repository output and exercise publication in isolated copies."""

import copy
import html
import json
import re
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from typing import Any
from unittest.mock import patch

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "philosophy/scripts"))

import archive  # noqa: E402
import audit_source  # noqa: E402
import corpus  # noqa: E402
import daily  # noqa: E402
import paragraphs  # noqa: E402


class RepositoryOutputTests(unittest.TestCase):
    """Require checked-in output to match the current renderer and progress."""

    def test_current_reading_matches_saved_progress(self) -> None:
        """Catch stale README formatting without publishing another reading."""
        daily.publish_daily_reading(REPOSITORY_ROOT, check_only=True)

    def test_archive_matches_current_renderer(self) -> None:
        """Catch stale archive output after source or rendering changes."""
        archive.prepare_archive(REPOSITORY_ROOT, check_only=True)


class ReadingsTests(unittest.TestCase):
    """Verify that publication preserves source text and advances safely."""

    def setUp(self) -> None:
        """Create a disposable repository with a fresh publication state."""
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        self.root = Path(temporary_directory.name)
        shutil.copytree(
            REPOSITORY_ROOT / "philosophy/sources",
            self.root / "philosophy/sources",
        )
        self.source = (self.root / corpus.SOURCE_PATH).read_bytes()
        self.plan = corpus.read_json_file(
            REPOSITORY_ROOT / corpus.READING_PLAN_PATH
        )
        self._write_json_file(corpus.READING_PLAN_PATH, self.plan)
        self.catalog = corpus.build_catalog(self.source, self.plan)
        self._write_json_file(corpus.CATALOG_PATH, self.catalog)
        self.passages = self.catalog["passages"]
        catalog_content = (self.root / corpus.CATALOG_PATH).read_bytes()
        self.initial_state = {
            "catalog_sha256": corpus.calculate_checksum(catalog_content),
            "next_index": 0,
            "last_published_date": None,
            "passage_id": None,
        }
        self._write_json_file(daily.PROGRESS_PATH, self.initial_state)
        self.readme_path = self.root / "README.md"
        self.readme_path.write_bytes(
            b"# Personal notes\r\nKeep <this> & that.\r\n"
            + daily.START_MARKER
            + b"\n\n"
            + daily.INITIAL_READING
            + b"\n\n"
            + daily.END_MARKER
            + b"\r\n## Links\r\nKeep these too.\r\n"
        )

    def _quote_payload(self, rendered: bytes) -> bytes:
        """Remove quote prefixes while retaining original line endings."""
        body = rendered.split(b"</sub>\n\n", 1)[1].split(b"\n\n<sub>", 1)[0]
        quotes = re.findall(
            rb"(?:\A|\n\n)(> .*?)(?=(?<!\r)\n\n|\Z)", body, re.DOTALL
        )
        self.assertTrue(quotes)
        payload = b""
        for quote in quotes:
            lines = quote.splitlines(keepends=True)
            self.assertTrue(all(line.startswith(b"> ") for line in lines))
            self.assertNotIn(b">     ", quote)
            payload += b"".join(line[2:] for line in lines)
        return re.sub(rb"\\([\\`*_{}\[\]()#+\-.!|~])", rb"\1", payload)

    def _write_json_file(self, relative_path: str, value: Any) -> None:
        """Write test data beneath the disposable repository root."""
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((json.dumps(value, indent=2) + "\n").encode("utf-8"))

    def _snapshot_publication(self) -> tuple[bytes, bytes]:
        """Capture both files whose contents publication may change."""
        readme = self.readme_path.read_bytes()
        progress = (self.root / daily.PROGRESS_PATH).read_bytes()
        return readme, progress

    def _assert_publication_stopped(
        self, today: date = date(2026, 10, 20)
    ) -> None:
        """Require validation to reject input before either file is written."""
        original_files = self._snapshot_publication()
        with self.assertRaises((ValueError, KeyError, TypeError)):
            daily.publish_daily_reading(self.root, today=today)
        self.assertEqual(original_files, self._snapshot_publication())

    def test_source_corruption_stops_publication(self) -> None:
        """Changing even an unused snapshot invalidates source verification."""
        for filename in corpus.SOURCE_FILENAMES:
            with self.subTest(source=filename):
                path = self.root / "philosophy/sources" / filename
                original_content = path.read_bytes()
                path.write_bytes(original_content + b"alteration")
                self._assert_publication_stopped()
                path.write_bytes(original_content)

    def test_missing_or_duplicate_checksum_is_rejected(self) -> None:
        """The manifest must cover every source exactly once."""
        manifest_path = self.root / "philosophy/sources/SHA256SUMS"
        lines = manifest_path.read_bytes().splitlines(keepends=True)
        invalid_manifests = (
            b"".join(lines[:-1]),
            b"".join(lines + lines[:1]),
        )
        for manifest in invalid_manifests:
            with self.subTest(manifest=manifest):
                manifest_path.write_bytes(manifest)
                self._assert_publication_stopped()

    def test_catalog_metadata_or_boundaries_cannot_change(self) -> None:
        """The saved catalog must agree with independently extracted ranges."""
        mutations = (
            ("id", "invented"),
            ("start", 0),
            ("end", 1),
            ("sha256", "0" * 64),
            ("book", 2),
            ("last", 99),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                changed_catalog = copy.deepcopy(self.catalog)
                changed_catalog["passages"][0][field] = value
                self._write_json_file(corpus.CATALOG_PATH, changed_catalog)
                self._assert_publication_stopped()

        changed_catalog = copy.deepcopy(self.catalog)
        changed_catalog["passages"].pop()
        self._write_json_file(corpus.CATALOG_PATH, changed_catalog)
        self._assert_publication_stopped()

    def test_overlapping_or_invalid_reading_plan_is_rejected(self) -> None:
        """Grouping must use real section numbers and nonoverlapping ranges."""
        valid_group = {
            "book": 1,
            "first": 1,
            "last": 4,
            "reason": "Family notes.",
        }
        invalid_plans = (
            [valid_group, dict(valid_group, first=3, last=5)],
            [dict(valid_group, first=True)],
            [dict(valid_group, last=18)],
            [dict(valid_group, reason="")],
        )
        for groups in invalid_plans:
            with self.subTest(groups=groups):
                self._write_json_file(
                    corpus.READING_PLAN_PATH, {"groups": groups}
                )
                self._assert_publication_stopped()

    def test_all_sections_and_source_bytes_are_covered_once(self) -> None:
        """Reassembled readings equal independently located book bodies."""
        source, passages, _ = corpus.load_corpus(self.root)
        self.assertEqual(source, self.source)
        represented_sections = [
            (passage["book"], section_number)
            for passage in passages
            for section_number in range(passage["first"], passage["last"] + 1)
        ]
        self.assertEqual(len(represented_sections), 487)
        self.assertEqual(len(set(represented_sections)), 487)

        for book_number, numeral in enumerate(corpus.BOOK_NUMERALS, start=1):
            with self.subTest(book=book_number):
                book_passages = [
                    passage
                    for passage in passages
                    if passage["book"] == book_number
                ]
                heading = f"\r\n{numeral}.\r\n".encode()
                book_body = source.split(heading, 1)[1]
                if book_number < 12:
                    next_numeral = corpus.BOOK_NUMERALS[book_number]
                    next_heading = f"\r\n{next_numeral}.\r\n".encode()
                else:
                    next_heading = b"\r\nINDEXES."
                book_body = book_body.split(next_heading, 1)[0].strip(b"\r\n")
                reconstructed_book = b"".join(
                    source[passage["start"] : passage["end"]]
                    for passage in book_passages
                )
                self.assertEqual(reconstructed_book, book_body)
                for previous, following in zip(
                    book_passages, book_passages[1:]
                ):
                    self.assertEqual(previous["end"], following["start"])

    def test_render_roundtrip_preserves_every_character(self) -> None:
        """HTML escaping preserves literal markup, entities, and CRLF bytes."""
        original_text = (
            b"<section>&amp; & [A] _words_\r\n    indented\r\n</pre>\r\n"
            b"\r\n2. Literal *stars*, `code`, [link](url), and \\slashes."
        )
        passage = dict(self.passages[0], start=0, end=len(original_text))
        rendered = daily.render_reading(
            original_text, passage, "2026-10-20", 1, 2
        )
        payload = self._quote_payload(rendered)
        self.assertNotIn(b"<", payload)
        self.assertIn(b"&amp;amp;", payload)
        self.assertEqual(
            html.unescape(payload.decode()).encode(), original_text
        )

    def test_every_reading_renders_exact_source_bytes(self) -> None:
        """All 437 rendered payloads recover their original source slices."""
        for reading_number, passage in enumerate(self.passages, start=1):
            with self.subTest(passage=passage["id"]):
                rendered = daily.render_reading(
                    self.source,
                    passage,
                    "2026-10-20",
                    reading_number,
                    len(self.passages),
                )
                payload = self._quote_payload(rendered)
                original_text = self.source[passage["start"] : passage["end"]]
                self.assertEqual(
                    html.unescape(payload.decode()).encode(), original_text
                )
                definitions = re.findall(
                    rb"(?m)^ {0,4}\[[A-Z]\] ", original_text
                )
                collapsed_notes = b"".join(
                    re.findall(
                        rb"<details>(.*?)</details>", rendered, re.DOTALL
                    )
                )
                hidden_definitions = re.findall(
                    rb"(?m)^> (?:&#32;){0,4}\\\[[A-Z]\\\] ",
                    collapsed_notes,
                )
                self.assertEqual(len(hidden_definitions), len(definitions))
                if not definitions:
                    self.assertNotIn(b"<details>", rendered)

    def test_reviewed_paragraphs_preserve_whitespace_and_notes(self) -> None:
        """Editorial breaks retain spaces, CRLF, and note placement."""
        original = (
            b"First sentence.[A] Second sentence.\r\nThird sentence.\r\n\r\n"
            b"    [A] A note remains intact. More explanation.\r\n\r\n"
        )
        passage = dict(self.passages[0], start=0, end=len(original))
        anchors = (b"Second sentence.", b"Third sentence.")
        with patch.dict(paragraphs.PARAGRAPH_STARTS, {passage["id"]: anchors}):
            source_blocks = daily.split_translator_notes(original)
            split_blocks = paragraphs.split_paragraphs(
                source_blocks, passage["id"]
            )
            self.assertEqual(
                split_blocks,
                [
                    (False, b"First sentence.[A] "),
                    (False, b"Second sentence.\r\n"),
                    (False, b"Third sentence.\r\n\r\n"),
                    source_blocks[-1],
                ],
            )
            rendered = daily.render_reading(
                original, passage, "2026-10-20", 1, 2
            )
            archive_rendered = daily.render_reading(
                original,
                passage,
                None,
                1,
                2,
                archive_url="../README.md#readings",
            )
        self.assertIn(b"\\[A\\]&#32;\n\n> Second", rendered)
        self.assertIn(b"sentence\\.\r\n\n\n> Third", rendered)
        self.assertEqual(rendered.count(b"<details>"), 1)
        self.assertIn(b'href="philosophy/paragraph-review.md"', rendered)
        self.assertIn(b'href="../paragraph-review.md"', archive_rendered)
        self.assertEqual(
            html.unescape(self._quote_payload(rendered).decode()).encode(),
            original,
        )

    def test_invalid_editorial_paragraphs_are_rejected(self) -> None:
        """Reject anchors within sentences, verse, or hidden notes."""
        passage_id = "test-paragraphs"
        cases = (
            ([(False, b"First. Next.")], (b"Missing.",)),
            ([(False, b"First. Next. Next.")], (b"Next.",)),
            ([(False, b"First. Second. Third.")], (b"Third.", b"Second.")),
            ([(False, b"First. Next.")], (b"Next.", b"Next.")),
            ([(False, b"First. Next.")], (b"First.",)),
            ([(False, b"First. Next.")], (b" Next.",)),
            ([(False, b"First. Next.")], (b"",)),
            ([(False, b"First; Next.")], (b"Next.",)),
            ([(False, b"First.Next.")], (b"Next.",)),
            ([(False, b"First.\r\n\r\nNext.")], (b"Next.",)),
            ([(False, b"    Verse. Another line.")], (b"Another line.",)),
            (
                [(False, b"First.\r\n\r\n"), (True, b"[A] Note. More.")],
                (b"More.",),
            ),
            (
                [(False, b"First. "), (False, b"Next.")],
                (b"Next.",),
            ),
        )
        for blocks, anchors in cases:
            with self.subTest(blocks=blocks, anchors=anchors):
                with patch.dict(
                    paragraphs.PARAGRAPH_STARTS, {passage_id: anchors}
                ):
                    with self.assertRaises(ValueError):
                        paragraphs.split_paragraphs(blocks, passage_id)

    def test_archive_navigation_and_source(self) -> None:
        """Every archive arrow resolves and every payload preserves bytes."""
        pages = archive.render_archive(self.source, self.passages)
        self.assertEqual(len(pages), len(self.passages))
        for reading_number, passage in enumerate(self.passages, start=1):
            with self.subTest(reading=reading_number):
                filename = f"reading-{reading_number:03d}.md"
                reading = pages[filename]
                self.assertEqual(reading.count(b"# Reading "), 1)
                self.assertTrue(
                    reading.startswith(
                        f"# Reading {reading_number}\n".encode()
                    )
                )
                self.assertEqual(reading.count(b"**Marcus Aurelius"), 1)
                payload = self._quote_payload(reading)
                self.assertEqual(
                    html.unescape(payload.decode()).encode(),
                    self.source[passage["start"] : passage["end"]],
                )
                self.assertEqual(
                    b'aria-label="Previous reading"' in reading,
                    reading_number > 1,
                )
                self.assertEqual(
                    b'aria-label="Next reading"' in reading,
                    reading_number < len(self.passages),
                )
                targets = re.findall(rb'href="(reading-\d+\.md)"', reading)
                expected_targets = []
                if reading_number > 1:
                    expected_targets.append(
                        f"reading-{reading_number - 1:03d}.md"
                    )
                if reading_number < len(self.passages):
                    expected_targets.append(
                        f"reading-{reading_number + 1:03d}.md"
                    )
                self.assertEqual(
                    [target.decode() for target in targets], expected_targets
                )
                for target in targets:
                    self.assertIn(target.decode(), pages)

    def test_daily_previous_arrow_crosses_book_boundary(self) -> None:
        """The daily reading links directly to the preceding archived text."""
        reading_number = next(
            index + 1
            for index, passage in enumerate(self.passages)
            if passage["book"] == 2
        )
        rendered = daily.render_reading(
            self.source,
            self.passages[reading_number - 1],
            "2026-10-20",
            reading_number,
            len(self.passages),
            previous_url=daily.previous_reading_url(reading_number),
        )
        self.assertIn(b'href="philosophy/readings/reading-010.md"', rendered)

    def test_notes_collapse_without_hiding_prose_or_verse(self) -> None:
        """Only definitions and their continuation paragraphs are collapsed."""
        prose = b"A thought[A] with [a clarification].\r\n\r\n"
        verse = b"    Verse belongs in the main reading.\r\n\r\n"
        note = (
            b"    [A] A translator's explanation.\r\n\r\n"
            b"    Another paragraph of that note.\r\n\r\n"
        )
        following = b"2. The next thought[B].\r\n\r\n"
        second_note = b"[B] An unindented note."
        original = prose + verse + note + following + second_note
        self.assertEqual(
            daily.split_translator_notes(original),
            [
                (False, prose + verse),
                (True, note),
                (False, following),
                (True, second_note),
            ],
        )
        passage = dict(self.passages[0], start=0, end=len(original))
        rendered = daily.render_reading(original, passage, "2026-10-20", 1, 2)
        self.assertEqual(rendered.count(b"<details>"), 2)
        self.assertNotIn(b"<details open", rendered)
        self.assertIn(b"\\[a clarification\\]", rendered)
        self.assertNotIn(b"&#91;", rendered)
        self.assertEqual(
            html.unescape(self._quote_payload(rendered).decode()).encode(),
            original,
        )

    def test_daily_progress_rerun_and_missed_days(self) -> None:
        """Reruns are inert and missed dates never skip unread passages."""
        original_readme = self.readme_path.read_bytes()
        original_start, original_end = daily.find_reading_region(
            original_readme
        )
        daily.publish_daily_reading(self.root, today=date(2026, 10, 20))
        published_files = self._snapshot_publication()
        first_passage = self.passages[0]
        payload = self._quote_payload(published_files[0])
        self.assertEqual(
            html.unescape(payload.decode()).encode(),
            self.source[first_passage["start"] : first_passage["end"]],
        )
        daily.publish_daily_reading(self.root, today=date(2026, 10, 20))
        self.assertEqual(self._snapshot_publication(), published_files)
        daily.publish_daily_reading(self.root, today=date(2026, 10, 25))
        state = corpus.read_json_file(self.root / daily.PROGRESS_PATH)
        self.assertEqual(state["next_index"], 2)
        self.assertEqual(state["passage_id"], self.passages[1]["id"])

        updated_readme = self.readme_path.read_bytes()
        updated_start, updated_end = daily.find_reading_region(updated_readme)
        self.assertEqual(
            updated_readme[:updated_start], original_readme[:original_start]
        )
        self.assertEqual(
            updated_readme[updated_end:], original_readme[original_end:]
        )
        before_check = self._snapshot_publication()
        daily.publish_daily_reading(self.root, check_only=True)
        self.assertEqual(self._snapshot_publication(), before_check)

    def test_invalid_markers_or_reading_fail_without_writes(self) -> None:
        """Marker damage or edited content cannot overwrite the README."""
        original_readme = self.readme_path.read_bytes()
        invalid_readmes = (
            original_readme.replace(daily.END_MARKER, b""),
            original_readme + daily.START_MARKER,
            daily.END_MARKER + b"\n" + daily.START_MARKER,
            original_readme.replace(daily.INITIAL_READING, b"edited"),
        )
        for readme in invalid_readmes:
            with self.subTest(readme=readme):
                self.readme_path.write_bytes(readme)
                self._assert_publication_stopped()

    def test_invalid_state_and_backward_date_fail_without_writes(self) -> None:
        """Invalid progress and dates cannot advance the reading."""
        mutations = (
            ("next_index", True),
            ("next_index", -1),
            ("catalog_sha256", "wrong"),
            ("passage_id", "wrong"),
            ("last_published_date", "not-a-date"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                changed_state = dict(self.initial_state, **{field: value})
                self._write_json_file(daily.PROGRESS_PATH, changed_state)
                self._assert_publication_stopped()

        self._write_json_file(daily.PROGRESS_PATH, self.initial_state)
        daily.publish_daily_reading(self.root, today=date(2026, 10, 20))
        self._assert_publication_stopped(date(2026, 10, 19))
        state = corpus.read_json_file(self.root / daily.PROGRESS_PATH)
        state["last_published_date"] = "2026-02-30"
        self._write_json_file(daily.PROGRESS_PATH, state)
        self._assert_publication_stopped()

    def test_final_reading_is_published_then_stops(self) -> None:
        """The complete sequence ends without resetting or repeating."""
        next_index = len(self.passages) - 1
        state = dict(
            self.initial_state,
            next_index=next_index,
            last_published_date="2026-10-19",
            passage_id=self.passages[next_index - 1]["id"],
        )
        self._write_json_file(daily.PROGRESS_PATH, state)
        previous_reading = daily.render_reading(
            self.source,
            self.passages[next_index - 1],
            "2026-10-19",
            next_index,
            len(self.passages),
            previous_url=daily.previous_reading_url(next_index),
        )
        self.readme_path.write_bytes(
            daily.START_MARKER + previous_reading + daily.END_MARKER
        )
        daily.publish_daily_reading(self.root, today=date(2026, 10, 20))
        self.assertIn(
            b"Meditations is complete", self.readme_path.read_bytes()
        )
        final_state = corpus.read_json_file(self.root / daily.PROGRESS_PATH)
        self.assertEqual(final_state["next_index"], len(self.passages))
        completed_files = self._snapshot_publication()
        daily.publish_daily_reading(self.root, today=date(2026, 10, 21))
        self.assertEqual(completed_files, self._snapshot_publication())

    def test_source_audit_detects_new_format_differences(self) -> None:
        """An altered HTML word cannot hide among reviewed differences."""
        html_source = (self.root / audit_source.HTML_SOURCE_PATH).read_text()
        original_differences = audit_source.compare_source_formats(
            self.source, html_source
        )
        self.assertEqual(len(original_differences), 11)
        changed_html = html_source.replace(
            "From my grandfather Verus", "From my grandfather Someone", 1
        )
        changed_differences = audit_source.compare_source_formats(
            self.source, changed_html
        )
        self.assertEqual(len(changed_differences), 12)
        self.assertEqual(changed_differences[0]["book"], 1)
        self.assertEqual(changed_differences[0]["section"], 1)
        with self.assertRaises(ValueError):
            audit_source.parse_html_sections(
                html_source.replace("<h2>VI.</h2>", "", 1)
            )

    def test_local_footnotes_cannot_be_detached(self) -> None:
        """A standalone section with a later note fails the footnote audit."""
        first_section = corpus.parse_sections(self.source)[0]
        detached_reading = dict(self.passages[0], end=first_section["end"])
        with self.assertRaises(ValueError):
            audit_source.verify_footnotes(self.source, [detached_reading])
        audit_source.verify_footnotes(self.source, self.passages)


if __name__ == "__main__":
    unittest.main()
