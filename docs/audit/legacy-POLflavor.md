# `events/POLflavor.txt` — line-by-line logic review

*2026-09-06. Poland / Congress Poland / Kraków flavour: the "Future of Poland" constitutional
chain (99957 → 99956 → 99954/99953/99952/99951 → 99949/99948/99947/99946 → 99950/99955) and the
Kraków integration event 99800. Mechanical audits (modcheck braces/provinces/tags, refcheck,
audit_events, cwtools) were at baseline before and after; everything below is logic.*

The chain has exactly one entry point: `decisions/KRA.txt` `become_poland` (any polish-culture tag
that owns Warsaw/Poznań/Kraków). It is not reachable any other way, and nothing in
`events/RUSFlavor.txt` 95070–95073 (November Uprising) touches these ids or flags — the two files
share no flag (`cpl_uprising` / `cpl_organic_statute` vs `POL_refused` / `krakow_integrated`), so
they cannot double-fire. 95073's `NOT = { exists = CPL }` branch covers a CPL that formed POL.

## Fixed

| line | id | problem | fix |
|---|---|---|---|
| 14, 26 | 99957 | **[high]** `become_poland` fired `country_event = 99957` as the *first* statement of its effect, before `change_tag = POL`; the options then did `POL = { country_event = 99956 }` / `99955`. At that instant POL does not exist (the decision's own `potential` requires `NOT = { exists = POL }`), so both options were silent no-ops and the entire constitutional chain was dead content — the player picked a form of government and nothing happened. | Fire the follow-ups on the root scope (`country_event = 99956` / `99955`), and move `country_event = 99957` in `decisions/KRA.txt:256` to the **last** statement of the `become_poland` effect, after `change_tag = POL`. The root is the same country entity either way, so the four proposal branches (which do `POL = { … }` from SAX/AUS/PRU/RUS) now resolve. |
| 565 | 99800 | **[high]** the trigger accepts `OR = { tag = POL tag = PLC }` but the effect was `POL = { inherit = KRA }`. Fired by PLC (Poland-Lithuania), POL does not exist: Kraków is never annexed, yet the option still sets `krakow_integrated` on PLC, permanently locking the event out. Wrong-recipient scope. | `inherit = KRA` on the root, which is POL or PLC as appropriate. |
| 471, 17-21 | 99950 / 99957 | **[medium]** refusal loop. Every refusal branch routes back to 99950 → 99957 with `days = 1`, and each refuser sets `POL_refused` on *itself*, which the accept options gate to `factor = 0`. So an AI Poland that keeps rolling the 60 % monarchy option re-proposes to countries that can now only refuse, forever (terminating only by chance on the 40 % republic option). | 99950 sets `POL_union_refused` on Poland; 99957's monarchy option gets `modifier = { factor = 0 has_country_flag = POL_union_refused }`, so after any refusal the AI goes republic and the loop closes. Human players are unaffected. |
| 342, 367 | 99951 | **[medium]** implausible magnitude/ai_chance. Accepting "reconciliation" makes Russia cede **every province cored POL or LIT** (99946: all of Congress Poland *and* Lithuania/Belarus) and vassalise Poland, at `factor = 60` vs 40 — Russia gave away its western third more often than not, a decade after the Congress settlement. Compare AUS (70, cedes GLM cores only) and PRU (40, PZN cores only). | `factor = 10` accept / `90` refuse. The cession itself is left alone: it is the flavour payoff of the branch, and it is correctly scoped (`RUS = { any_owned = { … } }`, so the provinces are Russia's, per `docs/audit/owner-scope.md`). |

## Reported, not changed

- **[medium] 137/147 — 99949 inverts the Saxon union.** Every other branch makes Poland the junior
  partner (`AUS = { … create_vassal = POL }`, `PRU = { … }`, `RUS = { … }`), but the Wettin branch
  runs `create_vassal = SAX` **in Poland's scope**, so newly-freed Poland vassalises Saxony after
  Saxony agreed to supply a king. Either reading is defensible for a Wettin personal union, so the
  direction is a design call, not a bug — but it should be made deliberately. If Saxony is meant to
  be senior, mirror 99948: `SAX = { diplomatic_influence = { who = POL value = 500 } create_vassal = POL }`.
- **[low] 99949 is also the only branch with no territorial clause.** Consistent, since Saxony holds
  no Polish cores in 1821; noted only so it does not look like an omission.
- **[low] 122/195/278/364 — `POL_refused` is per-refuser and never cleared.** Once Austria refuses,
  Austria can never accept in a later run of the chain, even decades later. Intentional-looking, and
  harmless now that the loop terminates.
- **[low] 210-245 / 293-328 — vassalisation immediately after `create_alliance`.** 99948 and 99947
  create an alliance in Poland's scope and then vassalise Poland in the partner's scope; the engine
  drops the alliance when the vassal relation is created, so the `create_alliance` line is cosmetic.
  `diplomatic_influence = { value = 500 }` is likewise clamped to the engine cap.
- **[low] 379-410 — 99946 `secede_province = POL` + `add_core = POL`.** Correct order (the core is
  added to the province after it changes hands), and `add_core` on POL cores is a no-op; it exists
  to core the LIT-core provinces. No change needed.
- **[low] whole file — no localisation.** Every title/desc/option here is a hard-coded English
  string rather than `EVTNAME99957`-style keys, unlike the rest of the mod (`RUSFlavor` 95070-95073
  next door uses keys). Not a defect — the engine prints unknown strings verbatim — but the chain
  can never be translated and does not appear in `loc-find`.
- **[low] 417-459 — 99945 is commented out** together with the option in 99951 that reached it
  ("enlarge the Kingdom … but remain under personal union"). The dead code is self-consistent: no
  live option points at 99945, so this is a removed branch, not a dangling reference. Left in place
  as history, like the abandoned events recorded in the Audax baseline.
- **[low] 544-569 — 99800 vs `events/AUSFlavor.txt:2257`.** Both can move Kraków, but the actors
  differ (Poland/PLC as an Austrian vassal here, Austria itself there) and 99800 requires
  `KRA = { sphere_owner = { tag = AUS } }`, which a KRA already annexed by Austria cannot satisfy.
  Not a duplicated episode.
- **[low] 483-540 — 99955 reform packages are all valid** against `common/issues.txt`
  (`landed_estates`, `commoners_properties` are PDM social reforms) and the four national values
  exist in `common/nationalvalues.txt`; `ruling_party_ideology = reactionary/liberal/conservative`
  all match parties defined in `common/countries/Poland.txt`. No dead branch.

## Windows

Nothing in the file is year-gated, so there is no 1836-vs-1821 window problem: the chain is gated on
`become_poland` (needs `romanticism = 1`), and 99800 on being an Austrian vassal while Kraków sits in
Austria's sphere. Both are reachable from the 1821 start once Poland exists.
