# Sources and accuracy

## Selected source: Project Gutenberg

- Work: *Thoughts of Marcus Aurelius Antoninus* (*Meditations*)
- Translator: George Long
- Provider: Project Gutenberg, ebook 15877
- Landing page: https://www.gutenberg.org/ebooks/15877
- Text download: https://www.gutenberg.org/ebooks/15877.txt.utf-8
- HTML download: https://www.gutenberg.org/cache/epub/15877/pg15877-images.html
- Retrieved: 2026-10-20
- Text file: `meditations-george-long-gutenberg.txt` (451,715 bytes)
- HTML file: `meditations-george-long-gutenberg.html` (555,877 bytes)
- Text encoding: UTF-8; original CRLF line endings
- Ebook's stated last update: December 14, 2020

Both downloads are frozen HTTP response bodies, saved without text processing.
The original license notices, introductions, indexes, notes and all text
markings remain in the snapshots. The repository's software license does not
replace the notices supplied with these source files. See
[third-party notices](../../THIRD_PARTY_NOTICES.md) for attribution and terms.

The reading corpus uses the numbered sections of the twelve books from the
text file. Each reading stores byte offsets and a checksum, not rewritten text.
Translator notes and publisher illustration placeholders within those ranges
are retained. Introduction, indexes, book headings, and surrounding blank lines
are outside the daily reading ranges but remain in the original ebook.

All 487 numbered sections received an AI editorial review for grouping and
local footnote attachment. They produce 437 readings, with no fixed word count.
The [reading plan](../data/reading-plan.json) records every grouping decision;
the [review record](../data/source-review.json) records the findings.
The HTML snapshot provides a separate structural check of the text extraction,
but is another format of the same ebook, not an independent historical witness.

An offline comparison checks all 487 section bodies, excluding notes and
illustrations and normalizing only presentation conventions in comparison
copies. Eleven differences remain, including Greek versus transliteration,
spacing, punctuation, `enioyment` versus `enjoyment` in III.6, and an additional
sentence in the plain text of XI.6. The
[comparison review](../data/source-comparison.json) records every difference
and pins both compared texts by checksum. The selected plain text is preserved
throughout; the audit does not merge the formats or correct discrepancies.

### What accuracy means here

The automated checks establish exact fidelity to the frozen text snapshot.
They verify source hashes, section numbering, contiguous coverage of each book,
every reading's offsets and checksum, and the README content against its source
slice. Markdown quote prefixes, escapes, and collapsible note wrappers are
presentation additions. Reversing them and joining all blocks in source order
is verified to recover the original bytes. The browser wraps prose naturally and may collapse source whitespace;
the linked source retains the original layout.

AI review cannot certify that the ebook's transcription or translation is
error-free. Apparent anomalies remain unchanged, including `who snowed` in
V.15, the potentially consequential `not` in VI.41, and the reference to
VII.85 in X.26 even though Book VII has 75 sections. The full review record
lists other findings.

Some passages are incomplete in the source and the translator explicitly
discusses corrupt or uncertain underlying text. XI.28 and XI.30–32 are short
fragments whose missing context cannot be supplied by grouping nearby sections.
They are preserved without invented connective wording. The source's `+`,
ellipses, brackets, underscores, transliterated Greek, and illustration captions
are intentional parts of the frozen text contract.

Do not silently correct, modernize, normalize, or combine different editions.
Changing editions requires a separately reviewed source and a new reading plan,
not patching the existing snapshot.

## Rejected corpus candidate: MIT

- File: `meditations-george-long-mit.txt`
- Work: *The Meditations*, Marcus Aurelius
- Translator credited by the source: George Long
- Provider: The Internet Classics Archive
- Landing page: https://classics.mit.edu/Antoninus/meditations.html
- Raw download: https://classics.mit.edu/Antoninus/meditations.mb.txt
- Retrieved: 2026-10-20
- Size: 244,067 bytes
- Encoding observed: ASCII; LF line endings
- Status: **Known incomplete; not approved as the daily-reading corpus.**

The HTTP response body was saved without text processing. The original
whitespace, line wrapping, spelling, punctuation, header, and copyright
statement are preserved. The repository's `.gitattributes` disables Git
line-ending conversion for this file.

### Source-quality finding

Book XII stops mid-sentence before `THE END`. The corresponding
[MIT HTML page](https://classics.mit.edu/Antoninus/meditations.12.twelve.html)
has the same cutoff.

The corresponding passage is numbered XII.27 in
[Project Gutenberg's George Long edition](https://www.gutenberg.org/cache/epub/15877/pg15877-images.html).
That edition continues the sentence and includes XII.28 through XII.36.
This comparison establishes an omission in the MIT source; it is not a
complete audit of either edition.

This download is retained unchanged locally as a reference, excluded from Git,
and never used by the daily publisher. It is not redistributed with this
repository; its archive-specific rights notice has not been relicensed. Gutenberg supplies the selected corpus in its entirety;
the two editions have not been spliced together.

## Verify the saved bytes

From this directory, run:

```sh
shasum -a 256 -c SHA256SUMS
```

This verifies fidelity to both distributed Gutenberg snapshots. It does not prove
that a provider's transcription matches a printed edition.
