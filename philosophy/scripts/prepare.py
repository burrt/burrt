"""Build or check passage metadata without writing to the source files."""

import argparse
import json

import corpus
from models import ReadingPlan


def main() -> None:
    """Run the offline corpus preparation command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the existing catalog without writing files.",
    )
    arguments = parser.parse_args()

    if arguments.check:
        _, passages, _ = corpus.load_corpus()
    else:
        corpus.verify_sources()
        root = corpus.REPOSITORY_ROOT
        source = (root / corpus.SOURCE_PATH).read_bytes()
        reading_plan: ReadingPlan = corpus.read_json_file(
            root / corpus.READING_PLAN_PATH
        )
        catalog = corpus.build_catalog(source, reading_plan)
        catalog_json = json.dumps(catalog, indent=2) + "\n"
        (root / corpus.CATALOG_PATH).write_text(catalog_json, encoding="utf-8")
        passages = catalog["passages"]

    print(f"Validated 12 books, 487 sections, {len(passages)} readings.")


if __name__ == "__main__":
    main()
