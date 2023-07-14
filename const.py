import os, sys, time, json, copy

import scu
from scu import printc, printf, txt_c

SCALE = 1
FT = ('Consolas', SCALE*8)
FS = ('Consolas', SCALE*10)
FM = ('Consolas', SCALE*12)
FL = ('Consolas', SCALE*15)
FH = ('Consolas', SCALE*25)
FXH = ('Consolas', SCALE*50)
FXXH = ('Consolas', SCALE*100)

PAD = (1,1)
TAB_WIDTH = 130//4

FLAG_RUN = True

ATTR_DECODE = ['MU', 'KL', 'IN', 'CH', 'FF', 'GE', 'KO', 'KK']

TALENTS = [ ('Fliegen',                 'Körpertalente', (0,2,5), True, 'B'),
            ('Gaukeleien',              'Körpertalente', (0,3,4), True, 'A'),
            ('Klettern',                'Körpertalente', (0,5,6), True, 'B'),
            ('Körperbeherrschung',      'Körpertalente', (5,5,6), True, 'D'),
            ('Kraftakt',                'Körpertalente', (6,7,7), True, 'B'),
            ('Reiten',                  'Körpertalente', (3,5,7), True, 'B'),
            ('Schwimmen',               'Körpertalente', (5,6,7), True, 'B'),
            ('Selbstbeherrschung',      'Körpertalente', (0,0,6), False, 'D'),
            ('Singen',                  'Körpertalente', (1,3,6), None, 'A'),
            ('Sinnesschärfe',           'Körpertalente', (1,2,2), None, 'D'),
            ('Tanzen',                  'Körpertalente', (1,3,5), True, 'A'),
            ('Taschendiebstahl',        'Körpertalente', (0,4,5), True, 'B'),
            ('Verbergen',               'Körpertalente', (0,2,5), True, 'C'),
            ('Zechen',                  'Körpertalente', (1,6,7), False, 'A'),
            ('Überzeugen & Bekeh.',     'Gesellschaftstalente', (0,1,3), False, 'B'),
            ('Betören',                 'Gesellschaftstalente', (0,3,3), None, 'B'),
            ('Einschüchtern',           'Gesellschaftstalente', (0,2,3), False, 'B'),
            ('Etikette',                'Gesellschaftstalente', (1,2,3), None, 'B'),
            ('Gassenwissen',            'Gesellschaftstalente', (1,2,3), None, 'C'),
            ('Menschenkentniss',        'Gesellschaftstalente', (1,2,3), False, 'C'),
            ('Überreden',               'Gesellschaftstalente', (0,2,3), False, 'C'),
            ('Verkleiden',              'Gesellschaftstalente', (2,3,5), None, 'B'),
            ('Willenskraft',            'Gesellschaftstalente', (0,2,3), False, 'D'),
            ('Färtensuchen',            'Naturtalente', (0,3,5), True, 'C'),
            ('Fesseln',                 'Naturtalente', (1,4,7), None, 'A'),
            ('Fischen & Angeln',        'Naturtalente', (4,5,6), None, 'A'),
            ('Orientierung',            'Naturtalente', (1,2,2), False, 'B'),
            ('Pflanzenkunde',           'Naturtalente', (1,4,6), None, 'C'),
            ('Tierkunde',               'Naturtalente', (0,0,3), True, 'C'),
            ('Wildnisleben',            'Naturtalente', (0,5,6), True, 'C'),
            ('Brett & Glücksspiel',     'Wissenstalente', (1,1,2), False, 'A'),
            ('Geographie',              'Wissenstalente', (1,1,2), False, 'B'),
            ('Geschichtswissen',        'Wissenstalente', (1,1,2), False, 'B'),
            ('Götter & Kulte',          'Wissenstalente', (1,1,2), False, 'B'),
            ('Kriegskunst',             'Wissenstalente', (0,1,2), False, 'B'),
            ('Magiekunde',              'Wissenstalente', (1,1,2), False, 'C'),
            ('Mechanik',                'Wissenstalente', (1,1,4), False, 'B'),
            ('Rechnen',                 'Wissenstalente', (1,1,2), False, 'A'),
            ('Rechtskunde',             'Wissenstalente', (1,1,2), False, 'A'),
            ('Sagen & Legenden',        'Wissenstalente', (1,1,2), False, 'B'),
            ('Sphärenkunde',            'Wissenstalente', (1,1,2), False, 'B'),
            ('Sternkunde',              'Wissenstalente', (1,1,2), False, 'A'),
            ('Alchimie',                'Handwerkstalente', (0,1,4), True, 'C'),
            ('Boote & Schiffe',         'Handwerkstalente', (4,5,7), True, 'B'),
            ('Fahrzeuge',               'Handwerkstalente', (3,5,6), True, 'A'),
            ('Handel',                  'Handwerkstalente', (1,2,3), False, 'B'),
            ('Heilkunde Gift',          'Handwerkstalente', (0,1,2), True, 'B'),
            ('Heilkunde Krankh.',       'Handwerkstalente', (0,1,6), True, 'B'),
            ('Heilkunde Seele',         'Handwerkstalente', (2,3,6), False, 'B'),
            ('Heilkunde Wunden',        'Handwerkstalente', (1,4,4), True, 'D'),
            ('Holzbearbeitung',         'Handwerkstalente', (4,5,7), True, 'B'),
            ('Lebensmittelbear.',       'Handwerkstalente', (2,4,4), True, 'A'),
            ('Lederbearbeitung',        'Handwerkstalente', (4,5,6), True, 'B'),
            ('Malen & Zeichnen',        'Handwerkstalente', (2,4,4), True, 'A'),
            ('Metallbearbeitung',       'Handwerkstalente', (4,5,6), True, 'C'),
            ('Musizieren',              'Handwerkstalente', (3,4,6), True, 'A'),
            ('Schlösserknacken',        'Handwerkstalente', (2,4,4), True, 'C'),
            ('Steinbearbeitung',        'Handwerkstalente', (4,4,7), True, 'A'),
            ('Stoffbearbeitung',        'Handwerkstalente', (1,4,4), True, 'A')]

