"""Typed records stored in the reading plan, catalog, and progress files."""

from typing import Optional, TypedDict


class Section(TypedDict):
    """A numbered source section and its exclusive byte range."""

    book: int
    section: int
    start: int
    end: int


class ReadingGroup(TypedDict):
    """Adjacent sections that the editorial review keeps together."""

    book: int
    first: int
    last: int
    reason: str


class ReadingPlan(TypedDict):
    """Reviewed merges; unspecified sections remain separate readings."""

    groups: list[ReadingGroup]


class Passage(TypedDict):
    """One immutable reading, identified by source offsets and checksum."""

    id: str
    book: int
    first: int
    last: int
    start: int
    end: int
    sha256: str


class Catalog(TypedDict):
    """The complete reading sequence for one frozen source."""

    source: str
    source_sha256: str
    passages: list[Passage]


class ProgressState(TypedDict):
    """Position and publication date tied to a specific catalog version."""

    catalog_sha256: str
    next_index: int
    last_published_date: Optional[str]
    passage_id: Optional[str]
