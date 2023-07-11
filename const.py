import os, sys, time, json, copy

import scu
from scu import printc, printf, txt_c

SCALE = 1
FT = ('Consolas', SCALE*8)
FS = ('Consolas', SCALE*10)
FM = ('Consolas', SCALE*12)
FL = ('Consolas', SCALE*15)
FH = ('Consolas', SCALE*25)

PAD = (1,1)

FLAG_RUN = True

ADVANTAGE_RANGE_TALENT = (-6, 6)

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

COMBAT = [  ('Armbrüste',           (4,), 'B', False, 6),
            ('Bögen',               (4,), 'C', False, 6),
            ('Wurfwaffen',          (4,), 'B', False, 6),
            ('Dolche',              (5,), 'B', True, 6),
            ('Fechtwaffen',         (5,), 'C', True, 6),
            ('Hiebwaffen',          (7,), 'C', True, 6),
            ('Kettenwaffen',        (7,), 'C', False, 6),
            ('Lanzen',              (7,), 'B', True, 6),
            ('Raufen',              (5,7), 'B', True, 6),
            ('Schilde',             (7,), 'C', True, 6),
            ('Schwerter',           (5,7), 'C', True, 6),
            ('Stangenwaffen',       (5,7), 'C', True, 6),
            ('Zweihandhiebwaffen',  (7,), 'C', True, 6),
            ('Zweihandschwerter',   (7,), 'C', True, 6)]

TEXT_SIZE_TALENT_NAME = 42

def TALENT_STRING(Talent_ID):
    Talent = TALENTS[Talent_ID]
    pack = len(tuple(True for i in Talent[2] if CHAR['attr']['values'][i]['value'] > 12))
    Val = 4-(2+CHAR['talents']['TAL_'+str(Talent_ID+1)])//3
    if pack == 3 and Val < 4:
        Routine = '({:>+2.0f} QS{:1.0f})'.format(Val, max(1,(CHAR['talents']['TAL_'+str(Talent_ID+1)]/2-1)//3+1))
    elif pack == 2 and Val < 4:
        Routine = '({:>+2.0f}!)   '.format(Val)
    else:
        Routine = len('(NN QSN)')*' '
    return '{:20} {}/{}/{} {:>2.0f} {}'.format(Talent[0], ATTR_DECODE[Talent[2][0]], ATTR_DECODE[Talent[2][1]], ATTR_DECODE[Talent[2][2]], CHAR['talents']['TAL_'+str(Talent_ID+1)], Routine)
    

def load_cnfg():
    global CNFG
    global ADVANTAGE_RANGE_TALENT
    with open(sys.path[0]+'/cnfg.txt', 'r') as f:
        pack = f.readlines()
    pack = [x.replace('\n', '').replace(' ', '').split(':') for x in pack]
    CNFG = {x[0]: ':'.join(x[1:]) for x in pack}
    ADVANTAGE_RANGE_TALENT = (int(CNFG['Advantage_Range_Talent_Min']), int(CNFG['Advantage_Range_Talent_Max']))
    return True

def store_cnfg():
    return True

def load_character():
    global CHAR
    with open(CNFG['Character'], 'r') as f:
        pack = f.readlines()
    CHAR = json.loads(''.join(pack))
    return True

load_cnfg()
load_character()

printc('Version:', CNFG['Version'], Color='Grey')