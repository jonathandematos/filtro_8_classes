#!/usr/bin/python
#
from __future__ import print_function
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
import numpy as np
import joblib
import os
#
def print_parameters(clf):
    print("Best parameters with score {:.5f}% set found on development set:".format(clf.best_score_))
    print(clf.best_estimator_)
    print()
    print("Grid scores on development set:")
    print()
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
#############################
# LOADING CRC
#############################
f = open("svm_tissues/tissue_pftas.txt","r")
#
X = list()
Y = list()
for i in f:
	linha = i[:-1].split(";")
        x_tmp = list()
        for j in linha[2:-1]:
            x_tmp.append(float(j))
        if(len(x_tmp) != 162):
            continue
        X.append(x_tmp)
	c = int(linha[0][0:2])
	#
	# 0 - importante
	# 1 - irrelevante
	#
	if(c > 4):
		Y.append(1)
	else:
		Y.append(0)
#
f.close()
#############################
# TRAINING SVM
#############################
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
#
del X
del Y
#
#tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1, 8e-1, 7e-1, 6e-1, 4e-1, 2e-1, 1e-1],
#                     'C': [5e-1, 5, 50, 500, 5000, 60000]},
#                    {'kernel': ['linear'], 'C': [1e-1, 1, 10, 100, 1000, 5000]}]
##
#clf = GridSearchCV(SVC(), probability=True, tuned_parameters, cv=5, scoring='accuracy')
#clf.fit(X_train, Y_train)
##
#print_parameters(clf)
##
if( os.path.exists("classificador_crc.pkl") == True ):
    clf = joblib.load("classificador_crc.pkl")
else:
    clf = SVC(probability=True)
    clf.fit(X_train, Y_train)
    joblib.dump(clf, "classificador_crc.pkl")
#
#print(clf.score(X_test, Y_test))
#############################
# LOADING BREAKHIS
#############################
f = open("svm_tissues/pftas_file_150.txt","r")
#
X = list()
Y = list()
Z = list()
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
    Y.append(class_str)
    Z.append(linha[1])
#
f.close()
#
#
#np_X = np.array([X])
#
for i in range(len(X)):
    pred = clf.predict_proba(np.array([X[i]]))
    if(pred.argmax() == 0):
        print("\n{};{};".format(Y[i], Z[i]), end="")
        for j in X[i]:
            print("{:.6f};".format(j),end="")
#
exit(0)
