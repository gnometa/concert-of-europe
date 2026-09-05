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
```

If nothing is modified in the working tree, use `git diff --name-only HEAD~1` instead so the last commit is checked. For a full sweep use `CoE_RoI_R/events/*.txt CoE_RoI_R/decisions/*.txt CoE_RoI_R/common/*.txt`.

Known pre-existing findings (as of 2026-09-05) that are not regressions:
- `ids`: duplicate 300999 inside `events/PERFlavour.txt`; duplicate 2000000 between `events/SetupGVG.txt` and `decisions/SetupGVG.txt`.
- `encoding`: a dozen vanilla-inherited localisation csvs contain NEL (0x85) or 0x9d bytes.
- `loc-check`: about 160 malformed rows across 21 csvs, mostly `0000_economic_rework.csv`, `newCE.csv`, `PDM_CE.csv` (UTF-8 and/or missing `x` terminator).

Report any finding **not** in that list as a regression.

## Stage 1b: CWTools (headless, no game needed)

```
python scripts/cwtools_check.py
```

Filtered output; see `.claude/skills/cwtools-lsp/SKILL.md` for what the filter drops. Known baseline (2026-09-05): "Too many attacker_goal" in `CBsAndCores.txt:2448` and `Indochina.txt:188` (multiple war goals in one `war` effect are valid; rule gap), and 12 "Too many clauses" warnings in `production_types.txt` (rule gap). Anything else is new.

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
