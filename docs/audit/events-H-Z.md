# Event audit — `CoE_RoI_R/events/` files H–Z

Scope: the 93 top-level `events/*.txt` whose filename starts H–Z (the `DIM/`
subfolder and files 0-9/+/A–G belong to the companion audit `events-A-G.md`).

Method: `scripts/audit_events.py` (shared parser, `refcheck.py`) run over the
H–Z file set, then manual triage of every hit. Checks that `scripts/refcheck.py`
already performs — dead event ids, missing localisation keys, undefined
modifiers/flags, orphan events, unknown culture/religion/goods/cb/reform names —
are **not** repeated here.

## Counts

| | |
|---|---|
| files in scope | 93 (91 contain events) |
| `country_event` / `province_event` blocks | 1697 |
| `fire_only_once = yes` | 258 |
| `is_triggered_only = yes` | 425 |
| with `mean_time_to_happen` | 1292 |
| distinct unknown keywords after triage | 4 real typos (+2 scanner false positives) |
| defects reported | 5 high, 8 medium, 6 low |

## Triage notes (things deliberately **not** reported)

* **`NOT = { A B C }` is NOR, not NAND** in Victoria 2
  (`docs/wiki/list-of-conditions.md:86`): it is true only when every child is
  false. The many `NOT = { tag = TUR tag = RUS ... }` guards in `GREFlavor.txt`,
  `MEXFlavor.txt` and `NationalUnification.txt` are therefore correct.
* **`year = 18xx` gates are usually intentional.** 410 raw hits; a flavour event
  about the 1911 Mexican Revolution *should* be gated at 1911. Only gates that
  contradict the event's own subject matter are listed below.
* **`NOT = { year = 1836 }` upper bounds** (10 hits in `MEXFlavor`,
  `Ottoman_Event`, `PORFlavor`, `SPAFlavor`) are the mod's *deliberate*
  early-period windows, paired with a `year = 1821` lower bound or a flag. They
  are 1821-start content working as intended, not leftovers.
* **`move_issue_percentage`'s `to =` / `from =`** (14 hits, `JAPFlavor.txt`) and
  **`alliance = TAG`** (`PORFlavor.txt:1903`) are valid vanilla vocabulary; the
  keyword scanner does not know them.
* `IssueSuggestion.txt:380` (event 3005, repeatable `add_province_modifier`)
  guards each province with `NOT = { has_province_modifier = government_sanitarium }`,
  so nothing stacks; repeating across provinces is the design. Not a defect.
* `NationalUnification.txt:189` `FROM = { country_event = 49510 }` inside
  `random_owned` is fine — `FROM` re-scopes to a country.

## Defects

### [high]

`CoE_RoI_R/events/TemperanceLeague.txt:11` (also `:99`, `:365`, `:437`, `:511`)
— the religion filter is an **empty `OR = { }`** (both `pop_majority_religion`
lines are commented out). An empty `OR` evaluates false, so all five Temperance
League events (ids 100 and the four following) are permanently dead; the whole
feature never appears in game. Fix: delete the empty `OR` block, or restore
`OR = { pop_majority_religion = catholic pop_majority_religion = protestant }`.

`CoE_RoI_R/events/NationalUnification.txt:969` — `relio = north_german` is not a
condition (typo). It sits inside the `GER = { any_core = { ... } }` guard of the
German-unification trigger; an unrecognised key makes the clause false, so that
branch of unification can never qualify. Fix: `culture = north_german` (confirm
against the sibling blocks that use `culture =` in province scope).

`CoE_RoI_R/events/USAFlavorGVG.txt:26` — `realtion = { who = USA value = 100 }`
is a typo for `relation`. The effect is silently dropped, so Texas asking the USA
for help produces no relations change — the whole point of option A of event
1000100. Fix: `relation = { who = USA value = 100 }`. (This is one of the team's
own GVG files, so it is a regression, not inherited PDM.)

