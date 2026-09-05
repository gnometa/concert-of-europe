---
name: new-event
description: Scaffold a new country_event or province_event for the mod with a free, registered event id and matching localisation keys. Use when asked to add a flavour, setup, or scripted event.
argument-hint: <TAG or theme> "<event title>"
---

# new-event

Follow these steps in order. Do not skip the id registry or localisation.

## 1. Pick the id range

| Content | Range | File |
|---|---|---|
| Japan flavour | 1000000-1000099 | `events/JAPFlavorGVG.txt` |
| USA flavour | 1000100-1000199 | `events/USAFlavorGVG.txt` |
| Byzantium flavour | 1000200-1000299 | `events/BYZFlavorGVG.txt` |
| Game-start setup | 2000000+ | `decisions/SetupGVG.txt` (yes, decisions folder) |
| New country/theme | next free 100-block above 1000299 | new `events/<TAG>FlavorGVG.txt` |

For a new country, reserve a fresh block (e.g. 1000300-1000399) and add a line to `CoE_RoI_R/events/GVG Event IDs.txt`.

## 2. Get a free id

```
python scripts/modcheck.py next-id <lo> <hi>
```

This scans every top-level event definition in `events/` and `decisions/`.

## 3. Write the event

Copy `templates/country_event.txt` from this skill's directory (or an existing block from the same file) and fill it in. Rules:

- Script `.txt` files are ASCII with **CRLF** line endings. Match the indentation of the target file (tabs).
- `title` and `desc` must be quoted keys: `"EVTNAME<id>"`, `"EVTDESC<id>"`. Option names should be keys too (`"EVTOPTA<id>"`), not literal text.
- Any province number must exist in `CoE_RoI_R/map/definition.csv`; any tag must be registered in `common/countries.txt`. The PostToolUse hook checks both after every edit.
- Check trigger/effect names against `docs/wiki/list-of-conditions.md` and `docs/wiki/list-of-effects.md`. Copy patterns from a working file rather than inventing syntax.
- Use `fire_only_once = yes` for one-shot flavour, or a `set_country_flag` guard in the trigger (see existing GVG events).
- Events that are only fired from other events/decisions/on_actions need `is_triggered_only = yes`.
- If the event needs a new picture, confirm `gfx/pictures/events/<name>.tga` (or `.dds`) exists.

## 4. Localisation

Use the `/loc-add` skill (never Edit/Write on a .csv):

```
python scripts/modcheck.py loc-add GVG_events.csv EVTNAME<id> "<title>"
python scripts/modcheck.py loc-add GVG_events.csv EVTDESC<id> "<description>"
python scripts/modcheck.py loc-add GVG_events.csv EVTOPTA<id> "<option A>"
```

Add `EVTOPTB<id>` etc. for more options, and the `_NEWS_*` keys if `news = yes`.

## 5. Register and verify

- If a new range was reserved, append it to `CoE_RoI_R/events/GVG Event IDs.txt`.
- If the event must fire on a pulse, wire it in `common/on_actions.txt`.
- Run:
  ```
  python scripts/modcheck.py ids
  python scripts/modcheck.py braces CoE_RoI_R/events/<file>.txt
  python scripts/modcheck.py loc-find EVTNAME<id>
  ```
- Remind the user that in-game verification is still required (`/validate`).
