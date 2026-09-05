# Diplomacy / wars / units / tech / inventions / poptypes audit

Generated 2026-09-06. Mechanical checks: `python scripts/audit_diplomacy.py` (read-only; no mod
file was modified). Start date assumed **1821.9.1**. Vanilla `common/{event_modifiers,
static_modifiers,issues,nationalvalues,traits,cb_types}.txt` plus `docs/wiki/modifier-effects.md`
are used as the modifier-key oracle; `docs/wiki/list-of-conditions.md` as the trigger oracle.

## Counts

| Thing | Count |
|---|---|
| Tags registered in `common/countries.txt` | 432 |
| Tags owning >= 1 province at 1821.9.1 | 199 |
| Diplomacy files / entries | 8 / 119 (58 vassal, 51 alliance, 7 substate, 3 union) |
| Guarantees / spheres declared in history | 0 (`Guarantees.txt` is empty) |
| War files / ongoing at 1821.9.1 | 17 / 9 |
| CB types / goods / buildings / units / poptypes | 82 / 30 / 18 / 24 / 13 |
| Technologies / inventions | 200 / 740 |
| Tech `year` range | 1821-1930; **0 techs with year < 1821**; 27 at 1821, then 1825(4), 1830(10), 1840(8), 1845(3), 1850(17) |
| Machine findings | 41 (5 high, 29 medium, 7 low) -> **37 (0 high, 29 medium, 8 low)** after the 2026-09-06 fix pass |

Clean (zero defects found): unit `build_cost`/`supply_cost` goods, `activate_unit` /
`activate_building` targets, unit `active = no` reachability, invention `limit` references,
duplicate technology/invention names, tech `area`/`year`/`cost` completeness, poptype
`life/everyday/luxury_needs` goods, poptype `rebel` unit refs, `promote_to`, `ideologies`,
war participant tags, `casus_belli` names, `state_province_id`s.

**Tech year answer:** the tree was *shifted*, not extended. No technology has `year < 1821`, so
nothing is free at start; there is a genuine 27-tech 1821 tier (the `post_napoleonic_*` /
`early_*` entries) acting as the pre-1836 tier. Costs are present on all 200 techs.

## Defects

### High

- `CoE_RoI_R/history/wars/PeruvianWarofIndependence.txt:36` — the 1822.5.24 teardown block has the
  sides swapped: it does `rem_defender = SPA` (SPA was added as an *attacker*) and
  `rem_attacker = CHL` / `rem_attacker = ARG` (both were added as *defenders*). Those three
  countries are therefore never removed and the war runs forever.
  Fix: `rem_attacker = SPA`, `rem_defender = CHL`, `rem_defender = ARG`.
- `CoE_RoI_R/history/wars/PeruvianWarofIndependence.txt:3` — sides are also historically inverted:
  the Expedición Libertadora was San Martín (ARG/CHL/PEU) attacking royalist Spain, but SPA is the
  attacker and PEU/ARG/CHL the defenders. Fix: swap `add_attacker`/`add_defender` and move the
  `make_puppet` goals to Spain as defender goals.
- `CoE_RoI_R/history/diplomacy/Alliances.txt:2` — `alliance GCO/ECU` is active at start but **ECU
  owns no province at 1821.9.1** (Ecuador is inside Gran Colombia until 1830). An alliance with a
  non-existent country is a dangling reference. Fix: delete, or set `start_date = 1830.5.13`.
- `CoE_RoI_R/history/diplomacy/Alliances.txt:9`, `:16`, `:30`, `:37` — same problem for **BOL**
  (GCO/BOL, PRG/BOL, BOL/CHL, BOL/ARG). Bolivia owns nothing until 1825. Fix: `start_date = 1825.8.6`.
- `CoE_RoI_R/history/wars/PeruvianWarofIndependence.txt:11` and
  `CoE_RoI_R/history/wars/ColombianWarofIndependence.txt:14` — `liberate_country` war goals name
  `country = BOL` / `country = ECU`. Both tags exist and hold cores (BOL 33, ECU 10 province cores)
  so this parses, but neither is a living country; verify in-game that the goal resolves rather
  than silently voiding the war. Fix: confirm on a test start, otherwise use `acquire_all_cores`.

### Medium

