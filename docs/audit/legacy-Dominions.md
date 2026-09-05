# Line-by-line review: `events/BritishDominions.txt` + `events/CANFlavor.txt`

*2026-09-06. Dominion creation (D-tags NEW/AST/NZL/SAF/RHO/LSK/CAN/QUE/MRU/COL/RPL/MTC),
Canada 1837-1867, Rupert's Land, British Columbia, the CNR chain and the Metis events.
Mechanical audits (`modcheck`, `refcheck`, `audit_events`, `cwtools_check`) were at baseline
before and after; everything below came from reading the script.*

## Verified, no defect

- **The old "Canadian statehood popup" collision is closed.** `decisions/ACW.txt`
  `apply_for_USA_statehood` (TEX/DES/CAL/LSK) and `decisions/CAN.txt`
  `apply_for_USA_statehood2` (NEW/MRU/COL/MTC/RPL/CAN) both fire `USA = { country_event = 16400 }`,
  and 16400 (`events/ACW.txt:2547`) carries `allow_multiple_instances = yes`. Two applicants in
  the same tick queue two popups instead of one swallowing the other. Each applicant also gates
  itself with its own `usstatehood_we_have_applied` flag, so nobody applies twice.
- **Dominion release paths still pick a legal ruling party** after tonight's move of the party
  start dates to 1800. Every releasable tag (CAN QUE MRU COL NEW AST NZL SAF RHO LSK RPL MTC AOT)
  has a `ruling_party` in `history/countries/` that is defined in its `common/countries/*.txt`
  and is active at 1821 (4 parties live per file at the start date). `release_vassal` cannot land
  on an undefined or not-yet-started party.
- Sub-culture handling is correct throughout: `has_pop_religion = anglo_canadian` (44305, 44301,
  44302, 44322, 44350) is the mod's convention, while `metis`, `cree`, `french_canadian` and
  `native_american_minor` are real cultures in `common/cultures.txt`. Nothing to convert.
