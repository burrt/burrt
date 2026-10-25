# Meditations reading plan

437 readings cover all 487 numbered sections of the twelve books, in order.
Each reading opens on its own page, with ← and → navigation.
Only the selected passage is displayed.
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

Run these checks after changing output or rendering code, and again if a
merge or daily update changes the final files. The test suite also checks
the actual README against saved progress and verifies every generated archive
page against the current renderer. All of these checks are read-only.

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
| [1](readings/reading-001.md) | I.1–4 | [Read](sources/meditations-george-long-gutenberg.txt#L2132-L2165) |
| [2](readings/reading-002.md) | I.5 | [Read](sources/meditations-george-long-gutenberg.txt#L2165-L2172) |
| [3](readings/reading-003.md) | I.6 | [Read](sources/meditations-george-long-gutenberg.txt#L2172-L2194) |
| [4](readings/reading-004.md) | I.7 | [Read](sources/meditations-george-long-gutenberg.txt#L2194-L2222) |
| [5](readings/reading-005.md) | I.8 | [Read](sources/meditations-george-long-gutenberg.txt#L2222-L2237) |
| [6](readings/reading-006.md) | I.9–13 | [Read](sources/meditations-george-long-gutenberg.txt#L2237-L2286) |
| [7](readings/reading-007.md) | I.14 | [Read](sources/meditations-george-long-gutenberg.txt#L2286-L2310) |
| [8](readings/reading-008.md) | I.15 | [Read](sources/meditations-george-long-gutenberg.txt#L2310-L2331) |
| [9](readings/reading-009.md) | I.16 | [Read](sources/meditations-george-long-gutenberg.txt#L2331-L2418) |
| [10](readings/reading-010.md) | I.17 | [Read](sources/meditations-george-long-gutenberg.txt#L2418-L2488) |

</details>

<details>

<summary>Book II</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [11](readings/reading-011.md) | II.1 | [Read](sources/meditations-george-long-gutenberg.txt#L2496-L2512) |
| [12](readings/reading-012.md) | II.2 | [Read](sources/meditations-george-long-gutenberg.txt#L2512-L2523) |
| [13](readings/reading-013.md) | II.3–4 | [Read](sources/meditations-george-long-gutenberg.txt#L2523-L2544) |
| [14](readings/reading-014.md) | II.5 | [Read](sources/meditations-george-long-gutenberg.txt#L2544-L2556) |
| [15](readings/reading-015.md) | II.6 | [Read](sources/meditations-george-long-gutenberg.txt#L2556-L2564) |
| [16](readings/reading-016.md) | II.7 | [Read](sources/meditations-george-long-gutenberg.txt#L2564-L2571) |
| [17](readings/reading-017.md) | II.8 | [Read](sources/meditations-george-long-gutenberg.txt#L2571-L2575) |
| [18](readings/reading-018.md) | II.9 | [Read](sources/meditations-george-long-gutenberg.txt#L2575-L2581) |
| [19](readings/reading-019.md) | II.10 | [Read](sources/meditations-george-long-gutenberg.txt#L2581-L2596) |
| [20](readings/reading-020.md) | II.11 | [Read](sources/meditations-george-long-gutenberg.txt#L2596-L2622) |
| [21](readings/reading-021.md) | II.12 | [Read](sources/meditations-george-long-gutenberg.txt#L2622-L2639) |
| [22](readings/reading-022.md) | II.13 | [Read](sources/meditations-george-long-gutenberg.txt#L2639-L2654) |
| [23](readings/reading-023.md) | II.14 | [Read](sources/meditations-george-long-gutenberg.txt#L2654-L2673) |
| [24](readings/reading-024.md) | II.15 | [Read](sources/meditations-george-long-gutenberg.txt#L2673-L2677) |
| [25](readings/reading-025.md) | II.16 | [Read](sources/meditations-george-long-gutenberg.txt#L2677-L2693) |
| [26](readings/reading-026.md) | II.17 | [Read](sources/meditations-george-long-gutenberg.txt#L2693-L2720) |

</details>

<details>

<summary>Book III</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [27](readings/reading-027.md) | III.1 | [Read](sources/meditations-george-long-gutenberg.txt#L2728-L2744) |
| [28](readings/reading-028.md) | III.2 | [Read](sources/meditations-george-long-gutenberg.txt#L2744-L2769) |
| [29](readings/reading-029.md) | III.3 | [Read](sources/meditations-george-long-gutenberg.txt#L2769-L2785) |
| [30](readings/reading-030.md) | III.4 | [Read](sources/meditations-george-long-gutenberg.txt#L2785-L2825) |
| [31](readings/reading-031.md) | III.5 | [Read](sources/meditations-george-long-gutenberg.txt#L2825-L2836) |
| [32](readings/reading-032.md) | III.6 | [Read](sources/meditations-george-long-gutenberg.txt#L2836-L2862) |
| [33](readings/reading-033.md) | III.7 | [Read](sources/meditations-george-long-gutenberg.txt#L2862-L2879) |
| [34](readings/reading-034.md) | III.8 | [Read](sources/meditations-george-long-gutenberg.txt#L2879-L2889) |
| [35](readings/reading-035.md) | III.9–11 | [Read](sources/meditations-george-long-gutenberg.txt#L2889-L2932) |
| [36](readings/reading-036.md) | III.12 | [Read](sources/meditations-george-long-gutenberg.txt#L2932-L2941) |
| [37](readings/reading-037.md) | III.13 | [Read](sources/meditations-george-long-gutenberg.txt#L2941-L2949) |
| [38](readings/reading-038.md) | III.14 | [Read](sources/meditations-george-long-gutenberg.txt#L2949-L2964) |
| [39](readings/reading-039.md) | III.15 | [Read](sources/meditations-george-long-gutenberg.txt#L2964-L2968) |
| [40](readings/reading-040.md) | III.16 | [Read](sources/meditations-george-long-gutenberg.txt#L2968-L2989) |

</details>

<details>

<summary>Book IV</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [41](readings/reading-041.md) | IV.1 | [Read](sources/meditations-george-long-gutenberg.txt#L2997-L3010) |
| [42](readings/reading-042.md) | IV.2 | [Read](sources/meditations-george-long-gutenberg.txt#L3010-L3013) |
| [43](readings/reading-043.md) | IV.3 | [Read](sources/meditations-george-long-gutenberg.txt#L3013-L3064) |
| [44](readings/reading-044.md) | IV.4 | [Read](sources/meditations-george-long-gutenberg.txt#L3064-L3082) |
| [45](readings/reading-045.md) | IV.5 | [Read](sources/meditations-george-long-gutenberg.txt#L3082-L3088) |
| [46](readings/reading-046.md) | IV.6 | [Read](sources/meditations-george-long-gutenberg.txt#L3088-L3094) |
| [47](readings/reading-047.md) | IV.7 | [Read](sources/meditations-george-long-gutenberg.txt#L3094-L3098) |
| [48](readings/reading-048.md) | IV.8 | [Read](sources/meditations-george-long-gutenberg.txt#L3098-L3101) |
| [49](readings/reading-049.md) | IV.9–10 | [Read](sources/meditations-george-long-gutenberg.txt#L3101-L3112) |
| [50](readings/reading-050.md) | IV.11 | [Read](sources/meditations-george-long-gutenberg.txt#L3112-L3116) |
| [51](readings/reading-051.md) | IV.12 | [Read](sources/meditations-george-long-gutenberg.txt#L3116-L3124) |
| [52](readings/reading-052.md) | IV.13 | [Read](sources/meditations-george-long-gutenberg.txt#L3124-L3127) |
| [53](readings/reading-053.md) | IV.14–15 | [Read](sources/meditations-george-long-gutenberg.txt#L3127-L3134) |
| [54](readings/reading-054.md) | IV.16 | [Read](sources/meditations-george-long-gutenberg.txt#L3134-L3138) |
| [55](readings/reading-055.md) | IV.17 | [Read](sources/meditations-george-long-gutenberg.txt#L3138-L3141) |
| [56](readings/reading-056.md) | IV.18 | [Read](sources/meditations-george-long-gutenberg.txt#L3141-L3147) |
| [57](readings/reading-057.md) | IV.19 | [Read](sources/meditations-george-long-gutenberg.txt#L3147-L3158) |
| [58](readings/reading-058.md) | IV.20 | [Read](sources/meditations-george-long-gutenberg.txt#L3158-L3171) |
| [59](readings/reading-059.md) | IV.21 | [Read](sources/meditations-george-long-gutenberg.txt#L3171-L3192) |
| [60](readings/reading-060.md) | IV.22 | [Read](sources/meditations-george-long-gutenberg.txt#L3192-L3196) |
| [61](readings/reading-061.md) | IV.23 | [Read](sources/meditations-george-long-gutenberg.txt#L3196-L3203) |
| [62](readings/reading-062.md) | IV.24 | [Read](sources/meditations-george-long-gutenberg.txt#L3203-L3215) |
| [63](readings/reading-063.md) | IV.25–26 | [Read](sources/meditations-george-long-gutenberg.txt#L3215-L3227) |
| [64](readings/reading-064.md) | IV.27 | [Read](sources/meditations-george-long-gutenberg.txt#L3227-L3236) |
| [65](readings/reading-065.md) | IV.28–29 | [Read](sources/meditations-george-long-gutenberg.txt#L3236-L3251) |
| [66](readings/reading-066.md) | IV.30 | [Read](sources/meditations-george-long-gutenberg.txt#L3251-L3256) |
| [67](readings/reading-067.md) | IV.31 | [Read](sources/meditations-george-long-gutenberg.txt#L3256-L3261) |
| [68](readings/reading-068.md) | IV.32 | [Read](sources/meditations-george-long-gutenberg.txt#L3261-L3279) |
| [69](readings/reading-069.md) | IV.33 | [Read](sources/meditations-george-long-gutenberg.txt#L3279-L3293) |
| [70](readings/reading-070.md) | IV.34 | [Read](sources/meditations-george-long-gutenberg.txt#L3293-L3296) |
| [71](readings/reading-071.md) | IV.35 | [Read](sources/meditations-george-long-gutenberg.txt#L3296-L3299) |
| [72](readings/reading-072.md) | IV.36 | [Read](sources/meditations-george-long-gutenberg.txt#L3299-L3306) |
| [73](readings/reading-073.md) | IV.37 | [Read](sources/meditations-george-long-gutenberg.txt#L3306-L3311) |
| [74](readings/reading-074.md) | IV.38 | [Read](sources/meditations-george-long-gutenberg.txt#L3311-L3314) |
| [75](readings/reading-075.md) | IV.39 | [Read](sources/meditations-george-long-gutenberg.txt#L3314-L3326) |
| [76](readings/reading-076.md) | IV.40 | [Read](sources/meditations-george-long-gutenberg.txt#L3326-L3333) |
| [77](readings/reading-077.md) | IV.41 | [Read](sources/meditations-george-long-gutenberg.txt#L3333-L3336) |
| [78](readings/reading-078.md) | IV.42 | [Read](sources/meditations-george-long-gutenberg.txt#L3336-L3339) |
| [79](readings/reading-079.md) | IV.43 | [Read](sources/meditations-george-long-gutenberg.txt#L3339-L3343) |
| [80](readings/reading-080.md) | IV.44 | [Read](sources/meditations-george-long-gutenberg.txt#L3343-L3347) |
| [81](readings/reading-081.md) | IV.45 | [Read](sources/meditations-george-long-gutenberg.txt#L3347-L3355) |
| [82](readings/reading-082.md) | IV.46 | [Read](sources/meditations-george-long-gutenberg.txt#L3355-L3366) |
| [83](readings/reading-083.md) | IV.47 | [Read](sources/meditations-george-long-gutenberg.txt#L3366-L3373) |
| [84](readings/reading-084.md) | IV.48 | [Read](sources/meditations-george-long-gutenberg.txt#L3373-L3395) |
| [85](readings/reading-085.md) | IV.49 | [Read](sources/meditations-george-long-gutenberg.txt#L3395-L3415) |
| [86](readings/reading-086.md) | IV.50 | [Read](sources/meditations-george-long-gutenberg.txt#L3415-L3438) |
| [87](readings/reading-087.md) | IV.51 | [Read](sources/meditations-george-long-gutenberg.txt#L3438-L3441) |

</details>

<details>

<summary>Book V</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [88](readings/reading-088.md) | V.1 | [Read](sources/meditations-george-long-gutenberg.txt#L3449-L3474) |
| [89](readings/reading-089.md) | V.2 | [Read](sources/meditations-george-long-gutenberg.txt#L3474-L3477) |
| [90](readings/reading-090.md) | V.3 | [Read](sources/meditations-george-long-gutenberg.txt#L3477-L3485) |
| [91](readings/reading-091.md) | V.4 | [Read](sources/meditations-george-long-gutenberg.txt#L3485-L3493) |
| [92](readings/reading-092.md) | V.5 | [Read](sources/meditations-george-long-gutenberg.txt#L3493-L3511) |
| [93](readings/reading-093.md) | V.6 | [Read](sources/meditations-george-long-gutenberg.txt#L3511-L3532) |
| [94](readings/reading-094.md) | V.7 | [Read](sources/meditations-george-long-gutenberg.txt#L3532-L3537) |
| [95](readings/reading-095.md) | V.8 | [Read](sources/meditations-george-long-gutenberg.txt#L3537-L3582) |
| [96](readings/reading-096.md) | V.9 | [Read](sources/meditations-george-long-gutenberg.txt#L3582-L3600) |
| [97](readings/reading-097.md) | V.10 | [Read](sources/meditations-george-long-gutenberg.txt#L3600-L3620) |
| [98](readings/reading-098.md) | V.11 | [Read](sources/meditations-george-long-gutenberg.txt#L3620-L3626) |
| [99](readings/reading-099.md) | V.12–15 | [Read](sources/meditations-george-long-gutenberg.txt#L3626-L3672) |
| [100](readings/reading-100.md) | V.16 | [Read](sources/meditations-george-long-gutenberg.txt#L3672-L3689) |
| [101](readings/reading-101.md) | V.17–20 | [Read](sources/meditations-george-long-gutenberg.txt#L3689-L3715) |
| [102](readings/reading-102.md) | V.21 | [Read](sources/meditations-george-long-gutenberg.txt#L3715-L3721) |
| [103](readings/reading-103.md) | V.22 | [Read](sources/meditations-george-long-gutenberg.txt#L3721-L3727) |
| [104](readings/reading-104.md) | V.23 | [Read](sources/meditations-george-long-gutenberg.txt#L3727-L3737) |
| [105](readings/reading-105.md) | V.24 | [Read](sources/meditations-george-long-gutenberg.txt#L3737-L3742) |
| [106](readings/reading-106.md) | V.25 | [Read](sources/meditations-george-long-gutenberg.txt#L3742-L3746) |
| [107](readings/reading-107.md) | V.26 | [Read](sources/meditations-george-long-gutenberg.txt#L3746-L3755) |
| [108](readings/reading-108.md) | V.27 | [Read](sources/meditations-george-long-gutenberg.txt#L3755-L3761) |
| [109](readings/reading-109.md) | V.28–29 | [Read](sources/meditations-george-long-gutenberg.txt#L3761-L3789) |
| [110](readings/reading-110.md) | V.30 | [Read](sources/meditations-george-long-gutenberg.txt#L3789-L3796) |
| [111](readings/reading-111.md) | V.31 | [Read](sources/meditations-george-long-gutenberg.txt#L3796-L3810) |
| [112](readings/reading-112.md) | V.32 | [Read](sources/meditations-george-long-gutenberg.txt#L3810-L3816) |
| [113](readings/reading-113.md) | V.33 | [Read](sources/meditations-george-long-gutenberg.txt#L3816-L3843) |
| [114](readings/reading-114.md) | V.34–35 | [Read](sources/meditations-george-long-gutenberg.txt#L3843-L3854) |
| [115](readings/reading-115.md) | V.36 | [Read](sources/meditations-george-long-gutenberg.txt#L3854-L3873) |

</details>

<details>

<summary>Book VI</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [116](readings/reading-116.md) | VI.1 | [Read](sources/meditations-george-long-gutenberg.txt#L3881-L3886) |
| [117](readings/reading-117.md) | VI.2 | [Read](sources/meditations-george-long-gutenberg.txt#L3886-L3893) |
| [118](readings/reading-118.md) | VI.3 | [Read](sources/meditations-george-long-gutenberg.txt#L3893-L3896) |
| [119](readings/reading-119.md) | VI.4 | [Read](sources/meditations-george-long-gutenberg.txt#L3896-L3899) |
| [120](readings/reading-120.md) | VI.5 | [Read](sources/meditations-george-long-gutenberg.txt#L3899-L3902) |
| [121](readings/reading-121.md) | VI.6 | [Read](sources/meditations-george-long-gutenberg.txt#L3902-L3905) |
| [122](readings/reading-122.md) | VI.7 | [Read](sources/meditations-george-long-gutenberg.txt#L3905-L3908) |
| [123](readings/reading-123.md) | VI.8 | [Read](sources/meditations-george-long-gutenberg.txt#L3908-L3912) |
| [124](readings/reading-124.md) | VI.9 | [Read](sources/meditations-george-long-gutenberg.txt#L3912-L3918) |
| [125](readings/reading-125.md) | VI.10 | [Read](sources/meditations-george-long-gutenberg.txt#L3918-L3927) |
| [126](readings/reading-126.md) | VI.11 | [Read](sources/meditations-george-long-gutenberg.txt#L3927-L3932) |
| [127](readings/reading-127.md) | VI.12 | [Read](sources/meditations-george-long-gutenberg.txt#L3932-L3939) |
| [128](readings/reading-128.md) | VI.13 | [Read](sources/meditations-george-long-gutenberg.txt#L3939-L3953) |
| [129](readings/reading-129.md) | VI.14 | [Read](sources/meditations-george-long-gutenberg.txt#L3953-L3969) |
| [130](readings/reading-130.md) | VI.15 | [Read](sources/meditations-george-long-gutenberg.txt#L3969-L3984) |
| [131](readings/reading-131.md) | VI.16 | [Read](sources/meditations-george-long-gutenberg.txt#L3984-L4013) |
| [132](readings/reading-132.md) | VI.17 | [Read](sources/meditations-george-long-gutenberg.txt#L4013-L4017) |
| [133](readings/reading-133.md) | VI.18 | [Read](sources/meditations-george-long-gutenberg.txt#L4017-L4024) |
| [134](readings/reading-134.md) | VI.19 | [Read](sources/meditations-george-long-gutenberg.txt#L4024-L4029) |
| [135](readings/reading-135.md) | VI.20 | [Read](sources/meditations-george-long-gutenberg.txt#L4029-L4039) |
| [136](readings/reading-136.md) | VI.21 | [Read](sources/meditations-george-long-gutenberg.txt#L4039-L4044) |
| [137](readings/reading-137.md) | VI.22 | [Read](sources/meditations-george-long-gutenberg.txt#L4044-L4048) |
| [138](readings/reading-138.md) | VI.23 | [Read](sources/meditations-george-long-gutenberg.txt#L4048-L4056) |
| [139](readings/reading-139.md) | VI.24 | [Read](sources/meditations-george-long-gutenberg.txt#L4056-L4061) |
| [140](readings/reading-140.md) | VI.25 | [Read](sources/meditations-george-long-gutenberg.txt#L4061-L4067) |
| [141](readings/reading-141.md) | VI.26 | [Read](sources/meditations-george-long-gutenberg.txt#L4067-L4076) |
| [142](readings/reading-142.md) | VI.27 | [Read](sources/meditations-george-long-gutenberg.txt#L4076-L4084) |
| [143](readings/reading-143.md) | VI.28 | [Read](sources/meditations-george-long-gutenberg.txt#L4084-L4089) |
| [144](readings/reading-144.md) | VI.29 | [Read](sources/meditations-george-long-gutenberg.txt#L4089-L4092) |
| [145](readings/reading-145.md) | VI.30 | [Read](sources/meditations-george-long-gutenberg.txt#L4092-L4119) |
| [146](readings/reading-146.md) | VI.31 | [Read](sources/meditations-george-long-gutenberg.txt#L4119-L4124) |
| [147](readings/reading-147.md) | VI.32 | [Read](sources/meditations-george-long-gutenberg.txt#L4124-L4133) |
| [148](readings/reading-148.md) | VI.33 | [Read](sources/meditations-george-long-gutenberg.txt#L4133-L4139) |
| [149](readings/reading-149.md) | VI.34 | [Read](sources/meditations-george-long-gutenberg.txt#L4139-L4142) |
| [150](readings/reading-150.md) | VI.35 | [Read](sources/meditations-george-long-gutenberg.txt#L4142-L4150) |
| [151](readings/reading-151.md) | VI.36 | [Read](sources/meditations-george-long-gutenberg.txt#L4150-L4160) |
| [152](readings/reading-152.md) | VI.37 | [Read](sources/meditations-george-long-gutenberg.txt#L4160-L4164) |
| [153](readings/reading-153.md) | VI.38 | [Read](sources/meditations-george-long-gutenberg.txt#L4164-L4171) |
| [154](readings/reading-154.md) | VI.39 | [Read](sources/meditations-george-long-gutenberg.txt#L4171-L4175) |
| [155](readings/reading-155.md) | VI.40 | [Read](sources/meditations-george-long-gutenberg.txt#L4175-L4184) |
| [156](readings/reading-156.md) | VI.41 | [Read](sources/meditations-george-long-gutenberg.txt#L4184-L4202) |
| [157](readings/reading-157.md) | VI.42 | [Read](sources/meditations-george-long-gutenberg.txt#L4202-L4218) |
| [158](readings/reading-158.md) | VI.43 | [Read](sources/meditations-george-long-gutenberg.txt#L4218-L4223) |
| [159](readings/reading-159.md) | VI.44 | [Read](sources/meditations-george-long-gutenberg.txt#L4223-L4243) |
| [160](readings/reading-160.md) | VI.45 | [Read](sources/meditations-george-long-gutenberg.txt#L4243-L4250) |
| [161](readings/reading-161.md) | VI.46 | [Read](sources/meditations-george-long-gutenberg.txt#L4250-L4255) |
| [162](readings/reading-162.md) | VI.47 | [Read](sources/meditations-george-long-gutenberg.txt#L4255-L4270) |
| [163](readings/reading-163.md) | VI.48 | [Read](sources/meditations-george-long-gutenberg.txt#L4270-L4278) |
| [164](readings/reading-164.md) | VI.49 | [Read](sources/meditations-george-long-gutenberg.txt#L4278-L4284) |
| [165](readings/reading-165.md) | VI.50 | [Read](sources/meditations-george-long-gutenberg.txt#L4284-L4294) |
| [166](readings/reading-166.md) | VI.51 | [Read](sources/meditations-george-long-gutenberg.txt#L4294-L4298) |
| [167](readings/reading-167.md) | VI.52 | [Read](sources/meditations-george-long-gutenberg.txt#L4298-L4302) |
| [168](readings/reading-168.md) | VI.53 | [Read](sources/meditations-george-long-gutenberg.txt#L4302-L4305) |
| [169](readings/reading-169.md) | VI.54 | [Read](sources/meditations-george-long-gutenberg.txt#L4305-L4308) |
| [170](readings/reading-170.md) | VI.55 | [Read](sources/meditations-george-long-gutenberg.txt#L4308-L4312) |
| [171](readings/reading-171.md) | VI.56 | [Read](sources/meditations-george-long-gutenberg.txt#L4312-L4315) |
| [172](readings/reading-172.md) | VI.57 | [Read](sources/meditations-george-long-gutenberg.txt#L4315-L4321) |
| [173](readings/reading-173.md) | VI.58 | [Read](sources/meditations-george-long-gutenberg.txt#L4321-L4325) |
| [174](readings/reading-174.md) | VI.59 | [Read](sources/meditations-george-long-gutenberg.txt#L4325-L4327) |

</details>

<details>

<summary>Book VII</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [175](readings/reading-175.md) | VII.1 | [Read](sources/meditations-george-long-gutenberg.txt#L4335-L4343) |
| [176](readings/reading-176.md) | VII.2 | [Read](sources/meditations-george-long-gutenberg.txt#L4343-L4352) |
| [177](readings/reading-177.md) | VII.3 | [Read](sources/meditations-george-long-gutenberg.txt#L4352-L4360) |
| [178](readings/reading-178.md) | VII.4 | [Read](sources/meditations-george-long-gutenberg.txt#L4360-L4365) |
| [179](readings/reading-179.md) | VII.5 | [Read](sources/meditations-george-long-gutenberg.txt#L4365-L4375) |
| [180](readings/reading-180.md) | VII.6 | [Read](sources/meditations-george-long-gutenberg.txt#L4375-L4379) |
| [181](readings/reading-181.md) | VII.7 | [Read](sources/meditations-george-long-gutenberg.txt#L4379-L4384) |
| [182](readings/reading-182.md) | VII.8 | [Read](sources/meditations-george-long-gutenberg.txt#L4384-L4388) |
| [183](readings/reading-183.md) | VII.9 | [Read](sources/meditations-george-long-gutenberg.txt#L4388-L4399) |
| [184](readings/reading-184.md) | VII.10 | [Read](sources/meditations-george-long-gutenberg.txt#L4399-L4404) |
| [185](readings/reading-185.md) | VII.11 | [Read](sources/meditations-george-long-gutenberg.txt#L4404-L4407) |
| [186](readings/reading-186.md) | VII.12 | [Read](sources/meditations-george-long-gutenberg.txt#L4407-L4409) |
| [187](readings/reading-187.md) | VII.13 | [Read](sources/meditations-george-long-gutenberg.txt#L4409-L4423) |
| [188](readings/reading-188.md) | VII.14 | [Read](sources/meditations-george-long-gutenberg.txt#L4423-L4428) |
| [189](readings/reading-189.md) | VII.15 | [Read](sources/meditations-george-long-gutenberg.txt#L4428-L4432) |
| [190](readings/reading-190.md) | VII.16 | [Read](sources/meditations-george-long-gutenberg.txt#L4432-L4444) |
| [191](readings/reading-191.md) | VII.17 | [Read](sources/meditations-george-long-gutenberg.txt#L4444-L4449) |
| [192](readings/reading-192.md) | VII.18 | [Read](sources/meditations-george-long-gutenberg.txt#L4449-L4457) |
| [193](readings/reading-193.md) | VII.19 | [Read](sources/meditations-george-long-gutenberg.txt#L4457-L4464) |
| [194](readings/reading-194.md) | VII.20 | [Read](sources/meditations-george-long-gutenberg.txt#L4464-L4468) |
| [195](readings/reading-195.md) | VII.21 | [Read](sources/meditations-george-long-gutenberg.txt#L4468-L4471) |
| [196](readings/reading-196.md) | VII.22 | [Read](sources/meditations-george-long-gutenberg.txt#L4471-L4478) |
| [197](readings/reading-197.md) | VII.23 | [Read](sources/meditations-george-long-gutenberg.txt#L4478-L4485) |
| [198](readings/reading-198.md) | VII.24 | [Read](sources/meditations-george-long-gutenberg.txt#L4485-L4494) |
| [199](readings/reading-199.md) | VII.25 | [Read](sources/meditations-george-long-gutenberg.txt#L4494-L4499) |
| [200](readings/reading-200.md) | VII.26 | [Read](sources/meditations-george-long-gutenberg.txt#L4499-L4507) |
| [201](readings/reading-201.md) | VII.27 | [Read](sources/meditations-george-long-gutenberg.txt#L4507-L4514) |
| [202](readings/reading-202.md) | VII.28 | [Read](sources/meditations-george-long-gutenberg.txt#L4514-L4518) |
| [203](readings/reading-203.md) | VII.29 | [Read](sources/meditations-george-long-gutenberg.txt#L4518-L4524) |
| [204](readings/reading-204.md) | VII.30 | [Read](sources/meditations-george-long-gutenberg.txt#L4524-L4527) |
| [205](readings/reading-205.md) | VII.31 | [Read](sources/meditations-george-long-gutenberg.txt#L4527-L4534) |
| [206](readings/reading-206.md) | VII.32 | [Read](sources/meditations-george-long-gutenberg.txt#L4534-L4537) |
| [207](readings/reading-207.md) | VII.33 | [Read](sources/meditations-george-long-gutenberg.txt#L4537-L4543) |
| [208](readings/reading-208.md) | VII.34 | [Read](sources/meditations-george-long-gutenberg.txt#L4543-L4549) |
| [209](readings/reading-209.md) | VII.35–40 | [Read](sources/meditations-george-long-gutenberg.txt#L4549-L4580) |
| [210](readings/reading-210.md) | VII.41–45 | [Read](sources/meditations-george-long-gutenberg.txt#L4580-L4606) |
| [211](readings/reading-211.md) | VII.46–48 | [Read](sources/meditations-george-long-gutenberg.txt#L4606-L4637) |
| [212](readings/reading-212.md) | VII.49 | [Read](sources/meditations-george-long-gutenberg.txt#L4637-L4644) |
| [213](readings/reading-213.md) | VII.50–51 | [Read](sources/meditations-george-long-gutenberg.txt#L4644-L4661) |
| [214](readings/reading-214.md) | VII.52 | [Read](sources/meditations-george-long-gutenberg.txt#L4661-L4666) |
| [215](readings/reading-215.md) | VII.53 | [Read](sources/meditations-george-long-gutenberg.txt#L4666-L4671) |
| [216](readings/reading-216.md) | VII.54 | [Read](sources/meditations-george-long-gutenberg.txt#L4671-L4676) |
| [217](readings/reading-217.md) | VII.55 | [Read](sources/meditations-george-long-gutenberg.txt#L4676-L4696) |
| [218](readings/reading-218.md) | VII.56 | [Read](sources/meditations-george-long-gutenberg.txt#L4696-L4700) |
| [219](readings/reading-219.md) | VII.57 | [Read](sources/meditations-george-long-gutenberg.txt#L4700-L4703) |
| [220](readings/reading-220.md) | VII.58 | [Read](sources/meditations-george-long-gutenberg.txt#L4703-L4719) |
| [221](readings/reading-221.md) | VII.59 | [Read](sources/meditations-george-long-gutenberg.txt#L4719-L4722) |
| [222](readings/reading-222.md) | VII.60 | [Read](sources/meditations-george-long-gutenberg.txt#L4722-L4728) |
| [223](readings/reading-223.md) | VII.61 | [Read](sources/meditations-george-long-gutenberg.txt#L4728-L4732) |
| [224](readings/reading-224.md) | VII.62 | [Read](sources/meditations-george-long-gutenberg.txt#L4732-L4738) |
| [225](readings/reading-225.md) | VII.63 | [Read](sources/meditations-george-long-gutenberg.txt#L4738-L4744) |
| [226](readings/reading-226.md) | VII.64–66 | [Read](sources/meditations-george-long-gutenberg.txt#L4744-L4788) |
| [227](readings/reading-227.md) | VII.67 | [Read](sources/meditations-george-long-gutenberg.txt#L4788-L4798) |
| [228](readings/reading-228.md) | VII.68 | [Read](sources/meditations-george-long-gutenberg.txt#L4798-L4815) |
| [229](readings/reading-229.md) | VII.69 | [Read](sources/meditations-george-long-gutenberg.txt#L4815-L4819) |
| [230](readings/reading-230.md) | VII.70 | [Read](sources/meditations-george-long-gutenberg.txt#L4819-L4825) |
| [231](readings/reading-231.md) | VII.71 | [Read](sources/meditations-george-long-gutenberg.txt#L4825-L4829) |
| [232](readings/reading-232.md) | VII.72 | [Read](sources/meditations-george-long-gutenberg.txt#L4829-L4833) |
| [233](readings/reading-233.md) | VII.73 | [Read](sources/meditations-george-long-gutenberg.txt#L4833-L4837) |
| [234](readings/reading-234.md) | VII.74 | [Read](sources/meditations-george-long-gutenberg.txt#L4837-L4841) |
| [235](readings/reading-235.md) | VII.75 | [Read](sources/meditations-george-long-gutenberg.txt#L4841-L4928) |

</details>

<details>

<summary>Book VIII</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [236](readings/reading-236.md) | VIII.1 | [Read](sources/meditations-george-long-gutenberg.txt#L4936-L4956) |
| [237](readings/reading-237.md) | VIII.2 | [Read](sources/meditations-george-long-gutenberg.txt#L4956-L4962) |
| [238](readings/reading-238.md) | VIII.3 | [Read](sources/meditations-george-long-gutenberg.txt#L4962-L4972) |
| [239](readings/reading-239.md) | VIII.4 | [Read](sources/meditations-george-long-gutenberg.txt#L4972-L4975) |
| [240](readings/reading-240.md) | VIII.5 | [Read](sources/meditations-george-long-gutenberg.txt#L4975-L4984) |
| [241](readings/reading-241.md) | VIII.6 | [Read](sources/meditations-george-long-gutenberg.txt#L4984-L4990) |
| [242](readings/reading-242.md) | VIII.7 | [Read](sources/meditations-george-long-gutenberg.txt#L4990-L5008) |
| [243](readings/reading-243.md) | VIII.8 | [Read](sources/meditations-george-long-gutenberg.txt#L5008-L5014) |
| [244](readings/reading-244.md) | VIII.9 | [Read](sources/meditations-george-long-gutenberg.txt#L5014-L5017) |
| [245](readings/reading-245.md) | VIII.10 | [Read](sources/meditations-george-long-gutenberg.txt#L5017-L5023) |
| [246](readings/reading-246.md) | VIII.11 | [Read](sources/meditations-george-long-gutenberg.txt#L5023-L5027) |
| [247](readings/reading-247.md) | VIII.12 | [Read](sources/meditations-george-long-gutenberg.txt#L5027-L5034) |
| [248](readings/reading-248.md) | VIII.13 | [Read](sources/meditations-george-long-gutenberg.txt#L5034-L5038) |
| [249](readings/reading-249.md) | VIII.14 | [Read](sources/meditations-george-long-gutenberg.txt#L5038-L5049) |
| [250](readings/reading-250.md) | VIII.15 | [Read](sources/meditations-george-long-gutenberg.txt#L5049-L5055) |
| [251](readings/reading-251.md) | VIII.16 | [Read](sources/meditations-george-long-gutenberg.txt#L5055-L5061) |
| [252](readings/reading-252.md) | VIII.17 | [Read](sources/meditations-george-long-gutenberg.txt#L5061-L5069) |
| [253](readings/reading-253.md) | VIII.18 | [Read](sources/meditations-george-long-gutenberg.txt#L5069-L5074) |
| [254](readings/reading-254.md) | VIII.19 | [Read](sources/meditations-george-long-gutenberg.txt#L5074-L5079) |
| [255](readings/reading-255.md) | VIII.20 | [Read](sources/meditations-george-long-gutenberg.txt#L5079-L5086) |
| [256](readings/reading-256.md) | VIII.21 | [Read](sources/meditations-george-long-gutenberg.txt#L5086-L5095) |
| [257](readings/reading-257.md) | VIII.22 | [Read](sources/meditations-george-long-gutenberg.txt#L5095-L5101) |
| [258](readings/reading-258.md) | VIII.23 | [Read](sources/meditations-george-long-gutenberg.txt#L5101-L5105) |
| [259](readings/reading-259.md) | VIII.24 | [Read](sources/meditations-george-long-gutenberg.txt#L5105-L5108) |
| [260](readings/reading-260.md) | VIII.25 | [Read](sources/meditations-george-long-gutenberg.txt#L5108-L5121) |
| [261](readings/reading-261.md) | VIII.26 | [Read](sources/meditations-george-long-gutenberg.txt#L5121-L5127) |
| [262](readings/reading-262.md) | VIII.27 | [Read](sources/meditations-george-long-gutenberg.txt#L5127-L5136) |
| [263](readings/reading-263.md) | VIII.28 | [Read](sources/meditations-george-long-gutenberg.txt#L5136-L5142) |
| [264](readings/reading-264.md) | VIII.29 | [Read](sources/meditations-george-long-gutenberg.txt#L5142-L5148) |
| [265](readings/reading-265.md) | VIII.30 | [Read](sources/meditations-george-long-gutenberg.txt#L5148-L5151) |
| [266](readings/reading-266.md) | VIII.31 | [Read](sources/meditations-george-long-gutenberg.txt#L5151-L5164) |
| [267](readings/reading-267.md) | VIII.32 | [Read](sources/meditations-george-long-gutenberg.txt#L5164-L5175) |
| [268](readings/reading-268.md) | VIII.33 | [Read](sources/meditations-george-long-gutenberg.txt#L5175-L5178) |
| [269](readings/reading-269.md) | VIII.34 | [Read](sources/meditations-george-long-gutenberg.txt#L5178-L5192) |
| [270](readings/reading-270.md) | VIII.35–37 | [Read](sources/meditations-george-long-gutenberg.txt#L5192-L5226) |
| [271](readings/reading-271.md) | VIII.38 | [Read](sources/meditations-george-long-gutenberg.txt#L5226-L5229) |
| [272](readings/reading-272.md) | VIII.39 | [Read](sources/meditations-george-long-gutenberg.txt#L5229-L5233) |
| [273](readings/reading-273.md) | VIII.40 | [Read](sources/meditations-george-long-gutenberg.txt#L5233-L5239) |
| [274](readings/reading-274.md) | VIII.41 | [Read](sources/meditations-george-long-gutenberg.txt#L5239-L5255) |
| [275](readings/reading-275.md) | VIII.42 | [Read](sources/meditations-george-long-gutenberg.txt#L5255-L5258) |
| [276](readings/reading-276.md) | VIII.43 | [Read](sources/meditations-george-long-gutenberg.txt#L5258-L5264) |
| [277](readings/reading-277.md) | VIII.44 | [Read](sources/meditations-george-long-gutenberg.txt#L5264-L5270) |
| [278](readings/reading-278.md) | VIII.45 | [Read](sources/meditations-george-long-gutenberg.txt#L5270-L5282) |
| [279](readings/reading-279.md) | VIII.46 | [Read](sources/meditations-george-long-gutenberg.txt#L5282-L5289) |
| [280](readings/reading-280.md) | VIII.47 | [Read](sources/meditations-george-long-gutenberg.txt#L5289-L5301) |
| [281](readings/reading-281.md) | VIII.48 | [Read](sources/meditations-george-long-gutenberg.txt#L5301-L5310) |
| [282](readings/reading-282.md) | VIII.49 | [Read](sources/meditations-george-long-gutenberg.txt#L5310-L5319) |
| [283](readings/reading-283.md) | VIII.50 | [Read](sources/meditations-george-long-gutenberg.txt#L5319-L5334) |
| [284](readings/reading-284.md) | VIII.51 | [Read](sources/meditations-george-long-gutenberg.txt#L5334-L5349) |
| [285](readings/reading-285.md) | VIII.52 | [Read](sources/meditations-george-long-gutenberg.txt#L5349-L5357) |
| [286](readings/reading-286.md) | VIII.53 | [Read](sources/meditations-george-long-gutenberg.txt#L5357-L5362) |
| [287](readings/reading-287.md) | VIII.54 | [Read](sources/meditations-george-long-gutenberg.txt#L5362-L5369) |
| [288](readings/reading-288.md) | VIII.55 | [Read](sources/meditations-george-long-gutenberg.txt#L5369-L5374) |
| [289](readings/reading-289.md) | VIII.56 | [Read](sources/meditations-george-long-gutenberg.txt#L5374-L5381) |
| [290](readings/reading-290.md) | VIII.57 | [Read](sources/meditations-george-long-gutenberg.txt#L5381-L5398) |
| [291](readings/reading-291.md) | VIII.58 | [Read](sources/meditations-george-long-gutenberg.txt#L5398-L5404) |
| [292](readings/reading-292.md) | VIII.59 | [Read](sources/meditations-george-long-gutenberg.txt#L5404-L5407) |
| [293](readings/reading-293.md) | VIII.60 | [Read](sources/meditations-george-long-gutenberg.txt#L5407-L5411) |
| [294](readings/reading-294.md) | VIII.61 | [Read](sources/meditations-george-long-gutenberg.txt#L5411-L5414) |

</details>

<details>

<summary>Book IX</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [295](readings/reading-295.md) | IX.1 | [Read](sources/meditations-george-long-gutenberg.txt#L5422-L5480) |
| [296](readings/reading-296.md) | IX.2 | [Read](sources/meditations-george-long-gutenberg.txt#L5480-L5491) |
| [297](readings/reading-297.md) | IX.3 | [Read](sources/meditations-george-long-gutenberg.txt#L5491-L5517) |
| [298](readings/reading-298.md) | IX.4 | [Read](sources/meditations-george-long-gutenberg.txt#L5517-L5520) |
| [299](readings/reading-299.md) | IX.5 | [Read](sources/meditations-george-long-gutenberg.txt#L5520-L5523) |
| [300](readings/reading-300.md) | IX.6 | [Read](sources/meditations-george-long-gutenberg.txt#L5523-L5527) |
| [301](readings/reading-301.md) | IX.7 | [Read](sources/meditations-george-long-gutenberg.txt#L5527-L5530) |
| [302](readings/reading-302.md) | IX.8 | [Read](sources/meditations-george-long-gutenberg.txt#L5530-L5536) |
| [303](readings/reading-303.md) | IX.9 | [Read](sources/meditations-george-long-gutenberg.txt#L5536-L5570) |
| [304](readings/reading-304.md) | IX.10 | [Read](sources/meditations-george-long-gutenberg.txt#L5570-L5576) |
| [305](readings/reading-305.md) | IX.11 | [Read](sources/meditations-george-long-gutenberg.txt#L5576-L5582) |
| [306](readings/reading-306.md) | IX.12 | [Read](sources/meditations-george-long-gutenberg.txt#L5582-L5586) |
| [307](readings/reading-307.md) | IX.13 | [Read](sources/meditations-george-long-gutenberg.txt#L5586-L5589) |
| [308](readings/reading-308.md) | IX.14 | [Read](sources/meditations-george-long-gutenberg.txt#L5589-L5593) |
| [309](readings/reading-309.md) | IX.15 | [Read](sources/meditations-george-long-gutenberg.txt#L5593-L5597) |
| [310](readings/reading-310.md) | IX.16 | [Read](sources/meditations-george-long-gutenberg.txt#L5597-L5604) |
| [311](readings/reading-311.md) | IX.17 | [Read](sources/meditations-george-long-gutenberg.txt#L5604-L5607) |
| [312](readings/reading-312.md) | IX.18 | [Read](sources/meditations-george-long-gutenberg.txt#L5607-L5611) |
| [313](readings/reading-313.md) | IX.19 | [Read](sources/meditations-george-long-gutenberg.txt#L5611-L5614) |
| [314](readings/reading-314.md) | IX.20 | [Read](sources/meditations-george-long-gutenberg.txt#L5614-L5617) |
| [315](readings/reading-315.md) | IX.21 | [Read](sources/meditations-george-long-gutenberg.txt#L5617-L5630) |
| [316](readings/reading-316.md) | IX.22 | [Read](sources/meditations-george-long-gutenberg.txt#L5630-L5637) |
| [317](readings/reading-317.md) | IX.23 | [Read](sources/meditations-george-long-gutenberg.txt#L5637-L5644) |
| [318](readings/reading-318.md) | IX.24 | [Read](sources/meditations-george-long-gutenberg.txt#L5644-L5654) |
| [319](readings/reading-319.md) | IX.25 | [Read](sources/meditations-george-long-gutenberg.txt#L5654-L5659) |
| [320](readings/reading-320.md) | IX.26 | [Read](sources/meditations-george-long-gutenberg.txt#L5659-L5663) |
| [321](readings/reading-321.md) | IX.27 | [Read](sources/meditations-george-long-gutenberg.txt#L5663-L5671) |
| [322](readings/reading-322.md) | IX.28 | [Read](sources/meditations-george-long-gutenberg.txt#L5671-L5691) |
| [323](readings/reading-323.md) | IX.29 | [Read](sources/meditations-george-long-gutenberg.txt#L5691-L5710) |
| [324](readings/reading-324.md) | IX.30 | [Read](sources/meditations-george-long-gutenberg.txt#L5710-L5720) |
| [325](readings/reading-325.md) | IX.31 | [Read](sources/meditations-george-long-gutenberg.txt#L5720-L5726) |
| [326](readings/reading-326.md) | IX.32 | [Read](sources/meditations-george-long-gutenberg.txt#L5726-L5734) |
| [327](readings/reading-327.md) | IX.33 | [Read](sources/meditations-george-long-gutenberg.txt#L5734-L5739) |
| [328](readings/reading-328.md) | IX.34 | [Read](sources/meditations-george-long-gutenberg.txt#L5739-L5745) |
| [329](readings/reading-329.md) | IX.35 | [Read](sources/meditations-george-long-gutenberg.txt#L5745-L5753) |
| [330](readings/reading-330.md) | IX.36 | [Read](sources/meditations-george-long-gutenberg.txt#L5753-L5760) |
| [331](readings/reading-331.md) | IX.37 | [Read](sources/meditations-george-long-gutenberg.txt#L5760-L5767) |
| [332](readings/reading-332.md) | IX.38 | [Read](sources/meditations-george-long-gutenberg.txt#L5767-L5770) |
| [333](readings/reading-333.md) | IX.39 | [Read](sources/meditations-george-long-gutenberg.txt#L5770-L5784) |
| [334](readings/reading-334.md) | IX.40 | [Read](sources/meditations-george-long-gutenberg.txt#L5784-L5803) |
| [335](readings/reading-335.md) | IX.41 | [Read](sources/meditations-george-long-gutenberg.txt#L5803-L5818) |
| [336](readings/reading-336.md) | IX.42 | [Read](sources/meditations-george-long-gutenberg.txt#L5818-L5860) |

</details>

<details>

<summary>Book X</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [337](readings/reading-337.md) | X.1 | [Read](sources/meditations-george-long-gutenberg.txt#L5868-L5889) |
| [338](readings/reading-338.md) | X.2 | [Read](sources/meditations-george-long-gutenberg.txt#L5889-L5898) |
| [339](readings/reading-339.md) | X.3 | [Read](sources/meditations-george-long-gutenberg.txt#L5898-L5909) |
| [340](readings/reading-340.md) | X.4 | [Read](sources/meditations-george-long-gutenberg.txt#L5909-L5912) |
| [341](readings/reading-341.md) | X.5 | [Read](sources/meditations-george-long-gutenberg.txt#L5912-L5917) |
| [342](readings/reading-342.md) | X.6 | [Read](sources/meditations-george-long-gutenberg.txt#L5917-L5939) |
| [343](readings/reading-343.md) | X.7 | [Read](sources/meditations-george-long-gutenberg.txt#L5939-L5977) |
| [344](readings/reading-344.md) | X.8–9 | [Read](sources/meditations-george-long-gutenberg.txt#L5977-L6056) |
| [345](readings/reading-345.md) | X.10–11 | [Read](sources/meditations-george-long-gutenberg.txt#L6056-L6085) |
| [346](readings/reading-346.md) | X.12 | [Read](sources/meditations-george-long-gutenberg.txt#L6085-L6095) |
| [347](readings/reading-347.md) | X.13 | [Read](sources/meditations-george-long-gutenberg.txt#L6095-L6107) |
| [348](readings/reading-348.md) | X.14 | [Read](sources/meditations-george-long-gutenberg.txt#L6107-L6112) |
| [349](readings/reading-349.md) | X.15 | [Read](sources/meditations-george-long-gutenberg.txt#L6112-L6119) |
| [350](readings/reading-350.md) | X.16 | [Read](sources/meditations-george-long-gutenberg.txt#L6119-L6122) |
| [351](readings/reading-351.md) | X.17 | [Read](sources/meditations-george-long-gutenberg.txt#L6122-L6126) |
| [352](readings/reading-352.md) | X.18 | [Read](sources/meditations-george-long-gutenberg.txt#L6126-L6130) |
| [353](readings/reading-353.md) | X.19 | [Read](sources/meditations-george-long-gutenberg.txt#L6130-L6137) |
| [354](readings/reading-354.md) | X.20 | [Read](sources/meditations-george-long-gutenberg.txt#L6137-L6141) |
| [355](readings/reading-355.md) | X.21–23 | [Read](sources/meditations-george-long-gutenberg.txt#L6141-L6175) |
| [356](readings/reading-356.md) | X.24 | [Read](sources/meditations-george-long-gutenberg.txt#L6175-L6181) |
| [357](readings/reading-357.md) | X.25 | [Read](sources/meditations-george-long-gutenberg.txt#L6181-L6192) |
| [358](readings/reading-358.md) | X.26 | [Read](sources/meditations-george-long-gutenberg.txt#L6192-L6201) |
| [359](readings/reading-359.md) | X.27 | [Read](sources/meditations-george-long-gutenberg.txt#L6201-L6209) |
| [360](readings/reading-360.md) | X.28 | [Read](sources/meditations-george-long-gutenberg.txt#L6209-L6217) |
| [361](readings/reading-361.md) | X.29 | [Read](sources/meditations-george-long-gutenberg.txt#L6217-L6221) |
| [362](readings/reading-362.md) | X.30 | [Read](sources/meditations-george-long-gutenberg.txt#L6221-L6229) |
| [363](readings/reading-363.md) | X.31–32 | [Read](sources/meditations-george-long-gutenberg.txt#L6229-L6270) |
| [364](readings/reading-364.md) | X.33 | [Read](sources/meditations-george-long-gutenberg.txt#L6270-L6301) |
| [365](readings/reading-365.md) | X.34 | [Read](sources/meditations-george-long-gutenberg.txt#L6301-L6321) |
| [366](readings/reading-366.md) | X.35 | [Read](sources/meditations-george-long-gutenberg.txt#L6321-L6331) |
| [367](readings/reading-367.md) | X.36 | [Read](sources/meditations-george-long-gutenberg.txt#L6331-L6357) |
| [368](readings/reading-368.md) | X.37 | [Read](sources/meditations-george-long-gutenberg.txt#L6357-L6361) |
| [369](readings/reading-369.md) | X.38 | [Read](sources/meditations-george-long-gutenberg.txt#L6361-L6370) |

</details>

<details>

<summary>Book XI</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [370](readings/reading-370.md) | XI.1 | [Read](sources/meditations-george-long-gutenberg.txt#L6378-L6403) |
| [371](readings/reading-371.md) | XI.2 | [Read](sources/meditations-george-long-gutenberg.txt#L6403-L6413) |
| [372](readings/reading-372.md) | XI.3 | [Read](sources/meditations-george-long-gutenberg.txt#L6413-L6424) |
| [373](readings/reading-373.md) | XI.4 | [Read](sources/meditations-george-long-gutenberg.txt#L6424-L6428) |
| [374](readings/reading-374.md) | XI.5 | [Read](sources/meditations-george-long-gutenberg.txt#L6428-L6432) |
| [375](readings/reading-375.md) | XI.6 | [Read](sources/meditations-george-long-gutenberg.txt#L6432-L6469) |
| [376](readings/reading-376.md) | XI.7 | [Read](sources/meditations-george-long-gutenberg.txt#L6469-L6473) |
| [377](readings/reading-377.md) | XI.8 | [Read](sources/meditations-george-long-gutenberg.txt#L6473-L6491) |
| [378](readings/reading-378.md) | XI.9 | [Read](sources/meditations-george-long-gutenberg.txt#L6491-L6503) |
| [379](readings/reading-379.md) | XI.10 | [Read](sources/meditations-george-long-gutenberg.txt#L6503-L6513) |
| [380](readings/reading-380.md) | XI.11 | [Read](sources/meditations-george-long-gutenberg.txt#L6513-L6518) |
| [381](readings/reading-381.md) | XI.12 | [Read](sources/meditations-george-long-gutenberg.txt#L6518-L6524) |
| [382](readings/reading-382.md) | XI.13 | [Read](sources/meditations-george-long-gutenberg.txt#L6524-L6538) |
| [383](readings/reading-383.md) | XI.14 | [Read](sources/meditations-george-long-gutenberg.txt#L6538-L6541) |
| [384](readings/reading-384.md) | XI.15 | [Read](sources/meditations-george-long-gutenberg.txt#L6541-L6561) |
| [385](readings/reading-385.md) | XI.16 | [Read](sources/meditations-george-long-gutenberg.txt#L6561-L6577) |
| [386](readings/reading-386.md) | XI.17 | [Read](sources/meditations-george-long-gutenberg.txt#L6577-L6581) |
| [387](readings/reading-387.md) | XI.18 | [Read](sources/meditations-george-long-gutenberg.txt#L6581-L6669) |
| [388](readings/reading-388.md) | XI.19 | [Read](sources/meditations-george-long-gutenberg.txt#L6669-L6681) |
| [389](readings/reading-389.md) | XI.20 | [Read](sources/meditations-george-long-gutenberg.txt#L6681-L6723) |
| [390](readings/reading-390.md) | XI.21 | [Read](sources/meditations-george-long-gutenberg.txt#L6723-L6733) |
| [391](readings/reading-391.md) | XI.22–26 | [Read](sources/meditations-george-long-gutenberg.txt#L6733-L6760) |
| [392](readings/reading-392.md) | XI.27 | [Read](sources/meditations-george-long-gutenberg.txt#L6760-L6765) |
| [393](readings/reading-393.md) | XI.28 | [Read](sources/meditations-george-long-gutenberg.txt#L6765-L6770) |
| [394](readings/reading-394.md) | XI.29 | [Read](sources/meditations-george-long-gutenberg.txt#L6770-L6774) |
| [395](readings/reading-395.md) | XI.30 | [Read](sources/meditations-george-long-gutenberg.txt#L6774-L6776) |
| [396](readings/reading-396.md) | XI.31 | [Read](sources/meditations-george-long-gutenberg.txt#L6776-L6779) |
| [397](readings/reading-397.md) | XI.32 | [Read](sources/meditations-george-long-gutenberg.txt#L6779-L6782) |
| [398](readings/reading-398.md) | XI.33 | [Read](sources/meditations-george-long-gutenberg.txt#L6782-L6786) |
| [399](readings/reading-399.md) | XI.34 | [Read](sources/meditations-george-long-gutenberg.txt#L6786-L6792) |
| [400](readings/reading-400.md) | XI.35 | [Read](sources/meditations-george-long-gutenberg.txt#L6792-L6796) |
| [401](readings/reading-401.md) | XI.36 | [Read](sources/meditations-george-long-gutenberg.txt#L6796-L6798) |
| [402](readings/reading-402.md) | XI.37–38 | [Read](sources/meditations-george-long-gutenberg.txt#L6798-L6809) |
| [403](readings/reading-403.md) | XI.39 | [Read](sources/meditations-george-long-gutenberg.txt#L6809-L6812) |

</details>

<details>

<summary>Book XII</summary>

| Reading | Sections | Original text |
| --- | --- | --- |
| [404](readings/reading-404.md) | XII.1 | [Read](sources/meditations-george-long-gutenberg.txt#L6820-L6841) |
| [405](readings/reading-405.md) | XII.2 | [Read](sources/meditations-george-long-gutenberg.txt#L6841-L6850) |
| [406](readings/reading-406.md) | XII.3–4 | [Read](sources/meditations-george-long-gutenberg.txt#L6850-L6890) |
| [407](readings/reading-407.md) | XII.5 | [Read](sources/meditations-george-long-gutenberg.txt#L6890-L6907) |
| [408](readings/reading-408.md) | XII.6 | [Read](sources/meditations-george-long-gutenberg.txt#L6907-L6912) |
| [409](readings/reading-409.md) | XII.7 | [Read](sources/meditations-george-long-gutenberg.txt#L6912-L6916) |
| [410](readings/reading-410.md) | XII.8 | [Read](sources/meditations-george-long-gutenberg.txt#L6916-L6921) |
| [411](readings/reading-411.md) | XII.9 | [Read](sources/meditations-george-long-gutenberg.txt#L6921-L6926) |
| [412](readings/reading-412.md) | XII.10 | [Read](sources/meditations-george-long-gutenberg.txt#L6926-L6929) |
| [413](readings/reading-413.md) | XII.11 | [Read](sources/meditations-george-long-gutenberg.txt#L6929-L6932) |
| [414](readings/reading-414.md) | XII.12 | [Read](sources/meditations-george-long-gutenberg.txt#L6932-L6938) |
| [415](readings/reading-415.md) | XII.13 | [Read](sources/meditations-george-long-gutenberg.txt#L6938-L6941) |
| [416](readings/reading-416.md) | XII.14 | [Read](sources/meditations-george-long-gutenberg.txt#L6941-L6952) |
| [417](readings/reading-417.md) | XII.15 | [Read](sources/meditations-george-long-gutenberg.txt#L6952-L6956) |
| [418](readings/reading-418.md) | XII.16–17 | [Read](sources/meditations-george-long-gutenberg.txt#L6956-L6976) |
| [419](readings/reading-419.md) | XII.18 | [Read](sources/meditations-george-long-gutenberg.txt#L6976-L6980) |
| [420](readings/reading-420.md) | XII.19 | [Read](sources/meditations-george-long-gutenberg.txt#L6980-L6985) |
| [421](readings/reading-421.md) | XII.20 | [Read](sources/meditations-george-long-gutenberg.txt#L6985-L6988) |
| [422](readings/reading-422.md) | XII.21 | [Read](sources/meditations-george-long-gutenberg.txt#L6988-L6994) |
| [423](readings/reading-423.md) | XII.22 | [Read](sources/meditations-george-long-gutenberg.txt#L6994-L6999) |
| [424](readings/reading-424.md) | XII.23 | [Read](sources/meditations-george-long-gutenberg.txt#L6999-L7019) |
| [425](readings/reading-425.md) | XII.24 | [Read](sources/meditations-george-long-gutenberg.txt#L7019-L7035) |
| [426](readings/reading-426.md) | XII.25 | [Read](sources/meditations-george-long-gutenberg.txt#L7035-L7038) |
| [427](readings/reading-427.md) | XII.26 | [Read](sources/meditations-george-long-gutenberg.txt#L7038-L7054) |
| [428](readings/reading-428.md) | XII.27 | [Read](sources/meditations-george-long-gutenberg.txt#L7054-L7071) |
| [429](readings/reading-429.md) | XII.28 | [Read](sources/meditations-george-long-gutenberg.txt#L7071-L7104) |
| [430](readings/reading-430.md) | XII.29 | [Read](sources/meditations-george-long-gutenberg.txt#L7104-L7110) |
| [431](readings/reading-431.md) | XII.30 | [Read](sources/meditations-george-long-gutenberg.txt#L7110-L7125) |
| [432](readings/reading-432.md) | XII.31 | [Read](sources/meditations-george-long-gutenberg.txt#L7125-L7133) |
| [433](readings/reading-433.md) | XII.32 | [Read](sources/meditations-george-long-gutenberg.txt#L7133-L7141) |
| [434](readings/reading-434.md) | XII.33 | [Read](sources/meditations-george-long-gutenberg.txt#L7141-L7145) |
| [435](readings/reading-435.md) | XII.34 | [Read](sources/meditations-george-long-gutenberg.txt#L7145-L7149) |
| [436](readings/reading-436.md) | XII.35 | [Read](sources/meditations-george-long-gutenberg.txt#L7149-L7155) |
| [437](readings/reading-437.md) | XII.36 | [Read](sources/meditations-george-long-gutenberg.txt#L7155-L7170) |

</details>
