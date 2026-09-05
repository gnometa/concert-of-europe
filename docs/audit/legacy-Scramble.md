# Legacy audit: `events/Scramble for Africa.txt` and `events/New Colonies.txt`

*2026-09-06. Line-by-line logic review of the colonial machinery: Berlin Conference (95500-95503),
protectorates (95505-95507), Sale of Assab (95508-95509), Eritrea (95510), Colonial Ambition
(95511/95515), Zemene Mesafint (95512-95513), Ethiopian expansion (95514), colonial core spread
(98900/98905). Line numbers are post-fix. Mechanical audits (modcheck braces/provinces/tags,
refcheck, audit_events, cwtools) were clean on both files before and after; everything below is
logic the tools cannot see.*

**Scope note.** `New Colonies.txt` is 4502 lines of which 4370 are commented out: the whole
`98800-98895` colonial-core-spread series is disabled and only `98900` (South Africa) and `98905`
(Rupert's Land) are live. Nothing in the dead block was reviewed beyond confirming it is inert.

**Reachability note.** `95504` (Sahel Jihad) requires `war = no`. MAS is locked in the 1818 Massina
Jihad until `WarResolutionsGVG` 1002200/1002201 settles it (1843-1848 window), so MAS can only take
the jihad after that peace - the chain is now reachable, which it was not before tonight's fix. No
overlap with ASHWarGVG (1001600-1001603): ASH is not in the 95504 tag list, is not a Sahel
neighbour of 1786/1789/1794/1800/1804/1808/1878/1880, and shares no flags with this file.

## Fixed in place

| file:line | id | problem | fix |
|---|---|---|---|
| Scramble:340 | 95505 | **[high]** option B "Throw the Europeans out!" had `any_greater_power = { limit = { NOT = { is_sphere_leader_of = THIS } diplomatic_influence = { who = THIS value = -100 } } }` - the influence statement sat in the `limit`, where it is a trigger (`influence >= -100`, always true), and the effect body was **empty**. The block did nothing: only the sphere owner ever lost influence. | moved `diplomatic_influence` out of the `limit` into the effect body, matching the sibling `sphere_owner` block. |
| Scramble:939 | 95514 | **[medium]** the first `random_owned` branch required 1864 **and** 1866 **and** 1867 empty, while branches 2 and 3 require 1864 (and 1866) non-empty. The case "1864 empty, 1866 settled" matched no branch, so the event fired every 12 months granting `years_of_research = 0.25` and colonising nothing - a free research drip in a dead state. | branch 1 limit reduced to `1864 = { empty = yes }`, giving a proper 1864 -> 1866 -> 1867 ladder. |
| Scramble:418 | 95507 | **[medium]** duplicated episode: two `random_owned` blocks with byte-identical effects (CB + war on FROM), branching only on whether the scoped country itself has `has_global_flag = berlin_conference` - a global flag, so both branches are the same country and the same outcome. The `random_owned`/`owner` hop was also a no-op indirection back to the event root. | collapsed to a single country-scope `casus_belli` + `war` on FROM. |
| New Colonies:4419 | 98900 | **[medium]** the only mtth modifier was `factor = 5` with its sole condition (`region = ENG_2083`) commented out. A modifier with no conditions always applies, so SAF core spread ran at 300 months instead of 60 - effectively never in a normal game. | removed the dead modifier; mtth is the intended 60 months. |

## Reported, not changed

| file:line | id | problem | suggested fix |
|---|---|---|---|
| Scramble:99 | 95503 | **[medium]** no year gate and `mean_time_to_happen = { days = 1 }`, so "$COUNTRY$ in the Modern Age" fires in **September 1821** for every coastal African unciv, handing each one `relation = +50` with every civilized country below +25. Written for the 1836 vanilla start; from 1821 it is a free day-one diplomatic windfall for ~30 tags. | gate on `year = 1840` (or on a western-contact condition) instead of firing at the bookmark. |
| Scramble:51 | 95502 | **[medium]** implausible magnitude: a single forced option drives relations to the **-200 floor** with *every* European civ/GP/colonial nation and breaks their alliances, 5 days after the Berlin Conference, for every African unciv at once. It also pre-empts 95505's protectorate diplomacy by pinning influence targets at maximum hostility. | -50 or -75 conveys the same story without saturating the cap. |
| Scramble:600 | 95510 | **[medium]** effects contradict the option text: option A is "This cannot be allowed!" yet it runs the same `any_owned = { limit = { region = ENG_1848 } secede_province = ETH }` as option B "Let it go", and additionally awards `prestige = 3` for losing the region. Only the relation/CB differ. | keep the cession in option B only, or reword option A and drop the prestige gain. |
| Scramble:568 | 95509 | **[medium]** the "sale" of Assab is not a sale: 95508 option A secedes 1851 unconditionally and only *then* notifies the owner, whose single option is titled "Assab belongs to $COUNTRY$!" while doing nothing to recover it. The owner (an unciv) is also granted a `place_in_the_sun` CB, a great-power CB it can never use, and the European aggressor is handed a `demand_concession_casus_belli` on its victim. | give the owner a usable CB and drop the aggressor's reward, or rename the option to acknowledge the loss. |
| Scramble:597 | 95509 | **[low]** `any_country = { limit = { is_greater_power = yes } diplomatic_influence = { who = THIS value = -100 } }` strips influence from all eight GPs, including ones with no connection to Assab and including the buyer. | restrict to GPs with existing influence in the scoped country. |
| Scramble:246 | 95505 | **[low]** dead condition: `NOT = { has_country_flag = delay_unciv_annexation }` plus the `factor = 10` mtth modifier keyed on the same flag. `delay_unciv_annexation` is set nowhere in the mod (also referenced dead in 95502), so the trigger is always true and the modifier never applies. | delete both references, or set the flag somewhere in the unciv westernisation chain. |
| Scramble:377 | 95506 | **[low]** wrong recipient by intent: option A sets `refused_protectorate` on **FROM** (the African tag), so one great power declining permanently immunises that country against *every* future protectorate offer from *any* power. The flag name reads as the offering power's decision. | scope the flag to the offering power, or clear it after N years. |
| Scramble:365 | 95506 | **[low]** absurd ai_chance: below 0.92 badboy option A is `factor = 0` and option B `factor = 95`, so the AI **always** annexes; above 0.92 option B is 0 and it never does. The "decline" branch is unreachable in normal play. | give option A a nonzero floor (e.g. 15) so restraint is possible. |
| Scramble:750 | 95511 | **[low]** the second `random_country` grants **THIS** (the acting great power) a `place_in_the_sun` CB against a random rival colonial power it is on *good* terms with (`NOT = { relation = { who = THIS value = -50 } ... }`). Per the narrative the rival should be the one gaining a CB on the newcomer. | swap the scopes, or drop the block. |
| Scramble:690 | 95511 | **[low]** the `NOT = { ... any_owned_province = { continent = africa } ... }` block (NOR) restricts "Colonial Ambition" to powers owning **no** African province at all, so it fires once per power and never again; combined with `ai = yes` the player never sees it despite flavour text addressing the player. | intended as a first-colony nudge; if not, split the African-holdings check out of the NOR. |
| Scramble:206 | 95504 | **[low]** the pop filter `#limit = { has_pop_religion = sunni }` is commented out (correctly - pop religion carries sub-cultures in this mod, so religion-form pop tests are dead), but the result is that the jihad calms **every** pop in the country by 3 militancy and pushes all of them toward jingoism, animist and Christian minorities included. | filter on `is_primary_culture = yes`, as 95512 does. |
| Scramble:785 | 95515 | **[low]** implausible magnitude plus a single forced option: `relation = { who = THIS value = -200 }` from FROM immediately before the war declaration - the war itself already tanks relations, and -200 is the floor. | -50 is enough. |
| New Colonies:4381 | 98900 | **[low]** `title = "EVTNAME98800"` on both 98900 and 98905, pointing at the loc key of the commented-out Nigeria event; the key still exists so nothing breaks visibly, but the South Africa and Rupert's Land events show Nigeria's title. | add `EVTNAME98900` / `EVTNAME98905` and point the events at them. |
| New Colonies:4406 | 98900 | **[low]** `SAF = { vassal_of = THIS is_culture_group = THIS }` inside a non-triggered `province_event`: `THIS` is the event root, i.e. the **province**, not a country, so that branch is not a meaningful country test. The other OR branch (`owner = { owns = 2087 }` + `SAF = { exists = no }`) still works, so cores still spread; only the vassal path is suspect. | restructure through `owner = { ... }` after confirming the idiom against a working PDM file. |
