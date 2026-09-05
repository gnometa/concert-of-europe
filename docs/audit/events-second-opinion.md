# Events / decisions - second-opinion audit

Read-only sweep of all `CoE_RoI_R/events/**/*.txt` and `CoE_RoI_R/decisions/*.txt`
with `scripts/audit_events2.py` (tolerant Clausewitz parser from `refcheck.py`).

Deliberately **different lenses** from `docs/audit/events-A-G.md` / `events-H-Z.md`
(`scripts/audit_events.py`): those covered unknown keywords, date gates, repeatable
permanent effects, always-false triggers, fire-site scope, `ai_chance`, MTTH factor 0.
`refcheck.py` covers references / loc / flags. This pass looks at FROM resolution,
scope of effects inside province events, random weights, option/news/UI hygiene,
modifier duration consistency, tag-switch and release targets, global-flag misuse.

Run: `python scripts/audit_events2.py` (JSON: counts, examples, defect list).

## Corpus and counts

| Metric | Value |
|---|---|
| country/province events parsed | 3180 |
| decisions parsed | 1247 |
| event fire sites (`country_event`/`province_event` effects) | 1500 |
| (a) `is_triggered_only` + FROM, fired with no country scope change | 6 |
| (a) FROM-reading events reachable only from a FROM-less `on_action` | 4 (all false alarms, see below) |
| (a) province events using country-only effects at province scope | 3 |
| (b) `random_list` summing to 0 | 0 |
| (b) `random_list` with a single entry | 0 |
| (b) `random = { chance = N }` with N <= 0 or >= 100 | 0 |
| (c) option blocks with no effect at all (only `name`/`ai_chance`) | 89 |
| (c) `major = yes` events that are not `is_triggered_only` | 198 |
| (d) `news = yes` without `news_desc_long/medium/short` | 0 |
| (d) news loc keys with no entry in any csv | 19 (7 events) |
| (d) `picture = "x"` missing (`python scripts/gfxtool.py missing`) | 0 |
| (e) modifiers added both with `duration = -1` and with a finite duration | 20 names |
| (f) `change_tag` to a tag with no registration/history file | 1 (false alarm, see below) |
| (f) `release`/`release_vassal` targets with no core in `history/provinces` | 92, of which **3** have no `add_core` anywhere |
| (g) `set_global_flag` names | 537 distinct; 19 look per-country |
| (h) province events whose trigger uses `owner = { ... }` with no ownership gate | 67 |

### Not defects (checked and dismissed)

- **on_actions FROM (4 hits)**: 90950 (`on_my_factories_nationalized`), 70002/70003/70004
  (`on_debtor_default*`). The engine defines FROM for these actions (nationaliser /
  debtor). No change needed; the heuristic's whitelist is just incomplete.
- **`change_tag = QNG`** (`events/Taiping.txt:1353`): the history file is
  `history/countries/QNG.txt`, not `QNG - Qing China.txt`. The engine keys on the first
  three characters, so it loads. Only a naming inconsistency with the other ~520 files.
- **89 empty options / 67 ungated `owner = {}` province triggers**: counted only, as
  requested. Empty options are mostly deliberate "acknowledge" outs on notification
  events; `owner = {}` on an unowned province simply evaluates false in Vic2.
- **`money = N` inside `any_pop`/`middle_strata`** is a pop effect, not a country
  effect - excluded from lens (a) after inspection of `BoerWar.txt`, `PER_crises.txt`.

## Defects

### High

1. `CoE_RoI_R/decisions/archaeology.txt:52` (also `:124`, `:218`, `:286`, `:355`, `:427`)
   - the six excavation decisions fire the "host asks permission" event from inside a
   province scope: `1767 = { province_event = { id = 19040 } }`. The event is
   `is_triggered_only` and its options do `FROM = { random_owned = { limit = { is_capital
   = yes } province_event = 19041 } }`, expecting FROM to be the *requesting great
   power*. Because the call is made in province scope with no country scope change, FROM
   is not the deciding country, so the follow-up ("Egypt Allows", 19041/19042 and the
   190411/201005/... siblings) fires in the wrong capital or nowhere. **Fix**: set a
   country flag / use `THIS` before descending, e.g.
   `1767 = { owner = { country_event = ... } }` from the GP scope, or have the decision
   do `THIS = { ... }` around the province call so FROM resolves to the great power.
   [high] - this is the single highest-value finding of this pass.
