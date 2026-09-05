# Legacy logic audit - `CoE_RoI_R/events/SPAFlavor.txt`

Line-by-line review of the 41 Spanish events in this file (37700-37763, 97150-97166): the
Trienio Liberal / 1823 French intervention, the Carlist-Christino civil-war machinery, the
Glorious Revolution succession chain, the Spanish-American War treaties and the Chincha
Islands colonial chain. The mechanical audits (modcheck, refcheck, audit_events,
owner_scope, cwtools) were at baseline before this pass, so everything below is a semantic
defect a script cannot see. Line numbers are pre-fix. **[FIXED]** entries were applied in
this commit; the rest are proposals left for the maintainers.

## Fixed

- **376,409 (37708) - [high]** - The event commented `#Madoz's Deamortisation` is in fact
  the **Guardia Civil** event: its window is 1842-1845 (the corps was founded in 1844) and
  its options move officers/soldiers against artisans/craftsmen. But it displayed
  `EVTNAME37707`/`EVTDESC37707`, i.e. *"Madoz's Desamortisation ... In 1855, needing cash
  for the state..."* - which is event 37707's own text, already used by 37707 two blocks
  earlier. `EVTNAME37708` = "La Guardia Civil" and `EVTDESC37708` exist in `text.csv` and
  were unreachable. **Fix:** point at `EVTNAME37708`/`EVTDESC37708` and correct the file
  comment. (The `la_guardia_civil` modifier itself comes from
  `decisions/SPA.txt:establish_la_guardia_civil`; the event is pure flavour, and 37710
  already does `remove_country_modifier = la_guardia_civil`.)
- **399,404 (37708) - [medium]** - The same event's MTTH modifiers test `year = 1855` /
  `year = 1856`, outside its own 1842-1845 window, so the "gets likelier" ramp is dead and
  the event sits at a flat 5-month MTTH. Copy-paste from 37707. **Fix:** 1843 / 1844.
- **163,169 (37702) - [medium]** - The Cuban unrest event fires 1851-1884 (`year = 1851`,
  `NOT = { year = 1885 }`) but its two MTTH modifiers require `year = 1886` / `1887`; both
  are unreachable. **Fix:** 1852 / 1853, matching every other event in the file.
- **3165 (37740) - [high]** - "The American Demand" (fired by
  `decisions/ColonialSpain_Dec.txt:135`, the treaty the USA offers **while it is winning**)
  showed `EVTDESC37750`, the text of the *post-defeat* Treaty of Paris: *"We have lost the
  war with the Americans, and Cuba has been wrested from us"*. Spain was told it had
  already lost Cuba while it still owned it, and the correct `EVTDESC37740` (*"We are
  losing the war with $FROMCOUNTRY$..."*, present in `00_PDM_events.csv`) went unused.
  **Fix:** `desc = "EVTDESC37740"`.
- **787-790, 824 (37711) - [medium]** - The Carlist-victory option sets
  `christino_provinces = 5` (matching the five provinces it stamps with
  `christino_sympathies`) and *then* calls `country_event = 37710`, whose first effects are
  `set_variable christino_provinces = 0` and `carlist_provinces = 0`. The counter that
  drives 37718/37719 and the loyalist comeback was therefore reset to 0 while five
  provinces carried the modifier, so it under-reported by five for the rest of the game.
  **Fix:** move the `set_variable` after the nested event call.
- **1108-1120 (37743) - [medium]** - Carlist Propaganda's trigger requires
  `NOT = { reactionary = 30 }`, yet three MTTH modifiers apply `factor = 0.8` at
  `reactionary = 30 / 40 / 50`. They can never fire. **Fix:** removed (behaviour
  unchanged); the sister event 37714, whose trigger admits `reactionary = 30`, keeps its
  copies - which is where the block was copied from.
- **3903 (97151) - [medium]** - Peru apologises for Talambo, Spain answers by declaring war
  (`war = { ... make_puppet }`) - and pays **no infamy at all**, while the same aggression
  in 97152, against a Peru that *refused* to apologise, costs `badboy = 2`. Attacking the
  side that climbed down was the cheaper option. **Fix:** `badboy = 2` in 97151 too.
- **4443-4446 (37762) - [medium]** - France's "Ferdinand will have to deal with his own
  parliament" option rewards the liberal powers with +15 relations through
  `OR = { NOT = { OR = { absolute_monarchy... } } NOT = { OR = { prussian_constitutionalism... } } }`.
  That OR is a tautology: an absolute monarchy satisfies the second branch and everything
  else satisfies the first, so *every* civilised European country - Russia, Austria and
  Prussia included - thanked France for refusing to crush the Spanish liberals.
  **Fix:** `AND`, i.e. "neither an absolute monarchy nor a Prussian constitutionalist",
  the mirror of option A's reactionary bloc.

## Proposals (not applied)

- **831-865 (37712) - [medium]** - "The Carlists Defeated!" needs only
  `has_country_flag = carlist_war` and `NOT = { num_of_revolts = 1 }` at a 1-month MTTH.
  37711 sets that flag without spawning any rebel army - the Carlists come later, out of
  the militancy and `carlist_sympathies` it seeds - so on most runs the civil war is
  declared over about a month after it starts, before a single Carlist stack exists, which
  wipes `carlist_sympathies` from every province and zeroes `carlist_provinces`. Suggest
  gating on a minimum duration (a war-start flag plus a 12-24 month MTTH) or on
  `NOT = { has_country_modifier = national_confusion }`.
- **840 (37712) - [low]** - `remove_accepted_culture = basque` is a no-op: SPA's history
  file has only `primary_culture = spanish` and nothing in this file grants basque as an
  accepted culture, so the "we take the fueros back" beat never lands.
- **868-900 (37713) - [low]** - "Return of the Carlists" does not exclude an ongoing
  `carlist_war`; it can re-seed sympathies in the middle of the war it is meant to precede.
  The province events have a 0.2 MTTH factor for that case; this one has none.
- **2210+ (37720) - [low]** - The Glorious Revolution's Amadeo option fires
  `FRA = { country_event = 37721 }`. 37721's text is France congratulating itself for
  making Leopold of Hohenzollern turn the throne down, which reads correctly on the Savoy
  branch - but its option string, hardcoded as *"A German prince on the Spanish throne?
  Outrageous!"*, describes the branch that was **not** taken. A dedicated key (or
  "Leopold has withdrawn.") would fit; the -100 relations with the German GP are right
  either way.
