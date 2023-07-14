import os, sys, time, json, copy

import scu
from scu import printc, printf, txt_c

scu.imports('numpy', 'PySimpleGUI')
import numpy as np
import PySimpleGUI as sg

import const
import dsa_talents

printc('===> DSA fastroll <===', Color='Y')

sg.theme('DarkBlue2')
sg.theme_button_color((sg.theme_text_color() ,'#20405F'))

def layout_table(title, content, key=''):
    sx = [max(tuple(len(line[i]) for line in content)) for i in range(len(content[0]))]
    layout = [[sg.Text(k, size=(sx[i], 1), font=const.FS) for i, k in enumerate(line)] for line in content]
    return sg.Frame(key='F_table:'+key, layout=layout, element_justification='c', vertical_alignment='c', title=title, title_location='n', font=const.FS)

Talent_ID = None
Spell_ID = None
Combat_ID = None
Spell_IDs = []

layout_tab_die_B = [[sg.Text('', key='T_die_result_1', size=(12,1), font=const.FXXH, justification='c')],
                    [sg.Text('', key='T_die_result_2', size=(12,1), font=const.FH, justification='c')]]

layout_tab_die =    [[sg.Frame(key='F_tab_die', layout=layout_tab_die_B, element_justification='c', vertical_alignment='c', title='Ergebnisse', title_location='n', font=const.FH)],
                    [sg.Column(vertical_alignment='t',
                                    layout=[[sg.Button(button_text='1 W 2', key='B_die_1W2', size=(10,1), font=const.FL, border_width=0)]]),
                        sg.Column(vertical_alignment='t',
                                    layout=[[sg.Button(button_text='1 W 3', key='B_die_1W3', size=(10,1), font=const.FL, border_width=0)]]),
                        sg.Column(vertical_alignment='t',
                                    layout=[[sg.Button(button_text='1 W 6', key='B_die_1W6', size=(10,1), font=const.FL, border_width=0)],
                                            [sg.Button(button_text='2 W 6', key='B_die_2W6', size=(10,1), font=const.FL, border_width=0)],
                                            [sg.Button(button_text='3 W 6', key='B_die_3W6', size=(10,1), font=const.FL, border_width=0)]]),
                        sg.Column(vertical_alignment='t',
                                    layout=[[sg.Button(button_text='1 W 20', key='B_die_1W20', size=(10,1), font=const.FL, border_width=0)],
                                            [sg.Button(button_text='2 W 20', key='B_die_2W20', size=(10,1), font=const.FL, border_width=0)],
                                            [sg.Button(button_text='3 W 20', key='B_die_3W20', size=(10,1), font=const.FL, border_width=0)]])
                    ]]

layout_tab_talents_1A = [[sg.Frame(title='Körpertalente', font=const.FM, element_justification='c', title_location='n',
                            layout=[[sg.Button(const.TALENT_STRING(i), key='B_talent_select:'+str(i), size=(const.TEXT_SIZE_TALENT_NAME, 1), font=const.FT, pad=const.PAD, border_width=0)] for i, k in enumerate(const.TALENTS) if k[1] == 'Körpertalente'])]]
layout_tab_talents_1B = [[sg.Frame(title='Gesellschaftstalente', font=const.FM, element_justification='c', title_location='n',
                            layout=[[sg.Button(const.TALENT_STRING(i), key='B_talent_select:'+str(i), size=(const.TEXT_SIZE_TALENT_NAME, 1), font=const.FT, pad=const.PAD, border_width=0)] for i, k in enumerate(const.TALENTS) if k[1] == 'Gesellschaftstalente'])],
                        [sg.Frame(title='Naturtalente', font=const.FM, element_justification='c', title_location='n',
                            layout=[[sg.Button(const.TALENT_STRING(i), key='B_talent_select:'+str(i), size=(const.TEXT_SIZE_TALENT_NAME, 1), font=const.FT, pad=const.PAD, border_width=0)] for i, k in enumerate(const.TALENTS) if k[1] == 'Naturtalente'])]]
layout_tab_talents_1C = [[sg.Frame(title='Wissenstalente', font=const.FM, element_justification='c', title_location='n',
                            layout=[[sg.Button(const.TALENT_STRING(i), key='B_talent_select:'+str(i), size=(const.TEXT_SIZE_TALENT_NAME, 1), font=const.FT, pad=const.PAD, border_width=0)] for i, k in enumerate(const.TALENTS) if k[1] == 'Wissenstalente'])]]
