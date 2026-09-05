# Logic review — `CoE_RoI_R/events/ITAFlavor.txt`

*2026-09-06. Line-by-line read of all 13 events (35300, 35301, 35302, 35305, 35310-35314, 90038,
96160-96163, 96165, 96170). Mechanical audits (`modcheck`, `refcheck`, `audit_events`, cwtools)
were clean on this file at baseline, so everything below is logic, not syntax. Line numbers are
post-fix.*

Checked and **not** a defect (recorded so nobody "fixes" them again):

- `has_pop_religion = north_italian` / `south_italian` (35311, 35312) is correct in this mod:
  sub-cultures live in the pop religion field. Do not rewrite them as culture conditions.
- Multi-statement `NOT = { ... }` gates (35300-35302, 35310, 96160, 96170) are NOR, which is the
  intended "none of this yet".
- `THIS` inside `random_country` / `any_owned` / `AUS = { ... }` resolves to the event root, so
  35310's `THIS = { war = { target = LOM } }` and 96170's `secede_province = THIS` are right.
- `AUS_726 = { add_core = ... }` / `PAP_741` / `MOD_739` / `TUS_744` are state-region scopes; the
  same idiom is used by `decisions/Italy.txt`.
- `history/countries/AUS - Austria.txt:122` sets `italian_rebellions` and `ITA - Italy.txt:51` sets
  `first_italian_war`, but both sit in the **1861.1.1** block, so they do not pre-empt 35310 at the
  1821 bookmark.
- 35311 borrows `EVTNAME35310`; 96170 borrows `EVTOPTA11103` / `EVTOPTB11103`. Both keys exist.
- All province ids used (465, 466, 472, 726, 727, 728, 729, 741, 749, 1731) exist in
  `map/definition.csv`; 60130 (`CleanUp.txt`) and 11101 (`NationalUnification.txt`) exist.

## Fixed in place

| line | id | problem | fix |
|---|---|---|---|
| 1446-1454, 1486-1494, 1531-1539 | 96162, 96163 | **[high]** The flag-cosmetic events set `government = X` **directly inside `random_owned`**, i.e. in *province* scope, where the effect does nothing. Every option of 96162 and option A of 96163 were silent no-ops: the player picked a royal standard and the government variant — and therefore the flag — never changed. Option B of 96163 already had the correct form, which gives the intended pattern away. | wrapped all nine statements in `owner = { government = ... }`, matching 96163's working option. |
| 777, 801 | 90038 | **[high]** The Pact of Plombières is offered to France by the `plombieres` decision, whose `potential` is `OR = { tag = SAR tag = SVY }` — but option A hardcoded `diplomatic_influence = { who = SAR ... }` and `SAR = { prestige = 10 ... create_alliance = FRA }`. In a Savoy game France allied and influenced *Sardinia* instead, so the `call_ally = yes` in the war blocks below (which do handle SVY) never dragged the actual signatory in: the Second War of Independence started without the ally it was signed with. | `who = FROM` and `FROM = { ... }`. |
| 1360, 1364, 1366 | 35311 | **[high]** 35310 fires 35311 at `tag = SAR` *or* `tag = SVY`, and the war block correctly uses `target = THIS` — but three effects hardcoded SAR: `FRA = { diplomatic_influence = { who = SAR value = -100 } }`, `LOM = { annex_to = SAR }` and `AUS_726 = { add_core = SAR }`. In a Savoy game Lombardy was annexed by a third party (possibly non-existent), Milan's cores went to Sardinia and France's influence penalty hit the wrong country, while Savoy still got the war with Austria. | `who = THIS`, `annex_to = THIS`, `add_core = THIS`. |
| 988 | 96160 | **[high]** "Union with Sardinia" had **no year and no tech gate** — only `ai = yes`, `primary_culture = italian`, neighbour and sphere checks — with `mean_time_to_happen = 24 months`. From the 1821.9.1 start Sardinia could therefore `inherit` Modena, Parma, Lucca or Tuscany by ~1823, decades before `nationalism_n_imperialism` and right on top of tonight's ITARisingsGVG 1831 chain. Its sibling 96170 (Il Risorgimento) *is* tech-gated. | added `nationalism_n_imperialism = 1`, matching 96170. |
| 320-352, 354-386, 440-472, 474-506 | 35310 | **[medium]** In options A and C the nation-building block sat **inside** `any_owned`, so it ran once per seceded province: LOM and VEN each received `small_country_draft`, `militancy = -6`, `military_industry` / `light_industry` / `horses = 50` and `leadership = 40` three-odd times over (leadership 120+), and Austria re-declared the same war once per province. `military_industry = 50` was also written twice in each block. | the `any_owned` now only secedes; the country-level effects moved into a `random_country = { limit = { tag = LOM/VEN exists = yes } ... }` that runs once, and the duplicate `military_industry` line was dropped. |

## Reported, not changed

