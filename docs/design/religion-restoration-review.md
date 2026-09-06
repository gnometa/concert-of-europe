# Adversarial review: `docs/design/religion-restoration.md`

Reviewed against `docs/design/religion-restoration.md` and `scripts/religion_restore.py` at
commit `6597d534`. Line numbers under `events/` and `decisions/` were read from the working
tree while an unrelated `audit_common` pass was in flight, so re-grep before editing rather
than trusting a number blind.

**Verdict: the tool is sound and `--apply` is safe to run. The plan around it has five defects,
two of them blocking.** The most serious is not a missing edit — it is that §4.3/§4.4 reason
about the sub-culture triggers in the wrong direction, which makes the whole "restores a gate
that has been off" framing wrong and hides where the real risk is.

---

## 0. The framing error, first, because everything else depends on it

§4.3 says of the negated sub-culture sites: *"All three are currently **always true** (nothing
has that 'religion'), so converting them restores a gate that has been off."*

That is backwards. Verified:

- `CoE_RoI_R/common/religion.txt:466` defines `north_italian` **as a religion** (as §5 itself
  says: lines 150-3271 are a copy of `cultures.txt`).
- `CoE_RoI_R/history/pops/1821.9.1/Italy.txt:7` is `religion = north_italian #religion = catholic`.

So `has_pop_religion = north_italian` **matches today**. All 121 sub-culture sites are *live,
working gates right now*. The conversion to `has_pop_culture` / `culture` is therefore
**behaviour-preserving 1:1**, not a restoration — the pops keep the same value, it just moves
from the religion field to the culture field and the trigger key moves with it.

Two consequences the design gets wrong as a result:

1. **The negated sites need no behaviour review at all** — provided they are converted. §4.3's
   "each needs a behaviour review, not just a text substitution" is wasted effort.
2. **A *missed* site is the entire risk, and a missed *negated* site is catastrophic rather
   than merely inert.** A missed positive site silently no-ops; a missed negated site becomes
   universally true and switches a gate **off**. §7 step 4 must therefore be driven by an
   exhaustive sweep, not by the hand-written table — which is short by 7 (§3 below).

The §4.4 claim *is* correct, because it concerns **real** religions (`catholic`, `sunni`, …),
which no pop carries today. `is_state_religion` really is universally false today. Keep §4.4;
discard §4.3's reasoning.

---

## 1. `scripts/religion_restore.py` — no defects found

Dry run reproduces the design exactly: 21 026 entries, 21 024 from comments, 2 explicit,
0 unresolved, 0 orphans, 1 910 sub-culture moves, 22 936 lines in 61 files, both validation
lines `none`.

