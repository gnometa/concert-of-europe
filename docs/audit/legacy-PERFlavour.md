# Audit: events/PERFlavour.txt (line-by-line logic review)

*2026-09-06. 57 event blocks, ids 300983-300990 / 300999-301075. Mechanical audits
(`modcheck braces/provinces/tags`, `refcheck`, `audit_events`, `cwtools_check`) are all at
baseline before and after this pass. Line numbers are post-fix.*

Chains in the file: the Kurdish/Sheikh Ubeydullah pair (300999-301000), the Durrani succession
(301011-301012), Merv (301013-301014), Treaty of Shiraz/Bahrain (301015-301017), the Griboyedov
Legation crisis (301020-301037), the 1821-23 Ottoman war and both Treaties of Erzurum
(301040-301045, 300983-300990), the 1825-28 Russo-Persian build-up (301053-301063), Turkmenchay
(301070-301071), and the Khiva/Herat AI wars (301073-301075).

## Is the Russo-Persian War 1826-28 / Turkmenchay modelled?

Yes, and coherently. Four mutually exclusive entry events branch on how much of the Erivan/
Nakhchivan/Karabakh group (1098-1102, 2667) PER still holds - 301053 (1825, Lake Gokcha),
301057 (Kapan already ceded), 301058 (Gyumri ceded), 301060 (No Peace No War), 301062 (Sardar of
Erivan) - each offering war (`set_country_flag = khanates_contested`, `war` vs RUS with a
`release_puppet` goal on AZB) or a further cession. Turkmenchay itself (301070) is fired from
`decisions/RUS.txt:106`, and 301071 is the Persian-victory counterfactual. `khanates_contested`
(PER) and `turkmenchay_treaty` (RUS) are both set in the `1836.1.1` blocks of the respective
history files, which correctly retires the whole chain for a 1836 start without blocking it in
1821. Nothing here is dead.

## Fixed in this pass

| line | id | problem | fix |
|---|---|---|---|
| 1732 | 301040 | `casus_belli = { target = TUR type = cut_down_to_size duration = 24 }` - the parameter is `months`; `duration` is silently ignored, so the CB was granted with no timer (every other `casus_belli` in the file uses `months`). **[high]** | `months = 24` |
| 3386-3393 | 301071 | `DAG = { any_owned = { limit = { is_core = AZB } } secede_province = PER }` - the `}` closed `any_owned` before the effect, so `secede_province` ran at DAG *country* scope (a province effect in a country scope = no-op). The Persian victory transferred nothing. **[high]** | moved `secede_province = PER` inside `any_owned` |
| 1385-1400 | 301030 | `create_vassal = AZB` sat inside the `PER = { ... }` block, so the Azerbaijan just seceded as a *Russian* concession became **Persia's** vassal - the exact opposite of the option ("We Russians are know for our magnanimity", PER's option text is "Concessions! Please the Russians"). The twin event 301037 has it correctly at RUS root. **[high]** | moved `create_vassal = AZB` out of the `PER` scope |
| 1401-1404 | 301030 | `diplomatic_influence = { who = AZB value = 400 }` - influence is capped at 100. **[medium]** | `value = 100` |
| 1877-1880 | 301043 | Option "This war is a needless distraction" (TUR *accepting* peace) applied `relation = { who = PER value = -400 }`: wrong sign for the option text, and double the +/-200 engine cap. The mirror effect on PER (301044) is positive. **[high]** | `value = 200` |
| 1919-1922 | 301044 | `relation = { who = TUR value = 325 }` past the +/-200 cap. **[medium]** | `value = 200` |
| 1383, 1425, 1599, 1638 | 301030, 301037 | RUS's `the_war_drums` flag is set in 301021 and cleared on every other terminal node (301025, 301026, 301034), but not on the concession branches. RUS kept a stale war flag for the rest of the game, permanently skewing the `has_country_flag = the_war_drums` ai_chance modifiers in 301025/301026/301030/301037. **[medium]** | added `clr_country_flag = the_war_drums` to all four options |

## Reported, not changed

