"""Simulate future publication dates in a disposable copy of the repository."""

import argparse
import shutil
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

import corpus
import daily


def _snapshot_publication(root: Path) -> tuple[bytes, bytes]:
    """Read the two files that a publication may change."""
    readme = (root / "README.md").read_bytes()
    progress = (root / daily.PROGRESS_PATH).read_bytes()
    return readme, progress


def simulate(
    root: Path = corpus.REPOSITORY_ROOT,
    days: Optional[int] = 3,
    preview: bool = False,
) -> list[str]:
    """Exercise future publications without modifying the working repository.

    Args:
        root: Repository containing the current reading and frozen corpus.
        days: Number of future readings to simulate, or None for all remaining.
        preview: Include the next reading's exact text in the output.

    Returns:
        A concise report of dates, readings, reruns, and completion checks.

    Raises:
        ValueError: The current repository is invalid or days is not positive.
        RuntimeError: Publication skips a reading or a rerun changes files.
    """
    if days is not None and days < 1:
        raise ValueError("The number of days must be positive")
    daily.publish_daily_reading(root, check_only=True)
    original_files = _snapshot_publication(root)
    source, passages, _ = corpus.load_corpus(root)
    state = corpus.read_json_file(root / daily.PROGRESS_PATH)
    initial_index = state["next_index"]
    remaining_count = len(passages) - initial_index
    day_count = remaining_count if days is None else min(days, remaining_count)
    last_date = state["last_published_date"]
    first_date = (
        date.fromisoformat(last_date) + timedelta(days=1)
        if last_date is not None
        else datetime.now(daily.PUBLICATION_TIMEZONE).date()
    )
    report = [
        f"Starting at reading {initial_index} of {len(passages)}.",
        "Using a temporary copy; no Git commands or network calls.",
    ]

    with tempfile.TemporaryDirectory(
        prefix="meditations-simulation-"
    ) as folder:
        simulation_root = Path(folder)
        for directory in ("sources", "data", "state"):
            relative_path = Path("philosophy") / directory
            shutil.copytree(
                root / relative_path, simulation_root / relative_path
            )
        shutil.copyfile(root / "README.md", simulation_root / "README.md")

        for offset in range(day_count):
            simulated_date = first_date + timedelta(days=offset)
            daily.publish_daily_reading(simulation_root, today=simulated_date)
            saved_state = corpus.read_json_file(
                simulation_root / daily.PROGRESS_PATH
            )
            expected_index = initial_index + offset + 1
            expected_passage = passages[expected_index - 1]
            if (
                saved_state["next_index"] != expected_index
                or saved_state["passage_id"] != expected_passage["id"]
            ):
                raise RuntimeError("Simulation skipped or repeated a reading")

            published_files = _snapshot_publication(simulation_root)
            daily.publish_daily_reading(simulation_root, today=simulated_date)
            if _snapshot_publication(simulation_root) != published_files:
                raise RuntimeError("A same-date rerun changed publication")

            if offset < 3 or offset == day_count - 1:
                report.append(
                    f"{simulated_date}: reading {expected_index} — "
                    f"{expected_passage['id']}; rerun unchanged."
                )
            elif offset == 3:
                report.append("...")

        if initial_index + day_count == len(passages):
            completed_files = _snapshot_publication(simulation_root)
            next_date = first_date + timedelta(days=day_count)
            daily.publish_daily_reading(simulation_root, today=next_date)
            if _snapshot_publication(simulation_root) != completed_files:
                raise RuntimeError("Publication changed after completion")
            report.append(
                "End of book: next-day run leaves both files unchanged."
            )

    if _snapshot_publication(root) != original_files:
        raise RuntimeError("The real README or progress changed")
    report.append(
        f"PASS: {day_count} future readings and same-date reruns verified. "
        "Real README and progress unchanged."
    )
    if preview and remaining_count:
        next_passage = passages[initial_index]
        report.extend(
            [
                "",
                f"Next reading preview: {next_passage['id']}",
                source[next_passage["start"] : next_passage["end"]].decode(
                    "utf-8"
                ),
            ]
        )
    return report


def main() -> None:
    """Run a short or complete simulation from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    duration = parser.add_mutually_exclusive_group()
    duration.add_argument("--days", type=int, default=3, help="Defaults to 3.")
    duration.add_argument(
        "--all", action="store_true", help="Simulate all remaining readings."
    )
    parser.add_argument(
        "--preview", action="store_true", help="Also print the next reading."
    )
    arguments = parser.parse_args()
    try:
        days = None if arguments.all else arguments.days
        print("\n".join(simulate(days=days, preview=arguments.preview)))
    except (ValueError, RuntimeError, OSError, KeyError, TypeError) as error:
        parser.exit(1, f"Simulation stopped: {error}\n")


if __name__ == "__main__":
    main()
