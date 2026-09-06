# Design: restoring real pop religions

Status: **APPLIED, 2026-09-06 — steps 1-6 of §7 are done and committed; step 7 (deploy and
in-game smoke test) has not been run.** The owner chose the full restoration. Where this
document and `docs/design/religion-restoration-review.md` disagree the review was followed —
in particular §4.3's "restores a gate that has been off" framing is wrong (the sub-culture
triggers were live all along, so the conversion is 1:1), the site count is **121** not 115, and
there are **7** negated sites not 3. The accepted-culture table actually applied is the review's
§7, and the review's answers in its §10 are the answers to §8 below. Post-state and the
re-runnable gate (`python scripts/audit_religion.py check`, must stay at 0):
`docs/audit/religion-dead-content.md`. Changelog: `docs/CHANGELOG.md`, "Religion restoration".
Companion tool: `scripts/religion_restore.py` (dry-run by default; re-running it now reports
0 sub-culture moves). Prior analysis: `scripts/audit_religion.py`.

## 0. Executive summary

The 1821 pop files were mechanically transposed at some point: the real religion was pushed
into a trailing comment and the religion field was filled with the pop's culture or
sub-culture name. `common/religion.txt` was then extended with a copy of `common/cultures.txt`
so the values would parse.

Three facts make the restoration far cheaper than the earlier audit assumed:

1. **All 21 026 pop entries are losslessly recoverable.** 21 024 carry `#religion = <real
   religion>`; the remaining 2 are recoverable from git (`a3a51224`). No pop needs a religion
   guessed from province data.
2. **Every sub-culture is already a real culture in `common/cultures.txt`**, in the correct
   culture group. Nothing has to be added to `cultures.txt`. The earlier audit's claim that
   this needs "~257 new cultures" was wrong: only 10 sub-cultures actually appear in pop data
   and all 10 are already defined.
3. **The target state is vanilla's.** Vanilla `history/pops/1836.1.1` uses exactly
   `north_german/protestant`, `south_german/catholic`, `north_italian/catholic`,
   `dixie/protestant`, `anglo_canadian/protestant`, … The restoration returns the mod's data
   to the shape the engine and vanilla content were built for.

The real work is not the pop files (one scripted pass). It is (a) the 37 German and 16 Italian
country files whose `primary_culture = german` / `= italian` would be left with **zero** pops,
and (b) the mechanical rewrite of 115 sub-culture triggers from the religion form to the
culture form.

## 1. Inventory

Source: `python scripts/religion_restore.py` over `CoE_RoI_R/history/pops/1821.9.1`
(62 files, all pure CRLF, cp1252).

| measure | value |
|---|---|
| pop entries (one `culture` + one `religion` line each) | **21 026** |
| entries with `#religion = <real religion>` recoverable from the comment | **21 024** |
| entries with no commented religion | **2** |
| entries with `#culture = <sub-culture>` | **1 794** |
| entries whose religion field differs from the live culture field | **1 910** |
| fully-commented pop blocks (ignored by the tool) | 156 lines, 0 live entries |
| lines the rewrite touches | **22 936** in **61** of 62 files |

### 1.1 The two unrecoverable pops

Both were collateral of the 2026-09-06 dead-negatives pass (commit `a3a51224`), which
overwrote the last two live real religions to make the data uniform. Git gives the originals,
so no province-religion inference is needed:

| file | pop | was | restore to |
|---|---|---|---|
| `history/pops/1821.9.1/India.txt:6970` (prov 1721) | `tamil` capitalists | `religion = sunni` | `sunni` |
| `history/pops/1821.9.1/Persia Afghanistan Baluchistan.txt:529` | `tabari` artisans | `religion = shiite` | `shiite` |

These are hard-coded in `EXPLICIT` in `scripts/religion_restore.py`. The tool also carries a
data-driven fallback chain (modal religion of the same culture in the same file, then mod-wide)
for any future gap, and **refuses to `--apply`** while any pop is still unresolved.

Vanilla cross-check (`D:\Steam\steamapps\common\Victoria 2\history\pops\1836.1.1`): vanilla
Tamil pops are hindu 48 / sunni 15 / catholic 7 / protestant 3, so a Muslim Tamil pop in
province 1721 is vanilla-plausible; `tabari` is a mod-only culture with no vanilla pops, and
every other tabari pop in this mod is commented `#religion = shiite`. Both git values are
therefore consistent with their surroundings, and no province-level religion source is
required.

