# Legacy audit — events/NationalUnification.txt

Line-by-line logic review of the German/Italian/Yugoslav unification machinery
(events 11100-11125, 98650, 98651). Mechanical audits (`modcheck braces/provinces/tags`,
`refcheck`, `audit_events`, `cwtools_check`) were clean at baseline and still are;
everything below is behavioural. Line numbers are **post-fix**.

Reference notes used: multi-statement `NOT = { a b }` is NOR (docs/wiki/list-of-conditions.md);
`THIS` resolves to the event's root country even inside nested scopes;
`casus_belli` grants the **scoped** country a CB on `target`, while `add_casus_belli`
grants the **target** a CB on the scoped country (docs/wiki/list-of-effects.md:245-247).

## Fixed

- **620 / 11107 — `religion = south_german` where the twin branch uses `culture = north_german` — [high]**
  The NGF half of the "three hurrahs" trigger asked for an owned GER-core province whose
  *religion* is `south_german`. `north_german`/`south_german` are cultures (they are pop
  cultures in `history/pops/1821.9.1/German States.txt`); `common/religion.txt` only
  matches because the whole culture list is appended to it by mistake (pre-existing, out of
  scope, see Observations). This is the exact twin of the earlier `:969` fix, which sets
  `culture = north_german` in 11110, and of 11107's own SGF branch at 624-629.
  *Fixed:* `culture = south_german`. Both halves of 11107 are now symmetric and live.

- **1032 / 11110 — `is_cultural_union = no` trapped inside a NOR — [high]**
  `NOT = { tag = THIS  has_country_flag = post_colonial_country  is_cultural_union = no }`
  reads as "not us AND not post-colonial AND **is** a cultural union". The only germanic
  cultural union is GER, and the event's own trigger requires `NOT = { exists = GER }`, so
  the block matched nothing: no German minor ever handed its cores to the newly formed NGF.
  The very next `any_country` (1036-1046) still invites those same minors via 11106, so the
  branch was silently dead rather than visibly broken.
  *Fixed:* `is_cultural_union = no` moved out of the `NOT` as a sibling condition.

- **1518 / 11121 — `NOT = { tag = THIS }` inside an `OR` — [high]**
  Option B ("Willingly or not, they will join") intended to anger FROM's sphere leader, FROM's
  allies and Russia. With `NOT = { tag = THIS }` as a fourth `OR` branch the limit matched
  **every country in the world except the actor**: -100 relations, a forced `leave_alliance`
  and a 60-month `cut_down_to_size` CB from all of them. Absurd magnitude and an instant
  diplomatic death sentence for any AI that picked it.
  *Fixed:* `NOT = { tag = THIS }` moved out of the `OR` to a sibling condition.

- **473 / 482 / 11106 — `OR = { tag = FROM  tag = NGF }` grants cores to both federations — [medium]**
  The two `random_country` blocks were meant to say "if the invitation came from NGF, add my
  cores as NGF cores" (and likewise SGF). Written as an `OR`, a minor invited by **NGF** also
  matched the second block whenever SGF existed, so it donated its cores to SGF as well —
  a duplicated episode that hands the rival federation free claims on land it never asked for.
  *Fixed:* both limits are now `tag = FROM` + `tag = NGF` / `tag = SGF` (AND), i.e. "FROM is
  the federation in question". Formatting normalised at the same time.

- **1597 / 11122 — the flag the option sets was never checked by the trigger — [medium]**
  11122 ("The Slavic Union", AI-only, mtth 12 months) sets `not_join_yugoslavia` and fires
  60130 at YUG, but its own trigger only excluded `does_not_want_to_unify`. A sphered
  south-Slavic minor therefore re-offered itself to YUG every ~12 months until YUG either
  annexed it or picked 60130's option B. `decisions/Balkans.txt:923+` already reads
  `not_join_yugoslavia` as a terminal "this one is settled" flag.
  *Fixed:* `has_country_flag = not_join_yugoslavia` added to the trigger's `NOT` block.

## Flagged, not fixed (ambiguous intent)