- `CoE_RoI_R/history/diplomacy/PuppetStates.txt:152` — `vassal TUR/EGY` has `start_date = 1833.1.1`,
  so **Egypt is a fully independent country at the 1821 start**, not an Ottoman eyalet. In
  September 1821 Muhammad Ali was still an Ottoman wali (and is fighting the Sudan war in
  `EgyptianConquestofSudan.txt` *as an Ottoman subject*). Fix: add a `start_date = 1805.7.9`,
  `end_date = 1833.1.1` vassal entry, or model it as a substate.
- `CoE_RoI_R/history/diplomacy/PuppetStates.txt:373`, `:381`, `:389`, `:397` — four `vassal` entries
  with `start_date = 1861.1.1` (incl. `TUR/ROM`, `TUR/HDJ`). Inert at start; harmless but they
  duplicate the earlier WAL/MOL entries that only end in 1859. Fix: check the ROM entry does not
  overlap the WAL/MOL ones.
- `CoE_RoI_R/history/diplomacy/PuppetStates.txt:153` — `vassal` with `start_date = 1833.1.1`.
- `CoE_RoI_R/history/diplomacy/Peru-Bolivia.txt:2`, `:9` — `vassal PBC/…` `start_date = 1836.1.1`;
  1836-era leftovers, inactive at start (expected, kept for the later chain).
- `CoE_RoI_R/history/diplomacy/Unions.txt:19` — `union` with `start_date = 1839.4.19`, after start.
- `CoE_RoI_R/history/wars/ACW.txt:5` (CSA), `FarroupilhaWar.txt:4-5` (BRZ, RGS),
  `Taiping Rebellion.txt:4` (TPG), `TexanWarofIndependence.txt:5` (TEX) — participants own no
  province at 1821.9.1. Fine *provided* the tags are released before the war's own date; verify
  BRZ in particular, since Brazil is inside UPB and is released by event, not by history.
- `CoE_RoI_R/technologies/commerce_tech.txt:961,1020,1086,1155,1224,1291,1354,1417,1482,1544,1614,`
  `1688,1762,1832,1899,1971` (17 techs) — set `rich_luxury_needs`, a modifier key that appears
  nowhere in the vanilla game files (its 8 siblings `poor/middle/rich_life/everyday_needs` and
  `poor/middle_luxury_needs` all do). Likely valid but unverified. Fix: confirm in-game that the
  tech tooltip shows the effect; if not, drop the line.

### Low

- `CoE_RoI_R/history/diplomacy/Guarantees.txt:1` — file is empty. Nothing guarantees anything at
  start (no Anglo-Portuguese, no Concert guarantee of the Vienna settlement). Fix: populate or
  delete the file.
- `CoE_RoI_R/history/wars/ACW.txt:1`, `Cochinchina Campaign.txt:1`, `FarroupilhaWar.txt:1`,
  `OttomanBarbaryWar.txt:1`, `Taiping Rebellion.txt:1`, `TexanWarofIndependence.txt:1`,
  `XhosaWar.txt:1` — wars begin after 1821.9.1; expected, listed for completeness.
- `CoE_RoI_R/history/wars/OttomanBarbaryWar.txt:1`, `TexanWarofIndependence.txt:1`,
  `XhosaWar.txt:1`, `FarroupilhaWar.txt:1` — all four start on exactly `1835.10.2`, the PDM 1836
  bookmark's "day before start" convention. Under a 1821 start these are 14 years of untouched
  scripted history. Fix: re-date them to their real dates (Texas 1835.10.2 is correct;
  Xhosa War 1834.12.21; Farroupilha 1835.9.20; Ottoman-Barbary is not a real 1835 war).

## 1821 historical gaps

Present and correct:
- **Greek War of Independence** — `history/wars/GreekWarofIndependence.txt`, 1821.3.25, TUR + IRQ +
  TUN + KDS vs GRE, `annex_core_country`. GRE owns 5 provinces (Nafplion &c.) at start. Good.
- **Portuguese Brazil** — modelled as **UPB** ("Portugal-Brazil"), which owns the Portuguese *and*
  Brazilian provinces; POR and BRZ own nothing and hold cores. Correct for September 1821.