2. `CoE_RoI_R/events/archaeology.txt:1235` - province event 201009 executes
   `set_country_flag = inca_refused` at province scope (the sibling `relation`/`prestige`
   two lines above are correctly wrapped in `owner = { }`). The flag is silently not set,
   so the "Inca refused" branch never gates anything. **Fix**: move it inside the same
   `owner = { ... }` block. [high]
3. `CoE_RoI_R/events/BRZFlavor.txt:153` - province event 46302 does
   `set_country_flag = Sabinada` at province scope. Same class as above; the Sabinada
   revolt flag is never set. **Fix**: `owner = { set_country_flag = Sabinada }`. [high]
4. `CoE_RoI_R/events/GERFlavor.txt:107` - province event 33004 does
   `relation = { who = DEN value = 100 }` at province scope. `relation` requires a country
   scope; the +100 relation with Denmark never happens. **Fix**: wrap in `owner = { }`.
   [high]

### Medium

5. `CoE_RoI_R/events/newEvents.txt:502-854` - twelve `major = yes` "score milestone"
   events (ids **1100132-1100143**: Workshop of the World, and siblings) with the trigger
   `exists = yes` + a single score threshold (`industrial_score = 100`, etc.) and
   `mean_time_to_happen = { months = 1 }`. Every country in the world that crosses the
   threshold throws a full-screen popup at every player. With ~520 tags this is the worst
   popup-spam cluster in the mod. **Fix**: gate on `is_greater_power = yes` or
   `civilized = yes`, or drop `major = yes` and keep them as private events. [medium]
6. `CoE_RoI_R/events/CleanUp.txt:1532,1566,1600` - news events 60074, 60075 and 60076 all
   point at `EVTNAME60040_NEWS_TITLE` / `EVTDESC60040_NEWS_LONG/MEDIUM/SHORT`, and **none
   of those four keys exists in any csv** (`modcheck loc-find` confirms). Three copy-paste
   siblings all inherit the same dead keys, so the newspaper shows raw key text.
   **Fix**: add the 60040 keys once (they are referenced by four events), or repoint each
   event at its own `EVTDESC6007x_NEWS_*`. [medium]
7. `CoE_RoI_R/events/MOR.txt:109` - event 290115 uses a non-standard key scheme
   (`EVTNEWS290115_title/_long/_medium/_short`); none of the four keys exists. **Fix**:
   rename to `EVTNAME290115_NEWS_TITLE` / `EVTDESC290115_NEWS_LONG|MEDIUM|SHORT` and add
   them with `python scripts/modcheck.py loc-add`. [medium]
8. `CoE_RoI_R/events/DIM/PERFlavour_five_x.txt:4496` (`EVTNEWS190359_title`),
   `CoE_RoI_R/events/JAPFlavor.txt:251` (`EVTDESC97606_NEWS_SHORT`),
   `CoE_RoI_R/events/PORFlavor.txt:164` (`EVTDESC97000_NEWS_LONG`, borrowed from 97000)
   - remaining missing news loc keys, 19 in total across 7 events. **Fix**: same as above.
   [medium]
9. `CoE_RoI_R/events/BYZFlavorGVG.txt:119,150` vs `CoE_RoI_R/events/CrimeanWar.txt:703`
   - `protector_of_eastern_christendom` is added **permanently** (`duration = -1`) by the
   two GVG Byzantine events but only for **730 days** by the Crimean War event. The BYZ
   path is a forever-buff that the vanilla-derived path treats as temporary, and nothing
   removes it. **Fix**: pick one policy; if permanent is intended, add a
   `remove_country_modifier` when the protectorate lapses. [medium]
