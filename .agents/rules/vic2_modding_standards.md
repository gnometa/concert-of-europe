# Victoria 2 Modding & Repository Invariants

When working in this repository ("The Concert of Europe: Roar of Industry - Reignited"), adhere to the following engine, file format, and workflow invariants.

## 1. File Formats & Encoding (Strict)
- **Script Files (`.txt`)**: Must be **ASCII/ANSI with CRLF** line endings. Never save with bare LF line endings. Never use tools or scripts that write Unix LF without conversion.
- **Localisation Files (`.csv`)**: Must be **Windows-1252 (cp1252 / ANSI)**, semicolon-delimited, ending each line with `x` in the terminator column and **CRLF** line endings.
  - **NEVER save `.csv` files as UTF-8** (this creates in-game mojibake for accented characters).
  - To add localisation strings, prefer using `python scripts/modcheck.py loc-add <csv> KEY "text"` or an explicit cp1252 Python script.
- **Brace Integrity**: Paradox Clausewitz script files must have balanced braces `{}`. A single missing or extra brace can silently corrupt every file parsed after it.

## 2. Event & Decision IDs
- Event IDs are globally unique across the entire mod.
- Always grep `events/` before taking an ID.
- Check and update [events/GVG Event IDs.txt](file:///d:/Project/concert-of-europe/events/GVG%20Event%20IDs.txt) to allocate ranges (e.g. `1000000+` for historical/flavor chains, `2000000+` for setup/system events).
- Required localisation keys for events: `EVTNAME<id>`, `EVTDESC<id>`, `EVTOPTA<id>` (and `EVTOPTB<id>`, etc.).

## 3. Clausewitz Engine Scripting Pitfalls
- **`fire_only_once = yes`**: Engine-wide once-per-game, NOT once per country. Always guard repeatable/country-specific events with country flags set in every option.
- **`month` is 0-indexed**: `month = 0` is January, `month = 8` is September.
- **`continent` is province-scoped**: At country scope, wrap with `capital_scope = { continent = <name> }`.
- **`NOT = { a b }`**: Evaluates as NOR (true only if both `a` and `b` are false), NOT NAND.
- **`province_event`**: Must use block syntax `province_event = { id = X days = N }`. Bare `province_event = X` fails.
- **`treasury` / `money`**: Fixed-point int32 hundredths. High values wrap and may pay the country instead of charging.
- **Cultures & Religions**:
  - Pops carry real religions (`catholic`, `sunni`, etc.). Sub-culture is in the `CULTURE` field (`north_german`, `south_german`, `north_italian`, etc.).
  - `german` and `italian` have 0 pops; check sub-cultures or use `is_culture_group = germanic|italian`.
- **Province History Overrides**: Overridden by EXACT FILE PATH, not province ID. Do not move or rename files in `history/provinces/` relative to vanilla paths.

## 4. Verification & Tooling
- Run `python scripts/modcheck.py` to check for syntax, brace balance, CRLF, encoding, and duplicate IDs.
- Run `python scripts/refcheck.py` to check for missing localisation, dangling flags, or undefined modifiers.
- Run `pwsh -File scripts/deploy.ps1` to mirror mod files into `D:\Steam\steamapps\common\Victoria 2\mod\`.
- Run `pwsh -File scripts/gametest.ps1` to launch headless test runs to verify the game reaches the main menu without crashing.
