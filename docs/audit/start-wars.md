# Wars live at the 1821.9.1 start

`python scripts/audit_diplomacy.py` lists eight wars whose latest history entry at or before
1821.9.1 has added participants and no `rem_*`. The later `rem_*` dates in `history/wars/*.txt`
are **never applied** — history is only read up to the bookmark date — so every war below runs
until the AI (or a script) ends it.

A war ends when a belligerent enforces a war goal. That needs (a) the goal's provinces to be
reachable, and (b) a peace cost the AI can actually reach. `common/cb_types.txt` gives
`cut_down_to_size` a `peace_cost_factor` of **100**: an AI holding that goal holds out for a war
score it can never buy, which is exactly why the Spanish American wars had to be scripted out
(`events/SPAAyacuchoGVG.txt`, 1002100-1002102). Land adjacency below was computed from
`map/provinces.bmp` + `map/definition.csv`; cores/ownership from `history/provinces/`.

| War (file) | Sides | War goals | Adjacent? | Enforceable? | Historical end | Verdict |
|---|---|---|---|---|---|---|
| AliPashasRebellion (1820.6.1) | TUR IRQ TUN KDS vs EPI | `annex_core_country` TUR>EPI | yes, 13 borders | yes — all 9 EPI provinces are TUR cores, cost 0.7, `po_annex` | Ali Pasha killed 24 Jan 1822 | **AI can end it** |
| BurmeseConquestofAssam (1821.2.1) | BUR vs ASM | `conquest` BUR>ASM | yes, 5 borders | yes — cost 1.0, `po_annex`; ASM is 4 provinces | Assam annexed 1822, lost 1826 | **AI can end it** |
| GreekWarofIndependence (1821.3.25) | TUR IRQ TUN KDS vs GRE | `annex_core_country` TUR>GRE | yes (834-840 land link, plus sea) | yes — all 5 GRE provinces are TUR cores | Adrianople 1829 / London 1832 | **scripted resolution exists (1001401)** |
| ColombianWarofIndependence (1820.10.9) | GCO vs SPA | `establish_protectorate` SPA>GCO, `liberate_country` GCO>SPA | yes, 7 borders | no (see SPAAyacuchoGVG) | Ayacucho 1824 | **scripted resolution exists (1002100/1002102)** |
| PeruvianWarofIndependence (1821.7.28) | PEU ARG CHL vs SPA | `cut_down_to_size` x2 vs SPA, `make_puppet` SPA>PEU/CHL/ARG | yes, 17 borders | no — `cut_down_to_size` cost 100 | Ayacucho 1824 | **scripted resolution exists (1002100/1002102)** |
| DominicanWarofIndependence (1821.9.1) | SPA vs DOM | `establish_protectorate` SPA>DOM | island | no | Espana Boba ends Dec 1821 | **scripted resolution exists (1002100/1002102)** |
| MassinaJihad (1818.10.2) | MAS vs SEG | `acquire_all_cores` + **`cut_down_to_size`** MAS>SEG | yes, 3 borders (1804-1799/1802/1803) | **no** | Seku Amadu dies 1845; file's own `rem` is 1845.6.6 | **stuck** |
| Russian-CircassianWar (1804.7.1) | RUS FIN CPL vs CIR | `conquest` RUS>CIR | yes, 8 borders | yes — cost 1.0, `po_annex`; all 4 CIR provinces are RUS cores | 1864 (file's `rem` 1829) | **AI can end it** (early, but not stuck) |

## Notes

* **Greece.** `events/RUSTurkishWarGVG.txt` 1001401 (Treaty of Adrianople) does
  `end_war = TUR` for GRE and is the only place that sets `london_conference_1832_held`, which
  `events/GREKingdomGVG.txt` 1000500 requires. PDM's `events/RUSFlavor.txt` 95075 and
  `decisions/RUS.txt` `treaty_of_adrianople` are the maximalist alternative. Both need RUS to
  start the 1828 war first (1001400); if RUS never does, the Ottoman AI simply annexes Greece,
  which is ahistorical but is a *resolution*, not a stall.
* **Massina.** The only genuinely stuck war. MAS is a single province (1804), uncivilised, and
  carries a `cut_down_to_size` goal it can never buy — the same trap as Spain in the Americas.
  Its `can_use` also demands `THIS = { civilized = yes }`, so the goal was never legal for MAS
  to begin with; it exists only because history files bypass `can_use`. The paired
  `acquire_all_cores` (cost 0.5, MAS cores on 1799/1802/1803) is fine on its own, so the fix is
  simply to let the two sides stop.
* **Circassia.** Not stuck, but note `conquest`'s `can_use` requires
  `OR = { THIS = { civilized = no } civilized = yes }`, which a civilised RUS attacking an
  uncivilised CIR fails. History bypasses that check, so the goal is enforceable in practice; if
  a future engine/patch revalidates goals this war becomes stuck too. Left alone.
* **Not live at start.** `OttomanPersianWar.txt` begins 1821.9.10, nine days *after* the
  bookmark, so the engine never creates it — the 1821-23 war and the Treaty of Erzurum simply do
  not happen. XhosaWar (1834), FarroupilhaWar (1835), TexanWarofIndependence (1835),
  OttomanBarbaryWar (1835), Taiping (1850), ACW and Cochinchina (1861) are all post-start and
  likewise never fire from history; they are covered by events/decisions instead. There is no
  Cisplatine or Sudan war file in the tree.

## Added

`events/WarResolutionsGVG.txt`, ids **1002200-1002201**, closes the one stuck war:

* **1002200** (MAS, 1843-1847, MTTH 6 months) — Massina is offered the historical settlement with
  Segu. Accept ends the war (`ai_chance` 70); refuse sets `massina_fight_on`.
* **1002201** (MAS, 1848-1852, MTTH 6 months) — forced peace for a Massina that fought on.

Guards: `massina_peace_offered`, `massina_fight_on`, `massina_settled`.