| attack | result |
|---|---|
| lines the regexes silently skip | **0.** All 21 026 live `culture =` and all 21 026 live `religion =` lines match `CULTURE_RE`/`RELIGION_RE`; a strict re-implementation of the two patterns finds no exception. No line carries a second trailing comment that would make the match fail and drop a pop. |
| culture/religion mis-pairing across blocks (a live `culture` whose `religion` twin is commented out would pair with the *next* block's religion) | **0.** A state-machine pass over all 62 files finds no `culture` not immediately followed by a `religion` and no `religion` without a preceding `culture`. `orphans = 0` corroborates. |
| fully-commented pop blocks leaking in | Correct: 78 `#culture =` lines start with `#`, and `^(\s*)culture` cannot match them. Worth knowing that those dead blocks carry culture-named religions the live data no longer has (`ashkenazi`, `sephardic`, `ukrainian`, `mongol`, `north_caucasian` — `history/pops/1821.9.1/Russia.txt:6928-7070`). Harmless while commented; do not uncomment them after §5. |
| CRLF | Safe. `read_text` hard-aborts on a bare LF; `split("\r\n")` / `"\r\n".join` round-trips the trailing newline exactly. |
| ASCII / encoding | Safe. cp1252 in, cp1252 out; a byte outside cp1252 raises on decode. `python scripts/modcheck.py encoding CoE_RoI_R/history/pops` is clean today, so the round-trip is a no-op on every byte not deliberately changed. Rewritten values are `\w+` tokens lifted from the file, so ASCII by construction. |
| indentation | Preserved verbatim via `cul_ind`/`rel_ind`. Trailing whitespace is dropped — cosmetic. |
| a pop with **both** a `#culture` twin and a no-twin British sub-culture (the twin would win, the sub-culture would be lost) | **0 collisions.** 1 794 lines have a `#culture` twin; 116 lines carry `anglo_canadian`/`australian`/`anglo_african` in the religion field; 1 794 + 116 = 1 910 = the exact count of culture lines that change. Disjoint sets. |
| the two India/Persia pops | Correct values, applied only where intended: the `rel_com` branch returns before `EXPLICIT` is consulted, so the coarse `(basename, live culture)` key hits exactly `India.txt:6970` and `Persia Afghanistan Baluchistan.txt:529`. A `(file, line)` key would be tighter but is not needed. |

Two non-blocking nits:

- `by_file_modal` is keyed on the **old** culture, `global_modal` on the **new** culture.
  Inconsistent; dead today (0 fallbacks reach either) but will bite if a comment is ever lost.
- **The `--apply` "undefined religion" guard is vacuous.** It checks against
  `common/religion.txt`, which still contains every culture as a religion, so it cannot fail.
  Do not read the `religions used after restore: none` line as validation of the
  post-truncation state.

---

## 2. The 53 `primary_culture` changes

**No missing and no ambiguous `_rel` flag.** Every one of the 53 German/Italian tags carries
exactly one flag; none carries two. An independent sweep of `CoE_RoI_R/history/countries/*.txt`
reproduces the design's four tag lists exactly (26 / 11 / 13 / 3). Tree-wide flag counts:
north_german 26, south_german 11, north_italian 13, south_italian 3, yankee 21, dixie 14,
anglo_canadian 5, occitan 1; `picard`, `australian`, `anglo_african` have none, as the design
says.

### [BLOCKING] Three accepted-culture lines die and appear nowhere in the design

`grep -rnE "^\s*culture\s*=\s*(german|italian)\s*$" CoE_RoI_R/history/`:

| file:line | today | after |
|---|---|---|
| `CoE_RoI_R/history/countries/PAP - Papal States.txt:3` | `culture = italian` (already redundant — primary is also `italian`) | dead; PAP needs `culture = north_italian` (which §3 does say, but as a new line, not as a replacement) |
| `CoE_RoI_R/history/countries/SWI - Switzerland.txt:4` | `culture = italian` — **Ticino**, a genuine accepted minority | dead. §3 changes SWI's primary to `south_german` and says nothing about this line. Needs `culture = north_italian`. |
| `CoE_RoI_R/history/countries/DLM - Dalmatia.txt:3` | `culture = italian`, primary `croat` | dead. **DLM has no `_rel` flag and is not mentioned anywhere in the design.** Needs `culture = north_italian`. |

DLM is the instructive one: it is invisible to the `_rel`-flag method because its *primary*
culture is fine — only its *accepted* culture dies. Step 3 needs the
`grep history/ for 'culture = german|italian'` check added alongside the flag walk, or the same
class of tag will be missed again.

### [MEDIUM] Downstream

- **`change_tag` does not re-apply the target tag's history cultures.** Vanilla proves it by
  adding both sub-cultures explicitly after `change_tag = GER`
  (`D:\Steam\steamapps\common\Victoria 2\decisions\NationalUnification.txt:276-277`, and 323-324
  for Italy). Fixing `history/countries/GER - Germany.txt` is necessary but not sufficient — the
  `add_accepted_culture` effects in §3.1 must land in the same pass, and the *pre-formation*
  tags (PRU/NGF/SGF/AUS/SAR/SIC) are what actually determine what a formed GER/ITA accepts.
- **`nationalist_rebels` uses `independence = culture` with `allow_all_cultures = no`**
  (`common/rebel_types.txt:1489-1532`). After the split, 26 tags share
  `primary_culture = north_german`; which one north-German nationalists in Danish Holstein or
  French Alsace release is engine-chosen. Risk, not defect — smoke-test it.
- **USA/CSA is required, not optional.** 14 southern state tags and CSA carry `dixie_rel` but
  `primary_culture = yankee`, and USA has no accepted-culture line at all. 256 restored `dixie`
  pop entries go non-accepted under USA on day one without the fix.

### [LOW] Steps 2 and 3 are committable separately but not *playable* separately

Between them, every German and Italian state has 0% accepted population. The design should say
"do not deploy or smoke-test between step 2 and step 3" explicitly.

---

## 3. [BLOCKING] The trigger inventory is short by 7 sites

A brace-aware sweep of `events/` + `decisions/` for
`(has_pop_religion|pop_majority_religion|religion) = <culture name that is not one of the 18
kept religions>`, outside comments, finds **121 live sites**, not 115. Missing from §4.2:

| file | lines | key | why it was missed / why it matters |
|---|---|---|---|
| `CoE_RoI_R/events/+education_RGO_b.txt` | 44, 45, 48, 115, 116, 119 | `religion = french`, `= breton`, `= wallonian` | **Full cultures, not sub-cultures**, so the design's "sub-culture" filter skipped them. They sit in `any_pop = { limit = { … } literacy = X }` immediately beside `religion = occitan` / `= picard`, which §4.2 *does* list — i.e. half of one block is scheduled for conversion and half is not. |
| `CoE_RoI_R/events/AUSFlavor.txt` | 1268 | `has_pop_religion = north_italian` | plain omission. It is in the `"Never!"` option of the Lombardy event, two lines above an `any_owned = { limit = { culture = north_italian } }` that is already in culture form. |

The consequence is a **hard load error, not a silent no-op**: §5 truncates
`common/religion.txt` so `french`, `breton`, `wallonian`, `north_italian` … are no longer
defined religions. Anything left in religion form after step 4 becomes an undefined-religion
reference at load. **Gate step 5 on "the 121-site sweep returns 0 hits", not on the §4.2 table.**

### 3a. Sites whose conversion is load-bearing and is not flagged as such

- **`CoE_RoI_R/events/NationalUnification.txt:620, 627`** are inside the **`trigger` block of
  event `11107`** (`id = 11107`, `trigger = { … tag = NGF any_owned_province = { is_core = GER
  religion = south_german } … }`), not inside an effect `limit`. This is the NGF/SGF → GER
  pan-nationalist path. Miss it and the event never fires again; the design lists the lines in a
  flat table with everything else.
- **The 7 negated sites** (see 3b) — a miss there switches a gate off rather than making an
  effect inert.

### 3b. There are 7 negated sites, not 3

Brace-depth-aware scan (tracking an enclosing `NOT`/`not` frame, not a 3-line lookback):

| site | stack | in §4.3? |
|---|---|---|
| `decisions/ItalyOutsideUnification.txt:36, 37` | `allow/ITA/all_core/OR/NOT/OR` | **no** |
| `decisions/NationalUnification.txt:1119` | `form_north_german_confederation2/allow/GER/all_core/OR/NOT` | yes |
| `events/AUSFlavor.txt:1196` | `option/any_pop/limit/NOT` | yes |
| `events/Alternative ACW.txt:667, 681` | `any_state/limit/NOT/any_owned_province/OR` | **no** |
| `events/newEvents.txt:94` | `option/any_owned/state_scope/any_pop/limit/not` | yes (normalise `not` -> `NOT`) |

All four unlisted ones are inside `allow`-style `all_core` / `any_state` gates — the exact
class where "always true" silently disables a requirement:

- `decisions/ItalyOutsideUnification.txt:24-41`, decision `outside_form_italy`:
  `allow = { war = no  ITA = { all_core = { OR = { OR = { owned_by = THIS owner = { in_sphere = THIS } }  NOT = { OR = { has_pop_religion = north_italian has_pop_religion = south_italian } } } } } }`.
  If this is left unconverted, the `NOT` becomes universally true, the `all_core` passes with
  **zero territory**, and the only remaining gate is `war = no`. The effect is
  `any_country = { limit = { primary_culture = italian in_sphere = THIS } annex_to = THIS }` +
  `release_vassal = ITA`. Reachable within a few years of 1821 by e.g. France sphering Sardinia.
- `decisions/NationalUnification.txt:1088-1124`, `form_north_german_confederation2`: same shape;
  unconverted, a germanic GP forms NGF owning nothing.
- `events/Alternative ACW.txt:667, 681`: unconverted,
  `NOT = { any_owned_province = { OR = { religion = dixie is_core = TEX } } }` collapses to
  `NOT = { … is_core = TEX }` and `any_owned = { remove_core = CSA }` strips CSA cores from
  nearly every state.

Note `decisions/NationalUnification.txt:1119` is **province-scope `religion`**, which is not a
documented trigger (see §4) — its current truth value is genuinely unknown. Treat it as the one
site that needs in-game confirmation.

---

## 4. Trigger semantics

The conversion table in §4.1 is correct except for one row.

- `has_pop_religion = X` -> `has_pop_culture = X` at country/state/province/pop scope: **safe.**
  `docs/wiki/list-of-conditions.md` documents both only under Pop Scope (`:2836`, `:2848`), but
  `has_pop_culture` is demonstrably a country-scope trigger in vanilla —
  `D:\Steam\steamapps\common\Victoria 2\decisions\ACW.txt:302, 640, 710` use it in decision
  `potential` blocks — and this mod already does so in ~200 places.
- `pop_majority_culture` **exists** (`list-of-conditions.md:1439` country scope, `:2998` pop
  scope), so that row is fine, though no sub-culture site uses `pop_majority_religion`. The one
  live `pop_majority_religion` in the mod is `decisions/extra_decisions.txt:1179`
  (`pop_majority_religion = orthodox`, panslavism), a real religion — §4.4 material.
- Pop-scope `religion = X` -> `has_pop_culture = X`: **correct and well-argued.** Pop-scope
  `religion` means "the pop's cultural government has that state religion" and pop-scope
  `culture` means "the pop's *province* has a majority of that culture"; `has_pop_culture` is
  the only exact target. Good catch by the design.
- **[MEDIUM] Province-scope `religion = X` -> `culture = X` is asserted as "exact" but is
  unsupported.** The Province Scope section (`list-of-conditions.md:2094-2772`) defines neither
  `culture` nor `religion`; province-scope `culture` is documented only as an aside inside the
  *pop*-scope `culture` entry, and province-scope `religion` is not documented anywhere. So the
  13 province sites are not provably a rename — after conversion they are certainly a
  province-majority test, but what they are *today* is unknown. Confirm in game rather than by
  reading. There is no state-scope variant to worry about: all 13 sit inside
  `any_owned` / `any_owned_province` / `any_core` / `all_core`, all province iterators
  (`docs/wiki/list-of-scopes.md:11, 23, 59, 369`).

---

## 5. `culture = german|italian` at 32 script sites

Confirmed: exactly the 32 sites in §3.1, and none in `common/` — `cb_types.txt`,
`nationalvalues.txt` and `rebel_types.txt` carry no `german`/`italian` culture reference, and
`common/countries/*.txt` contains **no `primary_culture` key at all** (colour, graphical
culture, parties, unit names, government colours only).

| class | dead when? | correct fix |
|---|---|---|
| `add_accepted_culture = german` ×13, `= italian` ×3 | dead at step 2 | the two sub-cultures. Three already have the right line commented out beside them: `decisions/NationalUnification.txt:381, 546, 876`; `events/NationalUnification.txt:646`; `events/ITAFlavor.txt:1340` |
| `primary_culture = german/italian` as a **trigger** (`decisions/AUS.txt:253`, `decisions/France.txt:237`, `decisions/Italy.txt:1307, 1334`, `decisions/ItalyOutsideUnification.txt:50`, `events/ITAFlavor.txt:415, 533, 985`) | **not dead at step 2** — they read a country property — but dead at **step 3** | `is_culture_group = germanic` / `= italian`. That is strictly better than `OR = { primary_culture = north_x primary_culture = south_x }`, which would drop `russian_german`, `maltese`, `romansh`. `decisions/Italy.txt:1334` (`german_tyrol`) is the one case where the narrow `OR` is arguably right |
| `has_pop_culture = german` (`decisions/AUS.txt:719`, `decisions/RUS.txt:675, 676`) | dead at step 2 | add both sub-cultures to the same block; RUS 675 is a `NOT = { a b }` NOR, so same-block addition preserves intent |
| province-scope `culture = italian` (`events/AUSFlavor.txt:1073`, `decisions/AUS.txt:54`) | dead at step 2 | `OR = { culture = north_italian culture = south_italian }`. `AUSFlavor.txt:1073` is the Lombardy-independence trigger — user-visible |
| `primary_culture = <x>` as an **effect** (`decisions/AUS.txt:727, 1423`) | wrong value at step 3 | `south_german` |

Also worth listing in §3.1: `any_pop = { limit = { is_primary_culture = yes } }` matches zero
pops for any German/Italian tag between steps 2 and 3 —
`events/NationalUnification.txt:127, 235, 817, 1058` and `events/Greater Germany.txt:399, 454, 985`.
Step 3 repairs it automatically; it is another reason not to test between the two steps.

---

## 6. Unification: NGF / GER / SGF / ITA

**Union mechanics are unaffected, and the design is right about why.** `union = GER` sits at
`common/cultures.txt:84`, `union = ITA` at `:409`, `union = USA` at `:2328` — all at **group**
level, siblings of the culture blocks, so the sub-cultures inherit the union. Vanilla's own
1836 pop files contain **zero** `culture = german` and zero `culture = italian` pops; vanilla
GER is `north_german` primary + `south_german` accepted. Nothing in the union machinery counts
pops of a culture named `german`. `culture_has_union_tag`, `is_cultural_union`,
`change_tag = culture`, `add_accepted_culture = union` and the pan-nationalist content in
`events/PanNationalists.txt` all keep working.

Every formation gate survives, because none tests pop culture:

- `form_south_german_confederation` (`decisions/NationalUnification.txt:3-102`) and
  `form_north_german_confederation` (`:191-270`) gate on `has_country_flag = south_german_rel` /
  `north_german_rel`.
- `form_germany` / `form_germany2` / `form_germany_AUS` (`:335`, `:502`, `:667`) gate on
  `tag = NGF|SGF|AUS` plus core ownership.
- `form_italy` (`:821`) and `outside_form_italy` (`decisions/ItalyOutsideUnification.txt:8`)
  gate on `is_culture_group = italian`, a country trigger over the primary culture's *group* —
  `italian`, `north_italian` and `south_italian` are all in group `italian`, so it works before
  and after.
- `events/Greater Germany.txt` and `events/1german_revolution_1848.txt` use only
  `is_culture_group = germanic`, `is_primary_culture`, `is_accepted_culture`, `add_core`,
  `inherit`, `change_tag`. **No `add_core` anywhere is culture-conditioned.**
- `events/PanNationalists.txt` keys the German half on `has_country_flag = north_german_rel` /
  `south_german_rel` (`:360, 366, 394, 415, 427, 456, 482, 489, 491, 505, 514`) and the Italian
  half on `is_culture_group = italian` (`:161, 181, 205, 224, 243, 263`). Both survive.

**Direct answer to the question as posed:** yes, the union mechanics still work with
`north_german` pops and a union tag whose primary is `german` with 0 pops — because unions are
group-keyed, not culture-keyed. But such a tag is broken for every *other* reason (0% accepted
population), so it is not a state to ship. Mirror vanilla, per §7.

What actually breaks is the 16 `add_accepted_culture = german|italian` effects fired **at the
moment of formation** (§5) — and `events/NationalUnification.txt:620, 627` (§3a), which is the
only formation *trigger* in the whole set that touches a sub-culture.

---

## 7. Recommended accepted-culture table

Vanilla 1836 values from `D:\Steam\steamapps\common\Victoria 2\history\countries\`, quoted so
the deviations are visible.

| tag | vanilla 1836 | **recommendation** | note |
|---|---|---|---|
| PRU | `north_german` + `south_german` | same | |
| AUS | `south_german` | `south_german` only | do **not** add north_german — Austro-Prussian dualism content depends on Austria not being a north-German state |
| BAV | `south_german` | same | |
| GER | `north_german` + `south_german` | same, plus keep the mod's existing `russian_german` | |
| NGF | `north_german` + `south_german` | same | |
| SGF | `south_german` + `north_german` | same | |
| KUK | `south_german` + `hungarian` | `south_german` + `hungarian`, **no north_german** | §3 proposes north_german; vanilla does not, and KUK is Austria's successor |
| SAR | `north_italian` | same | |
| ITA | `north_italian` + `south_italian` | same | |
| SIC | `south_italian` | same | |
| PAP | `south_italian` + `north_italian` | same — **replacing** the dying `culture = italian` at line 3 | |
| SWI | (vanilla: `south_german` + `french` + `italian`) | `south_german` + `french` + `romansh` + **`north_italian`** | Ticino; the current `culture = italian` dies |
| DLM | n/a | `croat` + **`north_italian`** | not in the design at all |
| ENG | `british` + `anglo_canadian` | `british` + `anglo_canadian` **only** | see below |
| USA | `yankee` + `dixie` + `texan` | `yankee` + `dixie` (+ `texan` if the culture exists) | required, not optional |
| CSA | `dixie` + `texan` | `dixie` primary, `yankee` accepted | mod CSA is `yankee` + `dixie_rel`; must flip |
| CAN | `anglo_canadian` + `french_canadian` | follow vanilla | mod currently has `british` primary |
| FRA | `french` + `french_canadian` | + **`occitan`** + **`picard`** | see below |
| AST | `british` | `british` + **`australian`** | no `_rel` flag exists; 30 pop entries otherwise non-accepted |
| SAF | `british` + `boer` | mod is `boer` + `british`; add **`anglo_african`** | 18 pop entries |

**ENG: accept `anglo_canadian`, but *not* `australian` or `anglo_african`.** The brief's default
was to accept all three; I recommend against it:

1. Vanilla ENG accepts `anglo_canadian` and nothing else, and this mod's neo-European content
   (`events/CANFlavor.txt` 8 sites, `events/BoerWar.txt` 2, ASTFlavor) is written on the
   assumption that these populations are *distinct*. Accepting them under ENG makes the Canadian
   and Cape autonomy chains toothless.
2. `neo_european_cultures` (`common/cultures.txt:2331`) has **no union tag**, so accepted status
   is the only lever the release tags respond to.
3. Exposure is small and colonial: 68 + 30 + 18 = 116 pop entries.

**FRA: accept `occitan` and `picard`.** Mod-only cultures with no vanilla precedent; 100
non-accepted pop entries in metropolitan France at the 1821 start is an unhistorical Midi /
Picardy nationalism spike, and no content keys off their being non-accepted.
`events/+education_RGO_b.txt` already treats them as ordinary French regional populations
(literacy 0.25 / 0.21 against `french` 0.23).

---

## 8. Real-religion content going live

`history/countries/*.txt` sets **real religions everywhere** — 148 protestant, 115 sunni,
110 catholic, 36 animist, 27 hindu, 25 orthodox, 20 mahayana, 10 theravada, 8 shinto, 7 shiite,
6 coptic, 5 gelugpa, 1 each sikh/mormon/jewish/**ibadi**, and **zero** culture names. 521 of 522
files set one (only `REB - Rebels.txt` does not). So `is_state_religion` and `religion = THIS`
begin working with no history edits.

`history/provinces/**` carries **no `religion` field at all** (0 hits tree-wide) — province
religion is derived from pops. Nothing to migrate; the design should say so, since it is the
obvious place to go looking.

### [HIGH] `CoE_RoI_R/poptypes/` is missing from §6 entirely

§6 checks `common/issues.txt` and concludes "no religion-name triggers. No change." But the
religious-policy **issue weights** live in `poptypes/`, not `common/issues.txt`, and they use
`is_state_religion`:

- **48 `is_state_religion` sites**, 4 in each of 12 poptype files (`00_urban_poor`,
  `aristocrats`, `artisans`, `bureaucrats`, `capitalists`, `clergymen`, `clerks`, `craftsmen`,
  `farmers`, `labourers`, `officers`, `soldiers`; `slaves.txt` has none). E.g.
  `CoE_RoI_R/poptypes/farmers.txt:5043, 5053, 5076, 5102`:
  - `secularized = { factor = 1.25  modifier = { factor = 1.50  NOT = { is_state_religion = yes } } }`
    — applies to **every** pop today, to minorities only afterwards.
  - `moralism` and `pluralism` each carry `modifier = { factor = 1.25  is_state_religion = yes }`
    — **dead today**, applying to the majority afterwards.
  This is a mod-wide rebase of religious-policy pressure away from secularization on day one, in
  every country. Not a crash; a balance change that needs a deliberate look, and it is the single
  widest-reaching consequence of the whole pass.
- **10 `has_pop_religion = THIS` in `migration_target`** (e.g. `poptypes/farmers.txt:441`,
  `factor = 1.2`). Today it duplicates the culture check twenty lines above; afterwards it
  becomes real religious clustering and changes migration flows from 1821 onward.
- **20 `religion = jewish` / `religion = mormon`** in the same `migration_target` blocks
  (`poptypes/farmers.txt:464, 469`, gated on `is_core = ISR` / `is_core = DES`) — currently inert,
  becoming live.

### [MEDIUM] `common/pop_types.txt:88`

`modifier = { factor = -0.1  NOT = { religion = THIS }  country = { religious_policy = moralism } }`.
Today `religion = THIS` never matches, so every pop under moralism gets the -0.1 militancy;
afterwards only religious minorities do. Correct behaviour, global reach — put it on the
smoke-test list.

### [MEDIUM] Assimilation

The mod defines no `assimilation_chance`, so the engine default applies, and the engine
slows/blocks assimilation across a religion boundary. Active for the first time. Habsburg lands
and the Ottoman Balkans are the visible cases. Agreed with the design: test before deciding.

### [LOW] Nothing fires on day one because of restored religions

- **No real-religion name appears in any `trigger` / `potential` / `allow` /
  `mean_time_to_happen` block anywhere in `events/`, `decisions/`, `common/`, `inventions/`,
  `technologies/`.** Every one of the 200+ real-religion sites is a `limit = { … }` inside an
  effect. The only religion-based *gating* in the whole mod is `is_state_religion`, at 9 event
  sites (18 occurrences across `events/ColonialUprisings.txt`, `ExtraElectionEvents.txt`,
  `NationalistMovements.txt`).
- **`is_state_religion` changes make events rarer, not commoner.**
  `ColonialUprisings.txt:625-694` (id 14580, self-firing, mtth 200 months, no year gate, already
  firing from 1821): the trigger barely moves, option A's
  `any_pop = { limit = { is_state_religion = no } militancy = 5 }` **shrinks** from every pop in
  the state to the non-conforming ones, and option B's `= yes` limit stops being a guaranteed
  no-op. `NationalistMovements.txt:3589-3730` (id 15250, mtth 500 months) narrows sharply —
  Catholic Polish/Hungarian provinces under Catholic Austria stop qualifying.
  `ExtraElectionEvents.txt:3295-3395` (140801) and `:3398-3503` (140901) are completely dead
  today and become eligible in the `religious_policy` election pool; both are
  `is_triggered_only` and commented out of `common/on_actions.txt:78-79`, so they enter only via
  the engine election pool, and there are few elections in the 1820s.
- **The Persian chain is not a day-one hazard.** `events/DIM/PERFlavour_five_x.txt` has 155
  `has_pop_religion` sites (57 shiite / 57 sunni / 46 ibadi / 2 zoroastrian / 2 jewish), **all in
  effect `limit`s, none in a trigger**. The earliest self-firers are `190341`/`190342`
  (`year = 1832`) and `190345` (`year = 1836`); the rest are `year = 1844+` or flag-gated
  (`bab_has_appeared`, `tobacco_regie_accepted`, `naser_al_din`, …), all `tag = PER`, nearly all
  `fire_only_once = yes`. Balance review later, no gate now.
- **Mass conversion cannot happen.** `common/pop_types.txt:3506-3510` hard-disables it
  (`conversion_chance = { factor = 0.00  modifier = { factor = -100.0  always = yes } }`).
  Confirmed.
- **Rebels are unaffected.** Every type in `common/rebel_types.txt` sets
  `allow_all_religions = yes`; none uses `area = religion|nation_religion` or
  `independence = religion`. Confirmed.
- **Crime, national values, triggered/static modifiers, issues, on_actions, cb_types,
  `common/ai/`, `common/countries/*.txt`**: zero religion-name references. Confirmed.
- In-window but harmless: `events/MOR.txt` id 290100 (`tag = MOR  year = 1834`, `fire_only_once`)
  — Sol Hachuel's `religion = jewish` / `= sunni` limits become live. Mid-game and flag-gated:
  `events/Dungan.txt` 80120/80122/80126 (note `any_pop = { limit = { has_pop_religion = sunni }
  reduce_pop = 0.40 }` becomes a real Hui massacre instead of a no-op), `events/Taiping.txt`
  160001, `events/CHIFlavor.txt` 131725, `events/BRZFlavor.txt` 46331/46332,
  `events/ENGFlavor.txt` 36938/36939 (`year = 1864`), `events/Sepoy rebellion.txt` 99896/99901,
  `events/PER_crises.txt` 301113, `decisions/RUS.txt:360`, `decisions/Germany.txt:364`,
  `decisions/extra_decisions.txt:1179` (SER, `year = 1845`).
- Already working and unaffected: **country**-scope `religion = X`, which reads the country's
  state religion — `decisions/Italy.txt:441`, `events/1german_revolution_1848.txt:1372, 1451`,
  `events/Sepoy rebellion.txt:441`.

---

## 9. Remaining gaps in the plan

1. **§5 depends on §4 being exhaustive, and §4 is not.** With the 7 missing sites (§3), step 5
   would ship an undefined-religion reference. Add "the 121-site sweep returns 0 hits" as the
   entry gate on step 5.
2. **§4.3's premise is inverted** (§0). Replace it with "conversion is 1:1; the only risk is a
   missed site, and the 7 negated sites are where a miss switches a gate off".
3. **`poptypes/` is unexamined** (§8). It contains more `is_state_religion` sites (48) than the
   whole of `events/` (18).
4. **Step 3's method misses accepted-culture-only tags** (§2, DLM).
5. **No step checks that the 1 910 moved pops land in provinces whose owner accepts them.**
   `audit_countries.py` and `audit_owner_scope.py` will not catch a Bavarian province of
   `south_german` pops under a tag that only accepts `north_german`. Worth a throwaway script
   between steps 3 and 7: per province, `pop culture ∈ {primary} ∪ {accepted}` of the owner,
   list exceptions.
6. Cosmetic: §4.2's heading should read "121 live culture-named religion sites, of which 115
   name one of the 10 sub-cultures".

## 10. The five open questions, answered

1. **German/Italian accepted cultures** — mirror vanilla (§7), not "everyone accepts both".
   Austria *not* accepting north_german is load-bearing for the dualism content.
2. **CAN / AST / the Cape** — follow vanilla for CAN (`anglo_canadian` primary); add
   `culture = australian` to AST and `culture = anglo_african` to SAF; ENG accepts only
   `anglo_canadian` (§7).
3. **occitan / picard** — yes, FRA accepts both at 1821 (§7).
4. **Conversion** — leave hard-disabled. It is already off by an explicit
   `factor = -100.0 always = yes`, and re-enabling it in the same pass as restoring 16 religions
   would make the change unbisectable.
5. **The 2026-09-06 deletions** — re-instate the `carlist_rebels` catholic gate and the two
   `events/Dungan.txt` sunni limits; they were removed *because* they were dead and the premise
   no longer holds. Do it as step 6, after the game is confirmed to load.
