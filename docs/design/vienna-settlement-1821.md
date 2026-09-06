# The Vienna settlement at 1821.9.1: spheres and guarantees

*2026-09-06. Files touched: `CoE_RoI_R/history/units/1821/{AUS,ENG,FRA}_oob.txt`,
`CoE_RoI_R/history/diplomacy/Guarantees.txt`. **Untested in game.***

## The mechanical finding that reshaped this pass

The brief assumed spheres are written as `sphere = { first = ... second = ... }` in
`history/diplomacy/`, because `docs/audit/diplomacy-tech.md` reports "no `sphere` entry
exists anywhere in `history/diplomacy/`". That is true but misleading, and the audit's own
parenthesis is the correct part: **Victoria 2 does not read spheres from `history/diplomacy`
at all.** Start-of-game spheres live in the *sphere leader's* OOB file, as a relation block
(`docs/wiki/sphere-modding.md`, confirmed against `history/units/ENG_oob.txt` in the game
folder):

```
TAG = {
	value = -200..200      # relation
	level = 0..5           # 0 hostile 1 opposed 2 neutral 3 cordial 4 friendly 5 sphere
	influence_value = 0..  # banked influence points
}
```

Consequences:

1. **No `SpheresGVG.txt` was created.** A `sphere` clause in `history/diplomacy/` is not a
   keyword the engine knows; the file would be dead weight at best and error.log noise at
   worst. The sphere work is in the three 1821 OOB files instead.
2. **The 1821 start is *not* sphere-less.** The mod's `history/units/1821/*_oob.txt` already
   carry a full set of `level = 5` entries. The pre-existing state, by leader:

   | Leader | Sphered at 1821 before this pass |
   |---|---|
   | AUS | BAD BAV WUR SAX KRA PAR MOD TUS LUC |
   | ENG | HAN ATJ ABU RPL AWA BAS BER BIK BHO BUN GWA HYD IND JAI JAS JOD KUT MEW MYS NAG ORI TRA |
   | PRU | ANH BRA HEK LIP MEC NAS LUX |
   | RUS | FIN AKH CPL DAG AZB |
   | FRA | PAP |
   | TUR | IRQ KDS TUN MOL WAL |
   | NET | BIM SLW |
   | SPA | SUL |

   So this pass is a **correction and gap-fill**, not a from-scratch build. Only five
   entries changed.

## Great power set at 1821.9.1

A sphere leader must be a GP or the engine ignores the block. GP rank is by score
(prestige + industry + military), which cannot be computed statically, but the prestige
ladder in `history/countries/` is the dominant term at a 1821 start where industry is near
zero everywhere:

ENG 250, RUS 200, FRA 150, AUS 100, PRU 80, TUR 60, **NET 60**, USA 50, then SPA 40 and
SAR 30.

The eight GPs are therefore almost certainly ENG RUS FRA AUS PRU TUR NET USA, with **SPA
ninth and outside**. Every sphere edited in this pass belongs to ENG, FRA or AUS, all safely
inside the set. Noted but *not* changed: `SPA_oob.txt` sets `SUL` to `level = 5`, which is
probably dropped at load because Spain is not a GP; and NET's sphere over BIM/SLW depends on
the Netherlands holding eighth place. Both are pre-existing and out of scope.

## Spheres: the calls, one by one

### Austria - the Italian system

Austria already sphered Parma, Modena, Tuscany and Lucca (the Habsburg secundogenitures) and
Cracow, plus Baden, Bavaria, Wurttemberg and Saxony in Germany. Three changes:

- **PAP 3 -> 5, and FRA's PAP 5 -> 3.** The Papal States were in the *Austrian* orbit in
  1821: Consalvi's restored government was underwritten by the Austrian garrison in the
  Legations from 1815, and Austria marched through the Papal States to Naples in March 1821.
  The French protectorate over Rome dates from the 1849 expedition, three decades later; the
  vanilla-derived `FRA` sphere over PAP is a 1849+ fact imported into 1821. **Contestable**
  in that Rome played Vienna and Paris against each other throughout, but not in 1821, when
  only Austrian troops were on the ground.
- **SIC added at 5.** Two Sicilies is the clearest case of the whole pass: the Neapolitan
  revolution was crushed by an Austrian army on the Laibach mandate in March 1821, and an
  Austrian corps of occupation stayed until 1827, paid for by Naples. At the mod's start date
  the Austrians are literally garrisoning the country. AUS had *no* SIC entry at all before.
- **SAR 2 -> 4, and FRA's SAR 4 -> 3.** Austria put down the Piedmontese rising at Novara in
  April 1821 and garrisoned Alessandria to 1823. **Deliberately stopped at friendly, not
  sphere**: the occupation was explicitly temporary, Charles Felix kept a free hand, and
  Sardinia was built up at Vienna as a *barrier* state with British backing precisely so that
  it would not be an Austrian client. Sphering an eleven-province regional power for the rest
  of the game on the strength of a two-year garrison overstates it.

