# Russo-Turkish War 1828-29 and the Treaty of Adrianople

## What already exists

- `events/Ottoman_Event.txt:31264-31269` - the Greek Question. 31265 (RUS) offers
  "Call up the army!", which grants a `cut_down_to_size` CB and declares war on TUR.
  It fires on GRE's `legitimacy` flag, i.e. c. 1821-22, not 1828, and if Russia
  declines there is no second chance.
- `decisions/RUS.txt:treaty_of_adrianople` - the peace. Gated on `war_with = TUR`,
  `has_country_flag = greek_question` and Ottoman war exhaustion/occupation; it sets
  `adrianople_treaty` + `black_sea_claimed`, hands MOL/WAL influence and alliances and
  fires `RUSFlavor.txt:95074/95075` (the Ottoman capitulation).
- `history/countries/RUS - Russia.txt` sets `adrianople_treaty` for the 1836 bookmark.
- MOL, WAL and SER exist from 1821 as Ottoman vassals (`history/diplomacy/PuppetStates.txt`).

## What is missing

Nothing takes Russia to war in 1828 itself. Akkerman, Navarino and the Tsar's
ultimatum of April 1828 are unrepresented, and a Russia that answered the Greek
Question diplomatically can never reach the Adrianople decision. There is also no
Ottoman-side acknowledgement of the peace and no great-power reaction to a Russian
march on Constantinople.

## Design (events/RUSTurkishWarGVG.txt, ids 1001400-1001499)

All events use per-country flag guards, not `fire_only_once` (engine-wide).

1. **1001400 The Tsar's Ultimatum** - RUS, `year = 1828`, before 1833, TUR exists,
   Greek question still open (GRE exists or Russia already holds `greek_question`),
   not at war/truce/alliance with TUR, `adrianople_treaty` not yet set, guard flag
   `rus_turkish_ultimatum_1828`.
   - A (ai 75): declare war. `casus_belli` + `war = { target = TUR attacker_goal =
     { casus_belli = cut_down_to_size } call_ally = yes }`, sets `greek_question` so
     the existing Adrianople decision becomes reachable, and `russo_turkish_war_1828`.
   - B (ai 25): press the Porte diplomatically - influence and relations against TUR,
     small prestige, flag `rus_pressed_porte_1828`.

2. **1001401 The Treaty of Adrianople** - RUS, `war_with = TUR`,
   `has_country_flag = russo_turkish_war_1828`, `war_score = 20`, 1829-1833, guard
   flag `adrianople_offer_made`, and only while `adrianople_treaty` is unset (so it
   never competes with the PDM decision).
   - A (ai 80): moderate peace. `end_war = TUR`, prestige, sets `adrianople_treaty`
     and `black_sea_claimed` (which closes the decision), Danubian principalities and
     Serbia get Russian influence and relations, Greek independence is recognised -
     if GRE exists and no London conference is under way, `london_conference_1832_held`
     is set so `GREKingdomGVG` 1000500 can run - and TUR gets 1001403.
   - B (ai 20): march on Constantinople. War continues, `badboy = 4`, European great
     powers lose relations and get 1001402.

3. **1001402 The Powers and the Straits** - `is_triggered_only`, other European GPs.
   Protest (relations with RUS down further) or stand with the Porte (relations and
   influence to TUR). No CB is granted; `status_quo` and `humiliate` both carry
   `always = no` in `common/cb_types.txt`.

4. **1001403 The Peace of Adrianople (TUR)** - `is_triggered_only` mirror:
   prestige loss, relations with Russia restored, war exhaustion eased, flag
   `adrianople_signed`.

Pictures reuse existing mod art (`turkmenchay_treaty`, `caucasian_war`,
`greatpowers`, `ottoman`). No new province ids or tags are referenced.