- **3385 (37750) - [low]** - The Treaty of Paris (USA already victorious) reuses
  `title = "EVTNAME37740"`; `EVTNAME37750` exists in no csv. Harmless - both read "The
  American Demand" - but a distinct title would tell the two treaties apart.
- **3450-3465 (37750) - [medium]** - Its second option, *"We refuse! Let them fight for
  it!"*, is a dead branch: the decision that fires it requires `war = no`, a truce, and
  Cuba already independent, so there is no war left to refuse. It costs 10 war exhaustion,
  buys Spain nothing, and sends the USA to 37742, whose "lay claim to their colonies"
  option hands the USA cores it cannot act on until the truce lapses. `ai_chance = 5` keeps
  the AI out of it; a human can still take it. Suggest dropping it or turning it into a
  prestige-only protest.
- **3170, 3266 (37740/37741) - [low]** - `money = 1000000` to Spain and `money = -1000000`
  from the USA is the $20m Cuban indemnity, but 1,000,000 is an order of magnitude above a
  plausible 1898 treasury in this mod's economy; 100,000-200,000 would still be a fortune.
- **3700-3760 (37745) - [medium]** - Both options of the Moroccan Border Dispute run the
  *same* `FRA = { diplomatic_influence -100, relation -100, leave_alliance, add_to_sphere
  CB }` block, so "This must be resolved peacefully" wrecks the Franco-Moroccan
  relationship exactly as hard as the option that declares war on Morocco. If the intent is
  "Spain outbids France either way", the text should say so; otherwise the peaceful branch
  should leave France alone, or take only the influence and not the CB.
- **3172, 3220, 3418 (37740/37742/37750) - [low]** - `region = SPA_1459` and
  `region = SPA_1463` name regions that are **commented out** in `map/region.txt`; their
  provinces were folded into `SPA_1455`, which the same `OR` already lists. Dead but
  harmless - worth deleting so nobody re-adds the regions expecting them to matter.
- **97150-97166 - [low]** - The Chincha chain keys off `resisting_spanish_rule` /
  `restore_the_spanish_empire` from 1863 and shares no flag or id with tonight's
  `SPAAyacuchoGVG` (1002100-1002102, 1824-1833, `ayacucho_*` / `recognised_by_spain`) or
  with `PORMiguelistGVG`; no collision. Note only that a Spain which took the Ayacucho
  recognition deal in 1824 can still raise `restore_the_spanish_empire` in 1863 and demand
  Peru's submission. Historically that is the war of 1864-66, so it is defensible, but the
  recognition event promises a permanent settlement; a line acknowledging the reversal, or
  a `NOT = { has_country_flag = ayacucho_settled }` gate on the second option of
  97151/97152, would tie the two chains together.
- **4346-4360 (37761) - [low]** - "Appeal to the Holy Alliance" has no lower year bound and
  runs to 1835 on a 24-month MTTH (0.5 at 1823, 0.5 again at 1825). From the 1821.9 start
  it will normally fire in 1822-1824, but a Spain that keeps `hms_government` can still
  summon the Hundred Thousand Sons of Saint Louis in 1835. A `NOT = { year = 1828 }` cap
  would match the Trienio.
