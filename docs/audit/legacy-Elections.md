# Legacy audit: ElectionEvents.txt / ExtraElectionEvents.txt

Line-by-line logic review of the election campaign chain (every democracy, prussian
constitutionalism, HMS government and socialist democracy sees these -- see
`common/governments.txt` `election = yes`). Line numbers are as of the review; the
[high] and unambiguous [medium] items were fixed in place, so post-fix lines shift by
+1..+2 in `ExtraElectionEvents.txt` after line 3066.

Party-issue groups checked against `common/issues.txt` `party_issues`:
`trade_policy`, `economic_policy`, `religious_policy`, `citizenship_policy`, `war_policy`.

## Fixed

- **ExtraElectionEvents.txt 3066, 3098 - 140601 "Wretched Craftsmen" - [high]**
  `scaled_militancy = { issue = anit_industrial }` and
  `dominant_issue = { value = anit_industrial }` - `anit_industrial` is a typo; the
  `economic_policy` option is `anti_industrial`. Both effects were silently no-ops, so
  option A and option B lost half their intended payload (option B still applied
  `anti_industrial` correctly to non-craftsmen, which is why the typo went unnoticed).
  *Fixed:* renamed to `anti_industrial` (2 sites).

- **ExtraElectionEvents.txt 4108, 4177 - 142501 "The Right to Freedom", 142601
  "Slavery Debate Turns Violent!" - [high]**
  Both are `election = yes` + `is_triggered_only = yes` but carry **no `issue_group`**.
  The engine draws campaign events from the per-issue-group pools, so an
  `is_triggered_only` election event with no group is never fired: in all of vanilla
  there is exactly one `election = yes` event without an `issue_group`
  (`DANFlavor.txt` 36208) and it uses a `mean_time_to_happen` instead. Both events are
  fully written and localised but dead. They are state-scoped (`is_colonial`,
  `owner = {}`, `any_pop`), so converting them to mtth country events is not an option.
  *Fixed:* `issue_group = citizenship_policy` on both - slavery is the citizenship
  question, the group they thematically belong to, and their `slavery = yes_slavery`
  trigger keeps them confined to slave-holding states.

- **ExtraElectionEvents.txt 3013 - 140501 "Hands-Off Professor", option C
  ("Throw him in jail for deviant behavior") - [medium]**
  `scaled_militancy = { issue = pluralism factor = -4 }` alongside
  `{ issue = moralism factor = -4 }`. Jailing a man for private "deviant behaviour"
  cannot calm *both* camps; `pluralism` is the religious-tolerance stance and its
  supporters are the ones outraged by the arrest. The moralism `-4` is right.
  *Fixed:* `pluralism` factor `-4` -> `4`.

- **ExtraElectionEvents.txt 3389-3392 - 140801 "Tensions in the Graveyard", option D
  ("An excellent chance to provoke some violence.") - [medium]**
  `reduce_pop = 0.95` + `militancy = 8` + `consciousness = 8` on every
  non-state-religion pop in the state. That kills 5% of the state's religious
  minorities and pushes them straight past the revolt threshold, off a *graveyard
  dispute*, with no ai_chance guard (the AI takes it roughly 1 election in 4). No other
  option in either file exceeds `militancy = 4`, and `reduce_pop` appears nowhere else
  in the chain.
  *Fixed:* `reduce_pop = 0.99`, `militancy = 4`, `consciousness = 4` - still the pogrom
  option, at the magnitude the rest of the file uses.

## Reported, not fixed

- **ExtraElectionEvents.txt 1636 - 98314 "fascist election win" - [medium]**
  Guards only `NOT = { OR = { government = hms_government... } }`, while the sibling
  radical-win events 98313 (communist, line 1438) and 98316 (anarcho-liberal, 2017)
  also exclude `prussian_constitutionalism1..3`. Either the fascist event is missing the
  exclusion or a fascist win under a semi-authoritarian monarchy is deliberate; both
  readings are defensible, so left alone. If it is an oversight, add the second `OR`
  block to match the siblings.