`CoE_RoI_R/events/PER_crises.txt:581` and `:635` — `PER = { random_owned = {
limit = { has_province_modifier = futile } country_event = 301116 } }` fires a
**country_event from province scope**. 301116/301117 are declared as
`country_event` at `PER_crises.txt:657`. Fix: hoist the province test out, e.g.
`PER = { if = { limit = { any_owned_province = { has_province_modifier = futile } } country_event = 301116 } }`,
or keep `random_owned` and use `owner = { country_event = 301116 }`.

`CoE_RoI_R/events/LiberalRevolutions.txt:1600` — `any_state = { ... OR = { } }`:
every `has_building = ...` line in the OR is commented out, leaving an empty OR
that is always false, so this industrial-unrest event is unreachable. The
commented names (`machine_parts_factory`, `steel_factory`, …) look like casualties
of the Roar of Industry economy rework. Fix: re-enable the list with building
names that actually exist in the reworked production types, or delete the event.

### [medium]

`CoE_RoI_R/events/NobelPrize.txt:1700`, `:3379`, `:5059`, `:6739`, `:8420` — each
of these five 1935 award events requires `has_global_flag = 34NobelPhysics`
(resp. chemistry/medicine/literature/peace) at the top of the trigger and then
`not = { year = 1938 has_global_flag = 34NobelPhysics }`. Because Vic2 `NOT` is
NOR, the flag must be simultaneously set and unset: always false, so the 1935
prizes never fire. Fix: drop the flag from the inner `not` (keep only
`not = { year = 1938 }`) — compare the 1936 events, which do not repeat the flag.

`CoE_RoI_R/events/political_leaders.txt:2150` — `modifer = { ... }` inside
`mean_time_to_happen` (typo for `modifier`). The national-value weighting is
ignored, so this leader event's MTTH is a flat `months = 12` for everyone.
Fix: `modifier`.

`CoE_RoI_R/events/USAFlavorGVG.txt:12` — `has_truce = USA` is not a vanilla
condition and appears nowhere in the game folder's own events/decisions. It
almost certainly evaluates false, which — being inside a `NOT` (NOR) — leaves the
rest of the guard doing the work, so the event still fires, but not for the
intended reason. Fix: remove the line, or express the intent with
`NOT = { war_with = USA }` / a flag set when a truce is signed.

`CoE_RoI_R/events/FRAFlavor.txt:1534` (event 37244, July Revolution) — the
trigger has **no lower date bound**: `has_country_flag = three_glorious_days` OR
`average_militancy = 5`, plus a government check and `NOT = { year = 1836 }`.
On a 1821 start France can reach militancy 5 in the early 1820s and stage the
July Revolution up to a decade early. Fix: add `year = 1829` (or gate on the
`charles_x` flag that event 37240 sets in 1824).

`CoE_RoI_R/events/FRAFlavor.txt:1450`–`1525` — the event that was supposed to set
`three_glorious_days` is entirely commented out. The flag now only comes from the
`constitution_suspended` decision (`CoE_RoI_R/decisions/France.txt:610`), which
has no date gate either. The July Revolution chain is reachable but its
scripted historical path is gone. Fix: restore the commented event with a
`year = 1830` gate, or accept the decision as the only path and document it.

`CoE_RoI_R/events/PRUFlavor.txt:15`, `SWEFlavor.txt:88`, `USAFlavor.txt:802` —
`year = 1836` on what read as "opening flavour" events. On the 1821 start these
sit idle for the first 15 years. Judge individually: if the event describes a
dated historical episode, leave it; if it is scene-setting, lower the gate to
1821. Listed because 1836 exactly is the vanilla-start fingerprint.

`CoE_RoI_R/events/BELFlavor.txt:13` (event 36700) — Belgian flavour opens at
`year = 1837`, i.e. it presumes Belgium already exists. Nothing in the H–Z set
creates Belgium: see the coverage section below.

