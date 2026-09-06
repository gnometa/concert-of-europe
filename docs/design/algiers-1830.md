# The Conquest of Algiers (1827-1834) - design

## Problem

`docs/design/1821-1836-coverage.md:20` lists the Conquest of Algiers as
**partial**: "events/FRAFlavor.txt:37234 (Fan Affair only, no landing chain)".
That is accurate. Grepping the whole tree for `algier` / `algeria` / `dey` /
`abd al` returns only:

- `events/FRAFlavor.txt:1226` **37234 The Fan Affair** - `fire_only_once`, FRA,
  gated on `has_country_flag = charles_x` or `july_revolution`, MTTH 48 months
  (x0.1 after 1830), blocked by `NOT = { year = 1836 truce_with = ALD war_with = ALD }`.
  Option A moves ALD's capital to 1708 Constantine and immediately declares
  `war = { target = ALD attacker_goal = { casus_belli = demand_concession_casus_belli
  state_province_id = 1700 } }`. Option B pays: `treasury = -10000`,
  `ALD = { treasury = 10000 }`, `prestige = -5`.
- `events/FRAFlavor.txt:1296` **37235 The Algerian Rebellion** - repeatable
  (MTTH 3 months, no `fire_only_once`), fires for FRA whenever ALD is an
  uncivilised neighbour before 1860, grants FRA a `demand_concession` or
  `establish_protectorate` CB, and is switched off by the country flags
  `algerian_rebellion` / `no_more_algerian_rebellion` and by the country
  modifier `punitive_effects`.
- `decisions/France.txt:54` `support_french_foreign_legion` - `potential`
  requires `owns = 1700`. It is unreachable from the 1821 start until somebody
  takes Algiers, so this chain is what unlocks it.
- `decisions/New Colonies.txt:1716-1745` `organize_algeria` and
  `events/New Colonies.txt:999-1042` - both **fully commented out** (`##` / `#`),
  dead text, not content.
- `decisions/UncivFlavor.txt:599` `move_capital_to_algiers` (ALD, needs
  `owns = 1700`) and `:644` `claim_the_sahara_ALD` (needs `civilized = yes`).

So the insult and the war declaration exist, and nothing else does: no blockade,
no landing, no fall of the Dey, no choice between a punitive raid and a colony.

**What ALD is at 1821** (`history/countries/ALD - Aldjazair.txt`, registered at
`common/countries.txt:384`): capital 1700, `primary_culture = maghrebi`,
`culture = berber`, `religion = sunni`, `absolute_monarchy`, uncivilised,
`ruling_party = ALD_conservative`. It owns thirteen provinces, all verified in
`map/definition.csv` and `history/provinces/africa/`: 1700 Algiers, 1701 Bougie,
1702 Setif, 1703 Medea, 1704 Oran, 1705 Tlemcen, 1706 Mustaghanim, 1707 Mascara,
1708 Constantine, 1709 Bone, 1710 Biskra, 1711 Ouargla, 1715 Naama. FRA owns
nothing in the Maghreb.

**Sizing comes from the mod's own history files.** The dated blocks in
`history/provinces/africa/` say that at a 1836 start France holds exactly the
coastal strip - 1700 Algiers, 1701 Bougie, 1704 Oran, 1706 Mustaghanim,
1709 Bone, all `colonial = 1` - while the interior (1702, 1703, 1705, 1707,
1708, 1710, 1711, 1715) stays ALD until the `1861.1.1` blocks. The 1821 start
should be able to reach that same 1836 picture and no further. It nearly does
already: `map/region.txt:928` makes `FRA_1704 = { 1700 1704 }` a two-province
state, so 37234's `demand_concession` war on `state_province_id = 1700` yields
Algiers **and** Oran, and `map/region.txt:926` keeps the eleven interior
provinces in a separate state (`FRA_1700`) that the war cannot take. This chain
therefore never conquers anything by script except the three remaining coastal
ports on its most expensive branch, and hands one back on its cheapest.

