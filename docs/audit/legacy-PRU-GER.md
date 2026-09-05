# Legacy audit: events/PRUFlavor.txt and events/GERFlavor.txt

Line-by-line logic review (2026-09-06). Mechanical audits (modcheck, refcheck,
audit_events, cwtools) were already at baseline; everything below is a logic
finding. Items marked **FIXED** were corrected in place in the same commit.

## PRUFlavor.txt (ids 34600-34609)

- `PRUFlavor.txt:94,98` 34601 — `has_pop_religion = north_german` /
  `south_german`: those are *cultures* (`common/cultures.txt:36,53`), never
  religions, so the `limit` matched nothing and the option was a silent no-op.
  Fix: `has_pop_culture`. **[high] FIXED**
- `PRUFlavor.txt:454,458` 34608 — same religion/culture confusion in the child
  labour option. Fix: `has_pop_culture`. **[high] FIXED**
  (The identical pattern exists in `1german_revolution_1848.txt:315`,
  `ScandinavianEvents.txt:836`, `SWHFlavor.txt:118,216`, `VIP Events.txt:300,319`
  — out of scope here, worth a follow-up sweep.)
- `PRUFlavor.txt:349` 34607 — mean_time_to_happen modifiers were keyed to
  `year = 1850` / `1851` while the trigger window is 1856-1859, so both factors
  were permanently on and the event effectively had mtth 3.6 months instead of
  the intended ramp. Fix: 1857 / 1858. **[medium] FIXED**
- `PRUFlavor.txt:349` 34607 option A — `capitalists = { consciousness = 2 }`
  immediately followed by `capitalists = { consciousness = 1 }`: a duplicated
  block giving +3 consciousness where the sibling pop types get +1. Fix: kept
  the single `+2`. **[medium] FIXED**
- `PRUFlavor.txt:248` 34604 — the `limit = { has_pop_religion = jewish }` is
  commented out, so the Jewish-emancipation option raises consciousness in
  *every* pop in the country. `jewish` is a real religion
  (`common/religion.txt:65`), so the intended line is
  `limit = { has_pop_religion = jewish }`. Left as-is: the comment looks
  deliberate (the author may have wanted a nationwide reaction) and restoring it
  changes designed balance. **[medium] — decide and either uncomment or delete
  the dead comment.**
- `PRUFlavor.txt:158` 34603 — the first mtth modifier uses `year = 1844`, the
  same year the trigger window opens, so it is always active and only the second
  tier ever varies. Cosmetic. **[low]**
- `PRUFlavor.txt:415` 34608 — the only event in the file gated on bare
  `tag = PRU`; 34600-34607 and 34609 use `OR = { tag = PRU capital = 549 }` so
  they also fire for NGF/GER after unification. Harmless, but inconsistent.
  **[low]**
- 34609 reuses `EVTNAME34100`/`EVTDESC34100`/`EVTOPTA34100` rather than its own
  id. Not a bug: this is the shared Mozart-festival text also used by
  `BADFlavor.txt`, `BAYFlavor.txt`, `HEDFlavor.txt`, guarded by the
  `MozartFest1838` global/country flag pair. **[low, no action]**

## GERFlavor.txt (ids 33000-33035)

- `GERFlavor.txt:976` 33031 option B — `relation = { who = FROM value = 400 }`.
  Relations are clamped to +-200, so the value is nonsense and hides the real
  intent; the sibling option correctly uses -200. Fix: 200. **[high] FIXED**
- `GERFlavor.txt:662` 33020 — the League of Three Emperors event is fired only
  at `KUK` and `RUS` (`decisions/Germany.txt:565-566`; the `AUS` lines above are
  commented out), but the `random_country` block required
  `THIS = { tag = AUS }`, so the extra GER->recipient influence branch was dead.
  The option's own `ai_chance` modifier keys on `tag = KUK`, confirming KUK is
  the intended recipient. Fix: `THIS = { tag = KUK }`. **[medium] FIXED**
