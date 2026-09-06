---
name: validate
description: Run the mod's full check pipeline - static checks, deploy to the game folder, Audax Validator, and a diff of the game's error.log. Use before committing or after any batch of content changes.
disable-model-invocation: true
argument-hint: [static|deploy|game]
---

# validate

There is no compiler or test runner for this mod. This skill is the closest thing. Run the stages in order; stop and report at the first stage that fails. If an argument is given, run only that stage.

## Stage 1: static (no game needed)

```
python scripts/modcheck.py ids
python scripts/modcheck.py decisions        # must be 0: a decisions file without its political_decisions wrapper shows raw effect_title entries in game
python scripts/modcheck.py province-paths   # must be 0 path problems: a moved province file un-shadows vanilla and crashes at Executing History
python scripts/modcheck.py shadow           # vanilla files the mod fails to shadow: a renamed or omitted twin loads alongside ours
python scripts/modcheck.py encoding
python scripts/modcheck.py braces $(git diff --name-only HEAD -- 'CoE_RoI_R/**/*.txt')
python scripts/modcheck.py provinces $(git diff --name-only HEAD -- CoE_RoI_R/events CoE_RoI_R/decisions CoE_RoI_R/history)
python scripts/modcheck.py tags      $(git diff --name-only HEAD -- CoE_RoI_R/events CoE_RoI_R/decisions CoE_RoI_R/history)
python scripts/gfxtool.py missing
python scripts/refcheck.py
for f in CoE_RoI_R/localisation/*.csv; do python scripts/modcheck.py loc-check "$f"; done
```

If nothing is modified in the working tree, use `git diff --name-only HEAD~1` instead so the last commit is checked. For a full sweep use `CoE_RoI_R/events/*.txt CoE_RoI_R/decisions/*.txt CoE_RoI_R/common/*.txt`.

`braces`, `provinces` and `tags` take file paths, not directories, and the whole tree overflows
the command line in one go — sweep it a directory at a time:

```
for d in events decisions history/countries history/diplomacy history/wars; do
  find CoE_RoI_R/$d -name '*.txt' -print0 | xargs -0 python scripts/modcheck.py provinces
done
```

### Stage 1 baseline (re-measured 2026-09-06)

One line per check. Anything not on this list is a regression.