### 1.2 Religions that become live

| religion | pops | | religion | pops |
|---|---|---|---|---|
| catholic | 4 915 | | shiite | 417 |
| animist | 3 998 | | theravada | 285 |
| sunni | 3 835 | | gelugpa | 205 |
| protestant | 2 656 | | shinto | 204 |
| orthodox | 1 704 | | coptic | 122 |
| mahayana | 1 530 | | sikh | 39 |
| jewish | 559 | | zoroastrian | 22 |
| hindu | 529 | | mormon | 4 |

All 16 are already defined in the first six groups of `common/religion.txt`
(`christian`, `muslim`, `jewish_group`, `zoroastrian_group`, `eastern`, `pagan`, lines 1-148)
with distinct icons 1-15 plus mod icons 17-19. `druze`, `ibadi` and `fetishist` stay defined
but unused by pops. No icon renumbering is needed.

### 1.3 Sub-culture moves

| religion-field value | live culture becomes | pops | recovered from |
|---|---|---|---|
| north_german | `german` -> `north_german` | 604 | `#culture =` comment |
| south_german | `german` -> `south_german` | 534 | comment |
| dixie | `yankee` -> `dixie` | 256 | comment |
| north_italian | `italian` -> `north_italian` | 206 | comment |
| south_italian | `italian` -> `south_italian` | 94 | comment |
| anglo_canadian | `british` -> `anglo_canadian` | 68 | **religion field** (no comment) |
| occitan | `french` -> `occitan` | 58 | comment |
| picard | `french` -> `picard` | 42 | comment |
| australian | `british` -> `australian` | 30 | **religion field** |
| anglo_african | `british` -> `anglo_african` | 18 | **religion field** |

Total 1 910 pops. The three British ones never had a `#culture =` twin because the transposer
only wrote one when the sub-culture was being *replaced*; for them the sub-culture survives
only in the religion field, and the tool takes it from there.

### 1.4 Culture population, before -> after

| culture | before | after | |
|---|---|---|---|
| german | 1 138 | **0** | primary culture of 37 tags |
| italian | 300 | **0** | primary culture of 16 tags |
| north_german | 0 | 604 | |
| south_german | 0 | 534 | |
| north_italian | 0 | 206 | |
| south_italian | 0 | 94 | |
| yankee | 563 | 307 | |
| dixie | 0 | 256 | |
| british | 506 | 390 | |
| french | 501 | 401 | |
| occitan / picard | 0 | 58 / 42 | |
| anglo_canadian / australian / anglo_african | 0 | 68 / 30 / 18 | |

`german` and `italian` being emptied is the single biggest consequence of the change and drives
section 3.

## 2. common/cultures.txt

**No change required.** All 272 cultures stay. The 10 sub-cultures already exist in the right
groups:

| culture | group | union |
|---|---|---|
| north_german, south_german | `germanic` | GER |
| north_italian, south_italian | `italian` | ITA |
| occitan, picard | `french` | (none) |
| yankee, dixie | `american_cultures` | USA |
| anglo_canadian, australian, anglo_african | `neo_european_cultures` | (none) |

Consequences worth naming:

- `is_culture_group = germanic` / `= italian` keeps matching, so the German and Italian
  unification chains (which are written against culture groups, not cultures) are unaffected.
- The cultural-union tags (GER, ITA, USA) are attached to the *group*, so union mechanics,
  `cultural_union` scope and pan-nationalist rebels are unaffected.
- `anglo_canadian`/`australian`/`anglo_african` are in `neo_european_cultures`, which is a
  **different group from `british`** and has no union. Under ENG (`primary_culture = british`)
  those 116 pops become non-accepted, raising militancy/consciousness in Canada, Australia and
  the Cape. This is exactly vanilla behaviour (vanilla ENG likewise does not accept
  anglo_canadian at 1836), but it is a live change for this mod and must be smoke-tested.

## 3. history/countries: primary and accepted cultures

Any tag whose `primary_culture` is emptied must be repointed. The mod already records the
intended sub-culture per tag as a country flag `<subculture>_rel`, set in the history file, so
the mapping is unambiguous and needs no judgement calls.

