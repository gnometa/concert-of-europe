# 1821 starting literacy

*2026-09-06. Replaces the flat `literacy = 0.01` that commit `8f5e1248` ("economic
rework base", 2020) stamped on all 521 country history files. Applied by
`scripts/apply_literacy.py`, which carries this table as a dict; edit the script and
re-run it rather than hand-editing `history/countries`.*

## What changed and what did not

- Only the `literacy = ` value in the **top-level (undated) block** of each
  `CoE_RoI_R/history/countries/*.txt` is set. 472 of 521 files moved; the rest were
  already at their tier value (0.01).
- `non_state_culture_literacy` **stays at the 0.01 floor** everywhere. In 1821 the
  non-state cultures of the big multi-ethnic states (Habsburg Slavs, Ottoman and
  Russian subject peoples, every colonial population) genuinely were near-illiterate,
  and leaving the floor in place keeps the education rework's `RGO_education_0`
  bracket meaningful for colonies.
- The dated `1836.1.1` / `1861.1.1` blocks are **left flat**. Their pre-flatten values
  were deliberate and internally consistent (they are the PDM/vanilla timeline), but
  the mod ships a single bookmark at `1821.9.1` and the engine never reads a dated
  history block later than the start date, so restoring them would change nothing that
  can be observed in game. `REB - Rebels.txt` has no literacy line and is skipped.
- The old PDM value survives as the trailing `#literacy = X` comment on every line, so
  the reference is still there to read.

## How the numbers were chosen

Three inputs, in order of weight:

1. **Real-world 1821 adult literacy estimates.** These are the target. Where an
   estimate exists for a state (Prussia, Sweden, England, France, Russia, Japan) it is
   used directly; elsewhere the closest documented neighbour or the schooling regime
   (Lutheran catechism, Volksschule, medrese, terakoya, monastery, none) sets the band.
2. **The pre-flatten values** recovered from `8f5e1248^` (they survive inline as
   `#literacy = X`). Useful as an *ordering* check, but they are PDM's 1836 numbers
   backdated by a fixed shave and are systematically too high for 1821 - PDM has
   Prussia at 0.785 and the north German minors at 0.69, where the real 1821 figures
   are nearer 0.55 and 0.50. They were not copied.
3. **Vanilla `history/countries` 1836 literacy** as a sanity ceiling (Prussia 0.70,
   UK 0.55, USA 0.50, Japan 0.40, Russia 0.10, Spain 0.13). Every 1821 value here sits
   at or below its vanilla 1836 counterpart, which is the direction history runs.

Values are assigned by **tier**, never per tag, so that every tag sharing a nation gets
the same number: the Japanese han (`CHO`, `SAT`, `TOS`, `KAG`, `SEN`, `YZW`) and the
imperial court tag `JAP` all match the Shogunate `TKG`; the Indian princely states all
match `HND`; the Chinese warlord and successor tags all match `QNG`; the German minors
all match each other; the US state release tags follow the free/slave-state split that
the `USA` blend averages.

## Tiers

| tier | literacy | justification | tags |
|---|---:|---|---|
| `nordic` | 0.70 | Lutheran household examination (husforhor); reading literacy was near-universal by 1800 | DEN, FIN, ICL, NOR, SCA, SWE |
| `usa_north` | 0.60 | New England and Old Northwest common schools; the highest attested rate anywhere in 1821 | DAK, FSA, MAN, NEN, UIA, UIL, UIN, UMI, UMN, UNB, UNJ, UNY, UOH, UOR, UPA, UWI |
| `britain` | 0.55 | English signature literacy ~0.55, Scottish parish schools ~0.75, Welsh Sunday schools; blended | ENG, ENL, SCO, WHA |
| `lowlands` | 0.55 | Dutch 1806 school law and Swiss cantonal schools plus dense urban print culture | NET, SWI |
| `prussia_saxony` | 0.55 | Compulsory Volksschule since 1763/1805; the best-schooled states in Europe in 1821 | PRU, SAX |
| `usa` | 0.55 | Free-state ~0.60 blended with the slave South ~0.35 into one country | USA |
| `north_german` | 0.50 | Protestant north German states with Prussian-style school ordinances | ANH, BRA, BRE, COB, DZG, EFR, FRM, HAM, HAN, HEK, HES, HOL, LIP, LUB, LUZ, MEC, MEI, NAS, NGF, OLD, PML, RHI, SAA, SCH, SLS, SWH, WEI, WES |
| `settler` | 0.50 | British settler colonies: literate emigrant stock, church schools from the start | AST, COL, MRU, NEW, NZL, SNZ |
| `german_unified` | 0.45 | Unification tag: north German schooling blended with the Catholic south | GER |
| `usa_west` | 0.45 | Anglo settler populations, no established school system yet | CAL, DES |
| `canada` | 0.42 | The Canadas in 1821 are majority French-Canadian stock; between Quebec and the anglophone colonies | CAN |
| `france_belgium` | 0.42 | Restoration France and the southern Netherlands; ~0.45 male, ~0.35 female | ALS, BEL, FLA, FRA, LUX, WLL |
| `baltic_lutheran` | 0.40 | Estonian, Latvian and Finnish Lutheran reading literacy high, writing literacy low | EST, LAT, UBD |
| `boer` | 0.35 | Cape and Boer settler society, Dutch Reformed home schooling | NAL, ORA, SAF, TRN |
| `south_german` | 0.35 | Catholic south Germany and Austria proper: schooling later and thinner than Prussia | AUS, BAD, BAV, SGF, WUR |
| `usa_south` | 0.35 | Plantation South: no common-school system, slave literacy criminalised | CSA, TEX, UAL, UAR, UFL, UGA, UKY, ULA, UMO, UMS, UNC, USC, UTN, UVA, UWV |
| `bohemia` | 0.30 | Bohemian Normalschulen; the best-schooled Habsburg crownland | BOH, CZH |
| `france_periphery` | 0.30 | Breton and Occitan non-French-speaking peripheries lagged the national rate | BRT, OCC |
| `ireland` | 0.30 | Hedge schools before the 1831 national system | IRE |
| `japan` | 0.30 | Terakoya and han schools; the highest non-Western rate in 1821 | CHO, JAP, KAG, SAT, SEN, TKG, TOS, YZW |
| `quebec` | 0.30 | French-Canadian literacy well below anglophone British North America | QUE |
| `habsburg_dual` | 0.28 | Austrian-administered Slovene and Adriatic lands, and the dual-monarchy tag | KUK, SLO, TRE |
| `north_italy` | 0.25 | Piedmont, Lombardy-Venetia, Tuscany and the duchies; Austrian school law in the north | LOM, LUC, MOD, PAR, RMG, SAR, SRD, SVY, TUS, VEN |
| `hungary` | 0.22 | Hungarian and Slovak lands: county schools for the gentry, little for the peasantry | BAN, DNB, HUN, SLV |
| `frontier_mixed` | 0.20 | Metis, Rupert-s Land and Sapmi: mixed settler/indigenous, some mission schooling | MTC, RPL, SMI |
| `iberia` | 0.20 | Spain after the Cadiz reforms; schooling urban and clerical | BSQ, CAT, IBR, SPA, SPC |
| `italy_unified` | 0.20 | Unification tag: northern rates blended with the Mezzogiorno | ITA |
| `poland` | 0.20 | Congress Poland and Krakow: the 1815-30 Polish school system before its suppression | CPL, KRA, PLC, POL, PZN |
| `habsburg_south` | 0.18 | Croatian Military Frontier schooling, above the Ottoman Balkans | CRO |
| `portugal` | 0.15 | Portugal and the Portugal-Brazil union: poorest schooling in western Europe | POR, UPB |
| `qing` | 0.15 | Qing China: Rawski puts adult male literacy at 30-45%, blended with a much lower female rate | CHI, FJN, GMJ, GNG, GXI, HNN, HUI, KMT, MCK, QNG, SXI, SZC, TAI, TPG, XBI, YNN |
| `caribbean` | 0.12 | Caribbean colonies: literate free population over an enslaved majority | ANC, CUB, GUY, JAM, PRI, TTB |
| `eastern_catholic` | 0.12 | Galicia, Bukovina, Transylvania, Dalmatia, Lithuania: Habsburg and Polish periphery | BKV, DLM, GLM, LIT, RUT, SIE, SYL |
| `latam_mid` | 0.12 | Larger post-independence republics: creole urban literacy over an illiterate countryside | ARG, BRZ, CHL, CLM, ENT, GCO, LPL, MEX, PNM, PRG, RGS, URU, VNZ |
| `south_italy` | 0.12 | Two Sicilies, the Papal States, Malta and Corsica: no state schooling | CRS, MLT, PAP, SIC |
| `centam` | 0.10 | Central American republics: parish schooling in the towns | COS, ELS, GUA, HON, NIC, UCA |
| `dynamic` | 0.10 | Generic dynamic/release placeholder tag, never present at the 1821 start | D01, D02, D03, D04, D05, D06, D07, D08, D09, D10, D11, D12, D13, D14, D15, D16, D17, D18, D19, D20, D21, D22, D23, D24, D25, D26, D27, D28, D29, D30, D31, D32, D33, D34, D35, D36, D37, D38, D39, D40, D41, D42, D43, D44, D45, D46, D47, D48, D49, D50 |
| `greece` | 0.10 | Greek merchant and church schools, well above the Ottoman average | BYZ, CRE, GRE, ION, PON |
| `korea` | 0.10 | Joseon: hanja for the yangban, growing hangul literacy below it | KOR |
| `liberia` | 0.10 | Americo-Liberian settlers were literate; the interior was not | LIB |
| `philippines` | 0.10 | Spanish parish schools in the Christianised lowlands | PHL |
| `ryukyu` | 0.10 | Ryukyu kingdom, schooled on the Japanese and Chinese model | RYU |
| `latam_low` | 0.08 | Andean and Mesoamerican republics with large unschooled indigenous majorities | BOL, CHP, DOM, ECU, LOS, NPU, OAX, PBC, PEU, PTG, RGR, SON, SPU, UNM, YUC |
| `ottoman_christian` | 0.08 | Armenian, Assyrian and Maronite communities ran their own schools | ASY, LBN |
| `seasia_buddhist` | 0.08 | Theravada monastery schooling gave Burma and Siam unusually high male literacy | BUR, CAM, CHK, LNA, LUA, LXA, SIA, WIA |
| `seasia_confucian` | 0.08 | Vietnamese village schools on the Chinese classical model | DAI |
| `balkan_ottoman` | 0.06 | Christian Ottoman subject nations: monastery schooling only | BOS, BUL, EPI, MCD, MOL, MON, ROM, SER, WAL, YUG |
| `russia` | 0.06 | Serf empire; literacy confined to nobility, clergy and townsmen | AKH, BYE, CRI, DON, KRL, RUS, TAR, UKR, URA |
| `egypt` | 0.05 | Muhammad Ali had only just founded his first state schools; the base was kuttab literacy | EGY |
| `haiti` | 0.05 | Post-revolutionary Haiti; schooling limited to the Port-au-Prince elite | HAI |
| `india` | 0.05 | Company India and the princely states; village and maktab schools, ~5-6% of adult males | ASM, AWA, BAS, BER, BHO, BIH, BIK, BNG, BUN, DRA, GWA, HDU, HND, HYD, IND, JAI, JAS, JOD, KAS, KRN, KUT, MAH, MEW, MRT, MUG, MYS, NAG, ORI, PAK, PNJ, RAJ, SHI, SIN, SRI, TRA |
| `ottoman` | 0.05 | Ottoman Empire: medrese literacy in Turkish and Arabic, ~5% of adults | CYP, TUR |
| `ottoman_arab` | 0.05 | Arab Ottoman provinces, same medrese base as the metropole | BAB, IRQ, ISR, JOR, PLS, SYR |
| `persia` | 0.05 | Qajar Persia: maktab literacy in the towns | GLN, KHR, KHZ, PER |
| `caucasus` | 0.04 | Georgian and Armenian church schooling in a mostly illiterate countryside | ARM, AZB, CIR, DAG, GEO, TCA |
| `africa_muslim` | 0.03 | Sahelian and Swahili Muslim states with Quranic school networks | ADW, BDU, BMK, DAM, DAR, DND, GBU, JAL, KBO, KNG, KRT, MAS, MLI, MOS, SEG, SOK, SUD, TOU, TRZ, WAD, WOL, ZAN |
| `arabia` | 0.03 | Arabian emirates and imamates: Quranic schooling only | ABU, ARB, ARU, ASR, BHR, HAL, HDJ, KWT, NEJ, NYE, OMA, YEM |
| `balkan_muslim` | 0.03 | Albanian highlands: no schooling in any language | ALB |
| `maghreb` | 0.03 | North African regencies: Quranic schooling, no state system | ALD, CYR, LBY, MGH, MOR, TRI, TUN |
| `qing_frontier` | 0.03 | Tibet, Mongolia, Xinjiang: monastic or madrasa literacy only | MGL, TIB, TNT, UYG, XIN |
| `russia_frontier` | 0.03 | Siberian, steppe and Arctic governorates | ALT, KAM, KMK, LSK, SIB, YAK |
| `centralasia` | 0.02 | Afghan and Turkestani khanates: madrasa literacy in a few cities | AFG, BLC, BUK, DUR, HRT, HZJ, KAL, KAZ, KDH, KDS, KHI, KNZ, KOK, KYR, MAK, TAJ, TKM, TKS, UZB |
| `himalaya` | 0.02 | Nepal, Bhutan, Sikkim, Ladakh: monastic literacy only | BHU, LAD, NEP, SIK |
| `horn` | 0.02 | Ethiopian church schooling and Somali Quranic schooling, both very narrow | AWS, ERT, ETH, GEL, GON, MAJ, SHW, SOM, TIG |
| `pacific_tribal` | 0.02 | Pacific and other tribal societies; mission schooling only beginning in 1821 | AIN, AOT, CHE, FIJ, HAW, TGA |
| `seasia` | 0.02 | Malay and Indonesian archipelago states: pesantren literacy only | ATJ, BAL, BIM, BRU, DJA, INO, JAV, JOH, KCH, KLM, KTI, LAN, MAL, MLY, SAK, SHA, SLW, SUL, SWK |
| `africa` | 0.01 | Non-literate or newly-missionised African societies | ANG, ARO, ASH, AZA, BEN, BRD, BSH, BUG, CAR, CGO, CHD, CLA, CMR, CNG, DAH, GAB, GAZ, GMB, GNE, IVC, KNY, KON, KUB, KZB, LBA, LOA, LUN, MAD, MAT, MLW, MNG, MOZ, NGR, NIG, OYO, RHO, RWA, SHO, SLE, SNG, SUA, TNZ, TOG, TOO, TSW, WRI, XHO, ZAM, ZUL |

## Literacy growth: `LITERACY_CHANGE_SPEED`

A historical 1821 start is only half the job. Victoria 2 grows pop literacy from the
clergy share of each state, scaled by `LITERACY_CHANGE_SPEED` in
`CoE_RoI_R/common/defines.lua` (alongside `BASE_CLERGY_FOR_LITERACY = 0.003` and
`MAX_CLERGY_FOR_LITERACY = 0.05`, both already tuned by this mod). There is **no script
effect that sets literacy**, so this define is the only lever on the growth side.

The mod had `LITERACY_CHANGE_SPEED = 0.0050`, one twentieth of vanilla's `0.1`. With a
flat 0.01 start that was survivable, because education-efficiency modifiers were doing
all the differentiating. With historical start values it is not: a state at 0.05 would
still be at roughly 0.05 in 1900, which is the opposite of what happened.

Real-world calibration:

| | 1820 | ~1900 | change over 80 years |
|---|---:|---:|---:|
| Russia | ~0.06 | ~0.28 (1897 census) | +0.22 |
| Prussia/Germany | ~0.55 | ~0.99 | +0.44 |

So the slowest large state in Europe still quadrupled, and the fastest closed a
0.45 gap. Set to **`LITERACY_CHANGE_SPEED = 0.05`** — half of vanilla, ten times the
old mod value. Half of vanilla rather than vanilla itself because this mod already
grants a flat `education_efficiency_modifier = 2.00` in `common/static_modifiers.txt`
`base_values` (vanilla grants none) on top of a hundred-plus further education
modifiers, so the effective rate is well above the raw define.

RUS (0.06) and TUR (0.05) keep their historical start values: the problem those numbers
appeared to cause was never the start value, it was the frozen growth rate.

**Untested in game.** The interaction with the mod's clergy defines and the
education-efficiency stack can only be checked by running the 1821 bookmark and
sampling literacy in 1840/1860/1900 for RUS, TUR, QNG, PRU and ENG. This belongs on the
play-test checklist; if literacy runs away, `0.02-0.03` is the next step down.

## Per-tag values

`pre` is the pre-flatten PDM value recovered from `8f5e1248^`, shown for comparison
only. Files are listed by tag; `ETH` and `SAR`/`SRD` appear twice because two history
files carry them.

| tag | file | tier | 1821 | pre |
|---|---|---|---:|---:|
| ABU | ABU - Abu Dhabi | `arabia` | 0.03 | 0.29 |
| ADW | ADW - Adamawa | `africa_muslim` | 0.03 | 0.002 |
| AFG | AFG - Afghanistan | `centralasia` | 0.02 | 0.01 |
| AIN | AIN - Ainu | `pacific_tribal` | 0.02 | 0.03 |
| AKH | AKH - Astrakhan | `russia` | 0.06 | 0.04 |
| ALB | ALB - Albania | `balkan_muslim` | 0.03 | 0.14 |
| ALD | ALD - Aldjazair | `maghreb` | 0.03 | 0.04 |
| ALS | ALS - Elsass | `france_belgium` | 0.42 | 0.8 |
| ALT | ALT - Altai Republic | `russia_frontier` | 0.03 | 0.1 |
| ANC | ANC - Antillean Confederation | `caribbean` | 0.12 | 0.17 |
| ANG | ANG - Angola | `africa` | 0.01 | 0.13 |
| ANH | ANH - Anhalt | `north_german` | 0.5 | 0.69 |
| AOT | AOT - Aotearoa | `pacific_tribal` | 0.02 | 0.1 |
| ARB | ARB - Arabia | `arabia` | 0.03 | 0.4 |
| ARG | ARG - Argentina | `latam_mid` | 0.12 | 0.11 |
| ARM | ARM - Armenia | `caucasus` | 0.04 | 0.09 |
| ARO | ARO - Aro | `africa` | 0.01 | 0.02 |
| ARU | ARU - Arab Union | `arabia` | 0.03 | 0.6 |
| ASH | ASH - Ashanti | `africa` | 0.01 | 0.03 |
| ASM | ASM - Assam | `india` | 0.05 | 0.02 |
| ASR | ASR - Asir | `arabia` | 0.03 | 0.01 |
| AST | AST - Australia | `settler` | 0.5 | 0.7 |
| ASY | ASY - Assyria | `ottoman_christian` | 0.08 | 0.06 |
| ATJ | ATJ - Atjeh | `seasia` | 0.02 | 0.02 |
| AUS | AUS - Austria | `south_german` | 0.35 | 0.49 |
| AWA | AWA - Awadh | `india` | 0.05 | 0.09 |
| AWS | AWS - Awsa | `horn` | 0.02 | 0.02 |
| AZA | AZA - Azande | `africa` | 0.01 | 0.003 |
| AZB | AZB - Azerbaijan | `caucasus` | 0.04 | 0.02 |
| BAB | BAB - Babylonia | `ottoman_arab` | 0.05 | 0.28 |
| BAD | BAD - Baden | `south_german` | 0.35 | 0.64 |
| BAL | BAL - Bali | `seasia` | 0.02 | 0.005 |
| BAN | BAN - Banat | `hungary` | 0.22 | 0.1 |
| BAS | BAS - Bastar | `india` | 0.05 | 0.01 |
| BAV | BAV - Bavaria | `south_german` | 0.35 | 0.59 |
| BDU | BDU - Bondou | `africa_muslim` | 0.03 | 0.004 |
| BEL | BEL - Belgium | `france_belgium` | 0.42 | 0.6 |
| BEN | BEN - Benin | `africa` | 0.01 | 0.02 |
| BER | BER - Beroda | `india` | 0.05 | 0.01 |
| BHO | BHO - Bhopal | `india` | 0.05 | 0.01 |
| BHR | BHR - Bahrain | `arabia` | 0.03 | 0.008 |
| BHU | BHU - Bhutan | `himalaya` | 0.02 | 0.01 |
| BIH | BIH - Bihar | `india` | 0.05 | 0.09 |
| BIK | BIK - Bikaner | `india` | 0.05 | 0.01 |
| BIM | BIM- Bima | `seasia` | 0.02 | 0.03 |
| BKV | BKV - Bukovina | `eastern_catholic` | 0.12 | 0.1 |
| BLC | BLC - Baluchistan | `centralasia` | 0.02 | 0.02 |
| BMK | BMK - Bamako | `africa_muslim` | 0.03 | 0.004 |
| BNG | BNG - Bengal | `india` | 0.05 | 0.1 |
| BOH | BOH - Bohemia | `bohemia` | 0.3 | 0.7 |
| BOL | BOL - Bolivia | `latam_low` | 0.08 | 0.08 |
| BOS | BOS - Bosnia | `balkan_ottoman` | 0.06 | 0.2 |
| BRA | BRA - Braunschweig | `north_german` | 0.5 | 0.69 |
| BRD | BRD - Urundi | `africa` | 0.01 | 0.01 |
| BRE | BRE - Bremen | `north_german` | 0.5 | 0.69 |
| BRT | BRT - Brittany | `france_periphery` | 0.3 | 0.48 |
| BRU | BRU - Brunei | `seasia` | 0.02 | 0.02 |
| BRZ | BRZ - Brazil | `latam_mid` | 0.12 | 0.07 |
| BSH | BSH - Basotho | `africa` | 0.01 | 0.01 |
| BSQ | BSQ - Basqueland | `iberia` | 0.2 | 0.48 |
| BUG | BUG - Buganda | `africa` | 0.01 | 0.01 |
| BUK | BUK - Bukkhara | `centralasia` | 0.02 | 0.01 |
| BUL | BUL - Bulgaria | `balkan_ottoman` | 0.06 | 0.4 |
| BUN | BUN - Bundelkhand | `india` | 0.05 | 0.01 |
| BUR | BUR - Burma | `seasia_buddhist` | 0.08 | 0.01 |
| BYE | BYE - Belarus | `russia` | 0.06 | 0.4 |
| BYZ | BYZ - Byzantium | `greece` | 0.1 | 0.22 |
| CAL | CAL - Californian Republic | `usa_west` | 0.45 | 0.50 |
| CAM | CAM - Cambodia | `seasia_buddhist` | 0.08 | 0.01 |
| CAN | CAN - Canada | `canada` | 0.42 | 0.6 |
| CAR | CAR - Central African Republic | `africa` | 0.01 | 0.004 |
| CAT | CAT - Catalonia | `iberia` | 0.2 | 0.13 |
| CGO | CGO - Congo-Brazzaville | `africa` | 0.01 | 0.004 |
| CHD | CHD - Chad | `africa` | 0.01 | 0.002 |
| CHE | CHE - Cherokee | `pacific_tribal` | 0.02 | 0.005 |
| CHI | CHI - China | `qing` | 0.15 | 0.05 |
| CHK | CHK - Champasak | `seasia_buddhist` | 0.08 | 0.01 |
| CHL | CHL - Chile | `latam_mid` | 0.12 | 0.10 |
| CHO | CHO - Choshu | `japan` | 0.3 | 0.39 |
| CHP | CHP - Chiapas | `latam_low` | 0.08 | 0.09 |
| CIR | CIR - Circassia | `caucasus` | 0.04 | 0.02 |
| CLA | CLA - Calabar | `africa` | 0.01 | 0.02 |
| CLM | CLM - Colombia | `latam_mid` | 0.12 | 0.11 |
| CMR | CMR - Cameroon | `africa` | 0.01 | 0.004 |
| CNG | CNG - Congo Free State | `africa` | 0.01 | 0.28 |
| COB | COB - Saxe | `north_german` | 0.5 | 0.69 |
| COL | COL - Columbia | `settler` | 0.5 | 0.6 |
| COS | COS - Costa Rica | `centam` | 0.1 | 0.17 |
| CPL | CPL - Congress Poland | `poland` | 0.2 | 0.19 |
| CRE | CRE - Crete | `greece` | 0.1 | 0.22 |
| CRI | CRI - Crimea | `russia` | 0.06 | 0.1 |
| CRO | CRO - Croatia | `habsburg_south` | 0.18 | 0.2 |
| CRS | CRS - Corsica | `south_italy` | 0.12 | 0.48 |
| CSA | CSA - CSA | `usa_south` | 0.35 | 0.50 |
| CUB | CUB - Cuba | `caribbean` | 0.12 | 0.17 |
| CYP | CYP - Cyprus | `ottoman` | 0.05 | 0.04 |
| CYR | CYR - Cyrenaica | `maghreb` | 0.03 | 0.02 |
| CZH | CZH - Czechoslovakia | `bohemia` | 0.3 | 0.28 |
| D01 | D01 | `dynamic` | 0.1 | 0.17 |
| D02 | D02 | `dynamic` | 0.1 | 0.17 |
| D03 | D03 | `dynamic` | 0.1 | 0.17 |
| D04 | D04 | `dynamic` | 0.1 | 0.17 |
| D05 | D05 | `dynamic` | 0.1 | 0.17 |
| D06 | D06 | `dynamic` | 0.1 | 0.17 |
| D07 | D07 | `dynamic` | 0.1 | 0.17 |
| D08 | D08 | `dynamic` | 0.1 | 0.17 |
| D09 | D09 | `dynamic` | 0.1 | 0.17 |
| D10 | D10 | `dynamic` | 0.1 | 0.17 |
| D11 | D11 | `dynamic` | 0.1 | 0.17 |
| D12 | D12 | `dynamic` | 0.1 | 0.17 |
| D13 | D13 | `dynamic` | 0.1 | 0.17 |
| D14 | D14 | `dynamic` | 0.1 | 0.17 |
| D15 | D15 | `dynamic` | 0.1 | 0.17 |
| D16 | D16 | `dynamic` | 0.1 | 0.17 |
| D17 | D17 | `dynamic` | 0.1 | 0.17 |
| D18 | D18 | `dynamic` | 0.1 | 0.17 |
| D19 | D19 | `dynamic` | 0.1 | 0.17 |
| D20 | D20 | `dynamic` | 0.1 | 0.20 |
| D21 | D21 | `dynamic` | 0.1 | 0.03 |
| D22 | D22 | `dynamic` | 0.1 | 0.02 |
| D23 | D23 | `dynamic` | 0.1 | 0.02 |
| D24 | D24 | `dynamic` | 0.1 | 0.03 |
| D25 | D25 | `dynamic` | 0.1 | 0.01 |
| D26 | D26 | `dynamic` | 0.1 | 0.03 |
| D27 | D27 | `dynamic` | 0.1 | 0.02 |
| D28 | D28 | `dynamic` | 0.1 | 0.02 |
| D29 | D29 | `dynamic` | 0.1 | 0.02 |
| D30 | D30 | `dynamic` | 0.1 | 0.02 |
| D31 | D31 | `dynamic` | 0.1 | 0.02 |
| D32 | D32 | `dynamic` | 0.1 | 0.02 |
| D33 | D33 | `dynamic` | 0.1 | 0.02 |
| D34 | D34 | `dynamic` | 0.1 | 0.17 |
| D35 | D35 | `dynamic` | 0.1 | 0.17 |
| D36 | D36 | `dynamic` | 0.1 | 0.17 |
| D37 | D37 | `dynamic` | 0.1 | 0.17 |
| D38 | D38 | `dynamic` | 0.1 | 0.17 |
| D39 | D39 | `dynamic` | 0.1 | 0.17 |
| D40 | D40 | `dynamic` | 0.1 | 0.17 |
| D41 | D41 | `dynamic` | 0.1 | 0.17 |
| D42 | D42 | `dynamic` | 0.1 | 0.17 |
| D43 | D43 | `dynamic` | 0.1 | 0.17 |
| D44 | D44 | `dynamic` | 0.1 | 0.17 |
| D45 | D45 | `dynamic` | 0.1 | 0.17 |
| D46 | D46 | `dynamic` | 0.1 | 0.17 |
| D47 | D47 | `dynamic` | 0.1 | 0.17 |
| D48 | D48 | `dynamic` | 0.1 | 0.17 |
| D49 | D49 | `dynamic` | 0.1 | 0.17 |
| D50 | D50 | `dynamic` | 0.1 | 0.17 |
| DAG | DAG - Dagestan | `caucasus` | 0.04 | 0.02 |
| DAH | DAH - Dahomey | `africa` | 0.01 | 0.03 |
| DAI | DAI - Dai Viet | `seasia_confucian` | 0.08 | 0.01 |
| DAK | DAK - Dakota | `usa_north` | 0.6 | 0.50 |
| DAM | DAM - Damagaram | `africa_muslim` | 0.03 | 0.05 |
| DAR | DAR - Darfur | `africa_muslim` | 0.03 | 0.05 |
| DEN | DEN - Denmark | `nordic` | 0.7 | 0.69 |
| DES | DES - Deseret | `usa_west` | 0.45 | 0.50 |
| DJA | DJA - Jambi | `seasia` | 0.02 | 0.02 |
| DLM | DLM - Dalmatia | `eastern_catholic` | 0.12 | 0.2 |
| DNB | DNB - Danubian Federation | `hungary` | 0.22 | 0.25 |
| DND | DND - Dendi | `africa_muslim` | 0.03 | 0.02 |
| DOM | DOM - Dominican Republic | `latam_low` | 0.08 | 0.09 |
| DON | DON - Cossackia | `russia` | 0.06 | 0.15 |
| DRA | DRA - Dravidistan | `india` | 0.05 | 0.02 |
| DUR | DUR - Durrani Empire | `centralasia` | 0.02 | 0.2 |
| DZG | DZG - Danzig | `north_german` | 0.5 | 0.65 |
| ECU | ECU - Ecuador | `latam_low` | 0.08 | 0.09 |
| EFR | EFR - East Frisia | `north_german` | 0.5 | 0.59 |
| EGY | EGY - Egypt | `egypt` | 0.05 | 0.06 |
| ELS | ELS - El Salvador | `centam` | 0.1 | 0.17 |
| ENG | ENG - United Kingdom | `britain` | 0.55 | 0.58 |
| ENL | ENL - England | `britain` | 0.55 | 0.55 |
| ENT | ENT - Entre Rios | `latam_mid` | 0.12 | 0.1 |
| EPI | EPI - Epirus | `balkan_ottoman` | 0.06 | 0.14 |
| ERT | ERT - Eritrea | `horn` | 0.02 | 0.02 |
| EST | EST - Estonia | `baltic_lutheran` | 0.4 | 0.6 |
| ETH | ETH - Abyssinia | `horn` | 0.02 | 0.07 |
| ETH | ETH - Ethiopia | `horn` | 0.02 | 0.07 |
| FIJ | FIJ - Fiji | `pacific_tribal` | 0.02 | 0.02 |
| FIN | FIN - Finland | `nordic` | 0.7 | 0.64 |
| FJN | FJN - Fujian | `qing` | 0.15 | 0.03 |
| FLA | FLA - Flanders | `france_belgium` | 0.42 | 0.28 |
| FRA | FRA - France | `france_belgium` | 0.42 | 0.59 |
| FRM | FRM - Frankfurt am Main | `north_german` | 0.5 | 0.69 |
| FSA | FSA - Free States of America | `usa_north` | 0.6 | 0.50 |
| GAB | GAB - Gabon | `africa` | 0.01 | 0.004 |
| GAZ | GAZ - Gaza | `africa` | 0.01 | 0.01 |
| GBU | GBU - Gabu | `africa_muslim` | 0.03 | 0.001 |
| GCO | GCO - Gran Colombia | `latam_mid` | 0.12 | 0.11 |
| GEL | GEL - Geledi | `horn` | 0.02 | 0.003 |
| GEO | GEO - Georgia | `caucasus` | 0.04 | 0.1 |
| GER | GER - Germany | `german_unified` | 0.45 | 0.87 |
| GLM | GLM - Galicia-Lodomeria | `eastern_catholic` | 0.12 | 0.6 |
| GLN | GLN - Gilan | `persia` | 0.05 | 0.3 |
| GMB | GMB - Gambia | `africa` | 0.01 | 0.004 |
| GMJ | GMJ - Guominjun | `qing` | 0.15 | 0.03 |
| GNE | GNE - Guinea | `africa` | 0.01 | 0.004 |
| GNG | GNG - Guangdong | `qing` | 0.15 | 0.04 |
| GON | GON - Gonder | `horn` | 0.02 | 0.02 |
| GRE | GRE - Greece | `greece` | 0.1 | 0.21 |
| GUA | GUA - Guatemala | `centam` | 0.1 | 0.17 |
| GUY | GUY - Guyana | `caribbean` | 0.12 | 0.08 |
| GWA | GWA - Gwalior | `india` | 0.05 | 0.01 |
| GXI | GXI - Guangxi Clique | `qing` | 0.15 | 0.04 |
| HAI | HAI - Haiti | `haiti` | 0.05 | 0.07 |
| HAL | HAL - Hail | `arabia` | 0.03 | 0.025 |
| HAM | HAM - Hamburg | `north_german` | 0.5 | 0.69 |
| HAN | HAN - Hannover | `north_german` | 0.5 | 0.69 |
| HAW | HAW - Hawaii | `pacific_tribal` | 0.02 | 0.29 |
| HDJ | HDJ - Hedjaz | `arabia` | 0.03 | 0.025 |
| HDU | HDU - Hindustan | `india` | 0.05 | 0.03 |
| HEK | HEK - HesseKassel | `north_german` | 0.5 | 0.69 |
| HES | HES - HesseDarmstadt | `north_german` | 0.5 | 0.69 |
| HND | HND - India | `india` | 0.05 | 0.58 |
| HNN | HNN - Hunan | `qing` | 0.15 | 0.04 |
| HOL | HOL - Holstein | `north_german` | 0.5 | 0.8 |
| HON | HON - Honduras | `centam` | 0.1 | 0.17 |
| HRT | HRT - Herat | `centralasia` | 0.02 | 0.01 |
| HUI | HUI - Anhui | `qing` | 0.15 | 0.04 |
| HUN | HUN - Hungary | `hungary` | 0.22 | 0.25 |
| HYD | HYD - Hyderabad | `india` | 0.05 | 0.01 |
| HZJ | HZJ - Hazarajat | `centralasia` | 0.02 | 0.005 |
| IBR | IBR - Iberia | `iberia` | 0.2 | 0.13 |
| ICL | ICL - Iceland | `nordic` | 0.7 | 0.87 |
| IND | IND - Indore | `india` | 0.05 | 0.01 |
| INO | INO - Indonesia | `seasia` | 0.02 | 0.03 |
| ION | ION - Ionian Islands | `greece` | 0.1 | 0.21 |
| IRE | IRE - Ireland | `ireland` | 0.3 | 0.55 |
| IRQ | IRQ - Iraq | `ottoman_arab` | 0.05 | 0.26 |
| ISR | ISR - Israel | `ottoman_arab` | 0.05 | 0.87 |
| ITA | ITA - Italy | `italy_unified` | 0.2 | 0.28 |
| IVC | IVC - Ivory Coast | `africa` | 0.01 | 0.004 |
| JAI | JAI - Jaipur | `india` | 0.05 | 0.01 |
| JAL | JAL - Jallon | `africa_muslim` | 0.03 | 0.02 |
| JAM | JAM - Jamaica | `caribbean` | 0.12 | 0.15 |
| JAP | JAP - Japan | `japan` | 0.3 | 0.39 |
| JAS | JAS - Jaisalmer | `india` | 0.05 | 0.01 |
| JAV | JAV - Java | `seasia` | 0.02 | 0.03 |
| JOD | JOD - Jodhpur | `india` | 0.05 | 0.01 |
| JOH | JOH - Johore | `seasia` | 0.02 | 0.01 |
| JOR | JOR - Jordan | `ottoman_arab` | 0.05 | 0.08 |
| KAG | KAG - Kaga | `japan` | 0.3 | 0.39 |
| KAL | KAL - Kalat | `centralasia` | 0.02 | 0.01 |
| KAM | KAM - Far Eastern Federal District | `russia_frontier` | 0.03 | 0.01 |
| KAS | KAS - Kashmir | `india` | 0.05 | 0.01 |
| KAZ | KAZ - Kazakhstan | `centralasia` | 0.02 | 0.007 |
| KBO | KBO - Kanem-Bornu | `africa_muslim` | 0.03 | 0.003 |
| KCH | KCH - Kachin | `seasia` | 0.02 | 0.02 |
| KDH | KDH - Kandahar | `centralasia` | 0.02 | 0.005 |
| KDS | KDS - Kurdistan | `centralasia` | 0.02 | 0.14 |
| KHI | KHI - Khiva | `centralasia` | 0.02 | 0.01 |
| KHR | KHR - Khorasan | `persia` | 0.05 | 0.02 |
| KHZ | KHZ - Khuzestan | `persia` | 0.05 | 0.009 |
| KLM | KLM - Kalimantan | `seasia` | 0.02 | 0.02 |
| KMK | KMK - Kalmykia | `russia_frontier` | 0.03 | 0.28 |
| KMT | KMT - Nationalist China | `qing` | 0.15 | 0.05 |
| KNG | KNG - Kong | `africa_muslim` | 0.03 | 0.02 |
| KNY | KNY - Kenya | `africa` | 0.01 | 0.004 |
| KNZ | KNZ - Kunduz | `centralasia` | 0.02 | 0.009 |
| KOK | KOK - Kokand | `centralasia` | 0.02 | 0.01 |
| KON | KON - Kongo | `africa` | 0.01 | 0.01 |
| KOR | KOR - Korea | `korea` | 0.1 | 0.05 |
| KRA | KRA - Krakow | `poland` | 0.2 | 0.59 |
| KRL | KRL - Karelia | `russia` | 0.06 | 0.7 |
| KRN | KRN - Karnatak | `india` | 0.05 | 0.02 |
| KRT | KRT - Kaarta | `africa_muslim` | 0.03 | 0.003 |
| KTI | KTI - Kutai | `seasia` | 0.02 | 0.02 |
| KUB | KUB - Kuba | `africa` | 0.01 | 0.001 |
| KUK | KUK - Austria-Hungary | `habsburg_dual` | 0.28 | 0.25 |
| KUT | KUT - Kutch | `india` | 0.05 | 0.01 |
| KWT | KWT - Kuwait | `arabia` | 0.03 | 0.28 |
| KYR | KYR - Kyrgyzstan | `centralasia` | 0.02 | 0.01 |
| KZB | KZB - Kazembe | `africa` | 0.01 | 0.001 |
| LAD | LAD - Ladakh | `himalaya` | 0.02 | 0.01 |
| LAN | LAN - Lanfang | `seasia` | 0.02 | 0.02 |
| LAT | LAT - Latvia | `baltic_lutheran` | 0.4 | 0.6 |
| LBA | LBA - Luba | `africa` | 0.01 | 0.01 |
| LBN | LBN - Lebanon | `ottoman_christian` | 0.08 | 0.06 |
| LBY | LBY - Libya | `maghreb` | 0.03 | 0.03 |
| LIB | LIB - Liberia | `liberia` | 0.1 | 0.12 |
| LIP | LIP - Lippe | `north_german` | 0.5 | 0.69 |
| LIT | LIT - Lithuania | `eastern_catholic` | 0.12 | 0.6 |
| LNA | LNA - Lan Na | `seasia_buddhist` | 0.08 | 0.02 |
| LOA | LOA - Loango | `africa` | 0.01 | 0.0006 |
| LOM | LOM - Lombardia | `north_italy` | 0.25 | 0.4 |
| LOS | LOS - Los Altos | `latam_low` | 0.08 | 0.09 |
| LPL | LPL - La Plata | `latam_mid` | 0.12 | 0.12 |
| LSK | LSK - Alaska | `russia_frontier` | 0.03 | 0.1 |
| LUA | LUA - Luang Prabang | `seasia_buddhist` | 0.08 | 0.01 |
| LUB | LUB - Lubeck | `north_german` | 0.5 | 0.69 |
| LUC | LUC - Lucca | `north_italy` | 0.25 | 0.44 |
| LUN | LUN - Lunda | `africa` | 0.01 | 0.001 |
| LUX | LUX - Luxemburg | `france_belgium` | 0.42 | 0.6 |
| LUZ | LUZ - Luzica | `north_german` | 0.5 | 0.8 |
| LXA | LXA - Lan Xang | `seasia_buddhist` | 0.08 | 0.02 |
| MAD | MAD - Madagascar | `africa` | 0.01 | 0.03 |
| MAH | MAH - Maharashtra | `india` | 0.05 | 0.02 |
| MAJ | MAJ - Majeerteen | `horn` | 0.02 | 0.02 |
| MAK | MAK - Makran | `centralasia` | 0.02 | 0.01 |
| MAL | MAL - Maluku | `seasia` | 0.02 | 0.03 |
| MAN | MAN - Manhattan Commune | `usa_north` | 0.6 | 0.50 |
| MAS | MAS - Massina | `africa_muslim` | 0.03 | 0.006 |
| MAT | MAT - Matabele | `africa` | 0.01 | 0.01 |
| MCD | MCD - Macedonia | `balkan_ottoman` | 0.06 | 0.4 |
| MCK | MCK - Manchukuo | `qing` | 0.15 | 0.04 |
| MEC | MEC - Mecklenburg | `north_german` | 0.5 | 0.69 |
| MEI | MEI - Saxe | `north_german` | 0.5 | 0.69 |
| MEW | MEW - Mewar | `india` | 0.05 | 0.01 |
| MEX | MEX - Mexico | `latam_mid` | 0.12 | 0.14 |
| MGH | MGH - Maghreb | `maghreb` | 0.03 | 0.03 |
| MGL | MGL - Mongolia | `qing_frontier` | 0.03 | 0.03 |
| MLI | MLI - Mali | `africa_muslim` | 0.03 | 0.004 |
| MLT | MLT - Malta | `south_italy` | 0.12 | 0.28 |
| MLW | MLW - Malawi | `africa` | 0.01 | 0.004 |
| MLY | MLY - Malaya | `seasia` | 0.02 | 0.03 |
| MNG | MNG - Mongo | `africa` | 0.01 | 0.01 |
| MOD | MOD - Modena | `north_italy` | 0.25 | 0.44 |
| MOL | MOL - Moldavia | `balkan_ottoman` | 0.06 | 0.09 |
| MON | MON - Montenegro | `balkan_ottoman` | 0.06 | 0.09 |
| MOR | MOR - Morocco | `maghreb` | 0.03 | 0.09 |
| MOS | MOS - Mossi | `africa_muslim` | 0.03 | 0.01 |
| MOZ | MOZ - Mozambique | `africa` | 0.01 | 0.13 |
| MRT | MRT - Marathas | `india` | 0.05 | 0.02 |
| MRU | MRU - Maritime Union | `settler` | 0.5 | 0.6 |
| MTC | MTC - Metis Confederacy | `frontier_mixed` | 0.2 | 0.17 |
| MUG | MUG - Mughalistan | `india` | 0.05 | 0.03 |
| MYS | MYS - Mysore | `india` | 0.05 | 0.01 |
| NAG | NAG - Nagpur | `india` | 0.05 | 0.01 |
| NAL | NAL - Natalia | `boer` | 0.35 | 0.25 |
| NAS | NAS - Nassau | `north_german` | 0.5 | 0.79 |
| NEJ | NEJ - Nejd | `arabia` | 0.03 | 0.025 |
| NEN | NEN - New England | `usa_north` | 0.6 | 0.50 |
| NEP | NEP - Nepal | `himalaya` | 0.02 | 0.006 |
| NET | NET - Netherlands | `lowlands` | 0.55 | 0.82 |
| NEW | NEW - Newfoundland | `settler` | 0.5 | 0.6 |
| NGF | NGF - North German Fed | `north_german` | 0.5 | 0.87 |
| NGR | NGR - Nigeria | `africa` | 0.01 | 0.004 |
| NIC | NIC - Nicaragua | `centam` | 0.1 | 0.17 |
| NIG | NIG - Niger | `africa` | 0.01 | 0.004 |
| NOR | NOR - Norway | `nordic` | 0.7 | 0.69 |
| NPU | NPU - North Peru | `latam_low` | 0.08 | 0.1 |
| NYE | NYE - North Yemen | `arabia` | 0.03 | 0.025 |
| NZL | NZL - New Zealand | `settler` | 0.5 | 0.5 |
| OAX | OAX - Oaxaca | `latam_low` | 0.08 | 0.03 |
| OCC | OCC - Occitania | `france_periphery` | 0.3 | 0.48 |
| OLD | OLD - Oldenburg | `north_german` | 0.5 | 0.69 |
| OMA | OMA - Oman | `arabia` | 0.03 | 0.025 |
| ORA | ORA - Oranje | `boer` | 0.35 | 0.35 |
| ORI | ORI - Orissa | `india` | 0.05 | 0.01 |
| OYO | OYO - Oyo | `africa` | 0.01 | 0.002 |
| PAK | PAK - Pakistan | `india` | 0.05 | 0.02 |
| PAP | PAP - Papal States | `south_italy` | 0.12 | 0.34 |
| PAR | PAR - Parma | `north_italy` | 0.25 | 0.44 |
| PBC | PBC - Peru-Bolivian Confederation | `latam_low` | 0.08 | 0.1 |
| PER | PER - Persia | `persia` | 0.05 | 0.022 |
| PEU | PEU - Peru | `latam_low` | 0.08 | 0.09 |
| PHL | PHL - Philippines | `philippines` | 0.1 | 0.28 |
| PLC | PLC - Polish-Lithuanian Commonwealth | `poland` | 0.2 | 0.5 |
| PLS | PLS - Palestine | `ottoman_arab` | 0.05 | 0.08 |
| PML | PML - Pomerelia | `north_german` | 0.5 | 0.6 |
| PNJ | PNJ - Panjab | `india` | 0.05 | 0.04 |
| PNM | PNM - Panama | `latam_mid` | 0.12 | 0.25 |
| POL | POL - Poland | `poland` | 0.2 | 0.6 |
| PON | PON - Pontus | `greece` | 0.1 | 0.14 |
| POR | POR - Portugal | `portugal` | 0.15 | 0.12 |
| PRG | PRG - Paraguay | `latam_mid` | 0.12 | 0.09 |
| PRI | PRI - Puerto Rico | `caribbean` | 0.12 | 0.14 |
| PRU | PRU - Prussia | `prussia_saxony` | 0.55 | 0.785 |
| PTG | PTG - Patagonia | `latam_low` | 0.08 | 0.1 |
| PZN | PZN - Poznan | `poland` | 0.2 | 0.6 |
| QNG | QNG | `qing` | 0.15 | 0.045 |
| QUE | QUE - Quebec | `quebec` | 0.3 | 0.6 |
| RAJ | RAJ - Rajputana | `india` | 0.05 | 0.02 |
| REB | REB - Rebels | - | - | - |
| RGR | RGR - Rio Grande | `latam_low` | 0.08 | 0.1 |
| RGS | RGS - Rio Grande do Sul | `latam_mid` | 0.12 | 0.1 |
| RHI | RHI - Rhineland | `north_german` | 0.5 | 0.8 |
| RHO | RHO - Southern Rhodesia | `africa` | 0.01 | 0.2 |
| RMG | RMG - Romagna | `north_italy` | 0.25 | 0.45 |
| ROM | ROM - Romania | `balkan_ottoman` | 0.06 | 0.21 |
| RPL | RPL - Rupert's Land | `frontier_mixed` | 0.2 | 0.17 |
| RUS | RUS - Russia | `russia` | 0.06 | 0.085 |
| RUT | RUT - Ruthenia | `eastern_catholic` | 0.12 | 0.15 |
| RWA | RWA - Ruanda | `africa` | 0.01 | 0.001 |
| RYU | RYU - Ryukyu | `ryukyu` | 0.1 | 0.05 |
| SAA | SAA - Saar | `north_german` | 0.5 | 0.8 |
| SAF | SAF - South Africa | `boer` | 0.35 | 0.2 |
| SAK | SAK - Siak | `seasia` | 0.02 | 0.025 |
| SAR | SAR - Sardinia | `north_italy` | 0.25 | 0.44 |
| SAT | SAT - Satsuma | `japan` | 0.3 | 0.39 |
| SAX | SAX - Saxony | `prussia_saxony` | 0.55 | 0.69 |
| SCA | SCA - Scandinavia | `nordic` | 0.7 | 0.8 |
| SCH | SCH - Schleswig | `north_german` | 0.5 | 0.8 |
| SCO | SCO - Scotland | `britain` | 0.55 | 0.55 |
| SEG | SEG - Segu | `africa_muslim` | 0.03 | 0.003 |
| SEN | SEN - Sendai | `japan` | 0.3 | 0.39 |
| SER | SER - Serbia | `balkan_ottoman` | 0.06 | 0.09 |
| SGF | SGF - South German Fed | `south_german` | 0.35 | 0.87 |
| SHA | SHA - Shan | `seasia` | 0.02 | 0.02 |
| SHI | SHI - Shimla | `india` | 0.05 | 0.02 |
| SHO | SHO - Shona | `africa` | 0.01 | 0.003 |
| SHW | SHW - Shewa | `horn` | 0.02 | 0.01 |
| SIA | SIA - Siam | `seasia_buddhist` | 0.08 | 0.01 |
| SIB | SIB - Siberian Republic | `russia_frontier` | 0.03 | 0.01 |
| SIC | SIC - Two Sicilies | `south_italy` | 0.12 | 0.09 |
| SIE | SIE - Siebenburgen | `eastern_catholic` | 0.12 | 0.1 |
| SIK | SIK - Sikkim | `himalaya` | 0.02 | 0.006 |
| SIN | SIN - Sind | `india` | 0.05 | 0.01 |
| SLE | SLE - Sierra Leone | `africa` | 0.01 | 0.004 |
| SLO | SLO - Slovenia | `habsburg_dual` | 0.28 | 0.35 |
| SLS | SLS - Silesia | `north_german` | 0.5 | 0.8 |
| SLV | SLV - Slovakia | `hungary` | 0.22 | 0.65 |
| SLW | SLW - Sulawesi | `seasia` | 0.02 | 0.02 |
| SMI | SMI - Sapmi | `frontier_mixed` | 0.2 | 0.6 |
| SNG | SNG - Senegal | `africa` | 0.01 | 0.004 |
| SNZ | SNZ - South Island | `settler` | 0.5 | 0.5 |
| SOK | SOK - Sokoto | `africa_muslim` | 0.03 | 0.002 |
| SOM | SOM - Somalia | `horn` | 0.02 | 0.006 |
| SON | SON - Sonora | `latam_low` | 0.08 | 0.1 |
| SPA | SPA - Spain | `iberia` | 0.2 | 0.12 |
| SPC | SPC - Carlist Spain | `iberia` | 0.2 | 0.20 |
| SPU | SPU - South Peru | `latam_low` | 0.08 | 0.1 |
| SRD | SRD - Sardinia | `north_italy` | 0.25 | 0.45 |
| SRI | SRI - Sri Lanka | `india` | 0.05 | 0.02 |
| SUA | SUA - Suazi | `africa` | 0.01 | 0.002 |
| SUD | SUD - Sudan | `africa_muslim` | 0.03 | 0.01 |
| SUL | SUL - Sulu | `seasia` | 0.02 | 0.02 |
| SVY | SVY - Savoy | `north_italy` | 0.25 | 0.45 |
| SWE | SWE - Sweden | `nordic` | 0.7 | 0.69 |
| SWH | SWH - Schleswig-Holstein | `north_german` | 0.5 | 0.69 |
| SWI | SWI - Switzerland | `lowlands` | 0.55 | 0.64 |
| SWK | SWK - Sarawak | `seasia` | 0.02 | 0.02 |
| SXI | SXI - Shanxi | `qing` | 0.15 | 0.04 |
| SYL | SYL - Transylvania | `eastern_catholic` | 0.12 | 0.1 |
| SYR | SYR - Syria | `ottoman_arab` | 0.05 | 0.08 |
| SZC | SZC - Sichuan | `qing` | 0.15 | 0.04 |
| TAI | TAI - Taiwan | `qing` | 0.15 | 0.03 |
| TAJ | TAJ - Tajikstan | `centralasia` | 0.02 | 0.01 |
| TAR | TAR - Tatarstan | `russia` | 0.06 | 0.1 |
| TCA | TCA - Transcaucasia | `caucasus` | 0.04 | 0.1 |
| TEX | TEX - Texas | `usa_south` | 0.35 | 0.50 |
| TGA | TGA - Tonga | `pacific_tribal` | 0.02 | 0.80 |
| TIB | TIB - Tibet | `qing_frontier` | 0.03 | 0.007 |
| TIG | TIG - Tigray | `horn` | 0.02 | 0.025 |
| TKG | TKG - Shogunate Japan | `japan` | 0.3 | 0.39 |
| TKM | TKM - Turkmenistan | `centralasia` | 0.02 | 0.02 |
| TKS | TKS - Turkestan | `centralasia` | 0.02 | 0.01 |
| TNT | TNT - Tannu Tuva | `qing_frontier` | 0.03 | 0.28 |
| TNZ | TNZ - Tanzania | `africa` | 0.01 | 0.004 |
| TOG | TOG - Togo | `africa` | 0.01 | 0.004 |
| TOO | TOO - Tooro | `africa` | 0.01 | 0.002 |
| TOS | TOS - Tosa | `japan` | 0.3 | 0.39 |
| TOU | TOU - Toucouleur | `africa_muslim` | 0.03 | 0.004 |
| TPG | TPG - Taiping | `qing` | 0.15 | 0.05 |
| TRA | TRA - Travancore | `india` | 0.05 | 0.01 |
| TRE | TRE - Trieste | `habsburg_dual` | 0.28 | 0.25 |
| TRI | TRI - Tripoli | `maghreb` | 0.03 | 0.02 |
| TRN | TRN - Transvaal | `boer` | 0.35 | 0.35 |
| TRZ | TRZ - Trarza | `africa_muslim` | 0.03 | 0.02 |
| TSW | TSW - Botswana | `africa` | 0.01 | 0.003 |
| TTB | TTB - Trinidad & Tobago | `caribbean` | 0.12 | 0.15 |
| TUN | TUN - Tunis | `maghreb` | 0.03 | 0.025 |
| TUR | TUR - Ottoman Empire | `ottoman` | 0.05 | 0.19 |
| TUS | TUS - Tuscany | `north_italy` | 0.25 | 0.44 |
| UAL | UAL - Alabama | `usa_south` | 0.35 | 0.50 |
| UAR | UAR - Arkansas | `usa_south` | 0.35 | 0.50 |
| UBD | UBD - United Baltic Provinces | `baltic_lutheran` | 0.4 | 0.6 |
| UCA | UCA - United States of Central America | `centam` | 0.1 | 0.09 |
| UFL | UFL - Florida | `usa_south` | 0.35 | 0.50 |
| UGA | UGA - Georgia | `usa_south` | 0.35 | 0.50 |
| UIA | UIA - Iowa | `usa_north` | 0.6 | 0.50 |
| UIL | UIL - Illinois | `usa_north` | 0.6 | 0.50 |
| UIN | UIN - Indiana | `usa_north` | 0.6 | 0.50 |
| UKR | UKR - Ukraine | `russia` | 0.06 | 0.15 |
| UKY | UKY - Kentucky | `usa_south` | 0.35 | 0.50 |
| ULA | ULA - Louisiana | `usa_south` | 0.35 | 0.50 |
| UMI | UMI - Michigan | `usa_north` | 0.6 | 0.50 |
| UMN | UMN - Minnesota | `usa_north` | 0.6 | 0.50 |
| UMO | UMO - Missouri | `usa_south` | 0.35 | 0.50 |
| UMS | UMS - Mississippi | `usa_south` | 0.35 | 0.50 |
| UNB | UNB - Nebraska | `usa_north` | 0.6 | 0.50 |
| UNC | UNC - North Carolina | `usa_south` | 0.35 | 0.50 |
| UNJ | UNJ - New Jersey | `usa_north` | 0.6 | 0.50 |
| UNM | UNM - New Mexico | `latam_low` | 0.08 | 0.50 |
| UNY | UNY - New York | `usa_north` | 0.6 | 0.50 |
| UOH | UOH - Ohio | `usa_north` | 0.6 | 0.50 |
| UOR | UOR - Oregon | `usa_north` | 0.6 | 0.6 |
| UPA | UPA - Pennsylvania | `usa_north` | 0.6 | 0.50 |
| UPB | UPB - Portugal-Brazil | `portugal` | 0.15 | 0.12 |
| URA | URA - Ural Republic | `russia` | 0.06 | 0.01 |
| URU | URU - Uruguay | `latam_mid` | 0.12 | 0.09 |
| USA | USA - USA | `usa` | 0.55 | 0.49 |
| USC | USC - South Carolina | `usa_south` | 0.35 | 0.50 |
| UTN | UTN - Tennessee | `usa_south` | 0.35 | 0.50 |
| UVA | UVA - Virginia | `usa_south` | 0.35 | 0.50 |
| UWI | UWI - Wisconsin | `usa_north` | 0.6 | 0.50 |
| UWV | UWV - West Virginia | `usa_south` | 0.35 | 0.50 |
| UYG | UYG - Uyghurstan | `qing_frontier` | 0.03 | 0.02 |
| UZB | UZB - Uzbekistan | `centralasia` | 0.02 | 0.01 |
| VEN | VEN - Venice | `north_italy` | 0.25 | 0.4 |
| VNZ | VNZ - Venezuela | `latam_mid` | 0.12 | 0.11 |
| WAD | WAD - Wadai | `africa_muslim` | 0.03 | 0.003 |
| WAL | WAL - Wallachia | `balkan_ottoman` | 0.06 | 0.09 |
| WEI | WEI - Saxe | `north_german` | 0.5 | 0.69 |
| WES | WES - Westfalen | `north_german` | 0.5 | 0.8 |
| WHA | WHA - Wales | `britain` | 0.55 | 0.55 |
| WIA | WIA - Wiang Chhan | `seasia_buddhist` | 0.08 | 0.01 |
| WLL | WLL - Wallonia | `france_belgium` | 0.42 | 0.28 |
| WOL | WOL - Wolof | `africa_muslim` | 0.03 | 0.002 |
| WRI | WRI - Warri | `africa` | 0.01 | 0.002 |
| WUR | WUR - Wurttemberg | `south_german` | 0.35 | 0.64 |
| XBI | XBI - Xibei San Ma | `qing` | 0.15 | 0.04 |
| XHO | XHO - Xhosa | `africa` | 0.01 | 0.002 |
| XIN | XIN - Xinjiang | `qing_frontier` | 0.03 | 0.04 |
| YAK | YAK - Yakutia-Sakha | `russia_frontier` | 0.03 | 0.01 |
| YEM | YEM - Yemen | `arabia` | 0.03 | 0.03 |
| YNN | YNN - Yunnan | `qing` | 0.15 | 0.04 |
| YUC | YUC - Yucatan | `latam_low` | 0.08 | 0.1 |
| YUG | YUG - Yugoslavia | `balkan_ottoman` | 0.06 | 0.28 |
| YZW | YZW - Yonezawa | `japan` | 0.3 | 0.39 |
| ZAM | ZAM - Zambia | `africa` | 0.01 | 0.004 |
| ZAN | ZAN - Zanzibar | `africa_muslim` | 0.03 | 0.04 |
| ZUL | ZUL - Zulu | `africa` | 0.01 | 0.01 |

## Known soft spots

- **`dynamic` (D01-D50) 0.10** is a placeholder. These are release/dominion shells with
  no capital; they never exist at the 1821 start, so any value is arbitrary.
- **`usa_north` 0.60 vs `usa` 0.55 vs `usa_south` 0.35.** The single `USA` tag has to be
  one number, so it carries the blend; the state release tags carry the real regional
  split. A CSA released early therefore drops from 0.55 to 0.35, which is intended.
- **`frontier_mixed` 0.20** (`MTC`, `RPL`, `SMI`) and **`pacific_tribal` 0.02**
  (`AIN`, `AOT`, `CHE`, `FIJ`, `TGA`, `HAW`) are the weakest evidence in the table;
  mission schooling in all of these was only starting in the 1820s.
- **`seasia_buddhist` 0.08** (Burma, Siam, the Lao states) is deliberately above the
  rest of South-East Asia: Theravada monastery schooling gave those societies male
  literacy far above their neighbours, which surprises people reading the table.
- **`PZN` (Poznan) 0.20** is filed under `poland` rather than `north_german` even though
  it was under Prussian school administration, because the population was Polish
  peasantry. `DZG` (Danzig) and `SLS` (Silesia) go the other way, at 0.50.