- `GERFlavor.txt:577` 33015 — the `war = { attacker_goal = { casus_belli =
  call_allies_cb } call_ally = yes }` effect has no `target`. The same effect in
  `Oriental Crisis.txt:610` does specify `target = TUR`; a targetless `war`
  block does nothing (`GreatWar_Events.txt:137` has the same omission). The
  event can therefore fire, set `called_german_allies` and never call anyone.
  Not auto-fixed: the trigger allows six different war partners, so the target
  has to be chosen by design (probably `random_country = { limit = { war_with =
  THIS } ... }` around the war effect). **[medium]**
- `GERFlavor.txt:436,528` 33009/33010 — both are gated on `tag = NGF` but test
  `410 = { is_core = GER }` and remove `FRA_412` cores from **GER**. The Alsace
  cores are added as GER cores (`decisions/Germany.txt:761`), so an NGF player
  passes the trigger yet the option's
  `attacker_goal = { casus_belli = unification_casus_belli state_province_id =
  410 }` is being declared by a tag that does not own the core. Verify in-game
  whether NGF inherits GER cores; if not, either add `tag = GER` to the trigger
  `OR` or make the decision add NGF cores too. **[medium]**
- `GERFlavor.txt:1011` 33035 — no `fire_only_once` and no flag guard, mtth 12
  months, and the trigger re-qualifies as long as a germanic GP neighbour exists.
  The AI can therefore repeat -100 relations plus a humiliate CB against the same
  challenger every year or so. A `has_country_flag` guard (or a truce/CB check)
  is wanted; not auto-fixed because a deliberate repeat is plausible. **[medium]**
- `GERFlavor.txt:664,818` 33020/33027 — `diplomatic_influence` values of `200`
  and `-200`. Influence is a 0-100 pool, so these just clamp; harmless but
  misleading. **[low]**
- `GERFlavor.txt:513,569` 33009/33010 — `prestige = -50` on the renounce
  options. At the top of the plausible range for a single flavour choice, but
  defensible as the price of abandoning Alsace-Lorraine. **[low]**
- `GERFlavor.txt:4` 33003 — the comment says "parallel event is BAY 33403" and
  the loc keys are `EVTNAME33403`/`EVTDESC33403`; the trigger's tag check is
  `NOT = { exists = BAV ... }`. `BAV` is the registered tag
  (`common/countries.txt:281`); `BAY` only appears in comments, so the script is
  correct and only the comment/loc-key naming is confusing. **[low, no action]**
- 33025/33026/33027 (Spanish Pacific) — chain checked end to end: the decision
  (`decisions/Germany.txt:850-866`) fires 33025 at SPA/SPC so `FROM` = GER, 33025
  hands off with `FROM = { country_event = 33026 }` so `FROM` = SPA in the
  reply events. Seller gains `treasury = 50000`, buyer pays `-50000` — matched,
  in range, no overflow. **[no action]**
- 33006/33007/33008 (Heligoland) — fired from `decisions/ENG.txt:404` as
  `GER = { country_event = 33006 }`; 33006 hardcodes ENG rather than using FROM,
  which is safe because that decision is the only caller. Province 533 and the
  `owns = 2029` guards check out against `map/definition.csv`. **[no action]**
- 33004 — province event; `DEN = { country_event = 36206 }` resolves to
  `DANFlavor.txt:393`, and provinces 371/598/619/926/2029/2048 all exist.
  **[no action]**

## Interaction with ZollvereinGVG and decisions/Germany.txt

No id collisions: this file pair uses 33000-33035 and 34600-34609, Zollverein
uses 1000900-1000904. No flag is shared either — Zollverein works on
`zollverein_*`, `north_german_rel`, `south_german_rel`, `southern_union_member`,
none of which are read or written here. The one contact point is that
34600-34607/34609 fire on `OR = { tag = PRU capital = 549 }`, so a Zollverein-led
NGF/GER still receives the Prussian flavour chain; that is intended and, with
the culture fix above, its pop effects now actually apply to German pops.
