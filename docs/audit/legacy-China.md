# Legacy audit: `events/China.txt` + `events/CHIFlavor.txt`

*2026-09-06. Line-by-line read of the Qing/China chain: westernisation 90900-90904, the Opium
War lead-in (1316080/1316081/131709), the unequal-treaty payoffs (1316082-1316097), the Second
Opium War (1316181/1316182), Tibet (131711-131714) and the Xinhai/New Army/warlord hand-off
(164599, 164600, 131715). Cross-checked against `events/CHIOpiumGVG.txt`, `events/Taiping.txt`,
`decisions/China.txt`, `decisions/ENG.txt`, `decisions/UncivFlavor.txt`, `common/on_actions.txt`
and `common/cb_types.txt`. Mechanical audits (modcheck, refcheck, audit_events, cwtools) were at
baseline before and after.*

## Findings

`file line id - problem - fix`

### [high]

None. Every wrong-recipient candidate in the chain resolved to correct or to vanilla behaviour on
inspection; see "Verified, not defects" below for the three that look wrong and are not.

### [medium]

- `events/China.txt:318-345` 90903 - the "province breaks away instead of westernising" event
  hardcodes **CHI** as the overlord in three places (`leave_alliance = CHI`, `substate_of = CHI`,
  `CHI = { country_event = 90904 }`). From an 1821 start the overlord is **QNG**; CHI only exists
  after the Xinhai hand-off in 164599. The fix would be `FROM` in all three - but nothing fires
  90903 (marked `#Unused? -Koro`; the only callers of this file are `on_civilize` and
  `decisions/UncivFlavor.txt:55`, both of which fire 90900), so `FROM` is undefined and the branch
  is unreachable. **Not changed**: rehooking it is a design decision, not a repair. 90902 and
  90904 are orphaned with it (90902 is only ever fired by 90903).
- `events/CHIFlavor.txt:2381-2434` 1316182 - the British reaction to the Arrow Incident has three
  `random_owned` branches. Branch 2 (`THIS = { NOT = { nationalism_n_imperialism = 1 } }`) and
  branch 3 (`THIS = { nationalism_n_imperialism = 1 }`) are identical in effect: same
  `demand_concession_casus_belli`, same `state_province_id = 1496`, same `call_ally`. The tech
  test therefore does nothing; one branch was presumably meant to escalate (an `acquire_any_state`
  or `cut_down_to_size` goal, as branch 1 uses). Not fixed - which branch was meant to differ is a
  guess.
- `events/CHIFlavor.txt:1354-1425` 1316081 with `1307-1348` 1316080 - one-shot dead end. 1316080 is
  `fire_only_once` and is the only source of `foreign_smugglers` in China; 1316081 sets the global
  flag `kowloon_incident` in `immediate` and its option A wipes the smugglers from every province
  (`any_owned = { remove_province_modifier = foreign_smugglers }`) *before* Britain answers. If ENG
  then takes 131709 option B ("Leave the Chinese alone"), the First Opium War can never be offered
  again: 1316081's trigger needs a `foreign_smugglers` province that no longer exists, and the flag
  blocks a re-fire anyway. Suggested fix: move the removal into the war branch of 131709, or clear
  `kowloon_incident` in 131709 option B. Not applied (changes the event's fire-once contract).
- `events/CHIFlavor.txt:2612-2770` 131715 "The New Army" - no year floor. QNG starts 1821 with
  `unciv_light_armament = gunpowder_weapons` (`history/countries/QNG.txt`), so the uncivilised
  branch of the trigger only needs `civilization_progress = 0.20` - the same bar as the
  `civilize_your_nation_china` decision - with `months = 30`. `the_new_army` can therefore be set
  in the 1830s-40s, and it is the sole gate on the Xinhai Revolution (164599, `months = 12`) and
  the Tongmenghui (164600): a 1911 episode can resolve before 1850. Suggested fix: a `year = 1890`
  floor on 131715, or on 164599/164600. Not applied - the floor value is a balance call, and this
  is the file's pacing shape throughout (the warlord events are gated only by
  `warlord_era_has_begun`).
- `events/CHIFlavor.txt:932` 1316175 - duplicated episode. 1316175 and 1316180 are both titled
  "Empire of the Great Qing", both `picture = "qing_emperor"`, both about snubbing the sphere
  leader; 1316175 even borrows the other's loc key (`title = "EVTNAME1316180"`; no
  `EVTNAME1316175` exists in any csv). They cannot fire together - 1316175 needs the sphere leader
  at relation < -100 and 1316180 at >= -100 - so this is cosmetic, but the player meets the same
  headline twice. Left as-is; fixing it means writing new loc, not editing script.

### [low]

- `events/CHIFlavor.txt:28` 164550 - `relation = { who = UYG value = -400 }`; the engine range is
  +/-200. **Fixed** to -200.
