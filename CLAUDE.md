# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"The Concert of Europe: Roar of Industry" is a **Victoria 2 (Heart of Darkness) mod** built on top of the Pop Demand Mod (PDM), with a start date of **1821.9.1** (see `CoE_RoI/common/bookmarks.txt`). There is no build system, compiler, test runner, or linter. All content is Paradox Clausewitz script (`.txt`), Lua defines, `.csv` localisation, and `.bmp`/`.dds` assets that the game engine parses at launch.

Layout:
- `CoE_RoI.mod` — mod descriptor. Declares `path = "mod/CoE_RoI"` and `user_dir = "CoE_RoI"`, so the repo root is meant to be dropped into the game's `mod/` folder.
- `CoE_RoI/` — the actual mod content, mirroring the vanilla game directory structure (`common`, `decisions`, `events`, `gfx`, `history`, `interface`, `inventions`, `localisation`, `map`, `news`, `poptypes`, `technologies`, `units`). Files here override vanilla files of the same name.
- `CoE_RoI/ValidatorSettings.txt` — config for the Audax Validator (third-party Paradox script checker); currently only sets `AddFlag = NoCheckKey`. There is no checked-in validator output log.

## Testing / validation

There is no automated test. Verification means:
1. Launch Victoria 2 with the mod selected and check `error.log` in the user dir (`user_dir = "CoE_RoI"`).
2. Optionally run the Audax Validator against `CoE_RoI/` (it picks up `CoE_RoI/ValidatorSettings.txt`) and look for new errors. A local copy of the validator lives in `Audax.Validator/` at the repo root; it is git-ignored, so install it there yourself if missing.

Historical crashes in this repo have come from **wrong province IDs** in history/event files (e.g. commit `31764737` fixed an 1830 crash from province 3309 vs 1408). When editing anything that references a province, confirm the ID exists in `CoE_RoI/map/definition.csv`.

## Architecture: how the pieces connect

**Countries**: A tag must exist in three places to work:
- `common/countries.txt` — registers `TAG = "countries/Name.txt"` (keep alphabetically sorted, per the file header).
- `common/countries/Name.txt` — color, graphical culture, party definitions.
- `history/countries/TAG - Name.txt` — starting state (capital, cultures, government, reforms, tech, flags). ~520 files.
Localisation for the tag name goes in a `.csv` (`TAG;English;...`), typically `localisation/00_PDM_countries.csv` or `CountriesGVG.csv`.

**Events** (`events/*.txt`, ~170 files): `country_event`/`province_event` blocks keyed by numeric `id`. IDs are globally unique across all files and are reserved by range:
- `events/EventIDs.txt` — PDM's range registry (e.g. Political Events 3000–5000, Flavor Events 31000–48000, Clean Up 60000, On Action 70000).
- `events/GVG Event IDs.txt` — this team's own additions: `2000000+` setup events, `1000000–1000099` JAPFlavorGVG, `1000100–1000199` USAFlavorGVG, `1000200–1000299` BYZFlavorGVG.
- Not in either registry but in use: the Roar of Industry economy rework in `events/00_CoE_RoI.txt` (ids ~99984 and 6016xxx), `97xxx` pulse events (`Canals.txt`, fired from `on_actions.txt`), and `999xxxxx` education/RGO events (`+education_RGO*.txt`). Grep `events/` for an id before taking it.
Pick a new ID from an appropriate free range and record it in the registry file. Events reference localisation keys `EVTNAME<id>`, `EVTDESC<id>`, `EVTOPTA<id>`/`EVTOPTB<id>`, and for news `EVTNAME<id>_NEWS_TITLE`, `EVTDESC<id>_NEWS_LONG/MEDIUM/SHORT`.

**Decisions** (`decisions/*.txt`): `political_decisions = { name = { potential/allow/effect/ai_will_do } }`. Localisation keys are `<name>_title` and `<name>_desc`. Note `decisions/SetupGVG.txt` actually contains `country_event` blocks (ids 2000000–2000002) that run once at game start via `has_country_flag = setup_done` — this is the mod's start-of-game setup hook, not a decision file despite its location. `decisions/00_setup_decisions.txt` is a disabled (`always = no`) hook into the education/RGO event chain.

**Scripting conventions seen in this codebase**: file-naming suffixes indicate origin — `*Flavor.txt` / `*FlavorGVG.txt` (GVG = this team's additions), `DIM_*` (Dutch East Indies submod content), `000_persia_*` / `000_crownsteler_*`, `VIP_*`, `GAGA*`, and `00_CoE_RoI` / `0000_economic_rework` / `+education_RGO*` (Roar of Industry economy rework). New Concert-of-Europe-specific content generally uses the GVG suffix and the 1000000+/2000000+ ID ranges.

**Triggers/effects hooks**: `common/on_actions.txt` fires events on engine actions (e.g. `on_yearly_pulse`, `on_quarterly_pulse`). `common/defines.lua` holds engine constants (there is no `countries.lua` in this mod).

**Map** (`map/`): `definition.csv` maps province IDs to colors; `region.txt` groups provinces into states; `positions.txt`, `adjacencies.csv`, `terrain.txt`. Province history lives in `history/provinces/<region>/<id> - Name.txt`.

## File format requirements

- **Encoding**: game script `.txt` files are ASCII/ANSI with **CRLF** line endings. Localisation `.csv` files must be **Windows-1252 (ANSI)**, semicolon-delimited, ending each line with `x` in the terminator column, CRLF. Do **not** save them as UTF-8 — the game renders mojibake for accented characters. `text.csv` is the vanilla-override base and is huge (~3.7 MB); prefer adding new keys to a smaller mod-specific `.csv` rather than editing it. (`0000_economic_rework.csv` and `newCE.csv` are currently UTF-8 without BOM; don't propagate that to other files.)
- CSV column order: `KEY;English;French;German;Polish;Spanish;Italian;Swedish;Czech;Hungarian;Dutch;Portuguese;Russian;Finnish;x`. Only English is filled in for most mod strings.
- Comments in script files use `#`. Files must have balanced braces; a single mismatched brace can silently break every file parsed after it.

## Git workflow

Since the 2022 Roar of Industry rework, commits land directly on `master` (short informal messages, no PRs). In September 2026 all remote branches were consolidated into `master`: `Development` -> `Remake` -> `economic-rework` were a linear chain (fast-forwarded), and the still-applicable parts of the 2018 `autonomous_india` branch (country colours, HPM-derived defines/crime/tech-school changes) were ported by hand onto the `CoE_RoI/` tree. Those remote branches are now historical only. There is no license file in `CoE_RoI/`.
