# Legacy audit: CrimeAndPunishment.txt and Political Scandals.txt

Line-by-line logic review, 2026-09-06. Both files are universal (no tag gate);
`CrimeAndPunishment.txt` holds ids 22000-22080, `Political Scandals.txt` (GAGA/APD, 2012)
holds 880130-880210. Format: `file line id — problem — fix`. Items marked FIXED were
changed in the same commit as this document.

## Fixed

- `events/CrimeAndPunishment.txt` 517-539 22070 — **[high]** both options were mechanically
  identical *and* net-zero: each applied `capitalists = { militancy = -0.5 }` immediately
  followed by `capitalists = { militancy = 0.5 }` (the second overwrites nothing, the two
  cancel), so "The issue deserves due consideration" and "I am not convinced" did exactly
  the same nothing. — FIXED: A (reform debtor's prisons) now angers capitalists (+0.5 MIL)
  and calms the poor (-0.5 MIL); B mirrors it.
- `events/CrimeAndPunishment.txt` 68-75 22000 — **[medium]** the refusal option gave every pop
  in a random state `consciousness = 2` *and* `militancy = 2`, 2-4x anything else in the file
  (siblings use 0.5-1) for declining a prison-labour scheme. — FIXED: halved to 1 / 1.
- `events/CrimeAndPunishment.txt` 434-447 22050 — **[medium]** `EVTDESC22050` describes a
  *state-wide* manhunt, but both options applied their militancy nation-wide (`rich_strata` /
  `poor_strata` at country scope), and option A used `militancy = 2` against B's 1. — FIXED:
  both options wrapped in `random_state`, A lowered to 1 for symmetry.
- `events/Political Scandals.txt` 1106+ 880200 — **[medium]** "Grave Consequences" is the
  resolution of the scandal chain (it calls `election = yes`), but it never cleared
  `ruling_party_scandal` / `party_scandal_evidence`. Its trigger only requires one of those
  modifiers and `election = no`, and its MTTH is 40 months against a 730/365-day modifier, so
  a second forced early election plus another -10 prestige could land inside the same scandal
  window. — FIXED: the option now removes both modifiers (removing an absent modifier is a
  no-op, so this is safe on either branch of the chain).

## Not fixed (judgement calls / cosmetic)

- `events/Political Scandals.txt` 148, 300, 447, 595, 743, 892, 1041 (880130-880190) —
  **[low]** every scandal ends with `scaled_consciousness = { ideology = X factor = 5 }` on top
  of an `ideology = { value = X factor = -0.1 }` shift, i.e. up to +5 CON on every non-colonial
  pop from one flavour event. Deliberately left: `factor = 5` occurs 18 times elsewhere in
  `events/`, and 4/5/6 are within this mod's range, so this is house style, not a typo. Revisit
  only as a deliberate consciousness-inflation pass.
- `events/Political Scandals.txt` 118, 270, 417, 565, 713, 862, 1011, 1107, 1214 — **[low]**
  option names are raw literals ("Outrageous!", "Things do not bode well.") instead of
  `EVTOPTA<id>` keys. The engine prints the literal, so it works but can never be localised.
  Fixing means nine new loc keys; not done here to keep this commit mechanical.
- `events/Political Scandals.txt` 119-131 (and the six copies) — **[low]** the scandal penalty
  is applied through `random_owned = { limit = { owner = { ruling_party_ideology = X } } owner = { ... } }`.
  That is a country-scope test done from a province scope; it works (`exists = yes` guarantees a
  province) but `if = { limit = { ruling_party_ideology = X } ... }` would be clearer. When the
  scandalised ideology is *not* the ruling party the option has no country effect at all - that
  is intended (opposition scandal), not a dead branch.
- `events/Political Scandals.txt` 1128 880200 — **[low]** `plurality = 1` on a scandal reads
  against the text, but an election campaign raising plurality matches vanilla behaviour.
- `events/CrimeAndPunishment.txt` 348-352, 407-411, 449-453, 494-500 (22040-22070) — **[low]**
  these four lack the `civilized = yes` their siblings carry. Content (chain gangs, debtors'
  prisons, manhunts) is not Europe-specific, so uncivs firing them is arguable, not wrong.
- `events/CrimeAndPunishment.txt` 240-243 22080 — **[low]** repeatable every 120 months with
  `plurality = 1` on *both* options, so it is a slow plurality faucet. Symmetric by design;
  flagged only for the pacing pass.

## Checked and clean

- **Crime names**: neither file touches `has_crime` / `add_crime` at all, so nothing can point
  at a crime missing from `common/crime.txt` (which defines `anarchic_bomb_throwers`,
  `citizen_guard`, `immoral_business`, `machine_politics`, `mafia`, `rotten_boroughs`,
  `spoil_system`, `terrorist_cells`).
- **Modifier names**: `trustee_system`, `penal_colonies`, `ruling_party_scandal`,
  `party_scandal_evidence` and all 24 ruler personalities removed by 880200 exist in
  `common/event_modifiers.txt`.
- **Reform/issue names**: `press_rights`, `political_parties` and `vote_franschise` are all
  spelled as `common/issues.txt` spells them - `vote_franschise` looks like a typo but is the
  mod's (and PDM's) actual issue name, used 1200+ times; do not "correct" it.
- **Effects**: `election = yes`, `ruling_party_ideology`, `upper_house = { ideology value }`,
  pop `ideology = { value factor }`, `dominant_issue`, `scaled_consciousness/militancy` all
  match `docs/wiki/list-of-effects.md`. `random_state = { any_owned = { ... } }` in 22000 is
  odd-looking but is a vanilla pattern (6 uses in the game's own `events/`).
- **Techs**: `social_science` and `state_n_government` (22020, 22080) are real entries in
  `technologies/culture_tech.txt`.
- **NOT-as-NOR**: every multi-statement `NOT` in both files (22000, 22010, 22070, and the
  scandal guards) reads correctly as NOR - each was meant as "none of these are true".
- **Scope**: no province-scope trigger is used at country scope or vice versa; the only
  scope smell was 22050, fixed above. No `ai_chance` blocks exist in either file (all options
  are single or symmetric pairs), so there are no AI extremes to flag.
