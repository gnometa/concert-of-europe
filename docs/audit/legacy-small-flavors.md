# Legacy audit: Small flavour files

Scope: `events/DANFlavor.txt`, `events/BAYFlavor.txt`, `events/SWIFlavor.txt`, `events/PAPFlavor.txt`,
`events/PEUFlavor.txt`, `events/URUFlavor.txt`, `events/HAIFlavor.txt`, `events/DOMFlavor.txt`,
`events/LANFlavour.txt`, `events/SWEFlavor.txt`, `events/NORFlavor.txt`, `events/BADFlavor.txt`,
`events/SAXFlavor.txt`, `events/COBFlavor.txt`, `events/NASFlavor.txt`, `events/HAMFlavor.txt`,
`events/FRMFlavor.txt`, `events/ANHFlavor.txt`, `events/OLDFlavor.txt`, `events/HEKFlavor.txt`,
`events/HEDFlavor.txt`, `events/TURFlavor.txt`, `events/PBCFlavor.txt`.

## Fixed

| file | line | id | problem | fix |
|---|---|---|---|---|
| URUFlavor.txt | 182, 183, 187, 226 | 46411, 46412 | **[high]** Relation values of -400 and +400 with ARG and URU exceed the engine signed-integer clamp of -200..200. | Clamped to -200 and +200. |
| PBCFlavor.txt | 108 | 97041 | **[high]** Relation value of 400 with PEU exceeds the engine clamp of -200..200. | Clamped to 200. |
| PBCFlavor.txt | 466 | 97047 | **[high]** Relation value of 300 with neighboring nations exceeds the engine clamp of -200..200. | Clamped to 200. |
| DANFlavor.txt | 1055 | 36217 | **[medium]** Option A text key `EVTOPTA36217` missing in all localisation CSVs; displayed raw tag in game. | Added definition to `GVG_flavor_repairs.csv`. |
| DANFlavor.txt | 1093-1098 | 36218 | **[medium]** Tivoli Gardens event title, desc, and option text keys (`EVTNAME36218`, `EVTDESC36218`, `EVTOPTA36218`) unlocalised across all CSVs. | Added full text definitions to `GVG_flavor_repairs.csv`. |
| DANFlavor.txt | 1141-1146 | 36219 | **[medium]** Rødding Folk High School event keys (`EVTNAME36219`, `EVTDESC36219`, `EVTOPTA36219`) unlocalised across all CSVs. | Added full text definitions to `GVG_flavor_repairs.csv`. |
| DANFlavor.txt | 1195-1200 | 36220 | **[medium]** Georg Brandes Modern Breakthrough event keys (`EVTNAME36220`, `EVTDESC36220`, `EVTOPTA36220`) unlocalised across all CSVs. | Added full text definitions to `GVG_flavor_repairs.csv`. |
| DOMFlavor.txt | 41-46 | 45006 | **[medium]** Dominican bankruptcy event keys (`EVTNAME45006`, `EVTDESC45006`, `EVTOPTA45006`) unlocalised across all CSVs. | Added full text definitions to `GVG_flavor_repairs.csv`. |
| ANHFlavor.txt | 5, 39-44 | 48300 | **[medium]** Anhalt reunification event and news keys (`EVTNAME48300`, `EVTDESC48300`, `EVTOPTA48300`, and all four `NEWS_*` keys) unlocalised across all CSVs. | Added full text and news definitions to `GVG_flavor_repairs.csv`. |

## Checked and found sound

* **DANFlavor 36207 trigger.** `vote_franschise = universal_voting` sits inside a `NOT = { ... }` condition block, which is valid engine condition syntax (unlike the effect error previously found in CLMFlavor).
* **MozartFest1838 flags in German minors.** `BADFlavor.txt:56`, `BAYFlavor.txt:212`, `NASFlavor.txt:12`, `HEKFlavor.txt:12`, `HEDFlavor.txt:12` share the flag `MozartFest1838` to coordinate the 1838 festival attendance and reaction. Each tag carries its own distinct trigger and options.
* **Louis Napoleon crisis in Switzerland (SWIFlavor 36000).** Triggers, `leave_alliance`, and France's reaction chain execute with valid scopes.
* **Swedish and Norwegian cultural events.** Bellman, Berzelius, Jenny Lind, Munch, Ibsen chains verified for scope integrity and dates.
