# Logic audit: `events/NETFlavor.txt` + `events/BELFlavor.txt`

*2026-09-06. Line-by-line read of the Dutch flavour file and the PDM Belgian secession /
London Conference chain (36700-36746), against tonight's `BELRevolutionGVG.txt` prelude
(1000301-1000308) and `JavaWarGVG.txt` (1001300-1001302). Mechanical audits
(`modcheck braces/provinces/tags`, `refcheck`, `audit_events`, `cwtools_check`) were clean at
baseline and still are; everything below is logic, not syntax.*

`[fixed]` marks what this pass changed in place.

## High

- **BELFlavor.txt 443/491/569/622 - 36711, 36715, 36716 - misspelt flag `signed_treay_of_london`.**
  The whole alternate Treaty-of-London path set and tested the typo, while the conference path
  (36739/36740), `decisions/NET.txt` (`mediate_belgian_independence`, `repudiate_treaty_of_london`)
  and `NETFlavor.txt` 40/153 use the correct `signed_treaty_of_london`. Consequence: after NET
  signed via 36711/36716, ENG could immediately re-run `mediate_belgian_independence` and stage the
  treaty a second time, and NET could never repudiate it. `history/countries/NET - Netherlands.txt:136`
  had the same typo, so the 1861 bookmark shipped the dead flag too.
  *Fix:* renamed all five to `signed_treaty_of_london`. `[fixed]`
- **BELFlavor.txt 829 - 36725 - the PDM London Conference has no gate against the GVG prelude.**
  `BELRevolutionGVG.txt` is the scripted 1830 revolution and runs its own conference
  (1000303 FRA / 1000304 ENG / 1000305 Twenty-Four Articles). 36725 only asks
  `BEL = { exists = yes }`, so as soon as 1000302 releases Belgium every European GP starts a
  *second* conference with partition options on top of the first - the duplicated episode 36720
  was already gated against.
  *Fix:* added `NET = { has_country_flag = BEL_revolt_in_progress }` to 36725's `NOT` block,
  mirroring 36720. `[fixed]`
- **BELFlavor.txt 1539 - 36740 option B - the refusal partitions Belgium anyway.**
  Option name is "We refuse! Belgium belongs to us!", but the effect ran the identical three
  `any_owned` blocks as the acceptance branch: 381/396/397/398 to PRU, 387/392-395 to FRA,
  388-391 to FLA, plus `create_vassal = FLA` for the host. NET therefore gave away everything it
  had just refused to give away, and paid extra infamy and relation penalties for the privilege -
  the branch was strictly worse than accepting, so it was dead in practice.
  *Fix:* option B now keeps Belgium (`inherit = BEL` only) and hands PRU and FRA a relation hit
  plus `free_peoples`/`cut_down_to_size` CBs on NET instead. `[fixed]`

## Medium

- **BELFlavor.txt 829 - 36725 - no `NET = { exists = yes }` and no date floor.**
  36735/36736/36737 all require `NET = { exists = yes }` to resolve, so if the Netherlands is
  annexed mid-conference `london_conference_1830_in_progress` and every GP's
  `attending_london_conference_1830` flag stay set forever, permanently blocking the chain.
  The event is also named for 1830 but had no year gate at all, so an early Belgian release from
  the 1821 start could stage "the London Conference of 1830" in, say, 1824.
  *Fix:* added `year = 1830` and `NET = { exists = yes }` to the trigger. `[fixed]`
- **BELFlavor.txt 1251 - 36738 option A - effects continue in an annexed scope.**
  The option runs in BEL scope and does `NET = { inherit = BEL }`, then afterwards fires
  `any_country = { ... country_event = 36741 }` from the now-annexed BEL. The acknowledgement to
  the conference attendees (which is what clears `hosting_/attending_/supporting_*` on everybody)
  was riding on a dead country.
  *Fix:* moved the `any_country ... 36741` dispatch above the `NET = { inherit = BEL }` block. `[fixed]`
- **BELFlavor.txt 765/793 - 36720 - the fallback secession never clears `united_netherlands`.**
  `BELRevolutionGVG.txt` clears it on all three branches, and `FRAFlavor.txt` 1603/1629 tests it.
  Going through the PDM fallback left NET flagged as the united kingdom after losing Belgium.
  *Fix:* added `clr_country_flag = united_netherlands` to both options. `[fixed]`
- **BELFlavor.txt 1402 - 36739 - `ai_chance` favours defying the whole Concert.**
  Accept 40 vs refuse 60, i.e. the AI Netherlands rejects the Great Powers' verdict on Belgian
  independence about 60% of the time, with no gate on being a Great Power itself. The parallel
  Belgian event 36710 uses 80/20 and gates refusal on `is_greater_power`.
  *Fix:* 75/25 in favour of accepting. `[fixed]`
