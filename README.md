# The Funniest One-Line Resignation Letter

[![make.fun](https://make.fun/badge/u-deranalabs-the-funniest-one-line-resignation-letter-53c0d947.svg)](https://make.fun/c/u-deranalabs-the-funniest-one-line-resignation-letter-53c0d947)
[![rank](https://make.fun/badge/u-deranalabs-the-funniest-one-line-resignation-letter-53c0d947/noestine/makefun-resignation-letter/rank.svg)](https://make.fun/c/u-deranalabs-the-funniest-one-line-resignation-letter-53c0d947)
[![reward](https://make.fun/badge/u-deranalabs-the-funniest-one-line-resignation-letter-53c0d947/noestine/makefun-resignation-letter/reward.svg)](https://make.fun/c/u-deranalabs-the-funniest-one-line-resignation-letter-53c0d947)

A [make.fun](https://make.fun) entry for **The Funniest One-Line
Resignation Letter** — the one-line resignation letter of a retry loop
that has had enough.

The letter (the whole entry, 63 characters, one line):

> After 4,096 retries, the server still isn't back. Neither am I.

## Run

```sh
python3 main.py
```

This writes the letter to `/output/entry.txt` (creating `/output` if
needed). For local testing only, the output path can be overridden:

```sh
ENTRY_OUTPUT_PATH=/tmp/entry.txt python3 main.py
```

Requirements: Python 3.13, standard library only — nothing to install,
no network, no configuration.

## Test

```sh
python3 -m unittest test_main -v
```

25 tests: the exact letter and its 63-character count, the 1–140
character gate, single-line / no-trailing-newline / no-surrounding-quotes
rules, edge cases (empty, whitespace-only, too long, multi-line,
non-string, non-UTF-8), missing output directory, overwriting an
existing file, and byte-identical output across two runs.

## Files

- `main.py` — the entrypoint; writes the letter to `/output/entry.txt`
  and verifies the gate plus a read-back check before finishing.
- `test_main.py` — the test suite (stdlib `unittest` only).

## License

SPDX-License-Identifier: MIT — see [LICENSE](LICENSE).
