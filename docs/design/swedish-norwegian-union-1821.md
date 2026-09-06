# Swedish-Norwegian Union Consolidation & Constitutional Crises (1821-1836)

## Historical Context

The personal union between Sweden and Norway, created by the Treaty of Kiel and ratified by the Norwegian Storting in November 1814 under the Riksakt, was a dual monarchy with a shared king and foreign policy, but separate constitutions, laws, armies, navies, and currencies. The King of Sweden and Norway, Karl XIV Johan (the former Napoleonic Marshal Jean-Baptiste Bernadotte), held only a suspensive veto over Norwegian legislation: a bill passed unchanged by three successive Stortings became law even without the royal signature (Section 79 of the Constitution of Eidsvoll).

Throughout the 1820s and 1830s, Karl Johan repeatedly attempted to amalgamate the two kingdoms and expand royal prerogative, only to be rebuffed by the Norwegian Storting in a sequence of dramatic constitutional confrontations:

1. **The Abolition of Nobility (*Adelsloven*, 1821)**: In 1821, the Storting passed the abolition of hereditary nobility for the third time. Furious, Karl Johan assembled a military encampment of 6,000 Swedish and Norwegian soldiers at Etterstad outside Christiania and stationed warships in the fjord to coerce parliament. The Storting stood firm, and Karl Johan was forced to sign the law.
2. **Constitution Day & The 17th of May (1824-1828)**: The commemoration of the 17 May 1814 Eidsvoll Constitution became the rallying cry of Norwegian national consciousness. Karl Johan viewed it as an anti-Swedish demonstration and banned all public festivities.
3. **The Battle of the Square (*Torvslaget*, 17 May 1829)**: In Christiania, citizens gathered peacefully in the central square singing patriotic anthems. Swedish Governor-General (Statholder) Baltzar von Platen sent cavalry with drawn sabres into the crowd. The outcry, spearheaded by poet Henrik Wergeland, discredited Swedish viceregal rule.
4. **The Viceroyalty Dilemma (*Statholderstriden*)**: Following von Platen's death in late 1829, Karl Johan left the office of Governor-General vacant rather than provoke further riots, eventually appointing a Norwegian magnate (Count Herman Wedel-Jarlsberg in 1836).
5. **The 1836 Storting Dissolution Crisis (*Statskupp-forsøket*)**: In July 1836, to block local municipal democracy (*Formannskapslovene*) and customs reform, Karl Johan abruptly dissolved the Storting. The Storting responded by impeaching Prime Minister Severin Løvenskiold before the *Riksrett* (Court of Impeachment) for counter-signing the unconstitutional decree. Karl Johan yielded, accepted the verdict, summoned an extraordinary Storting, and confirmed Norwegian parliamentary liberties.

## Event Structure

- **ID Range**: `1003400-1003405` in `events/GVG Event IDs.txt`
- **File**: `CoE_RoI_R/events/SWENorwayGVG.txt`
- **Localisation**: `CoE_RoI_R/localisation/GVG_norway_union.csv`
- **New Modifier**: `norwegian_constitutional_spirit` in `common/event_modifiers.txt`

| ID | Title | Actor | Date / Trigger | Summary |
|---|---|---|---|---|
| `1003400` | The Abolition of the Norwegian Nobility | SWE | 1821, NOR vassal | Storting passes Adelsloven over royal veto. Karl Johan's Etterstad demonstration; accept (A) or escalate (B). |
| `1003401` | Constitution Day and the 17th of May | NOR | 1824-1828, vassal of SWE | Norwegians celebrate 17 May. Karl Johan issues a ban. Defy (A) or comply (B). |
| `1003402` | The Battle of the Square (Torvslaget) | NOR | 1829.05 | Governor-General von Platen sends cavalry into Christiania crowds. Wergeland's fury; national outrage. |
| `1003403` | The Viceroyalty Dilemma | SWE | 1829-1833, after Torvslaget | Leave post vacant (A), appoint a Norwegian viceroy (B), or maintain a Swedish magnate (C). |
| `1003404` | The Storting Dissolution Crisis of 1836 | SWE | 1836 | Karl Johan dissolves the Storting; Storting impeaches PM Løvenskiold in the Riksrett. King yields (A) or fights (B). |
| `1003405` | The Constitutional Settlement of 1836 | NOR | 1836, after resolution | Autonomy affirmed; municipal democracy paved; `norwegian_constitutional_spirit` granted. |

## Scripting Safeguards
- Tag checks: SWE (Sweden) and NOR (Norway).
- Province checks: Christiania (Oslo) = 313, Stockholm = 322.
- Verified in `definition.csv`.
