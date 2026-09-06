# Rhenish Industrial Take-off & Early German Railways (1826-1838)

## Historical Context

While the German Confederation of 1815 was initially an agrarian patchwork of small sovereign states dominated by Austrian diplomacy and Prussian military power, the 1820s and 1830s witnessed the quiet emergence of a technological and commercial revolution in western Germany:

1. **Krupp's Cast Steel Foundry (*Gussstahlfabrik*, Essen, 1826)**: In 1826, Friedrich Krupp died leaving an indebted workshop of seven workers in Essen. His 14-year-old son, Alfred Krupp, guided by his mother Therese, mastered crucible cast-steel metallurgy. Krupp's flawless cast-steel rollers and precision machinery established Essen as the metallurgical center of the Ruhr valley.
2. **The Bavarian Ludwigsbahn & The Locomotive *Der Adler* (December 1835)**: On 7 December 1835, Germany's first steam-powered railway opened between Nuremberg and Fürth in Bavaria. Propelled by the British-built locomotive *Der Adler* (The Eagle), the line ignited "railway fever" (*Eisenbahnfieber*) across the German states, proving the commercial viability of passenger steam rail.
3. **Deep-Shaft Mining in the Ruhr (1834-1838)**: Traditional coal extraction had been restricted to drift mines south of the Ruhr river. In the 1830s, industrialists Franz Haniel and Heinrich Huyssen (founders of the Gutehoffnungshütte in Oberhausen) successfully sank shafts through the thick marl layer (*Mergeldecke*) into the rich bituminous and coking coal basins to the north, utilizing high-pressure steam pumping engines.
4. **The Prussian Railway Law of 1838 (*Preußisches Eisenbahngesetz*)**: Following the opening of the Berlin-Potsdam Railway (1838) and the chartering of the Rhenish Railway Company (Cologne to Aachen and the Belgian border), Prussia enacted the landmark Railway Law of 3 November 1838. Drafted under Karl von Altenstein and Friedrich von Staegemann, the law provided private joint-stock corporations with secure rights-of-way, expropriation powers, and tariff freedom, while securing state inspection and mail/military conveyance, sparking the German railway boom.
5. **Rhenish Joint-Stock Finance**: The capital demands of railways and deep mining gave birth to modern German investment banking in Cologne and Aachen, led by figures like Ludolf Camphausen, David Hansemann, and Abraham Schaaffhausen (*A. Schaaffhausen'scher Bankverein*). This rising Rhenish industrial bourgeoisie became the economic backbone of the Zollverein and the leading political force of German constitutional liberalism.

## Event Structure

- **ID Range**: `1003700-1003704` in `events/GVG Event IDs.txt`
- **File**: `CoE_RoI_R/events/PRUIndustryGVG.txt`
- **Localisation**: `CoE_RoI_R/localisation/GVG_rhenish_industry.csv`
- **New Modifier**: `rhenish_heavy_industry` in `common/event_modifiers.txt`

| ID | Title | Actor | Date / Trigger | Summary |
|---|---|---|---|---|
| `1003700` | Krupp's Cast Steel Works in Essen | PRU | 1826, owns 578 | Crucible cast-steel foundry in Essen under young Alfred Krupp; metallurgical precision. |
| `1003701` | The Iron Way: The Bavarian Ludwigsbahn | BAV | 1835.12 | First steam railway between Nuremberg and Fürth; locomotive *Der Adler*; railway fever. |
| `1003702` | The Prussian Railway Law of 1838 | PRU | 1838 | Landmark statute regulating private joint-stock rail; spurs infrastructure boom; `rhenish_heavy_industry`. |
| `1003703` | Deep-Shaft Mining in the Ruhr Basin | PRU | 1834-1838, owns 578 | Penetration of the marl cover; steam pumps; Gutehoffnungshütte; rich coking coal unlocked. |
| `1003704` | Rhenish Joint-Stock Finance in Cologne | PRU | 1836-1838, owns 575 | Cologne merchant bankers (Camphausen, Hansemann, Schaaffhausen); corporate industrial credit. |

## Scripting Safeguards
- Tags: PRU (Prussia), BAV (Bavaria).
- Provinces: Cologne 575, Aachen 576, Dusseldorf/Ruhr 578, Nuremberg 595.
- Checked against `definition.csv`.
