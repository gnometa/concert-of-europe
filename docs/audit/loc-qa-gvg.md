# Localisation QA - GVG event chains (2026-09-06)

Editorial pass over the player-visible English added for event ids 1000301-1000308,
1000400-1000403, 1000500-1000502, 1000600-1000602, 1000700-1000702, 1000900-1000904,
1001000-1001003, 1001100-1001104, 1001200-1001202, 1001300-1001302, 1001400-1001403,
1001500-1001502, 1001600-1001603, 1001800-1001803, the four new decision keys, and the
15 event modifiers added after `cab739e0`. All rows live in
`CoE_RoI_R/localisation/GVG_events.csv` (Windows-1252, CRLF, 15 columns).

**53 rows changed** (39 of them option buttons). No keys added, removed or renamed; no meanings altered.

## Defects fixed

| Key | Class | Before -> After |
|---|---|---|
| `EVTDESC1001802_NEWS_SHORT` | **csv-breaking `;` in text** | `Francis I dead; Ferdinand succeeds.` (16 columns) -> `Francis I dead - Ferdinand succeeds.` (15) |
| `EVTNAME1001102_NEWS_TITLE` | capitalisation | `BOLOGNA PROCLAIMS THE UNITED ITALIAN PROVINCES` -> title case |
| `EVTNAME1001103_NEWS_TITLE` | capitalisation | `AUSTRIAN COLUMNS CROSS THE PO` -> title case |
| `EVTNAME1001104_NEWS_TITLE` | capitalisation | `THE CABINETS AND THE ITALIAN QUESTION` -> title case |
| `EVTNAME1000306` | capitalisation | `The Crown of Belgium is Offered` -> `... Is Offered` (matches `Is` in the other news/event titles) |
| `EVTDESC1000700` | **factual** + length (717 -> 583) | The Eskinci regulation was proclaimed in **May** 1826, not "on the fourteenth of June" (that was the mutiny). Rewritten as `In May the Sultan proclaimed the Eskinci ... Now the Janissaries have overturned their soup kettles`; present-tense `proclaims` in a perfect-tense paragraph also gone. |
| `EVTDESC1000700_NEWS_LONG` | length (652 -> 578) | trimmed the dervish clause and the closing sentence |
| `EVTDESC1001202_NEWS_LONG` | length (605 -> 582) | `the question of the hour in every counting-house from Boston to New Orleans` -> `... the question of the hour from Boston to New Orleans` |
| `EVTDESC1001400` | consistency | `Saint Petersburg` -> `St. Petersburg` (spelling used everywhere else, incl. the Decembrist chain) |
| `EVTDESC1000700` | consistency | `the Janissaries of Istanbul` -> anachronistic against the chain's own `Constantinople` (news rows); clause reworded |
| `EVTDESC1001801` | grammar | `hear their grievances of the constitution` -> `hear their constitutional grievances` |
| `EVTDESC1001301` | grammar (zeugma) | `Java is quiet, ruined and must now be made to pay.` -> `Java is quiet and ruined, and must now be made to pay.` |
| `nizam_i_cedid` | **factual** | `New Order Army` -> `Mansure Army`. The modifier is granted only after `janissaries_abolished` (TURAuspiciousGVG.txt:61,185), i.e. it is Mahmud II's Asakir-i Mansure of 1826, not Selim III's Nizam-i Cedid of 1793-1807. Key unchanged. |
| `canton_squeeze` | consistency | `The Canton Squeeze` -> `Canton Squeeze` (no other modifier name carries a leading article) |
| `metternich_system` | consistency | `The Metternich System` -> `Metternich System` (ditto) |

## Option lengths

39 `EVTOPT*` rows exceeded the ~40-character button budget (worst: 65, 61, 61, 58, 58)
and were shortened without changing the choice offered, e.g.

- `EVTOPTA1001002` `Miguel shall abdicate and go into exile. The Charter is restored.` (65) -> `Miguel abdicates. Restore the Charter.` (38)
- `EVTOPTC1000302` `Vienna and Petersburg made this kingdom - let them defend it.` (61) -> `Let Vienna and Petersburg defend it.` (36)
- `EVTOPTA1001202` `The Force Bill in one hand, Clay's compromise in the other` (58) -> `The Force Bill and Clay's compromise` (36)
- `EVTOPTB1000307` `Not while the Orange flag can still be raised in Brussels.` (58) -> `Never, while Orange may yet return.` (35)
- `EVTOPTA1001802` `Let the Chancellor lead the Staatskonferenz` (43) -> `Metternich leads the State Conference` (37); also drops the untranslated German that the same event's desc renders as "State Conference".

Trailing-punctuation style is per chain (the British, Zollverein, Ashanti and Austrian
chains use no final stop, the rest do); rewrites follow the chain they sit in.
Every option now reads as an imperative or a declared choice.

## Checked and found correct

Dates and names spot-checked against the brief and the sources: London Protocol 3 Feb 1830;
Otto at Nafplion 1833, aged 17, second son of Ludwig I, 3,500 Bavarians; Twenty-Four Articles
1831 and the Treaty of London 1839; Adrianople 1829 (Diebitsch, Nesselrode, Akkerman, Navarino,
Wittgenstein); Senate Square December 1825 (Taganrog, the Uspensky manifesto, three thousand
guardsmen, five hanged); Nsamankow January 1824 and Dodowa; Diponegoro taken at Magelang after
five years, 15,000 Dutch dead; Evora Monte May 1834 (Mindelo, Cape St Vincent); Ciro Menotti,
Via Grande, Francesco IV, hanged 1831; Zollverein "on the first of January" 1834; Clare
by-election 1828; Days of May 1832 and "Go for Gold, to Stop the Duke"; Columbia convention,
Force Bill, Clay's ten-year schedule; Huang Juezi and the Lintin traffic; Hungarian Diet after
thirteen years; Szechenyi's Hitel and the Academy; Francis I 1835 and the Staatskonferenz.

No non-ASCII bytes, no doubled spaces, no leading/trailing whitespace and no remaining
`;` in any text field in scope. `modcheck loc-check` on `GVG_events.csv` reports only the pre-existing, out-of-scope
`EVTDESC999999` split row (education/RGO rework) and the odd-width summary; see the
validate skill baseline. `refcheck loc`: 60 (baseline).
