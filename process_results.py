#!/usr/bin/python
#
import sys
import numpy as np
#
f = open(sys.argv[1], "r")
#
#SOB_B_A-14-22549G-100-030-550-150.png;0;0.129226;0.004267;0.007883;0.004518;0.175048;0.000307;0.677721;0.001031;
#
t = 0
Y = []
W = []
Z = []
#
for i in f:
    if(t == 0):
        t += 1
        continue
    else:
        linha = i.split(";")
        Y.append(int(linha[1]))
        wtmp = list()
        for j in linha[2:-1]:
            wtmp.append(float(j))
        W.append(wtmp)
        Z.append(linha[0])
#
f.close()
#
print(len(Y), len(W), len(Z))
#
correct = 0
total = 0
for i in range(len(Y)):
    if(Y[i] == np.argmax(W[i])):
        correct += 1
    total += 1
print(float(correct)/total)

