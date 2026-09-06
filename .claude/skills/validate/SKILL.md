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
| `refcheck loc` | 60 | 58 hidden/utility modifiers in `common/event_modifiers.txt` with no localisation, plus 2 rows for abandoned event 290115 |
| `refcheck flags` | 119 | orphans: 97 set but never checked, 30 checked but never set. Drifts as chains land; none is a spelling variant of a real flag |
| `refcheck options` | 8 | events with 6-8 options |
| `refcheck onactions` / `modifiers` / `names` | 0 | |
| `loc-check` malformed rows | 161 across 21 csvs | UTF-8 and/or missing `x` terminator; mostly `0000_economic_rework.csv`, `PDM_CE.csv`, `newCE.csv`. `GVG_events.csv` is clean and must stay clean |
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
```

Every script is expected at **0 `[high]`**. Baseline exceptions (re-measured 2026-09-06):

| Script | Expected now | Note |
|---|---|---|
| `audit_countries.py` | 39 highs | all "history file for tag X is not registered in `common/countries.txt`" (BMK, DUR, ERT, KRL, KYR, ...). Deferred — register or delete. Its other counters (`capital_not_owned`, `party_inactive`, `party_undefined`, `ideology_not_allowed`, `missing_common_file`) must stay 0 |
| `audit_events.py` | 0 highs, 0 unknown keywords | any new high is a regression |
| `audit_fire_once.py` | 124 findings (A 77, B 10, C 37) | a *list*, not a defect count: every self-firing `country_event` with engine-wide `fire_only_once` and no bare `tag =` / `owns =` test. Most class-A entries are alternative tags for one nation (`OR(ENG,ENL)`, ...); class C is genuine world events. Verdicts in `docs/audit/fire-only-once.md` — only review entries newer than that file |
| `audit_owner_scope.py` | 0 highs, 148 lows (see `docs/audit/owner-scope.md`) | advisory. Every low is a conditional release/secede or cede branch where the scope may legitimately own the province later in the game; a **high** means the block is dead in every reachable state and must be rescoped (`TAG = { any_owned = ... }`) |
| `audit_pacing.py` | exit 0, no `[high]` class | advisory. Current snapshot (28 runaway repeaters, 0 narrow-window) is `docs/audit/pacing-1821-1836.md`; `--write` rewrites it |
| `audit_religion.py` | exit 0 | read-only inventory of religion triggers/effects vs what the pops carry; snapshot in `docs/audit/religion-dead-content.md`. The dead-trigger count only drops if the design question is resolved |
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

A crash at launch is almost always a brace error (stage 1 should have caught it). A crash on Start Game or on a specific date is a content error: bad province id, unknown production type, or an event/history entry firing that day.