| flag | tags | action |
|---|---|---|
| `north_german_rel` (26) | ANH BRA BRE COB DZG FRM GER HAM HAN HEK HES HOL LIP LUB LUX MEC MEI NAS NGF OLD PRU RHI SAX SWH WEI WES | `primary_culture = north_german`; add `culture = south_german` for PRU, GER, NGF (vanilla does this for PRU and GER) |
| `south_german_rel` (11) | ALS AUS BAD BAN BAV DNB KUK SAA SGF SWI WUR | `primary_culture = south_german`; add `culture = north_german` for SGF, KUK |
| `north_italian_rel` (13) | CRS ITA LBY LOM LUC MOD PAR RMG SAR SVY TRE TUS VEN | `primary_culture = north_italian`; add `culture = south_italian` for ITA |
| `south_italian_rel` (3) | PAP SIC SRD | `primary_culture = south_italian`; add `culture = north_italian` for PAP (vanilla does this) |

Vanilla reference values, for comparison: PRU `north_german` + accepted `south_german`;
BAV/AUS `south_german`; GER `north_german` + `south_german`; SAR/TUS `north_italian`;
SIC `south_italian`; PAP `south_italian` + `north_italian`; ITA `north_italian` +
`south_italian`.

Tags that do **not** need a change but should be reviewed:

- `yankee_rel` (21 US-state tags + USA) and `dixie_rel` (14 + CSA) already use
  `primary_culture = yankee`; both cultures keep pops. USA should gain `culture = dixie`
  (vanilla has it) so the 256 dixie pops are accepted before the ACW; CSA
  (`primary_culture = yankee`, flag `dixie_rel`) should become `primary_culture = dixie` with
  `culture = yankee` accepted, matching the ACW content.
- `anglo_canadian_rel` (CAN COL MRU NEW RPL): CAN already sets `primary_culture = british`
  plus `culture = french_canadian`; vanilla uses `primary_culture = anglo_canadian`. Either
  keep `british` primary and add `culture = anglo_canadian`, or follow vanilla. Recommend
  following vanilla for CAN and adding `culture = anglo_canadian` to ENG-tier releasables.
- `occitan_rel` (OCC): `primary_culture = french` -> `occitan`, keep `culture = french`.
- AST (Australia) and any Cape/South-Africa release tag have no `_rel` flag; they need
  `culture = australian` / `culture = anglo_african` added, or the same militancy spike as
  under ENG.
- `picard` has no `_rel` flag and no tag of its own; the 42 pops stay non-accepted under FRA
  unless FRA gains `culture = picard`. Vanilla has no picard culture at all, so the mod is
  free here; recommend FRA accepting both `occitan` and `picard` at start to avoid an
  unhistorical 1821 nationalism spike in the Midi and Picardy.

### 3.1 Script sites that name `german` / `italian` as a culture

32 live sites; each breaks silently (never true / no-op) once those cultures have no pops.
They divide cleanly:

| kind | sites | fix |
|---|---|---|
| `add_accepted_culture = german` | `events/1german_revolution_1848.txt` 142, 356, 462, 578, 812, 911, 1020, 1370, 1449; `events/NationalUnification.txt:652`; `decisions/AUS.txt` 147, 727; `decisions/NationalUnification.txt` 380, 545, 720 | replace with two effects, `add_accepted_culture = north_german` + `= south_german` (or the single one the surrounding tag actually lacks) |
| `add_accepted_culture = italian` | `events/ITAFlavor.txt:1341`; `events/NationalUnification.txt:311`; `decisions/NationalUnification.txt:875` | -> `north_italian` + `south_italian` |
| `primary_culture = german` (trigger) | `decisions/AUS.txt` 253, 1423; `decisions/France.txt:237`; `decisions/Italy.txt:1334` | -> `OR = { primary_culture = north_german primary_culture = south_german }`, or `is_culture_group = germanic` where the intent is "any German state" |
| `primary_culture = italian` (trigger) | `events/ITAFlavor.txt` 415, 533, 985; `decisions/Italy.txt:1307`; `decisions/ItalyOutsideUnification.txt:50` | -> `is_culture_group = italian` |
| `has_pop_culture = german` | `decisions/AUS.txt:719`; `decisions/RUS.txt` 675, 676 | -> add `has_pop_culture = north_german` / `= south_german` alongside (RUS 675 is inside a `NOT = { … }`, i.e. a NOR: adding the two sub-cultures to the same block preserves the intent) |
| `culture = italian` (province majority) | `events/AUSFlavor.txt:1073`; `decisions/AUS.txt:54` | -> `OR = { culture = north_italian culture = south_italian }` |

