# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"The Concert of Europe: Roar of Industry - Reignited" is a **Victoria 2 (Heart of Darkness) mod** built on top of the Pop Demand Mod (PDM), with a start date of **1821.9.1** (see `CoE_RoI_R/common/bookmarks.txt`). There is no build system, compiler, test runner, or linter. All content is Paradox Clausewitz script (`.txt`), Lua defines, `.csv` localisation, and `.bmp`/`.dds` assets that the game engine parses at launch.

Layout:
- `CoE_RoI_R.mod` — mod descriptor. Declares `path = "mod/CoE_RoI_R"` and `user_dir = "CoE_RoI_R"`, so the repo root is meant to be dropped into the game's `mod/` folder (see "Game install and deploy target").
- `CoE_RoI_R/` — the actual mod content, mirroring the vanilla game directory structure (`common`, `decisions`, `events`, `gfx`, `history`, `interface`, `inventions`, `localisation`, `map`, `news`, `poptypes`, `technologies`, `units`). Files here override vanilla files of the same name.
- `CoE_RoI_R/ValidatorSettings.txt` — config for the Audax Validator (third-party Paradox script checker); currently only sets `AddFlag = NoCheckKey`. There is no checked-in validator output log.

## Game install and deploy target

- **Game folder**: `D:\Steam\steamapps\common\Victoria 2` (Steam, Heart of Darkness; `v2game.exe`, `victoria2.exe` launcher).
- **User folder**: `E:\OneDrive\Documents\Paradox Interactive\Victoria II`. Vanilla logs and `settings.txt` live here (`logs\error.log`). Because the descriptor sets `user_dir = "CoE_RoI_R"`, running with the mod writes to `E:\OneDrive\Documents\Paradox Interactive\Victoria II\CoE_RoI_R\` instead (`CoE_RoI_R\logs\error.log`, saves, settings). That folder is created on first launch with the mod; it does not exist yet.
- **Deploy target**: `D:\Steam\steamapps\common\Victoria 2\mod\`. The game expects `mod\CoE_RoI_R.mod` next to `mod\CoE_RoI_R\` (the `path` in the descriptor is relative to the game root). The repo is **not** cloned there; `scripts/deploy.ps1` mirrors `CoE_RoI_R/` and `CoE_RoI_R.mod` into it with robocopy `/MIR`, then verifies the result is exactly 1:1 (list-only re-mirror finds nothing, and SHA256 of every file matches); it exits non-zero and aborts the push on any difference.
- **Push to deploy**: `.githooks/pre-push` runs `scripts/deploy.ps1` on every `git push`, so pushing also deploys the current working tree (not just the committed state). It is enabled per clone with `git config core.hooksPath .githooks`; re-run that after a fresh clone. To deploy without pushing:

```powershell
pwsh -File scripts/deploy.ps1
```

`/MIR` deletes files in the target that are gone from the repo, so the script only ever targets `mod\CoE_RoI_R`. Do not edit files in the deploy target directly; edit in the repo and redeploy.

## Testing / validation

There is no automated test. Verification means:
1. Deploy (push, or run `scripts/deploy.ps1`), launch `victoria2.exe`, tick "The Concert of Europe: Roar of Industry - Reignited" in the launcher's mod list, start a game at the 1821 bookmark, then read `E:\OneDrive\Documents\Paradox Interactive\Victoria II\CoE_RoI_R\logs\error.log`. Clear or note the log's size before launching so new errors stand out.
2. Optionally run the Audax Validator: `Audax.Validator\Validator.exe` (GUI; .NET 4.0). Set Game Path to the game folder above (not a Documents path), pick Vic2, set Mod Name to `CoE_RoI_R`, and Validate. It reads the deployed copy, so deploy first. It picks up `CoE_RoI_R/ValidatorSettings.txt`. `Audax.Validator/` is git-ignored; install it there yourself if missing.

Historical crashes in this repo have come from **wrong province IDs** in history/event files (e.g. commit `31764737` fixed an 1830 crash from province 3309 vs 1408). When editing anything that references a province, confirm the ID exists in `CoE_RoI_R/map/definition.csv`.

## Architecture: how the pieces connect

**Countries**: A tag must exist in three places to work:
- `common/countries.txt` — registers `TAG = "countries/Name.txt"` (keep alphabetically sorted, per the file header).
- `common/countries/Name.txt` — color, graphical culture, party definitions.
- `history/countries/TAG - Name.txt` — starting state (capital, cultures, government, reforms, tech, flags). ~520 files.
Localisation for the tag name goes in a `.csv` (`TAG;English;...`), typically `localisation/00_PDM_countries.csv` or `CountriesGVG.csv`.

**Events** (`events/*.txt`, ~170 files): `country_event`/`province_event` blocks keyed by numeric `id`. IDs are globally unique across all files and are reserved by range:
- `events/EventIDs.txt` — PDM's range registry (e.g. Political Events 3000–5000, Flavor Events 31000–48000, Clean Up 60000, On Action 70000).
- `events/GVG Event IDs.txt` — this team's own additions: `2000000+` setup events, `1000000–1000099` JAPFlavorGVG, `1000100–1000199` USAFlavorGVG, `1000200–1000299` BYZFlavorGVG.
- Not in either registry but in use: the Roar of Industry economy rework in `events/00_CoE_RoI_R.txt` (ids ~99984 and 6016xxx), `97xxx` pulse events (`Canals.txt`, fired from `on_actions.txt`), and `999xxxxx` education/RGO events (`+education_RGO*.txt`). Grep `events/` for an id before taking it.
Pick a new ID from an appropriate free range and record it in the registry file. Events reference localisation keys `EVTNAME<id>`, `EVTDESC<id>`, `EVTOPTA<id>`/`EVTOPTB<id>`, and for news `EVTNAME<id>_NEWS_TITLE`, `EVTDESC<id>_NEWS_LONG/MEDIUM/SHORT`.

**Decisions** (`decisions/*.txt`): `political_decisions = { name = { potential/allow/effect/ai_will_do } }`. Localisation keys are `<name>_title` and `<name>_desc`. Note `decisions/SetupGVG.txt` actually contains `country_event` blocks (ids 2000000–2000002) that run once at game start via `has_country_flag = setup_done` — this is the mod's start-of-game setup hook, not a decision file despite its location. `decisions/00_setup_decisions.txt` is a disabled (`always = no`) hook into the education/RGO event chain.

**Scripting conventions seen in this codebase**: file-naming suffixes indicate origin — `*Flavor.txt` / `*FlavorGVG.txt` (GVG = this team's additions), `DIM_*` (Dutch East Indies submod content), `000_persia_*` / `000_crownsteler_*`, `VIP_*`, `GAGA*`, and `00_CoE_RoI_R` / `0000_economic_rework` / `+education_RGO*` (Roar of Industry economy rework). New Concert-of-Europe-specific content generally uses the GVG suffix and the 1000000+/2000000+ ID ranges.

**Triggers/effects hooks**: `common/on_actions.txt` fires events on engine actions (e.g. `on_yearly_pulse`, `on_quarterly_pulse`). `common/defines.lua` holds engine constants (there is no `countries.lua` in this mod).

**Map** (`map/`): `definition.csv` maps province IDs to colors; `region.txt` groups provinces into states; `positions.txt`, `adjacencies.csv`, `terrain.txt`. Province history lives in `history/provinces/<region>/<id> - Name.txt`.

## File format requirements

- **Encoding**: game script `.txt` files are ASCII/ANSI with **CRLF** line endings. Localisation `.csv` files must be **Windows-1252 (ANSI)**, semicolon-delimited, ending each line with `x` in the terminator column, CRLF. Do **not** save them as UTF-8 — the game renders mojibake for accented characters. `text.csv` is the vanilla-override base and is huge (~3.7 MB); prefer adding new keys to a smaller mod-specific `.csv` rather than editing it. (`0000_economic_rework.csv` and `newCE.csv` are currently UTF-8 without BOM; don't propagate that to other files.)
- CSV column order: `KEY;English;French;German;Polish;Spanish;Italian;Swedish;Czech;Hungarian;Dutch;Portuguese;Russian;Finnish;x`. Only English is filled in for most mod strings.
- Comments in script files use `#`. Files must have balanced braces; a single mismatched brace can silently break every file parsed after it.

## Git workflow

Since the 2022 Roar of Industry rework, commits land directly on `master` (short informal messages, no PRs). In September 2026 all remote branches were consolidated into `master`: `Development` -> `Remake` -> `economic-rework` were a linear chain (fast-forwarded), and the still-applicable parts of the 2018 `autonomous_india` branch (country colours, HPM-derived defines/crime/tech-school changes) were ported by hand onto the `CoE_RoI_R/` tree. Those remote branches are now historical only. There is no license file in `CoE_RoI_R/`.
