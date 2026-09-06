# Logic audit: GREFlavor / GREKingdomGVG / KORFlavor / ARAFlavor / CSAFlavor / SWHFlavor

*2026-09-06. Line-by-line read of the London Conference chain (31200-31213, 31230, 31240), the
Greek Kingdom chain (1000500-1000502), the Korea chains (85000-85030), the Arab/Mahdist chains
(96100-97171), CSA 16600-16656 and SWH 90050-90059. Format: `file line id - problem - fix`.
The [high] items and the unambiguous [medium]s were fixed in this commit.*

## Greece

- **[high] `events/GREFlavor.txt` 712-950, 31208/31209/31210/31211/31212/31213 - the whole
  "who supported which outcome" payout is dead.** 31201 sets `conference_weak_greece` /
  `conference_medium_greece` / `conference_strong_greece`; the payout blocks and the two
  `ai_chance` modifiers test `has_country_flag = weak_greece` etc., which are *variable* names, not
  flags, and are never set. Every attendee got the flat +2 prestige and nothing else.
  **Fixed:** all `has_/clr_country_flag` references renamed to the `conference_*` flags.
- **[high] `events/GREFlavor.txt` 502-509, 31206 - the medium-Greece settlement transfers no
  Ottoman land.** The `any_owned` limit inside `TUR = { }` lists `region = GRE_837`,
  `region = GRE_826` and `province_id = 845` as three ANDed statements; no province can satisfy all
  three, so the block never matched and Greece became independent with only 847/848 added.
  **Fixed:** wrapped the three in `OR = { }`, matching 31205/31207.
- **[high] `events/GREFlavor.txt` 906-911 and 943-948, 31212/31213 option B - clears the wrong
  conference's flags.** "We are secretly pleased" clears `hosting_london_conference_1830`,
  `attending_london_conference_1830`, `supporting_netherlands/belgium/partition` (copy-paste from
  the Belgian conference). The 1832 flags survive, so the country stays permanently
  "attending"/"hosting" and keeps matching later
  `has_country_flag = attending_london_conference_1832` scans. **Fixed:** replaced with the same
  six clears option A uses.
- [medium] `events/GREFlavor.txt` 641-682, 31207 option B - "They have no right! Greece is ours!"
  still secedes GRE_837/GRE_826/TUR_832/825/843/847/848 to Greece, `release_vassal = GRE`, gives
  GRE +5 prestige and moves its capital to Athens. Refusing differs from accepting only by keeping
  province 845 and by +2/-5 prestige and badboy 6. Not fixed - which effects the refusal should
  keep is a design call; either drop the secede/release block or turn it into a war branch.
- [medium] `events/GREFlavor.txt` 236-246 / 294-304 / 352-362, 31202/31203/31204 - the vote
  thresholds are asymmetric: weak and strong need `check_variable value = 2`, medium needs 1, and
  medium also carries the highest option weight in 31201 (50 vs 30/20). A single supporter carries
  the medium outcome. Not fixed (balance, not a defect).
- [low] 31212 852-854 - `relation = { who = GRE value = -150 }` and
  `diplomatic_influence = { who = GRE value = -150 }` where the identical 31211 branch uses -50;
  influence is a 0-100 pool, so -150 is just "zero, twice".
- [low] 31205 - refusing (option B) nets Greece +3 prestige against -1 for obeying; only badboy 6
  separates them.
- [low] 31240 - `prestige = -50` / `badboy = -15` sits at the edge of the plausible band, and with
  mtth 12 months x0.1 for a non-secondary power a minor BYZ reverts to GRE within a month or two.
  `fire_only_once` is safe here because only BYZ can trigger it.
- [low] 31230 option A - `relation = { who = GRE value = 200 }` pins relations at the cap in one
  event.
- [low] `events/GREKingdomGVG.txt` 163, 1000502 - `remove_country_modifier = bavarian_regency` can
  never do anything: the modifier is added in 1832 with `duration = 3650` (expires 1842) and the
  trigger requires `year = 1843`.
- [low] `events/GREKingdomGVG.txt` 59-72 / 96, 1000500 option B / 1000501 - "Greece must be a
  republic" sets `greek_crown_offered`, which is exactly the gate for Otto's arrival, so the
  republican branch gets a Bavarian king anyway (historical, but the option text does not say so).

## Korea

- **[high] `events/KORFlavor.txt` 28/32/46, 85000 - the French punitive chain is dead.** The
  trigger requires `KOR = { vassal_of = CHI }`, but at the 1821 start Korea is a vassal of **QNG**
  (`history/diplomacy/PuppetStates.txt`, QNG->KOR 1636-1876); CHI is the post-revolution republic
  tag (`history/countries/CHI - China.txt`, presidential_dictatorship) and does not exist in 1866.
  The event never fired, so 85001-85005 were unreachable. **Fixed:** the trigger now accepts
  `vassal_of = QNG` or `vassal_of = CHI`, the truce guard covers both tags, and the option fires
  85001 at the actual overlord through `random_country = { limit = { is_our_vassal = KOR } }` - the
  pattern 85011 already uses, which keeps `FROM` = France for 85001-85005.