- Multi-statement `NOT` blocks (44305, 44306, 44310, 44302) all read correctly as NOR.
- `THIS` inside nested scopes (44337's `FROM = { any_owned = { limit = { is_core = THIS } } }`)
  resolves to the event root, which is what those blocks want.

## Fixed

| file | line | id | problem | fix |
|---|---|---|---|---|
| BritishDominions.txt | 61, 179, 306, 423, 713, 832, 1321, 1364, 1446, 1562 | 44330/32/33/34/40/41 | **[high]** every dominion event triggers on `tag = ENG` **or** `tag = ENL`, but the release option hardcodes `TAG = { all_core = { remove_core = ENG } }`. Played as ENL the cores are never released, so `release_vassal` hands the dominion land the metropole still cores - permanent reconquest CBs and a broken vassal. | `remove_core = THIS` (the pattern 44333's NZL block already used) |
| CANFlavor.txt | 366, 495, 585, 718, 804, 933, 1021, 1150 | 44315/16/17/18 | **[high]** `CAN = { all_core = { change_controller = ENG remove_core = ENG } }` fires `change_controller` on *every* core of the new dominion worldwide, including provinces owned by the USA or a third party - a free, warless occupation flip - and again hardcodes ENG under an ENG/ENL trigger. | split into `any_owned = { limit = { is_core = CAN } change_controller = THIS }` + `CAN = { all_core = { remove_core = THIS } }`, so only our own land changes hands |
| CANFlavor.txt | 112 | 44306 | **[high]** Lord Durham's Report trigger ends `NOT = { ... any_owned_province = { ... NOT = { controlled_by = ENG } } }`. As ENL every owned province fails `controlled_by = ENG`, the inner NOT is always true and the event can never fire - the whole 1837-1867 Canadian chain is dead for ENL. | `controlled_by = THIS` |
| CANFlavor.txt | 170, 281-284 | 44306, 44310 | **[medium]** `USA = { relation = { who = ENG ... } leave_alliance = ENG casus_belli = { target = ENG } }` - as ENL the USA sours on, breaks with and gains a CB against a country that is not the one that refused. | `who` / `target` / `leave_alliance` = `THIS` |
| BritishDominions.txt | 1342 | 44340 | **[medium]** the "It shall remain a $COUNTRY_ADJ$ colony" option ran `USA_1 = { remove_core = THIS }` - the *keep it* branch silently stripped our own Alaska cores, the opposite of the option text (the other three options remove them deliberately, before releasing or seceding). | dropped the `USA_1` block; the militancy hit stays |
| BritishDominions.txt | 459 | 44333 | **[medium]** the New Zealand event was the only dominion event with no `tag = ENG / ENL` gate and no `exists = yes`; `NZL = { is_culture_group = THIS }` let any surviving British-culture-group power that owns an NZL core release New Zealand as *its* vassal and strip AOT's cores. | added the `OR = { tag = ENG tag = ENL }` + `exists = yes` header the other five use |
| BritishDominions.txt | 1435 | 44341 | **[medium]** Rhodesia's trigger is `year = 1924` but its "late" MTTH modifier is `year = 1910`, i.e. true from the first day the event can fire - the intended slow-then-fast curve is a flat halving. | `year = 1930` (mirrors NEW 1907/1912, AST 1901/1910, NZL 1907/1915, SAF 1909/1920) |
| BritishDominions.txt | 225, 242 | 44331 | **[medium]** the Newfoundland-bankruptcy event has no flag, no `fire_only_once` and a 6-month MTTH, so choosing "We shall prevail" (-20 prestige, +4 consciousness) re-asks every six months for as long as the depression modifier lasts - an unbounded prestige drain on one episode. | option B sets `NEW_will_prevail`; trigger takes `NOT = { has_country_flag = NEW_will_prevail }` |
| CANFlavor.txt | 1420 | 44321 | **[medium]** buying Rupert's Land costs CAN `treasury = -50000`, but the accept option's `ai_chance` only zeroes out if CAN is *already* bankrupt, while the refuse option zeroes out at `money = 50000`. An AI Canada with 5,000 in the bank takes the deal and defaults. | added `modifier = { factor = 0 NOT = { money = 50000 } }` to the accept branch, so both branches use the same affordability test |

## Left alone - recorded

- **[low]** `BritishDominions.txt:1035` (44339, Northwest Territories) fires for `CAN` *or* `ENG`,
  but every `random_owned` limit needs 17/23/43/2596 `owned_by = THIS`. Once CAN exists those are
  Canadian, so the ENG copy of the event quietly does nothing after 1867. Conditional, so it is
  the benign form of the `owner-scope.md` class, not a new high.
- **[low]** `BritishDominions.txt:895` (44335/44336): the "return our overseas cores" request is
  open to any civilised, non-substate vassal, which after civilisation includes **HND**. The
  `ai_chance` guard `factor = 0 / FROM = { is_culture_group = south_asian }` stops the AI handing
  India ENG's cores; a human ENG can still do it. Deliberate, per `owner-scope.md`.
- **[low]** `CANFlavor.txt:1673` (44351) sets `promised_national_railway`, which nothing reads.
  The CNR chain (44355-44357) gates on `build_the_cnr`, set only by the `build_the_cnr` decision
  in `decisions/CAN.txt:323`. Accepting British Columbia therefore promises a railway that the
  promise itself does not unlock. Left as-is because wiring it up would let the event bypass the
  decision's `money = 50000` / `the_iron_horse` gate; noted as the intended follow-up.
- **[low]** `CANFlavor.txt:1614` (44350 option B) sets `british_columbia_confederation`
  permanently, but the fallback release of COL (44318) requires `CAN = { has_country_flag =
  refused_columbia }`, which only CAN can set in 44351. If **ENG** is the one who refuses,
  British Columbia can never become a dominion nor join Canada. A dead branch, but repairing it
  means choosing new content rather than fixing a mistake.
- **[low]** `CANFlavor.txt:1248-1292` (44320): both options strip the same seven regions' cores
  from the metropole, so refusing to sell Rupert's Land still gives up the claim. Consistent
  across the accept/refuse/44322 branches, so it reads as intent rather than a slip.
- **[low]** `BritishDominions.txt:230` (44331) routes through `CleanUp.txt:60130`, whose refuse
  branch sets `does_not_want_to_unify` and clears `crown_from_the_gutter` on Newfoundland -
  unification-chain flags leaking into the dominion path. Harmless today; NEW is in no
  unification chain.
- **[low]** The CNR costs (`-100000`, `-200000`, `-300000` in 44355-44357, on top of the
  decision's `-50000`) are large, but each event gates on not being bankrupt and the payments are
  spread over 12/18/24-month MTTHs; plausible for a post-1870 Canada.
