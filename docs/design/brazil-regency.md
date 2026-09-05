# Brazil 1831-1840: abdication, Regency, Cabanagem, Majority - design

## Problem

`docs/design/1821-1836-coverage.md` line 57: "Abdication of Pedro I 1831 and the
Regency - missing; 46316 exists but is gated `year = 1840`". Brazil's 1820s are
covered (independence UPB-side in `events/PORFlavor.txt:97022-97029`, the
Cisplatine War in `events/URUFlavor.txt:46410-46420`), and 1835 has the
Farroupilha (`events/BRZFlavor.txt:46325` plus `history/wars/FarroupilhaWar.txt`),
but the decade between them - the Seventh of April 1831, the Regency, the
provincial revolts and the 1840 golpe da maioridade - has nothing.

## Chain (`events/BRZRegencyGVG.txt`, ids 1001900-1001903)

| id | when | options |
|---|---|---|
| 1001900 The Seventh of April | `tag = BRZ`, exists, `is_vassal = no`, 1830-1838, and either the Cisplatine defeat is settled (`URU` exists / `has_country_flag = cisplatine_war` cleared by 46413) or it is already 1831; guarded by both outcome flags; MTTH 6 months, major + news | A Pedro abdicates (ai 75): `brazil_regency`, `brazilian_regency` 9 y + `national_instability` 3 y, `ruling_party_ideology = liberal` (`BRZ_liberal` runs 1820-1870), upper house +liberal, prestige -5, liberal pop drift / B Pedro stays (ai 25): `brazil_pedro_stays`, prestige +2, militancy +2, reactionary drift, `national_instability` 5 y |
| 1001901 The Cabanagem | `brazil_regency`, `owns = 2410` (Belem), 1835-1841, not yet `brazil_cabanagem`; MTTH 8 months | A crush the cabanos (ai 60): prestige +2, heavy militancy and `patriot_uprising` on 2410, `country_event = 1001902` in 365 days / B negotiate (ai 40): prestige -3, lighter militancy, `nationalist_agitation` on 2410, no follow-up. Both set `brazil_cabanagem` |
| 1001902 The Price of the Cabanagem | `is_triggered_only`, from 1001901-A | single option: prestige -3, `national_instability` 2 y, leadership -20, further militancy on 2410 |
| 1001903 The Majority Coup | `brazil_regency`, 1840-1846, not yet `brazil_majority`; MTTH 4 months, major | A declare Pedro II of age (ai 85): clears `brazil_regency`, removes `brazilian_regency` and `national_instability`, prestige +10, `ruling_party_ideology = conservative`, upper house +conservative, militancy -3 / B prolong the regency (ai 15): prestige -3, militancy +2, `national_instability` 3 y, the regency modifier is refreshed for 3 more years |

## Interaction with existing Brazilian content

- **46325 (Farroupilha) and `history/wars/FarroupilhaWar.txt` are untouched.**
  1001901 is deliberately about Para (province 2410) only, so the two 1835
  revolts do not overlap: no `release`, no war, no core changes, no RGS mention.
- **46316** ("Pedro II comes of age", `year = 1840`, needs `pedro_events_begun`
  from 46315, which itself needs POR to be an absolute monarchy) stays in place.
  1001903-A does `clr_country_flag = pedro_events_begun` so the two coming-of-age
  events cannot both fire; if 46316 has already fired, 1001903 simply grants the
  political outcome the older event never had.
- 1001900 reads the Cisplatine state through `URU = { exists = yes }` /
  `has_country_flag = cisplatina_is_ours` only; it never re-opens that war.

## Deliberate limits

- **One new modifier**: `brazilian_regency` in `common/event_modifiers.txt`
  (militancy/consciousness up, prestige drag, `issue_change_speed`), following
  the `bavarian_regency` precedent from GREKingdomGVG. Everything else reuses
  `national_instability`, `nationalist_agitation` and `patriot_uprising`.
- **No new pictures**: `pedro_ii`, `streetriot` and `pedro_ii_grand` all ship in
  `gfx/pictures/events/`.
- **Provinces touched: 2410 only** (Belem; `owner = UPB` + `add_core = BRZ` at
  the 1821 start, so Brazil owns it after independence). Guarded with `owns`.
- **Every flag is written and read**: `brazil_regency` (1001900-A -> 1001901,
  1001903), `brazil_pedro_stays` (1001900-B -> guard on 1001900),
  `brazil_cabanagem` (1001901 -> guard on 1001901), `brazil_majority`
  (1001903 -> guard on 1001903).
- Windows are wider than the historical dates (1838 / 1841 / 1846) because each
  step waits on the previous one's MTTH, and no event is `fire_only_once`
  (engine-wide) - each is guarded by its own per-country flag instead.
