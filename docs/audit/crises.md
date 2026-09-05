# Crises, flashpoints and crisis CBs

*2026-09-06. Reviewed: `events/crises.txt`, `events/CBGeneration.txt`, the core/CB events in
`events/CBsAndCores.txt`, `common/defines.lua` (`CRISIS_*`/`TENSION_*`), `common/cb_types.txt`
(`crisis = yes/no`). Compared against vanilla HoD in the game folder.*

## What the system does here

Crises are engine-driven. A state holding a foreign core its owner does not satisfy accumulates
flashpoint tension; when tension peaks the engine opens a crisis, invites GPs, and fires `20000`
(declare interest) and `20102`-`20105` (back attacker / back defender). Script can only push
tension around (`state_scope = { flashpoint_tension = n }`), add temperature, and gate who is
asked. The mod keeps vanilla `20000`-`20105` almost verbatim (trigger re-ordering from the perf
pass, plus the two changes below) and adds a **crisis-suppression layer**, `20110`-`20115`:

| Event | Role |
|---|---|
| `20110` | Native-American flashpoints: massacre or conciliate, both drop tension (-75/-50). |
| `20111` | No civilised claimant for the state -> tension -50, "nobody would intervene". |
| `20112` | A claimant carries the `recent_crisis` modifier -> tension -50, "this again?". |
| `20115` | The only *source* of scripted tension: high-infamy owners of foreign-core land, +20. |

`recent_crisis` (`common/event_modifiers.txt:2372`, an empty marker) is handed out by `20000`
option A to every non-GP crisis participant for **3650 days**, which is what `20112` reads. So the
mod's real pacing is: engine cooldown 5 years (`CRISIS_COOLDOWN_MONTHS = 60`, vanilla) plus a
scripted 10-year per-nation lockout, plus `CRISIS_BASE_CHANCE = 10` (vanilla 20) and
`TENSION_ON_REVOLT = 40` (vanilla 50). Every other `CRISIS_*`/`TENSION_*`/`RANK_n_TENSION_DECAY`
define is identical to vanilla.

`CBGeneration.txt` is unrelated to crises except that all ten events are gated on
`NOT = { involved_in_crisis = yes }`; the mod added `exists = yes` and slowed them from
`months = 3` to `months = 24`. `CBsAndCores.txt` contains no crisis or flashpoint logic; its
relevance is that it hands out and removes the cores that *become* flashpoints.

`cb_types.txt`: no CB that vanilla allows in a crisis was disabled. The mod marks 29 CBs
`crisis = yes` (vanilla relies on the default) and 57 `crisis = no`. Because the key defaults to
yes, 30 further mod CBs are crisis-capable without saying so.

**1836 assumptions: none.** The only date gate in `crises.txt` is `NOT = { year = 1900 }` on the
native-flashpoint suppressor, and no engine define delays crises, so crises are live from
1821.9.1. `audit_events.py` reports no 1836-era gate in any of these files.

## Defects

- **[high] `CoE_RoI_R/events/crises.txt:445` - `20110` could weight both options at 0.** Option A
  ("silence them") drops to `factor = 0` at `badboy = 0.92`; option B ("work with them") was
  `factor = 0` for theocracies, absolute monarchies and Prussian constitutionalism - the majority
  of 1821 governments. An autocrat at 23+ infamy had *no* non-zero option, and the engine's choice
  is then undefined (it falls through to the first option, i.e. the massacre the infamy guard was
  meant to stop). **FIXED**: that modifier is now `factor = 0.1`, so autocrats conciliate only ~3%
  of the time but the infamy brake actually engages.
- **[high] `CoE_RoI_R/events/crises.txt:34` - `20000` option B ai_chance `factor = 0`.** Declining
  crisis interest was unreachable for the AI, so every eligible GP joined every crisis and
  `recent_crisis` was stamped on all non-GP participants each time. Vanilla omits `ai_chance`
  there, i.e. weight 1 against 100. **FIXED**: restored to `factor = 1` (still ~1%).
- **[medium] `CoE_RoI_R/events/crises.txt:484` - `ai = yes` in `20111`'s claimant test. FIXED.**
  The `ai = yes` sat inside `any_core = { ... }`, so it tested the *claimant*, not the country the
  event fires for - it was never a "hide bookkeeping from the player" gate (`20111` has no `major`
  and a single option, and its sibling `20115` runs the mirror-image `any_core` test with no `ai`
  clause). Its only effect was asymmetric: when the sole civilised claimant to a flashpoint state
  was human-played, the `NOT = { any_core = ... }` came out true and the suppressor drained the
  player's own flashpoint tension by 50, while an identical AI claimant blocked it. Removed; the
  claimant filters that carry meaning (`civilized`, `NOT = { tag = THIS }`, `post_colonial_country`)
  are unchanged. Suppression is now rarer, i.e. slightly more crises.