10. `CoE_RoI_R/events/CivilizationAndGunBoats.txt:1027` (`foreign_trading_post`,
    `duration = 3650`) vs `CoE_RoI_R/events/JAPFlavor.txt:178` (`duration = -1`); same
    pattern for `trade_restrictions` (`CivilizationAndGunBoats.txt:1128` = -1 vs
    `PORFlavor.txt:989` = 10950) and `the_homestead_act` (`ChileanEvents.txt:723` = 7650
    vs `decisions/ACW.txt:187` = -1). Each of these three modifiers has exactly one
    permanent and one temporary application, i.e. one of the two is almost certainly a
    typo. **Fix**: make the pair consistent. [medium]
11. `CoE_RoI_R/events/2nd_grand_revolution.txt:135,143` and
    `CoE_RoI_R/events/1german_revolution_1848.txt:722,1194,1291` - the 1848 chain stores
    per-country state in **global** flags whose names embed a tag
    (`1848_full_fra`, `1848_full_fra_rejected`, `1848_full_rus`, `1848_full_rus_rejected`,
    `1848_limited_fra`, `1848_limited_rus`, `1848_ger_victory_fra`, `1848_ger_victory_rus`,
    `1848_aus_ger_war`). This works only while exactly one country can be FRA/RUS/GER; the
    flags are never scoped and `clr_global_flag = 1848_full_rus` in one branch wipes state
    another branch depends on. Nine of the 19 suspect flags come from this one chain.
    **Fix**: convert to `set_country_flag` inside the relevant `FRA = { }` / `RUS = { }`
    scope where the state is genuinely per-country. [medium]
12. Other suspect global flags used for per-country state:
    `byz_eastern_protector` (`events/BYZFlavorGVG.txt:118,149`, read at `:16` inside a
    `tag = BYZ` trigger - works today, but blocks the flag from ever being reused),
    `rus_eastern_protector`, `armenia_renamed_tur` (`decisions/BYZ_Expansion.txt:1047`),
    `first_pbc_fell` (`events/PBCFlavor.txt:401` + `decisions/PBC.txt:281,346`),
    `fsa_right_to_secede` (`decisions/CSA.txt:173`), `kmt_has_lost`, `the_new_army`,
    `bab_has_appeared`, `hnd_independence_war`,
    `alt_american_civil_war_has_happened` (`events/Alternative ACW.txt:476,543`).
    **Fix**: audit each for whether more than one country can reach the setter; those that
    can should use country flags. [medium]

### Low

13. `CoE_RoI_R/decisions/gtfo.txt:95` (`release_vassal = PAK`), `:189` (`MLY`), `:351`
    (`LXA`) - the only three release targets in the whole mod with **no `add_core` in
    history, events or decisions**, so the tag can never exist as a vassal and the
    decision can never appear. (The other 89 "no province core" hits get cores from
    events and are fine.) **Fix**: give the tags cores or drop the three decisions. [low]
14. `CoE_RoI_R/history/countries/QNG.txt` - only country history file not named
    `TAG - Name.txt`. Harmless, but breaks tooling that splits on " - ". [low]
15. 89 option blocks with no effects and 67 ungated `owner = {}` province triggers -
    counted, not itemised; see the JSON output of `scripts/audit_events2.py`
    (`empty_ex`, `h_ex`) for representative examples such as
    `events/ACW.txt:2518`, `events/BerlinCongress.txt:2622`, `events/ACW.txt:1977`. [low]

## Clean results

`random_list` / `random = { chance }` weights are healthy across the whole tree (0 hits
in all three sub-checks). Every `news = yes` event supplies all three
`news_desc_*` keys. `python scripts/gfxtool.py missing` prints nothing, so no event,
decision or news layout references an absent picture.

## Fixed (2026-09-06)

- **#1 archaeology FROM** - the six ask/answer chains (19040/19041/19042, 190401/190411/190421,
  1904012/1904112/1904212, 201004-201006, 201007-201009, 201010-201012) are now `country_event`s.
  The decisions fire them with `any_country = { limit = { owns = <prov> } country_event = { id = X } }`,
  the idiom already proven in this mod (`decisions/Germany.txt` -> `GreatPowers.txt:19200`, where
  FROM is the decision-taker even through an intermediate country scope). All `owner = { }` wrappers
  inside the converted events were unwrapped, and `FROM = { random_owned = { limit = { is_capital = yes }
  province_event = X } }` collapsed to `FROM = { country_event = { id = X } }`. `$FROMCOUNTRY$` in
  EVTDESC19040/201004/201007/201010 now resolves to the requesting great power, and the
  `egypt_refused` / `maya_refused` / `inca_refused` / `crete_refused` / `greece_refused` /
  `mesopotamian_refused` flags land on the great power, which is where the decisions test them.
