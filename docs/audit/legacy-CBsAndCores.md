# Line-by-line audit: `events/CBsAndCores.txt`

*2026-09-06. 2455 lines, events 2510-2672: diplomatic-incident CB generators (2510-2570),
the core-integration / national-assimilation province chain (2600-2626) and the
territorial-loss chain (2650-2672). Line numbers are pre-fix.*

CB direction convention used throughout this audit (`docs/wiki/list-of-effects.md:245,247`):
`casus_belli = { target = X }` grants the **scoped** country a CB against X;
`add_casus_belli = { target = X }` grants **X** a CB against the scoped country. So the
`random_country = { ... add_casus_belli = { target = THIS } }` idiom in 2510/2520/2530/2540/
2550/2560/2570 hands the CB to the event's own country - which is what those events' texts
say ("we cannot allow this to go unpunished"), so those are correct as written.

## Fixed

| line | id | problem | fix |
|---|---|---|---|
| 1890 | 2616 | [high] `random_country` limit is `any_core = { owned_by = THIS ... }` with no `NOT = { tag = THIS }`, so the assimilating country itself qualifies (it owns its own cores) and can draw relation -50, `leave_alliance` and a casus belli **against itself**. The parallel selector in 2615:1716 has the guard. | added `NOT = { tag = THIS }` |
| 1901 | 2616 | [high] CB direction reversed: `add_casus_belli = { target = THIS type = humiliate }` inside the aggrieved country's scope gives *the assimilator* a humiliate CB against the country whose minority it just repressed. Both the desc ("a diplomatic incident ... minorities claim") and the designed-for counterpart 2626:2181 (`casus_belli = { target = FROM }`) want the aggrieved country to gain the claim. | `add_casus_belli` -> `casus_belli` |
| 546 | 2530 | [medium] `relation = { who = THIS value = -20 }` sits at the option root, i.e. the country's relation *with itself* - a silent no-op, so the incident costs nothing. 2510:134 and 2520:197 put the same effect inside the other country's scope. | moved into the neighbour's `owner = { }` scope |
| 1401 | 2610 | [medium] `any_country` limit without `NOT = { tag = THIS }`: the assimilator is included in the -50 relation sweep (self-relation, no-op, but it also makes the block's intent unreadable and matches the 2616 defect class). | added `NOT = { tag = THIS }` |
| 1561 | 2612 | [medium] the trigger's `any_core` omits `NOT = { is_cultural_union = THIS }`, which the option's own limit at 1587 has. Assimilation aimed at a cultural-union core is therefore never cancelled by this event even though 2610/2615/2620 all refuse to progress it, leaving `national_assimilation` stuck on the province forever. | added the missing `NOT` to the trigger |
| 2330-2420 | 2670 | [medium] both `ai_chance` ladders are cumulative `relation = { who = FROM value = N }` rungs (the trigger is `>=`, so a good relation satisfies every lower rung as well). The bottom rung `value = -200` is always true, so option A ("comply") is multiplied by `factor = 0` unconditionally and the AI **always** refuses its overlord. | each rung below the top gated with `NOT = { relation = { who = FROM value = <next rung up> } }`, in both options |

## Reported, not changed

| line | id | problem |
|---|---|---|
| 981 | 2570 | [medium] `add_casus_belli = { type = acquire_state }` with no `state_province_id`. Per the wiki that field identifies the state for acquire_state; without it the granted CB has no goal. Fixing it needs the target's state picked in script (`random_owned` inside the target, then `owner = { ... }`), which changes the event's shape - left for a deliberate rework. Same class, 883/2560: `release_puppet` without `country =`; that omission is however the established idiom in this mod (`1german_revolution_1848.txt:556`). |
| 115, 148 | 2510 | [low] `military_industry = -1` is not an effect - `military_industry` is a factory/goods type (`inventions/industry_inventions.txt`), only valid inside modifier blocks. Silently ignored, so option A and option B differ only in relations/prestige. Same idiom in `DIM/DIM_East_Sumatra.txt:90` and `MostlyHarmless.txt:57`; a tree-wide decision, not a local one. |
| 809-819 | 2550 | [low] an uncivilised, non-colonial country is handed `humiliate` **and** `place_in_the_sun`. `common/cb_types.txt` gates `place_in_the_sun` on `can_use = { THIS = { ai = yes } }`, so a human in this position can never use the CB the option promises; the AI can. Flavour-plausible, mechanically half-dead. |
| 283 | 2520 | [low] `months = 3` on a humiliate CB against a great power. Three months is shorter than mobilisation plus a march; the CB will usually expire unused. Compare 12 months everywhere else in the file. |
| 566-696 | 2540 | [low] single option, so "Merchant Conflict" is a forced CB with no player choice and no `ai_chance`; the trigger also lacks `war = no`, unlike 2510/2530, so it can fire mid-war. |
| 1043, 1312 | 2600/2610 | [low] `owner = { badboy = 2 }` for merely *starting* integration/assimilation of a province already owned and of accepted culture. 2 infamy is the price of an annexation war goal; the AI ladders below then spend three more modifiers trying to undo it. |
| 2116-2226 | 2626 | [low] both options end with `FROM = { random_owned = { ... remove_core = THIS } }`, so "We will not stand for this!" still surrenders the core, only with CBs attached. Event deliberately disabled since 2022 (its only caller, 2625:2096, is commented out) - left alone. |
| 2229, 2245, 2317 | 2650/2651/2670 | [low] known orphans, nothing fires them; 2660/2671/2672 are only reachable through them, so the whole territorial-loss chain is dead content. Kept for a future caller. |
| 2444-2450 | 2672 | [low] two `attacker_goal` blocks (`acquire_all_cores` and `make_puppet`) in one `war`; the engine takes one war goal per declaration, so `make_puppet` is decoration. |
| 1029, 1069 | 2600 etc. | [low] province events compare `is_core = THIS` / `controlled_by = THIS` where the root is the province and the engine coerces to its owner. Ugly but the mod-wide idiom; changing it would be a rewrite of the whole 2600-2625 chain. |

## Windows / pacing from the 1821 start

Nothing in the file is unreachable at the bookmark. 2510 needs `steamers` and 2570 a fascist
government, so both are naturally late; the 2600-2625 chain is MTTH 120-180 months and gated on
`war = no`, i.e. it is a slow peacetime background system, which is intended.
