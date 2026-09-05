# Decembrist Revolt mini-chain (RUS, December 1825)

Fills the gap found by `docs/audit/events-H-Z.md` ("1821-1836 coverage"): `RUSFlavor.txt`
starts in 1827, so Alexander I's death, the Constantine/Nicholas interregnum and the
Decembrist rising are unscripted. New file `CoE_RoI_R/events/RUSDecembristGVG.txt`,
ids 1000400-1000499 (registered in `events/GVG Event IDs.txt`).

Context assumed by the existing 1827+ Russian events: tag RUS, `government = absolute_monarchy3`,
ruling party `RUS_conservative`, upper house 60 conservative / 21 reactionary / 19 liberal,
prestige 200. The chain never changes the ruling party (only `RUS_liberal` exists as an
alternative and Nicholas historically kept the conservatives); it moves the upper house and
pop ideology instead, which is what the later flavour events also do.

## Events

### 1000400 - Death of Alexander I: The Interregnum (fires late 1825)
`fire_only_once`, trigger `tag = RUS`, `year = 1825`, `month = 10`, `NOT = { year = 1826 }`,
MTTH 1 month. Flavour: Taganrog, Constantine's secret renunciation, three weeks of two
emperors. Single option: prestige -5, `any_pop = { consciousness = 1 }`, sets
`has_country_flag = rus_interregnum` and fires 1000401 after 20 days.

### 1000401 - The Decembrists on Senate Square (`is_triggered_only`, `major = yes`, `news = yes`)
The newspaper article ("Revolt in St Petersburg") is produced by `news = yes` +
`news_desc_long/medium/short`, the same idiom as `RUSFlavor.txt` id 32500 - no separate GP event.
Options:
1. **Grapeshot** (historical, `ai_chance = 80`): prestige +10; `capital_scope` pops militancy
   spike then `any_pop = { militancy = -2 ideology = { value = reactionary factor = 0.1 } }`;
   `add_country_modifier = { name = nicholas_reaction duration = 3650 }` (the one new modifier,
   below) and `{ name = purge duration = 730 }` for the officer purge / leadership malus
   (`purge` already exists: `leadership_modifier = -0.75`). Sets `nicholas_reaction` flag ->
   1000402.
2. **Negotiate with the officers** (alt-history, `ai_chance = 10`): `any_pop = { consciousness = 2 }`,
   `upper_house = { ideology = liberal value = 0.15 }` (effect verified in
   `docs/wiki/list-of-effects.md`), `add_country_modifier = { name = liberal_agitation duration = 1825 }`,
   prestige -5. Sets `rus_decembrist_compromise` -> 1000403.
3. **Let Constantine take the throne** (alt, `ai_chance = 10`): prestige -15, militancy -1,
   `CPL`/`POL` relations +50 if the tag exists (both are registered in `common/countries.txt`),
   `any_pop = { ideology = { value = conservative factor = 0.1 } }`, flag `rus_constantine_tsar`.

### 1000402 - The Third Section (1826, if crushed)
Trigger: flag `nicholas_reaction`, `year = 1826`, MTTH 4 months, `fire_only_once`.
Option A: found the gendarmerie - `add_country_modifier = { name = secret_police duration = 3650 }`
(existing modifier). Option B: leave it to the ministries - prestige +5, no modifier,
`any_pop = { consciousness = 1 }`.

### 1000403 - Pestel's Russkaya Pravda (1826, if negotiated)
Trigger: flag `rus_decembrist_compromise`, `year = 1826`, MTTH 4 months, `fire_only_once`.
Option A: let the pamphlet circulate - consciousness +1, `upper_house` liberal +0.1,
`liberal_agitation` 5 years. Option B: quietly confiscate it - militancy +1 among liberals'
pops, prestige +5, `secret_police` 5 years.

## New modifier (1 only)

`nicholas_reaction` in `common/event_modifiers.txt`:
`issue_change_speed = -0.5`, `global_pop_consciousness_modifier = -0.02`,
`global_pop_militancy_modifier = -0.02`, `suppression_points_modifier = 0.25`,
`prestige = 0.02`, `icon = 15`. Localisation key `nicholas_reaction` in `GVG_events.csv`.
Everything else reuses `purge`, `secret_police`, `liberal_agitation`.

## Pictures

`emperor_funeral` (1000400), `streetriot` (1000401), `Police` (vanilla, 1000402),
`senate_debate` (1000403) - all already present, so `gfxtool.py missing` stays silent.
