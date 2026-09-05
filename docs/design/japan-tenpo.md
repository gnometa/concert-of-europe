# Japan 1825-1841: the Tenpo crisis (JAPTenpoGVG)

`docs/design/1821-1836-coverage.md` lists JAP as having **0 dated events** before 1853:
`events/JAPFlavor.txt` is 3224 lines of Bakumatsu content (97600-97646) that all starts
with Perry's squadron. This chain fills the thirty years before it.

## Which tag

Research finding, and a correction to the brief: **TKG (Shogunate Japan) is the bakufu**
and the tag that matters. `history/diplomacy/Japan.txt` makes SEN, YZW, KAG, TOS, CHO,
SAT **and JAP** substates of TKG from `1821.9.1`. TKG owns 15 provinces (Edo 1649,
Hakodate, Ezo, the Kanto); JAP is the imperial court at Kyoto with three (1655 Osaka,
1657 Kyoto, 1659 Kobe); Nagasaki (1661) belongs to SAT.

Everything in this chain is bakufu policy - the 1825 uchiharai edict, the Bansha
persecution, famine relief, Mizuno Tadakuni's Tenpo Reforms - so all five events are
`tag = TKG`. The existing Bakumatsu chain agrees: 97600 (Sakoku, `sakoku` +
`uncivilized_isolationism` + `imperious_autocrat`, permanent) fires for TKG and the
fudai; 97601 (Rangaku, `rangaku`) fires for JAP and the tozama. Perry (97605) is TKG.

Because both isolation modifiers are already permanent on TKG from day 1, option (a)
below does **not** add another one - it pays in consciousness, prestige and relations
instead. Nothing here touches a flag the Perry chain reads
(`sakoku_applied`, `rangaku_applied`, `caved_to_commodore_perry`, `sonno_joi`, ...).

## Events (`events/JAPTenpoGVG.txt`, ids 1002000-1002004)

| id | date window | title | branches |
|---|---|---|---|
| 1002000 | 1825-1827 | The Edict to Repel Foreign Vessels | enforce (AI 80) / water and firewood |
| 1002001 | 1828-1830 | The Siebold Incident | punish (AI 70) / lenience |
| 1002002 | 1833-1837 | The Tenpo Famine | open the granaries / let it run (AI 60) |
| 1002003 | fired by 1002002, 50% | Oshio Heihachiro's Rising | crush (AI 70) / concede rice |
| 1002004 | 1841-1844 | The Tenpo Reforms | Mizuno's austerity (AI 60) / abandon |

All are `tag = TKG` + `exists = yes` + `fire_only_once = yes`; since only one tag can
ever trigger them, engine-wide `fire_only_once` is safe here (CLAUDE.md pitfall).

## Modifiers and effects

Only modifiers that already exist in `common/event_modifiers.txt` are used:
`secret_police` (Bansha purge, 5 y), `famine` (province, 2 y - idiom copied from the
Persian famine 190319 in `DIM/PERFlavour_five_x.txt`), `purge` (crushing Oshio, 2 y),
`tax_reforms` + `conservative_reaction` (the Tenpo Reforms). Pictures are all existing
files: `rangoku`, `starving`, `streetriot`, `military_reform`.

## Flags

Every flag set is read again inside the chain, so `refcheck flags` stays clean:

- `tkg_uchiharai_edict` / `tkg_uchiharai_relaxed` - set by 1002000, gate 1002001
  (the Siebold affair only lands once the coast policy is settled) and weight 1002004.
- `tkg_bansha_purge` / `rangaku_tolerated` - set by 1002001. `rangaku_tolerated` also
  shortens 1002004's MTTH and pushes its AI towards the liberal branch, which is the
  reward for having let the Dutch scholars work.
- `tkg_tenpo_relief` / `tkg_tenpo_neglect` - set by 1002002; neglect also rolls the 50%
  for Oshio. Both weight 1002004.
- `tkg_oshio_crushed` / `tkg_oshio_relief` - set by 1002003, weight 1002004.
- 1002004 is terminal and sets nothing.

## Localisation

`localisation/GVG_events.csv`, appended with `modcheck loc-add` (never Edit/Write).
Keys `EVTNAME/EVTDESC/EVTOPTA/EVTOPTB` for each of the five ids; no news keys.