- **[by design, not a defect] `CoE_RoI_R/events/CBsAndCores.txt:2101-2110` - assimilation does
  not remove the foreign core, and `2626` is deliberately dead.** `2625` requires an existing
  foreign core-holder in its trigger and sets `national_assimilation_complete` (10 days) for it,
  but the `any_country = { ... country_event = 2626 }` dispatch is commented out, so `2626` (its
  only possible caller - it is `is_triggered_only`, referenced by no decision, `on_actions.txt`
  entry or other event) never fires and no script path calls `remove_core`. **This was an
  intentional change, not rot**: commit `3d21520a` "no more disappearing cores + broken decision
  disabled" (Mitusonator, 2022-04-02) commented the dispatch out *and* replaced it in the same
  option with `add_core = THIS`, i.e. assimilation was re-designed to hand the assimilator a core
  instead of stripping the claimant's. The same commit dropped the `badboy = 2` cost and cut the
  MTTH from 300 to 120 months. Restoring the call would revert a deliberate design decision and
  reintroduce exactly the "disappearing cores" the author removed, so `2626` is left disabled and
  stays on the abandoned-events list in `.claude/skills/validate/SKILL.md`. Consequence to accept:
  foreign cores are monotonic (`2560`, `2605`, `2625` only ever `add_core`), so flashpoint sources
  accumulate over a 94-year game - which is part of why the suppression layer above exists.
  Cosmetic leftovers, harmless and left alone: `2625`'s `any_core` trigger clause and the 10-day
  `national_assimilation_complete` marker now have no reader.
- **[moot while `2626` is dead] `CoE_RoI_R/events/CBsAndCores.txt:2130-2133` and `:2191-2194` -
  `2626`'s core removal targets the wrong scope.** `FROM = { random_owned = { limit = { is_core =
  THIS } remove_core = THIS } }`: inside `random_owned` the current scope is a province, so `THIS`
  resolves to that province, not to the claimant country the event fires for; `remove_core = THIS`
  needs a country (`docs/wiki/list-of-effects.md`). Anyone reviving `2626` must first make the claimant
  reachable from inside `FROM`'s province loop (Victoria 2 rebinds `THIS` on every scope change,
  so neither `THIS` nor `FROM` names the claimant there) and verify the result in-game. Not fixed
  here, because correcting a scope inside an event that can never fire only makes dead code look
  live.
- **[medium] `post_colonial_country` is a dead flag.** Both setters are commented out
  (`decisions/New Colonies.txt:558,1780`), yet 30+ triggers test it, including `crises.txt:487` and
  `:597`. In the crisis events the effect is benign (the exclusion is inert, so suppression fires
  slightly less often), but the same dead flag gates `NationalUnification.txt` and
  `rebel_types.txt`. Out of scope here; needs its own pass.
- **[low] `CoE_RoI_R/events/crises.txt:51,106` - `the_watchers_on_the_wall` is checked and never
  set** (one of refcheck's 129 known orphan flags). Its setter is the commented-out `20120`
  "disable crises" prompt at the bottom of the file. Deliberate dormant hook; leave the gates and
  the block alone, or delete the whole feature together.
- **[low] `CoE_RoI_R/events/crises.txt:16` - `exists = no` inside `any_country`.** `any_country`
  only iterates living tags, so that half of the `OR` never contributes. Harmless.
- **[low] `CoE_RoI_R/events/crises.txt:598` - `exists =yes` (missing space) in `20115`.** Parses,
  but it is the only occurrence of that spacing in the file.

## Design observations

1. **The mod is a crisis *dampener*, not a crisis generator.** Three of the four added events only
   subtract tension (-50 to -75, on 12-36 month timers); the fourth adds +20 on a 250-month timer
   and only for owners above ~15 infamy. `CRISIS_BASE_CHANCE` is halved and participants get a
   10-year lockout on top of the engine's 5-year cooldown. Against a 1821 start with PDM's dense
   core map that is defensible for the first decades, but nothing ever re-opens the tap: expect
   very few crises after ~1860 even as the number of unredeemed cores grows. If "interesting
   crises" is the goal, the lever with the least collateral damage is the `recent_crisis` duration
   (3650 -> ~1825 days), not `CRISIS_BASE_CHANCE`.
2. **GP intervention AI is vanilla and close to unanimous escalation.** `20102`/`20103` weight
   backing at 95:5 and add `add_crisis_temperature = 10`; `20104`/`20105` at 70:30. With the
   interest event now 100:1 instead of 100:0, a crisis that starts still reaches war temperature
   almost deterministically. The war-policy MTTH modifiers only change *when* a GP is asked, not
   what it answers, so pacifist GPs escalate as readily as jingoists. A cheap believability win:
   mirror those war-policy modifiers into the `ai_chance` of `20102`-`20105` (pacifism and
   anti_military lowering the back-the-crisis factor), leaving the vanilla base weights.
3. **`recent_crisis` is granted at *interest* time, not at resolution.** A crisis that fizzles
   because no GP backed a side still burns the 10-year lockout for every small nation involved.
   Granting it on the resolution path, or shortening it, would read better.
4. **30 CBs are crisis-capable by default**, including `restore_byzantine_empire`,
   `restore_america`, `restore_austrian_empire` and the six `place_in_the_sun*` tiers. A GP can
   attach a continental-scale wargoal to an unrelated Balkan crisis. An explicit `crisis = no` on
   the "restore empire" CBs would cost nothing and remove an absurdity.
5. **Perf follow-up for `20110`-`20112`/`20115`** (flagged at 65,003 in `docs/audit/performance.md`
   as having "no leaf gate"): `has_flashpoint` and `flashpoint_tension` are documented as
   *province* conditions (`docs/wiki/list-of-conditions.md:2230,2314`). Hoisting
   `state_scope = { has_flashpoint = yes flashpoint_tension = 50 }` to bare top-level clauses would
   replace the state-scope switch with two leaf gates that reject ~99% of provinces immediately.
   It needs an in-game rate check first, since it assumes the province-level condition reads the
   same state value.
