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
```

If nothing is modified in the working tree, use `git diff --name-only HEAD~1` instead so the last commit is checked. For a full sweep use `CoE_RoI_R/events/*.txt CoE_RoI_R/decisions/*.txt CoE_RoI_R/common/*.txt`.

Known pre-existing findings (re-measured 2026-09-06 after the post-`464f3abf` content batch — the 1831 Italian risings, USA sectional crisis, Java War, Russo-Turkish War and Qing opium chains) that are not regressions:
- `ids`: duplicate 300999 inside `events/PERFlavour.txt`. Exactly 1 duplicate; the id total drifts upward as chains are added (3156 on 2026-09-06, after the ASH/Vormaerz/Brazil/Japan/Ayacucho/WarResolutions batch) - only the duplicate count is an invariant.
- `encoding`: 12 vanilla-inherited localisation csvs contain NEL (0x85) or 0x9d bytes (`modcheck encoding CoE_RoI_R/localisation`). `modcheck encoding CoE_RoI_R/events`, `.../decisions`, `.../common` and `.../history` must all be 0 - every script `.txt` in the mod is CRLF.
- `loc-check`: 161 malformed rows across 21 csvs, mostly `0000_economic_rework.csv` (55), `PDM_CE.csv` (28), `newCE.csv` (27) (UTF-8 and/or missing `x` terminator). `GVG_events.csv` is clean and must stay clean.
- `loc-check` column checks (added 2026-09-06): the command now also reports (a) rows where a `;` typed inside the English text splits it across the English and French columns, and (b) a per-file count of rows that are not exactly 15 columns wide. Baseline over `CoE_RoI_R/localisation/*.csv`: **13 split rows** (all vanilla/PDM-inherited: `00_PDM_events.csv` 2, `00_PDM_GAGA.csv` 2, `00_PDM_goods.csv` 1, `000_persia_events.csv` 1, `000_persia_map.csv` 1, `PDM_CE.csv` 3, `Taiping(move_later).csv` 1, `text.csv` 2; `GVG_events.csv:16` `EVTDESC999999` was fixed in `48a906ce` and no longer counts) and **27904 odd-width rows across 48 files** (harmless trailing/missing empty language columns, dominated by `text.csv`). New GVG content must add none of either.
- `refcheck` (baseline re-measured 2026-09-06): `events` 14 - the deliberately abandoned `is_triggered_only` events (1002, 90903, 95259, 95652, 95655, 97120, 98230, 99665, 99666, 99993, 290115, 375003) plus 99932 and 8016451 having a trigger with no MTTH (intentional: they fire the moment the trigger is true). `loc` 60 - 58 hidden/utility entries in `common/event_modifiers.txt` with no localisation, plus event 290115 (an abandoned event). `flags` 129 - orphan flags: 98 set but never checked and 31 checked but never set (the count drifts 129-133 as chains are added and as orphans are closed); none of the remaining ones is a spelling variant of a real flag. `options` 8 - events with 6-8 options. `onactions`, `modifiers` and `names` must stay at 0.
- `provinces` and `tags` over the whole tree (events, decisions, history/countries, history/diplomacy, history/wars) must stay at 0.

Report any finding **not** in that list as a regression.

## Stage 1b: CWTools (headless, no game needed)

```
python scripts/cwtools_check.py
```

Filtered output; see `.claude/skills/cwtools-lsp/SKILL.md` for what the filter drops. Known baseline (re-measured 2026-09-06): **14 diagnostics, 0 errors, 14 warnings** over ~760 files - "Too many attacker_goal" in `CBsAndCores.txt:2448` and `Indochina.txt:188` (multiple war goals in one `war` effect are valid; rule gap), and 12 "Too many clauses" warnings in `production_types.txt` (rule gap). Anything else is new.

## Stage 1c: subsystem audits (optional, no game needed)

Slower than stage 1 (`audit_perf` and `audit_provinces` take the longest) and mostly advisory.
Run the set after a large or cross-cutting change; skip it for a one-file edit.

```
for s in countries provinces diplomacy decisions common loc events perf; do python scripts/audit_$s.py; done
python scripts/audit_fire_once.py
python scripts/audit_pacing.py
```

Expect **0 `[high]`** from every script except these known baselines (re-measured
2026-09-06):

- `audit_countries.py`: **39 highs**, all "history file for tag X is not registered in
  `common/countries.txt`" (BMK, DUR, ERT, KRL, KYR, ...). Deferred — register or delete.
  Its other counters must stay at 0: `capital_not_owned`, `party_inactive`, `party_undefined`,
  `ideology_not_allowed`, `missing_common_file`.
- `audit_events.py`: **0 highs** (was 2 - 14540 and 22540, the re-firing events that granted
  a permanent `add_province_modifier`; both were given a country-flag guard in `70f3afaa` /
  `9dd159f0`, so any new high is a regression). `unknown keywords` must stay at **0**.
- `audit_fire_once.py`: **124 findings** (class A 77, B 10, C 37) and rising - it is a *list*,
  not a defect count. `fire_only_once` is engine-wide, so it lists every self-firing
  `country_event` with `fire_only_once` and no bare `tag =` / `owns =` test. Nearly all class-A
  entries are alternative tags for the same nation (`OR(ENG,ENL)`, `OR(AUS,KUK)`, ...) and class C
  is genuine world events. The verdicts are in `docs/audit/fire-only-once.md`; only check entries
  that are new since that file was written.
- `audit_pacing.py`: advisory report, **exit 0**, no `[high]` class. It lists the 1821-1836
  event load per playable tag plus same-day cascades and runaway repeaters; the current
  snapshot (28 repeaters, 0 narrow-window) is `docs/audit/pacing-1821-1836.md`, which also
  records the entries that were reviewed and deliberately left. `--write` rewrites it.

`audit_provinces.py`, `audit_diplomacy.py`, `audit_decisions.py`, `audit_common.py`
(`DEFECTS high=0`), `audit_loc.py` and `audit_perf.py` are all at 0 high. Their medium/low
findings are carried in the reports under `docs/audit/`; `audit_provinces.py` and
`audit_loc.py` rewrite their report file, so `git diff docs/audit/` after a run is expected.

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
