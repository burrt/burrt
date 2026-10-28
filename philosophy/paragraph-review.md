# Paragraph and daily-reading review

Reviewed on 2026-10-28. This is an AI-assisted editorial review, with separate
reviews of paragraph choices, daily boundaries, and rendering integrity. It is
not a scholarly certification of the Greek text or the translations.

The decision is to add a small set of explicit paragraph breaks to long prose
blocks while retaining the 437 daily readings and their order. The source
wording, punctuation, notes, catalog, and saved publication position stay intact.

## Evidence and method

The principal comparison is A. S. L. Farquharson's 1944 Oxford edition, using
the scan-backed [text and commentary on Wikisource](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus).
C. R. Haines's 1916 Loeb edition provides a second comparison, also through
[its scan-backed transcription](https://en.wikisource.org/wiki/Marcus_Aurelius_(Haines_1916)).
These are established scholarly editions, not a claim that one translation is
objectively the best. Their divisions inform our judgment; they are not rules
to transfer mechanically into George Long's different sentence structure.

Gregory Hays's shorter units were considered in the initial comparison. This
implementation does not claim a complete review of his printed edition, or use
unverified online reproductions as the authority for individual breaks. No
wording from another translation is inserted into Long's text.

All 437 readings were screened for existing paragraph lengths. The 18 visible
prose blocks of at least 300 whitespace-delimited words received closer review.
The length screen selected candidates, not break positions. Each accepted break
must follow a complete sentence in Long, introduce a useful shift of thought,
and leave an argument and its examples understandable in sequence. No automatic
sentence splitter, target paragraph length, new heading, or added summary is
used. Existing paragraphs, verse, and translator notes retain their layout.

The exact approved sentence beginnings live in
[scripts/paragraphs.py](scripts/paragraphs.py). Matching is literal, unique,
and ordered. Publication fails if an anchor disappears, becomes ambiguous,
does not follow sentence-ending punctuation, or falls inside a translator note
or indented text. Sentence completeness itself was checked editorially; a
punctuation check alone cannot establish it.

## Paragraph decisions

These are our editorial readings of the argument, checked against the cited
translations. They do not claim to reproduce Marcus's manuscript layout.
The counts below describe the candidate source paragraph after the change;
other existing paragraphs in that section remain as they were.

| Section | Decision | Reason for the chosen divisions |
| --- | --- | --- |
| I.16 | 9 paragraphs | Core virtues; friendship; careful government; comfort; philosophy and health; support of talent; steady work; daily simplicity; concluding self-command. The Socrates and Maximus examples stay with the conclusion. |
| I.17 | 3 paragraphs | Family and restraint; upbringing under a modest ruler; the remaining thanks. The final 420-word sentence stays intact: breaking its semicolon list would exceed this conservative policy. |
| III.2 | Retain | Natural examples and the perception of beauty form one continuous movement. Being just over the screening threshold does not itself justify a change. |
| III.4 | 4 paragraphs | Warning about idle speculation; the test for benevolent thoughts; the positive portrait and proper work; kinship without dependence on unwise praise. |
| III.6 | 3 paragraphs | The opening challenge; its converse concerning rational and social good; practical choice. The long conditional and the human/animal distinction remain intact. |
| III.11 | 3 paragraphs | Defining the object; the value of examination and appropriate virtue; application. This stays within the existing III.9–11 reading. |
| IV.3 | 3, then the existing conclusion | Inner retreat; renewal; diagnoses of discontent. Long's dash-linked objections and answers remain together, followed by his existing concluding paragraph. |
| V.1 | 2 paragraphs | The dialogue about rising and rest; self-love and devotion to one's work. The final social-duty question stays with the comparison to other crafts. |
| V.8 | 4 paragraphs | Prescription analogy; fitting parts and causes; acceptance; two concluding reasons. Both reasons and their explanation remain together. |
| VI.16 | 3 paragraphs | Biological functions and applause; positive value in proper action; consequences of external attachments and the alternative of honouring the mind. |
| VI.30 | 2 paragraphs | Instruction about imperial character; Antoninus as the worked example, including the closing invitation to imitate him. |
| IX.1 | 5 paragraphs | Injustice; falsehood; pleasure and pain; indifference; clarification about universal nature. Related premises and examples remain connected. |
| IX.3 | 2 paragraphs | Death as a natural operation; supplementary consolation. The instruction to care for people remains with the latter. |
| IX.9 | 3 paragraphs | Material affinity; higher analogues in intelligence and society; humans' apparent separation and continuing connection. |
| IX.42 | 4 paragraphs | Expect imperfect people; exercise the appropriate virtue; examine harm and expectations; give service without seeking repayment. The eye/foot analogy stays with that last argument. |
| X.7 | 3 paragraphs | Change within the whole; the alternative description without personifying Nature; bodily renewal. The uncertain ending stays attached to its explanation and note. |
| X.8 | 4 paragraphs | Define virtues; the corresponding life and its opposite; resolve; remembering through characteristic work. Conditions and examples remain attached. X.9 stays in the same daily reading. |
| X.33 | 4 paragraphs | Appropriate action; physical/rational contrast; using obstacles; civic criterion of harm. The concluding law/state/citizen inference stays together. |

Comparison text by book:
[Farquharson I](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Book_1),
[III](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Book_3),
[IV](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Book_4),
[V](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Book_5),
[VI](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Book_6),
[IX](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Book_9),
[X](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Book_10).

The same sections were cross-checked in
[Haines I](https://en.wikisource.org/wiki/Marcus_Aurelius_(Haines_1916)/Book_1),
[III](https://en.wikisource.org/wiki/Marcus_Aurelius_(Haines_1916)/Book_3),
[IV](https://en.wikisource.org/wiki/Marcus_Aurelius_(Haines_1916)/Book_4),
[V](https://en.wikisource.org/wiki/Marcus_Aurelius_(Haines_1916)/Book_5),
[VI](https://en.wikisource.org/wiki/Marcus_Aurelius_(Haines_1916)/Book_6),
[IX](https://en.wikisource.org/wiki/Marcus_Aurelius_(Haines_1916)/Book_9),
[X](https://en.wikisource.org/wiki/Marcus_Aurelius_(Haines_1916)/Book_10).
There is no uniform agreement about exact paragraph positions. For example,
Farquharson more distinctly marks the positive-value turn in VI.16 and the
shared-intelligence turn in IX.9; Haines groups those portions differently.
X.33's final civic paragraph follows Long's explicit concluding turn, while
Haines keeps that inference in a larger paragraph. The accepted breaks remain
our editorial judgments, rather than a claim of consensus at every position.

I.16 illustrates the restraint used throughout. Haines and Farquharson separate
equivalent topics, but some of their divisions fall inside one of Long's
sentences. We keep that sentence together, even when a resulting paragraph
remains relatively long. This is why the layout is not an exact copy of either
edition, and why I.17's final sentence and IV.3's linked dialogue stay long.
[Haines I](https://en.wikisource.org/wiki/Marcus_Aurelius_(Haines_1916)/Book_1)

A second editorial pass moved the proposed III.6 break from “All these things”
to “But do thou”. This keeps the warning about rival goods beside its referent
and places the break at the practical choice it actually introduces.

## Daily boundaries

The separate boundary audit inspected the openings, endings, and visible prose
lengths of all 487 numbered sections; reread all 26 merged groups with their
notes; and reread apparent dependencies and fragments. Relevant Farquharson
commentary was consulted for Books I–V and X–XII. This was a targeted context
review, not a line-by-line comparison of every section in multiple translations.

There is no sufficiently clear improvement to justify changing a daily boundary:

- **I.16** is one cumulative portrait of Antoninus Pius, moving from public
  conduct to private habits and balanced self-command. **I.17** is one
  thanksgiving. Keeping each together preserves its purpose despite its length.
  [Farquharson, commentary on Book I](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Commentary_on_Book_1)
- **XI.18** is a connected sequence of remedies for anger, followed by the
  return to the nine gifts and a tenth. Its existing paragraphs already expose
  much of this structure; it should remain one reading.
  [Commentary on Book XI](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Commentary_on_Book_11)
- **III.9–11, IV.9–10, IV.14–15, and IV.25–26** have contextual support in
  Farquharson's discussion. In particular, he notes that IV.14–15 are combined
  in the manuscripts and that the second illustrates the first.
  [Book III commentary](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Commentary_on_Book_3),
  [Book IV commentary](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Commentary_on_Book_4)
- **V.12–15 and V.17–20** retain useful thematic sequences. Those themes also
  extend to surrounding sections, so these are defensible daily selections,
  rather than uniquely established divisions.
  [Book V commentary](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Commentary_on_Book_5)
- Fifteen groups chiefly preserve local translator-note attachment. Some,
  including **VII.35–40 and XI.22–26**, contain several distinct examples.
  Their justification is keeping source text and its notes together, rather
  than claiming that every daily reading expresses exactly one thesis.

There are reservations. **II.3–4** spans a pause recognised by Farquharson,
although providence and using the time available make a reasonable daily
reflection. **IV.28–29** is a weaker editorial pairing: Farquharson treats
IV.28 as an interruption and connects IV.29–30. Our pairing juxtaposes defective
character with separation from reason and society, but it is not a dependency
established by those editions. Neither case clearly requires repartitioning.
[Book II commentary](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Commentary_on_Book_2),
[Book IV commentary](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Commentary_on_Book_4)

Extending IV.28–29 to include IV.30 was specifically debated in the independent
review. Farquharson connects IV.29–30 as a contrast, so the larger grouping is
a reasonable alternative: material poverty need not imply the dependence
criticised in IV.29. One reviewer mildly preferred that juxtaposition. However,
IV.30's philosopher examples already
illustrate holding to reason despite poverty; IV.29 does not supply a missing
antecedent. Long also marks the ending uncertain, and translates it differently
from Farquharson. A merger would not resolve that problem. The final decision
is to retain the existing boundaries and disclose the uncertainty, rather than
present the broader grouping as necessary or reconstruct Long's wording.

Some source fragments have no recoverable complete lesson. **XI.28** refers to
a lost answer, and **XI.30–32** contain obscure quotations. Combining neighbours
would not restore their missing context. The existing
[source notes](sources/README.md) continue to disclose these limits.
[Book XI commentary](https://en.wikisource.org/wiki/The_Meditations_of_the_Emperor_Marcus_Antoninus/Commentary_on_Book_11)

Splitting by word count, merging unrelated short passages, or copying another
translation's divisions wholesale was rejected. Paragraphs give readers places
to pause while the original daily argument remains available in full.

## Integrity and publication

Paragraph boundaries are presentation additions. Each exact source slice is
rendered in order, retaining its original spaces, indentation, and CRLF bytes.
Removing Markdown quote prefixes and escapes and joining the quote blocks
recovers the complete original passage byte-for-byte, including hidden notes.
Affected readings link here so the additions are distinguishable from Long's
source paragraphing.

The archive is regenerated with the same renderer. Today's README is refreshed
from its saved passage and publication date, without invoking publication or
advancing progress. One reading per London date, same-date reruns, missed days,
and completion retain their existing behaviour.

Validation on the final rendering change:

- All 20 unit tests, the independent source audit, daily check, archive check,
  and pinned Ruff checks passed.
- A separate CommonMark parse of the old and new output found exactly 44
  additional paragraphs across 17 archive pages. All 437 parsed quote sequences
  and the README's quoted text were unchanged.
- Frozen text and HTML, reading plan, catalog, and progress were compared with
  the original Git revision and remained byte-identical. Today's saved reading
  remains number 9, dated 2026-10-28.
- The temporary-copy simulation passed all 428 remaining readings, same-date
  reruns, and the no-change run after completion. The real README and progress
  were unchanged by simulation.
