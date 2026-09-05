# Legacy audit: `events/Ottoman_Event.txt` + `events/TURFlavor.txt`

*2026-09-06. Line numbers are pre-fix. `NOT = { a b }` with several statements is NOR
(true only when all are false) - those guards are correct and are not listed.*

## Fixed in this pass

| line | id | problem | fix |
|---|---|---|---|
| 2154 | 31252 | **[high]** `CRE = { all_core = { remove_core = TUR } }` on the branch where Egypt agrees to *pacify Crete for the Sultan*. The effect contradicts the option text: it permanently deletes the Ottoman claim on every Cretan core while TUR still owns the island, turning helpful vassal support into a silent loss of cores (and later nationalist unrest against TUR). | line removed |
| 2221 | 31253 | **[high]** identical `CYP = { all_core = { remove_core = TUR } }` in the Cyprus twin. | line removed |
| 2230 | 31253 | **[medium]** the refusal option ("The Empire must fend for itself") also ran `leave_alliance = TUR`; the identical option in the Crete twin (31252) does not, and outright defection is what 31261 option B is for. Duplicated-episode asymmetry. | line removed |
| 2636 | 31264 | **[medium]** no `fire_only_once`, unlike its Russian twin 31265. The only re-entry guard is the country flag `greek_question`, which **31269 option A/B clears** while GRE still exists and still holds `legitimacy`. Every European GP could therefore be re-offered the Greek Question after the Egyptian peace and pay `treasury = -1000` + `create_alliance = GRE` again, repeatedly. | permanent country flag `greek_question_answered` added (trigger + all three options). `fire_only_once` is **engine-global**, so on 31264 - which any European GP can receive - it would have let only the first GP in the world ever see the event; 31265 is RUS-only so its `fire_only_once` is harmless. |

## Reviewed and deliberately not changed

### Chain wiring (Greek War of Independence, 31250-31269)

The FROM/THIS hops are sound. 31251 fires 31252/31253 into `EGY`, whose options answer with
`TUR = { country_event = 31254/31255 }`; 31257 fires 31259 to itself and 31258 to a human GRE;
31259 -> 31261 (EGY) -> 31262/31263 (TUR). Every `random_country = { limit = { tag = X ... } }`
wrapper re-scopes with an explicit `TUR = { ... }` / `EGY = { ... }` before writing flags, so no
flag lands on the wrong country. Province ids (834, 839, 845, 847, 848, 855, 973-1048) and the
regions used (`GRE_826`, `GRE_837`, `TUR_805`, `TUR_823`, `TUR_832`, `TUR_855`, `EGY_843`) all
exist in `map/definition.csv` / `map/region.txt`.

- **[low] 2172, 2751** - `title = "EVTNAME31252"` on 31253 and `title = "EVTNAME31264"` on 31265
  are shared keys, not typos: `EVTNAME31253` and `EVTNAME31265` do not exist in any csv, so
  "correcting" them would print the raw key. Adding the two keys would be an improvement, not a fix.
- **[low] 1936** - 31250's `any_owned` region list omits `GRE_826` (Peloponnese) and `TUR_832`
  (Thessalia). Looks like an omission but is not: 31256 fires on the same day (TUR owns 839, GRE
  does not exist, mtth 1 day) and applies the heavier `militancy = 6` + `patriot_uprising` to
  exactly `GRE_826` + 845. The two events partition the map; do not merge the lists.
- **[low] 1946/1951** - 31250 hands `GRE` and `EPI` a draft modifier although neither exists in
  1821 (TUR owns the land). Harmless in the engine, but the modifier is wasted.
- **[low] 2019-2029, 2261** - `any_pop = { limit = { culture = greek } }`: in pop scope `culture`
  tests the *province majority*, not the pop (`docs/wiki/list-of-conditions.md`, has_pop_culture).
  Consistent PDM-wide sloppiness; changing it would silently rebalance the whole chain.
