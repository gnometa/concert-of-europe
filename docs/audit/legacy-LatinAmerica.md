# Legacy audit: Latin America flavour

Scope: `events/USCAFlavor.txt`, `events/SouthAmericaFlavor.txt`, `events/ARGFlavor.txt`,
`events/CLMFlavor.txt` — the Central American federation, the Gran Colombia breakup,
Argentina/Rosas and the Rio de la Plata. Line numbers are pre-fix.

## Fixed

| file | line | id | problem | fix |
|---|---|---|---|---|
| USCAFlavor.txt | 808 | 975591 | **[high]** "The Secession of Panama": every effect in option A targets **NIC** — `relation`, the `war` block and the `casus_belli` — so declaring war on the Panamanian secession attacks Nicaragua instead, and does nothing at all if NIC never seceded. Copy-paste from 97559. | retargeted the whole block to PNM |
| USCAFlavor.txt | 1394 | 32550 | **[high]** Belize purchase, option B ("We refuse"): `UCA = { country_event = 32552 }`. The root of 32550 *is* the owner of 2190 — `decisions/USCA.txt:296` does `2190 = { owner = { country_event = 32550 } }` — so the refusal notice goes to the refuser, whose `FROM` is itself; the buyer is never told and the -100 relation lands on nobody. It also hardcodes UCA although the decision is open to any great power. | `FROM = { country_event = 32552 }` |
| ARGFlavor.txt | 176 | 46605 | **[high]** dead event. The trigger's multi-statement `NOT` is a NOR and `exists = yes` sits inside it, so the event demands a country that *does not exist*. The whole Platine-War support branch — `will_support_entre_rios`, read by 46610's MTTH and by its option B — could never fire. | split into `exists = yes` + `NOT = { tag = ARG }` + the NOR of the flags |
| CLMFlavor.txt | 538 | 37806 | **[high]** the option B effect block contains `vote_franschise = none_voting`. `vote_franschise` is a *condition*, not an effect; the engine logs it and the franchise rollback — the entire point of the reactionary concession — never happens. | `political_reform = none_voting` |
| USCAFlavor.txt | 1466 / 1489 | 97580, 44850 | **[medium]** both options of "Joining Mexico?" set `join_mexico`, but `MEXFlavor.txt` 44850 (First Mexican Empire) gates on `UCA = { has_country_flag = join_mexico }`. A Central America that chose "We will make our own way" still hands Iturbide his empire trigger; the flag was doing double duty as a "decision taken" guard. | option B now sets `usca_own_way`; 97580's own guard NORs both flags |
| USCAFlavor.txt | 128, 190, 252, 314, 376 | 97551-97555 | **[medium]** all five independence events use the option text "The republic must live on!" while the effect secedes the province, drops prestige and hands the new state a `free_peoples` CB. The text is a literal string, not a loc key, lifted from 97550. | renamed to "There is nothing we can do to hold them." |

## Reported, not changed

