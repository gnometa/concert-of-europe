# Legacy audit: Scandinavia (SWE / DAN / NOR / ScandinavianEvents)

*2026-09-06. Line-by-line logic review of `events/SWEFlavor.txt`, `events/DANFlavor.txt`,
`events/NORFlavor.txt`, `events/ScandinavianEvents.txt` - the Sweden-Norway union, the
Schleswig-Holstein hand-off and the Scandinavianism / Kalmar chain. Mechanical checks
(braces, province ids, tags, encoding, duplicate ids) were already at baseline; this pass
hunts wrong recipients in FROM/THIS hops, effects that contradict the option text, dead
branches, impossible windows from the 1821 start and implausible magnitudes.*

Line numbers are pre-fix. Fixed items are marked **fixed**.

## [high]

`events/NORFlavor.txt` 536 - event 95095 "Independence for Norway" - the option that grants
independence ran `SWE = { government = hms_government }`, a hard-coded tag inside an event
whose only scope gate is `is_our_vassal = NOR`. Any other overlord of a vassal Norway
(DEN, SCA, a conqueror) would silently rewrite **Sweden's** government instead of its own,
and Sweden need not even be in the war. Root is the overlord, so the tag prefix is pure
loss. **fixed**: dropped to a bare `government = hms_government`, which is identical in the
normal SWE case and correct otherwise. (The neighbouring `NOR = { ... is_core = THIS
remove_core = THIS }` is right: THIS is the event root, so the overlord's cores come off
Norwegian soil.)

## [medium]

`events/DANFlavor.txt` 348 - event 36205 (Copenhagen fortifications) - option A applied
`dominant_issue` directly in country scope. `dominant_issue` is a pop effect; option B of
the same event wraps it in `any_pop`, so the "fortify" branch quietly lost both its
anti_military and its jingoism swing while the "do nothing" branch kept them - the opposite
of the intent. **fixed**: wrapped in `any_pop`.

`events/SWEFlavor.txt` 375 - event 36612 (Boden fortress) - option name was
`"EVTOPTA36611"`, the Strindberg event's button ("Intriguing!") on a fortress-building
option that costs 5000. `EVTOPTA36612` exists in `text.csv`. **fixed**.

`events/DANFlavor.txt` 520 - event 36208 - option name was `"EVTOPTA36207"`. `EVTOPTA36208`
exists (same string, but the wrong key breaks any future retranslation). **fixed**.

`events/DANFlavor.txt` 1198 - event 36220 (Brandes) - option name was `"EVTOPTA36219"`
("Splendid!"). `EVTOPTA36220` exists and actually describes the effect. **fixed**.

`events/ScandinavianEvents.txt` 528 - event 49506 "Norway demands independence" - the
peaceful option paid `badboy = -10`, i.e. it wiped essentially a full infamy bar for
letting a vassal go. Every parallel branch in the tree is an order of magnitude smaller
(95095 `-2`, DAN 36215 Iceland `-3`, SWH 90052 `-3`). **fixed**: `-2`.

`events/DANFlavor.txt` 852 - event 36215 (Iceland's independence) - the trigger is only
`owns = 252`, with no `tag = DEN`, yet the effects run `remove_core = DEN` and the picture
is `danishgovernment`. A non-Danish owner of Iceland fires a Danish-flavoured event and
strips a third party's core. **Not fixed** - narrowing it to DEN would silently delete the
(rare but reachable) case of another owner granting Icelandic independence; the wrong-tag
core removal is the part that needs a decision from the design side.

`events/DANFlavor.txt` 1275/1379 - events 36224/36226 (sell Accra / the Nicobars) - the two
`random_country` blocks are independent, so both a neighbouring GP and an unrelated European
GP can be offered the same territory. Whoever answers 36225/36227 second still pays DEN
20 000 but `secede_province` has already moved the province, so the second buyer pays for
nothing. **Not fixed** - the clean version is one `random_country` with an `OR` limit, which
changes who the AI picks; flagged for a follow-up.

`events/DANFlavor.txt` 1327/1426 - the buyer in 36225/36227 has no `money` gate, so an AI
with an empty treasury still hands over 20 000 and goes into debt. **Not fixed** (same
follow-up).

## [low]

`events/SWEFlavor.txt` 222-227 - event 36608 - the trigger carries two empty province
scopes, `329 = { }` and `316 = { }`, whose `has_building = railroad` lines are commented
out. Empty blocks are always true, so the railway event has no railway requirement. Dead
weight rather than a defect; deleting them would not change behaviour.

`events/SWEFlavor.txt` 833 - event 36650 (Norrland famine) - the AI weight tests
`NOT = { money = 10000 }` inside a **province** event, where `money` is not a country-scope
condition; the modifier probably never applies, so the AI spends the 3000 regardless of its
treasury. The `owner = { treasury = -3000 }` next to it is correctly scoped.

`events/DANFlavor.txt` 1235 - event 36223 answers SWE 36622 with `scaled_militancy` where
the Swedish side uses `scaled_consciousness`, for the same liberal-student episode. Almost
certainly a copy slip, but militancy is a defensible reading of the Danish reaction, so it
is left alone.

`events/ScandinavianEvents.txt` 71/231/325 - `set_country_flag = refused_kalmar_union` is
set by the refusal branch of all three offers (49501 Kalmar, 49503 customs union, 49504
political union). It is only read by `decisions/SCA.txt:363` and cleared in two places, so
refusing a *customs* union also locks the political union decision. Shared-flag conflation,
not a crash.

`events/ScandinavianEvents.txt` 122-138 - 49502 option B removes `kalmar_union` and
`customs_union` from FROM, which by construction never had either (only the *accepting*
side gets them in 49501/49503). No-op.

`events/ScandinavianEvents.txt` 785 - 49510 duplicates options 2 and 3 of SWH 90052
verbatim for a newly-formed SCA. It is not a double-fire (90052 needs
`has_country_flag = annex_schleswig_holstein`, 49510 is triggered only from
`NationalUnification.txt:189`), but the two copies must be edited together; 49510 also drops
90052's "retain autonomy" option and weights the remaining pair 100/0, so the SCA AI can
never annex both duchies.

## Checked and clean

- Multi-statement `NOT` blocks throughout these four files read as NOR and every one of them
  wants NOR semantics (year ceilings plus a "don't fire if" guard). No inverted windows.
- SWE 36618-36621 mirror NOR 36400-36405 through `set_global_flag` Munch / Aasen / Ibsen /
  Thrane on both sides, so the Norwegian-culture episodes fire exactly once whether or not
  Norway is a separate tag.
- `has_pop_religion = north_german` in 49510 is a sub-culture in the religion field
  (`common/religion.txt:153`), not a dead religion test.
- FROM/THIS hops in 36224 -> 36225, 36226 -> 36227, 49501/49503/49504 -> 49502, the
  usurp-Kalmar decision -> 49509 and `NationalUnification.txt` -> 49510 all address the
  intended country.
- `conquest_any` (49502) is `is_triggered_only` in `common/cb_types.txt`, so granting it by
  event is legitimate.
- All year windows are reachable from the 1821.9.1 bookmark; no window opens before the
  start date or after 1935.
