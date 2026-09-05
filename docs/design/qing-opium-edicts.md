# Qing China 1821-1839: Daoguang's opium edicts

Gap from `docs/design/1821-1836-coverage.md` (CHI/QNG row): the mod has generic
`local_opium_habit` province events and an Opium War chain that only starts to move in
1835 (`events/CHIFlavor.txt:1316080-1316081`). Nothing represents Daoguang's own
prohibition edicts, the silver drain of the 1830s, or the 1836 legalisation debate.

New file `events/CHIOpiumGVG.txt`, ids 1001500-1001599 (registered in
`events/GVG Event IDs.txt`). Tag is **QNG** at the 1821 start (`CHI` is the later
republic); QNG is `civilized = no`.

## Events

**1001500 - The Daoguang Edicts** (QNG, `year = 1821`, `NOT = { year = 1827 }`,
`civilized = no`, `fire_only_once`, MTTH 12 months).
- A: *Enforce the prohibition* (ai 70, historical). `opium_prohibition` country modifier
  (10 years), `set_country_flag = qing_opium_prohibition`, small consciousness bump,
  `relation = { who = ENG value = -25 }`, and fires the British event 1001502.
- B: *Tolerate the Canton trade* (ai 30). `treasury = 25000`, `canton_squeeze` modifier
  (tax up, militancy up, prestige down - the corruption branch),
  `set_country_flag = qing_opium_tolerated`, `relation = { who = ENG value = 10 }`.

**1001501 - The Silver Drain** (QNG, `year = 1830`, `NOT = { year = 1840 }`, requires
either flag from 1001500, `fire_only_once`, MTTH 15 months).
- A: *Debase the coinage* (ai 25). `treasury = 50000`, `silver_drain` modifier (10 years).
- B: *Crack down harder* (ai 60, the Huang Juezi / Lin Zexu line).
  `set_country_flag = qing_opium_crackdown`, refreshes `opium_prohibition`,
  `relation = { who = ENG value = -25 }`, militancy in coastal pops.
- C: *Legalise and tax it* (ai 15, alt-history). `set_country_flag = qing_opium_legalised`,
  clears the prohibition flag/modifier, `treasury = 75000`, `canton_squeeze`,
  consciousness up, `relation = { who = ENG value = 25 }`.

**1001502 - The Canton Trade** (ENG, `is_triggered_only`, fired by 1001500 option A).
- A: *Lobby for the trade* (ai 70). `set_country_flag = eng_canton_lobby`,
  `relation = { who = FROM value = -20 }`, small prestige.
- B: *Respect the edicts* (ai 30). `relation = { who = FROM value = 25 }`, prestige -5.

## Hook into the existing chain

The chain does **not** duplicate the war. It only adds `mean_time_to_happen` modifiers to
the existing Kowloon incident `events/CHIFlavor.txt:1316081`, which is what actually
starts the First Opium War (its option A calls ENG event 131709, which declares it):

- `factor = 0.75` if QNG `has_country_flag = qing_opium_prohibition`
- `factor = 0.75` if QNG `has_country_flag = qing_opium_crackdown`
- `factor = 0.8`  if `ENG = { has_country_flag = eng_canton_lobby }`
- `factor = 3`    if QNG `has_country_flag = qing_opium_legalised`

No trigger of 1316080/1316081 is re-gated, so an unmodified game plays as before. RGOs,
`common/goods.txt` (`opium` already exists) and province history are untouched; the
opium trade appears in flavour text only.

## Other files

- `common/event_modifiers.txt`: new `opium_prohibition`, `canton_squeeze`, `silver_drain`.
- `localisation/GVG_events.csv`: event/option/modifier keys (appended with
  `modcheck.py loc-add`, never with Edit/Write).
- Pictures: existing `Opium.tga` / `Opiumwar.tga` only.