`british`, `french` and `yankee` keep pops, so the other 45 culture sites naming them need no
change — but note that their pop counts drop (british 506->390, french 501->401,
yankee 563->307), so any site written as "majority" may flip in border provinces.

## 4. Trigger conversion table

115 **live** sub-culture religion sites in 29 files (the "128" figure in the brief includes 13
already-commented lines, which need no work). Counted by key: `has_pop_religion` 90,
`religion` 25, `pop_majority_religion` 0.

### 4.1 Conversion rules

Per `docs/wiki/list-of-conditions.md`, the pop-scope section:

| from | scope | to | exact? |
|---|---|---|---|
| `has_pop_religion = X` | country / state / province / pop | `has_pop_culture = X` | **yes** — same "any pop in scope has X" semantics |
| `religion = X` inside `any_pop = { limit = { … } }` | pop | `has_pop_culture = X` | **yes** |
| `religion = X` inside `any_owned_province` / `any_core` / `all_core` / `any_owned` | province | `culture = X` | **yes** — both mean "majority of the province is X" |
| `pop_majority_religion = X` | country / state / province | `pop_majority_culture = X` | yes (no sub-culture site uses it) |

Do **not** convert pop-scope `religion = X` to pop-scope `culture = X`: in pop scope
`culture = X` means "the pop's *province* has an X majority", and pop-scope `religion = X`
means "the pop's cultural-union country has state religion X" — neither is the pop's own
value. `has_pop_culture` is the only exact target inside a pop `limit`.

### 4.2 Sites, by file

`has_pop_religion = X` -> `has_pop_culture = X` (90 sites), all 1:1, no semantic caveat:

| file | lines |
|---|---|
| `events/MEXFlavor.txt` | 496, 2035, 2042, 2049, 2056, 2063, 2070, 2077, 2084, 2091, 2098, 2105, 2241, 2248, 2255, 2262, 2269, 2276 (all `dixie`) |
| `events/CANFlavor.txt` | 43, 443, 885, 1104, 1532, 1655, 1977, 2005 (`anglo_canadian`) |
| `events/ACW.txt` | 402, 418, 488, 503, 2297, 2311, 2881, 3132 (`dixie`/`yankee`) |
| `decisions/Italy.txt` | 483, 484, 871, 938, 939, 977, 1153, 1229, 1230 |
| `events/ITAFlavor.txt` | 604, 605, 641, 642, 682, 683, 729, 730 |
| `events/AUSFlavor.txt` | 394, 1089, 1128, 1191, **1196** |
| `events/PRUFlavor.txt` | 94, 98, 454, 458 |
| `events/LiberalRevolutions.txt` | 3864, 3952, 4007 |
| `decisions/ACW.txt` | 310, 792, 828 |
| `events/+education_RGO_b.txt` | 53, 55, 124, 126 (`yankee`/`dixie`) |
| `events/Alternative ACW.txt` | 647 |
| `events/BoerWar.txt` | 1229, 1270 (`anglo_african`) |
| `events/VIP Events.txt` | 300, 319 |
| `events/SWHFlavor.txt` | 118, 216 |
| `events/newEvents.txt` | 49, **94** |
| `events/1german_revolution_1848.txt` | 315, 316 |
| `events/ScandinavianEvents.txt` | 836 |
| `events/LOMFlavor.txt` | 42 |
| `events/FRAFlavor.txt` | 1067 |
| `decisions/AUS.txt` | 1645 |
| `decisions/NET.txt` | 472 |
| `decisions/ACW2_dec.txt` | 455 |
| `decisions/ItalyOutsideUnification.txt` | 36, 37 |

`religion = X` in a **pop** `limit` -> `has_pop_culture = X` (12 sites):

