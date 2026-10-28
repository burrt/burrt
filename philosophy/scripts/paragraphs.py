"""Apply reviewed paragraph starts without changing source bytes."""

import re

# Each anchor is an exact, unique beginning of a reviewed source sentence.
# The editorial evidence and reasons belong in philosophy/paragraph-review.md.
PARAGRAPH_STARTS: dict[str, tuple[bytes, ...]] = {
    "meditations-long-01-016-016": (
        b"And I observed that he had overcome",
        b"I\r\nobserved too his habit",
        b"And the things\r\nwhich conduce",
        b"Besides this,\r\nhe honored",
        b"He was most\r\nready to give",
        b"Further, he was not fond",
        b"He did not take the bath",
        b"There was in him nothing harsh",
    ),
    "meditations-long-01-017-017": (
        b"Further, I am\r\nthankful",
        b"I thank the gods for giving me",
    ),
    "meditations-long-03-004-004": (
        b"We ought then to check",
        b"For the man who is such",
        b"And he remembers also",
    ),
    "meditations-long-03-006-006": (
        b"But if nothing appears",
        b"But do thou, I\r\nsay, simply and freely choose the better",
    ),
    "meditations-long-03-009-011": (
        b"For nothing is so\r\nproductive",
        b"Wherefore, on every occasion",
    ),
    "meditations-long-04-003-003": (
        b"Constantly then give",
        b"For with what art\r\nthou discontented",
    ),
    "meditations-long-05-001-001": (b"So thou lovest not thyself",),
    "meditations-long-05-008-008": (
        b"For this is what we mean",
        b"Let us then receive these things",
        b"For two reasons then",
    ),
    "meditations-long-06-016-016": (
        b"Suppose then that thou hast given up",
        b"Wilt thou not cease to value",
    ),
    "meditations-long-06-030-030": (b"Do everything\r\nas a disciple",),
    "meditations-long-09-001-001": (
        b"And he too who lies",
        b"And indeed he who pursues pleasure",
        b"Now with respect to the things",
        b"And I say that the universal",
    ),
    "meditations-long-09-003-003": (b"But if thou requirest also",),
    "meditations-long-09-009-009": (
        b"Accordingly, then, everything also",
        b"See, then, what now takes place",
    ),
    "meditations-long-09-042-042": (
        b"It is useful\r\nto perceive this",
        b"Besides,\r\nwherein hast thou",
        b"But most of all when thou blamest",
    ),
    "meditations-long-10-007-007": (
        b"But if a man should even drop",
        b"And do not imagine",
    ),
    "meditations-long-10-008-009": (
        b"If, then, thou maintainest",
        b"Therefore fix thyself",
        b"In order, however to the\r\nremembrance",
    ),
    "meditations-long-10-033-033": (
        b"Now, it is not given to a cylinder",
        b"Place before thy eyes this\r\nfacility",
        b"And finally remember",
    ),
}


def split_paragraphs(
    blocks: list[tuple[bool, bytes]], passage_id: str
) -> list[tuple[bool, bytes]]:
    """Separate reviewed prose sentences while retaining all source whitespace.

    Args:
        blocks: Source-order blocks marked True for translator notes.
        passage_id: Identifier of the existing, unchanged daily reading.

    Returns:
        Source-order blocks with the reviewed visible paragraph divisions.

    Raises:
        ValueError: An anchor is missing, ambiguous, unordered, or unsuitable.
    """
    anchors = PARAGRAPH_STARTS.get(passage_id, ())
    if not anchors:
        return blocks

    original_text = b"".join(content for _, content in blocks)
    offsets = []
    for anchor in anchors:
        if not isinstance(anchor, bytes) or not anchor or anchor[:1].isspace():
            raise ValueError("Paragraph anchors must start with source text")
        if original_text.count(anchor) != 1:
            raise ValueError("Paragraph anchors must occur exactly once")
        offset = original_text.index(anchor)
        if offset == 0 or (offsets and offset <= offsets[-1]):
            raise ValueError("Paragraph anchors must follow source order")
        preceding_text = original_text[:offset]
        if not preceding_text[-1:].isspace() or not re.search(
            rb"""[.!?](?:\[[A-Z]\]|["')\]+])*$""",
            preceding_text.rstrip(),
        ):
            raise ValueError("Paragraphs must start after complete sentences")
        if re.search(rb"\r?\n[ \t]*\r?\n[ \t]*$", preceding_text):
            raise ValueError("A source paragraph already starts here")
        paragraph_prefix = re.split(rb"\r?\n[ \t]*\r?\n", preceding_text)[-1]
        if paragraph_prefix.startswith(b"    "):
            raise ValueError(
                "Editorial paragraphs cannot divide indented text"
            )
        offsets.append(offset)

    paragraphs: list[tuple[bool, bytes]] = []
    block_start = 0
    for is_note, content in blocks:
        block_end = block_start + len(content)
        contained_offsets = [
            offset for offset in offsets if block_start <= offset < block_end
        ]
        if contained_offsets and (
            is_note or contained_offsets[0] == block_start
        ):
            raise ValueError("Paragraph anchors must be inside visible prose")
        starts = [0] + [offset - block_start for offset in contained_offsets]
        ends = starts[1:] + [len(content)]
        paragraphs.extend(
            (is_note, content[start:end]) for start, end in zip(starts, ends)
        )
        block_start = block_end

    if b"".join(content for _, content in paragraphs) != original_text:
        raise ValueError("Separating paragraphs changed source text")
    return paragraphs
