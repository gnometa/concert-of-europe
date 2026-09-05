---
name: loc-add
description: Add or look up a localisation key in the mod's Windows-1252 .csv files without corrupting the encoding. Use whenever a new event, decision, country, modifier, or any other script entry needs player-visible text, or when checking whether a key already exists.
argument-hint: <csv-file> <KEY> "<English text>"
---

# loc-add

Localisation `.csv` files under `CoE_RoI_R/localisation/` must stay **Windows-1252 with CRLF**. The Edit and Write tools save UTF-8, so a PreToolUse hook blocks them on those files. Always go through `scripts/modcheck.py` instead.

## Adding a key

```
python scripts/modcheck.py loc-add <csv-file> <KEY> "<English text>"
```

- `<csv-file>` is a file name inside `CoE_RoI_R/localisation/` (e.g. `GVG_events.csv`) or a path.
- The script appends `KEY;English;;;;;;;;;;;;;x` with CRLF, encoded cp1252.
- It refuses if the key already exists in **any** csv, if the text contains `;`, or if a character cannot be represented in Windows-1252.
- It refuses to touch `text.csv` (3.7 MB vanilla override) unless `--force` is passed. Use a mod-specific file instead.

Which file to use:
| Content | File |
|---|---|
| GVG events (`EVTNAME`, `EVTDESC`, `EVTOPTA`...) | `GVG_events.csv` |
| Country names / adjectives | `CountriesGVG.csv` |
| Decisions (`<name>_title`, `<name>_desc`) | `VIP_decisions.csv` or `GVG_events.csv` |
| Roar of Industry economy strings | `0000_economic_rework.csv` (note: currently UTF-8; do not add non-ASCII text there) |

## Looking up a key

```
python scripts/modcheck.py loc-find <KEY>
```

## Changing existing text

`loc-add` only appends. To edit an existing line, run a short Python snippet that keeps the encoding:

```python
from pathlib import Path
p = Path("CoE_RoI_R/localisation/GVG_events.csv")
s = p.read_bytes().decode("cp1252")
s = s.replace("OLDKEY;Old text;", "OLDKEY;New text;", 1)
p.write_bytes(s.encode("cp1252"))
```

Then verify with `python scripts/modcheck.py loc-check <csv-file>`.

## Key naming

- Events: `EVTNAME<id>`, `EVTDESC<id>`, `EVTOPTA<id>`, `EVTOPTB<id>`, ... ; news: `EVTNAME<id>_NEWS_TITLE`, `EVTDESC<id>_NEWS_LONG/MEDIUM/SHORT`.
- Decisions: `<decision_name>_title`, `<decision_name>_desc`.
- Countries: `TAG`, `TAG_ADJ`; government-specific names `TAG_<government>`, `TAG_<government>_ADJ`.
- Modifiers: the modifier name as written in `common/event_modifiers.txt`.