- **1500-1511 / 11121 — coercion option grants the CB to the victim — [medium]**
  Option B is "Willingly or not, they will join": it adds FROM's European cores to us
  (correct, `add_core = THIS` inside `FROM`) but then `casus_belli = { target = THIS
  type = humiliate }` *inside the FROM scope*, i.e. the refusing minor gets a humiliate CB
  on us and we get nothing to enforce the annexation with. Changing the keyword to
  `add_casus_belli` would flip it to us-on-them and match the option text, but the current
  wording is also defensible as a backlash, so it is left alone. Compare 98651:1770-1790,
  which correctly uses `add_casus_belli` inside a `tag = FROM` scope to give the actor the
  conquest/make_puppet CB.

- **644-651 / 11107 — both accepted-culture branches are no-ops — [medium]**
  The NGF branch's only effect is commented out (`#owner = { add_accepted_religion =
  south_german }`) and the SGF branch does `add_accepted_culture = german`, which is already
  the primary culture of SGF, NGF and GER alike (`history/countries/*German Fed.txt:2`,
  `GER - Germany.txt:2`), so it does nothing. The wrapping `random_owned` blocks exist only
  to test the owner's tag. Whatever the merged GER should accept (`north_german` /
  `south_german`, given the pop cultures actually on the map) is a balance decision, not a
  mechanical one.

- **168-180 / 11101 — `random_owned` with a limit and an empty body — [low]**
  A six-line owner filter (excludes AUS, KUK, MOL, SYL, LUX, south_asian, scandinavian)
  guarding no effect at all. Harmless, but it is the shape of an effect that was deleted;
  the exclusions look like the leftovers of a per-culture-group `add_accepted_culture` list
  matching the ones 11100 does at 28-52.

- **313-325 / 11103 — invitation limit has no `exists = yes` — [low]**
  Every other invitation loop in the file (11107:740-757, 11110:1036-1046, 11115) filters on
  `exists = yes` or `num_of_cities`. 11103 relies on `num_of_cities = 1` alone, which is
  equivalent in practice but inconsistent.

- **326-342 / 11103 — the Papal option is silently harsher than the text — [low]**
  Choosing to unify strips PAP of *every* province except 749 (Rome — confirmed in
  `map/definition.csv:750`), including any colony, and drops relations by 200 without any
  warning in `EVTOPTA11103`. The parallel Austrian path (11107:660-710) at least routes
  through consent events 31530/31515.

## Observations (outside this file, not touched)

- `common/religion.txt` contains the religion definitions (lines 5-149) **followed by a
  complete copy of the culture-group list** (`germanic` at 150 onward, 270 `first_names`
  blocks). That is why `religion = south_german` parsed at all. It is a pre-existing
  data-file problem, unrelated to tonight's work; flagging it for whoever owns `common/`.
- GER/NGF/SGF all have `primary_culture = german` while the German provinces are populated
  with `north_german`/`south_german` pops, so a formed Germany has no primary-culture pops
  until something adds them. Relevant to the 11107 finding above.

## Zollverein (tonight) and decisions/Germany.txt

No conflict found. `ZollvereinGVG` lives entirely in its own flag namespace
(`zollverein_founded` global, `zollverein_member`/`_offered`/`_refused`/`_founder` country
flags, ids 1000900-1000904) and only shares the read-only `south_german_rel` /
`north_german_rel` tags that NationalUnification also reads. Unification never clears the
`zollverein_member` country modifier, but every path that would need to (11101/11106/11120
acceptance) ends in `inherit`/`annex_to`, so the country ceases to exist; on the
`change_tag = NGF` path at 11110:1023 the modifier is *meant* to carry over.
`decisions/Germany.txt` touches NGF/SGF only through `tag =` potentials and never sets any
of the flags fixed above.

## Verification after the fixes

`modcheck braces/provinces/tags` clean · `refcheck` 14/0/60/0/128/0/8 (unchanged) ·
`audit_events` unknown 0, [high] 0 · `cwtools_check` 14 warnings = baseline
(12x production_types + CBsAndCores:2448 + Indochina:188).
