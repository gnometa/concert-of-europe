# The Age of Reform (ENG, 1828-1832)

Fills the gap listed in `docs/design/1821-1836-coverage.md` (ENG row: "Catholic Emancipation
1829 - missing"). `ENGFlavor.txt`'s 1821-1836 content is almost entirely Australian
colonisation (36980-36984, 36996), so there is no overlap. New file
`CoE_RoI_R/events/ENGReformGVG.txt`, ids 1000600-1000699, registered in
`events/GVG Event IDs.txt`.

Context from `history/countries/ENG - United Kingdom.txt`: `government = hms_government`,
`ruling_party = ENG_conservative` (the only 1820s alternative is `ENG_liberal`, liberal,
1820-1859), prestige 250, upper house 83 conservative / 12 liberal / 5 reactionary,
`minorities_reform = limited`, `vote_franschise = wealth_weighted_voting`. The 1836 history
block moves the country to `wealth_voting`, which is exactly the next step in
`common/issues.txt` (`vote_franschise` is `next_step_only = yes`), so the Reform Act sets
that value and the chain lands on the historical 1836 state. Catholic Emancipation moves
`minorities_reform` `limited -> protected` (also `next_step_only`); the mod has no religious
*reform* group, only the `religious_policy` party issue, which events cannot set.

Irish provinces are `region = ENG_254 / ENG_258 / ENG_260 / ENG_263` (Ulster, Connacht,
Munster, Leinster; provinces 254-265). English/Welsh cores are `ENG_273 / ENG_277 / ENG_280 /
ENG_284 / ENG_291 / ENG_296 / ENG_300`. Both are scoped with the mod's usual
`any_owned = { limit = { OR = { region = ... } } }` idiom (as in `BELRevolutionGVG.txt`).

## Events

### 1000600 - The Catholic Question (1828-1830)
`fire_only_once`, trigger `tag = ENG`, `year = 1828`, `NOT = { year = 1831 }`, MTTH 4 months.
Flavour: O'Connell wins the Clare by-election and cannot take his seat; Peel and Wellington
face the Catholic Association. Picture `religious_question`.
- **A - Grant emancipation** (historical, `ai_chance = 75`): `minorities_reform = protected`,
  prestige +5, Irish pops militancy -3 / consciousness +1, `upper_house` reactionary +0.05
  (the Ultra-Tory backlash), `set_country_flag = catholic_emancipation`.
- **B - The Protestant constitution stands** (`ai_chance = 25`): Irish pops militancy +3 /
  consciousness +2, `add_province_modifier = { name = nationalist_agitation duration = 1825 }`
  on Irish provinces, `set_country_flag = eng_emancipation_refused`, prestige -5.

### 1000601 - The Reform Crisis (1830-1833), `major = yes`, `news = yes`
Trigger `tag = ENG`, `fire_only_once`, `NOT = { year = 1834 }`, and
`OR = { AND = { year = 1830 FRA = { has_country_flag = july_revolution } } year = 1831 }` -
i.e. the Paris July Revolution pulls the crisis forward, otherwise it starts in 1831.
MTTH 3 months. Grey's Whig ministry, Birmingham Political Union, rotten boroughs. Picture
`deliberation`. News gives the other GPs the "Reform Crisis in Britain" headline.
- **A - Pass the Reform Bill** (historical, `ai_chance = 80`): `vote_franschise = wealth_voting`,
  prestige +10, `any_pop = { militancy = -2 consciousness = -1 }`, `upper_house` liberal +0.10,
  `add_country_modifier = { name = great_reformer duration = 1825 }`,
  `set_country_flag = great_reform_act`.
- **B - The Lords throw out the Bill** (`ai_chance = 20`): English/Welsh pops militancy +3 /
  consciousness +2, `add_country_modifier = { name = growing_unrest duration = 730 }`,
  `set_country_flag = eng_days_of_may`, then `country_event = { id = 1000602 days = 180 }`.

### 1000602 - The Days of May (`is_triggered_only`)
Picture `streetriot`. "Go for gold, stop the Duke."
- **A - The King will create the peers** (`ai_chance = 85`): as 1000601 option A but prestige
  -5 instead of +10 and no `great_reformer`; sets `great_reform_act`.
- **B - Hold firm** (`ai_chance = 15`): prestige -10, all pops militancy +3 / consciousness +1,
  `add_country_modifier = { name = global_liberal_agitation duration = 1095 }`,
  `set_country_flag = eng_reform_refused`.

## Reuse

No new modifiers and no new pictures: `nationalist_agitation`, `growing_unrest`,
`great_reformer` and `global_liberal_agitation` are all in `common/event_modifiers.txt`, and
`religious_question` / `deliberation` / `streetriot` are already in `gfx/pictures/events/`, so
`gfxtool.py missing` stays silent. Only localisation is new (`localisation/GVG_events.csv`).
Flags `catholic_emancipation` and `great_reform_act` are free for later ENG content to test.
