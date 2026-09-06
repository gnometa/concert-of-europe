# Egyptian Morea Expedition & Battle of Navarino (1824-1828)

## Historical Context

In early 1824, after three years of Greek insurgency had paralyzed Ottoman forces in the Balkans, Sultan Mahmud II swallowed his pride and appealed to his nominally vassal viceroy, Muhammad Ali Pasha of Egypt. Muhammad Ali possessed the only modern military force in the empire: a French-trained army of Egyptian conscripts (the *Nizam-i Jedid*, drilled by Colonel Octave-Joseph Anthelme Sève, later Süleyman Pasha) and a modern fleet built at Alexandria, Marseille, and Venice.

In exchange for Egyptian intervention, Mahmud II promised Muhammad Ali the pashaliks of the Morea (Peloponnese) and Crete, with hints of Syria. In February 1825, an Egyptian expeditionary corps of 17,000 men under Muhammad Ali's son, Ibrahim Pasha, landed at Methoni (Modon) in the southwestern Peloponnese. Ibrahim's modernized army routed the Greek klephtic and irregular forces, recaptured Navarino, ravaged the interior, and in April 1826 captured the strategic bastion of Missolonghi after a year-long siege whose desperate breakout (*exodos*) shocked European Philhellenic opinion. In 1827, Ibrahim captured Athens and the Acropolis.

The devastation and impending extermination or enslavement of the Greek population compelled Britain, France, and Russia to sign the Treaty of London (6 July 1827), demanding an armistice and autonomy for Greece. When Ibrahim Pasha and Ibrahim's Ottoman superiors refused, a combined Allied fleet under Vice-Admiral Sir Edward Codrington, Rear-Admiral Henri de Rigny, and Rear-Admiral Login Geiden sailed into Navarino Bay on 20 October 1827. A tense standoff erupted into battle; in four hours, the Allied battle line annihilated the Ottoman-Egyptian fleet, sinking over 60 warships and killing 4,000 sailors without losing a single ship of their own.

Following Navarino, France dispatched the Maison Expedition (1828) with 14,000 troops to secure the Peloponnese. Cut off from naval supply, Ibrahim Pasha concluded the Alexandria Convention with Codrington and evacuated his surviving troops back to Egypt.

The diplomatic aftermath was toxic: Muhammad Ali had spent a fortune in treasure, lost his modern navy, and gained neither Morea (which became independent Greece) nor Syria (which Mahmud II refused to concede, offering only Crete). This grievance was the direct seed of Muhammad Ali's 1831 invasion of Syria, initiating the Egyptian-Ottoman Wars (Oriental Crisis).

## Event Structure

- **ID Range**: `1003300-1003306` in `events/GVG Event IDs.txt`
- **File**: `CoE_RoI_R/events/EGYMoreaGVG.txt`
- **Localisation**: `CoE_RoI_R/localisation/GVG_morea.csv`
- **New Modifier**: `egyptian_syrian_ambition` in `common/event_modifiers.txt`

| ID | Title | Actor | Date / Trigger | Summary |
|---|---|---|---|---|
| `1003300` | The Sultan's Appeal for the Morea | EGY | 1824+, TUR at war with GRE | Mahmud II promises Morea and Crete for intervention. EGY accepts (A), demands Syria upfront (B), or declines (C). |
| `1003301` | Ibrahim Pasha Lands at Methoni | EGY | 1825+, has `egypt_morea_expedition` | Egyptian regular army lands in the Peloponnese. Military experience gained; Greek unrest spikes. |
| `1003302` | The Fall of Missolonghi | GRE / TUR / EGY | April 1826 | The sortie of Missolonghi. Sets `fall_of_missolonghi`; European Philhellenism rises, Great Power relations drop. |
| `1003303` | The Treaty of London | ENG / FRA / RUS | 1827+ | Allied powers demand armistice and Greek autonomy. Choice to enforce mediation by naval force. |
| `1003304` | The Battle of Navarino | EGY (news to all) | 1827.10 | Allied fleet destroys Ottoman-Egyptian armada. Catastrophic naval losses; major world news. |
| `1003305` | The Maison Expedition and Evacuation | EGY / FRA / GRE | 1828+ | French troops land in Morea; Ibrahim Pasha signs evacuation convention; Peloponnese handed to Greece. |
| `1003306` | The Bitter Reckoning in Cairo | EGY | 1828-1829 | Muhammad Ali receives only Crete, not Syria. Sets `egyptian_syrian_ambition` and Levant claims, bridging to the 1831 war. |

## Scripting Safeguards
- All triggers guarded by per-country flags (`has_country_flag`), never bare `fire_only_once`.
- Province references checked against `map/definition.csv`: Nafplion 839, Missolonghi 837, Athens 834, Kalamata 841, Patras 842, Chania 847.
- Interlocks cleanly with `events/Ottoman_Event.txt:31257-31262` and `events/Oriental Crisis.txt:31270`.