Not changed: Austria keeps only `military_access = yes` on the northern German minors
(Anhalt, Bremen, Frankfurt, Hamburg, Hanover, Hesse-Kassel, Hesse-Darmstadt, Lippe, Lubeck,
Mecklenburg, Meiningen, Nassau, Oldenburg, Weimar) while Prussia holds them at 4-5. That is
the correct division of the Confederation: Austria presided, Prussia dominated the north
militarily and economically.

### Prussia - the northern minors

**No change.** Prussia already spheres Anhalt, Brandenburg, Hesse-Kassel, Lippe,
Mecklenburg, Nassau and Luxembourg, and holds Bremen, Cobourg, Frankfurt, Hamburg,
Hesse-Darmstadt, Lubeck, Meiningen, Oldenburg and Weimar at friendly. Three calls worth
recording as *deliberate non-changes*:

- **Hanover stays with Britain, not Prussia.** The mod models the personal union in
  `history/diplomacy/Unions.txt` (`union ENG/HAN`, 1814.10.12 - 1837.6.20) *and* as an
  `ENG` sphere at level 5. The sphere is redundant while the union holds, but harmless, and
  it keeps Hanover out of Prussia's column after the union lapses in 1837.
- **Saxony stays with Austria.** Contestable: Saxony lost half its territory to Prussia in
  1815 and was ringed by Prussian land, so an economic argument for a Prussian sphere exists.
  The political fact is the opposite - the Wettins resented the partition and leaned on
  Vienna for protection against exactly that pressure. Prussia's own file already puts Saxony
  at cordial (3), which is the right shape.
- The Hansa towns (Bremen, Hamburg, Lubeck) stay at friendly under Prussia rather than
  sphered. They were free cities with their own trade policy and heavy British commercial
  ties; the Zollverein pull that eventually takes them is a 1830s-1880s story and should be
  earned in play, not handed out at start.

### Britain - the maritime clients

- **UPB 4 -> 5.** Portugal-Brazil is Britain's oldest ally and, in 1821, close to a client:
  the 1810 Treaty of Alliance and Friendship, Beresford commanding the Portuguese army until
  the 1820 revolution expelled him, the Royal Navy shielding Brazilian trade, and the court
  only just returned from Rio. Britain had no closer European dependent. (POR owns zero
  provinces at 1821.9.1; the Braganza state is UPB, 100 provinces.)
- **ION added at 5.** The United States of the Ionian Islands was a *British protectorate*
  under the Treaty of Paris of 5 November 1815, run by a British Lord High Commissioner. ION
  is a registered tag owning two provinces at start and appeared in **no** 1821 OOB file at
  all. This is the least contestable addition in the pass.
- **NET left at 4, not sphered.** Argued and rejected: Britain co-authored the United
  Kingdom of the Netherlands as an anti-French barrier and returned the East Indies to it,
  but the Netherlands is itself a probable eighth great power (prestige 60, 65 provinces, a
  colonial empire and its own sphere over BIM/SLW). A sphere over a GP is meaningless to the
  engine, and treating the Dutch as a British satellite misreads a relationship that was
  already turning competitive in the Indies. Friendly is right.

### France - nothing

After the two downgrades above, **France starts with no sphere members at all**, which is
the historically correct and deliberate outcome. The army of occupation left French soil only
in 1818; France was admitted to the congress system at Aix-la-Chapelle on probation, and the
Quadruple Alliance's Article VI was aimed *at* her. The French client system begins with the
1823 intervention in Spain (Hundred Thousand Sons of Saint Louis) and the 1830 Algiers
expedition - both after the start date. France keeps cordial-to-friendly relations with the
Papacy, Naples, Switzerland, Sardinia, Spain and Morocco, which is exactly the right texture:
sympathy without clients.

### Russia - no change

Russia already spheres Finland, Congress Poland (CPL) and the Caucasian khanates, which is
the whole of the Vienna settlement's Russian column. The Balkans were argued and rejected:

- **Serbia, Wallachia, Moldavia are Ottoman vassals** in `history/diplomacy/PuppetStates.txt`
  (SER from 1817.11.6; WAL and MOL to 1859) *and* sit in the Ottoman sphere at level 5 in
  `TUR_oob.txt`. Russia's rights under Bucharest (1812) and later Akkerman were a treaty
  protectorate over another empire's provinces - real diplomacy, but not ownership of their
  market. Putting a Russian sphere on top of an Ottoman vassalage is engine-ambiguous and
  would pre-empt the 1826-1829 chain that is the point of the period. Russia keeps SER at
  friendly (4).
- **Greece stays at neutral (2) for everyone.** In September 1821 the revolt is five months
  old, Alexander I has publicly disavowed Ypsilanti, and no power has recognised anything.
  The existing level 2 across ENG/FRA/RUS is correct.