| line | id | problem | suggested fix |
|---|---|---|---|
| 1109-1111 | 96161 | **[medium]** "Failure of Plombières" — the desc says *"our deal with France is broken"* — nevertheless grants `465/466/472 = { add_core = FRA }`, handing France cores on Savoy and Nice. That is the *reward* the `cavours_diplomacy` decision pays on the success path (`decisions/Italy.txt:145`, which also does `remove_core = THIS`). Effect contradicts the option text, but it may be a deliberate irredentism seed for a later French CB. | design call: drop the three FRA cores from the failure branch and keep only `PAP_741` / `MOD_739` / `TUS_744`. |
| 545 | 35310 | **[medium]** Option C *"For the Republic of San Marco!"* declares war on Venice as Austria and then `change_tag_no_core_switch = VEN`, so the player ends up on the other side of a war they just declared, with `relation = { who = VEN value = -100 }` applied to the tag they are about to become. `ai_chance = 0` keeps the AI out; otherwise the option is a byte-for-byte copy of option A plus the tag switch. | drop the self-directed relation lines, or gate the option on `ai = no`. |
| 752, 754 | 35313 | **[medium]** `relation = { who = FROM value = 400 }` and `diplomatic_influence = { ... value = 200 }` exceed the engine's ±200 relation and 0-100 influence ranges, so they silently clamp. 17 other events under `events/` also use `value = 400`, so this is a mod-wide idiom rather than an ITAFlavor bug. | resolve once, globally; not worth an isolated edit. |
| 979 | 96160 | **[medium]** No `fire_only_once`; re-firing is prevented only by `attempted_sardinia_union`, which the option sets unconditionally even when neither SAR nor SVY exists — a minor that rolls the event while Sardinia is at war is locked out forever. | set the flag inside the `random_country` that actually finds SAR/SVY. |
| 796-798 | 90038 | **[low]** `badboy = -25` immediately followed by `badboy = 18` is an infamy *reset-to-18* hack for the AI branch. It works, but it is opaque and silently wipes unrelated infamy. | comment it, or use a single scaled value. |
| 819 | 90038 | **[low]** Sardinia gets `add_country_modifier = { name = csa_draft }` — the Confederate States draft modifier — on signing an Italian pact. Mechanically fine, thematically wrong; `small_country_draft` (used by 35310) fits. | rename to a neutral modifier. |
| 615, 623 | 35311 | **[low]** Option B (*avoid war*, `treasury = -10000`) costs Sardinia twice what option A (*declare war*, `treasury = -5000`) does, and option C (*refuse*) pays `prestige = 5` for doing nothing. The incentive ordering is backwards for a war-of-independence choice. | halve B's outlay, or drop C's prestige. |
| 1245 | 96170 | **[low]** 96170 (mtth, `major = yes`) and `NationalUnification.txt:303` event 11103 are the same episode: same `EVTNAME96170` title, same `change_tag = culture`, same follow-ups (11101, 96165), same PAP-partition block with `NOT = { province_id = 749 }`. 11103 is the triggered entry point used by `PanNationalists.txt:195`; the duplication is deliberate but the two copies have already drifted. | make 96170 a thin `country_event = 11103` wrapper so the effects live in one place. |
| 3, 44 | 35300, 35301 | **[low]** Two pure-prestige theatre events (1910-1913, 1902-1905) with an identical body, picture and mtth curve; only the years and `prestige = 2` / `3` differ. | harmless; merge if the file is ever trimmed. |
| 138 | 35305 | **[low]** The Guerra di Libia's four `random_owned` branches differ only by `ai = yes/no` and `1731 = { is_colonial }` — 130 lines of copy-paste. The `ai_chance` modifiers use `badboy = 0.6`, matching the `badboy = 0.68` idiom at 90038. | no change needed. |

## Interactions checked

- **ITARisingsGVG (1001100-1001104)** — no id overlap (35xxx / 9xxxx vs 10011xx) and no flag
  overlap: `carbonari_active`, `italian_risings_1831`, `mod_menotti_resolved`,
  `pap_legations_revolt` and `aus_intervened_1831` are read nowhere in ITAFlavor, and none of
  ITAFlavor's flags (`first_italian_war`, `italian_rebellions`, `plombieres`,
  `made_the_call_to_union`, `objects_to_italy`, `ita_cosmetic_picked`) are touched by the risings.
  The only thing that could have collided with 1831 was 96160, now tech-gated above.
- **NationalUnification.txt Italian branch** — 11103 / 11101 / 60130 are reached from 96170 and
  96160 respectively and all three exist; the only issue is the 96170/11103 duplication noted
  above. `decisions/Italy.txt` (`plombieres`, `cavours_diplomacy`) is the sole source of the
  `plombieres` and `cavour_has_done_his` flags 96161 reads, and `decisions/France.txt:358` is the
  only other reader of `plombieres_refused`.
- **Window sanity from 1821** — every year gate in the file (1860, 1870, 1880, 1890, 1891, 1902,
  1910) is reachable, and no `year` / `NOT = { year }` pair is inverted or empty. 35310 needs the
  1848 `hungarian_revolution_occurred` flag plus the `springtime_of_nations` modifier, both from
  `LiberalRevolutions.txt`, so it is not a dead branch.

## Verification

`modcheck braces` 0; `refcheck` 14/0/60/0/128/0/8; `audit_events` unknown 0, high 0; cwtools at the
known baseline (12 `production_types` + `CBsAndCores:2448` + `Indochina:188`). All unchanged from
before the edits.