- `events/CHIFlavor.txt:1579` 1316083 and `:1997` 1316091 - `relation = { who = FROM value = 300 }`
  after imposing an unequal treaty: out of range, and it reads oddly against the option text.
  **Fixed** to 200 (the clamp value, so in-game behaviour is unchanged).
- `events/CHIFlavor.txt:2205` 1316095 - `3250 = { secede_province = FROM }` (Guangzhou Wan) with no
  ownership guard; the province is QNG-owned in 1821 but the option pays 250000 and +50 relations
  even if China has already lost it. The firing decision (`decisions/China.txt:1385`) is the only
  guard.
- `events/CHIFlavor.txt:1336` 1316080 - option name is `EVTOPTA13050`, a key borrowed from vanilla
  event 13050 ("It is not our place to intervene"). Reads acceptably; a dedicated `EVTOPTA1316080`
  would be cleaner. Same class: `events/China.txt:264` 90901 option B uses `EVTOPTB90100`
  ("Never!") - the text fits, the id does not.
- `events/CHIFlavor.txt:1308-1310` 1316080 - `title`/`desc` are raw English strings rather than loc
  keys, so the event is untranslatable and cannot be edited from a csv.
- `common/on_actions.txt:121-122` - `on_civilize` lists `100 = 90900` (China) and `100 = 90910`
  (RotW) at equal weight. Only one entry is drawn; if the roll picks 90910 for a Chinese tag its
  trigger fails and the westernisation clean-up in 90900 is skipped. The decision path
  (`UncivFlavor.txt:55`) fires 90900 directly, so this only bites non-decision westernisation.
  Not this audit's file.

## Verified, not defects

- **The Opium GVG interlock is consistent.** `1001500` (QNG, 1821-1827) -> `1001501` (1830-1840,
  requires a `qing_opium_*` flag) -> `1316081` (`year = 1835`) is a well-ordered ladder, and
  1316081's MTTH really does read all four flags the GVG file sets: `qing_opium_prohibition`
  (x0.75), `qing_opium_crackdown` (x0.75), `qing_opium_legalised` (x3 - legalisation defuses the
  war) and `ENG = { has_country_flag = eng_canton_lobby }` (x0.8). 1001502's `relation = FROM` hops
  are correct (FROM = QNG).
- **1316090 / 1316091 `any_owned = { limit = { is_core = CHI ... } secede_province = FROM }`** run
  in the *victor's* scope and hand land *to* China. That looks like the owner-scope defect class
  (`docs/audit/owner-scope.md`) but is not: the `NOT` list excludes exactly the treaty ports,
  Taiwan and Hainan, so this is the give-back clause - the winner returns occupied Chinese core
  land minus its concessions. Both events do it identically.
- **All 21 multi-statement `NOT` blocks in the two files are intended NORs** (checked
  programmatically): 1645091's `NOT = { has_country_flag = mandate year = 1860 }`, 1316181's
  five-way `NOT`, the treaty province lists at 1924/2091 and the warlord `is_core` lists all want
  "none of these", which is what NOR gives.
- **The Taiping hand-off is intact from 1821.** `history/countries/QNG.txt` does set
  `taiping_has_happened`, `hong` and `yang`, but inside its `1861.1.1` block, so the 1821 start
  leaves `NOT = { has_global_flag = taiping_has_happened }` in Taiping.txt 160001 satisfiable and
  does not pre-arm 1645092 (Mandate lost) or 1316181 (Arrow Incident). QNG.txt does carry two
  `1861.1.1` blocks (lines 75 and 78) - harmless, and not this file.
- **Tonight's China.txt fixes hold up.** In 90900 `substate_of = THIS` is right (THIS is the event
  root, so the `NOT = { tag = THIS }` filter is meaningful and the substates of the westernising
  power are the recipients); in 90901 `FROM = { inherit = THIS }` inherits the substate into the
  overlord and `leave_alliance = FROM` in option B targets the overlord. Consistent with 90902.
- `release_vassal = THIS` in the substate's own scope (90901/90902/90903) is copied verbatim from
  vanilla `events/China.txt:87,108,138`; left alone rather than "corrected" to
  `FROM = { release_vassal = THIS }`.
- 164550's `release = UYG` has cores to work with (9 provinces carry UYG cores) and UYG is a
  registered tag with a history file, so the Khoja Rebellion war is not a no-op.
- 164599 removes QNG/TPG cores before `change_tag = CHI` and releases KOR/TIB/MGL from the right
  scopes; the province ids it names (1587, 1465, 1616, 1468, 1469) all exist in
  `map/definition.csv`.

## Changes applied

`events/CHIFlavor.txt` only: three out-of-range relation values clamped to the engine maximum
(lines 28, 1579, 1997). No behavioural change; everything else above is reported, not edited.
