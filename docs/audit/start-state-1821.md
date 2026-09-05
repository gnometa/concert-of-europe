# Start state, 1821.9.1 - historical plausibility pass

Follow-up to `docs/audit/history-countries.md` (plausibility section). Scope: countries whose
September 1821 government / ruling party looked visibly wrong. Each entry records what history
says, what the file already had, what was changed, and which event or decision chains were read
before changing (or not changing) anything.

Method for every candidate: read `history/countries/<TAG> - Name.txt`, the tag's party list in
`common/countries/*.txt` (ideology + start_date/end_date), the government's allow-list in
`common/governments.txt`, then grep `events/` and `decisions/` for triggers keyed on that tag's
government, ruling ideology or start flags. Only changes the existing scripts tolerate were made.

**Net result: one file changed (BAV). Six candidates were already correct or are load-bearing for
an event chain; two are deliberate design calls.**

---

## 1. SPA - Spain: already correct, and load-bearing. No change.

- History: Trienio Liberal, March 1820 - October 1823. Ferdinand VII rules under the restored
  1812 Cadiz constitution with a progresista/exaltado ministry.
- File had: `government = hms_government`, `ruling_party = SPA_liberal`
  ("Partido Progresista"), `wealth_voting`, `yes_meeting`,
  `set_country_flag = liberal_election_win`. This is already the Trienio.
- Changed: nothing.
- Events checked: **`events/SPAFlavor.txt` id 37761** ("Appeal to the Holy Alliance") has
  `OR = { government = hms_government hms_government2 hms_government3 }` in its trigger with an
  mtth weighted to 1823/1825 - i.e. the Hundred Thousand Sons chain **requires SPA to start as
  hms_government**. It fires 37762 at FRA, which unlocks
  `decisions/France.txt` -> `restore_spanish_absolutism` (potential: `war_with = SPA` +
  `has_country_flag = one_hunderd_thousand_sons`), whose effect sends SPA event **37763**
  ("Ferdinand's Restoration"): `government = absolute_monarchy` plus `political_reform = appointed
  / underground_parties / none_voting`. Touching SPA's start government would break this chain at
  the first link. Also checked 37707, 37760 (Carlism, 1830+) and 37710/37711 (Carlist War, which
  sets `government = absolute_monarchy` and `ruling_party_ideology = reactionary` on the SPC tag) -
  none depend on the 1821 state.
- Note: `press_rights = censored_press` is arguably a touch harsh for the 1820 press-freedom
  decree, but 37763 does not reset press rights, so raising it would leave a free press under
  restored absolutism from 1823 on. Left alone deliberately.

## 2. UPB - Portugal-Brazil: already correct, and load-bearing. No change.

- History: the 1820 Liberal Revolution; the Cortes Gerais Extraordinarias e Constituintes sat from
  January 1821 and Joao VI returned to Lisbon in July 1821. Vintista (liberal) ministry.
- File had: `government = hms_government`, `ruling_party = POR_liberal`, `wealth_voting`,
  `last_election = 1818.1.1`, `decision = UPB_setup`. Already the Vintista period.
- Changed: nothing.
- Events checked: **`events/PORFlavor.txt`** ids 97000, 97001, 97003 and 97015 all gate on
  `OR = { government = hms_government ... }` for `tag = POR` / `tag = UPB`; 97003's effect is
  `government = prussian_constitutionalism`, and 97002 is the mirror branch for the case where the
  country is *not* hms_government. Event 97027 ("Demands of the Absolutists") is the absolutist
  branch and expects `absolute_monarchy` by then, not at start. 97024 does `change_tag = POR` (the
  Brazilian separation, 1822). The Vintista start is the entry point for all of it.

## 3. SIC - Two Sicilies: confirmed correct. No change.

(The Two Sicilies tag in this mod is **SIC**, not TWO; there is no `TWOFlavor.txt`.)

- History: the 1820 Carbonari constitution was revoked after the Austrian intervention and the
  battle of Rieti, March 1821. Ferdinand I rules absolutely again from May 1821.
- File had: `government = absolute_monarchy`, `ruling_party = SIC_reactionary`
  ("Ristorazionista"), `none_voting`, `appointed`, `underground_parties`. Correct.
- Changed: nothing.
- Events checked: `events/ITAFlavor.txt` (SIC references are territorial, plus generic
  absolute/prussian/hms branches at lines 1417-1442), `events/LiberalRevolutions.txt` id 10001,
  which lists `tag = SIC` as an eligible country but only from `year = 1840` - it is the 1848
  wave, not 1820. `events/SPAFlavor.txt:616` uses `tag = SIC` + `absolute_monarchy` as a
  diplomatic-support clause inside the Carlist chain, which the current start state satisfies.

