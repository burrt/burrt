# Third-party notices

The repository's [MIT license](LICENSE) applies to its original software and
documentation. It does not relicense the book, its transcription, or the
third-party tools listed below.

## Meditations

*Thoughts of Marcus Aurelius Antoninus*, translated by George Long,
[Project Gutenberg ebook 15877](https://www.gutenberg.org/ebooks/15877).
The ebook credits Juliet Sutherland, Turgut Dincer, Leonard Johnson, and
the Online Distributed Proofreading Team.

Project Gutenberg lists this edition as public domain in the USA. That status
does not establish its copyright status in every country. Redistribution
with the Project Gutenberg name is subject to the terms included in the ebook.

The frozen [plain text](philosophy/sources/meditations-george-long-gutenberg.txt)
and [HTML](philosophy/sources/meditations-george-long-gutenberg.html) contain
their complete original notices and Project Gutenberg license. Both are
distributed unchanged and without charge. The README presents exact extracts
of the plain text, with reversible HTML escaping for display, and links to the
complete original ebook and license.

The incomplete MIT Internet Classics Archive download is a local reference
only and is excluded from Git. No permission to redistribute that archive's
additional material is asserted.

## Development and CI tools

These tools are referenced or installed by the workflows; their code and
binaries are not vendored in this repository:

- [actions/checkout](https://github.com/actions/checkout/blob/v7.0.1/LICENSE):
  MIT license.
- [Ruff](https://github.com/astral-sh/ruff/blob/0.17.1/LICENSE):
  MIT license, with additional bundled third-party notices in its distribution.

Python's standard library is used at runtime; no third-party Python runtime
packages or external AI services are required.
