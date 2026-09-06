# Legacy audit: ColonialUprisings.txt + CivilizationAndGunBoats.txt

*2026-09-06. Line-by-line logic review of the colonial-revolt and westernisation/gunboat
machinery (events 14500-14810 and 13000-13358 + 90910/90950). Format:
`file line id - problem - fix`. Fixed items are marked **[fixed]**.*

## High

- `events/ColonialUprisings.txt:1489` 14670 - "The Heart of Darkness", option A
  (*"$COUNTRY$ apologizes for nothing"*) applied `badboy = 15`. Infamy 25 is the pariah
  threshold, so a single click put a colonial power 60% of the way to being dogpiled, and the
  only brake is one `ai_chance` modifier at `badboy = 0.25`. Option B (*"We accept full
  responsibility"*) costs 5. - **[fixed]** `badboy = 15` -> `badboy = 8`; option B left at 5 so
  defiance still costs more.

No other high-severity defect was found. Two things that look wrong on a first read are not:

- `CivilizationAndGunBoats.txt:397` 13021 uses `add_casus_belli = { target = THIS }` inside a
  `random_country` scoped to FROM (the uncivilised sender). `add_casus_belli` gives *the target* a
  CB against *the scoped country* (the inverse of `casus_belli`), so this correctly hands the
  European power a CB against the unciv. Do not "fix" it.
- The 13240 -> 13250 -> 13260 -> 13270 chain fires each hop from inside a `FROM = { ... }` block.
  FROM in the receiving event is the *root* of the firing event, not the block scope, so the
  GP <-> unciv alternation holds all the way to the Opium War CB. Verified against
  `docs/wiki/event-modding.md` (the rock-paper-scissors sample chain).

## Medium

- `CivilizationAndGunBoats.txt:387` 13016 - option text said *"Shut down the ring immediately."*
  while the effect adds a permanent (`duration = -1`) `local_opium_habit`, i.e. the crackdown
  creates the addiction it claims to stop. - **[fixed]** option renamed to
  *"Break up the ring - the habit has already taken root."*; effects unchanged.
- `CivilizationAndGunBoats.txt:629` 13021 - the `factor = 0` vetoes for `war = yes` and
  `war_policy = pacifism` sat on option B (*"There is nothing we can do"*), so a great power
  already at war, or a pacifist one, **always** picked the aggressive option that adds a CB and
  drops relations 25. Backwards. - **[fixed]** both modifiers moved onto option A.
- `CivilizationAndGunBoats.txt:1694` 13065 - banning opium in one of our own states made a
  `random_country` great power (gated only on `num_of_ports = 1`, with no continent or interest
  test, unlike every sibling event in the file) lose 40 relations. Every comparable event in the
  file uses -5, -20 or -25. - **[fixed]** -40 -> -20. The missing continent gate is left alone;
  it would change which GP is picked.
- `CivilizationAndGunBoats.txt:2321` 13150 - this is a **province_event**, so `THIS` is the
  province; `any_country = { limit = { is_greater_power = yes } relation = { who = THIS ... } }`
  passes a province where the engine wants a country tag. Either a no-op or garbage. Not fixed:
  there is no in-scope way to name the owner (`owner = { ... }` does not rebind `THIS`); the
  correct repair is to route the option through a triggered country event on the owner, which is
  a content change rather than a bug fix.
- `ColonialUprisings.txt:670`, `:688` 14580 - both options filter pops with
  `any_pop = { limit = { is_state_religion = yes/no } }`. Pops in this mod carry a sub-culture in
  the religion field, so pop-scope religion tests are dead (see `docs/audit/religion-dead-content.md`).
  Reported only - per project rule, religion-form triggers are never converted to culture forms.
- `ColonialUprisings.txt` 14570/14630/14640/14810 (lines 584, 1123, 1201, 2517) - four separate
  events whose triggers overlap almost completely (`colonial_nation = yes`, `civilized = yes`)
  and whose only effect is "non-accepted pops in a random colonial state get militancy +3..+5 and
  separatist +0.10..+0.25". None is `fire_only_once`, so a colonial empire eats all four on
  repeat and separatism inflates well past what the revolt system expects. Duplicated episodes;
  needs a design decision (merge, or gate them on distinct conditions), not a mechanical fix.

## Low

- `ColonialUprisings.txt:795` 14600 - lowercase `or = {`. Parses, but CWTools and grep-based
  tooling miss it; the same trigger also wraps `has_global_flag` in an `owner = { ... }` scope
  inside `any_owned_province`, which is redundant (global flags are scope-free).
- `ColonialUprisings.txt:1500` 14670 - option A sets `militancy = 10` and `consciousness = 10`,
  the engine maxima, on every non-accepted pop of a state, on top of separatist +0.5. With the
  badboy fix above the option is no longer a self-destruct button, but the revolt is still
  guaranteed. Left as authored flavour.
- `ColonialUprisings.txt:2329` 14780 - option A kills 20% of every pop in a colonial state
  (`reduce_pop = 0.8`) *and* permanently lowers `life_rating`; the paid option B only kills 5%.
  Plague magnitudes elsewhere in the file are 0.95-0.99. `treasury = -10000` for option B is also
  the largest cash figure in either file. Line 2333 is unindented (`change_variable`).
- `ColonialUprisings.txt:2535` 14810 - "The Natives are Restless" uses `picture = "Hospital"` and
  hands the player `heavy_industry = 5` (5 units of the good into the national stockpile) for
  provoking separatism. Both look like copy-paste debris; harmless.
- `CivilizationAndGunBoats.txt:333` 13015 - `treasury = 5000` for confiscated contraband is a
  windfall on the scale of a great-power event, paid to an uncivilised nation.
- `CivilizationAndGunBoats.txt:3554` 13250 - inside `FROM = { ... }` (the unciv) the option runs
  `diplomatic_influence = { who = THIS value = -20 }`, i.e. the unciv loses influence *in the
  great power*. Uncivilised nations hold no influence, so it is a no-op; the intent was probably
  the reverse direction. Left alone because reversing it changes who is punished.
- `CivilizationAndGunBoats.txt` 13050 (:1064), 13065 (:1633), 13090 (:1872) - unlike every
  neighbouring event these triggers omit `civilized = no`, so they keep firing for a nation that
  westernised while a `foreign_trading_post` / `local_opium_habit` province modifier survived.
  90910 strips those modifiers on westernisation, so the window is narrow.
- `CivilizationAndGunBoats.txt:2391` 13160 - the option block carrying `EVTOPTB13160`
  ("Execute him") is written before the one carrying `EVTOPTA13160` ("Hand him over"), so the
  displayed order is B then A. Cosmetic; the effects match their own labels.
- `CivilizationAndGunBoats.txt:2259` 13140 - `war_exhaustion = 20` in a single, optionless event.
  Large, but it is gated on being at war with a European military mission in the country.

## Windows and start-date exposure (1821.9.1)

Nothing in either file is unreachable from the 1821 start. The only absolute year gate is
`year = 1860` on 14660 (Heia Safari, deliberately late-scramble); everything else is gated on
tech/inventions (`biologism`, `nationalism_n_imperialism`, `empiricism`, `mission_to_civilize`,
`ideological_thought` for the Doctrine of Lapse) or on modifiers the 13000 chain hands out from
month 6. `audit_events.py` reports no `[high]` and no unknown keywords for either file.

## `activate_unit = regular`

Re-checked as asked. The commented-out `#activate_unit = regular` at
`CivilizationAndGunBoats.txt:3959` (event 90910, westernisation) and the twin at
`events/China.txt:59` are the only event-side uses left in the mod. `units/regular.txt` has
`active = no`, but `inventions/other_inventions.txt:2097` still runs `activate_unit = regular`
in an invention `effect`, which is a valid context, so a newly civilised nation unlocks regulars
there. Nothing else depends on the removed effect.

## Verification after the fixes

`modcheck braces/provinces/tags` on both files: clean (2 files ok, 0 bad province refs, 0 unknown
tags). `refcheck.py`: 14 events / 0 onactions / 60 loc / 0 modifiers / 127 flags / 0 names /
8 options - unchanged from the pre-edit baseline. `audit_events.py`: 0 unknown keywords,
`[high] 0`, `[medium] 0`. `cwtools_check.py`: 0 errors; no diagnostic in either file.