| file | lines |
|---|---|
| `events/+education_RGO_b.txt` | 34, 35, 46, 47, 105, 106, 117, 118 |
| `decisions/VIP Decisions.txt` | 161, 163 |
| `decisions/CSA.txt` | 132, 218 |
| `events/AUSFlavor.txt` | 3119 |

`religion = X` in a **province** scope -> `culture = X` (13 sites):

| file | lines | enclosing scope |
|---|---|---|
| `events/NationalUnification.txt` | 620, 627, 967, 983 | `any_owned_province` / `any_core` |
| `events/Alternative ACW.txt` | 518, 585, 667, 681 | `any_owned_province` |
| `events/Greater Germany.txt` | 1020, 1021 | `all_core = { limit = { OR = { … } } }` |
| `decisions/France.txt` | 500 | `any_owned = { limit = { OR = { … } } }` |
| `decisions/NationalUnification.txt` | **1119** | `any_country = { … any_owned … }` |

### 4.3 The three negated sites

These are the only ones where NOT/NOR semantics matter. All three are currently **always
true** (nothing has that "religion"), so converting them *restores a gate that has been off*.
Each needs a behaviour review, not just a text substitution:

| site | current | after conversion | note |
|---|---|---|---|
| `events/AUSFlavor.txt:1196` | `NOT = { has_pop_religion = north_italian }` — always true | `NOT = { has_pop_culture = north_italian }` | paired with line 1191 which selects north_italian provinces; the pair becomes a real if/else |
| `events/newEvents.txt:94` | `not = { has_pop_religion = dixie }` — always true | `not = { has_pop_culture = dixie }` | paired with line 49; lowercase `not` is accepted by the engine but should be normalised to `NOT` |
| `decisions/NationalUnification.txt:1119` | `NOT = { religion = north_german }` — always true, province scope | `NOT = { culture = north_german }` | sits in a block that already has `owner = { NOT = { is_culture_group = germanic } }`; check the two clauses are not now redundant, and remember `NOT = { a b }` is NOR |

### 4.4 Sites that become live for the first time

These test real religions and are currently dead. They start working the moment pops carry
religions again; nothing needs editing, but each is a behaviour change to smoke-test.

- 20 `is_state_religion` sites in `events/ColonialUprisings.txt`, `events/ExtraElectionEvents.txt`
  and `events/NationalistMovements.txt` (province and pop scope). Today no province ever has a
  religion matching its owner's state religion, so `is_state_religion = no` is universally true
  and `= yes` universally false. After restoration both flip to meaningful, which changes the
  colonial-uprising and election-event pools noticeably.
- `decisions/extra_decisions.txt:1179` — `pop_majority_religion = orthodox` (panslavism,
  targets TUR) starts matching.
- The remaining real-religion sites catalogued in `docs/audit/religion-dead-content.md` §3:
  107 in `events/DIM/PERFlavour_five_x.txt` (the whole Sunni/Shiite Persian mechanic),
  `events/Dungan.txt` positives (lines 61, 82, 209, 361 — the Hui become testable via
  `has_pop_religion = sunni` in Gansu/Shaanxi/Yunnan again), `events/MOR.txt`,
  `events/ENGFlavor.txt`, `events/BRZFlavor.txt`, `events/CHIFlavor.txt:3164`,
  `events/Taiping.txt`, `events/Sepoy rebellion.txt`, `events/PER_crises.txt`,
  `decisions/Germany.txt:364`, `decisions/RUS.txt:360`, `decisions/Italy.txt:441`.
  **This is the payoff of the whole exercise**: ~124 previously dead triggers come alive.
  Two of the deletions made in the 2026-09-06 pass should be reconsidered as part of this
  work: the `carlist_rebels` `NOT = { has_pop_religion = catholic }` modifier and the two
  `events/Dungan.txt` limits were removed *because* they were dead; with religions back they
  would have been correct. See §7 step 6.

## 5. common/religion.txt

Current file: 3 271 lines, 43 top-level groups, ~290 entries. Lines 1-148 are the six real
groups (`christian`, `muslim`, `jewish_group`, `zoroastrian_group`, `eastern`, `pagan`);
lines 150-3271 are a copy of `common/cultures.txt` with each culture turned into a religion
(`icon = 1`, culture colour, name lists commented out with `##`).