- **[high] `events/KORFlavor.txt` 1166-1175, 85030 option A - two casus belli target their own
  owner.** Inside `FROM = { ... }` (China), `casus_belli = { target = FROM ... }` still resolves
  `FROM` to China, so China received `take_from_sphere` and `humiliate` CBs against itself while
  Japan got nothing. **Fixed:** both changed to `target = THIS` (Japan, the event root), matching
  the `release_puppet` CB two lines above.
- [medium] `events/KORFlavor.txt` 318-334, 85010 option B - "This is not in our interest" costs
  -20 prestige, breaks the alliance with Korea, drops relations with Korea by 100 and hands Japan a
  `release_puppet` CB on Korea's overlord. Those are the effects of a Korean refusal, not of Japan
  declining to act. Not fixed - needs a decision on what standing down should cost.
- [medium] `events/KORFlavor.txt` 638, 85020 - `any_greater_power = { diplomatic_influence =
  { who = THIS value = -200 } }` on a 0-100 influence pool zeroes every great power's Korean
  influence twice over, for a peasant revolt. Not fixed (balance).
- [low] 85028 - the `has_global_flag = berlin_conference` and `NOT = { berlin_conference }`
  `random_owned` blocks are identical in their effects; one of them is redundant.
- [low] 85027/85029 - `relation = { who = FROM value = 200 }` next to militancy +6 and
  `peasant_revolt` reads backwards, but it is deliberate: both events run right after
  `create_vassal`/`create_alliance` and the relation keeps the imposed alliance from breaking.
- [low] 85012/85013/85014/85030 reuse `EVTNAME85010` / `$FROMCOUNTRY$` titles; the per-id keys do
  not exist in localisation, so the reuse is intentional, not a missing-key bug.

## Arabia / Sudan

- [medium] `events/ARAFlavor.txt` 924-929, 97170 - the option scopes into `SUD = { all_core = {
  remove_core = EGY remove_core = TUR } }` while the trigger requires `SUD = { exists = no }`.
  Sudan is EGY-owned from the 1821 start, so this relies on the engine honouring `all_core` on a
  landless tag. The safe form is `any_owned = { limit = { is_core = SUD } remove_core = EGY
  remove_core = TUR }` in the owner's scope. Not fixed: dead-tag scoping is used throughout PDM and
  changing it blind could hand out core removals the current build never performs.
- [medium] `events/ARAFlavor.txt` 30-40, 96100 - the multi-statement `NOT` (a NOR) excludes
  `is_greater_power = yes`, so the Arab Revolt can never fire for a great-power Ottoman Empire,
  which is its historical subject and its state in nearly every 1821 game. Not fixed (design).
- [low] `events/ARAFlavor.txt` 966-972, 97171 - the province follow-up is gated `NOT = { year =
  1884 }` while the parent uprising only opens in 1870 with a 40-month mtth, leaving a very narrow
  window; the historical Mahdiyya ran to 1899.
- [low] 97170 - `news_desc_*` point at `EVTDESC96170_NEWS_*`. Checked: those keys exist in
  `localisation/00_PDM_news.csv`, so this is not a typo to "fix".
- [low] `events/ARAFlavor.txt` 693, 96115 option B - siding with Egypt gives every Hedjazi province
  a Turkish core (`any_owned = { add_core = TUR }`), i.e. the pro-Egypt choice manufactures the
  Ottoman claim.
- [low] 96100 - the `AND = { tag = TUR NOT = { ...governments } }` clause appears verbatim in both
  the outer `OR` and the requirement `OR`; the second is redundant.

## CSA / Schleswig-Holstein (spot checks)

- [ok] 16650/16651/16652 - the per-country guards are in place (`passenger_elevator_seen`,
  `barnum_circus_seen`, `standard_time_adopted`), the tag lists cover USA/CSA/FSA/TEX and the
  windows (1854-1864, 1871-1891, 1883+) are reachable and consistent with their mtths.
- [low] `events/CSAFlavor.txt` 70-99, 16601 - no flag guard and no `fire_only_once`: it repeats
  every ~16 months for the entire game, each time charging 20000 and growing slave pops by 2%.
  Probably intended as a recurring trade, but nothing ever ends it.
- [low] `events/SWHFlavor.txt` 490, 90055 - `badboy = -5` rewards pushing Denmark out of
  Schleswig-Holstein with an infamy refund.
- [note] 90056/90057 reuse `EVTNAME90054`; as with the Greek and Korean cases the per-id keys do
  not exist, so the shared title is deliberate.