- **BELFlavor.txt 1291 - 36738 option B - `badboy = 25` in a single click.**
  25 infamy is the containment threshold on its own; refusing reunification instantly made Belgium
  a legitimate target for every Great Power, which is not what the flavour text describes
  (the sibling refusals in 36739/36740 charge 15).
  *Fix:* lowered to 10. `[fixed]`
- **NETFlavor.txt 47 - 46450 - effects hardcoded to province 387 while the trigger scans for any.**
  The trigger requires `any_owned_province = { is_core = WLL culture = wallonian NOT = { has_province_modifier = wallingants } }`,
  but the option then added the core, the pop effects and the `wallingants` modifier to 387
  (Brussels) unconditionally. If NET does not own Brussels - the common case, since Belgium may
  have taken it - the modifier landed on another country's province while
  `wallingant_provinces` was still set to 1, desynchronising the counter that 46453 gates on.
  *Fix:* replaced `387 = { ... }` with `random_owned` carrying the trigger's own limit. `[fixed]`
- **BELFlavor.txt 441 - 36711 - Luxembourg can be left stateless.**
  36710 removes the LUX core from 398 whenever `LUX = { exists = no }`, but the actual
  `release_vassal = LUX` sits inside `random_owned = { limit = { province_id = 397 } }` in the
  follow-up event. If NET did not end up owning 397 (Belgium never held it, or a war moved it),
  the core is gone and the vassal is never released. Not fixed: the correct behaviour depends on
  which 1830 path ran, and 36739 handles 397 separately.

## Low

- BELFlavor.txt 1439 - 36740 option A - 388/389/390/391 are seceded to FLA and then
  `391 = { secede_province = NET }` takes Hasselt straight back, after `391 = { add_core = NET }`.
  It works out (NET keeps Limburg) but reads as an accident; a single `NOT = { province_id = 391 }`
  in the FLA limit would say it plainly.
- BELFlavor.txt 1123/1183 - 36736 and 36737 both use `title = "EVTNAME36735"`, and 36743/36746
  reuse `EVTNAME36742`/`EVTNAME36745`. All three conference outcomes therefore share one headline.
- BELFlavor.txt 1063-1240 - 36735/36736/36737 resolve on `check_variable value = 2`, i.e. two
  votes, with identical 60-day mtths. With a 5-6 GP conference the outcome is close to a coin flip
  between whichever two options cleared 2 first; there is no tie-break on the larger count.
- BELFlavor.txt 598 - 36716 option B repeats the same `random_owned` colonial-port block twice to
  take two Dutch colonial states. Deliberate, but the second pass can re-roll the same state and
  quietly do nothing.
- NETFlavor.txt 493 - 95252 tests `NOT = { has_country_flag = malacca_treaty }`; nothing in the mod
  ever sets that flag (`DIM/EastIndiesFlavor.txt:116` only reads it too). Harmless - the event is
  `fire_only_once` - but the check is decorative.
- NETFlavor.txt 383 - 46453 sets `WLL = { capital = 387 }` after `release_vassal = WLL`; if Brussels
  did not end up in Wallonia's release the capital assignment is a no-op.
- NETFlavor.txt 288 - 46453 mtth `modifier = { factor = 0.5 NOT = { ... } year = 1918 }` only ever
  applies after 1918, which for a chain gated behind `mass_politics` and `separatism` means it
  almost never bites.

## Checked and clean

- Recipients in the chain hop correctly: 36709 (NET) -> 36710 (BEL) -> 36711 (NET);
  36715 (NET) -> 36716 (BEL); 36735 -> BEL 36738; 36736/36737 -> NET 36739/36740; the
  acknowledgement events 36741-36746 all run in the recipient's own scope and clear their own flags.
- `THIS` in 46453's `WLL = { all_core = { remove_core = THIS } }` is the event root (NET), which is
  what the effect wants.
- The multi-statement `NOT` blocks in 36720, 36725 and 46450 are all intended as NOR.
- 95253's Anglo-Dutch exchange correctly wraps the British half in `ENG = { any_owned = { ... } }`,
  so no province effects run against the wrong owner (cf. `docs/audit/owner-scope.md`).
- No date window in either file is unreachable from the 1821 start; the flavour events
  (36700/36701/36704/36705/36706) all sit in 1837-1864 with `fire_only_once`, which is engine-wide
  and correct here since each is gated on `tag = BEL`.
