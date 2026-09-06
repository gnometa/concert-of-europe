# Legacy audit: `events/ACW.txt` (American Civil War chain, 16000+)

*2026-09-06. Line-by-line logic review of `CoE_RoI_R/events/ACW.txt` (3151 lines, ids
16000-16450 plus 8016451). Mechanical audits (`modcheck braces/provinces/tags`, `refcheck`,
`audit_events`, `cwtools_check`) were at baseline before and after; this pass looked only at
logic: recipients/scopes, effects vs. text, ai_chance, dead branches, year windows, magnitudes.*

## Which chain is live

All three American files are live and do **not** duplicate each other - they are three eras of
one timeline, kept apart by `american_civil_war_has_happened`:

| File | Ids | Gate | Role |
|---|---|---|---|
| `events/ACW.txt` | 16000-16450 | slavery-debate build-up, no ACW yet | **the** secession war (USA vs CSA) |
| `events/Alternative ACW.txt` | 16500-16515 | `year = 1865`, `NOT = { has_global_flag = american_civil_war_has_happened }` | peaceful fallback: Second Constitutional Convention -> FSA, only if 16000 never fired |
| `events/ACW2_Events.txt` | 95260-95316 | `has_global_flag = american_civil_war_has_happened` + USA not a democracy | a *later*, second civil war |

So the chain cannot stall forever: if the 16000 preconditions never assemble, the 1865 alt path
picks it up. `decisions/ACW.txt` is the flag source for the whole build-up (gag rule, Clay and
Douglas draft, Kansas-Nebraska, fugitive slave act, Custer, Anaconda, emancipation,
reconstruction); every flag ACW.txt reads is set there or in this file. No orphan flags.

## Findings

### Fixed in this pass

`line id - problem - fix`

- **33 16000 [high]** - the second trigger branch was `AND = { slavery = no_slavery
  NOT = { has_global_flag = american_civil_war_has_happened } }` with **no year gate and no
  build-up requirement**: any USA that passed the slavery reform early (perfectly possible from
  the 1821 start) got a full Confederate secession in the 1820s-30s, with none of the
  `the_slavery_debate` / John Brown / Dred Scott chain having run. The other branch is already
  pinned to 1850+ by `john_browns_raid` (16010, `year = 1850`) and `dred_scott_decision` (16020,
  `year = 1850`). Fixed: added `year = 1855` to the `no_slavery` branch, so both routes resolve
  in the intended 1855-1870 window and the 1830s are closed.
- **2367 16350 [high]** - Trent Affair. Britain's de-escalation option ("We will not risk a
  diplomatic incident") carried `ai_chance = { factor = 0 }` against `factor = 100` on the
  ultimatum, so **AI Britain always escalated**; with 16351's 40/60 split that put an
  ENG-vs-USA great war in ~40% of all games in which a CSA existed. Fixed: de-escalation
  `factor = 50` (2:1 in favour of the ultimatum, still the likely path).
- **2409 16351 [medium]** - the matching USA side, "All is fair in war!", was `factor = 40`.
  Combined with the above the AI now goes to war in ~13% of Trent affairs, the right order of
  magnitude for what was historically a climbdown. Fixed: `factor = 20`.
- **2046 16210 [medium]** - the Wakarusa War's only option was named `"EVTOPTA14210"`, a stray
  key from the 14xxx range that localises to *"Peace always prevails!"* while the effect kills
  5% of every militant pop in the province. `EVTOPTA16210` ("A black day for $STATENAME$")
  exists and is what the event means. Fixed (inherited from vanilla, wrong there too).
- **1373 16130 [medium]** - Fugitive Slave. The mod added
  `NOT = { ... has_country_flag = fugitive_slave_act_enacted }` to the trigger but kept vanilla's
  `modifier = { factor = 0.5 has_country_flag = fugitive_slave_act_enacted }` in the MTTH: the
  modifier can never apply, because the flag it wants is exactly the flag that blocks the event.
  Fixed: dead modifier removed.
