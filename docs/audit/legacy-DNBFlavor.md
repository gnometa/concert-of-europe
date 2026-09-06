# Logic audit - `events/DNBFlavor.txt` (Danubian Federation)

*2026-09-06. 58 events, ids 98655-98724. DNB is the federal successor of KUK
(Austria-Hungary): `decisions/AUS.txt` -> `propose_danube_federation` sets
`danube_proposal_in_progress`, the 98655-98687 blocks collect one global approval flag per
nationality (Hungarian gates all the others via the `OR` on the hungarian flags), and
`become_danube_federation` does `change_tag = DNB`. 98690-98695 pay off "full" approval,
98700-98706 release vassals for "partial", 98710-98716 punish "no" approval, 98720/98721 break
the federation up, 98722-98724 are the `is_triggered_only` receivers.*

Mechanical audits are at baseline after the fixes (refcheck 14/0/60/0/125/0/8, audit_events
unknown 0 / high 0, cwtools 14 known warnings, modcheck braces/provinces/tags clean).
No wrong FROM/THIS hop was found: `secede_province = THIS` inside `FROM = { any_owned }`
(98722/98723) and `relation = { who = THIS }` inside `any_country` (98720/98721) both resolve to
the event root, which is what those blocks want.

## Fixed in this pass

- **2365, 2432, 2540, 2600 (98720 both options, 98721 both options) - [high]** - `has_country_flag =
  south_german_rel` sits in the *effect* body of the option. It is a trigger; the engine logs an
  unknown effect and the flag the ex-federation is supposed to carry back into AUS is never set
  (the DNB history file sets it at start, but a `change_tag` chain that re-derives it needs the
  effect). Fixed: `set_country_flag = south_german_rel`.
- **2029-2298 (98710-98716, the seven rebellion events) - [high]** - each option did
  `TAG = { all_core = { remove_core = DNB add_province_modifier = { name = nationalist_agitation } } }`.
  `all_core` in a country scope walks *every* core of that tag worldwide, so DNB's Polish rebellion
  stamped `nationalist_agitation` on Russian and Prussian Poland, the Romanian one on Wallachia,
  Moldavia, Bessarabia and Ottoman Dobruja, the Croatian one on Ottoman/Bosnian land - effects on
  other countries' provinces (see `owner-scope.md`). Fixed: the `remove_core = DNB` sweep stays
  global (harmless, DNB cores only), the modifier moved to
  `any_owned = { limit = { is_core = TAG } add_province_modifier = ... }` so only DNB's own
  provinces are agitated. The Hungarian variant keeps its `NOT = { is_core = SLV is_core = CRO
  is_core = SYL }` exclusion in both blocks.
- **2452 (98720, option "Never! The Federation lives on!") - [medium]** - the `any_country` block
  handing out -100 relations and a humiliate CB had only `NOT = { vassal_of = THIS }`, so it also
  selected the non-existent nationality tags (no-op, but it silently diverged from the identical
  block in 98721 which does gate on `exists = yes`). Fixed by adding `exists = yes`.

## Reported, not changed

- **2495 (98721) - [low]** - `title = "EVTNAME98720"`, i.e. the totalitarian breakup reuses the
  democratic breakup's name key while using its own `EVTDESC98721`. `EVTNAME98721` does not exist
  in localisation; the shared title reads correctly ("End of the Federation"), so this is only
  worth splitting if the two need different headlines.
- **88-118, 165-188 (98656, 98657) - [medium]** - the Hungarian `ai_chance` is inverted relative to
  every other nationality. Hungarians: abort the whole chain 50 % (counter-proposal) and 75 %
  (refusal). Czechs/Romanians/Croats/Slovenes/Slovaks/Poles: abort 10 % and 20 %. Because the
  Hungarian flag gates all six other chains, an AI KUK abandons the federation before it starts in
  roughly two runs out of three. Deliberate ("Hungary is the co-equal partner") is defensible, so
  left alone; if the federation is meant to be a live AI outcome, 10/30/60 and 20/80 would match
  the rest of the file.
- **2369, 2436, 2544, 2604 (98720/98721, both "the Federation lives on" options) - [medium]** - the
  option text says the federation survives, but the effect strips *all seven* accepted cultures,
  exactly as the "we shall become Austria once more" option does. Either a copy-paste or an
  intentional turn to centralism; the accompanying civil war against HUN makes the harsh reading
  plausible, so not changed. If it is a copy-paste, delete the seven
  `remove_accepted_culture` lines from the second option of each event.
- **451-478 (98666) - [low]** - the Romanian counter-proposal keys off `is_core = SYL` /
  `is_possible_vassal = SYL` while its siblings 98665/98667 key off `is_core = ROM`. Both work
  (Transylvania and Bukovina carry SYL *and* ROM cores under AUS at the 1821 start, 12 and 14
  provinces respectively), so no branch is dead, but the mismatch means the "agree"/"refuse" pair
  can also fire on Bukovina alone while the counter-proposal cannot.
- **2269-2298 (98716) - [low]** - the Polish rebellion tests `is_core = POL` whereas the Polish
  celebration (98695) and release (98706) use `GLM`. After the fix the modifier is limited to
  owned provinces, so this only affects which *trigger* opens the event.
- **1716, 1759, 1806, 1861, 1904, 1955, 2002 (98700-98706) - [low]** - `diplomatic_influence =
  { who = X value = 200 }` on the freshly released vassal. Influence is capped at 100, so half the
  value is discarded. The paired `relation = { ... value = 200 }` is at the engine limit and fine.
- **2083 ff. (98711-98716) - [low]** - `remove_accepted_culture` for czech/romanian/croat/slovene/
  slovak/polish in the "no approval" branch, where that culture was never accepted (only the
  "full"/"partial" branches call `add_accepted_culture`). Silent no-op. Only the Hungarian case
  (98710) actually removes something, since `enact_dual_monarchy` accepted hungarian.
- **2651 vs 98720 - [low]** - 98721's "federation lives on" option sends 98722 (independence +
  civil war) to non-existent nationality tags holding DNB land; 98720's equivalent option does not,
  so under the democratic breakup only existing vassals can split off. Consistent with the reading
  that the totalitarian collapse is the more violent one, but the asymmetry is undocumented.
- **55-57 (98656) - [low]** - `is_possible_vassal = HUN` already implies `NOT = { HUN = { exists =
  yes } }`; the extra clause inside the `NOT` (which is a NOR here) is redundant.
- **No 1836-era or year-gated windows in this file**, so nothing is locked out by the 1821 start.
  No interaction with `AUSVormaerzGVG`, `ITARisingsGVG` or the Zollverein chain: those scope on AUS
  and on German tags, and DNB only comes into existence through KUK, which the German events do
  not touch. `decisions/AUS.txt` keeps DNB in the `embrace_*_minority` potentials, which is the
  only cross-file coupling.