- **Holy Alliance** — RUS/AUS, RUS/PRU, PRU/AUS alliances dated 1815.11.9. Present.
- **Ottoman vassals** — TRI (Tripoli), IRQ, KDS (Kurdistan), SER (1817.11.6), WAL, MOL, TUN are all
  vassals of TUR at start; SER/WAL/MOL/TUN own their own provinces. Correct.
- **Spanish American tags** — GCO (Gran Colombia, 32 prov), MEX (62), PEU (37), CHL (11), ARG (36),
  PRG (8), UCA (Central America, 19), SPA (96) all exist and own territory. BOL/ECU/VNZ/CLM/RPL
  are core-only shells, released later. Reasonable.
- **Persian vassals** — KHZ (Arabistan) and KHR (Khorasan) under PER from 1774; Afghan emirates
  (HRT, HZJ, KDH, KNZ, TAJ, MAK, KAL) under AFG. All own provinces.

Missing or wrong:
- **Ottoman-Persian War of 1821-23** — absent. TUR and PER are at peace at start. This was running
  in September 1821 (Erzurum front). Add a war file, attacker PER, defender TUR.
- **Mexican War of Independence** — absent. MEX simply starts with 62 provinces and no war, and SPA
  has no cores dispute scripted. The Treaty of Córdoba is 24 Aug 1821 so independence is right, but
  Spain's non-recognition (until 1836) has no representation.
- **Quadruple/Quintuple Alliance** — absent. Only the three eastern courts are allied; there is no
  ENG or FRA tie, so the Concert of Europe — the mod's namesake — has no diplomatic footprint at
  start. Add ENG/AUS, ENG/RUS, ENG/PRU (1815.11.20) and FRA from 1818.11.15, or model it as
  guarantees.
- **Anglo-Portuguese alliance** — absent. UPB appears in no diplomacy file at all (`grep UPB
  history/diplomacy/` is empty), so Britain's oldest alliance and its guarantee of Brazil are
  unmodelled.
- **Egypt** — independent at start (see Medium above). Should be an Ottoman vassal/substate in 1821.
- **Algiers (ALD)** — exists and owns province 1700, but is **not** an Ottoman vassal, while Tripoli
  and Tunis are. Deylik Algiers was nominally Ottoman too; either vassalise it or add a comment
  explaining the deliberate asymmetry.
- **Russian sphere ties** — no `sphere` entry exists anywhere in `history/diplomacy/` (the engine
  does not read spheres from there; they come from `history/countries/*.txt`). Nothing in the
  diplomacy tree makes Russia the patron of the Balkan or German minors.
- **Adams-Onís aftermath (1821)** — no war, no diplomacy entry, and no US-Spain relationship is
  scripted; Florida's status was not verifiable from the province tree (`198 - Tallahassee` has no
  matching history file under `history/provinces/usa/`). Worth checking that Florida is USA-owned
  at start, since ratification was February 1821.
