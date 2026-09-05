# `events/Indochina.txt` + `decisions/ENG.txt` (treaty_of_yandabo) - logic review

*2026-09-06. Line-by-line read of the Anglo-Burmese chain (95670-95679), the Lao rebellion
(95660), the French Cochinchina/Cambodia chains (95639-95650) and the two abandoned treaty
chains (95652-95657). Line numbers are post-fix. Mechanical checks were at baseline before and
after: `modcheck braces/provinces/tags/encoding` clean, `refcheck` 14/0/60/0/127/0/8,
`audit_events` unknown 0 / high 0 / medium 0, cwtools unchanged (the known CW242 rule gap is
still `Indochina.txt:188`).*

## Chain map (recipient / FROM at each hop), for reference

* 95670 BUR (Return of the King) -> 95671 ENG (FROM=BUR) -> agree 95672 BUR (FROM=ENG) /
  refuse 95673 BUR (FROM=ENG) -> back down 95674 ENG (FROM=BUR) / war -> 95675 or 95676 BUR,
  then ENG's `treaty_of_yandabo` decision -> 95677 BUR (FROM=ENG) -> 95678 ENG / 95679 ENG.
  **All FROM hops and all `THIS` uses resolve correctly**; the nested `THIS` in 95672/95675
  (`ASM = { all_core = { add_core = THIS } }`) is the event root BUR, as intended.
* 95639 owner-of-1380 -> 95640 FRA (FROM=DAI) -> 95641 DAI -> 95642 FRA. Correct throughout.
* 95645 CAM -> 95646 FRA -> 95647 DAI / 95649 CAM -> 95648 FRA. Correct throughout.
* `add_casus_belli` in 95650 grants the CB to `target = THIS` (the great power), which is the
  documented direction for that effect - **not** a reversed-CB bug.

## Fixed

| line | id | problem | fix |
|---|---|---|---|
| 355 | 95678 | **[medium]** `title = "EVTNAME95677"` - ENG's `major = yes` Yandabo event displayed the Burmese event's title. `EVTNAME95678` did not exist anywhere (only `EVTDESC95678` did). | title -> `EVTNAME95678`; key added to `PDM_CE.csv` ("The Treaty of Yandabo is Signed"). |
| 389 | 95639 | **[medium]** `title = "EVTNAME95640"` - the trigger event and the French response 95640 shared one title. `EVTNAME95639` did not exist. | title -> `EVTNAME95639`; key added to `00_PDM_events.csv`. |
| 706 | 95647 | **[medium]** `title = "EVTNAME95645"` - the event sent to DAI reused the CAM event's title. `EVTNAME95647` did not exist. | title -> `EVTNAME95647`; key added ("The French Demand for Cambodia"). |
| 378 | 95679 | **[medium]** dead branch: `treaty_of_yandabo` sets `yandabo_treaty` on ENG in its effect and its `potential` forbids re-taking it. If BUR picks 95677 option B ("We will fight on"), ENG is left in the war with the decision permanently greyed out - the treaty can never be offered again. | 95679 (the refusal event, ENG scope) now does `clr_country_flag = yandabo_treaty`, so ENG may re-offer after fighting on. |
| 396 | 95639 | **[medium]** impossible-window inverse: no year gate. The trigger only wants an uncivilised, unspheres owner of 1380 and a non-pacifist FRA with `state_n_government`, so the Cochinchina Campaign (hist. 1857-58) could fire in the 1820s from the 1821 start; the mtth's `berlin_conference` modifier shows late-game intent. | added `year = 1850` to the trigger. |
| 654 | 95645 | **[medium]** option text contradicts effects: "Throw out the **Thai**!" while the trigger requires `DAI = { is_our_vassal = THIS }` and every effect in the option targets DAI (Dai Nam). | text -> "Throw out the Vietnamese! We will risk war." |

## Reported, not changed

| line | id | problem |
|---|---|---|
| 111 | 95671 | **[medium]** option A "Deliver him to the Burmese" (i.e. ENG concedes) applies `diplomatic_influence = { who = FROM value = -50 }` - ENG *loses* 50 influence in Burma for giving in, while the refusal branch only costs relations. The sign looks inverted, but the designer may have meant "we look weak"; left alone as ambiguous. |
| 1024 | 95652 | **[medium]** `title = "EVTNAME95641"` (The French Demand) instead of a `EVTNAME95652`, which does not exist even though `EVTDESC95652` does - same defect class as the three fixed above. Left because 95652/95655 are the known abandoned treaty chains (nothing fires them). |
| 464 | 95640 | **[low]** option B ("continue on the diplomatic path") never clears `cochinchina_campaign`, which 95639 set before firing, so the whole Cochinchina chain is locked out for the rest of the game after one peaceful answer. Probably intended as once-only, but it is a permanent dead end. |
| 520-595 | 95642 | **[low]** three `random_owned` branches partitioned on `nationalism_n_imperialism` / `berlin_conference` whose bodies are byte-identical (same CB, same war, same `state_province_id = 1380`). Whatever was meant to differ was never written; ~75 lines could collapse to one block. |
| 620 | 95645 | **[low]** dead mtth modifier `DAI = { exists = no }` (factor 0.5): the trigger requires `DAI = { is_our_vassal = THIS }`, so DAI always exists when this is evaluated. |
| 214 | 95674 | **[low]** ENG gets `prestige = 5` under the option "But we were hoping for an excuse..." - the text is a disappointment, the effect a reward. |
| 224 / 254 | 95675 / 95676 | **[low]** the victory test is only "who owns Gauhati (1258) at truce". A white peace after a British thrashing, with BUR still holding 1258 and not disarmed, fires *Burmese Victory* and hands BUR every Assam core. |
| 313-315 | 95677 | **[low]** magnitudes: `treasury = -50000` on an uncivilised 1826 Burma is far beyond its cash (it just clamps), while ENG's matching `money = 50000` in 95678 is paid in full - the transfer is one-sided in practice. |
| 179-181 | 95673 | **[low]** in the war branch BUR "makes its point by force" but the `war` block runs in `FROM` (ENG) scope, so Britain is the attacker and Burma the defender. Historically right, textually backwards. |
| 715-722 | 95647 | **[low]** `random_country = { limit = { tag = SIA exists = yes } ... }` is a long way to write `SIA = { ... }`. |
| 2-40 | 95660 | **[low]** the Lao Rebellion has no `war = no` guard and its only mtth modifier (`factor = 0.2`, `war = yes`) makes it *more* likely mid-war, then opens two simultaneous wars against the freshly released WIA and CHK. |
| 890-960 | 95650 | **[low]** the second `random_country` branch drops `primary_culture = vietnamese`, and the third only covers `tag = DAI`, so a non-DAI Vietnamese-culture country with 2+ states matches no branch and the option does nothing for it. |
| 1115 | 95653 | **[low]** FRA takes `prestige = -10` because *Siam* refused its demand (option "A foolish move"). Abandoned chain, left. |
