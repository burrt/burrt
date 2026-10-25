# Meditations reading plan

437 readings cover all 487 numbered sections of the twelve books, in order.
Reading numbers open formatted passages with ← and → navigation.
The original-text links open the exact source lines, including the edition's notes.
Readings vary in length; no numbered section has been split.

## Operation

The daily GitHub Action runs at **06:17 Europe/London**, with daylight saving
handled by the schedule timezone. GitHub can delay or drop scheduled runs.
A missed day resumes at the next unread passage; it does not skip text or
publish a backlog. Running the action again on the same date changes nothing.
After the last passage, the final reading stays in place and publication stops.

The workflow runs from the default branch. It uses one standard Ubuntu job
with a five-minute timeout, Python's standard library, and the built-in
`GITHUB_TOKEN`. No API key, AI service, package installation, source download,
artifact storage, or cache is needed. README and progress are pushed in one
commit, and concurrent publishing runs are serialized. A racing external push
is rejected normally; rerunning the action safely retries.

Automated commits use Geoffrey Choy's name and GitHub no-reply address, supplied through
`GIT_AUTHOR_*` and `GIT_COMMITTER_*` environment variables in the commit step.
The workflow does not change local or runner Git configuration. Hosted runners
do not inherit the Git configuration on your laptop; the identity is explicit
in the workflow. Commit messages identify these updates as automated.
The built-in GitHub token still authenticates the push.

For your own local commits, configure the same public no-reply address in this
repository before committing (this does not change your global settings):

```sh
git config --local user.email "2559677+burrt@users.noreply.github.com"
```

Your name remains public for attribution. Changing the address does not remove
email addresses from earlier commits.

