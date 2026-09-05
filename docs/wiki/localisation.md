# Localisation

Source: https://vic2.paradoxwikis.com/Localisation

**Localisation** is an important part of Victoria 2's modding system. It connects the variable 'keys' used in the game's internal code and external scripting system with readable text, and also allows translation into multiple languages. Thus it controls the naming of everything from countries to parties to tech in Victoria 2.

### The localisation files

In the Victoria 2 folder, you can find the localisation folder. In here is a long list of documents in csv format. The csv format can be edited in excel or similar software.

The files can be quite chaotic to navigate. They are named after the patch in which the name was first defined. Each 'type' of name is generally stored together (names of countries together, event texts together etc.), but not always. All the possible names for e.g. California is stored across 3 different files. You will have to use the search function a lot. 

Note that many concepts multiple related texts-blurbs e.g. both a proper name and an adjective or the text for multiple buttons. They are usually stored next to each other or at least in the same section.

### Basics

A localisation looks like this (only English, French and German are officially supported and only the default English localisation is generally correct):

```
key;English;French;German;Polish;Spanish;Italian;Swedish;Czech;Hungarian;Dutch;Portugese;Russian;Finnish;
```

For example, this is the localisation for the single player button in the main menu:

```
FE_SINGLE_PLAYER;Single Player;Solo;Einzelspieler;Gra pojedyncza;Un jugador;Giocatore singolo;Egyjátékos mód;Hra pro jednoho hráèe;;;;;;x;;;;
```

Some [commands](list-of-effects.md) in Paradox Script create localisation keys.

#### Events

Events are localised through these three script commands: `title`, `desc`, `name` (the latter in an `option` code block).  

The commands assign keys like this: `command = "key"`. The quotation marks are optional, but it is standard practice to include them.

```
country_event = {
    id = 100
    title = "EVTNAME100"
    desc = "EVTDESC100"

    option = {
        name = "EVTOPTA100"
    }

    option = {
        name = "EVTOPTB100"
    }
}
```

The assigned keys can be any arbitrary string, but should follow the above standard: `"EVTNAME[ID]"` for the title, `"EVTDESC[ID]"` for  the description, and `"EVTOPT[A-F][ID]"` for options. 

The subtitles of election events are localised by adding `_sub` to the event's `title` key.

#### Decisions

Decisions are automatically localised using the name of the decision as defined through the script with the extensions `_title` and `_desc`.

#### Countries

Countries has both a proper name under `TAG` and it's adjective under `TAG_ADJ`. 

Countries can change names depending on government type. Example:

`tag_absolute_monarchy;name(English);name(French);name(German);;name(Spanish);;;;;;;;;x;`

`CAL_absolute_monarchy;Kingdom of California;Royaim de California;Kingdom of California;;Reino de California;;;;;;;;;x;`'

### Dynamic Localisation

Normally, events and deceisions can only have one localisation - or in other words, one specific event or decision has only one specific localisation key associated with it with is associated with only one piece of text. However, the `change_region_name` [effect](list-of-effects.md) can be abused to write decisions, events, or tooltips with localisation that changes depending on in-game circumstances. For more information, see [Dynamic localisation](dynamic-localisation.md).

### Common Modding Issues

There are a few common issues when modding relating to localisation. 

One issue is that accented and other special characters are not displaying correctly. E.g. your custom country called `Númenor` may show up as something weird like `NÃºmenor`. This is due to the encoding being incorrect when the file was saved. Encoding determines how the characters are saved, and must match what the game expects. The correct encoding to use is ANSI (or Western-1252). If you are using Notepad++, you can switch encoding through the Encoding menu. If you are using VSCode, you can switch encoding by opening the Command Palette then running Change File Encoding. Always ensure you open and save the files in the correct encoding.

Another issue is that localisation is shifted around and nonsensical. E.g. your custom country called `Númenor` is showing us as something completely unexpected and illogical like `France` or `Declare War` or some other text. This is due to there being an empty line in one of your localisation csv files. Simply delete the empty line and all will be well.

Moreover, to modify a single key in a localisation file, instead of copying the whole file along with other keys you are not interested in, you can create a .csv file with any name so long as the name is lexicographically ahead of the vanilla file where the key is located. For example, if you want to replace the text of small_arms_production_desc which is defined in `beta1.csv` in vanilla, your file name must be less than `beta1.csv`. `beta0.csv` will work and so will `0anyname.csv`; but not `beta1_my_replacement.csv`.

### Localisation Colours