- **3031 16440 [medium]** - Apache Wars applied `reduce_pop = 0.5` to every non-native pop in the
  state around province 105, i.e. **half the settler population of a whole state** for a flavour
  raid; every other `reduce_pop` in this file is 0.95 (a 5% loss). The mod also widened the
  recipient from vanilla's `tag = USA` to USA/CSA/FSA, so it can now hit three countries.
  Fixed: `reduce_pop = 0.95`.

### Not fixed - documented

- **64 16000 [medium]** - option A hands CSA cores to Kentucky (`USA_185`), Maryland (`USA_219`)
  and West Virginia (`USA_218`), then immediately secedes the Maryland and West Virginia regions
  back to USA. Those provinces stay CSA-cored forever, so the Union keeps a permanent claim
  target on Baltimore and Wheeling and CSA rebels can spawn there. Historically both stayed in
  the Union. Deliberate-looking (it is the vanilla border-state fudge), so left alone; if it is
  ever revisited, drop `USA_218`/`USA_219` from the core list rather than seceding them back.
- **118 16000 [low]** - option B secedes provinces 146-150 (region `USA_148`) back to USA after
  `release_vassal = CSA`. `USA_148` is never given a CSA core, so CSA never owns those provinces
  and the block is inert. Option A does the same job with the two regions only; the two options
  should use one shared list.
- **102/150 16000 [low]** - `capital = 220` is safe (220 sits in `USA_219`, which both options
  return to USA) but only because of the secede block a few lines earlier; it breaks silently if
  the core and secede lists are ever edited apart.
- **204 16002 [low]** - "Gag Rule under scrutiny" sets no flag on its second option ("No
  abolitionist nonsense for us!"), so the event re-fires on its 50-month MTTH until the player
  finally repeals. Harmless nagging, but asymmetric: option A ends the event, option B does not.
- **157 16001 [low]** - `NOT = { has_global_flag = american_civil_war_has_happened
  has_country_flag = house_gag_rule_enacted }` is a NOR, and the second clause is unreachable:
  the gag rule decision requires `has_country_modifier = the_slavery_debate`, which only 16001
  itself grants. Redundant, not harmful.
- **1821/1902 16180/16190, 3040 16445 [low]** - bare `has_country_flag` inside a province-scope
  trigger. Vanilla ships exactly this in 16445, so the engine resolves it against the owner; the
  mod-added `kansas_nebraska_act_acting` checks in 16180/16190 follow the same pattern and were
  left as-is rather than wrapped in `owner = { }`.
- **517 16030, 836 16070 [low]** - "A Southern Belle" and "Fire-Eaters" have no
  `fire_only_once`, no year gate and a 24-30 month MTTH, so they churn from 1821 onwards, three
  decades before the debate they are flavouring exists. Every other flavour event in the block
  is gated on `has_country_modifier = the_slavery_debate`; these two only need
  `slavery = yes_slavery`.
- **2196 16250 [low]** - Secessionist Sentiments has a 3-month MTTH and hands CSA cores to any
  slave state as soon as `romanticism` and `ideological_thought` are researched, which an 1821
  USA can reach well before 1850. It only paints cores (no war), and 16000 is now year-gated, so
  it is a slow map warning rather than an early war.
- **2544 16400 [low]** - statehood: `inherit = FROM` after
  `FROM = { all_core = { add_core = USA } }` hardcodes USA, and the event is also sent from
  `decisions/CAN.txt:205`. Correct today because both senders target USA, but the event is not
  tag-agnostic despite its generic name.
- **2961 16430, 3109 8016451 [low]** - `reduce_pop = 0.5` on the Dakota at the end of the Sioux
  Wars is vanilla and thematically intended; the Texas goods grant (money 1000, several industry
  levels, no MTTH so it fires at once) is by design.

## Verification

`modcheck braces/provinces/tags` clean on the file; `refcheck` 14/0/60/0/127/0/8 (unchanged);
`audit_events` unknown keywords 0, [high] 0, [medium] 0; `cwtools_check` at the known baseline
(12 `production_types` CW242 + `CBsAndCores.txt:2467` + `Indochina.txt:188`).
