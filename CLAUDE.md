# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"The Concert of Europe: Roar of Industry - Reignited" is a **Victoria 2 (Heart of Darkness) mod** built on top of the Pop Demand Mod (PDM), with a start date of **1821.9.1** (see `CoE_RoI_R/common/bookmarks.txt`). There is no build system, compiler or test runner; the repo's own Python checks under `scripts/` stand in for one (see "Claude Code tooling"). All content is Paradox Clausewitz script (`.txt`), Lua defines, `.csv` localisation, and `.bmp`/`.dds` assets that the game engine parses at launch.

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

Beyond the static checks, nothing can be verified without the game. Verification means:
1. Deploy (push, or run `scripts/deploy.ps1`), launch `victoria2.exe`, tick "The Concert of Europe: Roar of Industry - Reignited" in the launcher's mod list, start a game at the 1821 bookmark, then read `E:\OneDrive\Documents\Paradox Interactive\Victoria II\CoE_RoI_R\logs\error.log`. Clear or note the log's size before launching so new errors stand out.
2. `pwsh -File scripts/gametest.ps1` launches the deployed mod headlessly and reports PASS when the main menu is reached or FAIL with the exit code and the last log lines (about 90 s). Use it after every deploy and as the probe for `git bisect` when a crash has no error.log entry.
3. Optionally run the Audax Validator: `Audax.Validator\Validator.exe` (GUI; .NET 4.0). Set Game Path to the game folder above (not a Documents path), pick Vic2, set Mod Name to `CoE_RoI_R`, and Validate. It reads the deployed copy, so deploy first. It picks up `CoE_RoI_R/ValidatorSettings.txt`. `Audax.Validator/` is git-ignored; install it there yourself if missing.

Historical crashes in this repo have come from a **moved province history file** (see the path pitfall below; a crash at "Executing History" with an empty error.log is this or a capital the tag does not own) and from **wrong province IDs** in history/event files (e.g. commit `31764737` fixed an 1830 crash from province 3309 vs 1408). When editing anything that references a province, confirm the ID exists in `CoE_RoI_R/map/definition.csv`.

## Architecture: how the pieces connect

**Countries**: A tag must exist in three places to work:
- `common/countries.txt` — registers `TAG = "countries/Name.txt"` (keep alphabetically sorted, per the file header).
- `common/countries/Name.txt` — color, graphical culture, party definitions.
- `history/countries/TAG - Name.txt` — starting state (capital, cultures, government, reforms, tech, flags). One per tag, plus a few named `TAG.txt`.

Localisation for the tag name goes in a `.csv` (`TAG;English;...`), typically `localisation/00_PDM_countries.csv` or `CountriesGVG.csv`.

Two tag choices trip people up at the 1821 start:
- Japan is the Shogunate tag **TKG**; JAP (the imperial court) and the han are its substates (`history/diplomacy/Japan.txt`), so bakufu-level content is scripted on TKG.
- China is the Qing tag **QNG**; **CHI** owns no provinces at start and is the later republican tag reached through the Taiping/revolution chains, so new Qing content targets QNG.

**Events** (`events/*.txt`): `country_event`/`province_event` blocks keyed by numeric `id`. IDs are globally unique across every file, so always grep `events/` for an id before taking it. Two registries reserve ranges:
- `events/EventIDs.txt` — PDM's registry (Political, Flavor, Clean Up, On Action, ...).
- `events/GVG Event IDs.txt` — this team's ranges: `2000000+` for setup, `2000100+` for the economy pulse host election, and one hundred-wide block per flavour or history chain from `1000000` up (`*GVG.txt` files). It also lists ranges reserved by deleted files. It is the authoritative list — read and update it rather than duplicating it here.

Some in-use ids are in neither registry: the Roar of Industry economy rework (`events/00_CoE_RoI.txt`), the `Canals.txt` pulse events fired from `on_actions.txt`, and the education/RGO events (`+education_RGO*.txt`).

