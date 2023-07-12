import os, sys, time, json, copy

import scu
from scu import printc, printf, txt_c

scu.imports('numpy', 'PySimpleGUI')
import numpy as np
import PySimpleGUI as sg

import const
import dsa_talents

printc('===> DSA fastroll <===', Color='Y')

sg.theme('Default1')
sg.theme_button_color('#dde4ff')

Talent_ID = None

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
                        [sg.Frame(title='D'+str(i), key='F_talents_D'+str(i), element_justification='c', vertical_alignment='c', title_location='n', font=const.FL, 
                            layout=[[sg.Text('Value:  -', key='T_talents_DA'+str(i), size=(9, 1), font=const.FM, justification='c')],
                                    [sg.Text('-', key='T_talents_DR'+str(i), size=(2, 1), font=const.FH, justification='c')]]) for i in range(3)],
                        [sg.Text('', key='T_talents_crit', size=(20, 1), font=const.FH, justification='c')]]
layout_tab_talents_2B = ([[sg.Text('Adv', font=const.FS, justification='c')]] +
                            [[sg.Text('{:>+3.0f}'.format(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.ADVANTAGE_RANGE_TALENT[0], const.ADVANTAGE_RANGE_TALENT[1]+1)]
                            )
layout_tab_talents_2C = ([[sg.Text('QS', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_talents_QS_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.ADVANTAGE_RANGE_TALENT[0], const.ADVANTAGE_RANGE_TALENT[1]+1)]
                            )
layout_tab_talents_2D = ([[sg.Text('Succ', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_talents_succ_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.ADVANTAGE_RANGE_TALENT[0], const.ADVANTAGE_RANGE_TALENT[1]+1)]
                            )
layout_tab_talents_2E = ([[sg.Text('Fail', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_talents_fail_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.ADVANTAGE_RANGE_TALENT[0], const.ADVANTAGE_RANGE_TALENT[1]+1)]
                            )
layout_tab_talents_2F = ([[sg.Text('Exp QS', font=const.FS, justification='c')]] +
                            [[sg.Text('-', key='T_talents_exp_'+str(i), size=(8, 1), font=const.FS, pad=(0,0), justification='c')] for i in range(const.ADVANTAGE_RANGE_TALENT[0], const.ADVANTAGE_RANGE_TALENT[1]+1)]
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

layout_tabs = [[sg.Tab(title='Würfel', key='Tab_die', layout=layout_tab_die, element_justification='c'),
                    sg.Tab(title='Fertigkeiten', key='Tab_abilities', layout=layout_tab_talents, element_justification='c')]]

layout =    [[sg.Input(key='I_Char_select', visible=False, enable_events=True),
                sg.FileBrowse('Character', key='B_Char_Select', target=(sg.ThisRow, 0), file_types=(('JSON files','*.json'), ("ALL Files","*.*")), initial_folder=sys.path[0], tooltip='Select character file', font=const.FS),
                sg.Text(const.CHAR['name'], key='T_Char_select', s=(20,1), font=const.FS),
                sg.Text('  '.join([const.ATTR_DECODE[i]+':{:>2.0f}'.format(const.CHAR['attr']['values'][i]['value']) for i in range(8)]), key='T_Char_attributes', font=const.FM, justification='c')],
            [sg.TabGroup(layout=layout_tabs, key='TabG_Main', font=const.FM)]]
            

window = sg.Window(title='DSA fastroll '+const.CNFG['Version'], layout=layout)
window.finalize()
window['T_Char_attributes'].expand(expand_x=True, expand_y=False)
window['F_talents_die_rolling'].expand(expand_x=True, expand_y=True)

window.refresh()

def die_roll(Count, Size, Simroll):
    printc('> Rolling for: {:.0f}W{:.0f}'.format(Count, Size), Color='M')
    if Simroll:
        for t in range(10):
            roll = np.random.randint(1, Size+1, Count)
            window['T_die_result_1'].update(', '.join(['{:2.0f}']*Count).format(*roll))
            window.refresh()
            time.sleep(1/((10-t)*5))
    roll = np.random.randint(1, Size+1, Count)
    window['T_die_result_1'].update(', '.join(['{:2.0f}']*Count).format(*roll))
    if Count > 1:
        window['T_die_result_2'].update('Summe: {:.0f}'.format(np.sum(roll)))
    else:
        window['T_die_result_2'].update('')
    printc('Die results:', roll, Color='Grey')

while const.FLAG_RUN:
    event, values = window.read()

    # ==================================================================== EVENT
    if event in (sg.WIN_CLOSED,):
        const.FLAG_RUN = False

    # ==================================================================== EVENT
    elif event == 'I_Char_select':
        if not values['I_Char_select'] == '':
            const.CNFG['Character'] = values['I_Char_select']
        printc('> Character file:', const.CNFG['Character'], Color='M')
        const.store_cnfg()
        const.load_character()
        window['T_Char_select'].update(const.CHAR['name'])
        window['T_Char_attributes'].update('  '.join([const.ATTR_DECODE[i]+':{:>2.0f}'.format(const.CHAR['attr']['values'][i]['value']) for i in range(8)]))            
        for i in range(59):
            window['B_talent_select:'+str(i)].update(const.TALENT_STRING(i))

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
            window['T_talents_DA'+str(i)].update('Value: {:>2.0f}'.format(Targets[i]))

        if const.CNFG['Simroll'] == 'True':
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

        for i in range(const.ADVANTAGE_RANGE_TALENT[0], const.ADVANTAGE_RANGE_TALENT[1]+1):
            Rem = Talent_Value
            for a in range(3):
                Rem -= max(0, Results[a] - i - Targets[a])
            if flag_crit:
                window['T_talents_QS_'+str(i)].update('Crit')
            elif Rem < 0:
                window['T_talents_QS_'+str(i)].update('Fail')
            else:
                window['T_talents_QS_'+str(i)].update(str(max(1,(Rem-1)//3+1)))

        if (not talent_flag) and const.CNFG['Disable_Chances'] == 'False': 
            window.refresh()
            talent_simulation = dsa_talents.simulate_talent(const.ADVANTAGE_RANGE_TALENT, Targets, Talent_Value)
            for i in range(const.ADVANTAGE_RANGE_TALENT[0], const.ADVANTAGE_RANGE_TALENT[1]+1):
                window['T_talents_succ_'+str(i)].update('{:>4.1f}%'.format(talent_simulation[i][0]*100))
                window['T_talents_fail_'+str(i)].update('{:>4.1f}%'.format(talent_simulation[i][1]*100))
                window['T_talents_exp_'+str(i)].update('{:>3.1f}'.format(talent_simulation[i][2]))

    # ==================================================================== EVENT
    elif 'B_die_' in event:
        pack = event.split('_')[-1].split('W')
        die_roll(int(pack[0]), int(pack[1]), const.CNFG['Simroll'] == 'True')

    # ==================================================================== EVENT
    else:
        printc('>', event, Color='O')
        for value in values:
            printc(value, ':', values[value], Color='Grey')

window.close()