| file | line | id | problem | suggested fix |
|---|---|---|---|---|
| CLMFlavor.txt | 900 | 37808 | **[medium]** "Presidential Crisis" option B, "We're better off without them", still applies `political_reform = appointed/none_voting/underground_parties` + `government = presidential_dictatorship`. The equivalent conciliatory option in the twin event 37807 changes no reforms, so this looks like copy-paste from option A — but with `ai_chance = 90` it means an AI Gran Colombia *always* ends its democracy, which may be the intended flavour. Decide before touching. | drop the four reform/government lines from option B |
| SouthAmericaFlavor.txt | 1051 | 97086 | **[medium]** "Pacification of Patagonia" is a province event with no fire-once guard and no owner check; it grants `life_rating = 10` and gates on `NOT = { life_rating = 16 }`, so a province at life rating 4 fires twice and ends at 24. It also fires on uncolonised provinces, making Patagonia free real estate for the first coloniser. | tighten to `NOT = { life_rating = 8 }` or add a province flag |
| SouthAmericaFlavor.txt | 738 | 97084 | **[medium]** "Claiming the Pampas": MTTH 10 months, no `war = no`, no year or tech gate, no cost. From the 1821 bookmark Argentina absorbs all seven Pampas provinces by roughly 1823, while still fighting its war of independence; the Conquest of the Desert twin (97085) at least requires the `conquest_of_the_desert` flag. | gate on a flag or tech as 97085 does |
| CLMFlavor.txt | 683, 862 | 37807, 37808 | **[low]** every released successor (VNZ, ECU, DOM, PRI, CUB) is handed `leadership = 40`. A one-province new nation generates 1-3 leadership a month, so this is about two years of banked points each. It is consistent across both events, so it reads as deliberate ("the generals defect"), but the magnitude is out of scale. | halve, or scale by size |
| USCAFlavor.txt | 1129 | 97560 | **[low]** "The republic must end." pays `prestige = 5` for dissolving the federation while "We will fight to preserve the republic!" pays nothing; combined with `ai_chance` 80/20 the AI is paid to dissolve. | move the prestige to the fight option, or drop it |
| SouthAmericaFlavor.txt | 335 | 97075 | **[low]** `news_title = "EVTNAME97070_NEWS_TITLE"` reuses the *previous* event's headline, so "The Era of Conservatism" is reported under "La Carta de la Esclavitud". `EVTNAME97075_NEWS_TITLE` exists in no csv, so fixing the reference needs the loc key added first. | add `EVTNAME97075_NEWS_TITLE`, then point at it |
| ARGFlavor.txt | 1, 105 | 46600, 46601 | **[low]** both declare `news = yes` with `news_desc_*` but no `news_title`. | add `news_title` keys |
| ARGFlavor.txt | 576 | 46615 | **[low]** "Claiming the Malvinas" secedes 2131 without `add_core`, unlike its sibling 46630 which cores South Georgia. Argentina then holds the Malvinas as a non-core, which weakens the later 46616-46619 chain. | add `add_core = THIS` |
| CLMFlavor.txt | 26 | 37801 | **[low]** `history/countries/PRI - Puerto Rico.txt:48` sets `colombian_assistance` but, unlike CUB/DOM/ECU, never clears it later, so Puerto Rico stays eligible for annexation by Gran Colombia indefinitely — until some event clears it. | add the matching dated `clr_country_flag` block |

## Checked and found sound

* **97555 `CLM_1723`.** The Panama independence MTTH scopes to `CLM_1723` rather than `UCA_2204`
  like its siblings. This is not a typo: `map/region.txt:1182` defines
  `CLM_1723 = { 2204 1723 2205 2206 2208 }` as the Panama region, and there is no `UCA_2204`.
* **`THIS` in nested scopes.** 37803's `any_owned = { ... THIS = { add_accepted_culture = caribeno } }`
  resolves `THIS` to the event root — the annexing country — which is what it wants.
* **Falklands chain (46616 -> 46617 -> 46618/46619).** Every `FROM` hop is correct: 46617 fires on
  the owner of 2131 with `FROM` = Britain, 46618 fires back on Britain with `FROM` = Argentina, and
  the `war` and `change_controller` in 46618 use the right sides.
* **1821 start windows.** 97095 (Constitutional Controversy) is what grants Gran Colombia the
  `liberal_constitution` / `conservative_constitution` flag that 37805-37808 all require, and its
  `war = no` clause makes it wait for `SPAAyacuchoGVG` 1002100-1002102 to end the war of
  independence — so the breakup chain cannot start before about 1824. Brazil is correctly excluded
  by the flag set in `history/countries/BRZ - Brazil.txt:51`, so the empire is not forced into a
  republic by that event.
* **UCA/Mexico ordering.** 97580 -> 97581 (`inherit = FROM`) -> `MEXFlavor` 44850 is a consistent
  chain once the flag fix above is applied; 44850's `any_owned` regions (`UCA_2186` … `CLM_1723`)
  simply match nothing if the annexation never happened.
* **Gran Colombia releases.** The conditional `random_owned = { limit = { province_id = ... } GCO = {
  release = X } }` shape in 37807/37808 matches the pattern judged deliberate in
  `docs/audit/owner-scope.md`; no effects land on a third party's provinces.
