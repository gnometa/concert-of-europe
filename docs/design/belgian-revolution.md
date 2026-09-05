# Belgian Revolution (1830-1839) — design

## Problem

The 1821 start has NET owning all eleven Belgian-cored provinces (381, 387-396;
397/398 Luxembourg/Arlon start under LUX). BEL does not exist. `BELFlavor.txt`
opens at 1837 and assumes `tag = BEL`.

`BELFlavor.txt` already ships a large PDM secession/London-Conference machine
(36720 secession, 36725/36726 conference, 36735-36746 outcomes, 36709-36716
Treaty of London / fall of Amsterdam). It is **not** missing — what is missing is
a *cause*: 36720 fires on `year = 1825` with a flat 60-month MTTH, has no link to
the French July Revolution, and both of its options do the same thing (release
BEL immediately, no player agency, no war).

## Approach

Add a **prelude** chain in `events/BELRevolutionGVG.txt` (ids 1000301-1000307)
that supplies the 1830 trigger, the crack-down/concession choice and the war,
then hands off to the existing PDM conference (which fires by itself once
`exists = BEL`). Nothing in the PDM chain is duplicated: no new London
Conference, no new Treaty-of-London partition logic.

Two one-line guards are added to `BELFlavor.txt` event 36720 so the old
context-free secession cannot pre-empt or double-fire the new chain:
`year = 1825` -> `year = 1830`, plus `NOT = { has_country_flag = BEL_revolt_in_progress }`.

## Chain

| id | who | when | options |
|---|---|---|---|
| 1000301 | NET | 1830+, owns 387, BEL absent, MTTH 3 months (halved once FRA has `july_revolution`) | A crack down (militancy/consciousness in BEL cores, -> 1000302 in 40 days) / B concessions (`BEL_concessions_offered`, prestige -5, -> 1000302 in 150 days) |
| 1000302 | NET | triggered, `major` | A recognise: `release = BEL`, prestige -15 / B fight: release + `war` with `annex_core_country` / C appeal to the Holy Alliance: as B, plus a chance RUS or PRU allies NET |
| 1000303 | FRA | triggered | A back Brussels: influence + `create_alliance = BEL` / B leave it to the Powers |
| 1000304 | ENG | triggered | A independence and neutrality (influence BEL, sends NET the treaty) / B stay out |
| 1000305 | NET | triggered by 1000304-A only (avoids a double fire) | A accept the Twenty-Four Articles: `end_war = BEL` / B refuse: infamy +2, ENG/FRA relations |
| 1000306 | BEL | triggered 240 days after release | A Leopold of Saxe-Coburg (`hms_government`, ENG influence) / B the Duc de Nemours (FRA) / C a republic (`democracy`) |
| 1000307 | NET | 1839+, still at war with BEL, fire_only_once | A sign the Treaty of London / B fight on (infamy, war exhaustion) |

AI weights follow history: crack down 70/30; fight 70 / recognise 30 / Holy
Alliance 15 (recognise x2 if concessions were offered); refuse the Twenty-Four
Articles 70/30 in 1831 but accept 80/20 in 1839; Leopold 70/20/10; Britain and
France both intervene at 70/30.

## Deliberate limits

- **No province edits.** `release = BEL` moves exactly the NET-owned BEL cores.
  Luxembourg (397) and Arlon (398) are LUX-owned at the 1821 start and stay
  there, which is the historical 1839 settlement; no `inherit = LUX` (36720 does
  that, and it is the one behaviour of the old event this chain replaces).
- **No new modifiers or pictures.** Uses `no_more_war` and `national_confusion`
  from `common/event_modifiers.txt`, and the orphaned Belgian art the mod
  already ships (`DIM_muette_de_portici`, `DIM_belgian_revolution`,
  `DIM_garde_civique`) plus vanilla `greatpowers`, `treaty`, `lion`.
- **No new flags without a reader.** `BEL_revolt_in_progress`,
  `BEL_concessions_offered` and `BEL_war_of_secession` are each both set and
  tested; `belgium_seceded` and `united_netherlands` are the existing PDM flags
  and are set/cleared exactly as `BELFlavor.txt` and `FRAFlavor.txt` expect.
- `annex_core_country` is a legal war goal here: every province `release = BEL`
  hands over is also a NET core, which is what its `can_use` requires.
