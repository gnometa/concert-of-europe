# The Auspicious Incident (TUR, June 1826)

Fills the `docs/design/1821-1836-coverage.md` gap "Auspicious Incident 1826 (Janissaries)".
New file `CoE_RoI_R/events/TURAuspiciousGVG.txt`, ids **1000700-1000799** (1000700-1000702
used), registered in `events/GVG Event IDs.txt`.

Research notes:
- TUR is `civilized = yes` at the 1821 start (`history/countries/TUR - Ottoman Empire.txt`),
  so the `unciv_*` military reform group in `common/issues.txt` is **not** available to it.
  The chain therefore works through country modifiers, pops and prestige only.
- Nothing in the mod mentions "janissary" (grep over the whole tree), and no TUR event is
  dated 1826: `Ottoman_Event.txt` has 31250 (1821 Balkan rebellions), 31257 (1827 Navarino),
  31295 (1830 Tripolitania), 90037 (1837). No overlap.
- `decisions/TUR.txt:tanzimat_reforms` needs `ideological_thought = 1` and an autocratic/
  constitutionalist government, and sets `tanzimat_reforms_enacted` + the `tanzimat_era`
  modifier. Per the coverage doc's risk note the new flag is **additive only**: it is used as
  an `ai_will_do` weight, never in `potential`/`allow`, so backing down cannot block Tanzimat.

Two new modifiers in `common/event_modifiers.txt` (loc keys in `GVG_events.csv`):
`nizam_i_cedid` (land_organisation -0.10, mobilisation_size +0.02, consciousness +0.02) and
`janissary_ascendancy` (land_organisation -0.15, issue_change_speed -0.25, leadership -0.15).

## Events

### 1000700 - The Eskinci Corps (June 1826)
`tag = TUR`, `year = 1826`, `NOT = { year = 1832 }`, neither outcome flag set,
`fire_only_once`, MTTH 3 months. Mahmud II's new-model battalions drill in Istanbul and the
Janissaries overturn their kettles.
1. **Turn the guns on the barracks** (historical, `ai_chance = 80`): prestige +15;
   `capital_scope` militancy +4 / consciousness +2 and the *soldiers* pops militancy +3
   empire-wide; `any_pop` reactionary -0.05; `add_country_modifier = { name = nizam_i_cedid
   duration = 3650 }` (10 years of disorganised, half-trained troops while the new army is
   raised) plus `{ name = purge duration = 730 }`, reusing the existing officer-purge
   leadership malus. Sets `janissaries_abolished`, fires 1000701.
2. **Let the kettles lie** (alt-history, `ai_chance = 20`): prestige -10;
   `add_country_modifier = { name = janissary_ascendancy duration = 3650 }`;
   `upper_house = { ideology = reactionary value = 0.10 }`; `any_pop` reactionary +0.05.
   Sets `janissary_ascendancy_flag` and fires 1000702 after 1825 days (a second chance in 1831).

### 1000701 - The Mansure Army (`is_triggered_only`, fires ~1827-28)
Fired by 1000700 option A with `days = 400`, so it lands in mid-1827. Modest reward only.
1. **Hire Prussian and French instructors** (`ai_chance = 70`): `add_country_modifier =
   { name = military_reform duration = 3650 }` (existing: leadership +0.2, militancy +0.02),
   research points +200, relations +25 with PRU and FRA, consciousness +1.
2. **Officers from Egypt** (`ai_chance = 30`): prestige +5, leadership via `military_reform`
   for 5 years only, `relation = { who = EGY value = 50 }` - cheaper, and it strengthens the
   man who invades Syria in 1831 (`events/Oriental Crisis.txt:31270`).

### 1000702 - A Second Reckoning (`is_triggered_only`, 1831)
Only reachable from option B, so the historical outcome is never permanently locked out.
1. **Strike now**: `remove_country_modifier = janissary_ascendancy`, the same militancy spike
   at half strength, `nizam_i_cedid` for 5 years, sets `janissaries_abolished`. `ai_chance = 60`.
2. **The corps has earned its place**: prestige -5, `janissary_ascendancy` made permanent
   (`duration = -1`), sets `janissary_question_settled`. `ai_chance = 40`.

## Hook into the Tanzimat decision
`decisions/TUR.txt:tanzimat_reforms` gains only an `ai_will_do` modifier
(`factor = 5, has_country_flag = janissaries_abolished`). Requirements are unchanged.
