# Changelog

Notable changes to the mod, newest first. One line per change; file names where they help.
Audit reports live in `docs/audit/`, design notes in `docs/design/`.

## 2026-09-06 — audit and repair pass

A read-only audit of the whole tree (countries, provinces, diplomacy, decisions, `common/`,
localisation, events, performance, AI/balance) followed by the repairs it justified, plus three
new event chains. Nothing in this pass has been tested in a running game.

### Fixes (crash / logic)

- Province 2637 was filed under Chukotka; it is Lanfang's West Borneo capital (San Kuew Jong). Moved to `history/provinces/asia/`.
- Four province ids had two history files each (1396 Api, 1397 Sandakan, 2539 Bougainville, 686 Line Islands). Kept the copy matching `map/region.txt`, deleted the `indonesia/` duplicates.
- `history/provinces/japan/1661 - Nagasaki.txt` had a `1821.1.1` block dated before the 1821.9.1 start; merged into the top-level block.
- Boer appeal event 98241 used `add_casus_belli`, which grants the CB to the *target* — Britain handed the Boers a CB against itself. Now `casus_belli`.
- Missing event 98241 (`ENG`), a brace error in the CSA `leave_slave_trade` decision, a bad cb type, five flag-name typos, four wrong loc keys and ~40 missing strings, all found by the new `scripts/refcheck.py`.
- The economy rework (99997, 999958, 27 WorkPlaceEvents dispatchers) gated on `tag = BHU`, so annexing Bhutan switched it off. Now gated on the `economy_pulse_host` country flag, elected by new event 2000100, whose trigger (`is_greater_power` + no country holds the flag) re-elects a host the day after the old one dies.
- The treasury sink in 99997 could overflow: Clausewitz parses money as int32 hundredths, so the `-50000000` effects wrapped and could pay the country. Disabled pending real thresholds.
- `events/Goods.txt` 1107-1138 were briefly dispatched from 99997 via `random_owned`, which cut their conversion rate 10-30x. Reverted to MTTH province events with cheap-first triggers.
- 2000100 now clears `economy_pulse_host` from any previous holder, so a re-election cannot leave two hosts.
- `on_actions` weights are picks, not chances — the engine fires exactly one event per country per pulse. A watchdog event (2000101) had been added to both the yearly and quarterly lists, cutting the `Canals.txt` 97200/97250/97350 rate and then halving the whole quarterly economy pulse. The watchdog and its `economy_pulse_lock` flag are gone; `on_yearly_pulse` and `on_quarterly_pulse` hold what they originally did.
- Events A-G: cleared four unknown keywords (`has_truce`, `unciv_military_industry`, `random_neighbor`, `activate_unit`), stopped 99990/31240 re-firing, repointed the China awakening chain at THIS/FROM, guarded ACW 16000, fixed the `realtion` typo and the dead `suez_canal_built` flag, lowered two bare `year = 1836` start-guards.
- Events H-Z: restored the religion filter in five empty `TemperanceLeague` OR blocks (the whole feature was dead), replaced seven empty `LiberalRevolutions` OR blocks with real building names, fixed the NobelPrize off-by-one flag, `relio`/`religion = north_german` -> `culture`, PER_crises scope wrappers, the July Revolution year gate, `modifer` -> `modifier`, and the missing Taiping 1850-1855 MTTH step.
- Decisions: `the_vega_expedition` tested a flag the canal chain never sets; two duplicate decisions deleted; three spammy repeatables closed with `_taken` flags; `hide_debug_decisions` / `show_debug_decisions` added so the debug menu is actually toggleable.
- `common/`: invalid modifier keys in `crime.txt`, `event_modifiers.txt`, `triggered_modifiers.txt` and `issues.txt`; duplicate `silk_famine` block; `CEASECOLONIZATION_DIPLOMATIC_COST` assigned twice in `defines.lua`.
- Localisation: wrong country names (ABU, CNG, KAL), mojibake in `PDM_CE.csv`, five `[Placeholder]` descriptions, real mobilize/demobilize tooltips, and four `text.csv` rows whose keys were shifted one event forward.
- `history/countries`: 9 capitals moved into provinces the tag owns, 8 undefined and 14 out-of-window `ruling_party` names repointed, HAI/KMT government fixes, 35 dominion party start dates, ETH registration, ENG -> `ENG_conservative`.
- The 11 RGO education ladder events (`+education_RGO.txt` 9999959-9999969) are `is_triggered_only` and dispatched per state from the quarterly pulse 99997 instead of being evaluated for every province every day: -117k clause-evals/day. Resync latency goes from ~8-15 days to up to a quarter; see `docs/audit/performance.md`.
- Event trigger clauses in 26 files reordered cheap-gates-first (121 triggers). A permutation of a pure predicate cannot change what fires; modelled daily trigger work drops ~22%. See `docs/audit/performance.md`.

### Balance — **UNTESTED IN GAME**

