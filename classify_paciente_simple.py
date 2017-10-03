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
import arff
#
#
#
if(len(sys.argv) != 3):
    print("classify_paciente_simples.py [train] [test]")
    exit(0)
#
pftas_file_train = sys.argv[1]
pftas_file_test = sys.argv[2]
#
print("Argumentos: {}".format(sys.argv))
#
# Combine results by vote
#
def CombineByVote(results):
    if(len(results)>0):
        if(len(results[0])>0):
            vote_list = [0 for i in range(len(results[0]))]
            for i in results:
                vote_list[np.argmax(np.array(i))] += 1
            return np.argmax(np.array(vote_list))
        return -1
    return -1
#
# Combine results by sum
#
def CombineBySum(results):
    if(len(results)>0):
        if(len(results[0])>0):
            vote_list = [0 for i in range(len(results[0]))]
            for i in results:
                for j in range(len(i)):
                    vote_list[j] += i[j]
            return np.argmax(np.array(vote_list))
        return -1
    return -1
#
#
#
def LoadDataset(dataset):
    data = arff.load(open(dataset, "r"))

    X = list()
    Y = list()
    Z = list()

    for i in data['data']:
        x_tmp = list()
        for j in i[:-1]:
            x_tmp.append(float(j))
        X.append(x_tmp)
        #Z.append(str(i[-2:-1]))
        Y.append(int(i[-1]))
    return X, Y, Z
#
#
#
def StrToTumorClass(class_str):
    class_line = 0
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
    return class_line
#
#
#
def TumorClassToStr(class_line):
    class_str = ""
    if(class_line == 0):
    	class_str = 'adenosis'
    if(class_line == 4):
    	class_str = 'ductal_carcinoma'
    if(class_line == 1):
    	class_str = 'fibroadenoma'
    if(class_line == 5):
    	class_str = 'lobular_carcinoma'
    if(class_line == 6):
    	class_str = 'mucinous_carcinoma'
    if(class_line == 7):
    	class_str = 'papillary_carcinoma'
    if(class_line == 2):
    	class_str = 'phyllodes_tumor'
    if(class_line == 3):
    	class_str = 'tubular_adenoma'
    return class_str
 
#
X_train, Y_train, Z_train = LoadDataset(pftas_file_train)
X_test, Y_test, Z_train = LoadDataset(pftas_file_test)
#
#
#
#tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1, 1e-1, 10],
#                     'C': [5e-1, 50, 5000, 50000]}]
#                    {'kernel': ['linear'], 'C': [1e-1, 1, 10]}]
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1, 1e-1, 10],
                     'C': [50000, 150000, 300000]}]
#
clf = GridSearchCV(SVC(probability=True), tuned_parameters, cv=5, scoring='accuracy', n_jobs=2, verbose=4)
#clf = SVC(probability=True)
#clf = DecisionTreeClassifier()
#clf = RandomForestClassifier()
#X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.30)
clf.fit(X_train, Y_train)
#
print(clf.score(X_test, Y_test))
#
exit(0)
#
#
#
pacs = {}
imgs = {}
patch = {}
#
# SOB_B_A-14-22549G-100-030-550-150.png
#
correto = 0
total = 0
for i in range(len(X_test)):
    str_img = U_test[i].split("-")
    img = str(str_img[2])+str(str_img[3])+str(str_img[4])
    pac = str(str_img[0])+str(str_img[2])
    pred = np.squeeze(clf.predict_proba(np.array([X_test[i]])))
#    print("{};{};".format(U_test[i], Y_test[i]), end="")
#    for j in pred:
#        print("{:.6f};".format(j), end="")
#    print()
    #
    if(np.argmax(pred) == Y_test[i]):
        correto += 1
    total += 1
    if(img in imgs):
        imgs[img][1].append(pred)
    else:
        imgs[img] = [Y_test[i],list()]
        imgs[img][1].append(pred)
    #
    if(pac in pacs):
        pacs[pac][1].append(pred)
    else:
        pacs[pac] = [Y_test[i],list()]
        pacs[pac][1].append(pred)
#
#joblib.dump(pacs, "pacs.pkl")
#joblib.dump(imgs, "imgs.pkl")
#
#pacs = joblib.load("pacs.pkl")
#imgs = joblib.load("imgs.pkl")
#print(pacs)
#
print("Patches: {}".format(float(correto)/total))
exit(0)
#
correto = 0
total = 0
for i in imgs:
    if(imgs[i][0] == CombineBySum(imgs[i][1])):
        correto += 1
    total += 1
print("Combinacao de imagens por soma: {}".format(float(correto)/total))
#
correto = 0
total = 0
for i in imgs:
    if(imgs[i][0] == CombineByVote(imgs[i][1])):
        correto += 1
    total += 1
print("Combinacao de imagens por voto: {}".format(float(correto)/total))
#
correto = 0
total = 0
for i in pacs:
    if(pacs[i][0] == CombineBySum(pacs[i][1])):
        correto += 1
    total += 1
print("Combinacao de paciente por soma: {}".format(float(correto)/total))
#
correto = 0
total = 0
for i in pacs:
    if(pacs[i][0] == CombineByVote(pacs[i][1])):
        correto += 1
    total += 1
print("Combinacao de paciente por voto: {}".format(float(correto)/total))
#
exit(0)
