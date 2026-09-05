# The Zollverein, 1834 (GVG)

Fills the largest 1821-1836 hole (see `1821-1836-coverage.md`, item 1). Prussia's 1818
tariff law grew into the German Customs Union on 1 January 1834, binding the middle
states to Berlin a generation before political unification. Austria stayed out.

Files: `decisions/ZollvereinGVG.txt`, `events/ZollvereinGVG.txt` (ids 1000900-1000904),
two modifiers in `common/event_modifiers.txt`, loc in `localisation/GVG_events.csv`.

## Who counts as an eligible German minor

Reused in three places (offer, Austrian counter, completion check):

    exists = yes, civilized = yes, is_vassal = no, is_greater_power = no
    OR = { has_country_flag = north_german_rel has_country_flag = south_german_rel }
    NOT = { tag = THIS tag = AUS tag = KUK tag = DNB tag = SWI tag = LUX tag = NET }

The two `*_german_rel` flags are set in `history/countries/*` for every German tag, so
they are the mod's existing "is a German state" marker. Switzerland, Luxemburg and the
Danubian/Austrian tags carry the flag but are not Zollverein material, so they are
excluded by tag. Countries already `in_sphere = AUS` are skipped by the offer only.

## Decision `found_the_zollverein` (decisions/ZollvereinGVG.txt)

- potential: `civilized`, `north_german_rel`, not AUS/KUK/DNB, `NOT = { has_global_flag = zollverein_founded }`, `year = 1833`,
  and `tag = PRU` or (greater power owning a Prussian core - covers PRU being eaten/renamed).
- allow: `war = no`, `prestige = 50`, `state_n_government = 1`, and at least one eligible minor (`year = 1833` sits in
  the potential, so the decision is simply not offered before then).
- effect: prestige +10, `zollverein_leader` (permanent), `set_global_flag = zollverein_founded`,
  `set_country_flag = zollverein_founder` (a flag, not the modifier, because flags survive `change_tag`
  when Prussia later becomes NGF/GER),
  then `any_country = { limit = { <eligible> NOT = { in_sphere = AUS } } set_country_flag = zollverein_offered
  country_event = 1000900 }`.
- ai_will_do: factor 1, `modifier = { factor = 0 war = yes }`.

## Event 1000900 - "Accession to the Zollverein" (the minor, `is_triggered_only`)

`FROM` is the founder. Two options:

- **Join**: `set_country_flag = zollverein_member`, `zollverein_member` modifier (permanent),
  `relation = { who = FROM value = 50 }`, `FROM = { diplomatic_influence = { who = THIS value = 100 } }`
  (there is no `add_to_sphere` effect in Vic2 - only a CB of that name - so influence is the
  correct lever, per `list-of-effects.md`), relation with AUS -25, `FROM = { country_event = 1000901 }`.
  ai_chance weighted up by `in_sphere = FROM`, good relations with FROM, `NOT = { in_sphere = AUS }`.
- **Refuse**: `set_country_flag = zollverein_refused`, relation with FROM -25, AUS +25 and
  `AUS = { diplomatic_influence = { who = THIS value = 50 } }`, small prestige.
  ai_chance weighted up by `in_sphere = AUS`.

1000901/1000902 are the founder-side acceptance/refusal notes (`FROM` = the minor). 1000903 is
Vienna's reaction, fired at the founder's decision with a ten-day delay so that offers a human
player has to answer are settled first.

## Event 1000904 - "The Customs Union Complete" (founder)

Not `is_triggered_only`; trigger = `has_country_flag = zollverein_founder`,
`has_global_flag = zollverein_founded`, `NOT = { has_global_flag = zollverein_complete }`,
at least one member exists, and no country still carries `zollverein_offered` without
`zollverein_member`/`zollverein_refused`/`southern_union_member`. `zollverein_offered` is
what makes the tally possible without a counter: only countries that got the offer are
polled, so a minor Austria spheres afterwards cannot deadlock it. Reward scales with the
member count naturally (`any_country = { limit = { has_country_flag = zollverein_member } relation ... }`).

## Decision `form_the_southern_customs_union` (AUS counter, cheap)

Potential AUS/KUK, `has_global_flag = zollverein_founded`, not already done. Effect:
prestige, the existing `customs_union` modifier, `set_global_flag = southern_customs_union`,
and directly (no event) `set_country_flag = southern_union_member` + `customs_union` +
relation/influence for every eligible south-German minor that refused Prussia.

## Modifiers (2 new, deliberately modest)

    zollverein_member  = { tax_efficiency 0.05, factory_input -0.05, RGO_throughput 0.05 }
    zollverein_leader  = { prestige 0.05, influence_modifier 0.15, tax_efficiency 0.05 }

`customs_union` already exists (RGO_throughput 0.05) and is reused for the Austrian union.

## Deliberately out of scope

No change to the NGF/German unification decisions in `decisions/Germany.txt` or
`decisions/NationalUnification.txt`; the Zollverein flags are additive and read-only there.
Pictures are existing assets only (`SCA_customs_union`, `conference1`, `national_congress`,
`factory`, `treaty`).