**Interlock with 37234.** The chain does not re-script the insult and does not
declare war. 1002500 is gated `NOT = { war_with = ALD }` and `NOT = { truce_with = ALD }`
so it can only occupy the years *before* 37234 option A; 1002501 requires
`war_with = ALD`, i.e. the war 37234 started (or one the player declared with
the CB 1002500 option B grants); 1002501's MTTH halves when `ALD = { capital = 1708 }`,
the fingerprint 37234 option A leaves behind. No edit to `events/FRAFlavor.txt`
is needed and none is proposed - adding a flag to 37234's options was considered
and rejected, because a shared legacy file should not be edited for a state that
is already detectable.

## Chain - `events/FRAAlgiersGVG.txt`, ids 1002500-1002504

| id | who | when | options |
|---|---|---|---|
| 1002500 | FRA | year >= 1827, not yet 1832, charles_x or july_revolution, ALD uncivilised, no war and no truce with ALD, MTTH 6mo | A blockade the ports (AI 60) / B demand satisfaction at gunpoint, grants a CB (AI 25) / C lift the blockade (AI 15) |
| 1002501 | FRA | year >= 1828, not yet 1840, `war_with = ALD`, does not own 1700, MTTH 3mo, news | A the full expedition, 37,000 men at Sidi Ferruch (AI 75) / B a coastal demonstration only (AI 25) |
| 1002502 | FRA | year >= 1829, not yet 1845, `owns = 1700`, MTTH 2mo, major, news | A empty the treasury of the Casbah (AI 70) / B honour the terms of the capitulation (AI 30) |
| 1002503 | FRA | year >= 1833, not yet 1848, `has_country_flag = algiers_taken`, owns 1700, MTTH 6mo | A colonisation and a Governor-General (AI 45) / B occupation restreinte (AI 40) / C hand Oran back (AI 15) |
| 1002504 | ALD | year >= 1830, not yet 1845, uncivilised, `FRA = { owns = 1700 }`, does not own 1700, MTTH 4mo | A proclaim the jihad (AI 60) / B the Desmichels convention (AI 40) |

Every event is guarded by a country flag set in **every** option
(`algiers_blockade_decided`, `algiers_landing`, `algiers_taken`,
`algiers_settled`, `ald_emirate`) and none uses `fire_only_once`, per the
engine-wide-once pitfall. Nothing is added to `common/on_actions.txt`. Each
`NOT` block holds a single clause, so nothing depends on reading `NOT = { a b }`
as anything other than NOR.

### 1002500 The Blockade of Algiers (picture `ship_attacked`)

Option A is the historical three-year blockade: `treasury = -5000` (the squadron
off Cape Matifou), `prestige = 2`, `relation = { who = ALD value = -100 }`, and
`ALD = { any_owned = { limit = { OR = { province_id = 1700 province_id = 1701
province_id = 1704 province_id = 1706 province_id = 1709 } }
add_province_modifier = { name = algiers_blockade duration = 1095 } } }` - the
five ALD ports, checked against `history/provinces/africa/`. The `any_owned`
block sits **inside the ALD country scope**, which is the point of
`scripts/audit_owner_scope.py`: from FRA's own scope it would match nothing.

Option B is the escalation: the same blockade modifiers at `duration = 730`,
plus `badboy = 1`, `relation = { who = ALD value = -150 }`,
`relation = { who = ENG value = -10 }` and
`casus_belli = { target = ALD type = demand_concession_casus_belli
state_province_id = 1700 months = 24 }` - the same CB against the same state
37234 would have used, granted rather than fired, so the player can open the war
on his own timetable instead of waiting on a 48-month MTTH. It does not start a
war and so cannot duplicate 37234.

Option C lifts the blockade: `prestige = -3`, `relation = { who = ALD value = 50 }`,
`any_pop = { limit = { type = capitalists } militancy = 1 }` (the Marseille
houses whose grain contracts the blockade ruined). It leaves 37234 free to fire
later; it is not the indemnity, which 37234 option B already covers.

`ai_chance` carries the conditionality Vic2 options cannot: option A is weighted
up under `has_country_flag = charles_x`, option C up under `badboy = 15` and
`war_exhaustion = 5`.

