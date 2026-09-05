# Bridge audit: 1821 start -> vanilla/PDM 1836 content

Question: do the mod's 1830s set pieces still fire when the game begins 1821.9.1?
Method: for each episode, trace the trigger chain back to something an 1821 game
actually produces (a year gate, or a flag with a live event setter).

## Background: flags set only in `1836.1.1` history blocks

Victoria 2 applies country-history dated blocks only up to the bookmark date, so
every `set_country_flag` inside a `1836.1.1 = { ... }` block is dead in an 1821
game. 39 country files carry such blocks. Cross-checking each flag against
`events/` + `decisions/` shows they are *backfills*: almost all of them also have
a live event setter, because the mod already added "1821 Start Events" sections
(e.g. `MEXFlavor.txt` 44850, `USCAFlavor.txt` 97580, `RUSTurkishWarGVG.txt`,
`GREFlavor.txt`, `Ottoman_Event.txt` 31259-31262). `existing_country` is also
granted to any existing tag within ~3 days by `CleanUp.txt` 60160.

Only six 1836-history flags have no event setter anywhere:
`confederacy_formed`, `spanish_absolutism_restored`, `mohammed_shah`,
`succession_crisis` (referenced by nothing - harmless), plus
`malacca_treaty` (used only under `NOT`, so its absence keeps the NET/DIM events
*available*, not blocked) and `1836_pbc` (used positively in `PBCFlavor.txt`:334
and `decisions/PBC.txt`:387, but PBC does not exist in 1821). None of these are
inside the six episodes below, so nothing was changed.

## 1. Great Trek 1836-38 and the Boer republics - REACHABLE

`events/BoerWar.txt` is self-contained. 98200 (`tag = ENG`, `year = 1835`) sets
the global flag `great_boer_trek`; 98205 (`tag = ZUL`, `year = 1838`) branches
into 98206/98207. ENG owns 2087 (Cape Town) and 2093 from the top-level 1821
province history, ZUL exists in 1821, and every `release = NAL/ORA/TRN` is
preceded by explicit `add_core` calls in the same option, so the tags do not
depend on the `1861.1.1` blocks in `history/provinces/africa/` (those never run
in an 1821 game either). ORA/TRN follow from 98215/98220 (`owns = 2093`,
`year = 1845`), SAF from 98230 (`year = 1852`) and `decisions/BoerWar.txt`.
`NdebeleGazaWar.txt` (95519 `year = 1830`, 99666 `year = 1837`, 99665
`year = 1840`) is likewise year-gated only.

## 2. First Anglo-Afghan War 1839-42 - NOT MODELLED

There is no scripted Anglo-Afghan war anywhere in `events/`. `TheGreatGame.txt`
(95610 ENG / 95611 RUS) is a generic influence-and-CB framework over SIN, BLC,
AFG, HRT, KDH, PNJ, the khanates. It is *reachable* - its trigger has no year
gate at all, only `is_greater_power` on ENG and RUS plus a government check - but
that also means it can start in 1821, well before the historical Great Game.
Not a blocker, so left alone; adding a dedicated 1839 war is new content.

## 3. First Carlist War 1833-40 - REACHABLE

`SPAFlavor.txt` 37760 ("Carlism") requires `tag = SPA`, `year = 1830` and a
government in {hms_government*, prussian_constitutionalism*, absolute_monarchy*}.
Spain starts 1821 as `hms_government` (Trienio Liberal) and the 1823 restoration
moves it to `absolute_monarchy` - both branches satisfy the trigger, so the
government check cannot lock the chain out either way. 37760 sets
`carlism_questioned` itself (the SPA `1836.1.1` copy is only a backfill), which
then gates 37711 (the war, mtth 1 day after `national_instability` expires),
37712, 37713 and `decisions/SPA.txt`. Isabella's 1833 succession is not modelled
as a separate death/succession event; 37760's "which ruler would be better"
option abstracts it with a 12-month mtth from 1830.

## 4. Texas Revolution 1835-36 - REACHABLE

Chain: 44850 First Mexican Empire (`year = 1821`, needs
`UCA = { has_country_flag = join_mexico }`, which `USCAFlavor.txt` 97580 sets
from 1822) -> `first_empire` -> 44854 Cherokee in Tejas (`year = 1823`) ->
44855 Empresarios (`year = 1824`, window closes at 1836) which adds the TEX cores
(`TEX_132`, 103, 105) -> 996542 (`year = 1830`) -> 44856 Republic of Texas
(`year = 1830`, needs `TEX = { exists = no }` and an owned TEX core), which sets
`texas_seceded` and creates TEX. Every gate resolves from 1821; the MEX
`1836.1.1` flags (`first_empire`, `casa_mata_plan`, `cuernavaca_plan`,
`tejas_settled`, `texas_seceded`, `mission_to_cuba`) all have live event setters
in `MEXFlavor.txt`.

## 5. Rebellions of 1837-38 in Canada - REACHABLE

`CANFlavor.txt` 44305: `tag = ENG or ENL`, `owns = 57` (Ottawa, owner = ENG in
1821 province history), `year = 1837`, `NOT = { exists = CAN,
rebellion_1837_begun, lord_durhams_report }`. No 1836-only dependency; the
follow-ups key off `rebellion_1837_begun` which 44305 sets. `BritishDominions.txt`
is unrelated to 1837 (its events are 1901-1920 dominion grants).

## 6. Egyptian-Ottoman wars 1831-33 and 1839-41 - REACHABLE

`Oriental Crisis.txt` 31270 needs `tag = EGY`, `year = 1830` and
`TUR = { has_country_flag = promised_egyptian_levant }`. That flag comes from the
Greek war chain in `Ottoman_Event.txt`: the Greek revolt event fires 31259
(Egyptian Dilemma) -> 31261 -> Egypt fights Greece -> 31262 sets
`promised_egyptian_levant` on TUR. That is 1821-start content, so the first war
is reachable. 31271/31272 use `create_vassal = EGY`, which is a no-op/refresh
against the 1805 TUR->EGY vassalage rather than a conflict.

90075 ("The Fate of Egypt", second crisis) requires `vassal_of = TUR`,
`year = 1837` and no `kutahya_treaty` / `egypt_submitted_to_ottomans` - the 1805
vassal status is exactly what it wants, so the fix that made EGY a TUR vassal
helps rather than blocks it. 31275 (Kurdish rebellion) is gated on
`NOT = { has_country_flag = egyptian_opportunity }`; the KDS `1836.1.1` flag is
never set in 1821, so the event stays available. `adrianople_treaty`,
`legitimacy` and `london_conference_1832_held` (read by this chain) are all set
live by `RUSTurkishWarGVG.txt`, `Ottoman_Event.txt` 31258-31262 and
`GREFlavor.txt` 283/341/399.

## Verdict

Reachable: 1, 3, 4, 5, 6. Not modelled: 2 (First Anglo-Afghan War). No blocking
condition was found that a code change could remove, so no script files were
modified by this audit.