| line | id | problem | note |
|---|---|---|---|
| 265 | 301012 | Dead event. Its only caller, the `any_country = { limit = { vassal_of = THIS } country_event = 301012 }` block in 301011 (lines 252-258), is commented out, so the whole Durrani vassal-reaction event (three options, `release_vassal`, `remove_core = AFG`) is unreachable. **[medium]** - re-enabling the caller is a design call (it releases AFG's vassals wholesale). |
| 3496 | 301073 | Dead event, same cause: 301072 (its only caller) is commented out at lines 3435-3489. It also uses `casus_belli = { target = FROM ... }`; `FROM` as a CB target is not attested anywhere else in the mod. **[medium]** |
| 1705 | 301040 | `money = 50000` for choosing "Our honour needs to be satisfied" - a windfall roughly an order of magnitude above Persia's 1821 treasury, granted for *declaring* a war. Looks like a leftover war-chest. **[medium]**, left alone because the intended figure is unknowable. |
| 1687-1697 | 301040 | The only live option is the war one (the "War is a needless distraction" option is commented out, lines 1745-1777), trigger is `tag = PER` + `NOT = { has_country_flag = a_turkish_adventure }` with `months = 1`. PER is railroaded into the Ottoman war within weeks of the 1821 start. Historically defensible (the war began 1821) but the player has no choice. **[low]** |
| 2682, 2788, 2922, 3056 | 301057, 301058, 301060, 301062 | No year gate; only `mean_time_to_happen` nudges them (`NOT = { year = 1826 } factor = 2` = 12 months). They can therefore fire as early as 1822, four years before the Council of Sultanieh. 301053, the sibling entry point, does gate on `year = 1825`. **[medium]** - adding `year = 1825` to the four triggers would align them, but it changes pacing so it is left for a deliberate decision. |
| 2496-2504 | 301053 | Option "We will not be pressured into giving up territory" cedes 1099 (Gyumri) to RUS anyway. Readable as "we refuse, Russia takes it regardless" (the follow-up 301055 is titled *Treaty of Tiflis (Gyumri)*), but the option text contradicts its own effect. **[medium]**, wording fix rather than a script fix. |
| 2053 | 300983 | `badboy = 15` on TUR's "Only war can settle our issues" - 60% of the infamy limit from one option. Compare 301070's `badboy = 6` and 300988's `badboy = 10`. **[medium]** magnitude, deliberate-looking. |
| 2356-2408 | 300990 | Near-verbatim copy of 300989 (same four `any_owned` blocks, same space-indented body), except its first `any_country` limit drops `is_greater_power = no`, so it also white-peaces great-power allies out of the war. Almost certainly a copy-paste omission. **[low]** |
| 3, 32 | 300999 | Duplicate id 300999 (two different events; the second shadows the first). Known baseline, left as is. |
| 3521 | 301073 | The `has_pop_religion = shiite/sunni/ibadi` limit is already commented out - correct, since pops carry no real religion in this mod (`docs/audit/religion-dead-content.md`). No live religion-form trigger remains in this file. |
| 3528, 3572 | 301074, 301075 | No `fire_only_once`; PER can re-fire the Khiva/Herat war event every 8 months once the trigger is satisfied again. Gated on `ai = yes` and `war = no`, so the player never sees it and the AI cannot stack wars, but it is unbounded. **[low]** |

## Cross-file / scope checks that came back clean

- **FROM/THIS hops.** Every `country_event` hand-off in the Griboyedov and Erzurum chains lands on
  the intended recipient (verified by walking 301020 -> 301021 -> 301022/301023/301031 ->
  301024-301037, and 300983/300986 from `decisions/PERflavour.txt:327,367`). The `THIS` uses
  inside `RUS = { ... }` in 301070 and `ENG = { ... }` in 301071 resolve to the event root (PER),
  which is what those effects want.
- **Owner scope** (`docs/audit/owner-scope.md` class). The `any_owned` blocks in 300983, 300988,
  300989, 300990, 301030, 301037 and 301070 all sit inside an explicit owner scope
  (`PER = { ... }`, `TUR` root, `KHZ/IRQ/KDS/ASY = { ... }`) or are conditional-cession branches;
  none is the unconditional-early-window class. The one real instance in this file was the 301071
  brace bug fixed above.
- **Province ids.** All 15 ids referenced (929, 934, 1090, 1098-1102, 1108, 1121, 1162, 1205,
  1206, 1223, 2667) exist in `map/definition.csv`; `modcheck provinces` reports 0.
- **Duplication with `events/DIM/PERFlavour_five_x.txt`.** No id overlap at all (that file's 85
  events live in a different range) and no duplicated episode - it is the DIM submod's own Persian
  content.
