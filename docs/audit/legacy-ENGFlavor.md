# Logic review: `CoE_RoI_R/events/ENGFlavor.txt`

*2026-09-06. Hand review of all 62 events (4341 lines) for defects the mechanical audits
(`refcheck`, `audit_events*`, `audit_fire_once`, `audit_pacing`, `audit_owner_scope`) cannot see:
wrong recipient/scope, options whose effects contradict their text, `ai_chance` steering the AI
into absurd choices, dead flag/year gates, `NOT = { a b }` used where NAND was not meant,
implausible magnitudes, duplicated episodes.*

Counts: 20 defects - 4 [high], 10 [medium], 6 [low]. 16 fixed in place, 4 left as proposals.

## Fixed

### [high] `NOT = { a b }` is NAND, not "neither"

The file's dominant defect: a `NOT` block holding two or more conditions is true when *any one*
of them fails, so the second condition never constrains anything. Where the block is the only
re-fire guard (no `fire_only_once`), the event repeats. Every case below was split into one
`NOT` per condition.

| line (pre-fix) | id | block | effect of the bug |
|---|---|---|---|
| 165 | 36902 | `year = 1843` + `work_hours = no_work_hour_limit` | Thomas Cook tours fire long past 1843 |
| 474 | 36909 | `year = 1852` + `has_country_flag = CrystalPalace` | **repeatable +50 prestige** to 1852 |
| 571 | 36911 | `exists = IRE` + `year = 1896` | fires even after Ireland breaks away |
| 666 | 36913 | `year = 1855` + `war_with = USA` | America's Cup fires while at war with the USA |
| 1019 | 36922 | `exists = AST` + `year = 1886` | fires after Australia is independent |
| 1366 | 36929 | `exists = SCO` + `year = 1882` | Tay Bridge fires for a Scotland-less Britain |
| 1409 | 36930 | `war_with = QNG` + `year = 1868` | tea race fires during the China war |
| 1665 | 36937 | `year = 1936` + `has_global_flag = ENGRoyalHouseAnglified` | **repeatable** (flag is the only guard) |
| 1786 | 36939 | `year = 1857` + `exists = MUG` | Doctrine of Lapse fires with the Mughals alive |
| 2827 | 36970 | 5 conditions incl. `has_global_flag = suez_canal_global`, `is_canal_enabled = 2` | **repeatable** Suez investment, canal or no canal |
| 2899 | 36971 | 4 conditions incl. `has_global_flag = panama_canal_global` | same for Panama |
| 2966 | 36975 | `war_policy = pacifism` + `neutrality` + `has_country_flag = suez_egypt_intervention` | **repeatable** badboy +3 / free CB on Egypt |

### [high] 36909 - the Great Exhibition could never fire

`trigger` required `has_global_flag = PlanWorldFair`, but this mod's `events/WorldFairs.txt`
replaced vanilla's scheme: the decade gate is now `PlanWorldFair1850`...`PlanWorldFair1900`
(global) and the *host* gets `set_country_flag = PlanWorldFair` (event 300002, line 924).
Nothing sets the **global** flag anywhere in the mod, so the Crystal Palace event was dead - this
is the `PlanWorldFair` row refcheck reports under "checked but never set".
Fixed: the trigger now reads `has_country_flag = PlanWorldFair`, i.e. Britain won the bid.
The option's `clr_global_flag = PlanWorldFair` was dropped rather than converted: the fair chain
clears the country flag itself when the fair ends (`WorldFairs.txt:1416/1454/1514`), and clearing
it early would break every follow-up event that tests `has_country_flag = PlanWorldFair`.
`fire_only_once = yes` was added, matching every other one-shot in the file.

### [high] 36936 - event fires for the wrong country

Its own comment reads "parallel to AST43801, ENG more often than not will own AST directly at
this point, so needs own event", but the trigger was `tag = AST`, i.e. an exact duplicate of
`ASTFlavor.txt:48` (43801, Burke and Wills) that made Australia see the same episode twice and
Britain never. Changed to `OR = { tag = ENG tag = ENL }`, matching its sibling 36935.

### [medium] wrong option localisation keys

