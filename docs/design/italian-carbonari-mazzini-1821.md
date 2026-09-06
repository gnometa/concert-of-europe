# Italian Risings, Carbonari & Young Italy (1821-1834)

## Historical Context

Following the defeat of the 1820-1821 constitutional revolutions in Naples and Piedmont by Austrian intervention forces authorized at the Congress of Laibach, the Italian peninsula entered a decade of intense Austrian military surveillance and absolutist restoration. Austrian occupation corps remained in the Kingdom of the Two Sicilies until 1827 and in Piedmont until 1823. King Carlo Felice of Sardinia and King Ferdinand I of Two Sicilies purged liberal officers, judges, and educators. Prominent patriots such as Santorre di Santa Rosa fled into exile, with Santa Rosa dying heroically in May 1825 on the Greek island of Sphacteria fighting Ibrahim Pasha's Egyptian forces.

In Austrian-ruled Lombardy-Venetia, the police dismantled the *Federati* and *Carbonari* networks, staging the show trials of Count Federico Confalonieri, Piero Maroncelli, and writer Silvio Pellico. Sentenced to harsh confinement in the fortress prison of the Spielberg in Moravia, Pellico survived to publish *Le mie prigioni* (*My Prisons*) in 1832 in Turin. The unvarnished, compassionate account of his suffering caused a sensation throughout Europe, inflicting immense diplomatic damage on Austrian moral authority in Italy.

The failure of the 1831 Central Italian revolutions (Modena, Parma, and the Papal Legations) convinced young patriots that the Carbonari's conspiratorial secrecy, elitism, reliance on foreign princes, and regional fragmentation were fatally flawed. In July 1831, in exile in Marseille, the 26-year-old Genoese lawyer Giuseppe Mazzini founded *La Giovine Italia* (Young Italy). Rejecting secret codes in favor of open propaganda, Mazzini demanded a united, independent, and democratic Italian Republic ("One, Free, Independent, Republican Nation").

Young Italy spread with unprecedented speed among students, junior army officers, and urban artisans. In 1833, a widespread military conspiracy was uncovered in the Royal Sardinian Army across Genoa, Alessandria, and Chambery; King Carlo Alberto ordered twelve executions, while dozens were sentenced to death in absentia. In February 1834, Mazzini organized a disastrous armed incursion into Savoy from Switzerland led by General Girolamo Ramorino, accompanied by an abortive mutiny in the port of Genoa. A young sailor from Nice named Giuseppe Garibaldi was condemned to death in absentia and fled across the Atlantic to Brazil and Uruguay.

While Mazzini's early insurrections collapsed, they fundamentally created the modern national movement, shifting Italian debate toward unity and setting the stage for both the 1848 revolutions and the moderate Neo-Guelph movement.

## Event Structure

- **ID Range**: `1003500-1003505` in `events/GVG Event IDs.txt`
- **File**: `CoE_RoI_R/events/ITAMazziniGVG.txt`
- **Localisation**: `CoE_RoI_R/localisation/GVG_young_italy.csv`
- **New Modifier**: `giovine_italia` in `common/event_modifiers.txt`

| ID | Title | Actor | Date / Trigger | Summary |
|---|---|---|---|---|
| `1003500` | The Austrian Garrison in the Peninsula | SAR / SIC | 1821-1823 | Aftermath of 1821 revolts; Austrian garrison; royal purge of constitutionalists. |
| `1003501` | The Spielberg Trials and Silvio Pellico | AUS | 1832 | Publication of *Le mie prigioni*; moral blow to Austrian hegemony in Italy. |
| `1003502` | Giuseppe Mazzini Founds La Giovine Italia | Italian minors / SAR | 1831.07 | Foundation of Young Italy in Marseille; republican national program. |
| `1003503` | The Conspiracy in the Sardinian Army | SAR | 1833 | Mazzinian infiltration of garrison troops in Genoa and Alessandria; executions. |
| `1003504` | The Invasion of Savoy and Garibaldi's Flight | SAR | 1834.02 | Abortive invasion under Ramorino; Garibaldi condemned to death, flees to South America. |
| `1003505` | The Awakening of the Risorgimento | Italian tags | 1835-1836 | From clandestine plots to national consciousness; `giovine_italia` modifier. |

## Scripting Safeguards
- Culture check: `is_culture_group = italian`.
- Tags: SAR, SIC, AUS, PAP, TUS, MOD, PAR, LUC.
- Provinces: Milan 726, Turin 720, Genoa 724, Chambery 466, Nice 472.
