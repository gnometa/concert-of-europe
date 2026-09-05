# The Java War (1825-1830) — design

## Problem

`docs/design/1821-1836-coverage.md` lists the Java War and the Cultuurstelsel as
**missing** for NET; the only Indies revolt scripted is Palembang
(`events/DIM/DIM_East_Sumatra.txt:211202-211203`). Grepping the whole tree for
`diponegoro` / `cultuurstelsel` / `java war` returns nothing but one picture
reference (`DIM_cultuurstelsel_banner` reused by a Persian tea event,
`events/DIM/PERFlavour_five_x.txt:190324`). So the DIM submod ships the *art* for
this chain but never wrote it.

At the 1821 start NET owns all of Java outright — there is no Yogyakarta vassal
or substate. Provinces (verified against `map/definition.csv` and
`history/provinces/indonesia/`): 1413 Batavia, 1414 Bogor, 1415 Cirebon,
1416 Yogyakarta, 1417 Semarang, 1418 Surabaya, 1419 Surakarta, 1420 Probolinggo,
1421 Madura — all `owner = NET`, `add_core = JAV`, `add_core = INO`.
Do **not** use `region = NET_1413`: that region entry in `map/region.txt` also
contains 1716/1717/1724, which are Saharan provinces (Tindouf, Chenachene,
Tamanrasset). The chain enumerates province ids explicitly instead.

`JAV` is a real registered tag (`common/countries.txt:425`, capital 1413,
primary culture javan) and NET owns its capital, so `release_vassal = JAV` would
be legal. It is deliberately **not** used: it would hand the whole of Java —
NET's entire colonial economy — to a vassal over a provincial revolt, which is
neither historical nor a modest magnitude. The conciliatory branch buys the
Javanese aristocracy off instead.

## Chain — `events/JavaWarGVG.txt`, ids 1001300-1001302

| id | who | when | options |
|---|---|---|---|
| 1001300 | NET | year >= 1825, owns 1416, not yet 1831, MTTH 3mo, once, news | A fight (AI 80) / B negotiate (AI 15) / C overstretched (AI 5, weighted up by `war = yes` or `BEL_war_of_secession`) |
| 1001301 | NET | triggered 1825 days after A or C — "Diponegoro captured at Magelang", news | A Cultivation System (AI 75) / B lighter hand (AI 25) |
| 1001302 | NET | triggered from 1300 B — the Javanese settlement closes the chain | single option |

Option A of 1001300: `set_country_flag = java_war_in_progress`,
`treasury = -20000`, `war_exhaustion = 3`, `prestige = -3`, and a five-year
(`duration = 1825`) `java_war` province modifier plus pop militancy on the nine
Java provinces. Option C is the same but cheaper, longer and angrier — Vic2
options cannot carry triggers, so "overstretch" is expressed through
`ai_chance` modifiers rather than a conditional option.

Option A of 1001301 sets `cultuurstelsel` (flag + 20-year country modifier),
clears the province modifiers, `prestige = 10`, `war_exhaustion = -5`, and
raises Java militancy slightly. Option B clears them and calms the pops.

## New modifiers — `common/event_modifiers.txt` (GVG section, at end of file)

- `java_war` (province): `local_RGO_output -0.10`, `farm_RGO_size -0.10`,
  `local_ruling_party_support -0.05`, `population_growth -0.001`, icon 15.
- `cultuurstelsel` (country): `tax_efficiency 0.05`, `farm_RGO_size 0.10`,
  `global_pop_militancy_modifier 0.01`, icon 7.

## Localisation

`localisation/GVG_events.csv` (append only, `modcheck loc-add`): `EVTNAME/EVTDESC/EVTOPTx`
for the three ids, the three news keys for 1001300 and 1001301, and the two
modifier names.

## Pictures

Existing DIM art only, no new files: `DIM_java_manuscript` (1001300),
`DIM_indies_nobles` (1001302), `DIM_cultuurstelsel_banner` (1001301).

## Risks

Province ids are the historical crash source in this repo; all nine are checked
above and re-checked by `modcheck provinces`. The chain can overlap the Belgian
crisis - deliberately, which is what option C is for.