| Check | Expected now | Note |
|---|---|---|
| `ids` duplicates | 1 | duplicate 300999 inside `events/PERFlavour.txt`. Only the duplicate count is an invariant; the id total (3156 on 2026-09-06) drifts up as chains are added |
| `encoding` (`localisation`) | 12 files | vanilla-inherited csvs with NEL (0x85) or 0x9d bytes |
| `encoding` (`events`, `decisions`, `common`, `history`) | 0 | every script `.txt` in the mod is CRLF |
| `gfxtool missing` | 0 lines | must print nothing |
| `provinces` / `tags`, whole tree | 0 | events, decisions, history/countries, history/diplomacy, history/wars |
| `refcheck events` | 14 | 12 deliberately abandoned `is_triggered_only` events (1002, 90903, 95259, 95652, 95655, 97120, 98230, 99665, 99666, 99993, 290115, 375003) plus 99932 and 8016451, which have a trigger and no MTTH on purpose |
| `modcheck shadow` | 3 | `events/Arabia event.txt` and `events/ReformJealousy.txt` (vanilla content nobody chose to keep; no id collisions, no province refs) and `history/units/v2dd2.txt` (a Paradox dev-diary text file, not script). The `history/pops/1836.1.1`, `history/pops/1861.4.14` and `history/units/1861` lines are informational: `common/bookmarks.txt` has only the 1821.9.1 start, so nothing reaches them - add a bookmark and they load vanilla pops onto this map |
| `refcheck loc` | 2 | 2 rows for abandoned event 290115. Party names in `common/countries/` (registered tags only) and state names in `map/region.txt` are covered here as of 2026-09-06. The 58 unlocalised `common/event_modifiers.txt` names moved to `refcheck defs` and were filled in 2026-09-06 |
| `refcheck defs` | 0 | player-visible definition names (modifiers, issue options, ideologies, cultures, casus belli, techs, inventions, tags, ...) with no localisation key. Must stay 0 |
| `refcheck flags` | 116 | orphans: 111 set but never checked, 5 checked but never set. `from_liberation_to_conquest` (`00_CoE_RoI.txt:1164`) joined the list on 2026-09-06: it was written `set_country_flag = { x }`, which refcheck did not read as a set and which desynced the engine parser; fixing the syntax exposed the dead flag. Event 99985 sets it and 99984 clears it, nothing reads it. `hosting_the_congo_conference` (set, unread) and `congo_reform_association_active` (read, unset) joined on 2026-09-06 with `decisions/GreatPowers.txt`: both were inherited verbatim from vanilla's file, whose Congo Reform Association event chain PDM does not carry - `annex_the_congo` is dormant by design. Drifts as chains land; none is a spelling variant of a real flag. `check_flags()` scans `common/` as of 2026-09-06 - before that it missed every flag set from `cb_types.txt` `on_po_accepted` and reported 6 live flags as dead. The 3 remaining are design calls, not bugs: `the_watchers_on_the_wall` is the commented-out "Crises Disabled" toggle (`crises.txt:686`), `slave_trader`/`slave_trade_leader`/`slave_trade_reinstated` need the half-built CSA slave-trade chain finished - do NOT just set `slave_trader`, it makes 16602 (MTTH 1 month) reachable and its `clr_country_flag = the_slavery_debate` unlocks the `no_slavery` reform before 1875 (`issues.txt:277`) and `emancipation_proclamation` before the ACW (`ACW.txt:286`) |
| `modcheck desync` | 0 | effect-only scopes used as triggers, bare `province_event = <id>`, scalar effects given a block. Must stay 0 |
| `modcheck engine-counts` | 0 | needs a `gametest.ps1` launch first; diffs the engine's per-file decision/event counts in `setup.log` against a parse. Any mismatch is a parser desync whatever the cause. Must stay 0 |
| `refcheck options` | 8 | events with 6-8 options |
| `refcheck onactions` / `modifiers` / `names` | 0 | |
| `loc-check` malformed rows | 51 across 19 csvs | missing `x` terminator. The 110 rows in `0000_economic_rework.csv`, `newCE.csv` and `PDM_CE.csv` were normalised on 2026-09-06 (terminator column only; no text touched) - those three files must stay at 0 missing-terminator rows (`PDM_CE.csv` keeps its 3 inherited split rows, counted in the row below). `GVG_events.csv` is clean and must stay clean |
| `loc-check` split rows (`;` inside English text) | 13 | all vanilla/PDM-inherited: `00_PDM_events.csv` 2, `00_PDM_GAGA.csv` 2, `00_PDM_goods.csv` 1, `000_persia_events.csv` 1, `000_persia_map.csv` 1, `PDM_CE.csv` 3, `Taiping(move_later).csv` 1, `text.csv` 2 |
| `loc-check` odd-width rows (not 15 columns) | 27904 across 48 files | harmless trailing/missing empty language columns, dominated by `text.csv` |

New GVG content must add none of the localisation findings.

## Stage 1b: CWTools (headless, no game needed)

```
python scripts/cwtools_check.py
```

Filtered output; see `.claude/skills/cwtools-lsp/SKILL.md` for what the filter drops. Baseline (re-measured 2026-09-06): **14 diagnostics, 0 errors, 14 warnings** over ~780 files — 2 "Too many attacker_goal" (`CBsAndCores.txt:2467`, `Indochina.txt:188`; multiple war goals in one `war` effect are valid) and 12 "Too many clauses" in `common/production_types.txt`. Both are rule gaps. Anything else is new.

## Stage 1c: subsystem audits (optional, no game needed)

Slower than stage 1 (`audit_perf` and `audit_provinces` take the longest) and mostly advisory.
Run the set after a large or cross-cutting change; skip it for a one-file edit.

```
for s in countries parties provinces diplomacy decisions common loc events perf; do python scripts/audit_$s.py; done
python scripts/audit_fire_once.py
python scripts/audit_owner_scope.py
python scripts/audit_pacing.py
python scripts/audit_religion.py
python scripts/audit_religion.py check
```

Every script is expected at **0 `[high]`**. Baseline exceptions (re-measured 2026-09-06):

