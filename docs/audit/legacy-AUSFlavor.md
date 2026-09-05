# Logic review — `CoE_RoI_R/events/AUSFlavor.txt`

*2026-09-06. Line-by-line read of all 24 events (31501-31508, 31525, 31550-31552, 90016-90023,
90041, 98007, 98008, 22240). Mechanical audits (`modcheck`, `refcheck`, `audit_events`, cwtools)
were already clean on this file, so everything below is logic, not syntax.*

Checked and **not** a defect (recorded so nobody "fixes" them again):

- Multi-statement `NOT = { a b c }` guards (31503, 31504, 31508, 31525, 90017-90022, 98007) are
  NOR — true only when every member is false — which is exactly the intended "none of this has
  happened yet" gate. See `docs/wiki/list-of-conditions.md` ~line 86.
- `has_pop_religion = north_italian` (31507, 90018) and `religion = south_german` (22240) look like
  culture/religion confusion but are correct **in this mod**: `common/religion.txt` defines the
  culture list a second time as religions and `history/pops/1821.9.1/` really does assign
  `religion = north_italian`.
- `THIS` inside a nested scope (90017 `HUN = { ... secede_province = THIS }`, 90041
  `random_country = { ... target = THIS }`, 22240 `FROM = { ... secede_province = THIS }`) resolves
  to the event's root country, not the inner scope — same idiom as `SER = { neighbour = THIS }` in
  90016. All three read correctly.
- `add_casus_belli` in 90041 gives the *target* the CB, so the human-KRA branch (AUS gets a
  conquest CB) and the AI-KRA branch (AUS declares) are consistent, not inverted.
- 22240's population exchange is deliberate: Bielsko (2584) loses its AUS core and receives the
  Polish pops, Tesin (689) loses its POL/PLC cores and receives KRA's German pops. All eleven
  province ids referenced in the file (631, 682, 684, 689, 699, 702, 706, 714, 729, 771, 2584)
  exist in `map/definition.csv`.
- 31507 borrowing `EVTNAME35400`/`EVTOPTA35400` is intentional and commented (LOM parallel, 35400
  in `LOMFlavor.txt`).

## Fixed in place

| line | id | problem | fix |
|---|---|---|---|
| 562 | 98007 | **[high]** Option A *"Give them what they want."* grants `political_reform = free_press` and then raises Hungarian `militancy = 4` plus a 365-day `nationalist_agitation` on every Hungarian province — conceding was strictly worse for order than Option B's refusal (`militancy = 6`), so the AI's 60/40 split rewarded the wrong branch and the option text contradicted its own effect. | `militancy = -4` (consciousness stays +2: the concession politicises without inflaming) and the `nationalist_agitation` block dropped from the conceding branch only. Option B untouched. |
| 300 | 31505 | **[medium]** Option name pointed at `EVTOPTA31502` ("Reaction!"), a different event's key; `EVTOPTA31505` ("Vivat!") exists and is unused. | `name = "EVTOPTA31505"` |
| 352 | 31506 | **[medium]** Same copy-paste: `EVTOPTA31502` instead of the existing `EVTOPTA31506` ("An artistic genius"). | `name = "EVTOPTA31506"` |
| 2230 | 90023 | **[medium]** The shared "granted autonomy" event fires *at the newly released nation*; its only option is `"Wonderful!"` yet applied `prestige = -100` to it. Effect contradicts the option and the event title. | `prestige = 10`. (90023 is also fired from `Ottoman_Event.txt`; the change is an improvement there too.) |

## Reported, not changed

