#!/usr/bin/python
#
from __future__ import print_function
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
import numpy as np
import joblib
import os
#
#f = open("pftas_filtro_150.txt","r")
f = open("svm_tissues/pftas_file_150.txt","r")
#
X = list()
Y = list()
Z = list()
W = list()
for i in f:
    linha = i[:-1].split(";")
    x_tmp = list()
    for j in linha[2:-1]:
        x_tmp.append(float(j))
    if(len(x_tmp) != 162):
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
    #
    Y.append(class_line)
    Z.append(linha[1])
    a = linha[1].split("-")
    W.append(str(a[0])+"-"+str(a[1])+"-"+str(a[2])+"-"+str(a[3])+"-"+str(a[4]))
#
f.close()
#
#X_train, X_test, Y_train, Y_test, Z_train, Z_test = train_test_split(X, Y, Z, test_size=0.3)
#
for i in W:
    print(i)
exit(0)
#
Z_test = list()
Z_train = list()
#
f = open("svm_tissues/dsfold1.txt","r")
for i in f:
    linha = i[:-1].split("|")
    img = linha[0].split(".")[0]
    if(linha[3] == "train"):
        Z_train.append(img)
    else:
        Z_test.append(img)
f.close()
#
exit(0)
#
#
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1, 8e-1, 7e-1, 6e-1, 4e-1, 2e-1, 1e-1],
                     'C': [5e-1, 5, 50, 500, 5000, 60000]},
                    {'kernel': ['linear'], 'C': [1e-1, 1, 10, 100, 1000, 5000]}]
#
clf = GridSearchCV(SVC(probability=True), tuned_parameters, cv=5, scoring='accuracy', n_jobs=4)
#clf = SVC()
clf.fit(X_train, Y_train)
#
print(clf.score(X_test, Y_test))
#
exit(0)
