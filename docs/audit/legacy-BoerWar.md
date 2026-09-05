# Legacy review: `events/BoerWar.txt`, `events/NdebeleGazaWar.txt`, `decisions/BoerWar.txt`

*2026-09-06. Line-by-line logic pass over the Southern-Africa chain (Great Trek -> Natal ->
Oranje/Transvaal -> Boer wars -> Zulu/Xhosa), plus tonight's 98241 appeal and the Mfecane events.
Mechanical audits (`refcheck`, `audit_events`, `modcheck`, cwtools) were already clean here; this
is a semantic pass. `98230`, `99665`, `99666` are abandoned on purpose and were left alone.*

Fixed items are marked **[fixed]**; everything else is reported only.

## [high]

- `events/BoerWar.txt:220` event 98207 — option A *"They are colonial subjects, no more."* used
  `release = NAL`, which frees Natal outright. Every follow-up (98210 British Rule of Natal, and
  through it 98211/98212/98213) requires `NAL = { vassal_of = THIS }`, so the whole Natal arc died
  on the branch whose own text says Natal stays a subject. The parallel option in 98206 already
  used `release_vassal`. — **[fixed]** `release = NAL` -> `release_vassal = NAL`.
- `events/BoerWar.txt:561` event 98220 — `mean_time_to_happen` had a `modifier = { ORA = { exists =
  yes } }` with **no `factor`**; a factorless MTTH modifier is not a valid block. — **[fixed]**
  added `factor = 0.5` (Transvaal follows sooner once Oranje exists, which is the obvious intent).
- `decisions/BoerWar.txt:299` `claim_xhosa_lands` — the potential allows `ENG` **or** `ENL`, but the
  effect hard-wires `ENG = { war = { target = XHO ... } }`. Taken as ENL, the decision made *Britain*
  declare the Xhosa war while ENL paid the badboy and took the cores. — **[fixed]** unwrapped the
  `ENG = { ... }` scope so the war is declared by the decision-taker.
- `decisions/BoerWar.txt:9` `boer_republic` — gated on `has_global_flag = boer_convention_denied`,
  which is set *only* by event 98230, an abandoned (`is_triggered_only`, never fired) event. The
  decision was therefore unreachable, and with it `form_south_africa` (needs `republic_founded`),
  i.e. **SAF could never be formed in a 1821 game**. — **[fixed]** the gate is now
  `OR = { boer_convention_denied  transvaal_sovereignty }`; the latter is set by 98220, so the
  chain is live again without touching the abandoned 98230.

## [medium]

- `events/BoerWar.txt:504` (98215) and `600` (98220) — `relation = { who = ORA/TRN ... }` and
  `ORA/TRN = { prestige = -30 }` ran **before** `release = ORA/TRN`, and both triggers require the
  tag *not* to exist. All four lines were silent no-ops. — **[fixed]** `release` moved ahead of them.
- `events/BoerWar.txt:994` event 98245 — sets `set_global_flag = first_boer_war` and is titled
  "Annexation of the Transvaal", but the window is `year = 1897` with an x0.25 modifier at 1900.
  The historical annexation is 1877 and the First Boer War 1880-81; 1897+ is the *Second* war, and
  there is no separate 1880 episode in the chain. Either move the gate to ~1877 (and let the 1900
  modifier cover the second war) or rename the flag/loc. Left alone: it is a pacing decision, and
  moving the date changes when Britain fights the Boers by twenty years.
- `events/BoerWar.txt:1143` event 98247 — option A ("reconcile") costs `prestige = -50` while
  option B ("Never! There will be a reckoning") costs only `-25` *and* keeps the SAF cores *and*
  ends the same wars. B strictly dominates A, and neither option has an `ai_chance`, so the AI
  picks 50/50 on losing South Africa. Suggest -25/-40 and an explicit `ai_chance`.
- `decisions/BoerWar.txt:390-420` `roo_expedition` / `bushmen_expedition` — the potential only
  requires *one* of 2092/2093/2558 (resp. 2088) to be `empty = yes`, but the effect runs
  `secede_province = THIS` on all of them unconditionally. If another power has colonised one of
  those provinces in the meantime the decision annexes it with no war and no infamy. There is no
  clean conditional province effect for this, so it needs a redesign (province event, or per-province
  decisions); reported only.
- `events/NdebeleGazaWar.txt:130-165` event 95519 — the only option is *"End this travesty by
  negotiation"*, yet every `random_list` branch runs a country-wide `any_pop` with
  `reduce_pop = 0.3/0.35/0.4`, i.e. it kills 60-70% of every non-Nguni pop MAT owns (and 10-20% of
  the Nguni). Nothing limits it to the six provinces the option otherwise touches. Implausible
  magnitude for the negotiated outcome; suggest scoping the `any_pop` to those provinces and
  softening to ~0.8.
- `events/BoerWar.txt:642` / `677` events 98225 and 98226 are a duplicated episode: identical
  triggers, identical `desc = "EVTDESC98225"`, identical `set_province_flag = great_trek2`, and only
  the `move_pop` destination differs (2105 vs 2101). Because they share one flag, only one can ever
  fire per province, so the destination is decided by an MTTH coin-flip. If that is the intent it
  should be one event with a `random_list`; 98226 also has no loc key of its own.

## [low]

- `events/BoerWar.txt:1083` — `set_global_flag = no_boer_war` is never read anywhere in the mod.
- `events/BoerWar.txt:406` event 98212 option B — the leftover `civilized = yes` runs on NAL *after*
  `FROM = { inherit = THIS }`, so it applies to a country that no longer exists; the neighbouring
  `# DUPLICATED -Koro civilized = no` comment is from the same edit.
- `events/BoerWar.txt:942` event 98241 (new) — correct scoping: root is ENG, `FROM` the appellant,
  and `casus_belli = { target = FROM ... }` grants ENG the claim, matching `EVTDESC98241`. Two nits:
  option A's text promises protection but the only mechanical help is `+200` influence and `-2`
  militancy (no alliance, no sphere entry, no war join); and its `ai_chance` modifier
  `FROM = { war_with = ENG }` can never be true, since `appeal_to_the_british` already excludes
  `war_with = ENG` in its potential.
- `events/NdebeleGazaWar.txt:110` event 95518 — `MAT = { capital = 2071 }` is a no-op: Bulawayo is
  already MAT's capital in `history/countries/MAT - Matabele.txt`. The event is fired only from
  98220, so it is not orphaned.
- `events/BoerWar.txt:879` event 98235 — verified, not a bug: `add_casus_belli` gives the *target*
  the CB against the scoped country, so `random_country = { ... add_casus_belli = { target = THIS } }`
  correctly hands the greater power the `add_to_sphere` CB.
- `decisions/BoerWar.txt:400/408/416` and `events/BoerWar.txt:1543` — `change_variable = { which =
  dt_rating }` is used inside a *province* scope; variables are country-scope. Same pattern appears
  in `decisions/AUS.txt`, `CSA.txt`, `France.txt`, `HUN.txt`, so it is a mod-wide convention and is
  left for a separate pass.
- `events/BoerWar.txt:1209/1242` — `has_pop_religion = anglo_african` is *correct*: `anglo_african`
  is a sub-culture living in the pop religion field (18 pops in `history/pops/1821.9.1/Southern
  Africa.txt`). Do not convert it to a culture trigger.

## Verification

`modcheck braces/provinces/tags` clean on all three files; `refcheck` 14/0/60/0/128/0/8 (unchanged
baseline); `audit_events` unknown 0, [high] 0; `cwtools_check` 0 errors, 14 known warnings, none in
these files.