### 1002501 The Landing at Sidi Ferruch (picture `Artillery`, news)

Fires only while `war_with = ALD` and FRA does not yet own 1700, so it is the
scripted middle of a war the engine is already fighting.

Option A - Bourmont's 37,000 men: `treasury = -20000`, `war_exhaustion = 2`,
`prestige = 5`, `add_country_modifier = { name = armee_dafrique duration = 1825 }`,
and against the defender `ALD = { war_exhaustion = 8 any_pop = { militancy = 2 }
any_owned = { limit = { OR = { province_id = 1700 province_id = 1703 } }
add_province_modifier = { name = war_torn duration = 730 } } }` (1700 Algiers,
1703 Medea - Staoueli and the road to the Casbah). The war exhaustion pushed
onto ALD is what makes the AI accept the concession peace instead of grinding
out a long colonial war. MTTH modifiers: `factor = 0.5` on
`ALD = { capital = 1708 }` and `factor = 0.5` on `year = 1830`.

Option B - a coastal demonstration: `treasury = -6000`, `war_exhaustion = 1`,
`prestige = -2`, `ALD = { war_exhaustion = 3 }` and `war_torn` for 365 days on
1700 only. Cheaper, slower, and it leaves the Dey in place; weighted up by
`badboy = 15` and by `war_exhaustion = 5`.

### 1002502 The Fall of the Dey (picture `sultan`, major, news)

Trigger `owns = 1700` - the peace has already transferred the Algiers/Oran
state. Option A takes the Casbah treasure: `treasury = 25000` (a few weeks of
French revenue; the fixed-point ceiling is 2,147,483 and this is nowhere near
it), `ALD = { treasury = -10000 }`, `prestige = 5`, `badboy = 2`,
`ALD = { any_pop = { militancy = 2 } }`. Option B honours Bourmont's
capitulation: `prestige = 8`, `treasury = 5000` (the state chest only), no
infamy, `relation = { who = ALD value = 25 }`,
`ALD = { any_pop = { militancy = -1 } }`.

Both options give FRA `any_pop = { militancy = -1 }`. That is a deliberate and
deliberately small interaction with `events/FRAFlavor.txt:1534` (37244, the July
Revolution), which needs `average_militancy = 5` or the `three_glorious_days`
flag: a victory in Africa shaves a fraction off the pressure on Charles X
exactly as it did in July 1830, and cannot cancel the revolution.

### 1002503 The Ordonnance of 1834 (picture `scramble_for_africa`)

The real branch point of the chain.

Option A, colonisation:
`ALD = { any_owned = { limit = { OR = { province_id = 1701 province_id = 1706
province_id = 1709 } } secede_province = FRA } }` gives France Bougie,
Mostaganem and Bone - occupied 1832-33 historically, and exactly the provinces
the mod's own `1836.1.1` history blocks assign to FRA - and quietly does nothing
for any of the three ALD no longer holds, because the loop runs inside ALD's
scope. Cost: `badboy = 3`, `treasury = -10000`,
`relation = { who = ENG value = -25 }`, `ALD = { any_pop = { militancy = 3 }
any_owned = { add_province_modifier = { name = nationalist_agitation
duration = 1825 } } }`, and, following the precedent at
`events/FRAFlavor.txt:1203`, `random_country = { limit = { tag = ENG exists = yes
is_greater_power = yes NOT = { war_with = FRA } } casus_belli = { target = FRA
type = place_in_the_sun months = 12 } }` - Palmerston's price for a permanent
French Algiers. Note what that CB actually does: `place_in_the_sun` takes a
*colonial* state, and since nothing can flag Algiers or Oran as colonial (see
Risks) Britain will cash it in on Senegal or Guiana instead. The pressure is
real, the target is wherever France is weakest overseas, which is the same
bargain 37233 already offers. Gain: `prestige = 10` and, on 1700 and 1704,
`colonial_exploitation` and `colonial_recruitment` for 3650 days.

Option B, occupation restreinte: keep the two ports and stop.
`colonial_exploitation` on 1700/1704 for 1825 days only, `prestige = 3`, no
infamy, no British CB, `relation = { who = ENG value = 10 }`, and only
`ALD = { any_pop = { militancy = 1 } }`.

