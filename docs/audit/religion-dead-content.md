# Audit: religion content (restored 2026-09-06)

Companion tool: `scripts/audit_religion.py` (read-only inventory) and
`scripts/audit_religion.py check` (re-runnable regression gate, exit non-zero on any finding).
Design and review: `docs/design/religion-restoration.md`,
`docs/design/religion-restoration-review.md`.

**Status: the dead-religion condition described by the earlier version of this file has been
fixed.** Pops carry real religions again, the sub-cultures live in the culture field, and the
~124 previously unreachable religion triggers are live. What follows records the new state and
what to watch.

## 1. What pops carry now

`history/pops/1821.9.1` (62 files, 21 026 live pop entries) after the restoration:

| religion | pops | | religion | pops |
|---|---|---|---|---|
| catholic | 4 915 | | shiite | 418 |
| animist | 3 998 | | theravada | 285 |
| sunni | 3 836 | | gelugpa | 205 |
| protestant | 2 656 | | shinto | 204 |
| orthodox | 1 704 | | coptic | 122 |
| mahayana | 1 530 | | sikh | 39 |
| jewish | 559 | | zoroastrian | 22 |
| hindu | 529 | | mormon | 4 |

Zero pops hold a culture name in the religion field. 1 910 pops moved their sub-culture
(`north_german` 604, `south_german` 534, `dixie` 256, `north_italian` 206, `south_italian` 94,
`anglo_canadian` 68, `occitan` 58, `picard` 42, `australian` 30, `anglo_african` 18) into the
`culture` field, so `german` and `italian` now have **0 pops**.

The 78 fully-commented-out pop blocks in `Russia.txt` still carry culture-named religions
(`ashkenazi`, `sephardic`, `ukrainian`, `mongol`, `north_caucasian`). They are dead text; do not
uncomment them without converting them first.

## 2. `common/religion.txt`

Truncated to the six real groups (`christian`, `muslim`, `jewish_group`, `zoroastrian_group`,
`eastern`, `pagan`), 148 lines, 24 religions. The 269 cultures that had been copied in as
"religions" are gone. Every state religion in `history/countries/*.txt` (521 files, all real
religions: protestant 148, sunni 115, catholic 110, animist 36, hindu 27, orthodox 25,
mahayana 20, theravada 10, shinto 8, shiite 7, coptic 6, gelugpa 5, jewish/sikh/mormon/ibadi 1
each) is still defined. `druze`, `ibadi` and `fetishist` are defined but carried by no pop.

`common/cultures.txt` needed no change: all 10 sub-cultures were already defined in the right
groups, and the union tags (GER, ITA, USA) hang off the *group*, so union mechanics are
untouched.

## 3. What became live

Everything below was previously a no-op and now evaluates for real. None of it was edited; the
data change is what switched it on.

- **48 `is_state_religion` sites in `poptypes/`** (4 in each of 12 poptype files). The widest
  effect of the whole pass:
  - `secularized = { factor = 1.25  modifier = { factor = 1.50  NOT = { is_state_religion = yes } } }`
    applied to **every** pop before; now only to religious minorities.
  - the `moralism` and `pluralism` `modifier = { factor = 1.25  is_state_religion = yes }` blocks
    were dead; now they apply to the religious majority.
  Net: religious-policy pressure rebases away from secularization in every country on day one.
  **Deliberately not retuned in this pass.**
- **10 `has_pop_religion = THIS` migration_target modifiers** in `poptypes/*.txt` become real
  religious clustering; the 20 `religion = jewish` / `= mormon` migration modifiers
  (`is_core = ISR` / `is_core = DES`) become live.
- **`common/pop_types.txt:88`** - `NOT = { religion = THIS }` under `religious_policy = moralism`
  gave every pop -0.1 militancy; now only religious minorities get it.
- **18 `is_state_religion` occurrences at 9 event sites** in `events/ColonialUprisings.txt`,
  `events/ExtraElectionEvents.txt`, `events/NationalistMovements.txt`. These make events
  *narrower*, not commoner (14580's `is_state_religion = no` limit shrinks; 15250 narrows
  sharply; 140801/140901 stop being guaranteed no-ops).
- **The Persian Sunni/Shiite chain**, `events/DIM/PERFlavour_five_x.txt`, 155 `has_pop_religion`
  sites - all in effect `limit`s, none in a trigger, earliest self-firer 1832. Needs a balance
  review as a **separate pass**.
- `events/Dungan.txt` (the Hui massacre limits are real reductions now), `events/MOR.txt`
  (290100, 1834), `events/Taiping.txt`, `events/CHIFlavor.txt:3164`, `events/BRZFlavor.txt`,
  `events/ENGFlavor.txt`, `events/Sepoy rebellion.txt`, `events/PER_crises.txt`,
  `decisions/Germany.txt:364`, `decisions/RUS.txt:360`,
  `decisions/extra_decisions.txt:1179` (`pop_majority_religion = orthodox`, panslavism).
- **`carlist_rebels`**: the `NOT = { has_pop_religion = catholic }` spawn modifier was removed on
  2026-09-06 *because* it was always true (which zeroed the spawn chance for every pop). It has
  been reinstated and now does what it says.
- Country-scope `religion = X` (state religion) was always valid and is unaffected.

Assimilation is the one engine behaviour with no script site to point at: the mod defines no
`assimilation_chance`, and the engine slows assimilation across a religion boundary. This is
active for the first time (Habsburg lands, Ottoman Balkans). Conversion stays hard-disabled
(`common/pop_types.txt:3506-3510`, `factor = -100.0 always = yes`).

## 4. Rebels

Every rebel type sets `allow_all_religions = yes` and none uses `area = religion|nation_religion`
or `independence = religion`, so rebel membership and goals are unchanged by the religion side.
The *culture* split does matter: `separatist_rebels` / `nationalist_rebels` use
`area = nation_culture` with `allow_all_cultures = no`, so which tag north-German or Italian
nationalists try to release in foreign-held provinces (Danish Holstein, French Alsace, Austrian
Lombardy) is now decided over the sub-cultures. `history/countries` was repointed so each state's
own pops stay accepted.

## 5. Regression gate

```
python scripts/audit_religion.py check
```

asserts, and must stay at 0 problems:

1. no pop in `history/pops/1821.9.1` holds anything but a real religion;
2. no `has_pop_religion` / `pop_majority_religion` / `religion` in `events/`, `decisions/`,
   `common/`, `poptypes/`, `inventions/`, `technologies/`, `units/` names a culture;
3. no `culture = german` / `= italian` (or `primary_culture`, `has_pop_culture`,
   `add_accepted_culture`, ...) site remains - those cultures have no pops;
4. `common/religion.txt` defines no culture as a religion, and every state religion is defined.

## 6. Not done in this pass

- Balance review of the Persian Sunni/Shiite chain (155 sites).
- Retuning the religious-policy issue weights in `poptypes/` now that `is_state_religion` works.
- Deciding whether to re-enable `conversion_chance`.
- In-game smoke test: none of the above has been observed in a running game.