## 4. SAR - Sardinia-Piedmont: confirmed correct. No change.

(File is `history/countries/SAR - Sardinia.txt`; `SRD` is a separate tag.)

- History: the March 1821 Piedmontese revolt was crushed at Novara on 8 April 1821; Victor
  Emmanuel I abdicated and Charles Felix ruled absolutely, repudiating the constitution.
- File had: `government = absolute_monarchy`, `ruling_party = SAR_reactionary`
  ("Ristorazionista" / "Restaurazionisti"), `none_voting`. Correct.
- Changed: nothing.
- Events checked: `events/ITAFlavor.txt`, `decisions/Italy.txt` - all SAR references are
  territorial/unification triggers with no dependency on the 1821 government.

## 5. GRE - Greece: left as an absolute monarchy, deliberately. No change.

- History: in revolt since March 1821; the First National Assembly at Epidaurus (January 1822)
  produced a provisional **republic**. There was no Greek monarchy before Otto of Wittelsbach in
  1832, so `government = absolute_monarchy` at 1821 is an anachronism.
- File had: `government = absolute_monarchy`, `ruling_party = GRE_conservative`, capital 839
  Nafplion (fixed in the earlier pass).
- Changed: nothing. Reasons:
  1. **There is no Otto/Wittelsbach accession event anywhere in the mod.** Grepping `events/` and
     `decisions/` for `otto`, `wittelsbach` and for any effect setting a GRE monarchy returns
     nothing; `events/GREFlavor.txt` (ids 31200-31207, the 1832 London Conference) only
     creates/enlarges GRE and sets `civilized = yes`, never its government. So a republican start
     would never be converted back to a monarchy.
  2. **`decisions/GRE.txt` -> `hellenic_parliament`** (the 1844 Voule ton Ellinon) has
     `potential = { tag = GRE OR = { government = absolute_monarchy absolute_monarchy2
     absolute_monarchy3 } }` and its effect is `government = prussian_constitutionalism` plus
     `political_reform = wealth_weighted_voting`. Starting GRE as a democracy would permanently
     strip Greece of that decision and of the whole absolutism -> constitutional-monarchy arc it
     opens. That is the "leave and explain" case in the brief.
  3. The ruling party is in fact period-appropriate: `GRE_conservative` is localised
     "French Faction", i.e. one of the three revolutionary factions (English/French/Russian
     parties), and is defined 1820.1.1-1875.1.1.
- If the mod ever wants the historical republic, it needs an Otto accession event around 1832
  (setting `government = absolute_monarchy` and the relevant party) *before* GRE's start
  government is moved to `democracy`; doing the second without the first is the regression.

## 6. BAV - Bavaria: **CHANGED**.

- History: the Bavarian constitution of 26 May 1818 created a bicameral Landtag (an appointed
  Kammer der Reichsrate and an elected Kammer der Abgeordneten on a property/estate franchise);
  it sat in 1819 and again in 1822/1825. Bavaria was the model constitutional monarchy of the
  German Confederation in 1821, not an absolute one.
- File had: `government = absolute_monarchy`, `vote_franschise = none_voting`,
  `ruling_party = BAY_conservative_2`.
- Set:
  - `government = prussian_constitutionalism` - the mod's constitutional-monarchy-with-appointed-
    ministry form. `common/governments.txt:196` allows liberal/socialist/social_liberal/
    conservative/reactionary/fascist, so `BAY_conservative_2` (ideology `conservative`, defined
    from 1820.1.1) remains legal, and `appoint_ruling_party = yes` keeps the king choosing his
    ministry, which is exactly the 1818 arrangement.
  - `vote_franschise = landed_voting` - the government has `election = yes`, so `none_voting`
    would have been contradictory; `landed_voting` matches the Abgeordneten property franchise and
    is what FRA and NET use with the same government.
  - `last_election = 1819.5.1` added, so with `duration = 60` the next Landtag falls in 1824.
  - `upper_house_composition = appointed` kept (the Reichsrate were appointed), as were
    `state_press` and `underground_parties` (Karlsbad Decrees, in force since 1819).