- **#2 (archaeology 201009)** - fixed as part of #1: `set_country_flag = inca_refused` is now a
  country-scope effect in the converted `country_event`.
- **#3 BRZFlavor 46302** - `owner = { set_country_flag = Sabinada }`. (Note: nothing in the mod
  reads `Sabinada`; the flag is decorative but now actually set.)
- **#4 GERFlavor 33004** - `owner = { relation = { who = DEN value = 100 } }`.
- **#5 newEvents 1100132-1100143** - these are *not* per-country milestones: each threshold has
  `fire_only_once = yes` (once per game, engine-wide), grants the exclusive
  `workshop_of_the_world` modifier and strips it from the previous holder via 1100144. So the
  ladder is a single travelling title, twelve popups per campaign at most, and one event per
  threshold is correct. `ai = no` would wrongly deny the AI the title. Only `major = yes` ->
  `major = no` on all twelve, so the popup goes to the country that earned it instead of the
  whole world. MTTH of 1 month is harmless with `fire_only_once`.
- **#6/#7/#8 news localisation** - added to `localisation/GVG_events.csv`:
  `EVTNAME60040_NEWS_TITLE`, `EVTDESC60040_NEWS_LONG/MEDIUM/SHORT` (shared by 60040, 60074, 60075,
  60076), `EVTNEWS190359_title`, `EVTDESC97606_NEWS_SHORT`, `EVTDESC97000_NEWS_LONG` (used by
  97003). `events/MOR.txt` 290115 instead had its whole `news = yes` block **removed**: 290115 is
  on the abandoned-event list in `.claude/skills/validate/SKILL.md` (no EVTNAME/EVTDESC either), so
  writing four newspaper strings for an event that cannot fire would be dead weight.
  `d_news_loc` is now 0.
- **#9 protector_of_eastern_christendom** - the mod's policy is *permanent with explicit removal*:
  `decisions/RUS.txt:356` and both BYZ events grant `duration = -1`, and `CrimeanWar.txt:538`
  (Treaty of Paris) plus `GreatPowers.txt:1004` remove it. `CrimeanWar.txt:704` (event 97516) was
  the lone `duration = 730` and is now `-1`. While there, BYZ event 1000205 (BYZ loses the war over
  the protectorate) set `rus_eastern_protector` but left BYZ holding the modifier and the
  `byz_eastern_protector` flag - it now clears both.
- **audit_events [high] 14540 / 22540** - "Exotic Fauna" and "Stock Exchange Opened" could re-fire
  forever, each time stacking a permanent province modifier. `fire_only_once` was wrong here (it is
  once per *game*, and these are generic events every country should be able to get), so both got a
  country-flag guard instead: `NOT = { has_country_flag = colonial_natural_history_museum }` /
  `local_stock_exchange_built` in the trigger, set in the option that grants the modifier.
  `audit_events` is back to 0 high, 0 medium.

## Deferred

- **#10 foreign_trading_post / trade_restrictions / the_homestead_act** - left alone. Unlike
  `protector_of_eastern_christendom` these have no removal machinery to tell which side is
  authoritative, and each pair sits in a different author's content (PDM vs DIM vs GVG); picking a
  duration would be a guess about intent, not a bug fix. `e_mixed_duration` therefore stays at 19.
- **#11/#12 global flags carrying per-country state**, **#13 gtfo release targets**, **#14 QNG
  filename**, **#15 empty options / ungated `owner = {}`** - unchanged; all are design decisions or
  cosmetic, and #11 in particular needs the 1848 chain redesigned rather than patched.
- The workshop ladder still has a design wart: because `fire_only_once` is engine-wide, a country
  that crosses `industrial_score = 100` after some other country already took that rung never sees
  the event. Working as the original author wrote it, so left as is.
