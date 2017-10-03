#!/usr/bin/python
#
from __future__ import print_function
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
import numpy as np
import joblib
import os, sys
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
#
#
#
if(len(sys.argv) != 4):
    print("classify_paciente.py [pftas_file] [fold] [ampliacao]")
    exit(0)
#
ampliacao = int(sys.argv[3])
pftas_file = sys.argv[1]
fold = sys.argv[2]
#
outfile_train = str("train_test_files/")+fold.replace(".txt","_"+str(ampliacao)).replace("svm_tissues/","")
outfile_test = str("train_test_files/")+fold.replace(".txt","_"+str(ampliacao)).replace("svm_tissues/","")
outfile_train += "_train.txt"
outfile_test += "_test.txt"
#
print("Argumentos: {}".format(sys.argv))
#
#f = open("pftas_filtro_150.txt","r")
#f = open("svm_tissues/pftas_file_150.txt","r")
f = open(pftas_file, "r")
#
X = list()
Y = list()
Z = list()
W = list()
V = list()
U = list()
errados = 0
for i in f:
    linha = i[:-1].split(";")
    a = linha[1].split("-")
    if(int(a[3]) == ampliacao):
        W.append(str(a[0])+"-"+str(a[1])+"-"+str(a[2])+"-"+str(a[3])+"-"+str(a[4]))
        U.append(linha[1])
        V.append(linha[0])
        x_tmp = list()
        for j in linha[2:-1]:
            x_tmp.append(float(j))
        if(len(x_tmp) != 162):
            errados += 1
            continue
        X.append(x_tmp)
        class_str = linha[0]
        #
        # 0 - importante
        # 1 - irrelevante
        #
        if(class_str == 'adenosis'):
        	class_line = int(0)
        if(class_str == 'ductal_carcinoma'):
        	class_line = int(4)
        if(class_str == 'fibroadenoma'):
        	class_line = int(1)
        if(class_str == 'lobular_carcinoma'):
        	class_line = int(5)
        if(class_str == 'mucinous_carcinoma'):
        	class_line = int(6)
        if(class_str == 'papillary_carcinoma'):
        	class_line = int(7)
        if(class_str == 'phyllodes_tumor'):
        	class_line = int(2)
        if(class_str == 'tubular_adenoma'):
        	class_line = int(3)
        Y.append(class_line)
#
f.close()
#
#X_train, X_test, Y_train, Y_test, Z_train, Z_test = train_test_split(X, Y, Z, test_size=0.3)
#
Z_test = list()
Z_train = list()
#
#f = open("svm_tissues/dsfold1.txt","r")
f = open(fold,"r")
#
for i in f:
    linha = i[:-1].split("|")
    if(int(linha[1]) == ampliacao):
        img = linha[0].split(".")[0]
        if(linha[3] == "train"):
            Z_train.append(img)
        else:
            Z_test.append(img)
f.close()
#
X_test = list()
Y_test = list()
U_test = list()
V_test = list()
X_train = list()
Y_train = list()
U_train = list()
V_train = list()
for i in range(len(X)):
    if(W[i] in Z_test):
        X_test.append(X[i])
        Y_test.append(Y[i])
        U_test.append(U[i])
        V_test.append(V[i])
    if(W[i] in Z_train):
        X_train.append(X[i])
        Y_train.append(Y[i])
        U_train.append(U[i])
        V_train.append(V[i])
#
print(len(X_test), len(X_train))
#exit(0)
#
del X
del Y
del U
del Z_test
del Z_train
#
f = open(outfile_train, "w")
for i in range(len(X_train)):
    f.write("{};{};".format(V_train[i], U_train[i]))
    for j in X_train[i]:
        f.write("{:.6f};".format(j))
    f.write("\n")
f.close()
f = open(outfile_test, "w")
for i in range(len(X_test)):
    f.write("{};{};".format(V_test[i], U_test[i]))
    for j in X_test[i]:
        f.write("{:.6f};".format(j))
    f.write("\n")
f.close()
#
exit(0)