| Script | Expected now | Note |
|---|---|---|
| `audit_countries.py` | 0 highs | the 39 unregistered tags (BMK, DUR, ERT, KRL, KYR, ...) were registered on 2026-09-06; `registered` is now 521. All its counters (`unregistered`, `capital_not_owned`, `party_inactive`, `party_undefined`, `ideology_not_allowed`, `missing_common_file`) must stay 0. The 84 mediums are `REB` (the engine rebel tag has no capital/culture/government by design) plus the `D01`-`D50` dominion tags with no capital |
| `audit_events.py` | 0 highs, 0 unknown keywords | any new high is a regression |
| `audit_fire_once.py` | 124 findings (A 77, B 10, C 37) | a *list*, not a defect count: every self-firing `country_event` with engine-wide `fire_only_once` and no bare `tag =` / `owns =` test. Most class-A entries are alternative tags for one nation (`OR(ENG,ENL)`, ...); class C is genuine world events. Verdicts in `docs/audit/fire-only-once.md` — only review entries newer than that file |
| `audit_owner_scope.py` | 0 highs, 154 lows (see `docs/audit/owner-scope.md`) | advisory. Every low is a conditional release/secede or cede branch where the scope may legitimately own the province later in the game; a **high** means the block is dead in every reachable state and must be rescoped (`TAG = { any_owned = ... }`) |
| `audit_pacing.py` | exit 0, no `[high]` class | advisory. Current snapshot (28 runaway repeaters, 0 narrow-window) is `docs/audit/pacing-1821-1836.md`; `--write` rewrites it |
| `audit_religion.py` | exit 0 | read-only inventory of religion triggers/effects vs what the pops carry; snapshot in `docs/audit/religion-dead-content.md`. Since the 2026-09-06 restoration pops carry real religions, so the inventory reports no dead pop-religion sites |
| `audit_religion.py check` | **exit 0, 0 problems - hard invariant** | the religion-restoration regression gate: no pop may hold a culture name in the religion field, no `has_pop_religion`/`religion` trigger may name a culture, no `culture = german\|italian` site may exist (both cultures have 0 pops), and `common/religion.txt` must define no culture as a religion. Any finding here is a regression, not a baseline |
| `audit_parties.py`, `audit_provinces.py`, `audit_diplomacy.py`, `audit_decisions.py`, `audit_common.py`, `audit_loc.py`, `audit_perf.py` | 0 highs | medium/low findings are carried in the reports under `docs/audit/` |

`audit_provinces.py` and `audit_loc.py` rewrite their report file, so `git diff docs/audit/`
after a run is expected. `scripts/audit_events2.py` emits JSON rather than `[high]` lines and
is read on demand, not as part of this loop.

## Stage 2: deploy

```
pwsh -File scripts/deploy.ps1
```

Mirrors `CoE_RoI_R/` into `D:\Steam\steamapps\common\Victoria 2\mod\` and verifies a 1:1 hash match. Non-zero exit means the deploy target is out of sync; show the output.

## Stage 3: Audax Validator (GUI, user runs it)

The validator has no command line. Tell the user:

1. Launch `Audax.Validator\Validator.exe`.
2. Game Path: `D:\Steam\steamapps\common\Victoria 2`. Game: Victoria 2. Mod Name: `CoE_RoI_R`. Click Validate.
3. Save or paste the output.

Then read the output and group it: errors first, then warnings, dropping the noise already suppressed by `CoE_RoI_R/ValidatorSettings.txt`.

## Stage 4: in-game error.log

Log path: `E:\OneDrive\Documents\Paradox Interactive\Victoria II\CoE_RoI_R\logs\error.log`

1. Record the current size and line count (or note the file is absent).
2. Ask the user to launch `victoria2.exe`, tick the mod, start the 1821 bookmark, and let it run to the first month end.
3. Read only the lines appended since step 1 and summarise them by file/type. Any line mentioning a province id, missing localisation key, or unknown trigger/effect gets called out with the likely source file.

### Open in-game checks

Things static analysis cannot settle. Confirm these while the game is up and tick them off here.

- [ ] **`rich_luxury_needs`** - 17 commerce technologies in `technologies/commerce_tech.txt` grant this modifier. Vanilla never uses that exact key (it uses `middle_luxury_needs`, `poor_luxury_needs`, `rich_life_needs`, `rich_everyday_needs`), and the engine logs nothing for an unknown modifier key. Open the tech tree, hover a commerce tech such as `freedom_of_trade`, and confirm the rich-luxury line appears in the tooltip. If it does not, the bonus is dead on all 17 and the key needs replacing. Raised 2026-09-06 by `audit_diplomacy.py`.

A crash at launch is almost always a brace error (stage 1 should have caught it). A crash on Start Game or on a specific date is a content error: bad province id, unknown production type, or an event/history entry firing that day.