COMBAT = {  1:  ('Armbrüste',           (4,), 'B', False, 6, 'Ranged', True),
            2:  ('Bögen',               (4,), 'C', False, 6, 'Ranged', True),
            3:  ('Dolche',              (5,), 'B', True, 6, 'Melee', True),
            4:  ('Fechtwaffen',         (5,), 'C', True, 6, 'Melee', True),
            5:  ('Hiebwaffen',          (7,), 'C', True, 6, 'Melee', True),
            6:  ('Kettenwaffen',        (7,), 'C', False, 6, 'Melee', True),
            7:  ('Lanzen',              (7,), 'B', True, 6, 'Melee', True),
            8:  ('Peitschen',           (4,), 'B', False, 6, 'Melee', False),
            9:  ('Raufen',              (5,7), 'B', True, 6, 'Melee', True),
            10: ('Schilde',             (7,), 'C', True, 6, 'Melee', True),
            11: ('Schleudern',          (5,), 'B', False, 6, 'Ranged', False),
            12: ('Schwerter',           (5,7), 'C', True, 6, 'Melee', True),
            13: ('Stangenwaffen',       (5,7), 'C', True, 6, 'Melee', True),
            14: ('Wurfwaffen',          (4,), 'B', False, 6, 'Ranged', True),
            15: ('Zweihandhiebwaffen',  (7,), 'C', True, 6, 'Melee', True),
            17: ('> unknown <',         (5,), 'B', False, 6, 'Ranged', False),
            16: ('Zweihandschwerter',   (7,), 'C', True, 6, 'Melee', True),
            18: ('Blasrohre',           (5,), 'B', False, 6, 'Ranged', False),
            19: ('Diskusse',            (5,), 'B', False, 6, 'Ranged', False),
            20: ('> unknown <',         (5,), 'B', False, 6, 'Ranged', False)}

CANTRIPS =  {   7:  ('Lockruf')}

SPELLS =    {   1:  ('Adlerauge',               (1,2,4), '4AsP+2/5min', '2Akt', 'Self', '(A)', 'Heilung', 'B'),
                4:  ('Axxeleratus',             (1,2,4), '8Asp', '1Akt','Contact', 'QSx5KR', 'Heilung', 'B'),
                45: ('Wasseratem',              (1,2,6), '4AsP+2/5min', '8Akt', 'Contact', '(A)', 'Verwand.', 'B')}

LITURGIES = {   22: ('Objektsegen',             (0,2,3), '4Kap', '4Akt', 'Contact', 'QSx3h', 'allg', 'B'),
                48: ('Begnadeter Reiter',       (0,2,3), '8Kap', '2Akt', 'Self', '2h', 'Har', 'A'),
                68: ('Friedvoller Rausch',      (0,2,3), '8KaP', '8Akt*', '16 m', '2KR', 'Eks', 'B'),
                79: ('Heiliges Liebesspiel',    (0,2,3), '4KaP', '8Akt', 'Contact', 'QSx30min', 'Eks/Har', 'A'),
                131:('Berauschender Wein',      (0,2,3), '4KaP', '5min', 'Contact', 'Instant', 'Eks', 'A'),
                140:('Fest der Freude',         (0,2,3), '8KaP', '30min', 'Self', '6h', 'Eks', 'B')}

BLESSINGS = {   }