### [low]

`CoE_RoI_R/events/GREFlavor.txt:102` — event 31201 reuses `title = "EVTNAME31200"`;
31203/31204 reuse `EVTNAME31202`; 31206/31207 reuse `EVTNAME31205`. Probably
deliberate (same headline, different outcomes), but the London-Conference outcome
events are indistinguishable in the message log. Fix: give each its own key.

`CoE_RoI_R/events/HAIFlavor.txt:99`, `HEDFlavor.txt:8`, `HEKFlavor.txt:8`,
`NASFlavor.txt:8`, `Oriental Crisis.txt:918`, `Ottoman_Event.txt:1666`,
`RUSFlavor.txt:11`, `RUSFlavor.txt:222`, `SAXFlavor.txt:12`, `SPAFlavor.txt:16`,
`SWIFlavor.txt:8`, `SWIFlavor.txt:53`, `SWEFlavor.txt:12` — first event of the
file gated at 1837/1838, the classic "one year after the vanilla start". Each is
a candidate for a 1821–1836 counterpart; none is broken as written.

`CoE_RoI_R/events/Taiping.txt:24` — MTTH has weights for `< 1845`, `1845–1850`,
`1855–1860` and `1860+`, but no modifier for **1850–1855**, the years the rebellion
actually began. Harmless (falls through to `months = 12`) but likely unintended;
add a `factor = 0.5, year = 1850, NOT = { year = 1855 }` step.

