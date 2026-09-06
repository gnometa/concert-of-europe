# First Central American Civil War & Liberal Reforms (1826-1838)

## Historical Context

Following the collapse of Agustín de Iturbide's First Mexican Empire in 1823, the former Captaincy-General of Guatemala declared independence on 1 July 1823 as the Federal Republic of Central America (*Provincias Unidas del Centro de América*, later *República Federal de Centro América*), encompassing Guatemala, El Salvador, Honduras, Nicaragua, and Costa Rica.

However, the federation was crippled by deep structural conflicts: the commercial and clerical elite of Guatemala City sought a centralized conservative state, whereas the provincial elites of El Salvador, Honduras, and Nicaragua championed federalism, anticlericalism, and free trade.

1. **The Federal Rupture (1826)**: In 1825, Manuel José Arce was elected first Federal President. In 1826, Arce betrayed his liberal supporters and allied with the conservative Aycinena clan and the Church in Guatemala City. He dissolved the federal congress and deposed the liberal governor of Guatemala, sparking open rebellion in El Salvador and Honduras.
2. **The First Civil War & Rise of Morazán (1826-1829)**: The provincial liberals rallied behind 35-year-old Honduran general Francisco Morazán. At the Battle of La Trinidad (November 1827) and Gualcho (1828), Morazán's *Ejército Protector de la Ley* routed the federal forces. In April 1829, Morazán besieged and entered Guatemala City, expelling Arce, the conservative oligarchy, and Archbishop Ramón Casaus y Torres into foreign exile.
3. **The Morazán Reforms (1830-1835)**: Elected Federal President in 1830, Morazán moved the capital to San Salvador in 1834. He implemented radical Enlightenment reforms: the abolition of ecclesiastical tithes, the confiscation of religious estates, freedom of worship, civil marriage, the secularisation of education, British commercial concessions, and the introduction of the Livingston legal code with trial by jury.
4. **Carrera's Peasant Rebellion & Cholera (1837)**: The introduction of direct head taxes and the Livingston code alienated the indigenous majority. In 1837, the second Asiatic cholera pandemic struck. Conservative priests preached that the liberal government was poisoning wells to exterminate indigenous people. Rafael Carrera, a 23-year-old former soldier and pig driver, organized the rural masses under the banner "Viva la religión y mueran los extranjeros!".
5. **The Dissolution of the Federation (1838-1839)**: Carrera's forces seized Guatemala City. On 30 May 1838, the Federal Congress declared each state sovereign and free to govern itself. Nicaragua, Honduras, Costa Rica, and Guatemala formally seceded. Morazán made a valiant final stand in 1839 before going into exile in Panama, ending the dream of a united Central America.

## Event Structure

- **ID Range**: `1003600-1003605` in `events/GVG Event IDs.txt`
- **File**: `CoE_RoI_R/events/USCACivilWarGVG.txt`
- **Localisation**: `CoE_RoI_R/localisation/GVG_central_america.csv`
- **New Modifier**: `morazan_reforms` in `common/event_modifiers.txt`

| ID | Title | Actor | Date / Trigger | Summary |
|---|---|---|---|---|
| `1003600` | The Federal Rupture | UCA | 1826 | Arce dissolves Congress and aligns with Guatemalan conservatives. Civil war erupts. |
| `1003601` | The Rise of Francisco Morazán | UCA | 1827 | Battle of La Trinidad; Morazán organizes the Army Protector of the Law. |
| `1003602` | The Fall of Guatemala City | UCA | 1829.04 | Morazán captures the capital; expulsion of Arce and Archbishop Casaus. |
| `1003603` | Morazán's Liberal Reforms | UCA | 1830-1835 | Secularization, religious freedom, Livingston code, education. |
| `1003604` | The Cholera Outbreak & Carrera's Revolt | UCA | 1837 | Cholera pandemic blamed on liberals; Rafael Carrera leads the indigenous peasant uprising. |
| `1003605` | The Disintegration of the Federal Republic | UCA | 1838-1839 | Congress permits secession; collapse into Guatemala, El Salvador, Honduras, Nicaragua, Costa Rica. |

## Scripting Safeguards
- Tag checks: UCA, GUA, ELS, HON, NIC, COS.
- Province IDs from `map/definition.csv`: Guatemala 2186, San Salvador 2191, Comayagua 2193, Managua 2197, San Jose 2201.
- Interlocks cleanly with `events/USCAFlavor.txt:97550-97560`.
