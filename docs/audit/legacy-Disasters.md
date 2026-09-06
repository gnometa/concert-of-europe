# Legacy audit — events/Diseases.txt, events/NaturalDisasters.txt

Reviewed 2026-09-06. Both files contain only `country_event`s (mtth-driven); there is no
`province_event` here, so neither file appears in `audit_perf` (top 40 unchanged) and neither
adds a per-province daily evaluation surface. `[fixed]` marks changes applied in this pass.

Format: `file line id — problem — fix`.

## [high]

- `NaturalDisasters.txt:61` 21510 (Krakatoa) — `reduce_pop = 0.1` scales every pop in province
  1414 (Bogor) to **10 % of its size**, i.e. a 90 % death toll in one option, in a file where
  Tunguska uses `0.99` and the San Francisco earthquake `0.90`. `EVTDESC21510` states "over
  36500 dead in the Dutch East Indies", so the effect contradicts its own text by two orders of
  magnitude, and `life_rating = -1` / `dt_rating = -1` alongside it are sized for a small event.
  Almost certainly a dropped digit. — **fix:** `reduce_pop = 0.9`, matching 21520. `[fixed]`

## [medium]

- `Diseases.txt:288-300` 21030 (Strange Influenza) — three mtth modifiers were keyed on the bare
  `poor_strata_life_needs = 0.9 / 0.8 / 0.6`, which is true when needs are **met**, so a well-fed
  nation caught the pandemic up to 2× faster while a starving one was spared. Every other disease
  in the file (21000, 21020, 21040) writes the same ladder as `NOT = { poor_strata_life_needs = X }`,
  and 21030's own `factor = 0.9 NOT = { medicine = 1 }` is negated, so the omission is internal
  inconsistency, not intent. — **fix:** wrapped all three thresholds in `NOT`. `[fixed]`
- `Diseases.txt:136` 21010 / `Diseases.txt:327` 21030 — flat `treasury = -15000` / `-20000` relief
  costs. These are within int32-hundredths range (no wrap), but at the 1821 start a mid-size power
  holds a few thousand pounds, so the "aid them" option is unaffordable for most of the game's
  first decades; only the AI is protected (`ai_chance` drops to 0.1 when `NOT = { money = ... }`),
  the human is silently pushed into debt. — **fix (deferred, balance call):** scale to
  `-2000` / `-3000`, or make the cost proportional. Left as-is; flagged for the balance pass.
- `NaturalDisasters.txt:372` 880290 (Airplane Crash) — `picture = "cholera"` on an aviation
  disaster; the in-file comment says no free picture was available in the PDM era. `scripts/gfxtool.py`
  now exists for exactly this. — **fix (deferred, needs asset sourcing):** fetch a 1908-1913
  aeroplane-crash engraving and repoint the picture.

## [low] — verified or cosmetic, no change made

- `Diseases.txt:88-99` 21010 — the `NOT = { OR OR OR }` government modifier is multi-statement,
  i.e. NOR: "none of hms/democracy/prussian_constitutionalism". That is the intended reading and
  the complementary `factor = 1.2 OR = { ... }` covers the other half. Correct as written.
- `Diseases.txt:277` 21030 `year = 1880` — flagged by `audit_events` as an 1836-start assumption,
  but this is the historical window for the 1889-90 Russian flu. Intentional; do not "fix".
  `Diseases.txt:203-228` 21020's `year = 1850/1870/1890/1910` factors are progressive slowdowns,
  not gates. No other 1836-era window in either file.
- `Diseases.txt:56, 231, 249, 385, 407` — `random_state = { limit = { NOT = { any_owned_province =
  { has_province_modifier = X } } } }`. `any_owned_province` is valid inside a state scope (cf.
  `docs/wiki/national-focus-modding.md:183`), and `random_*` selects only among states matching the
  limit, so the anti-stacking guard works and the option is never a silent no-op.
- Chain-firing: 21000/21020/21040 have no country-level cooldown flag, but the guard above stops a
  state being re-infected while the modifier lasts, and mtth 400 months × best-case 0.65 ≈ 22 years
  makes repeat fires rare. 21030 is one-shot per country (`set_country_flag = pandemic_influenza`,
  never cleared, and re-checked in the trigger). All four 880xxx events share
  `NOT = { has_country_modifier = national_tragedy }` plus a 730-day modifier: a proper cooldown.
- `Diseases.txt:150` 21010 option B — `reduce_pop = 0.8` on `poor_strata` of a whole state
  (−20 %) is harsh but above the −30 % "drastic" line, and the text ("Sorry, I gave at the office")
  supports it being worse than option A's `0.9`. Kept.
- Overlap with `LiberalRevolutions.txt:10230` (cholera) and `JAPTenpoGVG` (Tenpo famine, 1833-37):
  no shared ids, flags or modifiers. Cholera uses its own `cholera_epidemic_small/big` province
  modifiers and its own `poor_strata_everyday_needs = 0.15` gate; the Tenpo famine is country-flag
  gated to TKG/JAP. The generic famine 21010 can co-fire with the Tenpo chain in Japan — thematic
  double-dipping only, no mechanical conflict. Not worth a guard.
- `NaturalDisasters.txt:12, 46, 80` — `fire_only_once = yes` is engine-wide, but each of these
  triggers on `owns = <single province>`, which at most one country satisfies at a time, so
  global-once and per-country-once coincide. No flag guard needed.
- `NaturalDisasters.txt:29` 21500 — permanent `life_rating = -10` on province 2694 (Erbogacen) for
  an airburst over empty taiga is heavy-handed next to Krakatoa's `-1`, but harmless.
- `NaturalDisasters.txt:174, 285, 405, 505` — option names are hardcoded English strings
  ("Horrible!", "Tell the truth.", "Blame the enemy.", "We will consider it.", "Oh the humanity!")
  rather than `EVTOPTA<id>` keys. The engine renders raw text, so this only blocks translation.
- `ai_chance`: only 21010 and 21030 set one (50/50 with a 0.1 penalty when broke). No extremes
  (`factor = 0` or `factor = 100`) anywhere in either file. 21020/21040's unweighted two-option
  choices leave the AI at an even split, which is acceptable for symmetric options.
- Province ids 84 (San Francisco), 1414 (Bogor) and 2694 (Erbogacen) all exist in
  `map/definition.csv` and match their events geographically. All referenced modifiers
  (`tuberculosis`, `typhoid`, `smallpox`, `pandemic_influenza`, `national_tragedy`) are defined in
  `common/event_modifiers.txt`; all pictures resolve (`gfxtool.py missing` is clean).