- **ExtraElectionEvents.txt 854-2409 - 98310..98317 - [low]**
  The eight "election concluded" events between them cover ruling-party ideologies
  conservative, socialist, liberal, communist, fascist, reactionary, anarcho_liberal,
  social_liberal. `common/ideologies.txt` also defines `pro_slavery`, `abolitionist`,
  `separatist`, `subordinate` and `insubordinate`. No party in `common/countries/*.txt`
  uses any of those five today, so there is no live gap - but if one is ever given to a
  party, that country's `election_initialized` flag and its `wartime_elections` /
  `violent_elections` / scandal modifiers are never cleared, and because 98300-98305 all
  require `NOT = { has_country_flag = election_initialized }` the whole election chain
  switches off permanently for that tag. Worth a catch-all event if such a party is added.

- **ExtraElectionEvents.txt 5380, 5572, 5796, 6056 - 999013..999016 - [low]**
  6, 7, 8 and 6 options; the UI clips at 5. Already in the `refcheck options` baseline
  (8 findings); listed here only so it is not rediscovered as new.

- **ElectionEvents.txt 11 - 14000 "Trade Policy" - [low]**
  An `issue_group = trade_policy` event whose options also nudge `interventionism` and
  `laissez_faire`. This is the vanilla/PDM pattern (correlated economic stances move
  with trade stances) and harmless; the `issue_group` only selects the debate slot.

- **ElectionEvents.txt (whole file) - [low]**
  No `ai_chance` anywhere in the 22 state debates, so the AI picks uniformly among 4-5
  options, including the extreme ones. `ExtraElectionEvents.txt` weights its national
  campaign events properly (41 `ai_chance` blocks, `factor = 25` with a `factor = 2`
  bump for the ruling party's own ideology - no option is ever forced). Matches vanilla
  `ElectionEvents.txt`, so baseline, but it is why the 140801 pogrom option mattered.

- **ExtraElectionEvents.txt 590, 815, 1444, 1642, 2023, 3038, 9196, 9202, 9261 - [low]**
  Multi-statement `NOT` blocks, i.e. `NOR`. Checked each: in every case "none of these
  may be true" is the intended reading (calm-election gates, government exclusions,
  cooldown/revolt gates). No fix needed.

- **ExtraElectionEvents.txt 2521 - [low]**
  Comment `#Officer and Supply` sits above 140101, whose localised title is
  "A War Hero Speaks Out". Cosmetic.

## Checked clean

- No duplicated events between the two files: `ElectionEvents.txt` holds 14000-14210
  (22 state debates), `ExtraElectionEvents.txt` holds 98300-98317 (election
  init/conclusion), 140001-142601 (16 extra state debates) and 999000-999065 (national
  campaign). Titles and issue groups are all distinct; no id collisions
  (`modcheck ids` clean).
- Every `issue_group` matches the issue values the options actually move, apart from the
  two entries above.
- All `dominant_issue` / `scaled_militancy` / `scaled_consciousness` `value=`/`issue=`
  names resolve against `common/issues.txt` (after the `anit_industrial` fix), all
  `ideology =` names against `common/ideologies.txt`.
- All `add_/remove_/has_country_modifier` names resolve (`election_cooldown`,
  `wartime_elections`, `violent_elections`, `ruling_party_scandal`,
  `party_scandal_evidence`, `support_the_government`).
- No renamed reforms: no `political_reform`/`social_reform` effect in either file
  references a name missing from `common/issues.txt`.
- Every `999xxx` event is gated on `election = yes` + `has_country_flag =
  election_initialized` + a cooldown check, and every option that ends a debate applies
  `election_cooldown`. No path leaks an event outside an election.
- No trigger excludes a government that holds elections: the only `government =` tests
  are the deliberate HMS / prussian-constitutionalism exclusions above.
- All `EVTNAME/EVTDESC/EVTOPT*` keys referenced by both files exist in
  `localisation/*.csv`.