Pick a new id from a free range and record it in the registry. Events reference localisation keys `EVTNAME<id>`, `EVTDESC<id>`, `EVTOPTA<id>`/`EVTOPTB<id>`, and for news `EVTNAME<id>_NEWS_TITLE`, `EVTDESC<id>_NEWS_LONG/MEDIUM/SHORT`. `docs/design/1821-1836-coverage.md` is the backlog of proposed content for the opening period, tag by tag.

**Decisions** (`decisions/*.txt`): `political_decisions = { name = { potential/allow/effect/ai_will_do } }`. Localisation keys are `<name>_title` and `<name>_desc`. The mod's start-of-game setup hook is not a decision: it is event 2000000 in `events/SetupGVG.txt`, which fires once per game for the player only (`ai = no`, guarded by the `setup_done` country flag). `decisions/00_setup_decisions.txt` is a disabled (`always = no`) hook into the education/RGO event chain.

**Scripting conventions seen in this codebase**: file-naming suffixes indicate origin — `*Flavor.txt` / `*FlavorGVG.txt` (GVG = this team's additions), `DIM_*` (Dutch East Indies submod content), `000_persia_*` / `000_crownsteler_*`, `VIP_*`, `GAGA*`, and `00_CoE_RoI` / `0000_economic_rework` / `+education_RGO*` (Roar of Industry economy rework). New Concert-of-Europe-specific content generally uses the GVG suffix and the 1000000+/2000000+ ID ranges.

**Triggers/effects hooks**: `common/on_actions.txt` fires events on engine actions (e.g. `on_yearly_pulse`, `on_quarterly_pulse`). `common/defines.lua` holds engine constants (there is no `countries.lua` in this mod).

**Scripting pitfalls** (each of these has cost a rewrite here; verified against the engine):

- `fire_only_once = yes` is once per game engine-wide, not once per country — guard with a country flag set in every option (`scripts/audit_fire_once.py`, verdicts in `docs/audit/fire-only-once.md`).
- `month` is 0-indexed (`month = 8` is September).
- `continent` is a province-scope trigger; at country scope wrap it as `capital_scope = { continent = north_america }`.
- `treasury` / `money` are fixed-point int32 hundredths — bigger literals wrap and can pay the country instead of charging it.
- `NOT = { a b }` is NOR (true only if every clause is false), not NAND.
- `on_actions` numbers are weights, not chances: exactly one event fires per country per pulse, so every entry added dilutes the rest.
- `province_event` needs the block form `province_event = { id = X days = N }`; the bare `province_event = X` does not work.
- `random_neighbor_country` does not exist (use `any_neighbor_country`).
- `efficiency` goods in `common/production_types.txt` are daily maintenance per level summed with `input_goods`, not a multiplier.
- Pops carry a real religion (`catholic`, `sunni`, ...) and their sub-culture is in the CULTURE field (`north_german`, `south_german`, `north_italian`, `south_italian`, `dixie`, `occitan`, `picard`, `anglo_canadian`, `australian`, `anglo_african`) — restored 2026-09-06, see `docs/design/religion-restoration.md`. Consequences: test sub-cultures with `has_pop_culture` / `culture` / `is_culture_group`, never with `religion`; **`german` and `italian` have zero pops**, so a `culture = german|italian` site is always a bug (use the sub-culture or `is_culture_group = germanic|italian`); `common/religion.txt` holds only the 24 real religions. `python scripts/audit_religion.py check` enforces all of this and must stay at 0 problems.
- Province history is overridden per FILE PATH, not per id: a mod file for province N must sit at exactly vanilla's relative path (`history/provinces/<folder>/<N - Vanilla Name>.txt`). Move or rename it and the vanilla file loads too; the alphabetically later one wins, and if that leaves a country without its capital the game dies at "Executing History" with an empty error.log (the 2637 Lanfang move, 2026-09-06). Rename provinces in localisation (`PROV<N>`) only. `python scripts/modcheck.py province-paths` enforces it.
- `sed -i` writes LF — never use it on `CoE_RoI_R/**`; script `.txt` must stay CRLF. Use Python with `newline=''`.

**Map** (`map/`): `default.map` references the definition file by mod-relative path (`../mod/CoE_RoI_R/map/definition.csv`), so it must be updated if the mod folder is ever renamed; search with no extension filter, since `.map` is easy to miss. `definition.csv` maps province IDs to colors; `region.txt` groups provinces into states; `positions.txt`, `adjacencies.csv`, `terrain.txt`. Province history lives in `history/provinces/<region>/<id> - Name.txt`.

## File format requirements

- **Encoding**: game script `.txt` files are ASCII/ANSI with **CRLF** line endings. Localisation `.csv` files must be **Windows-1252 (ANSI)**, semicolon-delimited, ending each line with `x` in the terminator column, CRLF. Do **not** save them as UTF-8 — the game renders mojibake for accented characters. `text.csv` is the vanilla-override base and is huge (~3.7 MB); prefer adding new keys to a smaller mod-specific `.csv` rather than editing it. (`0000_economic_rework.csv` and `newCE.csv` are currently UTF-8 without BOM; don't propagate that to other files.)
- CSV column order: `KEY;English;French;German;Polish;Spanish;Italian;Swedish;Czech;Hungarian;Dutch;Portuguese;Russian;Finnish;x`. Only English is filled in for most mod strings.
- Comments in script files use `#`. Files must have balanced braces; a single mismatched brace can silently break every file parsed after it.

## Graphics (gfx/) and sourcing free pictures

Formats the mod actually ships, by folder (the engine also accepts the other extension, and falls back to the vanilla file of the same name when the mod lacks one):

| Folder | Size | Format | Referenced from |
|---|---|---|---|
| `gfx/pictures/events/` | 521x203 | TGA 32-bit, bottom-up | `picture = "name"` in `events/*.txt` |
| `gfx/pictures/decisions/` | 95x95 | DDS uncompressed (some DXT1) | `picture = "name"` in `decisions/*.txt` |
| `gfx/pictures/news/` | 521x203 images, 714x104 mastheads | DDS uncompressed | `picture = "news/x.dds"` / `"events/x.tga"` in `news/news_layout.txt` (path relative to `gfx/pictures/`) |
| `gfx/flags/` | 93x64 | TGA 24-bit | `TAG.tga` plus `TAG_communist/_fascist/_monarchy/_republic.tga` |
| `gfx/loadingscreens/` | 1024x1024 | DDS | engine |

`scripts/gfxtool.py` (needs `python -m pip install Pillow`) is the only supported way to add pictures; there is no ImageMagick on this machine.
- `python scripts/gfxtool.py missing` lists pictures referenced by events/decisions/news that exist in neither the mod nor the game folder. It is part of `/validate` stage 1 and should print nothing.
- `python scripts/gfxtool.py search "<query>"` searches Wikimedia Commons and keeps only files whose licence is public domain / CC0 / CC-BY / CC-BY-SA **and** whose date is 1820–1914 (the Victorian-era filter; `--any-era` to disable, e.g. for maps). Engravings from *The Illustrated London News* / *The Graphic*, Barth/Angas-style travel lithographs and pre-1900 paintings pass; modern photos of monuments do not.
- `python scripts/gfxtool.py fetch "File:Name.jpg" --kind event|decision|news|masthead|loading --name <file>` downloads, crops to size (`--crop TOP|CENTER|BOTTOM`), applies the house "Victorian" look (sepia, vignette, light grain; `--no-filter` to skip) and writes the correctly formatted file. It refuses non-free or out-of-era files unless `--force`, and appends a row to `CoE_RoI_R/gfx/CREDITS.md`. Keep that file up to date; it is the mod's licence record for redistributed art.
- `gfxtool.py convert <local image> ...` does the same from a file on disk; `gfxtool.py preview <x.tga|x.dds> out.png` decodes a game image so it can be looked at.

Do not hand-copy pictures from other mods or image-search results: the licence must be checked and recorded, which is what `fetch` does.

## Git workflow

Since the 2022 Roar of Industry rework, commits land directly on `master` (short informal messages, no PRs). In September 2026 all remote branches were consolidated into `master`: `Development` -> `Remake` -> `economic-rework` were a linear chain (fast-forwarded), and the still-applicable parts of the 2018 `autonomous_india` branch (country colours, HPM-derived defines/crime/tech-school changes) were ported by hand onto the `CoE_RoI_R/` tree. Those remote branches are now historical only. There is no license file in `CoE_RoI_R/`. `docs/CHANGELOG.md` records notable changes per dated pass — add an entry there when a batch of work lands.

## Modding reference (local wiki mirror)

`docs/wiki/` is a Markdown mirror of the Paradox wiki's Victoria 2 modding section (https://vic2.paradoxwikis.com/Modding and everything it links to, fetched September 2026 by `scripts/fetch_wiki_docs.py`). Start at `docs/wiki/README.md` for the index. Read these before guessing at script syntax; they document the vanilla engine, which this mod does not change. The most useful pages:

- Script vocabulary: `list-of-conditions.md` (triggers), `list-of-effects.md`, `list-of-scopes.md`, `modifier-effects.md`, `defines-lua.md`.
- Content guides: `event-modding.md`, `how-to-make-a-decision.md`, `creating-a-country.md`, `localisation.md`, `province-history-modding.md`, `population-modding.md`, `map-modding.md`, `default-map.md`.
- `folder-file-overview.md` explains what each game directory holds; `console-commands.md` lists debug commands useful when testing in-game.

Caveats when applying the wiki here:
- The wiki's `countries.md` and `provinces.md` describe **vanilla**. This mod has its own map and its own tag list, so `CoE_RoI_R/map/definition.csv`, `common/countries.txt`, and `history/provinces/` are the only authoritative sources for IDs and tags.
- The wiki's rule of thumb for crashes: a crash **during startup** is almost always a syntax error (typically an unbalanced `}`); a crash on 'Start Game' or a specific in-game date points at a context error (a typo in a production type, an event/decision/history entry firing on that date; compare the province-ID crash noted under "Testing / validation").
- The wiki documents syntax but not behaviour in edge cases; when in doubt, copy the pattern from a working file in `CoE_RoI_R/` or from the vanilla game folder rather than inventing it.
- The mirror is a snapshot. Pages that were red links on the wiki (economy, reform, technology, ideology, pop-type, rebel, unit, interface modding, most `*.txt` file pages) do not exist locally either; for those, read the vanilla file in the game folder.

## Claude Code tooling (scripts/modcheck.py, .claude/)

`scripts/modcheck.py` is the mod's stand-in for a linter and test runner (run with no arguments for the subcommand list). `.claude/settings.json` wires two hooks around it:
- **PreToolUse** blocks Edit/Write on `localisation/*.csv` because those tools save UTF-8. Add keys with `python scripts/modcheck.py loc-add <csv> KEY "text"` or a cp1252 Python snippet (see the `/loc-add` skill).
- **PostToolUse** runs brace/CRLF/encoding checks on every edited `.txt` under `CoE_RoI_R/`, plus province-id and tag checks for events, decisions, and history files. Fix what it reports before moving on.

`scripts/audit_religion.py` inventories every religion trigger and effect against what the pops actually carry (`docs/audit/religion-dead-content.md`).

Useful `modcheck` one-offs: `next-id <lo> <hi>`, `ids` (duplicate event ids), `loc-find KEY`, `loc-check <csv>`, `encoding` (whole-tree audit).

Skills: `/loc-add` (localisation keys), `/new-event` (free id + scaffold + loc + registry), `/validate` (static checks, deploy, Audax, error.log diff; user-invoked only). Subagents: `script-reviewer` (read-only review of changed script) and `encoding-auditor`.

`scripts/refcheck.py` is the cross-reference checker: it parses the whole tree and reports event ids fired but never defined (and orphaned `is_triggered_only` events), missing localisation for event titles/options and decisions, undefined modifiers, flags set but never checked (or vice versa), unknown cultures/religions/goods/reform options, and `on_actions` entries. Run it for all checks or name one (`events`, `loc`, `flags`, `names`, `modifiers`, `onactions`, `options`); it prints one problem per line.

Alongside it sits a family of read-only audit scripts, one per subsystem, each printing `[high]`/`[medium]`/`[low]` findings and most of them regenerating a report under `docs/audit/`. Those reports are generated output — re-run the script rather than hand-editing, except for the hand-maintained Fixed/Deferred sections some of them preserve.

| Script | Covers |
|---|---|
| `audit_countries.py` | `history/countries` vs `common/countries.txt`: unregistered tags, capitals a tag does not own, undefined or out-of-window ruling parties, illegal ideologies |
| `audit_parties.py` | party blocks in `common/countries/`: ideologies, issues, dates, per-year coverage |
| `audit_provinces.py` | duplicate province history files, blocks dated before the start date, pops in unowned provinces |
| `audit_diplomacy.py` | `history/diplomacy` and `history/wars` consistency, technology/invention modifier keys |
| `audit_decisions.py` | duplicate decisions, missing `ai_will_do`, unguarded repeatables |
| `audit_common.py` | the `common/` vocabulary against vanilla, invalid modifier keys, the `defines.lua` diff |
| `audit_loc.py` | conflicting keys, mojibake, placeholders, malformed csv rows |
| `audit_events.py` | unknown trigger/effect keywords, re-firing events with permanent effects, `year = 1836` gates that lock out the 1821 start |
| `audit_events2.py` | second-opinion structural pass over events and decisions (FROM misuse, scope of effects, random_list weights, ...); emits JSON |
| `audit_fire_once.py` | self-firing events relying on engine-wide `fire_only_once` |
| `audit_owner_scope.py` | `any_owned` / `random_owned` blocks that can never match, because the enclosing country scope owns none of the provinces the `limit` names (the silent no-op the Anglo-Afghan chain shipped) |
| `audit_perf.py` | scores self-firing events by trigger cost and ranks the hotspots |
| `audit_pacing.py` | player-facing event load 1821-1836 per major playable tag: fires per year, `major = yes` popups, same-day cascades, runaway repeaters |
| `balance_factories.py` | factory and artisan margins including maintenance goods (`--vanilla` for the reference band, `--target R` for the budget solver) |

Design notes for content built on top of these findings live in `docs/design/`. Accepted baselines for all of the above are in `.claude/skills/validate/SKILL.md`; do not "fix" a known finding as a side effect of unrelated work.

## CWTools (VS Code)

Open `concert-of-europe.code-workspace`, not the bare folder: it lists `CoE_RoI_R` first (CWTools treats the first workspace folder as the mod root) and points `cwtools.rules_folder` at `.cwtools/`, a git-ignored copy of https://github.com/cwtools/cwtools-vic2-config (MIT). Re-fetch it after a fresh clone:

```powershell
Invoke-WebRequest https://github.com/cwtools/cwtools-vic2-config/archive/refs/heads/master.zip -OutFile cw.zip; Expand-Archive cw.zip -DestinationPath _cw; Move-Item _cw/cwtools-vic2-config-master .cwtools; Remove-Item cw.zip, _cw -Recurse
```

The Vic2 rule set is a 2020 stub: run unfiltered it reports tens of thousands of "errors" on this mod, nearly all rule gaps (it does not know `NOT`, `OR`, `months`, unit names, tags...). Two things make it usable anyway:
- `.claude/skills/cwtools-lsp/` is a project-scope Claude Code LSP plugin. It runs the server behind `.claude/skills/cwtools-lsp/bin/cwtools_lsp.py proxy`, which locates `CWTools Server.exe` inside the editor extension, injects the Vic2 init options and settings the server needs, and drops the noise classes so only parse errors, "Too many X" duplicates and warnings reach Claude after an edit. It loads once the workspace is trusted; check `/plugin` > Errors if diagnostics never appear.
- `python scripts/cwtools_check.py` runs the same thing headless over the whole mod (about 20 s); `--all` shows the unfiltered output, `--summary` groups it, `--via-proxy` exercises the plugin wiring. The current known-false-positive baseline lives in `.claude/skills/validate/SKILL.md`; treat anything not listed there as new.
`scripts/modcheck.py` and the game's `error.log` remain the source of truth.
