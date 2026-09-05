# The First Anglo-Afghan War, 1839-1842 (AFGWarGVG, ids 1002300-1002303)

## Why it needs scripting

`docs/audit/bridge-1836.md` item 2: nothing in `events/` models the Anglo-Afghan
war. `TheGreatGame.txt` (95610-95616, year-gated to 1828 by that audit) is a
generic influence-and-CB framework over the whole frontier; it can hand ENG a
`great_game_cb` against AFG but has no Simla, no Kabul, no Gandamak. This chain
adds the episode on top of it and reads its state (the `border_incident`
modifier, RUS's sphere) only as a pretext modifier - it never depends on it.

## 1821 start state (checked)

- AFG exists, capital 1209 Kabul (`owner = AFG`, `controller = REB` at 1821),
  1212 Herat, 1215 Kandahar, 1216 Jalalabad, 1217 Ghazni, 1218 Peshawar,
  1219 Quetta - all `owner = AFG` in `history/provinces/central asia/`.
- ENG does **not** border AFG directly in 1821: PNJ (Punjab) and SIN hold the
  ground between. By 1839 ENG may border AFG directly, hold it through a vassal,
  or only through a sphered PNJ/SIN. The trigger therefore accepts all three:
  `neighbour = AFG`, `any_country = { vassal_of = ENG neighbour = AFG }`,
  `AFG = { any_neighbor_country = { in_sphere = ENG } }`.

## Events

(a) **1002300 The Simla Manifesto** - ENG, 1838-1840, AFG exists and owns Kabul,
one of the three adjacency branches above, not at war/truce/allied/vassal with
AFG, guarded by `simla_manifesto_issued` / `anglo_afghan_stayed_out`. MTTH 6
months, x0.5 when AFG is in RUS's sphere or carries `border_incident` (the Great
Game pretext), x0.75 on bad relations.
 - A (AI 70) Army of the Indus: `cut_down_to_size` CB + `war = {}` (the
   vanilla-attested idiom used by `ASHWarGVG.txt` / `RUSTurkishWarGVG.txt`),
   prestige +2, badboy +1, flag `anglo_afghan_intervention`.
 - B (AI 30) stay behind the Sutlej: prestige -1, relations and influence to AFG.

(b) **1002301 The Retreat from Kabul** - ENG, 1841-1843, has
`anglo_afghan_intervention`, AFG exists, and `war_with = AFG` **or**
`controls = 1209`. The 18-month/1-year dwell is expressed as the 1841 year gate
plus a 5-month MTTH, house style. `news = yes`.
 - A (AI 60) Elphinstone's army destroyed: prestige -10, war exhaustion +5,
   `leadership = -5` (as `BRZRegencyGVG.txt`), +1 militancy in owned HND cores,
   flag `kabul_retreat_disaster`, fires 1002303 for AFG.
 - B (AI 40) hold Kabul through the winter: prestige +2, badboy +1, war
   exhaustion +2, `colonial_chaos` and militancy on 1209 if owned; sets
   `kabul_held_1841` + `anglo_afghan_settled`, which closes the chain.

(c) **1002302 The Army of Retribution** - ENG, 1842-1845, has
`kabul_retreat_disaster`, not settled, not the hold-Kabul branch. MTTH 6 months,
faster after 1843 and when AFG took Gandamak.
 - A (AI 75) burn the bazaar and withdraw: prestige +5, war exhaustion -3,
   `end_war = AFG`, relations +50, clears `colonial_chaos`.
 - B (AI 25) stay and make Afghanistan a protectorate: prestige +2, badboy +2,
   `establish_protectorate_casus_belli`, war left running.

(d) **1002303 Gandamak, the Afghan Side** - AFG, `is_triggered_only`, fired by
1002301 option A: flag `afghan_gandamak_victory`, prestige +5, war exhaustion -3,
militancy down / consciousness up among primary-culture pops.

## Notes

Magnitudes stay inside the band used by the other GVG war chains. Every country
reference is guarded with `exists`, every province effect with `owns`/`controls`
or an `any_owned` limit, so a game where ENG never reaches the frontier or where
AFG is gone simply never sees the chain. Pictures are existing files
(`persia_anglo_afghan`, `derrota`, `war_ended`, `dost_mohammad_khan`).
