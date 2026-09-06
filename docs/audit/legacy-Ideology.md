# Legacy audit — ideology enablement and ideology strongholds

Files: `events/IdeologyEnabling.txt` (393 lines, ids 1000-1004),
`events/Socialism_Fascism.txt` (4,989 lines, ids 17500-17730),
`events/Ideology_Strongholds.txt` (1,683 lines, ids 880010-880072).

Baseline at review time: modcheck braces clean, no duplicate ids in these files,
refcheck 14/0/60/0/127/0/8, audit_events unknown 0 / high 0, every ideology name used
in the three files exists in `common/ideologies.txt`, every government tag exists in
`common/governments.txt`, all province modifiers resolve. The mechanical surface is
clean; everything below is logic, not syntax.

## Context: how an ideology actually turns on

`common/ideologies.txt` auto-enables by date — anarcho_liberal 1848, socialist 1860,
communist 1865, social_liberal 1900, fascist 1905. `IdeologyEnabling.txt` is only an
*early* unlock on top of that, gated on inventions. Note the mod's renaming: event
1000 ("Enable Socialists") enables the `communist` ideology, event 1001 ("Enable
Communists") enables `socialist` (= social democracy). Nothing here breaks the 1821
start: the 2,301 parties whose `start_date` predates their ideology
(docs/audit/parties.md) stay inert and go live on the dates above, normal PDM behaviour.

## Findings

### [high]

`events/Socialism_Facism.txt` — 0-byte stray file, a misspelling of
`Socialism_Fascism.txt`; the engine parses it as an empty file and it invites future
edits to the wrong path — **fixed**: removed with `git rm`.

### [medium]

`IdeologyEnabling.txt:93 (id 1001)` — the chain 1000 (communist) -> 1001 (socialist)
is inverted by `common/ideologies.txt`, where socialist auto-enables in **1860** and
communist in **1865**. 1001 requires `is_ideology_enabled = communist` *and*
`NOT = { is_ideology_enabled = socialist }`, so from 1860 on it can never fire; its
only window is a game where event 1000 unlocked communist before 1860 — fix: swap the
two `date =` lines in `common/ideologies.txt` (socialist 1866, communist 1860) so the
dates match the event order. Not applied here: `ideologies.txt` is shared with the
party and reform audits and moving a date shifts hundreds of parties' activation, so
it needs its own balance pass.

`IdeologyEnabling.txt:177 (id 1002)` — the anarcho-liberal unlock is dead **twice
over**: `is_triggered_only = yes` with no caller anywhere in `events/` or
`decisions/`, plus `trigger = { always = no ... }`, plus a `mean_time_to_happen` that
can never be reached. Harmless in practice (the 1848 date still enables the ideology)
but it is the only enabling event with no path to `enable_ideology`, so its
`invention = populism_vs._establishment` prerequisite is decorative — fix: either
delete the event or drop `is_triggered_only`/`always = no` to restore the invention
gate. Left alone: `always = no` reads as a deliberate disable, and re-enabling it
would move anarcho-liberals earlier than 1848.

`Socialism_Fascism.txt:20, 235, 403, 629, 782, 1035, 1190, 1346, 1494, 1702` — every
socialism event gates on `is_ideology_enabled = socialist`, i.e. on the *second* link
of the chain (event 1001 / 1860), while the communist-flavour events at 4108, 4345,
4553 and 4757 gate on `is_ideology_enabled = communist`. Under the mod's renaming the
labour-union and strike content is conceptually "socialism" = `communist`, so the
whole 17500-17590 block unlocks a full ideology-step later than the fiction implies —
fix: retarget 17500-17590 to `is_ideology_enabled = communist`. Not applied: this
moves ten events' start date by years and belongs with the date swap above.

`Socialism_Fascism.txt` — every country event here uses the same five-way government
`OR` (prussian_constitutionalism, democracy, hms_government, absolute_monarchy,
theocracy). All 30 tags in `common/governments.txt` are valid, but
`presidential_dictatorship` and `bourgeois_dictatorship` are excluded from **all**
socialism and fascism flavour except 17715, so a country that falls into either gets
no ideology content at all — fix: add both to the shared OR list. Not applied: it
widens the firing population of 23 events at once.

`Socialism_Fascism.txt:2228 (17610 opt A), 2452 (17620 opt B), 2864 (17640 opt A),
4290 (17710 opt A)` — each event is guarded by `NOT = { has_province_modifier = X }`
(black_shirts / fascist_welfare / free_corps / militant_trade_union) but only *one* of
the two options applies X. Choosing the other leaves the guard unset, so the event
re-rolls at the same mtth with nothing changed. Not a spam risk at mtth 300-400
months, but the two options are not symmetric in cost — fix: give the passive option a
short-duration cooldown modifier. Not applied: it is a balance change.

`Ideology_Strongholds.txt:993 (880050)` — the socialist stronghold pair was the only
family inconsistent with itself: the small-nation variant 880052 requires
`is_core = THIS` while the large-nation 880050 did not, so a great power could grow a
socialist stronghold in freshly conquered non-core land that no other ideology can
use — **fixed**: added `is_core = THIS`, matching 880052 and the reactionary and
conservative pairs.

`Socialism_Fascism.txt:2423, 2462 (17620)` — the option limits tested
`unemployment = 0.1` while the event trigger requires `unemployment = 0.2`, so
`random_state` could pick a state that never satisfied the trigger — **fixed**: both
limits raised to 0.2 to match the trigger.

### [low]

`Ideology_Strongholds.txt` — the seven stronghold families use three different
ownership gates: `is_core = THIS` (reactionary 880010/880012, conservative
880020/880022, socialist 880050/880052), `is_primary_culture = yes` (fascist
880070/880072) and *nothing at all* (liberal 880030/880032, anarcho-liberal
880040/880042, communist 880060/880062). Each pair is now internally consistent, so
this is cosmetic drift rather than a bug — fix: pick one gate for all seven families.

`IdeologyEnabling.txt:334 (id 1004)` — the social-liberal event uses literal English
`title = "Social Liberalism"`, `desc` and option name instead of `EVTNAME1004` /
`EVTDESC1004` / `EVTOPTA1004`; those keys exist in no csv. It renders (the engine
falls back to the literal) but it is the only event in the file without localisation
and cannot be translated — fix: add the three keys with `modcheck.py loc-add` and
switch to key references.

`Socialism_Fascism.txt:4290, 4330, 4869, 4905` and the option names throughout
`Ideology_Strongholds.txt` — raw English strings ("Let them talk.", "Unfortunate for
them.", "They had best not cause trouble.") rather than `EVTOPTA<id>` keys, unlike the
17500-17620 block which uses keys consistently. Same fix as above.

`IdeologyEnabling.txt:74 and 331` — `any_country = { set_variable = { which =
successful_communist_rebellions value = 0 } }` never touches the firing country itself
(`any_country` excludes THIS), so the enabling country starts with the variable unset
rather than 0. `check_variable` on an unset variable reads 0 anyway, so there is no
observable effect.

`Socialism_Fascism.txt:3110 (17660)` — "The Massacre" has no `is_colonial = no` on its
`any_owned_province` clause, unlike its neighbours 17610/17620/17640/17690. Reaching
it needs a colonial province carrying `black_shirts`, which only 17610 grants and 17610
does exclude colonies, so it is unreachable rather than wrong.

`Socialism_Fascism.txt:4290 (17710 opt A)` — `ai_chance = { factor = 25 modifier = {
factor = 0 average_militancy = 4 } }` means the AI *never* cracks down once average
militancy reaches 4, i.e. exactly when a crackdown would matter. It looks deliberate
(it pushes the AI toward radicalisation) but it is the only hard 0 in the file.

## Performance

`audit_perf` still ranks 880010-880072 in the top 40 daily-trigger costs (~2,700 each
for 880040 and 880060). They were already reordered in the pass recorded in
docs/audit/performance.md (13,346 -> 1,241 each) and every clause after the cheap
prefix is the `owner = { ... any_owned_province }` stronghold-uniqueness test, which
cannot be made cheaper without changing firing rates. The `is_core = THIS` added to
880050 is a cheap clause sitting in the cheap prefix, so it lowers rather than raises
that event's cost. The two province events in `Socialism_Fascism.txt` (17500, 17730)
are gated on `is_ideology_enabled` first and are not hotspots.