`CoE_RoI_R/events/ColonialSpain_Event.txt` — the file is named for colonial Spain
but every event in it is Cuba/slavery flavour from 1843 onward (98100 "The Ladder
Conspiracy" is gated `year = 1843`, `NOT = { year = 1848 }`). Nothing here relates
to the mainland wars of independence. Cosmetic, but misleading when searching.

No defects found for: `ai_chance` blocks whose weights are all 0, and MTTH
`modifier { factor = 0 }` that applies to every country — the scan found none in
this file set. No `year` gate below 1821 (dead-on-arrival gate) exists in H–Z.

## 1821–1836 coverage

| Episode | Status | Where |
|---|---|---|
| Greek War of Independence / London Conference | **present, reachable** | `GREFlavor.txt` ids 31200–31207. Entry event 31200 needs a European GP and `GRE = { exists = yes ... has_country_flag = legitimacy }`; the Ottoman side is `Ottoman_Event.txt` id 31250 (`year = 1821`, `NOT = { year = 1836 }`, "Balkan Rebellions"). Reachable from 1821 provided something sets GRE's `legitimacy` flag — that hook lives outside the H–Z set and should be confirmed against the A–G events and `decisions/`. |
| Trienio Liberal / French intervention in Spain 1823 | **present** | `SPAFlavor.txt:4347` id 37761 "Appeal to the Holy Alliance", MTTH weighted toward 1823/1825, `NOT = { year = 1836 }`. |
| Portuguese constitutional crisis 1820s | **present** | `PORFlavor.txt:932` id 97021 "The Draft Constitution" (`year = 1821`, tag UPB), plus 1825/1836-window events at `:1889` and `:2009`. |
| July Revolution 1830 | **present but mis-gated** | `FRAFlavor.txt` ids 37240 (Accession of Charles X, `year = 1824 month = 9`) and 37244 (July Revolution). 37244 has no lower date bound — see the [medium] entry. The intermediate "Three Glorious Days" event is commented out. |
| Spanish American independence (1810–1825) | **missing as events** | `ColonialSpain_Event.txt` is 1843+ Cuba only; `CLMFlavor.txt`/`USCAFlavor.txt`/`ChileanEvents.txt` carry post-independence flavour and `MEXFlavor.txt:1452` (id 44851, United Provinces of Central America) assumes independence has already happened. The wars themselves are presumably resolved in `history/`; there is no scripted chain. |
| Decembrist revolt 1825 | **missing** | No hit for "Decembrist"/"Nicholas"/"Senate Square" anywhere under `events/` or `decisions/`. `RUSFlavor.txt`'s earliest date gates are 1827 and 1828 (Russo-Persian/Russo-Turkish). The single largest 1821-start gap for a great power. |
| Belgian Revolution 1830 | **missing** | `BELFlavor.txt` starts at `year = 1837` and assumes Belgium exists; the only reference to a `belgian_revolution` flag is a commented-out MTTH modifier at `FRAFlavor.txt:1494` (`has_global_flag = DIM_belgian_revolution`, a Dutch-East-Indies submod flag). `NETFlavor.txt:502` has 1825 content but no 1830 secession chain. Check `history/countries/BEL - Belgium.txt` and `decisions/NET.txt` for whether Belgium is simply a 1821 starting tag; if it is not, nothing creates it. |

Suggested order of work: the five [high] items (two of them, `TemperanceLeague`
and `LiberalRevolutions`, are single-line deletions that restore dead content),
then the Decembrist and Belgian Revolution gaps, then the July Revolution date
gate.

## Fixed (2026-09-06)

* `TemperanceLeague.txt` — un-commented `pop_majority_religion = catholic` /
  `= protestant` in all five empty `OR` blocks (10 lines). The religions exist in
  `common/religion.txt`; the five events are live again.
* `NationalUnification.txt:969` — `relio = north_german` -> `culture = north_german`
  (`north_german` is a culture in `common/cultures.txt:36`, matching the sibling
  province-scope test at `:629`). The same block's MTTH twin at `:985` used
  `religion = north_german` and was corrected the same way.
* `PER_crises.txt:581`, `:635` — the `random_owned` bodies now call
  `owner = { country_event = 301116 / 301117 }`; the two events keep their
  `country_event` declaration and their option bodies lost the now-invalid
  `owner = { ... }` wrapper (effects run directly in country scope).
* `LiberalRevolutions.txt` — all 7 empty `OR = { }` blocks of commented
  `has_building` names (event 10150 trigger at `:1600` plus its MTTH twins and the
  other Luddite events) now list the five factory buildings the economy rework
  actually defines in `common/buildings.txt`: `military_factory_building`,
  `heavy_factory_building`, `food_factory_building`, `light_factory_building`,
  `luxury_factory_building`.
* `NobelPrize.txt:1700`, `:3379`, `:5059`, `:6739`, `:8420` — the inner
  `not = { year = 1938 has_global_flag = 34Nobel<X> }` was an off-by-one: every
  other link in the chain names the *next* year's flag, and these events set
  `35Nobel<X>` in their option. Changed `34` -> `35`, which both unblocks the 1935
  prizes and keeps them one-shot.
* `FRAFlavor.txt:1534` — added `year = 1829` to event 37244 (July Revolution). No
  upper bound added; the existing `NOT = { year = 1836 }` already caps the window.
* `political_leaders.txt:2150` — `modifer` -> `modifier`.
* `Taiping.txt` — added the missing `factor = 0.5, year = 1850, NOT = { year = 1855 }`
  MTTH step (was the only gap in the ramp, and the years the rebellion began).

## Deferred

* `USAFlavorGVG.txt:12` (`has_truce = USA`) and `:26` (`realtion`) — that file is
  owned by the companion A–G audit pass; not touched here.
* `GREFlavor.txt:102` duplicate `EVTNAME` keys — A–G file.
* `FRAFlavor.txt:1450`–`1525` (commented-out "Three Glorious Days" event),
  `PRUFlavor.txt:15` / `SWEFlavor.txt:88` / `USAFlavor.txt:802` and the [low]
  1837/1838 first-event gates, `BELFlavor.txt:13`, the `ColonialSpain_Event.txt`
  file name, and the Decembrist / Belgian Revolution / Spanish-American coverage
  gaps — all content decisions rather than script defects; left for a design pass.
