# Legacy audit — generic government machinery

Scope: `CoE_RoI_R/events/Monarchy.txt` (800110-800123, 8001160),
`CoE_RoI_R/events/Dictatorship.txt` (20001-20010),
`CoE_RoI_R/events/UpperHouse.txt` (18000-18230).
Format: `file line id — problem — fix`. FIXED items were applied in this pass.

## Fixed

- Dictatorship.txt 199-207 / 225-233, id 20001 — **[high]** both options of the province-scope
  "Underground newspaper" event did `add_country_modifier = { name = freedom_talks duration = -1 }`.
  The event is repeatable and fires once per province, and Vic2 stacks duplicate country modifiers,
  so a large dictatorship accumulated dozens of permanent
  `global_pop_consciousness_modifier = 0.01` copies that nothing ever removed — the cleanup events
  20002/20007/20008/20009 each call `remove_country_modifier` once, which strips one copy.
  Monarchy.txt's equivalent (800116) already used remove + `duration = 365`.
  — FIXED: `remove_country_modifier = freedom_talks` before the add, and `duration = 730`.
- Dictatorship.txt 594, id 20004 — **[medium]** mtth modifier tested
  `has_country_flag = failed_ruler_assassination`; no such flag is ever set anywhere in the mod
  (the chain sets `failed_assassination_attempt`, in 20005). Dead modifier: the "revolutionaries are
  arrested faster after a botched attempt" speed-up never applied.
  — FIXED: renamed to `failed_assassination_attempt`.
- Dictatorship.txt 779, id 20007 — **[medium]** mtth modifier tested
  `has_country_flag = revolutionary_society`, but `revolutionary_society` is an event *modifier*
  (`common/event_modifiers.txt`), never a flag. Dead branch: the 0.7 speed-up on the revolution
  never applied. — FIXED: `has_country_modifier = revolutionary_society`.
- UpperHouse.txt 161/168, id 18060 — **[medium]** both option names were copy-pasted from 18050
  (`EVTOPTA18050` "Motion carries" / `EVTOPTB18050`), so the event showed the wrong button text.
  — FIXED: `EVTOPTA18060` / `EVTOPTB18060`. `EVTOPTB18060` was missing from localisation and was
  added to `localisation/newCE.csv` ("We cannot ignore their demands").
- UpperHouse.txt 738/745, id 18160 — **[medium]** same copy-paste: option names `EVTOPTA18150` /
  `EVTOPTB18150`. `EVTOPTA18160`/`EVTOPTB18160` already exist in `text.csv` and were simply unused.
  — FIXED: pointed at the 18160 keys.
- Monarchy.txt 1325, id 800121 and 1446, id 800122 — **[medium]** country-scope trigger used the
  pop-scope condition `consciousness = 3` / `consciousness = 4`. At country scope the engine's
  condition is `average_consciousness` (`docs/wiki/list-of-conditions.md` lists `consciousness`
  only in the pop section). Only 4 occurrences exist mod-wide, 2 of them here.
  — FIXED: `average_consciousness`. The other two, SWEFlavor.txt 839/856, are outside this scope.
- UpperHouse.txt 776, id 18170 — **[low]** lowercase `not = { ... }`. Works, but every other
  trigger in the family uses `NOT`. — FIXED: normalised to `NOT`.

## Reported, not changed

- UpperHouse.txt 1240-1250 and 1360-1370, id 18210 — **[medium, ambiguous]** options 2 and 3 each
  apply `scaled_consciousness = { ideology = reactionary factor = 4 }` immediately followed by
  `scaled_consciousness = { ideology = reactionary factor = 2 }` on the same `rich_strata` scope.
  A duplicated key on one scope; the parallel construction in Monarchy.txt (800123) pairs
  reactionary with conservative at half the factor, so the second block was probably meant to read
  `ideology = conservative`. Left alone because the intent cannot be proven; the effect today is at
  worst a wasted or doubled consciousness tick.
- UpperHouse.txt 2182/2208, id 18225 — **[low]** `ai_chance = { factor = 100 }` on "ban public
  meetings" against `factor = 0` on "keep the rules" — the AI *always* rolls the reform back.
  This is the house pattern for the whole reactionary-upper-house family (18210/18220/18230 use
  90 / 10 / 0; 18215 uses 100 / 0), so it is consistent rather than a typo, but it means no AI
  country ever resists a reactionary upper house. Worth a deliberate balance pass, not a bug fix.