### Switzerland - sphered by nobody, on purpose

AUS and FRA both hold SWI at cordial (3) and nobody spheres it. That is the right modelling
of a state whose perpetual neutrality all five powers guaranteed in November 1815; the
guarantee below is the mechanism, not a sphere.

## Guarantees

**Victoria 2 has a guarantee *relation* - `DIPRELCH_GUARANTEE`, `START_GUARANTEE_EFFECT` and
`CW_WARNGUARANTEED` are all in vanilla `localisation/text.csv`, and the AI uses it - but
there is no documented way to script one.** `docs/wiki/` never mentions guarantees; there is
no `guarantee` effect, trigger or OOB key; and the only circumstantial evidence that the
history parser knows the clause is that vanilla ships `history/diplomacy/Guarantees.txt`
**empty**, which is how Paradox ships placeholders for clause types it *does* support.

Decision: write the entries in the same shape as the other diplomacy clauses (`first` =
guarantor, `second` = guaranteed), keep the set small and literal, and flag the file in its
own header as **unverified - check `error.log` on the next launch and delete the file if the
parser complains**. Worst case is inert entries and a few log lines; there is no crash risk,
since an unknown clause in a history file is skipped.

Eleven entries, all of them things the Congress system actually wrote down:

| Guarantor(s) | Guaranteed | Dates | Basis |
|---|---|---|---|
| AUS ENG FRA PRU RUS | SWI | 1815.11.20 - 1936.1.1 | Act of Paris, 20 Nov 1815: perpetual Swiss neutrality and inviolability, guaranteed by all five. The single most literal "guarantee" in the settlement. |
| AUS PRU RUS | KRA | 1815.6.9 - 1846.11.16 | Vienna Final Act: the Free City of Cracow, a strictly neutral joint creation of the three partitioning powers. Ends at the Austrian annexation. |
| ENG | UPB | 1810.2.19 - 1825.8.29 | Treaty of Alliance and Friendship, 1810: British guarantee of the House of Braganza. Dated to match the `ENG/UPB` alliance already in `Alliances.txt`. |
| AUS | PAP | 1815.6.9 - 1848.3.13 | The restored Papal government, garrisoned in the Legations by Austria. Ends when 1848 destroys the arrangement. |
| AUS | SIC | 1821.3.23 - 1827.5.1 | The Austrian army entered Naples on 23 March 1821 to restore Ferdinand I; the occupation ran to 1827. |

Argued and **excluded**:

- **The German Confederation's mutual defence.** The brief suggested approximating Article
  XI with AUS and PRU guarantees of every small German state. Rejected as duplication:
  `history/diplomacy/German Confederation.txt` already ties every Bund member to *both*
  Austria and Prussia by full alliance, 1815.6.8 - 1848.3.13. Adding thirty-odd guarantees on
  top of forty existing alliances would only multiply the AI's call-to-arms webs.
- **Russia over Serbia / Wallachia / Moldavia.** Same reason as the sphere call: they are
  Ottoman vassals, and a guarantee against their own overlord has no coherent engine meaning.
- **France anywhere.** No French guarantee existed in 1821 beyond the Swiss act she signed
  with everyone else.
- **Britain over the Ionian Islands.** That is a protectorate, i.e. the sphere entry above,
  not a guarantee to a third party.

## Untested balance risk

Flagged explicitly, because none of this has been in front of the game:

- **Spheres lock markets.** A sphered state trades into its leader's market first, so the
  new and upgraded spheres (AUS over SIC and PAP, ENG over UPB and ION) hand Austria the
  Neapolitan and Roman RGO output and Britain a 100-province Portuguese-Brazilian market at
  turn one. Against the margins in `docs/design/factory-balance.md`, the goods that matter
  are Sicilian sulphur and grain and Brazilian coffee, sugar, cotton and dyes - all artisan
  and factory inputs whose price the sphere effectively fixes for the leader.
- **France losing PAP is a real nerf**, not a wash: France goes from one sphere member to
  zero at start and must earn clients through influence. Historically right, mechanically a
  handicap relative to the previous state.
- Neither effect can be checked statically. Verify by starting an 1821 game, reading the
  diplomacy screen (spheres) and `error.log` (the guarantee clause), and playing far enough
  for the Austrian and British markets to settle. Re-running
  `python scripts/balance_factories.py` does not capture this - it has no model of spheres.


## Review outcome (2026-09-06)

Victoria 2 has no guarantee diplomacy concept: the vanilla `Guarantees.txt` is a 0-byte template and no file or wiki page uses a `guarantee` block, so the 11 entries were reverted and the file is empty again. The treaty research above stands as documentation only; the OOB sphere corrections ship as-is. `ION` at level 5 for ENG is redundant (already a vassal) but harmless.
