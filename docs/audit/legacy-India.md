# Legacy audit: `events/India.txt` and `events/Sepoy rebellion.txt`

*2026-09-06. Line-by-line logic review of the Indian rebellion / nationalism chain. Line
numbers are the **post-fix** tree unless the row says "not fixed". The mechanical audits
(`modcheck`, `refcheck`, `audit_events`, `audit_owner_scope`, cwtools) were at baseline
before and after, so everything below is logic those tools cannot see.*

Cast: **ENG owns no province in India.** The vassal **HND** (primary culture `british`)
owns Delhi 1236, Calcutta 1251, Madras 1304, Bombay 1297, Patna 1247; **PNJ** owns Lahore
1227; princely states are separate tags.

## Fixed

| file:line | id | problem | fix |
|---|---|---|---|
| Sepoy rebellion.txt:196 | 99899 | **[high]** `fire_only_once` is engine-wide, but 99900 fires 99899 through `any_country = { limit = { ... vassal_of = ENG } }`. Only whichever princely state the engine reaches first ever sees "Mughals call for Help!"; every other Indian vassal is silently skipped, so the join-or-defect choice the whole chain is built around happens exactly once per game. | dropped `fire_only_once` |
| Sepoy rebellion.txt:427 | 99895 | **[high]** same defect: 99896 fans 99895 out over `any_country = { limit = { has_country_flag = is_part_of_raj } }`, so only one defector is ever re-vassalised. | dropped `fire_only_once` |
| Sepoy rebellion.txt:31 | 99902 | **[high]** option text "Situation escalates into full-blown rebellion!" ran `country_event = 90040`, but 90040 carries its own `year = 1857` gate while 99902 is Barrackpore, gated on `ENG = { war_with = BUR }` (first Anglo-Burmese war, 1824-26 from an 1821 start). The option was a no-op for thirty years, and the chain behind it (99901/99900/99899/99898/99897/99896/99895) was unreachable from here. | option now delivers its own escalation (non-primary-culture soldiers +5 consciousness/militancy, one `nationalist_agitation` province) and is renamed "The mutiny spreads through the ranks." 90040 keeps its historical 1857 window |
| India.txt:290, 366 | 97110, 97111 | **[high]** both options ran `clr_country_flag = sepoy_rebellion`. If the nationalism chain fires while the Sepoy rebellion is live the flag disappears; 90039 ("End of the Sepoy Rebellion") requires `has_country_flag = sepoy_rebellion`, so the rebellion can then never end, its `nationalist_agitation` is never cleaned up, and 90040 - which only checks `NOT = { has_country_flag = sepoy_rebellion }` - becomes eligible to fire a second time. | removed both `clr_country_flag` lines |
| India.txt:429 | 97115 | **[high]** `HND = { vassal_of ENG }` - missing `=`. A malformed statement inside the `AND`; at best the clause is ignored, at worst it wrecks the parse of the rest of the trigger. | `vassal_of = ENG` |
| India.txt:697 | 97125 | **[high]** trigger `tag = HND` + `primary_culture = british` + `is_vassal = no`, `months = 1`, no `fire_only_once`; effect `ENG = { inherit = HND }`. With ENG gone `inherit` is a no-op, the trigger stays true, and the event re-fires every month forever. | added `ENG = { exists = yes }` |
| India.txt:16 | 97100 | **[medium]** `controlled_by = THIS` in a `province_event`: THIS is the event root, i.e. the province itself, so the clause is a tautology. The intent (skip land already lost to the rebels) was never enforced and 97100 kept stacking agitation on rebel-held provinces. | `NOT = { controlled_by = REB }` |
| India.txt:378 | 97111 | **[medium]** 97111 is the FROM-side copy of 97110's `random_list` but omits 97110's empty `25 = { }` branch. Weights are relative, so the recipient (HND) got agitation 100% of the time where the originator gets it 75% - the copy is harsher than the original it mirrors. | added the missing `25 = { }` branch |
| India.txt:481 | 97116 | **[medium]** three `random_owned` CB branches, of which the second and third are byte-identical (`establish_protectorate_casus_belli`, 60 months) and differ only on `has_global_flag = berlin_conference`. Dead duplication - the flag changes nothing. | merged into one `nationalism_n_imperialism = 1` branch |
| Sepoy rebellion.txt:110 | 99901 | **[medium]** the Mughal restoration proclaimed at Delhi took `primary_culture = panjabi` while merely accepting `avadhi`. Delhi/Awadh is Avadhi ground, and Panjab is the one region the 1857 mutiny did *not* hold (PNJ/Lahore is a separate tag). | `primary_culture = avadhi`, panjabi moved into the accepted list, with the matching swap in 99896's `remove_accepted_culture` list so the reconquest still undoes exactly what 99901 granted |
| Sepoy rebellion.txt:378 | 99897 | **[medium]** `years_of_research = 5` for surviving the war of independence - a world-war-victory reward on this mod's scale, handed to a country the same file describes as barely civilised. | `years_of_research = 1` (prestige 100 left alone; it is a one-off national founding) |

