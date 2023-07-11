import os, sys, time, json, copy
import numpy as np

import scu
from scu import printc, printf, txt_c

PROB_1D20 = np.ones(20) / 20
PROB_2D20 = np.convolve(PROB_1D20, PROB_1D20)
PROB_3D20 = np.convolve(PROB_2D20, PROB_1D20)
PROB_3D20_CRIT = 1/20*(1/20+19/20*1/20)+19/20*1/20*1/20

Attributes = (12, 12, 12)
Skill = 4

def simulate_talent(Diffrange = (-6, 6), Attributes = Attributes, Skill = Skill):
    Pack = {}
    for difficulty in range(Diffrange[0], Diffrange[1]+1):
        Die_size = 20

        Results = [0,0,0,0]
        Points = []
        Total = pow(Die_size,3)
        
        for i in range(pow(Die_size,3)):
            decode = [(i//pow(Die_size, j))%Die_size+1 for j in range(3)]
            if decode.count(1) > 1:
                Results[0] += 1
            elif decode.count(20) > 1:
                Results[3] += 1
            else:
                Rem = copy.copy(Skill)
                for a in range(3):
                    Rem -= max(0, decode[a] - difficulty - Attributes[a])
                if Rem < 0:
                    Results[2] += 1
                else:
                    Results[1] += 1
                    Points.append(max(1,(Rem-1)//3+1))
        pack = [(Results[0]+Results[1])/Total, (Results[2]+Results[3])/Total, np.average(Points)]
        Pack.update({difficulty:pack})
    return Pack

if __name__ == '__main__':
    Pack = simulate_talent()
    for pack in Pack:
        txt =  txt_c(' {:+.0f}'.format(pack), Color='B')
        txt += txt_c(' {:>4.1f}%'.format(Pack[pack][0]*100), Color='G')
        txt += txt_c(' {:>4.1f}%'.format(Pack[pack][1]*100), Color='R')
        txt += txt_c(' {:>4.1f}'.format(Pack[pack][2]), Color='M')
        print(txt)