- UpperHouse.txt 1394, id 18215 and 1991, id 18225 — **[low]** unlike 18210/18220/18230 these two
  have no "Don't bring this up again" option, hence no `cutoff_reactionary_UH_*` flag
  (`cutoff_reactionary_UH_2` and `_4` do not exist). Both are self-limiting through their triggers
  (`public_meetings = yes_meeting`; `NOT = { has_country_flag = no_party_appointed_rollback }`),
  so there is no loop, but the player has no permanent opt-out for those two.
- Dictatorship.txt 39, id 20010 — **[low]** `year = 1865` gates the whole presidential-dictatorship
  chain. On a 1821 start that is 44 years of dead content; the gate looks inherited from the vanilla
  1836 timeline. `scripts/audit_events.py` already lists this class of finding as [info].
- Dictatorship.txt 378-397, id 20002 option A — **[low]** `ai_chance` base 10 with `factor = 0`
  when `NOT = { average_militancy = 1 }`, against 90 on "send troops". The AI essentially never
  concedes democracy at this stage; the peaceful path is a player-only branch. Deliberate-looking,
  but it makes 20002-A dead content for the AI.
- Dictatorship.txt 402-410, id 20002 option B — **[low]** `growing_unrest` at `duration = -1`.
  Permanent, but the event is one-shot per country (it sets `dictator_assassination_attempts`,
  which its own trigger excludes) and 20006/20007/20008/20009 all remove it, so it cannot stack.
- Monarchy.txt 1195, id 800119 — **[low]** trigger is only
  `has_country_modifier = revolutionary_society` with no government check, so a country that leaves
  absolute monarchy while the modifier is up still gets "revolutionaries arrested". Harmless —
  800120 clears the modifier on the same tick at `days = 1` — but the sibling 800118 does gate on
  government.
- UpperHouse.txt 545, id 18120 — **[low]** option A moves the upper house by
  `conservative value = 0.5` when the trigger already requires conservative >= 0.4. Every other
  event in the file moves 0.05-0.25. Same shape at 18090 (`liberal 0.45`) and 18130
  (`socialist 0.5`, arguably intentional for "Red Winds"). Balance call, left alone.

## Checks that came back clean

- `liberal_revolution(s)_should_now_fire` flag family: 9 references mod-wide, all spelled
  `liberal_revolutions_should_now_fire`, set exactly once (`LiberalRevolutions.txt:249`) and read by
  Monarchy.txt:414, LiberalRevolutions.txt, VassalRebellion.txt, Ottoman_Event.txt, PAPFlavor.txt,
  HUN.txt and NET.txt. No typo survives.
- Every `government = X` in the three files resolves to an entry in `common/governments.txt`,
  including the `*2`/`*3` variants, which do exist (`absolute_monarchy2/3`,
  `prussian_constitutionalism2/3`, `hms_government2/3`, `presidential_dictatorship2/3`, ...).
- Every `political_reform =` / `social_reform =` value used as an effect
  (`party_appointed`, `censored_press`, `state_press`, `no_meeting`, `none_voting`,
  `landed_voting`, `wealth_voting`, `wealth_weighted_voting`, `universal_weighted_voting`,
  `universal_voting`, `secret_ballots`, `non_secret_ballots`, `gerrymandering`, `harassment`,
  `underground_parties`, `population_equal_weight`, `trinket_health_care`, `trinket_subsidies`)
  is a real option in `common/issues.txt`.
- Every `add_country_modifier` / `add_province_modifier` name (`freedom_talks`, `growing_unrest`,
  `revolutionary_society`, `power_vacuum`, `underground_newspaper`) exists in
  `common/event_modifiers.txt`; so do `springtime_of_nations` and `global_liberal_agitation`.
- 18210's franchise-rollback ladder is ordered from the widest franchise down
  (universal -> universal_weighted -> wealth -> wealth_weighted -> landed), so the four sequential
  `random_owned` blocks cannot cascade a country several steps in a single option.
- `country_event = 800054`, fired by 20002 and 20007, exists — `Revolution_Event.txt:794`.
- No multi-statement `NOT` in these files relies on NAND semantics: every one reads correctly as NOR.
- No `fire_only_once` in any of the three files; all repeatable chains are gated by country flags.
- No pop-religion tests in these files.
