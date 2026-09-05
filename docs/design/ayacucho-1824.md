# Ayacucho and the loss of the Americas, 1824-1834 (SPAAyacuchoGVG)

Ids 1002100-1002102, file `CoE_RoI_R/events/SPAAyacuchoGVG.txt`.

## The problem at the 1821 start

Three `history/wars` files are live on 1821.9.1 and all involve SPA:

| file | sides | war goals |
|---|---|---|
| `PeruvianWarofIndependence.txt` | PEU, ARG, CHL vs SPA | colonies: `cut_down_to_size`; SPA: `make_puppet` on PEU/CHL/ARG |
| `ColombianWarofIndependence.txt` | GCO vs SPA | GCO: `liberate_country` ECU; SPA: `establish_protectorate` |
| `DominicanWarofIndependence.txt` | SPA vs DOM | SPA: `establish_protectorate` |

MEX is **not** at war at the start (Mexican independence has no war file).
The `rem_attacker` / `rem_defender` dates in those files (1822.2.5, 1822.5.24)
only build the correct war state for a *later* start date; they do nothing once
a 1821 game is running.

Nothing in `events/` ends these wars: no `end_war` anywhere names SPA or a
colonial tag, and the Spanish colonial chain in `SPAFlavor.txt` (97150-97166,
Chincha Islands) and `MEXFlavor.txt` 44861 are post-1863/post-1836 content.
Resolution is left to the AI: Spain must ship armies across the Atlantic to
enforce `make_puppet` and the colonies must land in Iberia to enforce
`cut_down_to_size`, so the wars can idle for decades.

## Chain

| id | Who | Fires | Content |
|---|---|---|---|
| 1002100 | SPA | 1824-1830, MTTH 6 mo, `major` | Ayacucho: settle or fight on |
| 1002101 | colony | triggered, +5 days | Spain recognises our independence |
| 1002102 | SPA | 1827-1834, MTTH 12 mo | The Cost of Empire: forced peace |

**1002100** trigger: `tag = SPA`, at war with one of PEU/GCO/CHL/ARG/MEX, at
least one of those colonies holding its own (`any_country` with
`NOT = { national_provinces_occupied = 0.25 }`), and `NOT = { war_score = 25 }`
so a Spain that really is winning is never offered the settlement. Per-country
flags `ayacucho_offer_made` / `ayacucho_settled` and the global
`spanish_american_independence` gate it, per house style (no `fire_only_once`,
which is engine-wide).

Option A (ai 70) is the historical one: prestige -10, war exhaustion -10, and an
`any_country` sweep over the colonial tags (the five above plus CLM, BOL, ECU,
VNZ, DOM) limited to `war_with = SPA` that runs `end_war = SPA` in the colony's
scope, resets relations and fires the mirror. Option B keeps the war, +10 war
exhaustion, militancy for Spanish pops and a liberal scaled militancy.

**1002101** (is_triggered_only) sets `recognised_by_spain`, prestige +10, war
exhaustion -10, relation +100 with SPA, militancy -2. No `FROM` is used, so it
is safe to fire from inside the `any_country` sweep.

**1002102** catches the fight-on branch: same war test, `ayacucho_fight_on` set,
still no war score, 1827-1834. Its single option repeats the sweep (skipping
tags that already have `recognised_by_spain`) at prestige -15, so the wars
always end inside the design window.

No `history/wars` file is touched.
