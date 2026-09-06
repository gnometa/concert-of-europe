# Legacy audit: SuffragetteMovements.txt / IssueSuggestion.txt

Scope: `CoE_RoI_R/events/SuffragetteMovements.txt` (ids 17000-17170) and
`CoE_RoI_R/events/IssueSuggestion.txt` (ids 3000-4001). Line numbers are
post-fix. `[fixed]` marks items applied in this pass.

## Verified clean

- Every `<issue_group> = <option>` pair in both files resolves against
  `common/issues.txt`, and every use is in the right group
  (`political_reform` -> political_reforms, `social_reform` -> social_reforms).
  No unknown reform option, no cross-group use.
- All `EVTNAME/EVTDESC/EVTOPT*` keys referenced exist in localisation.
- `has_country_modifier = female_suffrage` is granted by the
  `enact_female_suffrage` decision (`decisions/Political.txt:75`) and stripped
  by CleanUp event 60150, so 17170 is reachable and 17000-17160 do terminate.
- The multi-statement `NOT` blocks (3305 trigger, lines 864-871) read as NOR,
  which is what is wanted there (neither acceptable nor good tier).
- The chained `random_owned` reform ladders (3305 A/B, 3703 C) are ordered
  highest-tier-first, so no option cascades two steps in one click.

## Findings

- IssueSuggestion.txt 644, 659 — event 3301's options B and C were named
  `EVTOPTB3302` / `EVTOPTC3302`, so "The Familiar Institution" displayed
  event 3302's button text ("I belive we must bide our time") over effects
  that argue against a pension raise / repeal pensions entirely. — renamed to
  `EVTOPTB3301` / `EVTOPTC3301`, both of which exist and match the effects. —
  [high] [fixed]
- IssueSuggestion.txt 513 — event 3006 ("Dental Care Bill") is gated on
  `health_care = acceptable_health_care`, and option B ("Force it through")
  set `social_reform = acceptable_health_care`: a no-op, so the only reforming
  branch of the event did nothing while still paying the conservative
  militancy cost. — changed to `good_health_care`, the next tier up. —
  [high] [fixed]
- Both files, all 60 events — no `option` anywhere carries an `ai_chance`.
  The AI therefore picks uniformly among 2-3 options, several of which *roll
  reforms back* (3301 C `no_pensions`, 3401 A `no_subsidies`, 3701 C
  `no_work_hour_limit`, 3703 A `fourteen_hours`, 3801 C `no_minimum_wage`,
  3802 A `no_minimum_wage`, 3803 A `low_minimum_wage`, 3901 B
  `no_trade_unions`, 17050 C `no_meeting`). Net AI social-reform drift from
  this file is close to zero and can be negative. — add `ai_chance` to every
  option, weighting the progressive branch by `ruling_party_ideology` /
  `social_reform_want`. Deliberately not auto-applied: it is a balance
  change, not a correctness fix. — [medium]
- SuffragetteMovements.txt 1960-1965 — 17170 option B is
  `random_country = { prestige = -1 }` with no `limit`. It docks prestige from
  an arbitrary country anywhere on the map (possibly the player's own, or an
  uncivilised tag on another continent) for a decision about your own
  suffrage. — intended is almost certainly `prestige = -1` on the event
  country, or a `limit = { civilized = yes NOT = { tag = THIS } }`. Left alone
  because the intent is not recoverable from the option text. — [medium]
- IssueSuggestion.txt 2817 — event 4001 "$COUNTRY$ Has Abolished Slavery" is a
  one-off announcement (+2 prestige, -50 relations with a slaveholding
  neighbour) but has no repeat guard, so it re-rolls on a 200-month MTTH for
  as long as the country stays `no_slavery` with a slaveholding neighbour. —
  guard with `set_country_flag = announced_abolition` +
  `NOT = { has_country_flag = ... }`; do not use `fire_only_once`, which is
  engine-wide. — [medium]
- SuffragetteMovements.txt, all of 17000-17160 — same pattern: no country flag
  and no modifier is set by any option, and the only exit condition is the
  unrelated `enact_female_suffrage` decision. Each event re-rolls forever on
  its 600-month MTTH, so a long-lived democracy sees the same "Mud March" and
  "Hunger Strike" flavour repeatedly. — one shared
  `suffrage_flavour_<n>` flag per event, or an incrementing counter. —
  [medium]
- SuffragetteMovements.txt 363-413 — 17030 requires `year = 1900` in its
  trigger, yet its MTTH still carries `factor = 1.5 NOT = { year = 1880 }`,
  `NOT = { year = 1890 }` and `NOT = { year = 1900 }`. All three are
  permanently false; they are copied boilerplate. Same dead triple in 17110,
  17130, 17140, 17150, 17160 (all year-gated at 1890 or 1900). — drop the
  dead modifiers; note that MTTH 50 months for 17030 is already very fast for
  a war event. — [low]
- SuffragetteMovements.txt 439, 1256, 1459, 1563, 1677, 1788 — 17040, 17110,
  17130, 17140, 17150 and 17160 omit `invention = womens_suffrage_movement`,
  which every other event in the file requires. They instead lean on a bare
  `year = 1890`/`1900`, so a country that never researched the invention still
  gets suffragette hunger strikes. — add the invention check for consistency.
  — [low]
- SuffragetteMovements.txt 1535-1553 — 17130 "Lawless Suffragettes" has a
  single option, and that option is purely punitive (militancy on both
  conservatives and liberals). No player agency. — add a second option. —
  [low]
- IssueSuggestion.txt 2005-2026 — event 3701's options are declared in the
  order B, A, C, so the button labelled "If a little rest can keep them
  happy..." appears first and "Tick-tock, little puppets." second. The text
  still matches its own effects, so this is cosmetic ordering only. — [low]
- SuffragetteMovements.txt, whole file — the earliest anything here can fire
  is the `womens_suffrage_movement` invention or `year = 1870` via the
  decision, i.e. ~50 years after the 1821.9.1 bookmark. That is intentional,
  but it means the file contributes nothing to the mod's own start era; there
  is no early-19th-century franchise content to pair with it. — [low]