- **Guarantees** — the `Guarantees.txt` mechanism is unused entirely, which is the natural place to
  express the Vienna settlement (Cracow, Switzerland's neutrality, the Ionian protectorate).

## Fix pass 2026-09-06

Re-run `python scripts/audit_diplomacy.py`: **0 high findings remain** (was 5). Checks after the
edits: `modcheck braces/tags/provinces` clean on all seven touched files, `cwtools_check.py` at
baseline (12 `production_types` + `CBsAndCores:2448` + `Indochina:188`).

### Fixed

- **`history/wars/PeruvianWarofIndependence.txt`** — rewritten. Sides swapped to the historical
  arrangement: `add_attacker = PEU/ARG/CHL` (the Expedición Libertadora), `add_defender = SPA`.
  Teardown at 1822.5.24 now matches (`rem_attacker` on the three, `rem_defender = SPA`). War goals:
  `cut_down_to_size` for PEU and ARG against Spain (targetless cb, no `country`/`state_province_id`
  field required), and the three `make_puppet` goals kept but now belong to SPA as the *defender*.
  The invalid `liberate_country … country = BOL` goal was dropped — BOL is a core-only shell in 1821
  and the goal could not resolve. (The equivalent `country = ECU` goal in
  `ColombianWarofIndependence.txt` is left alone; it parses, and reworking that war was out of scope.)
- **`history/wars/OttomanPersianWar.txt`** (new) — the 1821-23 war. `1821.9.10` PER attacker vs TUR
  defender, single `status_quo` war goal (a stock cb with `po_status_quo = yes` and no state or
  third-country field), torn down `1823.7.28` at the Treaty of Erzurum. Modelled on
  `GreekWarofIndependence.txt`.
- **`history/diplomacy/Alliances.txt`** —
  - `GCO/BOL` re-dated `1825.8.6` → `1828.7.6` (Bolivia only exists from 1825; Sucre's republic was
    a Gran Colombian client until the Chuquisaca mutiny). Kept.
  - `GCO/ECU`, `PRG/BOL`, `BOL/CHL`, `BOL/ARG` **deleted**. All four had `end_date` *before* the tag
    could exist, so they could never have been live; and none is defensible once re-dated —
    Ecuador's existence *is* Gran Colombia's dissolution, Francia's Paraguay had no alliances at all,
    and Bolivia was not allied to Chile or Argentina (it fought Argentina in 1837). These were 1836-
    bookmark-shaped filler, not historical ties.
  - Added the **Quadruple Alliance**: `ENG/AUS`, `ENG/PRU`, `ENG/RUS`, `1815.11.20` → `1823.1.1`,
    matching the existing RUS/AUS, RUS/PRU, PRU/AUS Holy Alliance window.
  - Added the **Anglo-Portuguese alliance** as `ENG/UPB` (`1810.2.19` → `1825.8.29`). POR owns zero
    provinces in 1821; the Braganza state is UPB, which owns 100.
- **`history/diplomacy/PuppetStates.txt`** — `vassal TUR/EGY` `start_date` moved `1833.1.1` →
  `1805.7.9` (Muhammad Ali's investiture as wali). `end_date = 1840.7.1` unchanged, so Egypt is an
  Ottoman vassal for the whole 1821 start. Compatibility checked: `events/Oriental Crisis.txt`
  event 90075 *requires* `vassal_of = TUR` plus `year = 1837` before it fires `release_vassal = EGY`,
  so the Oriental Crisis chain now works as designed instead of being dead from turn one;
  `EgyptianConquestofSudan.txt` (1820-1821, EGY vs SUD) runs correctly with Egypt as an Ottoman
  subject, which is what it depicts. No decision or event was found that assumes EGY is
  *independent* at start.
- **1835.10.2 wars** — `XhosaWar.txt` re-dated to `1834.12.21` (Sixth Xhosa War), `FarroupilhaWar.txt`
  to `1835.9.20` (Porto Alegre rising). `TexanWarofIndependence.txt` left at `1835.10.2`, which is
  the real date (Gonzales). **`OttomanBarbaryWar.txt` kept**, not deleted: it is historical — the
  Porte deposed the last Karamanli pasha and restored direct rule over Tripolitania on 26 May 1835 —
  and it is the mechanism that returns TRI to Ottoman control. Re-dated to `1835.5.26` and a comment
  added recording why it stays.

### Left as-is (verified valid)

- **`rich_luxury_needs` in 17 commerce techs** — **valid, no change.** `docs/wiki/modifier-effects.md`
  documents the family as `(strata)_(level)_needs` with *strata* ∈ {poor, middle, rich} and *level* ∈
  {life, everyday, luxury}, so all nine combinations exist. Vanilla technologies/inventions happen to
  use only `luxury_needs`, `poor_luxury_needs` and `middle_luxury_needs`, which is why the audit's
  "no vanilla file uses it" heuristic flags it; that is an absence of usage, not of the key. The mod
  already uses `rich_luxury_needs` 58 times outside these techs. Downgrade this finding to noise.

### Deferred

- **FRA in the Quintuple Alliance** — *not* added. France acceded to the congress system at
  Aix-la-Chapelle (1818.11.15), but the Quadruple Alliance's Article VI was directed *against*
  France; a FRA/AUS alliance entry would misrepresent the relationship and hand France a great-power
  bloc at start. Left as a design decision.
- **`ENG/POR`** — not added, since POR owns nothing at 1821.9.1 and is released by event, not by
  history. If POR is ever given a scripted release date the alliance can be dated from it.
- **Spheres and guarantees** (`Guarantees.txt` still empty), Mexican non-recognition, Algiers'
  non-vassalage, the Adams-Onís/Florida check, the four `1861.1.1` puppet entries, and the
  `Peru-Bolivia.txt` / `Unions.txt` post-start entries — all untouched this pass.
