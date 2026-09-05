# Greek Kingdom (1830-1843) — design

## Problem

`docs/audit/start-state-1821.md`: GRE starts 1821 in revolt as an
`absolute_monarchy`. The absolutism is anachronistic for 1821 but **load-bearing**
— `decisions/GRE.txt` `hellenic_parliament` has `government = absolute_monarchy*`
in its `potential`, and is the mod's route to the 1844 constitution. The start
state is therefore left untouched.

What already exists: the Greek War of Independence and the recognition machinery.
`Ottoman_Event.txt` (31258-31269) fights the war and sets GRE's `legitimacy`
flag; `GREFlavor.txt` 31200-31213 runs the London Conference of 1832, decides
the borders (weak/medium/strong Greece) and sets the global flag
`london_conference_1832_held`. The 1836 bookmark hands both out in
`history/countries/GRE - Greece.txt`.

What is missing is everything *after* the borders: who wears the crown
(London Protocol, Feb 1830), the Bavarian regency and Otto's landing at
Nafplion (Feb 1833), and the bloodless coup of 3 September 1843 that forced the
constitution. This chain fills exactly that gap and adds **no** territory,
recognition or war logic.

## Chain (`events/GREKingdomGVG.txt`, ids 1000500-1000502)

| id | who | when | options |
|---|---|---|---|
| 1000500 | GRE | 1830+, `london_conference_1832_held`, not at war with TUR, `fire_only_once`, MTTH 2 months | A accept the powers' candidate (ai 80): prestige +10, ENG/FRA/RUS relations +25, sets `greek_crown_offered` / B demand a republic (ai 20): prestige +5, consciousness +2, ENG/FRA/RUS -10, sets `greek_crown_offered` **and** `greek_republic_demanded` |
| 1000501 | GRE | 1832+, `greek_crown_offered`, `fire_only_once`, MTTH 3 months, `major`, `news` | single option: prestige +10, BAV relations +100 (guarded by `random_country`), ENG/FRA/RUS +10, `bavarian_regency` modifier for 3650 days, sets `otto_arrived` |
| 1000502 | GRE | 1843+ (not past 1848), `otto_arrived`, still an absolute monarchy, `fire_only_once` | A grant the constitution (ai 80): mirrors `hellenic_parliament` / B crush the mutiny (ai 20): militancy +2, consciousness +1, prestige -10, reactionary drift, `liberal_agitation` for 5 years |

Option B of 1000500 does not switch the government: a republic would void
`hellenic_parliament`'s `potential` and orphan the 1844 constitution. The powers
impose Otto either way (as historically); B only records the resentment, and its
flag is read once, as an ai_chance modifier on 1000502's constitution option.

## No double grant with `hellenic_parliament`

1000502-A sets `set_country_flag = voule_ton_ellinon` and applies exactly what
the decision applies (`wealth_weighted_voting`, `harassment` if
`underground_parties`, `government = prussian_constitutionalism`, prestige,
militancy -2), plus `remove_country_modifier = bavarian_regency`. The decision's
`potential` already requires `NOT = { has_country_flag = voule_ton_ellinon }`
and an absolute monarchy, so after the event it disappears. Conversely, if the
player takes the decision before 1843, the event's `government = absolute_monarchy*`
trigger fails and it never fires. Only one of the two can ever resolve.

## Deliberate limits

- **No start-state change**, no province edits, no `secede_province`, no war.
- **One new modifier**, `bavarian_regency` in `common/event_modifiers.txt`
  (militancy/consciousness +0.02, prestige -0.01, icon 6). Everything else
  reuses `liberal_agitation`.
- **No new pictures**: `greatpowers` and `streetriot` ship in the mod,
  `bayern` ships in the mod (Otto was a Wittelsbach), `treaty` falls back to
  vanilla.
- **No new flags without a reader**: `greek_crown_offered` (read by 1000501),
  `greek_republic_demanded` (read by 1000502's ai_chance), `otto_arrived` (read
  by 1000502), `voule_ton_ellinon` (the existing decision's flag).
