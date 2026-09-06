#!/usr/bin/env python
# -*- coding: ascii -*-
"""Set a historical 1821 starting literacy on every history/countries file.

Every file in CoE_RoI_R/history/countries was flattened to `literacy = 0.01` by
commit 8f5e1248 ("economic rework base", 2020). This script restores a *historical*
1821 value per tag, grouped into tiers so that tags sharing a nation (substates,
han, princely states, release tags) always get the same number.

Only the `literacy = ` value in the top-level (undated) block is rewritten.
`non_state_culture_literacy` stays at the 0.01 floor, and the dated 1836.1.1 /
1861.1.1 blocks are left flat: the mod has a single bookmark (1821.9.1) and the
engine never reads a dated history block later than the start date, so those
numbers are unreachable.

Usage:
    python scripts/apply_literacy.py            # apply
    python scripts/apply_literacy.py --check    # report only, write nothing
    python scripts/apply_literacy.py --doc      # print the markdown tier table
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CDIR = os.path.join(ROOT, 'CoE_RoI_R', 'history', 'countries')

# tier -> (literacy, one-line justification)
TIERS = {
    'prussia_saxony':   (0.55, 'Compulsory Volksschule since 1763/1805; the best-schooled states in Europe in 1821'),
    'nordic':           (0.70, 'Lutheran household examination (husforhor); reading literacy was near-universal by 1800'),
    'lowlands':         (0.55, 'Dutch 1806 school law and Swiss cantonal schools plus dense urban print culture'),
    'britain':          (0.55, 'English signature literacy ~0.55, Scottish parish schools ~0.75, Welsh Sunday schools; blended'),
    'usa_north':        (0.60, 'New England and Old Northwest common schools; the highest attested rate anywhere in 1821'),
    'usa':              (0.55, 'Free-state ~0.60 blended with the slave South ~0.35 into one country'),
    'usa_south':        (0.35, 'Plantation South: no common-school system, slave literacy criminalised'),
    'usa_west':         (0.45, 'Anglo settler populations, no established school system yet'),
    'settler':          (0.50, 'British settler colonies: literate emigrant stock, church schools from the start'),
    'canada':           (0.42, 'The Canadas in 1821 are majority French-Canadian stock; between Quebec and the anglophone colonies'),
    'north_german':     (0.50, 'Protestant north German states with Prussian-style school ordinances'),
    'german_unified':   (0.45, 'Unification tag: north German schooling blended with the Catholic south'),
    'south_german':     (0.35, 'Catholic south Germany and Austria proper: schooling later and thinner than Prussia'),
    'habsburg_dual':    (0.28, 'Austrian-administered Slovene and Adriatic lands, and the dual-monarchy tag'),
    'bohemia':          (0.30, 'Bohemian Normalschulen; the best-schooled Habsburg crownland'),
    'hungary':          (0.22, 'Hungarian and Slovak lands: county schools for the gentry, little for the peasantry'),
    'habsburg_south':   (0.18, 'Croatian Military Frontier schooling, above the Ottoman Balkans'),
    'eastern_catholic': (0.12, 'Galicia, Bukovina, Transylvania, Dalmatia, Lithuania: Habsburg and Polish periphery'),
    'france_belgium':   (0.42, 'Restoration France and the southern Netherlands; ~0.45 male, ~0.35 female'),
    'france_periphery': (0.30, 'Breton and Occitan non-French-speaking peripheries lagged the national rate'),
    'ireland':          (0.30, 'Hedge schools before the 1831 national system'),
    'quebec':           (0.30, 'French-Canadian literacy well below anglophone British North America'),
    'baltic_lutheran':  (0.40, 'Estonian, Latvian and Finnish Lutheran reading literacy high, writing literacy low'),
    'north_italy':      (0.25, 'Piedmont, Lombardy-Venetia, Tuscany and the duchies; Austrian school law in the north'),
    'italy_unified':    (0.20, 'Unification tag: northern rates blended with the Mezzogiorno'),
    'south_italy':      (0.12, 'Two Sicilies, the Papal States, Malta and Corsica: no state schooling'),
    'iberia':           (0.20, 'Spain after the Cadiz reforms; schooling urban and clerical'),
    'portugal':         (0.15, 'Portugal and the Portugal-Brazil union: poorest schooling in western Europe'),
    'poland':           (0.20, 'Congress Poland and Krakow: the 1815-30 Polish school system before its suppression'),
    'russia':           (0.06, 'Serf empire; literacy confined to nobility, clergy and townsmen'),
    'russia_frontier':  (0.03, 'Siberian, steppe and Arctic governorates'),
    'caucasus':         (0.04, 'Georgian and Armenian church schooling in a mostly illiterate countryside'),
    'frontier_mixed':   (0.20, 'Metis, Rupert-s Land and Sapmi: mixed settler/indigenous, some mission schooling'),
    'greece':           (0.10, 'Greek merchant and church schools, well above the Ottoman average'),
    'balkan_ottoman':   (0.06, 'Christian Ottoman subject nations: monastery schooling only'),
    'balkan_muslim':    (0.03, 'Albanian highlands: no schooling in any language'),
    'ottoman':          (0.05, 'Ottoman Empire: medrese literacy in Turkish and Arabic, ~5% of adults'),
    'ottoman_arab':     (0.05, 'Arab Ottoman provinces, same medrese base as the metropole'),
    'ottoman_christian': (0.08, 'Armenian, Assyrian and Maronite communities ran their own schools'),
    'egypt':            (0.05, 'Muhammad Ali had only just founded his first state schools; the base was kuttab literacy'),
    'maghreb':          (0.03, 'North African regencies: Quranic schooling, no state system'),
    'arabia':           (0.03, 'Arabian emirates and imamates: Quranic schooling only'),
    'persia':           (0.05, 'Qajar Persia: maktab literacy in the towns'),
    'centralasia':      (0.02, 'Afghan and Turkestani khanates: madrasa literacy in a few cities'),
    'himalaya':         (0.02, 'Nepal, Bhutan, Sikkim, Ladakh: monastic literacy only'),
    'india':            (0.05, 'Company India and the princely states; village and maktab schools, ~5-6% of adult males'),
    'japan':            (0.30, 'Terakoya and han schools; the highest non-Western rate in 1821'),
    'qing':             (0.15, 'Qing China: Rawski puts adult male literacy at 30-45%, blended with a much lower female rate'),
    'qing_frontier':    (0.03, 'Tibet, Mongolia, Xinjiang: monastic or madrasa literacy only'),
    'korea':            (0.10, 'Joseon: hanja for the yangban, growing hangul literacy below it'),
    'ryukyu':           (0.10, 'Ryukyu kingdom, schooled on the Japanese and Chinese model'),
    'seasia_buddhist':  (0.08, 'Theravada monastery schooling gave Burma and Siam unusually high male literacy'),
    'seasia_confucian': (0.08, 'Vietnamese village schools on the Chinese classical model'),
    'seasia':           (0.02, 'Malay and Indonesian archipelago states: pesantren literacy only'),
    'philippines':      (0.10, 'Spanish parish schools in the Christianised lowlands'),
    'pacific_tribal':   (0.02, 'Pacific and other tribal societies; mission schooling only beginning in 1821'),
    'latam_mid':        (0.12, 'Larger post-independence republics: creole urban literacy over an illiterate countryside'),
    'latam_low':        (0.08, 'Andean and Mesoamerican republics with large unschooled indigenous majorities'),
    'centam':           (0.10, 'Central American republics: parish schooling in the towns'),
    'caribbean':        (0.12, 'Caribbean colonies: literate free population over an enslaved majority'),
    'haiti':            (0.05, 'Post-revolutionary Haiti; schooling limited to the Port-au-Prince elite'),
    'liberia':          (0.10, 'Americo-Liberian settlers were literate; the interior was not'),
    'boer':             (0.35, 'Cape and Boer settler society, Dutch Reformed home schooling'),
    'africa_muslim':    (0.03, 'Sahelian and Swahili Muslim states with Quranic school networks'),
    'africa':           (0.01, 'Non-literate or newly-missionised African societies'),
    'horn':             (0.02, 'Ethiopian church schooling and Somali Quranic schooling, both very narrow'),
    'dynamic':          (0.10, 'Generic dynamic/release placeholder tag, never present at the 1821 start'),
}

# file stem (without .txt) -> tier
ASSIGN = {}


def _t(tier, *stems):
    for s in stems:
        assert s not in ASSIGN, s
        ASSIGN[s] = tier


_t('prussia_saxony', 'PRU - Prussia', 'SAX - Saxony')
_t('nordic', 'DEN - Denmark', 'SWE - Sweden', 'NOR - Norway', 'ICL - Iceland',
   'SCA - Scandinavia', 'FIN - Finland')
_t('lowlands', 'NET - Netherlands', 'SWI - Switzerland')
_t('britain', 'ENG - United Kingdom', 'ENL - England', 'SCO - Scotland',
   'WHA - Wales')
_t('ireland', 'IRE - Ireland')
_t('usa', 'USA - USA')
_t('usa_north', 'UNY - New York', 'UNJ - New Jersey', 'UPA - Pennsylvania',
   'UOH - Ohio', 'UIN - Indiana', 'UIL - Illinois', 'UIA - Iowa',
   'UMI - Michigan', 'UMN - Minnesota', 'UWI - Wisconsin', 'UNB - Nebraska',
   'UOR - Oregon', 'NEN - New England', 'MAN - Manhattan Commune',
   'FSA - Free States of America', 'DAK - Dakota')
_t('usa_south', 'UVA - Virginia', 'UNC - North Carolina', 'USC - South Carolina',
   'UGA - Georgia', 'UAL - Alabama', 'UMS - Mississippi', 'UAR - Arkansas',
   'UTN - Tennessee', 'ULA - Louisiana', 'UFL - Florida', 'UWV - West Virginia',
   'UKY - Kentucky', 'UMO - Missouri', 'CSA - CSA', 'TEX - Texas')
_t('usa_west', 'CAL - Californian Republic', 'DES - Deseret')
_t('canada', 'CAN - Canada')
_t('settler', 'NEW - Newfoundland', 'MRU - Maritime Union',
   'COL - Columbia', 'AST - Australia', 'NZL - New Zealand',
   'SNZ - South Island')
_t('quebec', 'QUE - Quebec')
_t('frontier_mixed', 'MTC - Metis Confederacy', "RPL - Rupert's Land",
   'SMI - Sapmi')
_t('north_german', 'HAM - Hamburg', 'LUB - Lubeck', 'BRE - Bremen',
   'FRM - Frankfurt am Main', 'HAN - Hannover', 'BRA - Braunschweig',
   'ANH - Anhalt', 'MEC - Mecklenburg', 'OLD - Oldenburg', 'LIP - Lippe',
   'COB - Saxe', 'MEI - Saxe', 'WEI - Saxe', 'NAS - Nassau',
   'HEK - HesseKassel', 'HES - HesseDarmstadt', 'SWH - Schleswig-Holstein',
   'HOL - Holstein', 'SCH - Schleswig', 'EFR - East Frisia', 'WES - Westfalen',
   'RHI - Rhineland', 'SAA - Saar', 'SLS - Silesia', 'DZG - Danzig',
   'PML - Pomerelia', 'LUZ - Luzica', 'NGF - North German Fed')
_t('german_unified', 'GER - Germany')
_t('south_german', 'BAV - Bavaria', 'WUR - Wurttemberg', 'BAD - Baden',
   'AUS - Austria', 'SGF - South German Fed')
_t('habsburg_dual', 'KUK - Austria-Hungary', 'SLO - Slovenia', 'TRE - Trieste')
_t('bohemia', 'BOH - Bohemia', 'CZH - Czechoslovakia')
_t('hungary', 'HUN - Hungary', 'SLV - Slovakia', 'BAN - Banat',
   'DNB - Danubian Federation')
_t('habsburg_south', 'CRO - Croatia')
_t('eastern_catholic', 'GLM - Galicia-Lodomeria', 'BKV - Bukovina',
   'SYL - Transylvania', 'SIE - Siebenburgen', 'DLM - Dalmatia',
   'LIT - Lithuania', 'RUT - Ruthenia')
_t('france_belgium', 'FRA - France', 'BEL - Belgium', 'FLA - Flanders',
   'WLL - Wallonia', 'LUX - Luxemburg', 'ALS - Elsass')
_t('france_periphery', 'BRT - Brittany', 'OCC - Occitania')
_t('baltic_lutheran', 'EST - Estonia', 'LAT - Latvia',
   'UBD - United Baltic Provinces')
_t('north_italy', 'SAR - Sardinia', 'SRD - Sardinia', 'SVY - Savoy',
   'LOM - Lombardia', 'VEN - Venice', 'PAR - Parma', 'MOD - Modena',
   'TUS - Tuscany', 'LUC - Lucca', 'RMG - Romagna')
_t('italy_unified', 'ITA - Italy')
_t('south_italy', 'SIC - Two Sicilies', 'PAP - Papal States', 'MLT - Malta',
   'CRS - Corsica')
_t('iberia', 'SPA - Spain', 'SPC - Carlist Spain', 'CAT - Catalonia',
   'BSQ - Basqueland', 'IBR - Iberia')
_t('portugal', 'POR - Portugal', 'UPB - Portugal-Brazil')
_t('poland', 'POL - Poland', 'CPL - Congress Poland', 'KRA - Krakow',
   'PLC - Polish-Lithuanian Commonwealth', 'PZN - Poznan')
_t('russia', 'RUS - Russia', 'AKH - Astrakhan', 'BYE - Belarus',
   'UKR - Ukraine', 'CRI - Crimea', 'DON - Cossackia', 'KRL - Karelia',
   'TAR - Tatarstan', 'URA - Ural Republic')
_t('russia_frontier', 'ALT - Altai Republic', 'SIB - Siberian Republic',
   'YAK - Yakutia-Sakha', 'KAM - Far Eastern Federal District',
   'KMK - Kalmykia', 'LSK - Alaska')
_t('caucasus', 'GEO - Georgia', 'ARM - Armenia', 'CIR - Circassia',
   'DAG - Dagestan', 'TCA - Transcaucasia', 'AZB - Azerbaijan')
_t('greece', 'GRE - Greece', 'CRE - Crete', 'ION - Ionian Islands',
   'BYZ - Byzantium', 'PON - Pontus')
_t('balkan_ottoman', 'SER - Serbia', 'BUL - Bulgaria', 'MON - Montenegro',
   'WAL - Wallachia', 'MOL - Moldavia', 'ROM - Romania', 'BOS - Bosnia',
   'MCD - Macedonia', 'EPI - Epirus', 'YUG - Yugoslavia')
_t('balkan_muslim', 'ALB - Albania')
_t('ottoman', 'TUR - Ottoman Empire', 'CYP - Cyprus')
_t('ottoman_arab', 'IRQ - Iraq', 'SYR - Syria', 'PLS - Palestine',
   'JOR - Jordan', 'ISR - Israel', 'BAB - Babylonia')
_t('ottoman_christian', 'ASY - Assyria', 'LBN - Lebanon')
_t('egypt', 'EGY - Egypt')
_t('maghreb', 'MOR - Morocco', 'ALD - Aldjazair', 'TUN - Tunis',
   'TRI - Tripoli', 'CYR - Cyrenaica', 'LBY - Libya', 'MGH - Maghreb')
_t('arabia', 'ABU - Abu Dhabi', 'ARB - Arabia', 'ARU - Arab Union',
   'ASR - Asir', 'BHR - Bahrain', 'HAL - Hail', 'HDJ - Hedjaz', 'NEJ - Nejd',
   'OMA - Oman', 'KWT - Kuwait', 'YEM - Yemen', 'NYE - North Yemen')
_t('persia', 'PER - Persia', 'GLN - Gilan', 'KHR - Khorasan',
   'KHZ - Khuzestan')
_t('centralasia', 'AFG - Afghanistan', 'KDH - Kandahar', 'KNZ - Kunduz',
   'HZJ - Hazarajat', 'HRT - Herat', 'DUR - Durrani Empire', 'BUK - Bukkhara',
   'KHI - Khiva', 'KOK - Kokand', 'TKM - Turkmenistan', 'UZB - Uzbekistan',
   'TAJ - Tajikstan', 'KYR - Kyrgyzstan', 'KAZ - Kazakhstan',
   'TKS - Turkestan', 'BLC - Baluchistan', 'MAK - Makran', 'KAL - Kalat',
   'KDS - Kurdistan')
_t('himalaya', 'NEP - Nepal', 'BHU - Bhutan', 'SIK - Sikkim', 'LAD - Ladakh')
_t('india', 'HND - India', 'HDU - Hindustan', 'PAK - Pakistan', 'BNG - Bengal',
   'BIH - Bihar', 'ORI - Orissa', 'ASM - Assam', 'AWA - Awadh',
   'HYD - Hyderabad', 'MYS - Mysore', 'TRA - Travancore', 'KRN - Karnatak',
   'MAH - Maharashtra', 'MRT - Marathas', 'RAJ - Rajputana', 'JAI - Jaipur',
   'JOD - Jodhpur', 'JAS - Jaisalmer', 'BIK - Bikaner', 'MEW - Mewar',
   'IND - Indore', 'GWA - Gwalior', 'NAG - Nagpur', 'BUN - Bundelkhand',
   'BHO - Bhopal', 'BER - Beroda', 'KUT - Kutch', 'SIN - Sind', 'PNJ - Panjab',
   'KAS - Kashmir', 'BAS - Bastar', 'DRA - Dravidistan', 'SHI - Shimla',
   'SRI - Sri Lanka', 'MUG - Mughalistan')
_t('japan', 'TKG - Shogunate Japan', 'JAP - Japan', 'CHO - Choshu',
   'SAT - Satsuma', 'TOS - Tosa', 'KAG - Kaga', 'SEN - Sendai',
   'YZW - Yonezawa')
_t('ryukyu', 'RYU - Ryukyu')
_t('korea', 'KOR - Korea')
_t('qing', 'QNG', 'CHI - China', 'TPG - Taiping', 'KMT - Nationalist China',
   'GMJ - Guominjun', 'MCK - Manchukuo', 'FJN - Fujian', 'GNG - Guangdong',
   'GXI - Guangxi Clique', 'HNN - Hunan', 'HUI - Anhui', 'SXI - Shanxi',
   'SZC - Sichuan', 'YNN - Yunnan', 'XBI - Xibei San Ma', 'TAI - Taiwan')
_t('qing_frontier', 'TIB - Tibet', 'MGL - Mongolia', 'XIN - Xinjiang',
   'UYG - Uyghurstan', 'TNT - Tannu Tuva')
_t('seasia_buddhist', 'BUR - Burma', 'SIA - Siam', 'LNA - Lan Na',
   'LXA - Lan Xang', 'LUA - Luang Prabang', 'WIA - Wiang Chhan',
   'CHK - Champasak', 'CAM - Cambodia')
_t('seasia_confucian', 'DAI - Dai Viet')
_t('seasia', 'ATJ - Atjeh', 'BAL - Bali', 'BIM- Bima', 'BRU - Brunei',
   'DJA - Jambi', 'INO - Indonesia', 'JAV - Java', 'JOH - Johore',
   'KLM - Kalimantan', 'KTI - Kutai', 'LAN - Lanfang', 'MAL - Maluku',
   'MLY - Malaya', 'SAK - Siak', 'SLW - Sulawesi', 'SUL - Sulu',
   'SWK - Sarawak', 'SHA - Shan', 'KCH - Kachin')
_t('philippines', 'PHL - Philippines')
_t('pacific_tribal', 'AIN - Ainu', 'AOT - Aotearoa', 'CHE - Cherokee',
   'FIJ - Fiji', 'TGA - Tonga', 'HAW - Hawaii')
_t('latam_mid', 'MEX - Mexico', 'ARG - Argentina', 'CHL - Chile',
   'BRZ - Brazil', 'CLM - Colombia', 'GCO - Gran Colombia', 'VNZ - Venezuela',
   'URU - Uruguay', 'PRG - Paraguay', 'PNM - Panama', 'LPL - La Plata',
   'ENT - Entre Rios', 'RGS - Rio Grande do Sul')
_t('latam_low', 'BOL - Bolivia', 'ECU - Ecuador', 'PEU - Peru',
   'NPU - North Peru', 'SPU - South Peru',
   'PBC - Peru-Bolivian Confederation', 'PTG - Patagonia',
   'DOM - Dominican Republic', 'CHP - Chiapas', 'OAX - Oaxaca',
   'YUC - Yucatan', 'SON - Sonora', 'RGR - Rio Grande', 'UNM - New Mexico',
   'LOS - Los Altos')
_t('centam', 'GUA - Guatemala', 'HON - Honduras', 'NIC - Nicaragua',
   'COS - Costa Rica', 'ELS - El Salvador',
   'UCA - United States of Central America')
_t('caribbean', 'CUB - Cuba', 'PRI - Puerto Rico', 'JAM - Jamaica',
   'TTB - Trinidad & Tobago', 'ANC - Antillean Confederation', 'GUY - Guyana')
_t('haiti', 'HAI - Haiti')
_t('liberia', 'LIB - Liberia')
_t('boer', 'NAL - Natalia', 'ORA - Oranje', 'TRN - Transvaal',
   'SAF - South Africa')
_t('horn', 'ETH - Abyssinia', 'ETH - Ethiopia', 'GON - Gonder', 'SHW - Shewa',
   'TIG - Tigray', 'ERT - Eritrea', 'SOM - Somalia', 'MAJ - Majeerteen',
   'GEL - Geledi', 'AWS - Awsa')
_t('africa_muslim', 'SOK - Sokoto', 'KBO - Kanem-Bornu', 'DAM - Damagaram',
   'DAR - Darfur', 'MAS - Massina', 'TOU - Toucouleur', 'SEG - Segu',
   'WAD - Wadai', 'ADW - Adamawa', 'KRT - Kaarta', 'JAL - Jallon',
   'KNG - Kong', 'MOS - Mossi', 'DND - Dendi', 'BDU - Bondou', 'BMK - Bamako',
   'MLI - Mali', 'GBU - Gabu', 'WOL - Wolof', 'TRZ - Trarza',
   'ZAN - Zanzibar', 'SUD - Sudan')
_t('africa', 'ANG - Angola', 'ARO - Aro', 'ASH - Ashanti', 'AZA - Azande',
   'BEN - Benin', 'BRD - Urundi', 'BSH - Basotho', 'BUG - Buganda',
   'CAR - Central African Republic', 'CGO - Congo-Brazzaville', 'CHD - Chad',
   'CLA - Calabar', 'CMR - Cameroon', 'CNG - Congo Free State',
   'DAH - Dahomey', 'GAB - Gabon', 'GAZ - Gaza', 'GMB - Gambia',
   'GNE - Guinea', 'IVC - Ivory Coast', 'KNY - Kenya', 'KON - Kongo',
   'KUB - Kuba', 'KZB - Kazembe', 'LBA - Luba', 'LOA - Loango', 'LUN - Lunda',
   'MAD - Madagascar', 'MAT - Matabele', 'MLW - Malawi', 'MNG - Mongo',
   'MOZ - Mozambique', 'NGR - Nigeria', 'NIG - Niger', 'OYO - Oyo',
   'RHO - Southern Rhodesia', 'RWA - Ruanda', 'SLE - Sierra Leone',
   'SNG - Senegal', 'SHO - Shona', 'SUA - Suazi', 'TNZ - Tanzania',
   'TOG - Togo', 'TOO - Tooro', 'TSW - Botswana', 'WRI - Warri',
   'XHO - Xhosa', 'ZAM - Zambia', 'ZUL - Zulu')
_t('dynamic', *['D%02d' % i for i in range(1, 51)])

# no literacy line at all; nothing to set
SKIP = {'REB - Rebels'}

HEAD_RE = re.compile(r'^(\s*literacy\s*=\s*)([0-9.]+)')
DATE_RE = re.compile(r'^\s*1[89]\d\d\.\d+\.\d+\s*=')


def tag_of(stem):
    """Tag from a history filename stem. Handles 'QNG', 'D01' and 'BIM- Bima'."""
    return re.split(r'\s*-\s*', stem, 1)[0].strip()


def files():
    return sorted(f for f in os.listdir(CDIR) if f.endswith('.txt'))


def rewrite(path, value, dry):
    with open(path, 'r', newline='', encoding='cp1252') as fh:
        text = fh.read()
    lines = text.split('\n')          # CRLF survives as a trailing \r
    done = False
    for i, line in enumerate(lines):
        bare = line[:-1] if line.endswith('\r') else line
        if DATE_RE.match(bare):
            break                     # dated blocks are left flat
        if not done and HEAD_RE.match(bare):
            new = HEAD_RE.sub(lambda m: m.group(1) + ('%g' % value), bare, count=1)
            lines[i] = new + ('\r' if line.endswith('\r') else '')
            done = True
    if not done:
        return None
    out = '\n'.join(lines)
    if out != text and not dry:
        with open(path, 'w', newline='', encoding='cp1252') as fh:
            fh.write(out)
    return out != text


def main():
    dry = '--check' in sys.argv
    if '--doc' in sys.argv:
        print('| tier | literacy | justification | tags |')
        print('|---|---:|---|---|')
        for tier in sorted(TIERS, key=lambda t: (-TIERS[t][0], t)):
            tags = sorted(set(tag_of(s) for s in ASSIGN if ASSIGN[s] == tier))
            print('| `%s` | %.2f | %s | %s |'
                  % (tier, TIERS[tier][0], TIERS[tier][1], ', '.join(tags)))
        return 0
    missing = []
    changed = 0
    for f in files():
        stem = f[:-4]
        if stem in SKIP:
            continue
        tier = ASSIGN.get(stem)
        if tier is None:
            missing.append(stem)
            continue
        r = rewrite(os.path.join(CDIR, f), TIERS[tier][0], dry)
        if r is None:
            missing.append(stem + ' (no literacy line)')
        elif r:
            changed += 1
    for m in missing:
        print('UNASSIGNED: ' + m)
    print('%d files %s' % (changed, 'would change' if dry else 'changed'))
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main() or 0)