The repository was verified public on 2026-10-20. Standard hosted runners are
[free for public repositories](https://docs.github.com/en/billing/concepts/product-billing/github-actions).
For a private repository, GitHub Free includes 2,000 minutes per month across
the owner's repositories. A 1–3 minute daily job would use roughly 31–93 minutes
in a 31-day month; this is an estimate, not a measured hosted runtime.
The five-minute timeout caps the daily job at approximately 155 minutes per
31-day month, excluding manual runs and validation triggered by development.
There is no separate daily minute allowance.

Scheduled workflows can be disabled after 60 days without repository activity.
Normal daily commits keep this project active; after a long failure or at the
end of the corpus, the schedule may need re-enabling.
[GitHub schedule documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

## Local commands

Requires Python 3.9 or newer with IANA timezone data (provided by the configured
Ubuntu runner). Run from the repository root:

```sh
python3 -m unittest discover -s philosophy/tests
python3 philosophy/scripts/audit_source.py
python3 philosophy/scripts/daily.py --check
python3 philosophy/scripts/archive.py --check
```

To simulate three future readings and preview the next one:

```sh
python3 philosophy/scripts/simulate.py --days 3 --preview
```

To repeat the complete lifecycle simulation:

```sh
python3 philosophy/scripts/simulate.py --all
```

The simulator copies the required files into a temporary directory, advances
mock dates from the current reading, and retries each date to check that it
does not advance twice. A complete simulation also verifies that publication
stops after the final reading. It performs no Git commands or network calls,
removes its temporary copy, and verifies that the real README and progress
are unchanged.

To publish the next reading locally for today's London date:

```sh
python3 philosophy/scripts/daily.py
```

This changes only the reading between the root README markers and
`philosophy/state/progress.json`. Commit those files together.

Corpus preparation is a separate, offline operation:

```sh
python3 philosophy/scripts/prepare.py --check
```

`prepare.py` without `--check` regenerates passage metadata from the frozen
source and reviewed plan. It never writes source text. Changing the catalog
invalidates existing progress so a new reading order cannot silently reuse
the old position.

To rebuild the formatted archive after an intentional rendering or catalog
change, run `python3 philosophy/scripts/archive.py`. This does not advance
the daily reading or modify the frozen source. The first reading has no back
arrow; subsequent daily readings link directly to the previous archive entry.

## Verification

Every daily run verifies all source checksums and reconstructs the catalog
from the numbered sections and reviewed grouping plan. Joining the slices
must reproduce each complete book body byte-for-byte, with no gaps or overlap.
Every passage has its own SHA-256 checksum. The current and proposed README
readings must match the exact source slice after reversing Markdown and HTML escapes.
Markdown blockquotes let prose wrap naturally. Markdown escaping prevents
Markdown from renumbering sections or interpreting the edition's text markings.
Removing quote prefixes and reversing escapes recovers the original bytes,
including line endings and indentation; browser layout may collapse whitespace.
Translator note definitions and their indented continuation paragraphs appear
in collapsed **Translator notes** sections on every daily reading. Inline
references and bracketed prose remain visible. Notes stay in source order, and
joining the visible and collapsible blocks recovers the entire source slice.
Readings without notes have no extra collapsible section.

Progress validation rejects changed catalogs, invalid indexes or dates,
missing or repeated README markers, and edited reading content. The workflow
does not commit if a check fails. Tests exercise corruption, reruns, skipped
days, formatting and exhaustion.

The offline audit independently extracts all twelve books and 487 section
numbers from the frozen HTML edition. It compares section bodies after
documented presentation-only normalization and checks that every local footnote
reference has a definition in the same reading. Eleven differences between the
HTML and text formats were reviewed and recorded with exact comparison hashes
in [source-comparison.json](data/source-comparison.json). An unexpected
difference fails the audit. Comparison normalization never changes source files
or published readings.

An AI review selected boundaries and flagged source anomalies. It did not
rewrite the text or certify historical transcription accuracy. See the
[source notes](sources/README.md) and [full review record](data/source-review.json).

## Python style

The scripts use descriptive names, type hints, PEP 8 layout, and Google-style
docstrings. Ruff checks imports, basic correctness, docstrings, and formatting.
The separate validation workflow runs these checks on code changes; the daily
publisher has no third-party dependencies.

For local development:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/ruff check philosophy
.venv/bin/ruff format --check philosophy
```

## Readings

<!-- READING-INDEX -->

<details>

<summary>Book I</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [1](readings/book-01.md#reading-1) | I.1–4 | [Read](sources/meditations-george-long-gutenberg.txt#L2132-L2165) |
| [2](readings/book-01.md#reading-2) | I.5 | [Read](sources/meditations-george-long-gutenberg.txt#L2165-L2172) |
| [3](readings/book-01.md#reading-3) | I.6 | [Read](sources/meditations-george-long-gutenberg.txt#L2172-L2194) |
| [4](readings/book-01.md#reading-4) | I.7 | [Read](sources/meditations-george-long-gutenberg.txt#L2194-L2222) |
| [5](readings/book-01.md#reading-5) | I.8 | [Read](sources/meditations-george-long-gutenberg.txt#L2222-L2237) |
| [6](readings/book-01.md#reading-6) | I.9–13 | [Read](sources/meditations-george-long-gutenberg.txt#L2237-L2286) |
| [7](readings/book-01.md#reading-7) | I.14 | [Read](sources/meditations-george-long-gutenberg.txt#L2286-L2310) |
| [8](readings/book-01.md#reading-8) | I.15 | [Read](sources/meditations-george-long-gutenberg.txt#L2310-L2331) |
| [9](readings/book-01.md#reading-9) | I.16 | [Read](sources/meditations-george-long-gutenberg.txt#L2331-L2418) |
| [10](readings/book-01.md#reading-10) | I.17 | [Read](sources/meditations-george-long-gutenberg.txt#L2418-L2488) |

</details>

<details>

<summary>Book II</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [11](readings/book-02.md#reading-11) | II.1 | [Read](sources/meditations-george-long-gutenberg.txt#L2496-L2512) |
| [12](readings/book-02.md#reading-12) | II.2 | [Read](sources/meditations-george-long-gutenberg.txt#L2512-L2523) |
| [13](readings/book-02.md#reading-13) | II.3–4 | [Read](sources/meditations-george-long-gutenberg.txt#L2523-L2544) |
| [14](readings/book-02.md#reading-14) | II.5 | [Read](sources/meditations-george-long-gutenberg.txt#L2544-L2556) |
| [15](readings/book-02.md#reading-15) | II.6 | [Read](sources/meditations-george-long-gutenberg.txt#L2556-L2564) |
| [16](readings/book-02.md#reading-16) | II.7 | [Read](sources/meditations-george-long-gutenberg.txt#L2564-L2571) |
| [17](readings/book-02.md#reading-17) | II.8 | [Read](sources/meditations-george-long-gutenberg.txt#L2571-L2575) |
| [18](readings/book-02.md#reading-18) | II.9 | [Read](sources/meditations-george-long-gutenberg.txt#L2575-L2581) |
| [19](readings/book-02.md#reading-19) | II.10 | [Read](sources/meditations-george-long-gutenberg.txt#L2581-L2596) |
| [20](readings/book-02.md#reading-20) | II.11 | [Read](sources/meditations-george-long-gutenberg.txt#L2596-L2622) |
| [21](readings/book-02.md#reading-21) | II.12 | [Read](sources/meditations-george-long-gutenberg.txt#L2622-L2639) |
| [22](readings/book-02.md#reading-22) | II.13 | [Read](sources/meditations-george-long-gutenberg.txt#L2639-L2654) |
| [23](readings/book-02.md#reading-23) | II.14 | [Read](sources/meditations-george-long-gutenberg.txt#L2654-L2673) |
| [24](readings/book-02.md#reading-24) | II.15 | [Read](sources/meditations-george-long-gutenberg.txt#L2673-L2677) |
| [25](readings/book-02.md#reading-25) | II.16 | [Read](sources/meditations-george-long-gutenberg.txt#L2677-L2693) |
| [26](readings/book-02.md#reading-26) | II.17 | [Read](sources/meditations-george-long-gutenberg.txt#L2693-L2720) |

</details>

<details>

<summary>Book III</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [27](readings/book-03.md#reading-27) | III.1 | [Read](sources/meditations-george-long-gutenberg.txt#L2728-L2744) |
| [28](readings/book-03.md#reading-28) | III.2 | [Read](sources/meditations-george-long-gutenberg.txt#L2744-L2769) |
| [29](readings/book-03.md#reading-29) | III.3 | [Read](sources/meditations-george-long-gutenberg.txt#L2769-L2785) |
| [30](readings/book-03.md#reading-30) | III.4 | [Read](sources/meditations-george-long-gutenberg.txt#L2785-L2825) |
| [31](readings/book-03.md#reading-31) | III.5 | [Read](sources/meditations-george-long-gutenberg.txt#L2825-L2836) |
| [32](readings/book-03.md#reading-32) | III.6 | [Read](sources/meditations-george-long-gutenberg.txt#L2836-L2862) |
| [33](readings/book-03.md#reading-33) | III.7 | [Read](sources/meditations-george-long-gutenberg.txt#L2862-L2879) |
| [34](readings/book-03.md#reading-34) | III.8 | [Read](sources/meditations-george-long-gutenberg.txt#L2879-L2889) |
| [35](readings/book-03.md#reading-35) | III.9–11 | [Read](sources/meditations-george-long-gutenberg.txt#L2889-L2932) |
| [36](readings/book-03.md#reading-36) | III.12 | [Read](sources/meditations-george-long-gutenberg.txt#L2932-L2941) |
| [37](readings/book-03.md#reading-37) | III.13 | [Read](sources/meditations-george-long-gutenberg.txt#L2941-L2949) |
| [38](readings/book-03.md#reading-38) | III.14 | [Read](sources/meditations-george-long-gutenberg.txt#L2949-L2964) |
| [39](readings/book-03.md#reading-39) | III.15 | [Read](sources/meditations-george-long-gutenberg.txt#L2964-L2968) |
| [40](readings/book-03.md#reading-40) | III.16 | [Read](sources/meditations-george-long-gutenberg.txt#L2968-L2989) |

</details>

<details>

<summary>Book IV</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [41](readings/book-04.md#reading-41) | IV.1 | [Read](sources/meditations-george-long-gutenberg.txt#L2997-L3010) |
| [42](readings/book-04.md#reading-42) | IV.2 | [Read](sources/meditations-george-long-gutenberg.txt#L3010-L3013) |
| [43](readings/book-04.md#reading-43) | IV.3 | [Read](sources/meditations-george-long-gutenberg.txt#L3013-L3064) |
| [44](readings/book-04.md#reading-44) | IV.4 | [Read](sources/meditations-george-long-gutenberg.txt#L3064-L3082) |
| [45](readings/book-04.md#reading-45) | IV.5 | [Read](sources/meditations-george-long-gutenberg.txt#L3082-L3088) |
| [46](readings/book-04.md#reading-46) | IV.6 | [Read](sources/meditations-george-long-gutenberg.txt#L3088-L3094) |
| [47](readings/book-04.md#reading-47) | IV.7 | [Read](sources/meditations-george-long-gutenberg.txt#L3094-L3098) |
| [48](readings/book-04.md#reading-48) | IV.8 | [Read](sources/meditations-george-long-gutenberg.txt#L3098-L3101) |
| [49](readings/book-04.md#reading-49) | IV.9–10 | [Read](sources/meditations-george-long-gutenberg.txt#L3101-L3112) |
| [50](readings/book-04.md#reading-50) | IV.11 | [Read](sources/meditations-george-long-gutenberg.txt#L3112-L3116) |
| [51](readings/book-04.md#reading-51) | IV.12 | [Read](sources/meditations-george-long-gutenberg.txt#L3116-L3124) |
| [52](readings/book-04.md#reading-52) | IV.13 | [Read](sources/meditations-george-long-gutenberg.txt#L3124-L3127) |
| [53](readings/book-04.md#reading-53) | IV.14–15 | [Read](sources/meditations-george-long-gutenberg.txt#L3127-L3134) |
| [54](readings/book-04.md#reading-54) | IV.16 | [Read](sources/meditations-george-long-gutenberg.txt#L3134-L3138) |
| [55](readings/book-04.md#reading-55) | IV.17 | [Read](sources/meditations-george-long-gutenberg.txt#L3138-L3141) |
| [56](readings/book-04.md#reading-56) | IV.18 | [Read](sources/meditations-george-long-gutenberg.txt#L3141-L3147) |
| [57](readings/book-04.md#reading-57) | IV.19 | [Read](sources/meditations-george-long-gutenberg.txt#L3147-L3158) |
| [58](readings/book-04.md#reading-58) | IV.20 | [Read](sources/meditations-george-long-gutenberg.txt#L3158-L3171) |
| [59](readings/book-04.md#reading-59) | IV.21 | [Read](sources/meditations-george-long-gutenberg.txt#L3171-L3192) |
| [60](readings/book-04.md#reading-60) | IV.22 | [Read](sources/meditations-george-long-gutenberg.txt#L3192-L3196) |
| [61](readings/book-04.md#reading-61) | IV.23 | [Read](sources/meditations-george-long-gutenberg.txt#L3196-L3203) |
| [62](readings/book-04.md#reading-62) | IV.24 | [Read](sources/meditations-george-long-gutenberg.txt#L3203-L3215) |
| [63](readings/book-04.md#reading-63) | IV.25–26 | [Read](sources/meditations-george-long-gutenberg.txt#L3215-L3227) |
| [64](readings/book-04.md#reading-64) | IV.27 | [Read](sources/meditations-george-long-gutenberg.txt#L3227-L3236) |
| [65](readings/book-04.md#reading-65) | IV.28–29 | [Read](sources/meditations-george-long-gutenberg.txt#L3236-L3251) |
| [66](readings/book-04.md#reading-66) | IV.30 | [Read](sources/meditations-george-long-gutenberg.txt#L3251-L3256) |
| [67](readings/book-04.md#reading-67) | IV.31 | [Read](sources/meditations-george-long-gutenberg.txt#L3256-L3261) |
| [68](readings/book-04.md#reading-68) | IV.32 | [Read](sources/meditations-george-long-gutenberg.txt#L3261-L3279) |
| [69](readings/book-04.md#reading-69) | IV.33 | [Read](sources/meditations-george-long-gutenberg.txt#L3279-L3293) |
| [70](readings/book-04.md#reading-70) | IV.34 | [Read](sources/meditations-george-long-gutenberg.txt#L3293-L3296) |
| [71](readings/book-04.md#reading-71) | IV.35 | [Read](sources/meditations-george-long-gutenberg.txt#L3296-L3299) |
| [72](readings/book-04.md#reading-72) | IV.36 | [Read](sources/meditations-george-long-gutenberg.txt#L3299-L3306) |
| [73](readings/book-04.md#reading-73) | IV.37 | [Read](sources/meditations-george-long-gutenberg.txt#L3306-L3311) |
| [74](readings/book-04.md#reading-74) | IV.38 | [Read](sources/meditations-george-long-gutenberg.txt#L3311-L3314) |
| [75](readings/book-04.md#reading-75) | IV.39 | [Read](sources/meditations-george-long-gutenberg.txt#L3314-L3326) |
| [76](readings/book-04.md#reading-76) | IV.40 | [Read](sources/meditations-george-long-gutenberg.txt#L3326-L3333) |
| [77](readings/book-04.md#reading-77) | IV.41 | [Read](sources/meditations-george-long-gutenberg.txt#L3333-L3336) |
| [78](readings/book-04.md#reading-78) | IV.42 | [Read](sources/meditations-george-long-gutenberg.txt#L3336-L3339) |
| [79](readings/book-04.md#reading-79) | IV.43 | [Read](sources/meditations-george-long-gutenberg.txt#L3339-L3343) |
| [80](readings/book-04.md#reading-80) | IV.44 | [Read](sources/meditations-george-long-gutenberg.txt#L3343-L3347) |
| [81](readings/book-04.md#reading-81) | IV.45 | [Read](sources/meditations-george-long-gutenberg.txt#L3347-L3355) |
| [82](readings/book-04.md#reading-82) | IV.46 | [Read](sources/meditations-george-long-gutenberg.txt#L3355-L3366) |
| [83](readings/book-04.md#reading-83) | IV.47 | [Read](sources/meditations-george-long-gutenberg.txt#L3366-L3373) |
| [84](readings/book-04.md#reading-84) | IV.48 | [Read](sources/meditations-george-long-gutenberg.txt#L3373-L3395) |
| [85](readings/book-04.md#reading-85) | IV.49 | [Read](sources/meditations-george-long-gutenberg.txt#L3395-L3415) |
| [86](readings/book-04.md#reading-86) | IV.50 | [Read](sources/meditations-george-long-gutenberg.txt#L3415-L3438) |
| [87](readings/book-04.md#reading-87) | IV.51 | [Read](sources/meditations-george-long-gutenberg.txt#L3438-L3441) |

</details>

<details>

<summary>Book V</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [88](readings/book-05.md#reading-88) | V.1 | [Read](sources/meditations-george-long-gutenberg.txt#L3449-L3474) |
| [89](readings/book-05.md#reading-89) | V.2 | [Read](sources/meditations-george-long-gutenberg.txt#L3474-L3477) |
| [90](readings/book-05.md#reading-90) | V.3 | [Read](sources/meditations-george-long-gutenberg.txt#L3477-L3485) |
| [91](readings/book-05.md#reading-91) | V.4 | [Read](sources/meditations-george-long-gutenberg.txt#L3485-L3493) |
| [92](readings/book-05.md#reading-92) | V.5 | [Read](sources/meditations-george-long-gutenberg.txt#L3493-L3511) |
| [93](readings/book-05.md#reading-93) | V.6 | [Read](sources/meditations-george-long-gutenberg.txt#L3511-L3532) |
| [94](readings/book-05.md#reading-94) | V.7 | [Read](sources/meditations-george-long-gutenberg.txt#L3532-L3537) |
| [95](readings/book-05.md#reading-95) | V.8 | [Read](sources/meditations-george-long-gutenberg.txt#L3537-L3582) |
| [96](readings/book-05.md#reading-96) | V.9 | [Read](sources/meditations-george-long-gutenberg.txt#L3582-L3600) |
| [97](readings/book-05.md#reading-97) | V.10 | [Read](sources/meditations-george-long-gutenberg.txt#L3600-L3620) |
| [98](readings/book-05.md#reading-98) | V.11 | [Read](sources/meditations-george-long-gutenberg.txt#L3620-L3626) |
| [99](readings/book-05.md#reading-99) | V.12–15 | [Read](sources/meditations-george-long-gutenberg.txt#L3626-L3672) |
| [100](readings/book-05.md#reading-100) | V.16 | [Read](sources/meditations-george-long-gutenberg.txt#L3672-L3689) |
| [101](readings/book-05.md#reading-101) | V.17–20 | [Read](sources/meditations-george-long-gutenberg.txt#L3689-L3715) |
| [102](readings/book-05.md#reading-102) | V.21 | [Read](sources/meditations-george-long-gutenberg.txt#L3715-L3721) |
| [103](readings/book-05.md#reading-103) | V.22 | [Read](sources/meditations-george-long-gutenberg.txt#L3721-L3727) |
| [104](readings/book-05.md#reading-104) | V.23 | [Read](sources/meditations-george-long-gutenberg.txt#L3727-L3737) |
| [105](readings/book-05.md#reading-105) | V.24 | [Read](sources/meditations-george-long-gutenberg.txt#L3737-L3742) |
| [106](readings/book-05.md#reading-106) | V.25 | [Read](sources/meditations-george-long-gutenberg.txt#L3742-L3746) |
| [107](readings/book-05.md#reading-107) | V.26 | [Read](sources/meditations-george-long-gutenberg.txt#L3746-L3755) |
| [108](readings/book-05.md#reading-108) | V.27 | [Read](sources/meditations-george-long-gutenberg.txt#L3755-L3761) |
| [109](readings/book-05.md#reading-109) | V.28–29 | [Read](sources/meditations-george-long-gutenberg.txt#L3761-L3789) |
| [110](readings/book-05.md#reading-110) | V.30 | [Read](sources/meditations-george-long-gutenberg.txt#L3789-L3796) |
| [111](readings/book-05.md#reading-111) | V.31 | [Read](sources/meditations-george-long-gutenberg.txt#L3796-L3810) |
| [112](readings/book-05.md#reading-112) | V.32 | [Read](sources/meditations-george-long-gutenberg.txt#L3810-L3816) |
| [113](readings/book-05.md#reading-113) | V.33 | [Read](sources/meditations-george-long-gutenberg.txt#L3816-L3843) |
| [114](readings/book-05.md#reading-114) | V.34–35 | [Read](sources/meditations-george-long-gutenberg.txt#L3843-L3854) |
| [115](readings/book-05.md#reading-115) | V.36 | [Read](sources/meditations-george-long-gutenberg.txt#L3854-L3873) |

</details>

<details>

<summary>Book VI</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [116](readings/book-06.md#reading-116) | VI.1 | [Read](sources/meditations-george-long-gutenberg.txt#L3881-L3886) |
| [117](readings/book-06.md#reading-117) | VI.2 | [Read](sources/meditations-george-long-gutenberg.txt#L3886-L3893) |
| [118](readings/book-06.md#reading-118) | VI.3 | [Read](sources/meditations-george-long-gutenberg.txt#L3893-L3896) |
| [119](readings/book-06.md#reading-119) | VI.4 | [Read](sources/meditations-george-long-gutenberg.txt#L3896-L3899) |
| [120](readings/book-06.md#reading-120) | VI.5 | [Read](sources/meditations-george-long-gutenberg.txt#L3899-L3902) |
| [121](readings/book-06.md#reading-121) | VI.6 | [Read](sources/meditations-george-long-gutenberg.txt#L3902-L3905) |
| [122](readings/book-06.md#reading-122) | VI.7 | [Read](sources/meditations-george-long-gutenberg.txt#L3905-L3908) |
| [123](readings/book-06.md#reading-123) | VI.8 | [Read](sources/meditations-george-long-gutenberg.txt#L3908-L3912) |
| [124](readings/book-06.md#reading-124) | VI.9 | [Read](sources/meditations-george-long-gutenberg.txt#L3912-L3918) |
| [125](readings/book-06.md#reading-125) | VI.10 | [Read](sources/meditations-george-long-gutenberg.txt#L3918-L3927) |
| [126](readings/book-06.md#reading-126) | VI.11 | [Read](sources/meditations-george-long-gutenberg.txt#L3927-L3932) |
| [127](readings/book-06.md#reading-127) | VI.12 | [Read](sources/meditations-george-long-gutenberg.txt#L3932-L3939) |
| [128](readings/book-06.md#reading-128) | VI.13 | [Read](sources/meditations-george-long-gutenberg.txt#L3939-L3953) |
| [129](readings/book-06.md#reading-129) | VI.14 | [Read](sources/meditations-george-long-gutenberg.txt#L3953-L3969) |
| [130](readings/book-06.md#reading-130) | VI.15 | [Read](sources/meditations-george-long-gutenberg.txt#L3969-L3984) |
| [131](readings/book-06.md#reading-131) | VI.16 | [Read](sources/meditations-george-long-gutenberg.txt#L3984-L4013) |
| [132](readings/book-06.md#reading-132) | VI.17 | [Read](sources/meditations-george-long-gutenberg.txt#L4013-L4017) |
| [133](readings/book-06.md#reading-133) | VI.18 | [Read](sources/meditations-george-long-gutenberg.txt#L4017-L4024) |
| [134](readings/book-06.md#reading-134) | VI.19 | [Read](sources/meditations-george-long-gutenberg.txt#L4024-L4029) |
| [135](readings/book-06.md#reading-135) | VI.20 | [Read](sources/meditations-george-long-gutenberg.txt#L4029-L4039) |
| [136](readings/book-06.md#reading-136) | VI.21 | [Read](sources/meditations-george-long-gutenberg.txt#L4039-L4044) |
| [137](readings/book-06.md#reading-137) | VI.22 | [Read](sources/meditations-george-long-gutenberg.txt#L4044-L4048) |
| [138](readings/book-06.md#reading-138) | VI.23 | [Read](sources/meditations-george-long-gutenberg.txt#L4048-L4056) |
| [139](readings/book-06.md#reading-139) | VI.24 | [Read](sources/meditations-george-long-gutenberg.txt#L4056-L4061) |
| [140](readings/book-06.md#reading-140) | VI.25 | [Read](sources/meditations-george-long-gutenberg.txt#L4061-L4067) |
| [141](readings/book-06.md#reading-141) | VI.26 | [Read](sources/meditations-george-long-gutenberg.txt#L4067-L4076) |
| [142](readings/book-06.md#reading-142) | VI.27 | [Read](sources/meditations-george-long-gutenberg.txt#L4076-L4084) |
| [143](readings/book-06.md#reading-143) | VI.28 | [Read](sources/meditations-george-long-gutenberg.txt#L4084-L4089) |
| [144](readings/book-06.md#reading-144) | VI.29 | [Read](sources/meditations-george-long-gutenberg.txt#L4089-L4092) |
| [145](readings/book-06.md#reading-145) | VI.30 | [Read](sources/meditations-george-long-gutenberg.txt#L4092-L4119) |
| [146](readings/book-06.md#reading-146) | VI.31 | [Read](sources/meditations-george-long-gutenberg.txt#L4119-L4124) |
| [147](readings/book-06.md#reading-147) | VI.32 | [Read](sources/meditations-george-long-gutenberg.txt#L4124-L4133) |
| [148](readings/book-06.md#reading-148) | VI.33 | [Read](sources/meditations-george-long-gutenberg.txt#L4133-L4139) |
| [149](readings/book-06.md#reading-149) | VI.34 | [Read](sources/meditations-george-long-gutenberg.txt#L4139-L4142) |
| [150](readings/book-06.md#reading-150) | VI.35 | [Read](sources/meditations-george-long-gutenberg.txt#L4142-L4150) |
| [151](readings/book-06.md#reading-151) | VI.36 | [Read](sources/meditations-george-long-gutenberg.txt#L4150-L4160) |
| [152](readings/book-06.md#reading-152) | VI.37 | [Read](sources/meditations-george-long-gutenberg.txt#L4160-L4164) |
| [153](readings/book-06.md#reading-153) | VI.38 | [Read](sources/meditations-george-long-gutenberg.txt#L4164-L4171) |
| [154](readings/book-06.md#reading-154) | VI.39 | [Read](sources/meditations-george-long-gutenberg.txt#L4171-L4175) |
| [155](readings/book-06.md#reading-155) | VI.40 | [Read](sources/meditations-george-long-gutenberg.txt#L4175-L4184) |
| [156](readings/book-06.md#reading-156) | VI.41 | [Read](sources/meditations-george-long-gutenberg.txt#L4184-L4202) |
| [157](readings/book-06.md#reading-157) | VI.42 | [Read](sources/meditations-george-long-gutenberg.txt#L4202-L4218) |
| [158](readings/book-06.md#reading-158) | VI.43 | [Read](sources/meditations-george-long-gutenberg.txt#L4218-L4223) |
| [159](readings/book-06.md#reading-159) | VI.44 | [Read](sources/meditations-george-long-gutenberg.txt#L4223-L4243) |
| [160](readings/book-06.md#reading-160) | VI.45 | [Read](sources/meditations-george-long-gutenberg.txt#L4243-L4250) |
| [161](readings/book-06.md#reading-161) | VI.46 | [Read](sources/meditations-george-long-gutenberg.txt#L4250-L4255) |
| [162](readings/book-06.md#reading-162) | VI.47 | [Read](sources/meditations-george-long-gutenberg.txt#L4255-L4270) |
| [163](readings/book-06.md#reading-163) | VI.48 | [Read](sources/meditations-george-long-gutenberg.txt#L4270-L4278) |
| [164](readings/book-06.md#reading-164) | VI.49 | [Read](sources/meditations-george-long-gutenberg.txt#L4278-L4284) |
| [165](readings/book-06.md#reading-165) | VI.50 | [Read](sources/meditations-george-long-gutenberg.txt#L4284-L4294) |
| [166](readings/book-06.md#reading-166) | VI.51 | [Read](sources/meditations-george-long-gutenberg.txt#L4294-L4298) |
| [167](readings/book-06.md#reading-167) | VI.52 | [Read](sources/meditations-george-long-gutenberg.txt#L4298-L4302) |
| [168](readings/book-06.md#reading-168) | VI.53 | [Read](sources/meditations-george-long-gutenberg.txt#L4302-L4305) |
| [169](readings/book-06.md#reading-169) | VI.54 | [Read](sources/meditations-george-long-gutenberg.txt#L4305-L4308) |
| [170](readings/book-06.md#reading-170) | VI.55 | [Read](sources/meditations-george-long-gutenberg.txt#L4308-L4312) |
| [171](readings/book-06.md#reading-171) | VI.56 | [Read](sources/meditations-george-long-gutenberg.txt#L4312-L4315) |
| [172](readings/book-06.md#reading-172) | VI.57 | [Read](sources/meditations-george-long-gutenberg.txt#L4315-L4321) |
| [173](readings/book-06.md#reading-173) | VI.58 | [Read](sources/meditations-george-long-gutenberg.txt#L4321-L4325) |
| [174](readings/book-06.md#reading-174) | VI.59 | [Read](sources/meditations-george-long-gutenberg.txt#L4325-L4327) |

</details>

<details>

<summary>Book VII</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [175](readings/book-07.md#reading-175) | VII.1 | [Read](sources/meditations-george-long-gutenberg.txt#L4335-L4343) |
| [176](readings/book-07.md#reading-176) | VII.2 | [Read](sources/meditations-george-long-gutenberg.txt#L4343-L4352) |
| [177](readings/book-07.md#reading-177) | VII.3 | [Read](sources/meditations-george-long-gutenberg.txt#L4352-L4360) |
| [178](readings/book-07.md#reading-178) | VII.4 | [Read](sources/meditations-george-long-gutenberg.txt#L4360-L4365) |
| [179](readings/book-07.md#reading-179) | VII.5 | [Read](sources/meditations-george-long-gutenberg.txt#L4365-L4375) |
| [180](readings/book-07.md#reading-180) | VII.6 | [Read](sources/meditations-george-long-gutenberg.txt#L4375-L4379) |
| [181](readings/book-07.md#reading-181) | VII.7 | [Read](sources/meditations-george-long-gutenberg.txt#L4379-L4384) |
| [182](readings/book-07.md#reading-182) | VII.8 | [Read](sources/meditations-george-long-gutenberg.txt#L4384-L4388) |
| [183](readings/book-07.md#reading-183) | VII.9 | [Read](sources/meditations-george-long-gutenberg.txt#L4388-L4399) |
| [184](readings/book-07.md#reading-184) | VII.10 | [Read](sources/meditations-george-long-gutenberg.txt#L4399-L4404) |
| [185](readings/book-07.md#reading-185) | VII.11 | [Read](sources/meditations-george-long-gutenberg.txt#L4404-L4407) |
| [186](readings/book-07.md#reading-186) | VII.12 | [Read](sources/meditations-george-long-gutenberg.txt#L4407-L4409) |
| [187](readings/book-07.md#reading-187) | VII.13 | [Read](sources/meditations-george-long-gutenberg.txt#L4409-L4423) |
| [188](readings/book-07.md#reading-188) | VII.14 | [Read](sources/meditations-george-long-gutenberg.txt#L4423-L4428) |
| [189](readings/book-07.md#reading-189) | VII.15 | [Read](sources/meditations-george-long-gutenberg.txt#L4428-L4432) |
| [190](readings/book-07.md#reading-190) | VII.16 | [Read](sources/meditations-george-long-gutenberg.txt#L4432-L4444) |
| [191](readings/book-07.md#reading-191) | VII.17 | [Read](sources/meditations-george-long-gutenberg.txt#L4444-L4449) |
| [192](readings/book-07.md#reading-192) | VII.18 | [Read](sources/meditations-george-long-gutenberg.txt#L4449-L4457) |
| [193](readings/book-07.md#reading-193) | VII.19 | [Read](sources/meditations-george-long-gutenberg.txt#L4457-L4464) |
| [194](readings/book-07.md#reading-194) | VII.20 | [Read](sources/meditations-george-long-gutenberg.txt#L4464-L4468) |
| [195](readings/book-07.md#reading-195) | VII.21 | [Read](sources/meditations-george-long-gutenberg.txt#L4468-L4471) |
| [196](readings/book-07.md#reading-196) | VII.22 | [Read](sources/meditations-george-long-gutenberg.txt#L4471-L4478) |
| [197](readings/book-07.md#reading-197) | VII.23 | [Read](sources/meditations-george-long-gutenberg.txt#L4478-L4485) |
| [198](readings/book-07.md#reading-198) | VII.24 | [Read](sources/meditations-george-long-gutenberg.txt#L4485-L4494) |
| [199](readings/book-07.md#reading-199) | VII.25 | [Read](sources/meditations-george-long-gutenberg.txt#L4494-L4499) |
| [200](readings/book-07.md#reading-200) | VII.26 | [Read](sources/meditations-george-long-gutenberg.txt#L4499-L4507) |
| [201](readings/book-07.md#reading-201) | VII.27 | [Read](sources/meditations-george-long-gutenberg.txt#L4507-L4514) |
| [202](readings/book-07.md#reading-202) | VII.28 | [Read](sources/meditations-george-long-gutenberg.txt#L4514-L4518) |
| [203](readings/book-07.md#reading-203) | VII.29 | [Read](sources/meditations-george-long-gutenberg.txt#L4518-L4524) |
| [204](readings/book-07.md#reading-204) | VII.30 | [Read](sources/meditations-george-long-gutenberg.txt#L4524-L4527) |
| [205](readings/book-07.md#reading-205) | VII.31 | [Read](sources/meditations-george-long-gutenberg.txt#L4527-L4534) |
| [206](readings/book-07.md#reading-206) | VII.32 | [Read](sources/meditations-george-long-gutenberg.txt#L4534-L4537) |
| [207](readings/book-07.md#reading-207) | VII.33 | [Read](sources/meditations-george-long-gutenberg.txt#L4537-L4543) |
| [208](readings/book-07.md#reading-208) | VII.34 | [Read](sources/meditations-george-long-gutenberg.txt#L4543-L4549) |
| [209](readings/book-07.md#reading-209) | VII.35–40 | [Read](sources/meditations-george-long-gutenberg.txt#L4549-L4580) |
| [210](readings/book-07.md#reading-210) | VII.41–45 | [Read](sources/meditations-george-long-gutenberg.txt#L4580-L4606) |
| [211](readings/book-07.md#reading-211) | VII.46–48 | [Read](sources/meditations-george-long-gutenberg.txt#L4606-L4637) |
| [212](readings/book-07.md#reading-212) | VII.49 | [Read](sources/meditations-george-long-gutenberg.txt#L4637-L4644) |
| [213](readings/book-07.md#reading-213) | VII.50–51 | [Read](sources/meditations-george-long-gutenberg.txt#L4644-L4661) |
| [214](readings/book-07.md#reading-214) | VII.52 | [Read](sources/meditations-george-long-gutenberg.txt#L4661-L4666) |
| [215](readings/book-07.md#reading-215) | VII.53 | [Read](sources/meditations-george-long-gutenberg.txt#L4666-L4671) |
| [216](readings/book-07.md#reading-216) | VII.54 | [Read](sources/meditations-george-long-gutenberg.txt#L4671-L4676) |
| [217](readings/book-07.md#reading-217) | VII.55 | [Read](sources/meditations-george-long-gutenberg.txt#L4676-L4696) |
| [218](readings/book-07.md#reading-218) | VII.56 | [Read](sources/meditations-george-long-gutenberg.txt#L4696-L4700) |
| [219](readings/book-07.md#reading-219) | VII.57 | [Read](sources/meditations-george-long-gutenberg.txt#L4700-L4703) |
| [220](readings/book-07.md#reading-220) | VII.58 | [Read](sources/meditations-george-long-gutenberg.txt#L4703-L4719) |
| [221](readings/book-07.md#reading-221) | VII.59 | [Read](sources/meditations-george-long-gutenberg.txt#L4719-L4722) |
| [222](readings/book-07.md#reading-222) | VII.60 | [Read](sources/meditations-george-long-gutenberg.txt#L4722-L4728) |
| [223](readings/book-07.md#reading-223) | VII.61 | [Read](sources/meditations-george-long-gutenberg.txt#L4728-L4732) |
| [224](readings/book-07.md#reading-224) | VII.62 | [Read](sources/meditations-george-long-gutenberg.txt#L4732-L4738) |
| [225](readings/book-07.md#reading-225) | VII.63 | [Read](sources/meditations-george-long-gutenberg.txt#L4738-L4744) |
| [226](readings/book-07.md#reading-226) | VII.64–66 | [Read](sources/meditations-george-long-gutenberg.txt#L4744-L4788) |
| [227](readings/book-07.md#reading-227) | VII.67 | [Read](sources/meditations-george-long-gutenberg.txt#L4788-L4798) |
| [228](readings/book-07.md#reading-228) | VII.68 | [Read](sources/meditations-george-long-gutenberg.txt#L4798-L4815) |
| [229](readings/book-07.md#reading-229) | VII.69 | [Read](sources/meditations-george-long-gutenberg.txt#L4815-L4819) |
| [230](readings/book-07.md#reading-230) | VII.70 | [Read](sources/meditations-george-long-gutenberg.txt#L4819-L4825) |
| [231](readings/book-07.md#reading-231) | VII.71 | [Read](sources/meditations-george-long-gutenberg.txt#L4825-L4829) |
| [232](readings/book-07.md#reading-232) | VII.72 | [Read](sources/meditations-george-long-gutenberg.txt#L4829-L4833) |
| [233](readings/book-07.md#reading-233) | VII.73 | [Read](sources/meditations-george-long-gutenberg.txt#L4833-L4837) |
| [234](readings/book-07.md#reading-234) | VII.74 | [Read](sources/meditations-george-long-gutenberg.txt#L4837-L4841) |
| [235](readings/book-07.md#reading-235) | VII.75 | [Read](sources/meditations-george-long-gutenberg.txt#L4841-L4928) |

</details>

<details>

<summary>Book VIII</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [236](readings/book-08.md#reading-236) | VIII.1 | [Read](sources/meditations-george-long-gutenberg.txt#L4936-L4956) |
| [237](readings/book-08.md#reading-237) | VIII.2 | [Read](sources/meditations-george-long-gutenberg.txt#L4956-L4962) |
| [238](readings/book-08.md#reading-238) | VIII.3 | [Read](sources/meditations-george-long-gutenberg.txt#L4962-L4972) |
| [239](readings/book-08.md#reading-239) | VIII.4 | [Read](sources/meditations-george-long-gutenberg.txt#L4972-L4975) |
| [240](readings/book-08.md#reading-240) | VIII.5 | [Read](sources/meditations-george-long-gutenberg.txt#L4975-L4984) |
| [241](readings/book-08.md#reading-241) | VIII.6 | [Read](sources/meditations-george-long-gutenberg.txt#L4984-L4990) |
| [242](readings/book-08.md#reading-242) | VIII.7 | [Read](sources/meditations-george-long-gutenberg.txt#L4990-L5008) |
| [243](readings/book-08.md#reading-243) | VIII.8 | [Read](sources/meditations-george-long-gutenberg.txt#L5008-L5014) |
| [244](readings/book-08.md#reading-244) | VIII.9 | [Read](sources/meditations-george-long-gutenberg.txt#L5014-L5017) |
| [245](readings/book-08.md#reading-245) | VIII.10 | [Read](sources/meditations-george-long-gutenberg.txt#L5017-L5023) |
| [246](readings/book-08.md#reading-246) | VIII.11 | [Read](sources/meditations-george-long-gutenberg.txt#L5023-L5027) |
| [247](readings/book-08.md#reading-247) | VIII.12 | [Read](sources/meditations-george-long-gutenberg.txt#L5027-L5034) |
| [248](readings/book-08.md#reading-248) | VIII.13 | [Read](sources/meditations-george-long-gutenberg.txt#L5034-L5038) |
| [249](readings/book-08.md#reading-249) | VIII.14 | [Read](sources/meditations-george-long-gutenberg.txt#L5038-L5049) |
| [250](readings/book-08.md#reading-250) | VIII.15 | [Read](sources/meditations-george-long-gutenberg.txt#L5049-L5055) |
| [251](readings/book-08.md#reading-251) | VIII.16 | [Read](sources/meditations-george-long-gutenberg.txt#L5055-L5061) |
| [252](readings/book-08.md#reading-252) | VIII.17 | [Read](sources/meditations-george-long-gutenberg.txt#L5061-L5069) |
| [253](readings/book-08.md#reading-253) | VIII.18 | [Read](sources/meditations-george-long-gutenberg.txt#L5069-L5074) |
| [254](readings/book-08.md#reading-254) | VIII.19 | [Read](sources/meditations-george-long-gutenberg.txt#L5074-L5079) |
| [255](readings/book-08.md#reading-255) | VIII.20 | [Read](sources/meditations-george-long-gutenberg.txt#L5079-L5086) |
| [256](readings/book-08.md#reading-256) | VIII.21 | [Read](sources/meditations-george-long-gutenberg.txt#L5086-L5095) |
| [257](readings/book-08.md#reading-257) | VIII.22 | [Read](sources/meditations-george-long-gutenberg.txt#L5095-L5101) |
| [258](readings/book-08.md#reading-258) | VIII.23 | [Read](sources/meditations-george-long-gutenberg.txt#L5101-L5105) |
| [259](readings/book-08.md#reading-259) | VIII.24 | [Read](sources/meditations-george-long-gutenberg.txt#L5105-L5108) |
| [260](readings/book-08.md#reading-260) | VIII.25 | [Read](sources/meditations-george-long-gutenberg.txt#L5108-L5121) |
| [261](readings/book-08.md#reading-261) | VIII.26 | [Read](sources/meditations-george-long-gutenberg.txt#L5121-L5127) |
| [262](readings/book-08.md#reading-262) | VIII.27 | [Read](sources/meditations-george-long-gutenberg.txt#L5127-L5136) |
| [263](readings/book-08.md#reading-263) | VIII.28 | [Read](sources/meditations-george-long-gutenberg.txt#L5136-L5142) |
| [264](readings/book-08.md#reading-264) | VIII.29 | [Read](sources/meditations-george-long-gutenberg.txt#L5142-L5148) |
| [265](readings/book-08.md#reading-265) | VIII.30 | [Read](sources/meditations-george-long-gutenberg.txt#L5148-L5151) |
| [266](readings/book-08.md#reading-266) | VIII.31 | [Read](sources/meditations-george-long-gutenberg.txt#L5151-L5164) |
| [267](readings/book-08.md#reading-267) | VIII.32 | [Read](sources/meditations-george-long-gutenberg.txt#L5164-L5175) |
| [268](readings/book-08.md#reading-268) | VIII.33 | [Read](sources/meditations-george-long-gutenberg.txt#L5175-L5178) |
| [269](readings/book-08.md#reading-269) | VIII.34 | [Read](sources/meditations-george-long-gutenberg.txt#L5178-L5192) |
| [270](readings/book-08.md#reading-270) | VIII.35–37 | [Read](sources/meditations-george-long-gutenberg.txt#L5192-L5226) |
| [271](readings/book-08.md#reading-271) | VIII.38 | [Read](sources/meditations-george-long-gutenberg.txt#L5226-L5229) |
| [272](readings/book-08.md#reading-272) | VIII.39 | [Read](sources/meditations-george-long-gutenberg.txt#L5229-L5233) |
| [273](readings/book-08.md#reading-273) | VIII.40 | [Read](sources/meditations-george-long-gutenberg.txt#L5233-L5239) |
| [274](readings/book-08.md#reading-274) | VIII.41 | [Read](sources/meditations-george-long-gutenberg.txt#L5239-L5255) |
| [275](readings/book-08.md#reading-275) | VIII.42 | [Read](sources/meditations-george-long-gutenberg.txt#L5255-L5258) |
| [276](readings/book-08.md#reading-276) | VIII.43 | [Read](sources/meditations-george-long-gutenberg.txt#L5258-L5264) |
| [277](readings/book-08.md#reading-277) | VIII.44 | [Read](sources/meditations-george-long-gutenberg.txt#L5264-L5270) |
| [278](readings/book-08.md#reading-278) | VIII.45 | [Read](sources/meditations-george-long-gutenberg.txt#L5270-L5282) |
| [279](readings/book-08.md#reading-279) | VIII.46 | [Read](sources/meditations-george-long-gutenberg.txt#L5282-L5289) |
| [280](readings/book-08.md#reading-280) | VIII.47 | [Read](sources/meditations-george-long-gutenberg.txt#L5289-L5301) |
| [281](readings/book-08.md#reading-281) | VIII.48 | [Read](sources/meditations-george-long-gutenberg.txt#L5301-L5310) |
| [282](readings/book-08.md#reading-282) | VIII.49 | [Read](sources/meditations-george-long-gutenberg.txt#L5310-L5319) |
| [283](readings/book-08.md#reading-283) | VIII.50 | [Read](sources/meditations-george-long-gutenberg.txt#L5319-L5334) |
| [284](readings/book-08.md#reading-284) | VIII.51 | [Read](sources/meditations-george-long-gutenberg.txt#L5334-L5349) |
| [285](readings/book-08.md#reading-285) | VIII.52 | [Read](sources/meditations-george-long-gutenberg.txt#L5349-L5357) |
| [286](readings/book-08.md#reading-286) | VIII.53 | [Read](sources/meditations-george-long-gutenberg.txt#L5357-L5362) |
| [287](readings/book-08.md#reading-287) | VIII.54 | [Read](sources/meditations-george-long-gutenberg.txt#L5362-L5369) |
| [288](readings/book-08.md#reading-288) | VIII.55 | [Read](sources/meditations-george-long-gutenberg.txt#L5369-L5374) |
| [289](readings/book-08.md#reading-289) | VIII.56 | [Read](sources/meditations-george-long-gutenberg.txt#L5374-L5381) |
| [290](readings/book-08.md#reading-290) | VIII.57 | [Read](sources/meditations-george-long-gutenberg.txt#L5381-L5398) |
| [291](readings/book-08.md#reading-291) | VIII.58 | [Read](sources/meditations-george-long-gutenberg.txt#L5398-L5404) |
| [292](readings/book-08.md#reading-292) | VIII.59 | [Read](sources/meditations-george-long-gutenberg.txt#L5404-L5407) |
| [293](readings/book-08.md#reading-293) | VIII.60 | [Read](sources/meditations-george-long-gutenberg.txt#L5407-L5411) |
| [294](readings/book-08.md#reading-294) | VIII.61 | [Read](sources/meditations-george-long-gutenberg.txt#L5411-L5414) |

</details>

<details>

<summary>Book IX</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [295](readings/book-09.md#reading-295) | IX.1 | [Read](sources/meditations-george-long-gutenberg.txt#L5422-L5480) |
| [296](readings/book-09.md#reading-296) | IX.2 | [Read](sources/meditations-george-long-gutenberg.txt#L5480-L5491) |
| [297](readings/book-09.md#reading-297) | IX.3 | [Read](sources/meditations-george-long-gutenberg.txt#L5491-L5517) |
| [298](readings/book-09.md#reading-298) | IX.4 | [Read](sources/meditations-george-long-gutenberg.txt#L5517-L5520) |
| [299](readings/book-09.md#reading-299) | IX.5 | [Read](sources/meditations-george-long-gutenberg.txt#L5520-L5523) |
| [300](readings/book-09.md#reading-300) | IX.6 | [Read](sources/meditations-george-long-gutenberg.txt#L5523-L5527) |
| [301](readings/book-09.md#reading-301) | IX.7 | [Read](sources/meditations-george-long-gutenberg.txt#L5527-L5530) |
| [302](readings/book-09.md#reading-302) | IX.8 | [Read](sources/meditations-george-long-gutenberg.txt#L5530-L5536) |
| [303](readings/book-09.md#reading-303) | IX.9 | [Read](sources/meditations-george-long-gutenberg.txt#L5536-L5570) |
| [304](readings/book-09.md#reading-304) | IX.10 | [Read](sources/meditations-george-long-gutenberg.txt#L5570-L5576) |
| [305](readings/book-09.md#reading-305) | IX.11 | [Read](sources/meditations-george-long-gutenberg.txt#L5576-L5582) |
| [306](readings/book-09.md#reading-306) | IX.12 | [Read](sources/meditations-george-long-gutenberg.txt#L5582-L5586) |
| [307](readings/book-09.md#reading-307) | IX.13 | [Read](sources/meditations-george-long-gutenberg.txt#L5586-L5589) |
| [308](readings/book-09.md#reading-308) | IX.14 | [Read](sources/meditations-george-long-gutenberg.txt#L5589-L5593) |
| [309](readings/book-09.md#reading-309) | IX.15 | [Read](sources/meditations-george-long-gutenberg.txt#L5593-L5597) |
| [310](readings/book-09.md#reading-310) | IX.16 | [Read](sources/meditations-george-long-gutenberg.txt#L5597-L5604) |
| [311](readings/book-09.md#reading-311) | IX.17 | [Read](sources/meditations-george-long-gutenberg.txt#L5604-L5607) |
| [312](readings/book-09.md#reading-312) | IX.18 | [Read](sources/meditations-george-long-gutenberg.txt#L5607-L5611) |
| [313](readings/book-09.md#reading-313) | IX.19 | [Read](sources/meditations-george-long-gutenberg.txt#L5611-L5614) |
| [314](readings/book-09.md#reading-314) | IX.20 | [Read](sources/meditations-george-long-gutenberg.txt#L5614-L5617) |
| [315](readings/book-09.md#reading-315) | IX.21 | [Read](sources/meditations-george-long-gutenberg.txt#L5617-L5630) |
| [316](readings/book-09.md#reading-316) | IX.22 | [Read](sources/meditations-george-long-gutenberg.txt#L5630-L5637) |
| [317](readings/book-09.md#reading-317) | IX.23 | [Read](sources/meditations-george-long-gutenberg.txt#L5637-L5644) |
| [318](readings/book-09.md#reading-318) | IX.24 | [Read](sources/meditations-george-long-gutenberg.txt#L5644-L5654) |
| [319](readings/book-09.md#reading-319) | IX.25 | [Read](sources/meditations-george-long-gutenberg.txt#L5654-L5659) |
| [320](readings/book-09.md#reading-320) | IX.26 | [Read](sources/meditations-george-long-gutenberg.txt#L5659-L5663) |
| [321](readings/book-09.md#reading-321) | IX.27 | [Read](sources/meditations-george-long-gutenberg.txt#L5663-L5671) |
| [322](readings/book-09.md#reading-322) | IX.28 | [Read](sources/meditations-george-long-gutenberg.txt#L5671-L5691) |
| [323](readings/book-09.md#reading-323) | IX.29 | [Read](sources/meditations-george-long-gutenberg.txt#L5691-L5710) |
| [324](readings/book-09.md#reading-324) | IX.30 | [Read](sources/meditations-george-long-gutenberg.txt#L5710-L5720) |
| [325](readings/book-09.md#reading-325) | IX.31 | [Read](sources/meditations-george-long-gutenberg.txt#L5720-L5726) |
| [326](readings/book-09.md#reading-326) | IX.32 | [Read](sources/meditations-george-long-gutenberg.txt#L5726-L5734) |
| [327](readings/book-09.md#reading-327) | IX.33 | [Read](sources/meditations-george-long-gutenberg.txt#L5734-L5739) |
| [328](readings/book-09.md#reading-328) | IX.34 | [Read](sources/meditations-george-long-gutenberg.txt#L5739-L5745) |
| [329](readings/book-09.md#reading-329) | IX.35 | [Read](sources/meditations-george-long-gutenberg.txt#L5745-L5753) |
| [330](readings/book-09.md#reading-330) | IX.36 | [Read](sources/meditations-george-long-gutenberg.txt#L5753-L5760) |
| [331](readings/book-09.md#reading-331) | IX.37 | [Read](sources/meditations-george-long-gutenberg.txt#L5760-L5767) |
| [332](readings/book-09.md#reading-332) | IX.38 | [Read](sources/meditations-george-long-gutenberg.txt#L5767-L5770) |
| [333](readings/book-09.md#reading-333) | IX.39 | [Read](sources/meditations-george-long-gutenberg.txt#L5770-L5784) |
| [334](readings/book-09.md#reading-334) | IX.40 | [Read](sources/meditations-george-long-gutenberg.txt#L5784-L5803) |
| [335](readings/book-09.md#reading-335) | IX.41 | [Read](sources/meditations-george-long-gutenberg.txt#L5803-L5818) |
| [336](readings/book-09.md#reading-336) | IX.42 | [Read](sources/meditations-george-long-gutenberg.txt#L5818-L5860) |

</details>

<details>

<summary>Book X</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [337](readings/book-10.md#reading-337) | X.1 | [Read](sources/meditations-george-long-gutenberg.txt#L5868-L5889) |
| [338](readings/book-10.md#reading-338) | X.2 | [Read](sources/meditations-george-long-gutenberg.txt#L5889-L5898) |
| [339](readings/book-10.md#reading-339) | X.3 | [Read](sources/meditations-george-long-gutenberg.txt#L5898-L5909) |
| [340](readings/book-10.md#reading-340) | X.4 | [Read](sources/meditations-george-long-gutenberg.txt#L5909-L5912) |
| [341](readings/book-10.md#reading-341) | X.5 | [Read](sources/meditations-george-long-gutenberg.txt#L5912-L5917) |
| [342](readings/book-10.md#reading-342) | X.6 | [Read](sources/meditations-george-long-gutenberg.txt#L5917-L5939) |
| [343](readings/book-10.md#reading-343) | X.7 | [Read](sources/meditations-george-long-gutenberg.txt#L5939-L5977) |
| [344](readings/book-10.md#reading-344) | X.8–9 | [Read](sources/meditations-george-long-gutenberg.txt#L5977-L6056) |
| [345](readings/book-10.md#reading-345) | X.10–11 | [Read](sources/meditations-george-long-gutenberg.txt#L6056-L6085) |
| [346](readings/book-10.md#reading-346) | X.12 | [Read](sources/meditations-george-long-gutenberg.txt#L6085-L6095) |
| [347](readings/book-10.md#reading-347) | X.13 | [Read](sources/meditations-george-long-gutenberg.txt#L6095-L6107) |
| [348](readings/book-10.md#reading-348) | X.14 | [Read](sources/meditations-george-long-gutenberg.txt#L6107-L6112) |
| [349](readings/book-10.md#reading-349) | X.15 | [Read](sources/meditations-george-long-gutenberg.txt#L6112-L6119) |
| [350](readings/book-10.md#reading-350) | X.16 | [Read](sources/meditations-george-long-gutenberg.txt#L6119-L6122) |
| [351](readings/book-10.md#reading-351) | X.17 | [Read](sources/meditations-george-long-gutenberg.txt#L6122-L6126) |
| [352](readings/book-10.md#reading-352) | X.18 | [Read](sources/meditations-george-long-gutenberg.txt#L6126-L6130) |
| [353](readings/book-10.md#reading-353) | X.19 | [Read](sources/meditations-george-long-gutenberg.txt#L6130-L6137) |
| [354](readings/book-10.md#reading-354) | X.20 | [Read](sources/meditations-george-long-gutenberg.txt#L6137-L6141) |
| [355](readings/book-10.md#reading-355) | X.21–23 | [Read](sources/meditations-george-long-gutenberg.txt#L6141-L6175) |
| [356](readings/book-10.md#reading-356) | X.24 | [Read](sources/meditations-george-long-gutenberg.txt#L6175-L6181) |
| [357](readings/book-10.md#reading-357) | X.25 | [Read](sources/meditations-george-long-gutenberg.txt#L6181-L6192) |
| [358](readings/book-10.md#reading-358) | X.26 | [Read](sources/meditations-george-long-gutenberg.txt#L6192-L6201) |
| [359](readings/book-10.md#reading-359) | X.27 | [Read](sources/meditations-george-long-gutenberg.txt#L6201-L6209) |
| [360](readings/book-10.md#reading-360) | X.28 | [Read](sources/meditations-george-long-gutenberg.txt#L6209-L6217) |
| [361](readings/book-10.md#reading-361) | X.29 | [Read](sources/meditations-george-long-gutenberg.txt#L6217-L6221) |
| [362](readings/book-10.md#reading-362) | X.30 | [Read](sources/meditations-george-long-gutenberg.txt#L6221-L6229) |
| [363](readings/book-10.md#reading-363) | X.31–32 | [Read](sources/meditations-george-long-gutenberg.txt#L6229-L6270) |
| [364](readings/book-10.md#reading-364) | X.33 | [Read](sources/meditations-george-long-gutenberg.txt#L6270-L6301) |
| [365](readings/book-10.md#reading-365) | X.34 | [Read](sources/meditations-george-long-gutenberg.txt#L6301-L6321) |
| [366](readings/book-10.md#reading-366) | X.35 | [Read](sources/meditations-george-long-gutenberg.txt#L6321-L6331) |
| [367](readings/book-10.md#reading-367) | X.36 | [Read](sources/meditations-george-long-gutenberg.txt#L6331-L6357) |
| [368](readings/book-10.md#reading-368) | X.37 | [Read](sources/meditations-george-long-gutenberg.txt#L6357-L6361) |
| [369](readings/book-10.md#reading-369) | X.38 | [Read](sources/meditations-george-long-gutenberg.txt#L6361-L6370) |

</details>

<details>

<summary>Book XI</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [370](readings/book-11.md#reading-370) | XI.1 | [Read](sources/meditations-george-long-gutenberg.txt#L6378-L6403) |
| [371](readings/book-11.md#reading-371) | XI.2 | [Read](sources/meditations-george-long-gutenberg.txt#L6403-L6413) |
| [372](readings/book-11.md#reading-372) | XI.3 | [Read](sources/meditations-george-long-gutenberg.txt#L6413-L6424) |
| [373](readings/book-11.md#reading-373) | XI.4 | [Read](sources/meditations-george-long-gutenberg.txt#L6424-L6428) |
| [374](readings/book-11.md#reading-374) | XI.5 | [Read](sources/meditations-george-long-gutenberg.txt#L6428-L6432) |
| [375](readings/book-11.md#reading-375) | XI.6 | [Read](sources/meditations-george-long-gutenberg.txt#L6432-L6469) |
| [376](readings/book-11.md#reading-376) | XI.7 | [Read](sources/meditations-george-long-gutenberg.txt#L6469-L6473) |
| [377](readings/book-11.md#reading-377) | XI.8 | [Read](sources/meditations-george-long-gutenberg.txt#L6473-L6491) |
| [378](readings/book-11.md#reading-378) | XI.9 | [Read](sources/meditations-george-long-gutenberg.txt#L6491-L6503) |
| [379](readings/book-11.md#reading-379) | XI.10 | [Read](sources/meditations-george-long-gutenberg.txt#L6503-L6513) |
| [380](readings/book-11.md#reading-380) | XI.11 | [Read](sources/meditations-george-long-gutenberg.txt#L6513-L6518) |
| [381](readings/book-11.md#reading-381) | XI.12 | [Read](sources/meditations-george-long-gutenberg.txt#L6518-L6524) |
| [382](readings/book-11.md#reading-382) | XI.13 | [Read](sources/meditations-george-long-gutenberg.txt#L6524-L6538) |
| [383](readings/book-11.md#reading-383) | XI.14 | [Read](sources/meditations-george-long-gutenberg.txt#L6538-L6541) |
| [384](readings/book-11.md#reading-384) | XI.15 | [Read](sources/meditations-george-long-gutenberg.txt#L6541-L6561) |
| [385](readings/book-11.md#reading-385) | XI.16 | [Read](sources/meditations-george-long-gutenberg.txt#L6561-L6577) |
| [386](readings/book-11.md#reading-386) | XI.17 | [Read](sources/meditations-george-long-gutenberg.txt#L6577-L6581) |
| [387](readings/book-11.md#reading-387) | XI.18 | [Read](sources/meditations-george-long-gutenberg.txt#L6581-L6669) |
| [388](readings/book-11.md#reading-388) | XI.19 | [Read](sources/meditations-george-long-gutenberg.txt#L6669-L6681) |
| [389](readings/book-11.md#reading-389) | XI.20 | [Read](sources/meditations-george-long-gutenberg.txt#L6681-L6723) |
| [390](readings/book-11.md#reading-390) | XI.21 | [Read](sources/meditations-george-long-gutenberg.txt#L6723-L6733) |
| [391](readings/book-11.md#reading-391) | XI.22–26 | [Read](sources/meditations-george-long-gutenberg.txt#L6733-L6760) |
| [392](readings/book-11.md#reading-392) | XI.27 | [Read](sources/meditations-george-long-gutenberg.txt#L6760-L6765) |
| [393](readings/book-11.md#reading-393) | XI.28 | [Read](sources/meditations-george-long-gutenberg.txt#L6765-L6770) |
| [394](readings/book-11.md#reading-394) | XI.29 | [Read](sources/meditations-george-long-gutenberg.txt#L6770-L6774) |
| [395](readings/book-11.md#reading-395) | XI.30 | [Read](sources/meditations-george-long-gutenberg.txt#L6774-L6776) |
| [396](readings/book-11.md#reading-396) | XI.31 | [Read](sources/meditations-george-long-gutenberg.txt#L6776-L6779) |
| [397](readings/book-11.md#reading-397) | XI.32 | [Read](sources/meditations-george-long-gutenberg.txt#L6779-L6782) |
| [398](readings/book-11.md#reading-398) | XI.33 | [Read](sources/meditations-george-long-gutenberg.txt#L6782-L6786) |
| [399](readings/book-11.md#reading-399) | XI.34 | [Read](sources/meditations-george-long-gutenberg.txt#L6786-L6792) |
| [400](readings/book-11.md#reading-400) | XI.35 | [Read](sources/meditations-george-long-gutenberg.txt#L6792-L6796) |
| [401](readings/book-11.md#reading-401) | XI.36 | [Read](sources/meditations-george-long-gutenberg.txt#L6796-L6798) |
| [402](readings/book-11.md#reading-402) | XI.37–38 | [Read](sources/meditations-george-long-gutenberg.txt#L6798-L6809) |
| [403](readings/book-11.md#reading-403) | XI.39 | [Read](sources/meditations-george-long-gutenberg.txt#L6809-L6812) |

</details>

<details>

<summary>Book XII</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [404](readings/book-12.md#reading-404) | XII.1 | [Read](sources/meditations-george-long-gutenberg.txt#L6820-L6841) |
| [405](readings/book-12.md#reading-405) | XII.2 | [Read](sources/meditations-george-long-gutenberg.txt#L6841-L6850) |
| [406](readings/book-12.md#reading-406) | XII.3–4 | [Read](sources/meditations-george-long-gutenberg.txt#L6850-L6890) |
| [407](readings/book-12.md#reading-407) | XII.5 | [Read](sources/meditations-george-long-gutenberg.txt#L6890-L6907) |
| [408](readings/book-12.md#reading-408) | XII.6 | [Read](sources/meditations-george-long-gutenberg.txt#L6907-L6912) |
| [409](readings/book-12.md#reading-409) | XII.7 | [Read](sources/meditations-george-long-gutenberg.txt#L6912-L6916) |
| [410](readings/book-12.md#reading-410) | XII.8 | [Read](sources/meditations-george-long-gutenberg.txt#L6916-L6921) |
| [411](readings/book-12.md#reading-411) | XII.9 | [Read](sources/meditations-george-long-gutenberg.txt#L6921-L6926) |
| [412](readings/book-12.md#reading-412) | XII.10 | [Read](sources/meditations-george-long-gutenberg.txt#L6926-L6929) |
| [413](readings/book-12.md#reading-413) | XII.11 | [Read](sources/meditations-george-long-gutenberg.txt#L6929-L6932) |
| [414](readings/book-12.md#reading-414) | XII.12 | [Read](sources/meditations-george-long-gutenberg.txt#L6932-L6938) |
| [415](readings/book-12.md#reading-415) | XII.13 | [Read](sources/meditations-george-long-gutenberg.txt#L6938-L6941) |
| [416](readings/book-12.md#reading-416) | XII.14 | [Read](sources/meditations-george-long-gutenberg.txt#L6941-L6952) |
| [417](readings/book-12.md#reading-417) | XII.15 | [Read](sources/meditations-george-long-gutenberg.txt#L6952-L6956) |
| [418](readings/book-12.md#reading-418) | XII.16–17 | [Read](sources/meditations-george-long-gutenberg.txt#L6956-L6976) |
| [419](readings/book-12.md#reading-419) | XII.18 | [Read](sources/meditations-george-long-gutenberg.txt#L6976-L6980) |
| [420](readings/book-12.md#reading-420) | XII.19 | [Read](sources/meditations-george-long-gutenberg.txt#L6980-L6985) |
| [421](readings/book-12.md#reading-421) | XII.20 | [Read](sources/meditations-george-long-gutenberg.txt#L6985-L6988) |
| [422](readings/book-12.md#reading-422) | XII.21 | [Read](sources/meditations-george-long-gutenberg.txt#L6988-L6994) |
| [423](readings/book-12.md#reading-423) | XII.22 | [Read](sources/meditations-george-long-gutenberg.txt#L6994-L6999) |
| [424](readings/book-12.md#reading-424) | XII.23 | [Read](sources/meditations-george-long-gutenberg.txt#L6999-L7019) |
| [425](readings/book-12.md#reading-425) | XII.24 | [Read](sources/meditations-george-long-gutenberg.txt#L7019-L7035) |
| [426](readings/book-12.md#reading-426) | XII.25 | [Read](sources/meditations-george-long-gutenberg.txt#L7035-L7038) |
| [427](readings/book-12.md#reading-427) | XII.26 | [Read](sources/meditations-george-long-gutenberg.txt#L7038-L7054) |
| [428](readings/book-12.md#reading-428) | XII.27 | [Read](sources/meditations-george-long-gutenberg.txt#L7054-L7071) |
| [429](readings/book-12.md#reading-429) | XII.28 | [Read](sources/meditations-george-long-gutenberg.txt#L7071-L7104) |
| [430](readings/book-12.md#reading-430) | XII.29 | [Read](sources/meditations-george-long-gutenberg.txt#L7104-L7110) |
| [431](readings/book-12.md#reading-431) | XII.30 | [Read](sources/meditations-george-long-gutenberg.txt#L7110-L7125) |
| [432](readings/book-12.md#reading-432) | XII.31 | [Read](sources/meditations-george-long-gutenberg.txt#L7125-L7133) |
| [433](readings/book-12.md#reading-433) | XII.32 | [Read](sources/meditations-george-long-gutenberg.txt#L7133-L7141) |
| [434](readings/book-12.md#reading-434) | XII.33 | [Read](sources/meditations-george-long-gutenberg.txt#L7141-L7145) |
| [435](readings/book-12.md#reading-435) | XII.34 | [Read](sources/meditations-george-long-gutenberg.txt#L7145-L7149) |
| [436](readings/book-12.md#reading-436) | XII.35 | [Read](sources/meditations-george-long-gutenberg.txt#L7149-L7155) |
| [437](readings/book-12.md#reading-437) | XII.36 | [Read](sources/meditations-george-long-gutenberg.txt#L7155-L7170) |

</details>