Option C, the abandonment lobby: `random_country = { limit = { tag = ALD
exists = yes } FRA = { any_owned = { limit = { province_id = 1704 }
secede_province = ALD } } }` hands Oran back - wrapped in the `random_country`
existence check so a dead ALD is never resurrected by the secession - plus
`prestige = -8`, `war_exhaustion = -3`, `relation = { who = ALD value = 100 }`,
`badboy = -1`. France keeps Algiers alone, which is a defensible 1834 position
and a cheap exit for a player who does not want an African army.

### 1002504 The Emirate of Mascara (ALD, picture `arab_revolt`)

The defender's half of the chain, so ALD is not a spectator. Trigger
`FRA = { owns = 1700 }` together with `NOT = { owns = 1700 }`.

Option A, the jihad. The unrest has to land on the *occupier*, not on the Emir
who declares it, so the militancy goes into the French-held provinces:
`FRA = { any_owned = { limit = { OR = { province_id = 1700 province_id = 1704 } }
any_pop = { limit = { culture = maghrebi } militancy = 3 consciousness = 1 } } }`
- `culture` is the pop-scope trigger and 1700/1704 carry large maghrebi pops
(`history/pops/1821.9.1/North Africa.txt:1140`). ALD itself gets `prestige = 5`,
`relation = { who = FRA value = -100 }`, `patriot_uprising` for 730 days on
1705 Tlemcen and 1707 Mascara only (the Emir's own towns, and a province
modifier PDM applies province by province), and
`add_country_modifier = { name = small_country_draft duration = 730 }` - two
years, not five, because that modifier carries `prestige = -0.05` per day
(`common/event_modifiers.txt:1663`) and would otherwise strip about ninety
prestige off an uncivilised country.

Option B, the Desmichels convention of 1834: `prestige = -3`,
`relation = { who = FRA value = 50 }`, `treasury = 5000` (the French subsidy and
the arms that came with recognition), `any_pop = { militancy = -2
consciousness = -1 }`. No modifier: `loyal_askaris`, the obvious candidate, is
localised "Gurkhas, Askaris & Tirailleurs" and is applied by *colonial powers*
to their own colonies in `events/ColonialUprisings.txt:1682`; putting it on ALD
would read as nonsense.

Neither option touches `algerian_rebellion` or `no_more_algerian_rebellion`:
those belong to 37235, which keeps running on its own three-month MTTH once FRA
and ALD are neighbours, and whose gates must not be distorted from here.

## New modifiers

Written ready to paste to `docs/design/_pending/FRAAlgiersGVG_modifiers.txt`;
`common/event_modifiers.txt` is not edited by this chain.

- `algiers_blockade` (province): `local_RGO_throughput -0.25`,
  `pop_militancy_modifier 0.05`, icon 4. Keys copied from `colonial_dry_spell`
  (`common/event_modifiers.txt:157`).
- `armee_dafrique` (country): `mobilisation_size 0.02`, `land_organisation 0.05`,
  `supply_consumption 0.10`, `prestige 0.02`, icon 15. Keys copied from
  `prussian_general_staff` (`:558`) and `administrative_genius` (`:1893`).

Everything else is reused and already localised (checked with
`modcheck.py loc-find`): `war_torn` (`:1631`), `colonial_exploitation` (`:163`),
`colonial_recruitment` (`:182`), `nationalist_agitation` (`:1613`),
`patriot_uprising` (`:1619`) and `small_country_draft` (`:1663`).
`punitive_effects`
is deliberately **not** used: `common/cb_types.txt` tests for it in eleven
places, so applying it as flavour would silently disable CB construction.

## Localisation

New file `localisation/GVG_algiers.csv`, written only through
`python scripts/modcheck.py loc-add GVG_algiers.csv KEY "text"` (the Edit/Write
hook blocks csv edits, and the file must stay Windows-1252 / CRLF / 15 columns
with the `x` terminator). 32 keys, ASCII only:

- `EVTNAME` and `EVTDESC` for 1002500-1002504 (10), `EVTOPTA` and `EVTOPTB` for
  all five (10), `EVTOPTC` for 1002500 and 1002503 (2) - 22 keys.
- News for 1002501 and 1002502: `EVTNAME<id>_NEWS_TITLE` plus
  `EVTDESC<id>_NEWS_LONG` / `_MEDIUM` / `_SHORT` - 8 keys.
- The two modifier names, `algiers_blockade` and `armee_dafrique`.

No accented characters and no semicolons: "Sidi Ferruch", "Bourmont", "Bone",
"Mostaganem", "occupation restreinte", "Abd al-Qadir", "armee d'Afrique",
"the Dey Hussein".

## Pictures

Existing art only, nothing downloaded; `python scripts/gfxtool.py missing` must
stay silent. All five verified by listing
`CoE_RoI_R/gfx/pictures/events/` and
`D:\Steam\steamapps\common\Victoria 2\gfx\pictures\events\`:

| id | picture | found in |
|---|---|---|
| 1002500 | `ship_attacked` | mod `gfx/pictures/events/ship_attacked.tga` (also vanilla) |
| 1002501 | `Artillery` | vanilla `gfx/pictures/events/Artillery.tga` |
| 1002502 | `sultan` | mod `gfx/pictures/events/sultan.tga` (also vanilla) |
| 1002503 | `scramble_for_africa` | mod `gfx/pictures/events/scramble_for_africa.tga` |
| 1002504 | `arab_revolt` | mod `gfx/pictures/events/arab_revolt.tga` (used by 37235) |

## Risks

- **Province ids** are this repo's historical crash source. Every id used
  (1700, 1701, 1703, 1704, 1706, 1709) exists in `map/definition.csv` and is
  ALD-owned at 1821 in `history/provinces/africa/`. No file under
  `history/provinces/` is created, moved or renamed.
- **The chain can be silently absent.** Both 37234 and 1002500 require
  `charles_x` or `july_revolution`; if FRA has left an absolutist government
  before 1824.9 neither flag is ever set (37240, `events/FRAFlavor.txt:1396`)
  and no Algiers content fires at all. That is 37234's existing behaviour, and
  it is matched on purpose rather than worked around with a second gate.
- **The mirror of the 37234 sequence.** If the Fan Affair fires first and its
  option B is taken - the indemnity paid, relations mended - 1002500 still
  qualifies (no war, no truce, ALD alive) and can blockade a Dey whose debt was
  just settled. `relation = { who = ALD value = 25 }` is a valid country trigger
  and could exclude that case, but it is deliberately not used: it would also
  suppress the blockade in every game where FRA simply happens to like ALD, and
  the chronology wobble costs nothing mechanically. Accepted as-is.
- **The British CB in 1002503 option A** can turn into an Anglo-French colonial
  war. It is the deliberate price of the colonisation branch, it is the exact
  pattern already used at `events/FRAFlavor.txt:1203`, and it is guarded by
  `is_greater_power` and `NOT = { war_with = FRA }`.
- **Seceded provinces do not become colonial.** There is no effect that sets
  `colonial = 1` (`docs/wiki/list-of-effects.md` has `is_colonial` only as a
  state *filter*), so Bougie, Mostaganem and Bone arrive as ordinary
  non-accepted-culture provinces rather than as the colony the 1836 history
  files describe. Cosmetic, and the alternative would be editing province
  history, which is forbidden.
- **Overlap with 37235.** Once FRA owns 1700 the two tags are neighbours and the
  repeatable Algerian Rebellion event starts offering CBs every few months. That
  is the intended post-1830 texture - the raiding that produced Abd al-Qadir's
  war - and 1002504 is written not to touch its flags. `audit_pacing.py` should
  be re-read for FRA after this lands: the chain adds five events and one
  `major = yes` popup between 1827 and 1834, on top of the July Revolution
  cluster.
- **Registry.** `events/GVG Event IDs.txt` needs
  `#1002500-1002599: FRAAlgiersGVG (1827-1834 Conquest of Algiers; 1002500-1002504 used)`.
  This design does not edit it; the orchestrator merges that line.
