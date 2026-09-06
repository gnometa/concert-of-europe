# Logic audit — `CoE_RoI_R/events/GreatWar_Events.txt`

Reviewed 2026-09-06. Scope: entry conditions, world-wide `any_country` effects, `ai_chance`
extremes, effect magnitudes, dead branches, `FROM` chains, peace-conference partitioning.
Mechanical audits (modcheck braces/provinces/tags, refcheck, audit_events, cwtools) were at
baseline before and after the fixes below. Line numbers are post-fix.

## Fixed

- **12 (96000) — the Great War could never start; the whole file was dead code. [high]**
  The trigger ended with a mandatory `any_greater_power = { war_with = THIS
  has_country_flag = in_great_war }`, but `set_country_flag = in_great_war` and
  `add_country_modifier = { name = great_war }` exist *only* in this event's option
  (grep across the whole tree). No country can ever be the first to enter, so 96000 never
  fires, and with it neither the `great_war`/`great_war2`/`great_war3` escalation chain
  (96004-96006), the treaty/dismantling events (96010, 96035-96057), the "war is over"
  events (96020/96021), the colony transfers (96070-96081) nor 96085-96090. The Outrage /
  Assassination seeds (96065/96066) only hand out a `dismantle_cb`; they set no flag.
  *Fix*: the enemy GP now qualifies either by already being `in_great_war` **or** by being a
  non-exhausted `mass_politics = 1` great power, which bootstraps the first pair of
  belligerents and matches the intent of the second `OR` block just above it. Everything
  else about the entry gate is unchanged (still needs `war = yes`, GP/coalition/dismantle
  status, and no `great_war` modifier).
- **8202 (96065) and 8334 (96066) — a GP could grant itself `dismantle_cb`. [medium]**
  The `random_country` limit copied the trigger's `any_greater_power` block but dropped its
  `NOT = { tag = THIS }`, so the event root was a legal pick and `target = THIS` then aimed
  the CB at itself. *Fix*: `NOT = { tag = THIS }` added to both limits.
- **1668 (96021) — CAN/DNB/HUN/TKG lost their bespoke peace treaty. [medium]**
  96010 excludes 17 tags because each has a tag-specific treaty event (96035 GER/NGF/SGF/PRU,
  96038 NET, 96040 RUS, 96045 USA, 96049 CAN, 96050 ENG, 96051 JAP/TKG, 96053 HUN,
  96055 FRA, 96056 AUS/KUK/DNB, 96057 TUR — the partition is complete). 96021 ("war is over,
  lost") repeats that exclusion list but omits CAN, DNB, HUN and TKG. Those four, when
  reduced below secondary-power rank, matched 96021 (`days = 3`) which clears
  `dismantling_treaty`/`ultimatum_accepted` before their own treaty event (`days = 1..10`)
  could fire, silently skipping the whole dismantling. *Fix*: the four tags added to the
  `NOT` list, making it identical to 96010's.

## Reported, not changed

- **1618 (96020) vs 440 (96010) — no re-entry guard. [low]** Neither has `fire_only_once`
  (correct: it is engine-wide, one country firing would lock out everyone else), and both
  rely on the flag clean-up in their own option. A country that fights two great wars gets
  the full treaty twice; that appears intended.
- **1574 (96019) — no human-player priority. [low]** 96010's colony hand-out gives human GPs
  first refusal (96011) and only then falls through to AI GPs (96016) / secondary powers
  (96017) via `NOT = { any_greater_power = { ai = no truce_with = THIS } }`. 96019, the
  triggered variant, calls 96016/96017 directly without that guard, so in a game with a
  human GP at the table the AI picks first. Harmless but inconsistent.
- **628, 654 (96010) and the copies in 96035-96057 — `any_country` with `exists = no`.
  [low]** The Czechoslovakia release and the "release non-existing countries" block iterate
  `any_country` and then require `exists = no`. Whether `any_country` visits dead tags is
  version-dependent; PDM ships it this way and it is used identically in ~10 places here, so
  changing one would be inconsistent. If releases are observed not to happen in game, this is
  the first thing to test (swap for an explicit `TAG = { ... }` block).
- **`will_not_surrender` is cleared in 96010/96021 (and the tag variants) but set nowhere in
  the mod. [low]** Dead clean-up, harmless; either an InfamyWar flag that was renamed or a
  leftover. Left alone rather than guessing which.
- **8334 (96066) reuses `EVTOPTA96065`/`EVTOPTB96065` for its option names. [low]**
  `EVTOPTA96066` does not exist in any csv, so this is deliberate reuse, not a missing key —
  but the two events are otherwise identical apart from title/picture, so 96066 is
  effectively a second roll of 96065 with a different flavour text.
- **World-wide scopes are all bounded. [ok]** Every `any_country` in the file is narrowed by
  `truce_with = THIS`, `war_with = FROM`, `vassal_of = THIS`, `any_core = { owned_by = THIS }`
  or the `international_pariah` + `coalition_member` pair, so neutrals and the player are not
  hit by relation/core/secede effects they were not party to.
- **`FROM` chains are one hop deep. [ok]** 96000 -> 96025 (FROM = initiator) -> 96030
  (FROM = the GP seeking allies) -> 96031 (FROM = the country that accepted). No event reads
  `FROM` expecting a grandparent, and 96022/96076/96081 use `FROM = { ... THIS ... }` with
  `THIS` correctly meaning the event root.
- **`ai_chance` extremes are all deliberate. [ok]** The `factor = 100`/`factor = 0` pairs
  (96025, 96085) make the AI always seek allies and always accept the imposed government;
  the `factor = 0` modifiers in 96030 are ideology vetoes (communists never ally fascists and
  vice versa), not blanket refusals. 96070-96081 use 80/20 with GPs never refusing colonies.
- **Magnitudes are within engine range. [ok]** No `treasury`/`money` effects at all; the
  largest values are `relation = 200`, `diplomatic_influence = 200`, `war_exhaustion = 40`
  and `prestige = +/-2`, all engine-clamped. The `badboy = -1000` followed by
  `badboy = 24.99` in the eight treaty events is the mod's set-to-value idiom, not a bug.
- **The 1821 start is not a problem here. [ok]** Nothing in this file uses a `year =` gate;
  entry is gated on `mass_politics` (and `great_wars_enabled`, set by GreatPowers.txt 19355
  at `year = 1890`), so the machinery stays dormant until late-game tech regardless of the
  start date, and the 1947 end date leaves ample room.