Below is a list of colours recognised by Victoria 2's localisation system.<ref name="forum">https://forum.paradoxplaza.com/forum/threads/localization-text-key-list.946323/</ref> You can use colours to highlight important information in event or decision text or any part of the interface localisation. For example, to get "This text is red" to appear as red, you would write in the localisation: `§RThis text is red`.

| Key | Colour |
|---|---|
| §W | White |
| §Y | Yellow |
| §R | Red |
| §b | Black |
| §G | Green |
| §B | Blue |
| §g | Light grey |
| §! | Return to default colour |

### Localisation Keys

Below is a list of all localisation keys found in Victoria 2's files, along with their scopes and meanings.<ref name="forum" />

| Key | Scope | Description | Example Value |
|---|---|---|---|
| \n | Events/Decisions | Skips Line |  |
| @TAG | Events/Decisions | Adds the country flag of that tag | @ENG |
| $$ |  |  |  |
| $ACTION$ |  |  |  |
| $ACTIVE$ |  |  |  |
| $ACTOR$ |  |  |  |
| $ADJ$ |  |  |  |
| $AGAINST$ |  |  |  |
| $AGRESSOR$ |  |  |  |
| $ALLOWED$ |  |  |  |
| $AMOUNT$ |  |  |  |
| $ANYPROVINCE$ | Fake News | Any province in the country | Liverpool |
| $ARMY_NAME$ |  |  |  |
| $ARMY$ |  |  |  |
| $ASTATE$ |  |  |  |
| $ATTACKER$ |  |  |  |
| $ATTUNIT$ |  |  |  |
| $AVG$ |  |  |  |
| $BAC$ |  |  |  |
| $BADBOY$ |  |  |  |
| $BADWORD$ |  |  |  |
| $BASE_PERCENTAGE$ |  |  |  |
| $BASE$ |  |  |  |
| $BAT$ |  |  |  |
| $BLD$ |  |  |  |
| $BON$ |  |  |  |
| $BONUS$ |  |  |  |
| $BRIG$ |  |  |  |
| $BUD$ |  |  |  |
| $BUILDING$ |  |  |  |
| $BUY$ |  |  |  |
| $CAP$ |  |  |  |
| $CAPITAL$ | Events/Decisions | The capital city of the country | London |
| $CASH$ |  |  |  |
| $CASUS$ |  |  |  |
| $CAT$ |  |  |  |
| $CATEGORY$ |  |  |  |
| $CB_TARGET_NAME_ADJ$ |  |  |  |
| $CB_TARGET_NAME$ |  |  |  |
| $CHAN$ |  |  |  |
| $CHANCE$ |  |  |  |
| $CHANGE$ |  |  |  |
| $chief_of_army$ |  |  |  |
| $chief_of_navy$ |  |  |  |
| $chief_of_staff$ |  |  |  |
| $COMMANDER$ |  |  |  |
| $CON$ |  |  |  |
| $CONSTRUCTION$ |  |  |  |
| $CONTINENTNAME$ |  |  |  |
| $control$ |  |  |  |
| $COST$ |  |  |  |
| $COUNRTY_ADJ$ |  |  |  |
| $COUNT$ |  |  |  |
| $COUNTRIES$ |  |  |  |
| $COUNTRY_ADJ$ |  |  |  |
| $COUNTRY$ |  |  |  |
| $COUNTRY1$ |  |  |  |
| $COUNTRY2$ |  |  |  |
| $COUNTRYADJ$ |  |  |  |
| $COUNTRYCULTURE$ |  |  |  |
| $COUNTRYNAME$ |  |  |  |
| $CREATOR$ |  |  |  |
| $CREDITS$ |  |  |  |
| $CRISISAREA$ |  |  |  |
| $CRISISATTACKER$ |  |  |  |
| $CRISISDEFENDER$ |  |  |  |
| $CRISISTAKER_ADJ$ |  |  |  |
| $CRISISTAKER$ |  |  |  |
| $CRISISTARGET_ADJ$ |  |  |  |
| $CRISISTARGET$ |  |  |  |
| $CUL$ |  |  |  |
| $CULTURE_GROUP_UNION$ |  |  |  |
| $CULTURE$ |  |  |  |
| $CULTUREGROUP$ |  |  |  |
| $CURR$ |  |  |  |
| $CURRENT$ |  |  |  |
| $D$ |  |  |  |
| $DATE_LONG_0$ |  |  |  |
| $DATE_LONG_1$ |  |  |  |
| $DATE_SHORT_0$ |  |  |  |
| $DATE$ |  |  |  |
| $DAY$ |  |  |  |
| $DAYS$ |  |  |  |
| $DEFENDER$ |  |  |  |
| $DEFUNIT$ |  |  |  |
| $DESC$ |  |  |  |
| $DEST$ |  |  |  |
| $DETAILS$ |  |  |  |
| $DIRECTION$ |  |  |  |
| $DIST$ |  |  |  |
| $EFFECT$ |  |  |  |
| $EFFECTS$ |  |  |  |
| $EMILIST$ |  |  |  |
| $EMPLOYEE_MAX$ |  |  |  |
| $EMPLOYEES$ |  |  |  |
| $ENEMY$ |  |  |  |
| $ENGINEERMAXUNITS$ |  |  |  |
| $ENGINEERUNITS$ |  |  |  |
| $ESCORTS$ |  |  |  |
| $EVENT$ |  |  |  |
| $EVENTDESC$ |  |  |  |
| $EXC$ |  |  |  |
| $EXP$ |  |  |  |
| $EXPLANATION$ |  |  |  |
| $FACTION$ |  |  |  |
| $FACTORY$ |  |  |  |
| $FIRST$ |  |  |  |
| $FOCUS$ |  |  |  |
| $FOLDER$ |  |  |  |
| $FOR$ |  |  |  |
| $FRACTION$ |  |  |  |
| $FRIEND$ |  |  |  |
| $FROM$ |  |  |  |
| $FROMCOUNTRY_ADJ$ |  |  |  |
| $FROMCOUNTRY$ |  |  |  |
| $FROMPROVINCE$ |  |  |  |
| $FROMRULER$ |  |  |  |
| $FUNDS$ |  |  |  |
| $GOAL$ |  |  |  |
| $GOOD$ |  |  |  |
| $GOODS$ |  |  |  |
| $GOV$ |  |  |  |
| $GOVERNMENT$ |  |  |  |
| $GOVT$ |  |  |  |
| $GP_ADJ$ |  |  |  |
| $GP$ |  |  |  |
| $GROUP$ |  |  |  |
| $head_of_government$ |  |  |  |
| $HIGH_TAX$ |  |  |  |
| $HIT$ |  |  |  |
| $HOME$ |  |  |  |
| $HULL$ |  |  |  |
| $IAMOUNT$ |  |  |  |
| $ICOUNTRY$ |  |  |  |
| $IDE$ |  |  |  |
| $IDEOLOGY$ |  |  |  |
| $ILOCATION$ |  |  |  |
| $IMMLIST$ |  |  |  |
| $IMPACT$ |  |  |  |
| $INAME$ |  |  |  |
| $INCOME$ |  |  |  |
| $INDEP$ |  |  |  |
| $INF$ |  |  |  |
| $INFAMY$ |  |  |  |
| $INPUT$ |  |  |  |
| $INV$ |  |  |  |
| $INVENTION$ |  |  |  |
| $INVESTED_IN_US_MESSAGE$ |  |  |  |
| $INVESTED$ |  |  |  |
| $ISSUE$ |  |  |  |
| $LAW$ |  |  |  |
| $LEADER$ |  |  |  |
| $LEV$ |  |  |  |
| $LEVEL$ |  |  |  |
| $LEVELS$ |  |  |  |
| $LIM$ |  |  |  |
| $LIMIT$ |  |  |  |
| $LIST$ |  |  |  |
| $LITERACY$ |  |  |  |
| $LOC$ |  |  |  |
| $LOCAL$ |  |  |  |
| $LOCATION$ |  |  |  |
| $LORD$ |  |  |  |
| $LOSE$ |  |  |  |
| $LOW_TAX$ |  |  |  |
| $LVL$ |  |  |  |
| $M$ |  |  |  |
| $MAX$ |  |  |  |
| $MAXLOAN$ |  |  |  |
| $MEN$ |  |  |  |
| $MESSENGER$ |  |  |  |
| $MIL$ |  |  |  |
| $MILITANCY$ |  |  |  |
| $MIN$ |  |  |  |
| $MONARCHTITLE$ |  |  |  |
| $MONEY$ |  |  |  |
| $MONTH$ |  |  |  |
| $MONTHS$ |  |  |  |
| $MOVEMENT$ |  |  |  |
| $MUCH$ |  |  |  |
| $N$ |  |  |  |
| $NAME$ |  |  |  |
| $NATION$ |  |  |  |
| $NATIONALVALUE$ | UI | The National value of the country. | Order |
| $NATIVES$ |  |  |  |
| $NAVY_NAME$ |  |  |  |
| $NAVY$ |  |  |  |
| $NEED$ |  |  |  |
| $NEEDED$ |  |  |  |
| $NEGATIVE$ |  |  |  |
| $NEUT$ |  |  |  |
| $NEW$ |  |  |  |
| $NEWCOUNTRY$ |  |  |  |
| $NF$ |  |  |  |
| $NOW$ |  |  |  |
| $NUM$ |  |  |  |
| $NUMBER$ |  |  |  |
| $NUMFACTORIES$ |  |  |  |
| $NUMSPECIALFACTORIES$ |  |  |  |
| $ODDS$ |  |  |  |
| $OLD$ |  |  |  |
| $OLDCOUNTRY$ |  |  |  |
| $OPERATOR$ |  |  |  |
| $OPINION$ |  |  |  |
| $OPPOSING_ARMY$ |  |  |  |
| $OPPOSING_NAVY$ |  |  |  |
| $OPRESSOR$ |  |  |  |
| $OPT$ |  |  |  |
| $OPTIMAL$ |  |  |  |
| $OPTION$ |  |  |  |
| $ORDER$ |  |  |  |
| $ORG$ |  |  |  |
| $ORGANISATION$ |  |  |  |
| $OTHER$ |  |  |  |
| $OTHERRESULT$ |  |  |  |
| $OUR_LEAD$ |  |  |  |
| $OUR_NUM$ |  |  |  |
| $OUR_RES$ |  |  |  |
| $OURCAPITAL$ | Fake News | The capital of the country | London |
| $OURCOUNTRY_ADJ$ | Fake News | The name of the country | British |
| $OURCOUNTRY$ | Fake News | The name of the country | United Kingdom |
| $OUTPUT$ |  |  |  |
| $OVERLORD$ |  |  |  |
| $owner$ |  |  |  |
| $PARAM$ |  |  |  |
| $PARTY$ |  |  |  |
| $PASSIVE$ |  |  |  |
| $PAY$ |  |  |  |
| $PEN$ |  |  |  |
| $PENALTY$ |  |  |  |
| $PER$ |  |  |  |
| $PERC$ |  |  |  |
| $PERC2$ |  |  |  |
| $PERCENT$ |  |  |  |
| $PERCENTAGE$ |  |  |  |
| $PLAYER$ |  |  |  |
| $playername$ |  |  |  |
| $POLICY$ |  |  |  |
| $POP$ |  |  |  |
| $POPTYPE$ |  |  |  |
| $POPULARITY$ |  |  |  |
| $POSITION$ |  |  |  |
| $POSITIVE$ |  |  |  |
| $POWER$ |  |  |  |
| $PRES$ |  |  |  |
| $PRESCENCE$ |  |  |  |
| $PRESTIGE$ |  |  |  |
| $PRODUCED$ |  |  |  |
| $PRODUCER$ |  |  |  |
| $PROG$ |  |  |  |
| $PROGRESS$ |  |  |  |
| $PROJ$ |  |  |  |
| $PROV$ |  |  |  |
| $PROVINCE$ |  |  |  |
| $Province$ |  |  |  |
| $PROVINCECULTURE$ |  |  |  |
| $PROVINCENAME$ |  |  |  |
| $PROVINCERELIGION$ |  |  |  |
| $PROVINCES$ |  |  |  |
| $PROVS$ |  |  |  |
| $RANK$ |  |  |  |
| $RATE$ |  |  |  |
| $REC$ |  |  |  |
| $RECIPIENT$ |  |  |  |
| $RECONMAXUNITS$ |  |  |  |
| $RECONUNITS$ |  |  |  |
| $REFORM$ |  |  |  |
| $REGION$ |  |  |  |
| $REL$ |  |  |  |
| $RELATION$ |  |  |  |
| $REQ$ |  |  |  |
| $REQLEVEL$ |  |  |  |
| $REQUIRED$ |  |  |  |
| $RESOURCE$ |  |  |  |
| $RESULT$ |  |  |  |
| $RSTATE$ |  |  |  |
| $RULE$ |  |  |  |
| $RUNS$ |  |  |  |
| $SCR$ |  |  |  |
| $SEA$ |  |  |  |
| $SECOND_COUNTRY$ |  |  |  |
| $SECOND$ |  |  |  |
| $SELF$ |  |  |  |
| $SELL$ |  |  |  |
| $SETTING$ |  |  |  |
| $SHIPS$ |  |  |  |
| $SIZE$ |  |  |  |
| $SKILL$ |  |  |  |
| $SOURCE$ |  |  |  |
| $SPEED$ |  |  |  |
| $SPHEREMASTER$ |  |  |  |
| $STATE$ |  |  |  |
| $STATENAME$ |  |  |  |
| $STR$ |  |  |  |
| $STRATA$ |  |  |  |
| $STRENGTH$ |  |  |  |
| $STRING_0_0$ |  |  |  |
| $STRING_0_1$ |  |  |  |
| $STRING_0_2$ |  |  |  |
| $STRING_0_3$ |  |  |  |
| $STRING_0_4$ |  |  |  |
| $STRING_9_0$ |  |  |  |
| $STRINGS_LIST_4$ |  |  |  |
| $SUB$ |  |  |  |
| $TABLE$ |  |  |  |
| $TAG_0_0_$ |  |  |  |
| $TAG_0_0_ADJ$ |  |  |  |
| $TAG_0_0_UPPER$ |  |  |  |
| $TAG_0_0_upper$ |  |  |  |
| $TAG_0_0$ |  |  |  |
| $TAG_0_1_ADJ$ |  |  |  |
| $TAG_0_1_UPPER$ |  |  |  |
| $TAG_0_1$ |  |  |  |
| $TAG_0_2_ADJ$ |  |  |  |
| $TAG_0_2$ |  |  |  |
| $TAG_0_3_ADJ$ |  |  |  |
| $TAG_0_3$ |  |  |  |
| $TAG_1_0$ |  |  |  |
| $TAG_2_0_UPPER$ |  |  |  |
| $TAG_2_0$ |  |  |  |
| $TAG_3_0_UPPER$ |  |  |  |
| $TAG_3_0$ |  |  |  |
| $TAG$ |  |  |  |
| $TAG0_0$ |  |  |  |
| $TAGETLIST$ |  |  |  |
| $TARGET_COUNTRY$ |  |  |  |
| $TARGET$ |  |  |  |
| $TARGETLIST$ |  |  |  |
| $TECH$ |  |  |  |
| $TEMPERATURE$ |  |  |  |
| $TERMS$ |  |  |  |
| $TERRAIN$ |  |  |  |
| $TERRAINMOD$ |  |  |  |
| $TEXT$ |  |  |  |
| $THEIR_LEAD$ |  |  |  |
| $THEIR_NUM$ |  |  |  |
| $THEIR_RES$ |  |  |  |
| $THEIRLOST$ |  |  |  |
| $THEIRNUM$ |  |  |  |
| $THEIRSHIP$ |  |  |  |
| $THEM$ |  |  |  |
| $THIRD$ |  |  |  |
| $THREAT$ |  |  |  |
| $TIME$ |  |  |  |
| $TITLE$ |  |  |  |
| $TO$ |  |  |  |
| $TOT$ |  |  |  |
| $TOTAL$ |  |  |  |
| $TOTALEMI$ |  |  |  |
| $TOTALIMM$ |  |  |  |
| $TRA$ |  |  |  |
| $TRUTH$ |  |  |  |
| $TYPE$ |  |  |  |
| $UNEMPLOYED$ |  |  |  |
| $UNION_ADJ$ |  |  |  |
| $UNION$ |  |  |  |
| $UNIT$ |  |  |  |
| $UNITS$ |  |  |  |
| $UNTIL$ |  |  |  |
| $USLOSS$ |  |  |  |
| $USNUM$ |  |  |  |
| $VAL$ |  |  |  |
| $VALUE_INT_0_0$ |  |  |  |
| $VALUE_INT_0_1$ |  |  |  |
| $VALUE_INT_0_2$ |  |  |  |
| $VALUE_INT_0_3$ |  |  |  |
| $VALUE_INT_0_4$ |  |  |  |
| $VALUE_INT1$ |  |  |  |
| $VALUE$ |  |  |  |
| $VERB$ |  |  |  |
| $VERSUS$ |  |  |  |
| $WAR$ |  |  |  |
| $WARGOAL$ |  |  |  |
| $WE$ |  |  |  |
| $WHAT$ |  |  |  |
| $WHERE$ |  |  |  |
| $WHICH$ |  |  |  |
| $WHO$ |  |  |  |
| $WINNER$ |  |  |  |
| $X$ |  |  |  |
| $Y$ |  |  |  |
| $YEAR$ |  |  |  |
| $YEARS$ |  |  |  |
| $YESTERDAY$ |  |  |  |

### References

<references />
