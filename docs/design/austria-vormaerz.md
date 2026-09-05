# Austrian Vormärz, 1821-1835 (AUSVormaerzGVG)

Ids 1001800-1001803, file `CoE_RoI_R/events/AUSVormaerzGVG.txt`.

## Historical outline

Austria is the arbiter of the Concert but its script content starts only in 1836.
Between the Congress of Verona (October 1822) and the death of Francis I (2 March
1835) Metternich's system rested on the Carlsbad Decrees, the Mainz Central
Investigation Commission and a censorship apparatus run out of the Staatskanzlei.
The one real crack was Hungary: after thirteen years without a Diet, Francis
summoned it to Pressburg in 1825, where Széchenyi endowed what became the
Hungarian Academy of Sciences and the reform era began. On Francis's death the
incapable Ferdinand I brought the Staatskonferenz, in which Metternich and the
finance minister Kolowrat blocked each other until 1848.

## Facts checked against the tree

- `events/AUSFlavor.txt` has **nothing before 1836** (earliest is 31501, the 1836
  smoking ban), so 1821-1835 is free; 31502/31503 are 1842+.
- The 1831 Austrian intervention in Italy is already covered by
  `events/ITARisingsGVG.txt:1001103`; this file stays out of Italy.
- Cholera 1831 is **not** added: `events/LiberalRevolutions.txt:4435` is a generic
  province cholera event with `cholera_epidemic_small/big` modifiers. Slot (c) is
  the death of Francis I instead.
- Culture is `hungarian`, not "magyar". Hungarian provinces are addressed as
  `any_owned = { limit = { is_core = HUN } }` rather than by id list.
- AUS owns 633 Bratislava (Pressburg), 641 Budapest, 648 Debrecen at start; all
  three carry `add_core = HUN`.
- Pictures are existing files only: `greatpowers`, `Budapest`, `ferdinand`.
- Two new event modifiers are appended to `common/event_modifiers.txt`
  (`metternich_system`, `kolowrat_administration`); 1001803 adds none.

## Chain

| id | Fires | Content |
|---|---|---|
| 1001800 | 1822-1825, MTTH 5 months | The Metternich System |
| 1001801 | 1825-1828, MTTH 6 months, needs 633 or 641 | The Hungarian Diet Reconvened |
| 1001802 | 1835.3+, MTTH 2 months | The Death of Francis I |
| 1001803 | 1830-1834, needs `hungarian_diet_1825` | Széchenyi and the Academy |

All four are `tag = AUS` only, so `fire_only_once = yes` is safe (it is
engine-wide, per CLAUDE.md).

**1001800** - Verona and the Carlsbad Decrees.
- A "Enforce the decrees" (ai 75): `metternich_system` for 15 years, global
  consciousness -1, middle-strata militancy +1, prestige +2, relations RUS/PRU
  +25, sets `aus_metternich_system`.
- B "Loosen the censor's hand" (ai 25): consciousness +1, upper house liberal
  +0.10, relations ENG +20 / FRA +15, prestige -2, sets `aus_vormaerz_relaxed`.

**1001801** - trigger `owns = 633` OR `owns = 641`.
- A "Summon the Diet at Pressburg" (ai 60): militancy -2 and consciousness +1 in
  HUN-core provinces, prestige +2, sets `hungarian_diet_1825` (read by 1001803,
  and available to later 1848 content).
- B "Govern by rescript" (ai 40): militancy +1 in HUN-core provinces,
  `conservative_reaction` for 5 years, sets `hungarian_diet_stalled`.

**1001802** - `year = 1835 month = 2`, `NOT = { year = 1837 }`.
- A "Metternich leads the Staatskonferenz" (ai 60): `metternich_system` for 10
  years, consciousness -1, militancy -1, prestige +2, no new flag. `ai_chance`
  is raised by `aus_metternich_system` and by `hungarian_diet_stalled`.
- B "Kolowrat takes the finances" (ai 40): `kolowrat_administration` for 10
  years, consciousness +1, prestige -1. `ai_chance` is raised by
  `aus_vormaerz_relaxed` and by `hungarian_reform_era`.

**1001803** - gated on `hungarian_diet_1825`, not on the stall flag.
- A "Endow the Academy" (ai 55): HUN-core consciousness +1 and militancy -1,
  plurality +1, prestige +1, sets `hungarian_reform_era` (read by 1001802).
- B "The censor reads Hitel first" (ai 45): HUN-core militancy +1, global
  consciousness -1, no modifier, no flag.

Every flag this file sets is read again: `aus_metternich_system`,
`aus_vormaerz_relaxed`, `hungarian_diet_stalled` and `hungarian_reform_era` all
feed 1001802's `ai_chance`, and `hungarian_diet_1825` gates 1001803.
