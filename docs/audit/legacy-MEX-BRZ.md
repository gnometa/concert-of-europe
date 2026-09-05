# Legacy audit: MEXFlavor.txt / BRZFlavor.txt

*2026-09-06. Line-by-line logic review of `CoE_RoI_R/events/MEXFlavor.txt` (2830 lines, ids
44800-44865 + 996542) and `CoE_RoI_R/events/BRZFlavor.txt` (813 lines, ids 46300-46332), read
against the 1821.9.1 start. Format: `file line id - problem - fix`. Fixed entries are marked
**[fixed]**.*

## Chain map (verified, no defect)

- **Iturbide's empire is modelled.** `UCA - United States of Central America.txt:74` sets
  `join_mexico` only inside the `1836.1.1` block, so at the 1821 start the flag is clear;
  `USCAFlavor 97580` (year 1822) sets it, optionally firing `97581` whose `inherit = FROM`
  removes UCA. MEX `44850` (First Mexican Empire, needs `prussian_constitutionalism`, which
  `MEX - Mexico.txt:4` gives) then `44852` (Plan of Casa Mata -> republic) and `44853`
  (Cuernavaca -> Santa Anna's dictatorship, 1830+) reproduce 1822-1823 and 1834 correctly.
  `44851` (Central America secedes) is only reachable after `97581`, which is consistent.
- Recipient/FROM hops all check out: TEX `44840` -> MEX `44841` -> TEX `44842/3/4` -> USA
  `44846` (FROM = TEX); MEX `44825` -> USA `44826/44827` (FROM = MEX); MEX `44861` -> USA
  `44862` -> MEX `44863/44864`; PRG `46304` uses `random_country = { limit = { tag = BRZ ... }
  THIS = { war = ... } }`, i.e. the war is declared by PRG (THIS = event root), which is right.
- `has_pop_religion = dixie` (`44815`, `44855`, `996542`) is **live**: sub-cultures sit in the pop
  religion field (`history/pops/1821.9.1/United States.txt` has 235 `religion = dixie` rows).
  Do not "fix" these.
- BRZ `46316` guard is sound: both options of `BRZRegencyGVG 1001903` set `brazil_majority`, and
  option A also clears `pedro_events_begun`, so the Pedro chain cannot double-fire.

## [high]

- `MEXFlavor.txt:1933` 44854 (Cherokee in Tejas) - the "We refuse." option sets
  `cherokee_question_settled`, a flag that is **set and read nowhere else**, while the trigger
  gates on `cherokee_question_answered` (set only by the accept option). The event has no
  `fire_only_once`, so refusing re-fires it every ~3 months from 1823 to the end of the game:
  an endless popup that also stacks `consciousness = 2` on every Cherokee/native pop in 132.
  **[fixed]** - the refuse option now sets `cherokee_question_answered`.

## [medium]

- `BRZFlavor.txt:583` 46325 (War of the Farrapos) - `release = RGS` creates RGS as **BRZ's
  vassal**, and the very next effect declares `war = { target = RGS ... }`; an overlord cannot
  war its own vassal, so the war (the point of the only option, "Those fools!") is silently
  dropped and the Farroupilha ends as a peaceful vassalisation. **[fixed]** - replaced with
  `any_owned = { limit = { is_core = RGS } secede_province = RGS }`, the pattern already used by
  `44820` (Rio Grande) and `44856` (Texas); the RGS cores added just above (`BRZ_2467`, and
  `URU_2344` when Cisplatina is held) select exactly the same provinces `release` would have.
- `BRZFlavor.txt:160` 46303 (War of the Farrapos, duplicate title) - requires
  `has_country_flag = farrapos_war` **and** `owns = 2463` (Porto Alegre), but the only setter of
  that flag is 46325, which hands 2463 to RGS in the same effect. The event is therefore dead
  unless BRZ reconquers Porto Alegre before 1845 and is still in a monarchy government. It is
  also a duplicate episode of 46325 (same title, same subject). Fix: either drop it or gate it on
  `RGS = { exists = yes }` / re-owning 2463 after the war, and give it its own title key.
  Not changed - which of the two is meant to be the survivor is a design call.
- `BRZFlavor.txt:707,742,795` 46331/46332 - `any_pop = { limit = { has_pop_religion = catholic }
  ... }` is a **dead limit**: pops in this mod carry a sub-culture in the religion field
  (`CE_pops.txt:5741` is `religion = brazilian #religion = catholic`), so no pop is `catholic`
  and the militancy/consciousness effects of the Religious Question never touch anybody. Both
  options of 46331 and option B of 46332 are cosmetic. Reported only - per project rule,
  religion-form triggers are not to be rewritten into culture forms.
- `MEXFlavor.txt:429` 44810 - each provincial rebellion shifts the whole upper house by
  `ideology = reactionary value = 0.4` and moves 20% of the rich strata reactionary. The event is
  per-province and only self-blocked for 1095 days by `peasant_revolt`, so a Santa Anna Mexico
  compounds this to a 100% reactionary upper house within a few years. Vanilla uses ~0.1.
  Not changed - magnitude is a balance call.
- `MEXFlavor.txt:1335` 44850 - the Empire depends on MEX still being in
  `prussian_constitutionalism` when the 3-month MTTH elapses. Any earlier government change locks
  out `first_empire` permanently, and with it 44851 (Central America), 44852, 44853 -> 44805 and
  44861 (Cuba). Consider an `OR` fallback on `year = 1823`.

## [low]

- `USCAFlavor.txt:1488` 97580 - **both** options set `join_mexico`, including "We will make our
  own way", so MEX reads a refusal as an invitation and still proclaims the Empire in 44850.
  The flag is doing double duty as "question resolved".
- `MEXFlavor.txt:1044` 44840 - "Santa Anna Captured!" gets *more* likely the more of Texas is
  occupied (`national_provinces_occupied` modifiers on TEX). Defensible as San Jacinto following
  the Mexican advance, but it reads backwards.
- `MEXFlavor.txt:1233,1265` 44842/44843 - `relation = { who = MEX value = 400 }` (capped at 200)
  after a war of independence, and +200 for a mere ceasefire: Texas ends at maximum friendship
  with the country it just beat. Left alone: `value = 400` appears 28 times mod-wide, so this is
  a house idiom rather than a local slip.
- `MEXFlavor.txt:782,806` 44825/44826 - `treasury = 100000 / -100000` for the Mexican Cession is
  a large sum, but `-100000` occurs 11 times elsewhere in `events/` (and `-200000` four times),
  so it is within the mod's own scale. Not changed.
- `MEXFlavor.txt:1613` 44852 option B ("Defend the Empire!") pushes officers and soldiers
  *liberal*. This mirrors option A, where proclaiming the republic pushes them reactionary, i.e.
  the losing camp radicalises - intended symmetry, not a contradiction.
- `MEXFlavor.txt:2416` 44860 / `BRZFlavor.txt:340` 46305 - both are ungated repeating land-grab
  ladders (`treasury = -2000` / `-8000` per fire, one province each). The `empty = no` cascade
  makes exactly one branch true per fire, so they are self-limiting; only the unbounded repetition
  and the treasury drain on a broke AI are notable.
- `MEXFlavor.txt:2260` 996542 - an unregistered id (`events/GVG Event IDs.txt` does not cover
  99xxxx) reusing `EVTNAME44855`/`EVTDESC44855`; it is a deliberate second Empresario wave, but it
  should get its own id range entry and loc keys.
- **Coverage gap**: neither the **Pastry War** (1838-39, FRA vs MEX) nor the **Reform War**
  (1858-61) exists anywhere in `events/` or `decisions/` - `grep` for "pastry"/"reform war"
  returns nothing. The 1821 Mexican arc jumps from Cuernavaca (1834) to Guadalupe Hidalgo (1848)
  to Maximilian (44830) with nothing in between.

## Verification after the two fixes

`modcheck braces/provinces/tags` clean on both files; `refcheck` 14/0/60/0/128/0/8 (baseline);
`audit_events` unknown 0, [high] 0, [medium] 0.
