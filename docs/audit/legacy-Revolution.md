# Legacy audit — generic revolution machinery

*2026-09-06. Line-by-line logic review of `events/Revolution_Event.txt`,
`Revolution_Nationalism_Event.txt`, `Revolution_Relations_Event.txt`,
`Revolution_Spread_Event.txt`. Line numbers are post-fix. Known-and-kept orphans
(97700, 800147, 800149, 810055-57) are reviewed but not repaired.*

Fixed in this pass: F1-F7. Everything else is reported only.

## [high]

- **F1** `Revolution_Event.txt:848-861` **800054** — `remove_country_modifier =
  springtime_of_nations` / `global_liberal_agitation` ran *before* the
  `random_owned` block whose limit tests `has_country_modifier =
  springtime_of_nations`. The FRA `2nd_republic` flag could therefore never be
  set: a dead branch on every Jacobin revolution in France.
  **Fixed** — the FRA block now runs before the two removals.
- **F2** `Revolution_Event.txt:2244` **800055 option 1 ("Let them go")** — options
  2 and 3 clear `former_overlord`, option 1 did not. The flag is per-country but
  never expires, so an overlord that once let a vassal go was permanently
  excluded from the `NOT = { has_country_flag = former_overlord }` guards in
  800050-800054, 810055-57 and 800149 — i.e. it silently stopped reacting
  diplomatically to *every* later revolution in the game.
  **Fixed** — `clr_country_flag = former_overlord` added to option 1.
- **F3** `Revolution_Relations_Event.txt:909, 1170, 1248, 1390` **800075 /
  800081 / 800082 / 800083** — the summit triggers exclude the caller with
  `NOT = { tag = THIS }` inside `any_greater_power`, but the matching
  `random_country` in the option did not. `random_country` iterates the caller
  too, so the summit invitation (800076) could be sent to oneself, ending in
  `create_alliance = FROM` and `relation = { who = FROM }` with itself.
  **Fixed** — `tag = THIS` added to each option's `NOT` block (also added
  defensively to 800074:816, which was already covered by `neighbour = THIS`).

## [medium]

- **F4** `Revolution_Event.txt:2833` **97565** — the notification used
  `limit = { is_our_vassal = THIS is_sphere_leader_of = THIS }`, an AND, while
  the trigger admits `part_of_sphere = yes` **OR** `is_vassal = yes`. A vassal
  whose overlord is not also its sphere leader found no recipient, yet 97565
  still set `called_for_help`, which 97567 only clears once the danger passes —
  the call for help was lost for good. **Fixed** — wrapped in `OR`.
- **F5** `Revolution_Nationalism_Event.txt:21` **800100** — trigger gated on
  `money = 25000` but the option spends `treasury = -50000`, so the AI/player
  could be pushed to half the cost into deficit. **Fixed** — gate raised to
  `money = 50000` (the cost, not the gate, is the designed magnitude: the mtth
  modifiers all scale the *decision*, not affordability).
- **F6** `Revolution_Relations_Event.txt:1466, 1630, 1795, 1971, 2582, 2666,
  2750, 2843` — eight mtth blocks carried `war_policy = pro_military` twice
  (`factor = 0.9` and `factor = 2`) and no `pacifism` entry, breaking the
  jingoism 0.75 / pro_military 0.9 / anti_military 1.5 / pacifism 2 ladder used
  everywhere else in the file. Pacifist states got no slowdown and militarists
  a spurious 1.8x. **Fixed** — the `factor = 2` copy is now `pacifism`.
- **F7** `Revolution_Relations_Event.txt:2699` **800095** — the option's
  `random_country` required `relation = { who = THIS value = -50 }` while the
  trigger (and the identical 800094/800096/800097) use `-150`. Neighbours
  between -150 and -50 satisfied the trigger but matched no recipient, so the
  incident fired with no effect at all. **Fixed** — aligned to `-150`.
- ~~`Revolution_Event.txt:162, 414, 610, 1154` (800051/800052/800053/810056) —
  `owner = { ruling_party_ideology = <x> }` is a silent no-op.~~ **Retracted by
  integration review 6.** `ruling_party_ideology` is *both* a trigger and a
  country-scope effect - `docs/wiki/list-of-effects.md:206`: "Changes the current
  ideology of the country's ruling party. If there is more than one party for
  that ideology, the first party listed in the country file is chosen." The four
  "fall back to the moderate party" branches work as written, as do the other 25
  uses mod-wide. Nothing to fix.
- `Revolution_Event.txt:1875` **97700** and `:1977` **800151** are the same
  episode ("$COUNTRY_ADJ$ Patriots") with the same effects, one triggered-only
  and one self-firing. 97700 is the known dead copy; if it is ever revived they
  will double-fire. Keep exactly one.
- `Revolution_Nationalism_Event.txt:384, 403, 624, 658` (97175, 97181) —
  `country_units_in_province = THIS` inside a `province_event`, where `THIS` is
  the province, not a country. The clause is at best a no-op; it is meant to be
  the province owner. Same shape at `:670` (`owned_by = THIS`). Left alone
  because 97175 is the performance hotspot in `performance.md` and any change
  here changes its firing rate.

## [low]

- `Revolution_Event.txt:2245` **800055 option 1** — `badboy = -1` for letting a
  vassal go is a free infamy sink with no cooldown; the vassal-release loop can
  be farmed.
- `Revolution_Event.txt:372, 567` (800051/800052) — `any_country = {
  change_variable = { which = successful_fascist_rebellions value = 1 } }` with
  no `limit`, so the counter is written to every country including the
  revolutionary itself. It reads as a global counter and 800063/800083 use it as
  one, so it works, but it is per-country storage doing a global job.
- `Revolution_Event.txt:1631` **800147** — `set_global_flag =
  british_dismantled` is never read anywhere (`refcheck` flags it); and the
  `any_country` block below it hands a `make_puppet` CB to a country with
  `exists = no`. Both dead; 800147 is itself a known orphan.
- `Revolution_Event.txt:2899` **97570** — `NOT = { average_militancy = 6
  is_primary_culture = yes has_province_modifier = peasant_revolt }` uses
  `is_primary_culture` in province scope, which is a pop trigger. Suspect, but
  the NOR still short-circuits correctly on the other two clauses.
- `Revolution_Relations_Event.txt:1051/1077` **800077/800078** — only the summit
  *caller* is paid (`prestige = 20` / `5`); the country that accepted gets
  nothing. Asymmetric reward for a mutual act.
- `Revolution_Spread_Event.txt:127, 262, 409, 606` — "It's too risky." costs
  `prestige = -5` on all four spread events. Declining to run a covert
  propaganda campaign nobody knows about should not be publicly humiliating.
- `Revolution_Relations_Event.txt:860+` — the paired 95/5 `ai_chance` on
  800066-800074 and the summit callers means the AI effectively always opens the
  approach. Deliberate (the *recipient* is where the real roll happens, 75/25 in
  800067 and 50/30/20 in 800076), so it is left as is.
- Relation deltas of `-200` (800050-800054, 800055 option 3, 800056 option 2,
  800148) sit exactly on the engine clamp; they are one-shot reputational
  breaks, not compounding, so the magnitude is defensible — but note that
  800050-54 stack a `-200` influence *and* a `-50` relation *and*
  `leave_alliance` on the ex-overlord in a single option.
- Militancy in 800050-800054/810056 is applied through `scaled_militancy` with
  matched positive/negative pairs per ideology and no accumulating modifier, so
  there is no undecayed compounding here.
