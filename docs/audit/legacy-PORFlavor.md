# Legacy audit: events/PORFlavor.txt (97000-97031, 1000300)

Line-by-line review, 2026-09-06. Line numbers are post-fix. Mechanical audits
(modcheck braces/provinces/tags, refcheck, audit_events, cwtools) were at
baseline before and after; every fix below is applied in place unless marked
"not fixed".

Chain map (1821 start, UPB owns Portugal *and* Brazil):
97021 (draft constitution, fires day 1) -> either `colonial_brazil` ->
97022 -> 97023 (Ipiranga, releases BRZ + war) or `release_vassal = BRZ`
straight away; 97024 then flips UPB -> POR once BRZ holds Rio (2447), unless
the `unite_portugal_brazil` decision (decisions/POR.txt:395) has set
`portugal_brazil_united`. 97026/97028/97029 handle a vassal Brazil; 97030
(death of John VI, 1825) hands off to PORMiguelistGVG 1001000-1001003 via
`por_charter_granted` / `miguelist_usurpation`; 97031 is the foreign
intervention. BRZRegencyGVG (1001900-1001903) is BRZ-side only and shares no
flag with this file - no interaction problems found.

## Fixed

- 2011 97031 -- **wrong recipient window.** The trigger tested
  `POR = { OR = { government = absolute_monarchy... } }` with no `exists = yes`.
  At the 1821 start POR is a dead tag (UPB holds Portugal) and the engine still
  reads its history government, so *every* European GP could fire this from
  1821.9.1: -50000 money, +50 influence on a nonexistent Portugal, and
  `por_intervention_considered` set, permanently locking out the real
  intervention during the Liberal Wars. Added `exists = yes` inside the POR
  scope and a `year = 1826` floor (the Miguelist usurpation cannot precede
  97030, which needs `year = 1825`). [high]
- 2025 97031 -- four stray `military_industry = -2 / -5 / -2 / -5` lines in the
  support option. `military_industry` is a *technology* (technologies/
  industry_tech.txt), not a country effect, and a negative tech grant is
  meaningless. Removed. [high]
- 1472 97029 -- **wrong country changes tag.** Option A ended with a bare
  `country_event = 97024`, and 97024 does `all_core = { remove_core = UPB }` +
  `change_tag = POR`. 97028 explicitly allows `vassal_of = IBR`, so an Iberian
  overlord that let Brazil go would be turned into Portugal. Wrapped in
  `random_owned = { limit = { owner = { tag = UPB } } owner = { ... } }`. [high]
- 1866 97978 -- **inverted casus belli.** `POR = { add_casus_belli = { target =
  GAZ ... } }` gives *GAZ* a protectorate CB against Portugal (add_casus_belli
  grants the CB to the target, against the scoped country), the exact opposite
  of the option text "I've been waiting for this for a while!". Replaced with a
  root-scope `casus_belli = { target = GAZ ... }`. [high]
- 1858 97978 -- `GAZ = { exists = yes ... }` puts a trigger inside an effect
  block; the trigger already requires GAZ to exist. Removed. [medium]
- 561 97008 -- `region = ENG_2039` does not exist: map/region.txt:1007 has it
  commented out, merged into ENG_2044 (Tanganyika). Half of the Zanzibar
  purchase silently transferred nothing. Replaced with the four province ids
  the dead region held (2038-2041). [medium]
- 714 97011 -- same problem with `region = ENG_2016` (region.txt:1093,
  commented out, merged into ENG_2014 which is already listed one line above).
  Removed as redundant. [medium]
- 1521 1000300 -- `desc = "EVTNAME1000300"` pointed at the *title* key, so the
  new-capital event showed its own headline as its body text. EVTDESC1000300
  exists (localisation/newCE.csv:30). Fixed. [medium]
- 1901 / 1946 97030 -- `alliance = BRZ`, `relation = { who = BRZ }`,
  `leave_alliance = BRZ` and `BRZ = { country_event = 46315 }` all run
  unguarded, but 97030 fires for UPB as well as POR, and on the
  `portugal_brazil_united` branch BRZ never exists. Wrapped each in
  `random_country = { limit = { tag = BRZ exists = yes } ... }` using `THIS`
  (the event root) for the reciprocal side. [medium]
- 1728/1735/1788/1794 97039 -- `free_peoples` requires both `country` and
  `state_province_id`, `release_puppet` requires `country` (wiki
  list-of-effects.md:291). All four CB grants were missing them, so the GP
  backlash against a transatlantic Iberia produced no usable CB. Added
  `country = BRZ` (+ `state_province_id = 2447`, Rio). [medium]

## Not fixed (recorded)

- 1737/1796 97039 -- the second CB in each option targets `IBR`, which the
  trigger requires *not* to exist and which this event never forms; it is a
  no-op unless the player later takes `create_iberia_UPB`. Harmless, and
  removing it would break that intended follow-up. [low]
- 1348 97028 -- `mean_time_to_happen = { months = 480 }` (40 years) before
  modifiers for a vassal Brazil pushing for independence. The 0.2 modifiers
  bring it to ~8 years, so it works, but the base is an outlier for this file.
  [low]
- 248-262 97003 / 824+ 97020 -- both options re-list the same 23
  `remove_country_modifier` ruling-personality lines; a duplicated episode of
  bookkeeping rather than a bug. [low]
- 1546+ 1000300, decisions/POR.txt:483 -- `scaled_militancy = { factor = n }`
  with no `ideology` / `issue`. It is an established (if dubious) pattern in
  this mod, not local to PORFlavor; left alone deliberately. [low]
- 1519 1000300 -- option C ("old capital of Estado de Brazil") has no
  `ai_chance`, so it defaults to weight 1 against 75/25 - effectively
  player-only. Probably intended. Its option text is also phrased as a
  question. [low]
- localisation/newCE.csv:30 -- EVTDESC1000300 ends `x;` instead of `;x`
  (terminator in the wrong column). Not touched here: csv edits go through
  `modcheck loc-add`, and this is one row of a wider newCE.csv encoding issue.
  [low]
- 1844 97978 -- inline English title/desc rather than loc keys, and "cranage"
  is a typo for "carnage". Cosmetic. [low]
- 1148 97023 -- both options are byte-identical apart from
  `change_tag_no_core_switch = BRZ`; that is the deliberate "play as Brazil"
  offer, not a duplicated branch. No fix.

## Checked and clean

- FROM hops: 97010 (from decisions/POR.txt:185, THIS=POR, FROM=demander) ->
  97011 / 97012 both resolve `FROM` to the right side, and `secede_province =
  THIS` inside `FROM = { any_owned = { ... } }` correctly credits the event
  root. Same for 97008/97009 (money out of THIS, provinces out of FROM).
- Owner scope: 97021/97023/97039 restrict province effects with
  `limit = { continent = south_america }` and reach Uruguayan land through
  `URU = { all_core = { ... } }`, so nothing lands on the wrong half of the
  union (see docs/audit/owner-scope.md).
- Every province id in the file (517, 518, 527, 1999-2011, 2051-2581, 2134,
  2436, 2447) exists in map/definition.csv.
- Multi-statement `NOT` blocks (97000, 97015, 97024, 97028, 97029, 97030) all
  read correctly as NOR.
- Flag ledger: `maria_de_fonte_revolution`, `colonial_brazil`,
  `dom_pedro_refuses`, `regicide_king_carlos`, `iberian_destiny`,
  `has_chosen_capital`, `por_charter_granted`, `miguelist_usurpation` are each
  set and consumed; no branch requires a flag only one sibling option sets.