## Reported, not fixed

| file:line | id | problem | suggested fix |
|---|---|---|---|
| Sepoy rebellion.txt:52, 300 | 90040, 90039 | **[medium]** owner-scope (cf. `docs/audit/owner-scope.md`). Both triggers read `OR = { tag = ENG tag = ENL primary_culture = british }` then `owns = 1236 / 1251 / 1304 / 1297 / 1247 / 1227`, but ENG owns none of those - HND does, and 1227 is PNJ's. The `tag = ENG` and `tag = ENL` arms are dead; only the `primary_culture = british` arm (HND itself) can pass. 90039's payload `any_owned = { limit = { is_core = HND } ... }` would be dead for the same reason if ENG ever did reach it. | design call: either test ownership through `HND = { owns = ... }` for the ENG arms, or drop them and make the pair explicitly HND-only - applied to both events together |
| Sepoy rebellion.txt:15 | 99902 | **[medium]** no upper year bound. `ENG = { war_with = BUR }` also matches the 1852 and 1885 Anglo-Burmese wars in `Indochina.txt`, so a game that avoids the 1824 war still gets "Barrackpore" in 1885. | `NOT = { year = 1840 }` |
| Sepoy rebellion.txt:29, 136 | 99902, 99901 | **[medium]** stacked `ai_chance`: 5% to escalate at Barrackpore, then 10% for the Mughal branch. Even with the 99902 link repaired the seven-event Mughal chain is reachable in well under 1% of AI games. Rebalance as a set once the 90040 owner-scope question is settled. | rebalance |
| Sepoy rebellion.txt:127-134 | 99901 | **[low]** the liberation option installs `prussian_constitutionalism` plus `censored_press`, `gerrymandering`, `no_draft` and `social_reform = serfdom`. A national-liberation option that ends in serfdom contradicts its own text. | soften the reform package |
| India.txt:588 | 97122 | **[low]** the "Never!" option applies `militancy = 8` to every south-Asian pop on HND cores plus `war_exhaustion = 30`. Militancy caps at 10, so this is an instant nationwide revolt rather than the "stubbornness has a price" the option describes. | 4-5 |
| both files | 99902, 99901, 99900, 99899, 99898, 99897, 99896, 99895, 97124 | **[low]** titles and descriptions are literal English strings rather than `EVTNAME<id>`/`EVTDESC<id>` keys (99902 mixes a literal title with a keyed desc). The engine prints them, so nothing breaks, but they are unlocalisable and inconsistent with the rest of the file. | move to keys |
| Sepoy rebellion.txt | 99901, 99900, 99899, 99898, 99895 | **[low]** `mean_time_to_happen = { months = 1 }` on `is_triggered_only` events - ignored by the engine, pure noise. | delete |
| India.txt:110, 289, 351 | 97100, 97110, 97111 | **[low]** the seventeen-culture `OR` list is repeated verbatim three times here and once more in 99901's accepted-culture list. Any new south-Asian culture must be added in four places. | a `south_asian` culture-group test plus a short exclusion list |
| India.txt:127 | 97105 | **[low]** duplicated episode: 97100 (province) and 97105 (country) key off the same `sepoy_rebellion` / `indian_call_to_union` conditions and both apply `nationalist_agitation`, so a vassal can eat both. Deliberate double coverage or an oversight - needs a design decision. | |

## Checked, no defect found

- Windows: Sepoy 1857 (90040/90039), Barrackpore 1824 (99902) and Ranjit Singh's death
  (97115 - gated on `has_leader`, not a year) all sit inside the 1821-1936 game. No other
  1836-start `year =` assumption in either file.
- The Anglo-Sikh wars are not scripted here; 97115/97116 instead hand ENG a CB against PNJ,
  reachable from 1821 and not colliding with the Anglo-Burmese content in `Indochina.txt`.
- Province ids 1227, 1236, 1247, 1251, 1297, 1304 all exist in `map/definition.csv`.
- Tags ENG, ENL, HND, PNJ, DRA, HDU, MRT, BUR, REB are registered in `common/countries.txt`;
  every CB type, government and event modifier referenced exists.
- FROM hops verified: 97110 -> 97111, 97122 -> 97123 / 97124 / 800148 (`Revolution_Event.txt`),
  99900 -> 99899 / 99898, 99896 -> 99895. `THIS` inside the nested `FROM` / `ENG` / `HND`
  scopes resolves to the event root in every case, which is what each effect wants - notably
  `HND = { inherit = THIS }` in 99899 and `ENG = { create_vassal = THIS }` in 99895.
- No pop-level `religion = hindu/sunni` tests in either file. 99901's `religion = sunni` and
  99896's `religion = protestant` are country-scope state-religion effects and are correct.
- Event 99902 is live and recorded as such in `events/GVG Event IDs.txt`.