- 253, event 36903 (Victoria's wedding) used `name = "EVTOPTA36902"` -> "I could use a vacation
  too!". Now `EVTOPTA36903` ("A glorious couple!"), which already exists in `text.csv`.
- 402, event 36907 (Vanity Fair) used `name = "EVTOPTA36904"`. Now `EVTOPTA36907`
  ("A scandal!").

### [medium] 36907 - duplicated effect

`capitalists = { consciousness = 1 }` appeared twice in the same option, silently doubling the
capitalist consciousness hit relative to the clerks/officers in the same block. One copy removed.

### [medium] 36984 - wrong province event on the British branch

Perth (2497) under `owned_by = ENG` fired `province_event = { id = 36995 }` (The West Australia
Colony, life rating 15) while the comment on the same line and the AST branch two blocks down
both say Swan River (36994, life rating 20). Britain founding Perth got the worse province.
Changed to 36994.

## Proposals (not applied - design/balance calls)

- **[medium] 36909 `prestige = 50`.** The largest single prestige award in the file by a factor
  of two, and it now stacks on the +10 the World's Fair chain already pays the host (event
  300002). 10-15 would match the rest of the file (36923 Darwin is 25, everything else 1-5).
- **[medium] 36962 "The Dutch Have Refused" pays Britain 10,000 in both options.** Event 36960
  hands the Dutch `treasury = 10000` for signing the Gold Coast treaty, but the British side
  never pays it: 36961 (they agreed) has no cost, and 36962 (they refused) *credits* ENG 10,000
  in each option. Either the acceptance branch should carry `treasury = -10000` on the ENG side
  and 36962 none, or the refusal branch is meant to be a refund of money that was never spent.
- **[medium] 36943 `NOT = { life_rating = 35 average_militancy = 2 }`** (in both the trigger and
  the option's `any_owned` limit). The same NAND shape as the fixed list, but here the intent is
  genuinely unclear - "undeveloped **and** quiet" is the natural reading, yet splitting it
  narrows an already narrow New Zealand development event, and trigger and limit must move
  together. Left alone deliberately.
- **[medium] 36937 `year = 1821`.** "The Name of the Royal House" is the 1917 Windsor renaming
  ("in this time of war with the Germans"); with the mod's 1821 start the year gate is no gate at
  all, and the event can fire in an 1820s Prussian war. Its MTTH modifiers (1860/1880/1900)
  suggest the author expected it late. `year = 1914` would restore the intent.

## Noted, no change

- **[low] 36980-36984 use `tag = BHU` as a proxy.** The Australian colonisation chain fires for
  Bhutan, which takes the empty province in `immediate` and hands it to ENG/AST in the option.
  Deliberate (hence "DO NOT CHANGE ORDER!"), but it silently stops working if BHU is annexed;
  only 36984 bothers to check `exists = yes`.
- **[low] 36999 "Claiming Rupert's Land" has no year gate and no `fire_only_once`**, so it
  repeats every ~9 months from 1821.9.1 until the nine provinces are full. That is how the chain
  is meant to pace colonisation, and each step costs 4,000, so it is left alone.
- **[low] 36965 option B grants `badboy = -2` for *declining* to seize Lagos.** Infamy decay as
  a reward for inaction is odd but harmless and in keeping with PDM's habits.
- **[low] 36966 option B gives a small African state `prestige = 10` and `any_pop = { militancy = -6 }`**
  for declaring war on the British Empire. The magnitude (-6 militancy) is out of scale with the
  rest of the file, where +-1 to +-3 is normal.
- **[low] duplicate localisation keys outside this file.** `EVTNAME36990` is defined twice
  ("The South Australia Capital" and "Claiming Australia") and `EVTNAME36995` twice ("The
  Western Australia Colony" and "Claiming Rupert's Land"); which one shows depends on csv load
  order. Events 36980-36984 and 36996 all title themselves `EVTNAME36990`. Fixing this belongs
  in the localisation pass, not here.
- **[low] `THIS` inside `random_country`/`FROM` blocks (36961, 36966, 36975)** was checked
  against `docs/wiki/list-of-effects.md` ("THIS - the country that fires a country-scope event")
  and is correct: ENG keeps the influence and the alliance breaks land on the right party.

## Verification

`modcheck braces` clean; `refcheck` 14 events / 0 on-actions / 60 loc / 0 modifiers /
128 flags (better than the 129 baseline - the dead `PlanWorldFair` check is gone; a concurrent
`FRAFlavor.txt` pass moves this count too) /
0 names / 8 options; `audit_events` 0 unknown keywords, 0 high, 0 medium;
`cwtools_check` at baseline (12 `production_types` + `CBsAndCores:2448` + `Indochina:188`).