**Action: truncate the file after the `pagan` group** (delete `germanic = {` at line 150
through the end). Keep all 20 real religions: catholic, protestant, mormon, orthodox, coptic,
sunni, ibadi, shiite, druze, jewish, zoroastrian, mahayana, gelugpa, theravada, hindu, shinto,
sikh, animist and the six pagan `*_religion` entries.

Checks before and after:

- The truncation must land on a balanced brace: line 148 closes `pagan`. The `PostToolUse`
  brace check catches a mistake here immediately.
- Any state religion in `history/countries/*.txt` must still be defined. Per
  `docs/audit/religion-dead-content.md` §2 all 522 files use one of the real 16 plus `mormon`
  and `ibadi` — all kept. Re-run `scripts/audit_religion.py` to confirm zero `UNDEFINED`.
- Localisation: the culture-named religion keys are the same strings as the culture keys
  (`north_german;North German;…`), so removing the religions orphans nothing; the culture side
  keeps using them. No `.csv` edit needed. (`scripts/refcheck.py loc` will confirm.)
- Religion icons: the kept religions use icons 1-15, 17, 18, 19 and the existing
  `gfx/interface` religion strip already covers them. No renumber.
- Do the truncation **after** the pop rewrite, not before: while the pop files still carry
  culture-named religions the game would refuse to load.

## 6. Rebels, decisions, AI, crime, conversion

Checked file by file; the outcome is much quieter than expected.

- **Rebels** (`common/rebel_types.txt`): every one of the 20 rebel types sets
  `allow_all_religions = yes`, and no type uses `area`, `defection` or `independence` with a
  `religion` value. Restoring religions therefore does **not** change rebel membership or
  goals. The only rebel-relevant change is the *culture* split: `separatist_rebels` and
  `nationalist_rebels` use `area = nation_culture` with `allow_all_cultures = no`, and
  `nationalist_rebels` uses `independence = culture`. Splitting `german` into
  north/south_german and `italian` into north/south_italian therefore changes which tag
  nationalist rebels try to release in German and Italian provinces. Mitigated entirely by
  §3: as long as each state's primary/accepted cultures follow the `_rel` flags, its own pops
  stay accepted and no new separatists appear. Provinces held by a *foreign* power (Austrian
  Lombardy, Danish Holstein, French Alsace) are where behaviour genuinely shifts — and shifts
  towards the historically intended result.
- **Conversion**: `common/pop_types.txt` sets `conversion_chance = { factor = 0.00 ; modifier
  = { factor = -100.0 always = yes } }` with every real modifier commented out. Conversion is
  hard-disabled mod-wide, so restoring religions will **not** cause Catholic pops to convert in
  Protestant Prussia. If that is wanted later it is a separate, deliberate change.
- **Assimilation**: the mod defines no `assimilation_chance`, so the engine default applies.
  The engine is known to slow or block assimilation across a religion boundary; with 16 real
  religions in play this becomes active for the first time. Verify in game (Habsburg lands and
  the Ottoman Balkans are the visible cases) before deciding whether to add an explicit
  `assimilation_chance` block.
- **Militancy**: `common/pop_types.txt:88` has `modifier = { factor = -0.1 NOT = { religion =
  THIS } country = { religious_policy = moralism } }`. Today `religion = THIS` compares a
  culture name against the state religion and never matches, so the -0.1 applies to every pop
  under moralism. After restoration it applies only to religious minorities — a small but
  real, and correct, change.
- **Issues / reforms**: `common/issues.txt` defines `religious_policy` with `pro_atheism /
  secularized / pluralism / moralism` but no religion-name triggers. No change.
- **Crime, national_focus, triggered_modifiers, static_modifiers, nationalvalues,
  cb_types, inventions, technologies**: grepped, zero religion-name references. No change.
- **AI**: no `common/ai/` religion weighting exists in this mod. Party and government
  definitions in `common/countries/*.txt` carry no religion. No change.

## 7. Execution plan

Each step is independently committable and independently verifiable. Do **not** collapse
steps 1-3 into one commit: if the game fails to start, the split tells you which half broke it.

1. **Baseline.** Note the size of
   `E:\OneDrive\Documents\Paradox Interactive\Victoria II\CoE_RoI_R\logs\error.log`.
   Record the current output of `python scripts/audit_religion.py`,
   `python scripts/refcheck.py`, `python scripts/modcheck.py encoding`.