- Events checked: **`events/BAYFlavor.txt`** ids 33400 (Walhalla, 1841), 33401 and 33402 (both of
  which already accept `absolute_monarchy` OR `prussian_constitutionalism` OR `hms_government`),
  33403 (Wagner, 1875), 33404 (Mozartfest, 1838) - none require an absolute Bavaria.
  `decisions/Germany.txt` (`schwabing_circles`, `construct_the_walhalla`) keys on tag plus
  province ownership only. `decisions/AUS.txt` and `events/1german_revolution_1848.txt` reference
  BAV only for spheres, cores, vassalage and `ai = yes/no`. `events/GERFlavor.txt` and
  `events/GreatWar_Events.txt` likewise carry no government check on BAV.
- Out of scope but worth noting: **BAD (1818), WUR (1819), HAN and SAX are all
  `absolute_monarchy` + `none_voting` too**, and Baden and Wurttemberg had constitutions of the
  same generation as Bavaria's. Only BAV was in this task's scope; the same argument applies to
  them and they were left untouched rather than silently reworked.

## 7. PER - Persia: `civilized = yes` left alone. No change.

- The brief's test was whether the Persia flavour is written for a civilised Persia. It is written
  to work **either way**, and it is clearly intentional:
  - `decisions/PERflavour.txt` -> `per_expedition_to_europe` allows on
    `OR = { diplomatic_reform = balanced_diplomacy  civilized = yes }`, and
    `the_reuter_concession` on `OR = { civilized = yes  AND = { NOT = { finance_reform =
    no_finance_reform } NOT = { diplomatic_reform = isolationism } pre_indust = yes_pre_indust } }`
    - i.e. every gate has an explicit uncivilised branch.
  - `history/countries/PER - Persia.txt` still carries the uncivilised unit lines
    (`#unciv_light_armament = gunpowder_weapons`, `#unciv_artillery = early_light_artillery`)
    **commented out**, which is the signature of a deliberate switch from uncivilised to
    civilised rather than an oversight.
  - The flavour decisions apply civilised-only political reforms (`political_reform = landed_voting
    / censored_press / harassment / appointed`), which an uncivilised tag cannot use.
- Changed: nothing. Flipping `civilized` would be a balance decision affecting research,
  westernisation and the Great Game, not a factual correction, and there is no evidence in the
  scripts that it was accidental.

## 8. Sanity check: FRA, PRU, AUS, RUS - all correct at 1821.9.1. No change.

- **FRA** - `prussian_constitutionalism2`, `ruling_party = FRA_conservative_6`
  (localised **"Constitutionnel"**, defined 1820.1.1-1830.7.1), `landed_voting`, `censored_press`,
  `last_election = 1819.6.21`, `set_country_flag = conservative_election_win`.
  `docs/audit/history-countries.md` suggested `FRA_reactionary_3` ("Ultraroyaliste") because of
  the Villele ministry - but **Villele only took office on 14 December 1821**; on 1 September 1821
  Richelieu's moderate-royalist ministry was still in place, resting on the Constitutionnels
  against the ultras. `FRA_conservative_6` is therefore right *for this start date*, and the
  Charte's `prussian_constitutionalism2` is the right shape. `decisions/France.txt` ->
  `constitution_suspended` accepts absolute_monarchy OR prussian_constitutionalism, so the ultra
  turn is reachable in-game. No change; the earlier audit note is superseded.
- **PRU** - `absolute_monarchy` + `PRU_conservative_2`, `none_voting`. Frederick William III never
  granted the promised constitution; correct.
- **AUS** - `absolute_monarchy` + `AUS_conservative`, `none_voting`. Metternich; correct.
- **RUS** - `absolute_monarchy3` + `RUS_conservative`, `none_voting`. Alexander I; correct. (The
  `socialist_democracy` the first audit flagged was a false positive - it sits inside a
  `govt_flag = { }` skin block, not the top-level government.)

---

## Verification

- `python scripts/audit_countries.py` - `COUNTS files=522 unregistered=39 no_culture=1 no_nv=1
  no_gov=1 no_party=1`; 39 `[high]` findings, all of them the known unregistered-tag files, and
  the four `no_*` are the REB placeholder. No `party_inactive`, `party_undefined`,
  `ideology_not_allowed_by_government` or `capital_not_owned` findings.
- `python scripts/audit_countries.py --key` - BAV now reads
  `gov=prussian_constitutionalism ideo=conservative party=BAY_conservative_2 fran=landed_voting`.
- `python scripts/modcheck.py braces "CoE_RoI_R/history/countries/BAV - Bavaria.txt"` - ok.
- `python scripts/modcheck.py tags "CoE_RoI_R/history/countries/BAV - Bavaria.txt"` - 0 unknown
  tag references.
- `python scripts/refcheck.py` - 132 problems in flags, unchanged from before the edit.