- **[medium, not fixed - ambiguous]** 31251 option A ("Contact the governor of Egypt") is not
  gated on `EGY = { exists = yes }`. If Egypt has been annexed the option is a no-op and TUR never
  receives 31254/31255 - a soft dead end rather than a loop. Adding `exists` to the trigger would
  also remove option B ("handle this internally"), which should stay available; the right fix is a
  new `EGY = { exists = yes }` arm plus fallback text, i.e. content work, not a mechanical repair.
- **[low] 2358** - 31257 is a hard rail: `year = 1827` + mtth 1 day, so Greece is released and
  war declared on schedule even if GRE already exists (released by rebels) or TUR is mid-war.
  `NOT = { truce_with = GRE }` is the only brake. Historically defensible, deliberately scripted.
- **[low] 2416** - 31257 makes *every* European GP `leave_alliance = TUR` unconditionally.
  Harsh, but it is the diplomatic isolation the chain is modelling.
- **[low] 2938** - 31268 is a repeating province event with no `fire_only_once`, so it fires once
  per province of a flashpoint state. Intended (it is a tension suppressor), just noisy.

### Year windows and cross-chain interaction

Ordering from the 1821.9.1 bookmark is consistent, and nothing here is unreachable:
31250/31256 (1821, day 1) -> 31251 (islands, ungated) -> 31257 (1827) sets `GRE` flag `legitimacy`
-> 31264/31265 (`legitimacy` required) set `greek_question` -> **RUSTurkishWarGVG 1001400**
(1828-1833, needs `greek_question` or GRE existing) -> 1001401 sets `adrianople_treaty` and
`london_conference_1832_held`, which is the off switch for 31251/31256/31264/31265/31266/31267/31268
and the on switch for **GREKingdomGVG 1000500** (1830+). **TURAuspiciousGVG 1000700** (1826-1832)
is flag-independent and does not collide. Egypt's 1805 vassalage carries 31252/31253/31259-31263,
and `promised_egyptian_levant` (31262 only) correctly gates 31266/31269 - the Egyptian retaliation
arm is simply dead when TUR picks 31259 option B, which is the point of the branch.

- **[low]** 31267 clears `greek_question` on every country, including a RUS that got it from
  1001400. 1001400 cannot re-fire (`rus_turkish_ultimatum_1828` is never cleared), so this is safe.
- **[low]** 31251 has no year gate; without the Adrianople chain it can still fire in the 1890s.

### Rest of the file, and TURFlavor.txt

- **[low] 79** - 90025 option B ("Tunisia is part of the Empire!") still runs `release_vassal = TUN`
  and only then grants a `make_puppet` CB. Vanilla PDM idiom ("they leave anyway"), not a bug.
- **[low] 508-1520** - the 90029-90033 independence events carry no year gate and a 120-month mtth,
  so Bulgaria/Bosnia/Iraq/Crete can go autonomous in the 1820s. Gated on militancy 4 and
  `state_n_government` / `revolution_n_counterrevolution`, so it is improbable rather than wrong.
- **[low] 4126** - 98640 `any_core = { OR = { exists = yes exists = no } }` is a tautology; the
  surrounding `NOT = { region ... }` NOR lists are correct.
- **[low]** 90023, 90027-90035 are all reachable (`decisions/Ottoman_Dec.txt`, `AUSFlavor.txt`);
  every flag and event modifier referenced in the file is set somewhere and read somewhere
  (`balkans_call_for_help` is consumed by `common/cb_types.txt`).
- **TURFlavor.txt (31100, 31101)** - clean. Both are `fire_only_once`, both check `owns` for the
  province they describe (865 Canakkale, 926 Baghdad), 31101's multi-statement `NOT` is the
  intended NOR ("before 1910, unaligned"), and `EVTNAME33005`/`EVTDESC33005` on 31101 is the
  deliberate shared key with the German Berlin-Baghdad event that sets it up.