SPELL_PREFIXES = {'spells':'SPELL_', 'liturgies':'LITURGY_'}
SPELL_CATS = {'spells':SPELLS, 'liturgies':LITURGIES}

TEXT_SIZE_TALENT_NAME = 42
TEXT_SIZE_SPELL_NAME = 80

def TALENT_STRING(Talent_ID):
    Talent = TALENTS[Talent_ID]
    pack = len(tuple(True for i in Talent[2] if CHAR['attr']['values'][i]['value'] > 12))
    Val = 4-(2+CHAR['talents']['TAL_'+str(Talent_ID+1)])//3
    if CNFG['Talent_Routine_Unlock']:
        subpack = sum(max(13 - CHAR['attr']['values'][i]['value'], 0) for i in Talent[2])
        Val = 4-(2+CHAR['talents']['TAL_'+str(Talent_ID+1)]-3*subpack)//3        
        if pack == 3 and Val < 4:
            Routine = '({:>+2.0f} QS{:1.0f})'.format(Val, max(1,(CHAR['talents']['TAL_'+str(Talent_ID+1)]/2-1)//3+1))
        elif pack == 2 and Val < 4:
            Routine = '({:>+2.0f}!)'.format(Val)
        else:
            Routine = ''
    else:
        if pack == 3 and Val < 4:
            Routine = '({:>+2.0f} QS{:1.0f})'.format(Val, max(1,(CHAR['talents']['TAL_'+str(Talent_ID+1)]/2-1)//3+1))
        elif pack == 2 and Val < 4:
            Routine = '({:>+2.0f}!)'.format(Val)
        else:
            Routine = ''
    return '{:^20} {:>2}/{:>2}/{:>2} {:>2} {:<8}'.format(Talent[0], ATTR_DECODE[Talent[2][0]], ATTR_DECODE[Talent[2][1]], ATTR_DECODE[Talent[2][2]], CHAR['talents']['TAL_'+str(Talent_ID+1)], Routine)
    
def SPELL_STRING(Spell_ID, Spelltype):
    Spell = SPELL_CATS[Spelltype][Spell_ID]
    Spell_prefix = SPELL_PREFIXES[Spelltype]
    return '{:^22} {:>2}/{:>2}/{:>2} {:>2} {:^12} {:^5} {:^8} {:^8}'.format(Spell[0], ATTR_DECODE[Spell[1][0]], ATTR_DECODE[Spell[1][1]], ATTR_DECODE[Spell[1][2]], CHAR[Spelltype][Spell_prefix+str(Spell_ID)], Spell[2], Spell[3], Spell[4], Spell[5])

def COMBAT_STRING(Combat_ID):
    Combat = COMBAT[Combat_ID]
    if len(Combat[1]) == 1:
        Atr = ATTR_DECODE[Combat[1][0]]
    else:
        Atr = ATTR_DECODE[Combat[1][0]] + '/' + ATTR_DECODE[Combat[1][1]]
    if 'CT_'+str(Combat_ID) in CHAR['ct']:
        Val = CHAR['ct']['CT_'+str(Combat_ID)]
    else:
        Val = Combat[4]
    if Combat[5] == 'Melee':
        Atk = Val + (CHAR['attr']['values'][0]['value']-8)//3
    else:
        Atk = Val + (CHAR['attr']['values'][5]['value']-8)//3
    if Combat[3]:
        Pa = Val / 2 + max(((CHAR['attr']['values'][i]['value']-8)//3 for i in Combat[1]))
        Par = '{:2.0f}'.format(Pa)
    else:
        Pa = 0
        Par = 'X'
    return '{:^20}  {:>5}  {:>2}  {:>2}  {:>2}'.format(Combat[0], Atr, Val, Atk, Par), (Atk, Pa)

def load_cnfg():
    global CNFG
    with open(sys.path[0]+'/CNFG.json', 'r') as f:
        pack = f.readlines()
    CNFG = json.loads(''.join(pack))
    return True

def store_cnfg():
    global CNFG
    with open(sys.path[0]+'/CNFG.json', 'w') as f:
        f.write(json.dumps(CNFG, indent=0))
    return True

def load_character():
    global CHAR
    global CNFG
    try:
        with open(CNFG['Character_File'], 'r') as f:
            pack = f.readlines()
    except FileNotFoundError:
        printc('> Error in Filepath to Character file, switching to default', Color='R')
        CNFG['Character_File'] = sys.path[0]+'/Theariel.json'
        store_cnfg()
        with open(CNFG['Character_File'], 'r') as f:
            pack = f.readlines()        
    CHAR = json.loads(''.join(pack))
    return True

load_cnfg()
load_character()

printc('Version:', CNFG['Version'], Color='Grey')