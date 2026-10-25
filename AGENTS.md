# Repository guidance

Read [philosophy/README.md](philosophy/README.md) for operation, validation,
and simulation instructions.

## Local simulation

Run from the repository root:

```sh
# Simulate three future readings and show the next passage.
python3 philosophy/scripts/simulate.py --days 3 --preview

# Simulate all remaining readings, including same-date reruns and completion.
python3 philosophy/scripts/simulate.py --all
```

Simulations use a temporary copy. They do not advance the real README or
progress, invoke Git, or access the network. Prefer these commands when asked
to preview or test publication. Running `daily.py` without `--check` updates
the real README and progress.

## Integrity and Python style

Keep the frozen source files byte-for-byte unchanged. Never correct, normalize,
paraphrase, or regenerate their text. See
[source notes](philosophy/sources/README.md) for known discrepancies.

Use descriptive names, type hints, PEP 8 formatting, and Google-style docstrings.
Ruff settings are in `pyproject.toml`.

Read-only validation commands:

```sh
python3 -m unittest discover -s philosophy/tests
python3 philosophy/scripts/audit_source.py
python3 philosophy/scripts/daily.py --check
python3 philosophy/scripts/archive.py --check
```

After changing rendered output, rendering code, the catalog, or progress,
run all four commands against the final working tree before handing off or
committing. The test suite validates the actual README and archive as well
as isolated fixtures. Repeat validation if a merge, pull, or automated daily
update changes those files after the checks pass.

When formatting changes, update the displayed reading using its saved
passage and publication date; do not advance progress to fix stale output.