2. **Pop files.** `python scripts/religion_restore.py` (dry run) then `--apply`.
   Expect 22 936 lines in 61 files. Verify:
   - `python scripts/modcheck.py encoding` — still cp1252 + CRLF, no BOM.
   - brace balance on all 62 files (the `PostToolUse` hook does not fire for script writes, so
     run `python scripts/modcheck.py braces "CoE_RoI_R/history/pops/1821.9.1/"*.txt`
     explicitly).
   - `git diff --stat` shows only `history/pops/1821.9.1/`, and `git diff` shows only
     `culture =` / `religion =` lines.
   - Re-run `scripts/religion_restore.py`: it must now report 0 sub-culture moves and
     0 commented religions.

3. **history/countries.** Apply §3: repoint `primary_culture` for the 53 German/Italian tags
   from the `_rel` flags, add the accepted cultures listed, review CSA/USA/CAN/AST/OCC/FRA.
   Verify with `python scripts/audit_countries.py` (it checks primary cultures and ruling
   parties) and `python scripts/refcheck.py names` (unknown cultures/religions).

4. **Triggers.** Apply §4.2 — 90 `has_pop_religion` -> `has_pop_culture`, 12 pop-scope
   `religion` -> `has_pop_culture`, 13 province-scope `religion` -> `culture`. This is
   mechanical enough to script, but the three negated sites in §4.3 and the 32 `german`/
   `italian` culture sites in §3.1 must be done by hand. Verify with
   `python scripts/refcheck.py names` and `python scripts/audit_events.py` (unknown
   trigger/effect keywords), plus `python scripts/cwtools_check.py`.

5. **common/religion.txt.** Truncate per §5. Verify: brace balance,
   `python scripts/audit_religion.py` reports 0 `UNDEFINED` state religions and 0 pops holding
   a culture name, `python scripts/audit_common.py`.

6. **Revisit the 2026-09-06 deletions.** Restore the `carlist_rebels` catholic gate and the
   two `events/Dungan.txt` sunni limits that were removed as dead code (see
   `docs/audit/religion-dead-content.md` §5), now that they work. Update that audit file's
   "Fixed" and "Still open" sections and re-run `scripts/audit_religion.py` to regenerate the
   generated part.

7. **Deploy and smoke test.** `pwsh -File scripts/deploy.ps1`, launch, start at the 1821
   bookmark, read the new `error.log` tail. Check specifically:
   - the game reaches the map at all (a bad religion.txt truncation is a startup crash);
   - Prussia, Bavaria, Austria, Sardinia, Two Sicilies, USA, UK, France show sane
     accepted-culture and militancy numbers on day 1 (no red nationalism in Bavaria or Canada);
   - the religion pie in the population screen shows a plausible mix, not one slice;
   - run a year on observer and diff the error log.

8. **Follow-ups, separate passes.** The Persian Sunni/Shiite chain
   (`events/DIM/PERFlavour_five_x.txt`, 107 sites) now works and needs balance review; the
   `is_state_religion` events in §4.4 need a pacing pass (`python scripts/audit_pacing.py`);
   decide whether to re-enable `conversion_chance`. Add a `docs/CHANGELOG.md` entry.

## 8. Open questions for the owner

1. **Accepted-culture policy for the German and Italian states.** Vanilla gives PRU
   `north_german` + accepted `south_german` but gives BAV/AUS only `south_german`. Mirror
   vanilla, or make every German state accept both sub-cultures (gentler, less historical)?
2. **CAN, AST and the Cape.** Follow vanilla (`anglo_canadian` primary for CAN, non-accepted
   under ENG) and take the militancy, or have ENG accept all three neo-European cultures?
3. **occitan / picard.** Should FRA accept them at 1821? They are a mod addition with no
   vanilla precedent, and 100 non-accepted pops in metropolitan France at start is a design
   choice, not a data fact.
4. **Conversion.** Leave `conversion_chance` hard-disabled (recommended for this pass), or
   re-enable it now that religions are real?
5. **Scope of step 6.** Re-instate the three deletions from the 2026-09-06 pass, or leave them
   removed and treat the Carlist/Dungan gates as deliberately simplified?