- `common/production_types.txt`: the five factory templates' `efficiency` blocks are *maintenance* goods, bought daily per level and summed with `input_goods`. They were tuned against a price table 20-200x cheaper than the current `common/goods.txt`, so heavy (0.26x), light (0.15x) and food (0.21x) factories could not break even at any employment level — including the 376 `heavy_factory` levels that exist at the 1821 start.
- Each block is scaled by a single per-template factor to land at a 1.35x revenue/(input+maint) ratio at base prices. No `value`, `input_goods`, owner, employee or workforce entry moved. Also `military_factory` `heavy_industry` 35 -> 20, `luxury_factory` `light_industry` 22 -> 10 with `value` 25 -> 29, and `artisan_horsebreeder` relaxed to 2.42x because artisans are the world's only source of horses.
- Expected effect: the AI's industry is solvent from day one and stops ranking military/luxury factories 10x above everything else; raw-goods demand falls hard (those 376 heavy levels bought ~154,000/day of coal, iron, copper, lead, sulphur, timber, oil, rubber and horses, now ~16,800).
- Watch in a play test: RGO stagnation and collapsing raw prices (if so, raise `value` on the raw tiers rather than re-inflating maintenance); factory profitability after 1840, once `heavy_industry`/`light_industry` trade above base; `food_factory`, which still emits 400 units of a good priced 0.5 and will track `food_industry`'s price to the floor; whether artisans still crowd out factories.
- Method, before/after table and the solver (`scripts/balance_factories.py --target 1.35`) are in `docs/design/factory-balance.md`.
- Start-state tech outliers: AUS 14 -> 19 techs, CSA 49 -> 22 (the USA's list), 13 unformed release tags 24 -> 14, SPC prestige 50 -> 0.
- Event spam guards restored on `GreatPowers.txt` 800004/800006 and `00_CoE_RoI.txt` 99988.

### New content

- **Belgian Revolution prelude**, `events/BELRevolutionGVG.txt` ids 1000301-1000308: Brussels riots after the July Revolution, crack down or concede, the Provisional Government (recognise / fight / appeal to the Holy Alliance), French and British reactions, the Twenty-Four Articles, Leopold's accession, and an 1839 Treaty of London fallback, handing off to PDM's existing London Conference (36720, now gated to 1830 and to `BEL_revolt_in_progress`). No new provinces, modifiers or pictures. `docs/design/belgian-revolution.md`.
- **Decembrist revolt**, `events/RUSDecembristGVG.txt` ids 1000400-1000403: the death of Alexander I and the interregnum, the rising on Senate Square (crush / negotiate / let Constantine reign, with a news article), then the Third Section and Pestel's *Russkaya Pravda*. Fills the 1821-1836 gap; `RUSFlavor.txt` only starts in 1827. One new modifier, `nicholas_reaction`. `docs/design/decembrist-revolt.md`.
- **Greek kingdom**, `events/GREKingdomGVG.txt` ids 1000500-1000502: the London Protocol crown offer, Otto of Wittelsbach landing at Nafplion under the Bavarian regency, and the 3 September 1843 revolution (mutually exclusive with the `hellenic_parliament` decision via its `voule_ton_ellinon` flag). One new modifier, `bavarian_regency`. `docs/design/greek-kingdom.md`.

### Start-state history (1821.9.1)

- Bavaria is a constitutional monarchy, not an absolute one — the 1818 constitution gave a bicameral Landtag with an elected lower house. `BAYFlavor` 33401/33402 already accept it.
- Egypt starts as an Ottoman vassal from 1805 (`PuppetStates.txt`), and because a vassal cannot lead its own war the ongoing Egyptian conquest of Sudan was undefined behaviour. Sennar fell in June 1821 and Kordofan in August, so SUD's 17 provinces now start owned and controlled by EGY (SUD/DAR/ETH/TIG cores kept) and `history/wars/EgyptianConquestofSudan.txt` is deleted. SUD is still released later by the ARAFlavor chain.
- Peruvian War of Independence: attacker/defender sides were inverted. Now PEU/ARG/CHL vs SPA, with matching teardown and `cut_down_to_size` goals; the unresolvable `liberate_country BOL` goal is gone.
- New `history/wars/OttomanPersianWar.txt` (1821-1823, PER vs TUR, `status_quo`).
- Alliances: four impossible ECU/BOL pairs deleted, GCO/BOL re-dated to 1825, and the Quadruple Alliance (ENG with AUS/PRU/RUS) plus the Anglo-Portuguese alliance (ENG-UPB) added.
- Xhosa and Farroupilha wars re-dated; the Ottoman restoration of Tripoli kept and dated.
- Whole pass documented in `docs/audit/start-state-1821.md`: SPA (Trienio), UPB (Vintista), SIC, SAR, FRA, PRU, AUS and RUS were already correct, GRE deliberately stays absolute, PER `civilized = yes` is deliberate.

### Tooling

- `scripts/refcheck.py` — cross-reference checker: events fired but never defined, orphaned `is_triggered_only` events, missing localisation, undefined modifiers, one-sided flags, unknown names, `on_actions` entries, option counts.
- `scripts/audit_countries.py` — `history/countries` vs `common/countries.txt`: unregistered tags, capitals not owned, undefined/inactive ruling parties, illegal ideologies.
- `scripts/audit_provinces.py` — duplicate province history files, pre-start dated blocks, pops in unowned provinces, regions spanning continents. Regenerates `docs/audit/history-provinces.md`.
- `scripts/audit_diplomacy.py` — `history/diplomacy` and `history/wars` consistency, plus technology/invention modifier keys.
- `scripts/audit_decisions.py` — duplicate decisions, missing `ai_will_do`, unguarded repeatables, duplicate formation paths.
- `scripts/audit_common.py` — `common/` vocabulary and counts against vanilla, invalid modifier keys, duplicate definitions, `defines.lua` diff.
- `scripts/audit_loc.py` — conflicting keys, mojibake, placeholders, malformed rows, missing country names/adjectives.
- `scripts/audit_events.py` — unknown trigger/effect keywords, re-firing events with permanent effects, `year = 1836` gates that lock out the 1821 start.
- `scripts/audit_perf.py` — scores every self-firing event by trigger cost and ranks the hotspots.
- `scripts/balance_factories.py` — factory and artisan margins including maintenance; `--vanilla` for the reference band, `--target R` for the budget solver.

### Removed files

- Fully commented-out event files, with their id ranges recorded as reserved in `events/GVG Event IDs.txt`: `+demand.txt`, `industrial_demand.txt` (also a latent duplicate-id crash on 999971-999999), `+education_RGO1.txt`, `+education_RGO2.txt`, `0_demographic_transition.txt`, `0_demographic_transition2.txt`, `population trends.txt`.
- `events/money.txt` — a debug handout with an id past the int32 event-id range and a `TAG = HAW` line that is not a condition.
- `decisions/SetupGVG.txt` — a stale duplicate of `events/SetupGVG.txt`.
- `history/wars/EgyptianConquestofSudan.txt` and the four duplicate province files listed above.

### Deferred / design questions

- **Flat literacy.** Every one of the 521 history files starts at `literacy = 0.01`, and the dated 1836/1861 blocks were flattened too (commit `8f5e1248`). No script effect in Victoria 2 can set pop literacy, so this is a deliberate design, not a bug — recorded in `docs/audit/ai-balance.md` rather than reverted. Open question: whether the great powers should still start with a literacy edge.
- **Empty spheres and guarantees at start.** `history/diplomacy/Guarantees.txt` is empty and no `sphere` entry exists anywhere, so the Vienna settlement has no mechanical backing at 1821. See `docs/audit/diplomacy-tech.md`.
- **1031 conflicting localisation keys** across the csvs (the alphabetically first file wins). Only the winner rows were fixed this pass; the duplicates themselves stand. `docs/audit/localisation.md`.
- **39 history/countries files for tags not registered in `common/countries.txt`** (BMK, DUR, ERT, KRL, KYR, ...) plus the REB placeholder. Either register or delete; `audit_countries.py` reports them as `[high]` until then.
- **Abandoned events** — 14 `is_triggered_only` events nothing ever fires, kept on purpose. Baseline in `.claude/skills/validate/SKILL.md`.
- **Performance hotspots needing a design change, not a reorder**: `+education_RGO.txt` 9999959-9999969, `crises.txt` 20110-20112, Ottoman 31268, `Revolution_Nationalism_Event.txt` 97175, `TemperanceLeague.txt` 130, `BoerWar.txt` 98225/98226, and the `Goods.txt` 1107-1138 dispatch, which needs a per-province pulse that preserves the MTTH rate. `docs/audit/performance.md`, `docs/audit/core-systems.md`.
- **`food_factory` price floor** — at `food_industry` = 0.5 the template emits 400 units for 200 of revenue, so its margin is hostage to one price. Fixing it means moving `goods.txt`, which is a separate pass.
- **`defines.lua` values that need a decision, not a fix**: `INFAMY_STATUS_QUO` 0 -> 1 (white peace now costs infamy, which vanilla never does), `BADBOY_LIMIT` 25 -> 50 (containment coalitions almost never form), and the bureaucracy trio `MAX_BUREAUCRACY_PERCENTAGE` 0.01 -> 0.001 with `BUREAUCRACY_PERCENTAGE_INCREMENT` = 0, which freezes admin efficiency. All three are old deliberate commits; `docs/audit/common.md` has the archaeology.
- **Rebels and casus belli** — the `defection = none` changes, the 1-100 `spawn_chance` rebase and the 24 zero-infamy event CBs were traced back to the PDM import and to deliberate, self-documented rework. No change made; see `docs/audit/rebels-cb.md`.
