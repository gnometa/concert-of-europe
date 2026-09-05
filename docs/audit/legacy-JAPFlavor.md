# Legacy review: JAPFlavor.txt / JAPFlavorGVG.txt (+ JAPTenpoGVG hooks)

*2026-09-06. Line-by-line logic review of the Japan chain: Sakoku/Rangaku setup, Perry,
Sonno Joi, the Boshin War, the Meiji/Taisho content and the Line-of-Advantage wars.
Mechanical audits (`refcheck`, `audit_events`, `cwtools_check`) were at baseline before and
after; everything below is logic the tools cannot see. Items marked FIXED were changed in
this commit.*

Scope note: TKG is the bakufu; JAP and the han (SAT/CHO/TOS/KAG/SEN/YZW) are its substates.
`tozama_daimyo` / `fudai_daimyo` are set in `history/countries/`, so both branches are live.

## [high]

- `events/JAPFlavor.txt:1361` 97641 — the taiping_draft branch tested
  `foreign_training = no_foreign_training`, and there is no `foreign_training` reform group in
  `common/issues.txt` (only `unciv_military_training`). The branch never matched, and because
  the sibling branch only excludes `military_levies`, a levied shogunate got no draft at all
  while the two branches could also both fire for the same country. The parallel events 97640
  and 97642 use `unciv_military_training = military_levies`. **FIXED** to match them.
- `events/JAPFlavor.txt:3067` 97680 opt. B ("This is not in our interests at this time") did
  not set `sakhalin_line_of_advantage`, which the trigger's `NOT` guards on. Declining
  therefore re-armed the event forever, nagging Japan every MTTH roll for the rest of the game;
  every sibling (97675/97677/97678) sets its flag in both options. **FIXED** — flag added.

## [medium]

- `events/JAPFlavor.txt:1689` 97647 opt. B and `:1922` 97652 opt. B — "Never! We will fight
  to become the new Shogun!" ran `release_vassal = THIS` in the han's *own* scope, which
  releases nothing (the overlord must be the scope; 97642:1467 does it correctly as
  `TKG = { release_vassal = THIS }`). The defiant han stayed a substate and the option only
  cost it relations, i.e. the effects contradicted the option text. **FIXED** to
  `JAP = { release_vassal = THIS }` / `TKG = { release_vassal = THIS }`.
- `events/JAPFlavor.txt:3035` 97680 — `mean_time_to_happen = { months = 480 }` (40 years) on an
  event already gated on GP status, `line_of_advantage`, `nationalism_n_imperialism` and RUS
  holding Pogobi. Even with every modifier stacked it averaged ~45 months, so the Sakhalin
  Question effectively never fired; the three sibling Line-of-Advantage events use 3/24/24
  months. **FIXED** to 48 months (still the slowest of the group).
- `events/JAPFlavor.txt:1143` 97637 and `:1402` 97642 pointed at `EVTDESC97635` /
  `EVTDESC97640`, the *other* recipient's text, although recipient-specific `EVTDESC97637` and
  `EVTDESC97642` exist in localisation and were unreachable. Players read a description written
  from the shogunate's point of view. **FIXED** — each event now uses its own key.
- `events/JAPFlavor.txt:329,389` 97608/97609 — the Perry indemnity is `treasury = -100000` for
  the shogunate and `+100000` for the western power. For a 1850s unciv Japan (treasury in the
  low thousands) this is a ruinous, off-scale sum, and it is a windfall for a GP. A figure in
  the 10k-20k range would match the rest of the mod's unequal-treaty content. Not changed —
  balance judgement, needs the maintainer's call.
- `events/JAPTenpoGVG.txt:212` 1002002 opt. B — Oshio's Rising (1002003) is only queued from the
  neglect branch, at `chance = 50`. The relief branch can never see it, so `tkg_oshio_crushed` /
  `tkg_oshio_relief` are unreachable for a shogunate that fed its people; 1002004's ai_chance
  weights that reference them silently drop out. Historically the rising followed the famine
  either way. Suggest queuing it from both options with different chances. Not changed — design
  choice for the author of tonight's chain.

## [low]

- `events/JAPFlavor.txt:2254` 97670 — `treasury = -10000` is paid up front, but both
  `random_owned` blocks that actually annex Ootomari/Etorofu can fail their limits (the trigger
  admits the case where only one island is claimable). The player can pay and get nothing.
- `events/JAPFlavor.txt:1739` 97648 opt. B — "the capital shall remain in Kyoto" applies
  `gateway_to_harbor` to 1657 (Kyoto), an inland province; the modifier is a port bonus and the
  option is otherwise a pure downgrade of opt. A.
- `events/JAPFlavor.txt:2756` 97677 — `casus_belli = { target = KOR type = make_puppet
  months = 240 }` is a 20-year CB; every other CB in the file is 12-60 months.
- `events/JAPFlavor.txt:2396` 97675 — the only country gate is `has_country_modifier =
  line_of_advantage`. Nothing else in the mod grants that modifier today, so it works, but the
  event would misfire for any future non-Japanese holder; the siblings all pin `tag = JAP`.
- `events/JAPFlavor.txt:2890` 97679 opt. A ("We cannot fight them") annexes the whole target
  into JAP when it holds a single state, rather than ceding Formosa. Deliberate-looking, but the
  option text promises only the island.
- `events/JAPFlavor.txt:188` 97605 and the rest of the Perry chain only ever reach TKG (fired by
  `decisions/Japan.txt:46`). JAP and the han keep `sakoku`/`rangaku`/`uncivilized_isolationism`
  until the Boshin War resolves; a shogunate that caves in 1853 leaves its substates isolationist
  for fifteen years. No obvious cheap fix - noted for the redesign.
- Duplicated episode risk checked and cleared: 97646/97651 both have a trigger *and* are fired
  directly from 97645/97650, but their `has_global_flag = boshin_war` guard is cleared in the
  option, so neither can play twice.
- Year windows checked against the 1821 start: 97620 (1858), 97630 (1860), 97625 (1862) and the
  Tenpo windows (1825/1828/1833/1841) are all reachable and correctly ordered. `NOT` blocks with
  several statements in 97616, 97645, 97648 and the Line-of-Advantage triggers all read as NOR,
  which is what they want.

## The `EVTDESC2000002` westernisation warning

The old setup event still tells the player that Japan "is currently suffering from a bug caused
by the decisions after westernising ... only take 1 of these decisions every year". The
condition it warns about is unchanged: `decisions/Japan.txt` grants `years_of_research` in six
decisions (lines 442, 526, 553, 651, 933, 1039; 0.5-1 year each) and none of them is spaced by a
year gate or a cooldown flag, so a player who westernises and then clicks them all on the same
day gets one year's research income at the freshly-westernised (near-zero) rate instead of six.
The engine behaviour cannot be patched from script; the mod-side fix would be to convert them to
flat `research_points = N` grants, as `decisions/VIP Decisions.txt` does. Left alone here - it
is a balance change across six decisions, not a bug fix, and other agents are in that file.
