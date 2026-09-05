# First Anglo-Ashanti War, 1823-1831 (ASHWarGVG)

Ids 1001600-1001603, file `CoE_RoI_R/events/ASHWarGVG.txt`.

## Historical outline

Ashanti claims over the Fante coast collided with the British forts after the
Crown took over the African Company's posts in 1821. Governor Sir Charles
MacCarthy marched inland in 1823, was destroyed at Nsamankow on 21 January 1824
and killed. The British recovered at Dodowa (Katamanso) in August 1826, and the
war ended in the 1831 treaty that fixed the Pra as the boundary and left the
coastal states outside Ashanti authority.

## Map facts (verified)

- ASH exists at the 1821 start, capital 1910 Kumasi, also owns 1911 Kintampo.
- ENG owns **1908 Cape Coast** on the Gold Coast; **1907 Accra is Danish** until
  1861, so it must not be used as an ENG gate. 1909 Sekondi is unowned.
- 1908 borders 1910, so `neighbour = ASH` is true for ENG from the start
  (checked pixel-adjacency on `map/provinces.bmp`).
- No `military_defeat` / `great_victory` event modifier exists in this mod; the
  defeat uses the existing province modifier `colonial_chaos`, and the Ashanti
  side gets prestige and militancy only. No new modifiers are added.
- Pictures are all existing files: `mfecane`, `derrota`, `war_ended`, `timbuctu`.

## Chain

| id | Who | Fires | Content |
|---|---|---|---|
| 1001600 | ENG | 1823-1826, MTTH 6 months | MacCarthy's Expedition |
| 1001601 | ENG | triggered, 60 days after A | Disaster at Nsamankow |
| 1001602 | ENG | 1826-1832, flag-gated | Peace on the Pra |
| 1001603 | ASH | triggered from 1001601 | Nsamankow, Ashanti side |

**1001600** trigger: `tag = ENG`, `exists`, `owns = 1908`, `ASH = { exists = yes
owns = 1910 }`, `neighbour = ASH`, `year = 1823`, `NOT = { year = 1827 }`, and
`NOT = { war_with = ASH truce_with = ASH alliance_with = ASH
has_country_flag = anglo_ashanti_war_declared
has_country_flag = anglo_ashanti_coast_held }`. A per-country flag rather than
`fire_only_once` (which is engine-wide, per CLAUDE.md).
- A "March on Kumasi" (ai 70): flag, `casus_belli` + `war = { target = ASH
  attacker_goal = { casus_belli = cut_down_to_size } }` - the same pattern
  RUSTurkishWarGVG uses; `cut_down_to_size` needs no state fields. Queues 1001601.
- B "Hold the coast": flag `anglo_ashanti_coast_held`, relation and influence
  with ASH, small prestige cost.

**1001601** prestige -5, war exhaustion, `colonial_chaos` on 1908 for two years,
militancy on its pops, sets `nsamankow_disaster`, fires 1001603 for ASH. The war
itself continues normally; the AI fights it out.

**1001602** trigger: flag `anglo_ashanti_war_declared`, `year = 1826`,
`NOT = { year = 1832 }`, not yet settled.
- A "Treaty on the Pra": `end_war = ASH` (a no-op if the war already ended),
  prestige, relation, sets `anglo_ashanti_settled`. AI weighted up by
  `nsamankow_disaster` and by an Ashanti `ashanti_nsamankow_victory`.
- B "Press on to Kumasi": `badboy = 1`, small prestige, war continues.

**1001603** ASH: prestige +10, militancy -1, sets `ashanti_nsamankow_victory`
(read by 1001602's ai_chance).