| line | id | problem | suggested fix |
|---|---|---|---|
| 1547 | 90020 | **[medium]** Slovene independence needs `OR = { NOT = { owns = 771 } NOT = { owns = 729 } }`. 771 is Zagreb and 729 is Venice — neither is a Slovene province — and Austria owns both from 1821, so for the country the event is written for it is a **dead branch** until the empire is already dismembered. Either the ids are wrong (Ljubljana/Trieste intended) or the gate is a deliberate "only once Austria is collapsing"; both readings are defensible, so it needs a design call rather than an edit. | replace with the SLO-core provinces, or delete the `OR` and rely on `is_possible_vassal = SLO`. |
| 804, 1054 | 90017, 90018 | **[medium]** Unlike every other event in the file these have no `tag = AUS`/`tag = KUK` gate; they run for any country that satisfies `is_possible_vassal`. 90018 shows the author was aware (it carries `NOT = { tag = ITA ... }`), 90017 has no such guard at all. In practice only Austria holds the cores early, so it is latent rather than live. | add the `OR = { tag = AUS tag = KUK }` gate used by 31501-31525, or an explicit `NOT = { tag = HUN }`. |
| 1372, 1446 | 90019 | **[low]** Croatia is the only one of the six Austrian release events where *"Give them greater autonomy."* is weighted `factor = 70`, the same as the refusal — HUN/LOM/SLO/BOH/SLV all use 30. The Balkan trio (31550-31552) also uses 70, so this may be copy-paste from that group rather than a bug. | align 90019's autonomy option to 30 if the Austrian set is meant to be uniform. |
| 1058, 1291, 1527, 1763, 1992, 2365, 2601, 2837 | 90018-90022, 31550-31552 | **[low]** Eight release events (Lombardy, Croatia, Slovenia, Bohemia, Slovakia, Serbia, Montenegro, Macedonia) all use `picture = "Budapest"`, cloned from the Hungarian original. Visible mismatch, no mechanical effect. | give each a fitting picture, or a neutral one. |
| 441 | 31508 | **[low]** Titled with `EVTNAME32501`/`EVTDESC32501`/`EVTOPTA32501` although no event 32501 exists any more. The keys are present in localisation and the text fits, so it displays correctly; it just makes the loc hard to trace. | rename the keys to `*31508` in a loc pass. |
| 111 | 31503 | **[low]** "Hungarian as an official language" (1842+) does not know about tonight's Vormärz chain: `AUSVormaerzGVG` 1001801/1001803 already run the 1825 Diet and set `hungarian_diet_1825` / `hungarian_reform_era`. Historically the 1844 language law is a separate act, so this is duplication only if the two chains are meant to be exclusive. | if exclusivity is wanted, add `has_country_flag = hungarian_reform_era` to the existing NOR — it is a NOR, so a fourth member tightens the gate correctly. |
| 602 | 98008 | **[low]** The Czech coup is gated `year = 1849` with no upper bound, so a save that has kept Czech consciousness high can see the 1848-flavoured event fire in the 1890s. Its Hungarian counterpart 98007 is bounded by the revolution flag instead. | add `NOT = { year = 1852 }`, matching 31504. |
| 2221 | 90023 | **[low]** `military_industry = 50 / light_industry = 50 / horses = 20` treat two goods *groups* as goods. This idiom is mod-wide (`ACW.txt`, `+education_RGO.txt` use far larger values), so it is a baseline question, not an AUSFlavor one. | resolve once, globally. |
| 3073 | 22240 | **[low]** Marked `#unused`, but `decisions/KRA.txt:745` fires it (`country_event = 22240`). Stale comment; the stray `#Validator says FROM is not valid. Looks good to me. -Koro` note is also obsolete — the FROM usage is correct. | delete both comments. |
| 691 | 90016 | **[low]** `any_owned_province = { is_core = SER average_militancy = 4 }` uses a state-level condition in province scope, and Option A hands `militancy = -6` to every primary-culture pop for declaring war. Both work, but -6 is the largest single militancy swing in the file. | consider -3, in line with the rest of the file. |

## Interactions checked

- **AUSVormaerzGVG (1001800-1001803)** — no id, flag or modifier collision. `metternich_system`
  (1822-1837) and `aus_metternich_system` / `hungarian_diet_1825` / `hungarian_reform_era` are not
  read anywhere in AUSFlavor; the only overlap is the thematic one at 31503 noted above. The
  Vormärz events are gated `tag = AUS` while AUSFlavor accepts `AUS` or `KUK`, which is correct:
  KUK cannot exist before 1867.
- **ITARisingsGVG 1001103** — fired at AUS by 1001102 and sets `aus_intervened_1831`. AUSFlavor's
  Italian content is 31507 (1842 Nabucco, requires `NOT = { exists = LOM }`) and 90018; neither
  reads or clears that flag and neither can fire in 1831, so the chains do not interfere.
- **Window sanity from the 1821 start** — every year gate (1836, 1842, 1843, 1846, 1849, 1897,
  1911, 1914) is reachable and no `year`/`NOT = { year }` pair is inverted or empty.