layout_tab_talents_1D = [[sg.Frame(title='Handwerkstalente', font=const.FM, element_justification='c', title_location='n',
                            layout=[[sg.Button(const.TALENT_STRING(i), key='B_talent_select:'+str(i), size=(const.TEXT_SIZE_TALENT_NAME, 1), font=const.FT, pad=const.PAD, border_width=0)] for i, k in enumerate(const.TALENTS) if k[1] == 'Handwerkstalente'])]]

layout_tab_talents_2A = [[sg.Text('Talent', key='T_talents_talent', size=(const.TEXT_SIZE_TALENT_NAME, 1), font=const.FM, justification='c')],
                        [sg.Frame(title='D'+str(i), key='F_talents_D'+str(i), element_justification='c', vertical_alignment='c', title_location='n', font=const.FH, 
                            layout=[[sg.Text('Target:  -', key='T_talents_DA'+str(i), size=(16, 1), font=const.FM, justification='c')],
                                    [sg.Text('-', key='T_talents_DR'+str(i), size=(4, 1), font=const.FXH, justification='c')]]) for i in range(3)],
                        [sg.Text('', key='T_talents_crit', size=(20, 1), font=const.FH, justification='c')]]
layout_tab_talents_2B = ([[sg.Text('Adv', font=const.FS, justification='c')]] +
                            [[sg.Text('{:>+3.0f}'.format(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.CNFG['Advantage_Range_Talent'][0], const.CNFG['Advantage_Range_Talent'][1]+1)]
                            )
layout_tab_talents_2C = ([[sg.Text('QS', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_talents_QS_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.CNFG['Advantage_Range_Talent'][0], const.CNFG['Advantage_Range_Talent'][1]+1)]
                            )
layout_tab_talents_2D = ([[sg.Text('Succ', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_talents_succ_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.CNFG['Advantage_Range_Talent'][0], const.CNFG['Advantage_Range_Talent'][1]+1)]
                            )
layout_tab_talents_2E = ([[sg.Text('Fail', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_talents_fail_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.CNFG['Advantage_Range_Talent'][0], const.CNFG['Advantage_Range_Talent'][1]+1)]
                            )
layout_tab_talents_2F = ([[sg.Text('Exp QS', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_talents_exp_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.CNFG['Advantage_Range_Talent'][0], const.CNFG['Advantage_Range_Talent'][1]+1)]
                            )

layout_tab_talents =    [[sg.Frame(key='F_talents_die_rolling', layout=layout_tab_talents_2A, element_justification='c', vertical_alignment='c', title='Die rolling', title_location='n', font=const.FL),
                            sg.Column(layout=layout_tab_talents_2B, element_justification='c', vertical_alignment='c'),
                            sg.Column(layout=layout_tab_talents_2C, element_justification='c', vertical_alignment='c'),
                            sg.Column(layout=layout_tab_talents_2D, element_justification='c', vertical_alignment='c'),
                            sg.Column(layout=layout_tab_talents_2E, element_justification='c', vertical_alignment='c'),
                            sg.Column(layout=layout_tab_talents_2F, element_justification='c', vertical_alignment='c')],
                        [sg.Column(layout=layout_tab_talents_1A, element_justification='c', vertical_alignment='t'),
                            sg.Column(layout=layout_tab_talents_1B, element_justification='c', vertical_alignment='t'),
                            sg.Column(layout=layout_tab_talents_1C, element_justification='c', vertical_alignment='t'),
                            sg.Column(layout=layout_tab_talents_1D, element_justification='c', vertical_alignment='t')]]

Spell_Title_Text = '{:^22} {:^8} {:^2} {:^12} {:^5} {:^8} {:^8}'.format('Zauber / Liturgie', 'Probe', 'FW', 'Kosten', 'Dauer', 'Range', 'Wirkung')
layout_tab_spells_1A = ([[sg.Text(Spell_Title_Text, size=(const.TEXT_SIZE_SPELL_NAME,1), font=const.FS, justification='c')]]+
                            [[sg.Button(button_text='', key='B_spells_select:'+str(i), size=(const.TEXT_SIZE_SPELL_NAME,1), font=const.FS, pad=const.PAD, border_width=0)] for i in range(0, 30, 2)])
layout_tab_spells_1B = ([[sg.Text(Spell_Title_Text, size=(const.TEXT_SIZE_SPELL_NAME,1), font=const.FS, justification='c')]]+
                            [[sg.Button(button_text='', key='B_spells_select:'+str(i), size=(const.TEXT_SIZE_SPELL_NAME,1), font=const.FS, pad=const.PAD, border_width=0)] for i in range(1, 31, 2)])

layout_tab_spells_2A = [[sg.Text('Zauber / Liturgie', key='T_spells_spell', size=(const.TEXT_SIZE_SPELL_NAME, 1), font=const.FM, justification='c')],
                        [sg.Frame(title='D'+str(i), key='F_spells_D'+str(i), element_justification='c', vertical_alignment='c', title_location='n', font=const.FH, 
                            layout=[[sg.Text('Target:  -', key='T_spells_DA'+str(i), size=(16, 1), font=const.FM, justification='c')],
                                    [sg.Text('-', key='T_spells_DR'+str(i), size=(4, 1), font=const.FXH, justification='c')]]) for i in range(3)],
                        [sg.Text('', key='T_spells_crit', size=(20, 1), font=const.FH, justification='c')]]
layout_tab_spells_2B = ([[sg.Text('Adv', font=const.FS, justification='c')]] +
                            [[sg.Text('{:>+3.0f}'.format(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.CNFG['Advantage_Range_Spell'][0], const.CNFG['Advantage_Range_Spell'][1]+1)]
                            )
layout_tab_spells_2C = ([[sg.Text('QS', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_spells_QS_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.CNFG['Advantage_Range_Spell'][0], const.CNFG['Advantage_Range_Spell'][1]+1)]
                            )
layout_tab_spells_2D = ([[sg.Text('Succ', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_spells_succ_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.CNFG['Advantage_Range_Spell'][0], const.CNFG['Advantage_Range_Spell'][1]+1)]
                            )
layout_tab_spells_2E = ([[sg.Text('Fail', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_spells_fail_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.CNFG['Advantage_Range_Spell'][0], const.CNFG['Advantage_Range_Spell'][1]+1)]
                            )
layout_tab_spells_2F = ([[sg.Text('Exp QS', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_spells_exp_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.CNFG['Advantage_Range_Spell'][0], const.CNFG['Advantage_Range_Spell'][1]+1)]
                            )

layout_tab_spells = [[sg.Frame(key='F_spells_die_rolling', layout=layout_tab_spells_2A, element_justification='c', vertical_alignment='c', title='Die rolling', title_location='n', font=const.FL),
                            sg.Column(layout=layout_tab_spells_2B, element_justification='c', vertical_alignment='c'),
                            sg.Column(layout=layout_tab_spells_2C, element_justification='c', vertical_alignment='c'),
                            sg.Column(layout=layout_tab_spells_2D, element_justification='c', vertical_alignment='c'),
                            sg.Column(layout=layout_tab_spells_2E, element_justification='c', vertical_alignment='c'),
                            sg.Column(layout=layout_tab_spells_2F, element_justification='c', vertical_alignment='c')],
                    [sg.Column(layout=layout_tab_spells_1A, element_justification='c', vertical_alignment='t'),
                        sg.Column(layout=layout_tab_spells_1B, element_justification='c', vertical_alignment='t')]]

layout_tab_combat_A = ([[sg.Text('{:^20}  {:>5}  {:>2}  {:>2}  {:>2}'.format('Kampftechnik', '', 'KW', 'AT', 'PA'), size=(40,1), font=const.FM)]]+
                       [[sg.Button(const.COMBAT_STRING(k)[0], key='B_combat_select:'+str(k), size=(40,1), font=const.FM, border_width=0, pad=const.PAD)] for k in const.COMBAT if const.COMBAT[k][-1] or const.CNFG['Extended_Combat_Talents']])

layout_tab_combat_BX = [[sg.Text('Kampftechnik', key='T_combat_combat', size=(40, 1), font=const.FM, justification='c')],
                        [sg.Frame(title='D'+str(i), key='F_combat_D'+str(i), element_justification='c', vertical_alignment='c', title_location='n', font=const.FH, 
                            layout=[[sg.Text('Target:  -', key='T_combat_DA'+str(i), size=(16, 1), font=const.FM, justification='c')],
                                    [sg.Text('-', key='T_combat_DR'+str(i), size=(4, 1), font=const.FXH, justification='c')]]) for i in range(2)],
                        [sg.Text('', key='T_combat_crit', size=(20, 1), font=const.FH, justification='c')]]

layout_tab_combat_side = [[sg.Frame(key='F_combat_die_rolling', layout=layout_tab_combat_BX, element_justification='c', vertical_alignment='c', title='Die rolling', title_location='n', font=const.FL)],
                          [sg.Frame(key='F_combat_info_M', element_justification='c', vertical_alignment='c', title='Melee Modifiers', title_location='n', font=const.FL,
                            layout=[[layout_table('Target Size',
                                        [   ['Winzig:', '-4 AT'],
                                            [' Klein:', '-'],
                                            ['Mittel:', '-'],
                                            ['  Groß:', 'dodge / shield'],
                                            ['Riesig:', 'only dodge']], 'KI0'),
                            layout_table('Combat Space',
                                        [   ['         Kurz:', '-'],
                                            ['       Mittel:', '-4 AT, -4 PA'],
                                            ['         Lang:', '-8 AT, -8 PA'],
                                            [' Small Shield:', '-2 AT, -2 PA'],
                                            ['Medium Shield:', '-4 AT, -3 PA'],
                                            [' Large Shield:', '-6 AT, -4 PA']], 'KI1'),
                            layout_table(' Range Disadvantage',
                                        [   ['      ', '  Kurz', 'Mittel', '  Lang'],
                                            ['  Kurz', '  -   ', ' -2 AT', ' -4 AT'],
                                            ['Mittel', ' -2 AT', ' -    ', ' -2 AT'],
                                            ['  Lang', ' -4 AT', ' -2 AT', '  -   ']], 'KI2')]])],
                          [sg.Frame(key='F_combat_info_R', element_justification='c', vertical_alignment='c', title='Ranged Modifiers', title_location='n', font=const.FL,
                            layout=[[layout_table('Movement',
                                        [   ['      Ziel still:', '+2 FK'],
                                            ['   Ziel <4m/turn:', '-'],
                                            ['   Ziel >5m/turn:', '-2 FK'],
                                            ['     Ziehl haken:', '-4 FK, Ziehl GS/2'],
                                            ['Schütze <4m/turn:', '-2 FK'],
                                            ['Schütze >5m/turn:', '-4 FK']], 'KI3'),
                            layout_table('Target Distance',
                                        [   ['   Nah:', '+2 FK, +1 TP'],
                                            ['Mittel:', '-'],
                                            ['  Weit:', '-2 FK, -1 TP']], 'KI4'),
                            layout_table('Target Size',
                                        [   ['Winzig:', '-8 FK'],
                                            [' Klein:', '-4 FK'],
                                            ['Mittel:', '-'],
                                            ['  Groß:', '+4 FK'],
                                            ['Riesig:', '+8 FK']], 'KI5'),
                            layout_table('Defense',
                                        [   ['Schusswaffe:', '-4 Def'],
                                            ['  Wurfwaffe:', '-2 Def']], 'KI6')]])]]

layout_tab_combat = [[sg.Column(layout=layout_tab_combat_A, element_justification='c', vertical_alignment='t'),
                        sg.Column(key='Col_combat_side', layout=layout_tab_combat_side, element_justification='c', vertical_alignment='t')]]

layout_tabs = [[sg.Tab(title='Würfel'.center(const.TAB_WIDTH, ' '), key='Tab_die', layout=layout_tab_die, element_justification='c'),
                    sg.Tab(title='Fertigkeiten'.center(const.TAB_WIDTH, ' '), key='Tab_abilities', layout=layout_tab_talents, element_justification='c'),
                    sg.Tab(title='Zauber & Liturgien'.center(const.TAB_WIDTH, ' '), key='Tab_spells', layout=layout_tab_spells, element_justification='c'),
                    sg.Tab(title='Kampf'.center(const.TAB_WIDTH, ' '), key='Tab_combat', layout=layout_tab_combat, element_justification='c')]]

layout =    [[sg.Input(key='I_Char_select', visible=False, enable_events=True),
                sg.FileBrowse('Character', key='B_Char_Select', target=(sg.ThisRow, 0), file_types=(('JSON files','*.json'), ("ALL Files","*.*")), initial_folder=sys.path[0], tooltip='Select character file', font=const.FM),
                sg.Text(const.CHAR['name'], key='T_Char_select', s=(20,1), font=const.FM),
                sg.Text('    '.join([const.ATTR_DECODE[i]+': {:>2.0f}'.format(const.CHAR['attr']['values'][i]['value']) for i in range(8)]), key='T_Char_attributes', font=const.FM, justification='c')],
            [sg.TabGroup(layout=layout_tabs, key='TabG_Main', font=const.FM)]]
            

window = sg.Window(title='DSApy '+const.CNFG['Version'], layout=layout)
window.finalize()
window['T_Char_attributes'].expand(expand_x=True, expand_y=False)
window['F_talents_die_rolling'].expand(expand_x=True, expand_y=True)
window['F_spells_die_rolling'].expand(expand_x=True, expand_y=True)
window['Col_combat_side'].expand(expand_x=True, expand_y=True)
window['F_combat_die_rolling'].expand(expand_x=True, expand_y=False)
window['F_combat_D0'].update('Attacke')
window['F_combat_D1'].update('Parade')
window['F_combat_info_M'].expand(expand_x=True, expand_y=True)
window['F_combat_info_R'].expand(expand_x=True, expand_y=True)

def die_roll(Count, Size, Simroll):
    printc('> Rolling for: {:.0f}W{:.0f}'.format(Count, Size), Color='M')
    if Simroll:
        for t in range(10):
            roll = np.random.randint(1, Size+1, Count)
            window['T_die_result_1'].update(' '.join(['{:2.0f}']*Count).format(*roll))
            window.refresh()
            time.sleep(1/((10-t)*5))
    roll = np.random.randint(1, Size+1, Count)
    window['T_die_result_1'].update(' '.join(['{:2.0f}']*Count).format(*roll))
    if Count > 1:
        window['T_die_result_2'].update('Summe: {:.0f}'.format(np.sum(roll)))
    else:
        window['T_die_result_2'].update('')
    printc('Die results:', roll, Color='Grey')

def set_character():
    global Spelltype, Spellprefix, Spell_IDs
    printc('> Character file:', const.CNFG['Character'], Color='M')
    printc('{:<16} {}'.format('Character name:', const.CHAR['name']), Color='Grey')
    const.store_cnfg()
    const.load_character()
    window['T_Char_select'].update(const.CHAR['name'])
    window['T_Char_attributes'].update('  '.join([const.ATTR_DECODE[i]+': {:>2.0f}'.format(const.CHAR['attr']['values'][i]['value']) for i in range(8)]))            
    for i in range(59):
        window['B_talent_select:'+str(i)].update(const.TALENT_STRING(i))
    Spelltype, Spelprefix = None, None
    if len(const.CHAR['spells']) > 0:
        Spelltype = 'spells'
        Spellprefix = const.SPELL_PREFIXES[Spelltype]
    elif len(const.CHAR['liturgies']) > 0:
        Spelltype = 'liturgies'
        Spellprefix = const.SPELL_PREFIXES[Spelltype]
    printc('{:<16} {}'.format('Spelltype:', Spelltype), Color='Grey')
    if not Spelltype is None:
        window['Tab_spells'].update(disabled=False)
        Spell_IDs = []
        for i in range(30):
            if i < len(const.CHAR[Spelltype]):
                try:
                    Spell_IDs.append(int(list(const.CHAR[Spelltype])[i].split('_')[1]))
                    window['B_spells_select:'+str(i)].update(text=const.SPELL_STRING(Spell_IDs[-1], Spelltype), visible=True)
                except KeyError:
                    window['B_spells_select:'+str(i)].update(visible=False)
                    printc('X> SPELL / LITURGIE NOT FOUND:',list(const.CHAR[Spelltype])[i], Color='R', Style='B')
            else:
                window['B_spells_select:'+str(i)].update(visible=False)
    else:
        window['Tab_spells'].update(disabled=True)
    for i in const.COMBAT:
        if const.COMBAT[i][-1] or const.CNFG['Extended_Combat_Talents']:
            window['B_combat_select:'+str(i)].update(const.COMBAT_STRING(i)[0])
    return True

set_character()
window.refresh()

while const.FLAG_RUN:
    event, values = window.read()

    # ==================================================================== EVENT
    if event in (sg.WIN_CLOSED,):
        const.FLAG_RUN = False

    # ==================================================================== EVENT
    elif event == 'I_Char_select':
        if not values['I_Char_select'] == '':
            const.CNFG['Character_File'] = values['I_Char_select']
        set_character()

    # ==================================================================== EVENT
    elif 'B_die_' in event:
        pack = event.split('_')[-1].split('W')
        die_roll(int(pack[0]), int(pack[1]), const.CNFG['Simroll'])

    # ==================================================================== EVENT
    elif 'B_talent_select:' in event:
        temp = int(event.split(':')[1])
        talent_flag = Talent_ID == temp
        Talent_ID = int(event.split(':')[1])
        Talent_Value = const.CHAR['talents']['TAL_'+str(Talent_ID+1)]
        window['T_talents_talent'].update(const.TALENT_STRING(Talent_ID))
        printc('>', 'Rolling for:', const.TALENTS[Talent_ID][0], Color='M')
        Targets = np.array([const.CHAR['attr']['values'][x]['value'] for x in const.TALENTS[Talent_ID][2]])
        printc('Die targets:', Targets, Color='Grey')

        for i in range(3):
            window['F_talents_D'+str(i)].update(const.ATTR_DECODE[const.TALENTS[Talent_ID][2][i]])
            window['T_talents_DA'+str(i)].update('Target: {:>2.0f}'.format(Targets[i]))

        if const.CNFG['Simroll']:
            for t in range(10):
                Results = np.random.randint(1, 21, 3)
                for i in range(3):
                    window['T_talents_DR'+str(i)].update('{:2.0f}'.format(Results[i]))
                window.refresh()
                time.sleep(1/((10-t)*5))

        Results = np.random.randint(1, 21, 3)
        printc('Die results:', Results, Color='Grey')
        for i in range(3):
            window['T_talents_DR'+str(i)].update('{:2.0f}'.format(Results[i]))

        flag_crit = None
        if np.count_nonzero(Results == 1) == 2:
            flag_crit = True
            window['T_talents_crit'].update('Critical Succes')
        elif np.count_nonzero(Results == 1) == 3:
            flag_crit = True
            window['T_talents_crit'].update('SUPER CRICTICAL SUCCESS')
        elif np.count_nonzero(Results == 20) == 2:
            flag_crit = True
            window['T_talents_crit'].update('Critical Fail')
        elif np.count_nonzero(Results == 20) == 3:
            flag_crit = True
            window['T_talents_crit'].update('SUPER CRITICAL FAIL')
        else:
            window['T_talents_crit'].update('')      

        for i in range(const.CNFG['Advantage_Range_Talent'][0], const.CNFG['Advantage_Range_Talent'][1]+1):
            Rem = Talent_Value
            for a in range(3):
                Rem -= max(0, Results[a] - i - Targets[a])
            if flag_crit:
                window['T_talents_QS_'+str(i)].update('Crit')
            elif Rem < 0:
                window['T_talents_QS_'+str(i)].update('Fail')
            else:
                window['T_talents_QS_'+str(i)].update(str(max(1,(Rem-1)//3+1)))

        if (not talent_flag) and not const.CNFG['Disable_Chances']: 
            window.refresh()
            talent_simulation = dsa_talents.simulate_talent(const.CNFG['Advantage_Range_Talent'], Targets, Talent_Value)
            for i in range(const.CNFG['Advantage_Range_Talent'][0], const.CNFG['Advantage_Range_Talent'][1]+1):
                window['T_talents_succ_'+str(i)].update('{:>4.1f}%'.format(talent_simulation[i][0]*100))
                window['T_talents_fail_'+str(i)].update('{:>4.1f}%'.format(talent_simulation[i][1]*100))
                window['T_talents_exp_'+str(i)].update('{:>3.1f}'.format(talent_simulation[i][2]))

    # ==================================================================== EVENT
    elif 'B_spells_select:' in event:
        temp = int(event.split(':')[1])
        spell_flag = Spell_ID == temp
        Spell_ID = Spell_IDs[int(event.split(':')[1])]
        Spell_Value = const.CHAR[Spelltype][Spellprefix+str(Spell_ID)]
        Spell = const.SPELL_CATS[Spelltype][Spell_ID]
        window['T_spells_spell'].update(const.SPELL_STRING(Spell_ID, Spelltype)[:34])
        printc('>', 'Rolling for:', Spell[0], Color='M')
        Targets = np.array([const.CHAR['attr']['values'][x]['value'] for x in Spell[1]])
        printc('Die targets:', Targets, Color='Grey')

        for i in range(3):
            window['F_spells_D'+str(i)].update(const.ATTR_DECODE[Spell[1][i]])
            window['T_spells_DA'+str(i)].update('Target: {:>2.0f}'.format(Targets[i]))

        if const.CNFG['Simroll']:
            for t in range(10):
                Results = np.random.randint(1, 21, 3)
                for i in range(3):
                    window['T_spells_DR'+str(i)].update('{:2.0f}'.format(Results[i]))
                window.refresh()
                time.sleep(1/((10-t)*5))

        Results = np.random.randint(1, 21, 3)
        printc('Die results:', Results, Color='Grey')
        for i in range(3):
            window['T_spells_DR'+str(i)].update('{:2.0f}'.format(Results[i]))

        flag_crit = None
        if np.count_nonzero(Results == 1) == 2:
            flag_crit = True
            window['T_spells_crit'].update('Critical Succes')
        elif np.count_nonzero(Results == 1) == 3:
            flag_crit = True
            window['T_spells_crit'].update('SUPER CRICTICAL SUCCESS')
        elif np.count_nonzero(Results == 20) == 2:
            flag_crit = True
            window['T_spells_crit'].update('Critical Fail')
        elif np.count_nonzero(Results == 20) == 3:
            flag_crit = True
            window['T_spells_crit'].update('SUPER CRITICAL FAIL')
        else:
            window['T_spells_crit'].update('')      

        for i in range(const.CNFG['Advantage_Range_Spell'][0], const.CNFG['Advantage_Range_Spell'][1]+1):
            Rem = Spell_Value
            for a in range(3):
                Rem -= max(0, Results[a] - i - Targets[a])
            if flag_crit:
                window['T_spells_QS_'+str(i)].update('Crit')
            elif Rem < 0:
                window['T_spells_QS_'+str(i)].update('Fail')
            else:
                window['T_spells_QS_'+str(i)].update(str(max(1,(Rem-1)//3+1)))

        if (not spell_flag) and not const.CNFG['Disable_Chances']: 
            window.refresh()
            talent_simulation = dsa_talents.simulate_talent(const.CNFG['Advantage_Range_Spell'], Targets, Spell_Value)
            for i in range(const.CNFG['Advantage_Range_Spell'][0], const.CNFG['Advantage_Range_Spell'][1]+1):
                window['T_spells_succ_'+str(i)].update('{:>4.1f}%'.format(talent_simulation[i][0]*100))
                window['T_spells_fail_'+str(i)].update('{:>4.1f}%'.format(talent_simulation[i][1]*100))
                window['T_spells_exp_'+str(i)].update('{:>3.1f}'.format(talent_simulation[i][2]))

    # ==================================================================== EVENT
    elif 'B_combat_select:' in event:
        temp = int(event.split(':')[1])
        combat_flag = Combat_ID == temp
        Combat_ID = int(event.split(':')[1])
        Combat = const.COMBAT[Combat_ID]
        Data = const.COMBAT_STRING(Combat_ID)
        window['T_combat_combat'].update(Data[0][:20])
        printc('>', 'Rolling for:', Combat[0], Color='M')
        Targets = np.array(Data[1]).astype(int)
        printc('Die targets:', Targets, Color='Grey')

        window['T_combat_DA0'].update('Target: {:>2.0f}'.format(Targets[0]))
        if Combat[3]:
            window['T_combat_DA1'].update('Target: {:>2.0f}'.format(Targets[1]))
        else:
            window['T_combat_DA1'].update('Target:  X')

        if Combat[3]:
            n = 2
        else:
            n = 1
            window['T_combat_DR'+str(i)].update(' X')

        if const.CNFG['Simroll']:
            for t in range(10):
                Results = np.random.randint(1, 21, 2)
                for i in range(n):
                    window['T_combat_DR'+str(i)].update('{:2.0f}'.format(Results[i]))
                window.refresh()
                time.sleep(1/((10-t)*5))

        Results = np.random.randint(1, 21, 2)
        printc('Die results:', Results, Color='Grey')
        for i in range(n):
            window['T_combat_DR'+str(i)].update('{:2.0f}'.format(Results[i]))

        if np.count_nonzero(Results == 1) > 0 or np.count_nonzero(Results == 20) > 0:
            window['T_combat_crit'].update('Critical Roll')
        else:
            window['T_combat_crit'].update('')

    # ==================================================================== EVENT
    else:
        printc('>', event, Color='O')
        for value in values:
            printc(value, ':', values[value], Color='Grey')

window.close()