#!/usr/bin/python
#
from __future__ import print_function
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
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
#
# 01_TUMOR;1349E_CRC-Prim-HE-01_027.tif_Row_151_Col_151.png;0.89314;0
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
#
for i in range(len(X)):
    if(len(X[i]) != 162):
        print("Erro tamanho {}".format(i))
        exit(0)
#
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
#
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1, 8e-1, 7e-1, 6e-1, 4e-1, 2e-1, 1e-1],
                     'C': [5e-1, 5, 50, 500, 5000, 60000]},
                    {'kernel': ['linear'], 'C': [1e-1, 1, 10, 100, 1000, 5000]}]
#
clf = GridSearchCV(SVC(), tuned_parameters, cv=5, scoring='accuracy')
clf.fit(X_train, Y_train)
#
print_parameters(clf)
#
print(clf.score(X_test, Y_test))
#
exit(0)
