# `events/Taiping.txt` — line-by-line logic review

*2026-09-06. 1643 lines, 16 events (160001-160026). Mechanical audits (`modcheck braces/provinces/tags`,
`refcheck`, `audit_events`, `audit_owner_scope`, cwtools) were already clean on this file; everything below
is logic the tooling cannot see. Line numbers are post-fix.*

## Chain shape

`160011` (female shortage, 1840+) -> `160015` hong -> `160016` yang (1845+) are the three gates on `160001`,
the rebellion itself; `160009` arms the whole chain by setting `heavenly_kingdom` and zeroing the
`taiping_provinces` variable, which `160020` increments state by state. Outcome branches are `160002`
(TPG dead) / `160008` (QNG dead), with `160003`/`160004` truces feeding `160006`/`160007` "resume the war".
`160025` is the post-victory succession, `160026` an unrelated retreat-to-Formosa event that happens to live
in this file. **No event in the file fires another event**, so there are no FROM hops and no wrong-recipient
`country_event = { id = ... }` targets to get wrong. All `any_owned`/`random_owned` blocks run in the scope
that actually owns the land (`audit_owner_scope` reports nothing here).

## Findings

- **125, 186 — 160001 had no `ai_chance` on either option — FIXED.** The two options are byte-identical for
  ~60 lines; the only difference is that option B appends `change_tag_no_core_switch = TPG`. With no
  `ai_chance` the engine weights them equally, so an AI Qing had a ~50% chance of *becoming* the Taiping the
  moment the rebellion fired, deleting QNG from the game and orphaning every `tag = QNG` trigger in
  `CHIFlavor.txt`, `decisions/China.txt` and `common/rebel_types.txt`. Added `factor = 100` to "Crush them!"
  and `factor = 0` to "Out with the Manchu!" (the player-only tag-switch). **[high]**
- **1360 — 160025 option 2 "The Qing Dynasty must rule once more" — FIXED.** When QNG no longer exists the
  option does `change_tag = QNG` and then `add_accepted_culture = manchu`. `change_tag` adopts the new tag's
  primary culture, and `history/countries/QNG - Qing.txt:2` is `primary_culture = manchu`, so the line was a
  no-op and the entire nanfaren population — the country's own people one line earlier — was left an
  unaccepted minority on top of the `any_pop = { militancy = 6 }` the option already applies. Changed to
  `add_accepted_culture = nanfaren`. **[medium]**
- **764 — 160012 option A "silence these missionaries" applied `militancy = 10` — FIXED to 4.** 10 is the
  engine maximum, applied to every non-primary-culture pop in the province (for manchu-primary QNG that is
  effectively the whole province) *and* stacked with `reduce_pop = 0.98`. It guaranteed immediate rebellion
  and made the choice between the two options meaningless. **[medium]**
- **1080 — 160017 (single-option, repeatable, MTTH 200 months) applied `militancy = 10` — FIXED to 4.** Same
  magnitude problem, and worse here because the only gate on re-firing is `NOT = { average_militancy = 6 }`:
  a +10 hit blew straight past the gate, so the event could only ever fire once per province instead of
  escalating as designed. **[medium]**
- **385, 474 — dead `random_country` branch in 160006/160007.** `limit = { tag = TPG is_sphere_leader_of = QNG }`
  (and the mirror `tag = QNG is_sphere_leader_of = TPG`) can never match: only great powers hold spheres and
  both tags are uncivilised for the whole chain. Not fixed — the intended target is ambiguous (probably
  "whoever spheres my enemy"). **[medium]**
- **378, 467 — the sibling block above it is near-dead too.** `limit = { is_sphere_leader_of = TPG
  is_sphere_leader_of = QNG }` is an AND: it needs one country spheering *both* sides of the civil war.
  Harmless, but it is almost certainly a mis-written `OR`. Not fixed for the same reason. **[low]**
- **35 — unreachable first MTTH step in 160001.** `factor = 20 / NOT = { year = 1845 }` cannot be reached:
  160001 requires `has_global_flag = yang`, and 160016 (which sets it) has a hard `year = 1845` trigger, so
  the rebellion cannot fire before 1845 under any circumstances. Dead but harmless. **[low]**
- **36-56 — the 1850-1855 step added earlier tonight is consistent.** The ladder is
  `<1845: x20 | 1845-1850: x10 | 1850-1855: x0.5 | 1855-1860: x0.5 | 1860+: x0.1`, each window gated by
  `year = A` + `NOT = { year = B }`, contiguous with no gap and no double-count, and the new step matches the
  shape of its neighbours. Two observations, neither a defect: the 1850-1855 and 1855-1860 steps are the same
  0.5, so nothing accelerates across the historical peak of the rebellion; and the 1860+ step drops to 0.1
  (1.2 months), which makes a post-1860 start effectively instantaneous. **[low]**
- **893 — 160015 is localised off another event's keys.** `title = "EVTNAME164504"` / `desc = "EVTDESC164504"`
  on event id 160015. Both keys exist in `00_PDM_events.csv` so nothing displays raw, and `refcheck loc` is
  unaffected; left alone as deliberate PDM reuse. Same class at 654, where 160011's option uses
  `EVTOPTA16001` (present in `newtext.csv`) rather than `EVTOPTA160011`. **[low]**
- **1461 — 160026 "Retreat to Formosa" is mis-filed and over-broad.** It is a 20th-century Chinese-civil-war
  event (it clears `kuomintang_faction` / `beiyang_faction` / `communist_faction` flags) sitting in the
  Taiping file with no connection to the chain, and its trigger is only `is_culture_group = east_asian` +
  `NOT = { tag = KMT }`. A Japan or Korea reduced to exactly 1485 and 2562 would fire it and set TAI's
  primary culture to its own. The province-ownership requirement makes this a corner case, so not fixed.
  **[low]**
- **1639 — `money = 100000` to TAI in 160026.** Large but well inside the engine limit and defensible as
  "the treasury was evacuated to Taiwan". No change. **[low]**
- **78, 138 — lowercase `not = { province_id = 1616 }`.** The parser is case-insensitive, so this works, but
  it is the only lowercase operator in the file. **[low]**
- **1235 — `truce_with_taiping` is never cleared.** 160003 is `fire_only_once`, so the flag is set at most
  once and stays set for the rest of the game; 160006/160007 therefore stay armed forever and will offer
  "resume the war" in 1910 off a truce signed in 1852. Behaviourally mild (they need `war = no` and the other
  tag alive) and clearing the flag would change PDM pacing, so left as is. **[low]**
- **Multi-statement `NOT` blocks are all deliberate NORs.** 160011:660, 160012:697, 160013:810, 160017:1021,
  160020:1096 and the four `any_core = { NOT = { primary_culture = X tag = CHI } exists = no }` filters
  (280, 316, 594, 1284) all want "none of these", which is exactly what NOR gives. No change. **[low]**
- **No dead religion-form triggers.** The only religion tests are `has_pop_religion = sunni` (96, 159), which
  is live: `history/pops/1821.9.1/China.txt` has 235 sunni pop entries for the Hui. Nothing here needed
  converting, and nothing was converted.

## Magnitude sweep

All prestige changes are within ±20, no `badboy`, no `relation` beyond ±100, no `diplomatic_influence` beyond
±100, no treasury value near the 2,147,483 ceiling, and the largest `reduce_pop` is 0.90 (a 10% loss). Nothing
else in the file trips the implausible-magnitude thresholds.
