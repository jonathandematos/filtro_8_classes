#!/usr/bin/python
#
import sys
import math
from random import shuffle
#
if(len(sys.argv) != 3):
	print("Uso: folds.py [feature_file] [fold_nr]")
	exit(0)
#
tumors = ("SOB_B_A","SOB_B_F","SOB_B_PT","SOB_B_TA","SOB_M_DC","SOB_M_LC","SOB_M_MC","SOB_M_PC")
#
patients = list()
#
#tumors_amount = (0,0,0,0,0,0,0,0)
tumors_amount = list(0 for i in range(8))
train_amount = list(0 for i in range(8))
test_amount = list(0 for i in range(8))
#
feat_file = sys.argv[1]
fold_nr = sys.argv[2]
#
feats = open(feat_file,"r")
#
# Obtain the list of patients based on the features file
#
for i in feats:
	img_name = i.split(";")[0]
	patient = img_name.split("-")[0]+"-"+img_name.split("-")[1]+"-"+img_name.split("-")[2]
	if(patient == ""):
		continue
	try:
		patients.index(patient)
	except ValueError:
		patients.append(patient)
#
# Count the amount of patients that have each type of tumor
#
for j in patients:
	tumor = j.split("-")[0]
	try:
		idx = tumors.index(tumor)
	except ValueError:
		print("Erro")
	tumors_amount[idx] += 1
#
# Create the train and test sets 
#
for i in range(len(tumors_amount)):
	train_amount[i] = int(round(tumors_amount[i] * 0.7))
#	train_amount[i] = int(tumors_amount[i] * 0.7)
	test_amount[i] = int(tumors_amount[i] - train_amount[i])
#
#print(tumors_amount)
#print(train_amount)
#print(test_amount)
#
# Cria listas temporarias para gerar gerar um fold
#
temp_patients = list(patients)
train_patients = list(list() for i in range(8))
test_patients = list(list() for i in range(8))
temp_train_amount = list(train_amount)
temp_test_amount = list(test_amount)
#
# Shuffling all patients to generate a new random set every time
shuffle(temp_patients)
#
for j in temp_patients:
	# Tumor of the patient
	tumor = j.split("-")[0]
	try:
		# Index of the tumor in the tumor list
		idx = tumors.index(tumor)
	except ValueError:
		print("Erro")
	# All train tumors were selected, selecting test now
	if(temp_train_amount[idx]==0):
		test_patients[idx].append(j)
		temp_test_amount[idx] -= 1
	# Selecting train patients
	else:
		train_patients[idx].append(j)
		temp_train_amount[idx] -= 1
#print(temp_train_amount)
#print(temp_test_amount)
#
#for i in train_patients:
#	print(i)
#
feats.seek(0)
#
for j in range(8):
	for k in train_patients[j]:
		for i in feats:
			img_name = i.split(";")[0]
			patient = img_name.split("-")[0]+"-"+img_name.split("-")[1]+"-"+img_name.split("-")[2]
			mag = img_name.split("-")[3]
			#print("|{} {}|".format(patient, k))
			if(patient == k):
				print("{}|{}|{}|{}".format(img_name,mag,fold_nr,"train")) 
		feats.seek(0)	
#
feats.seek(0)
#
for j in range(8):
	for k in test_patients[j]:
		for i in feats:
			img_name = i.split(";")[0]
			patient = img_name.split("-")[0]+"-"+img_name.split("-")[1]+"-"+img_name.split("-")[2]
			mag = img_name.split("-")[3]
			#print("|{} {}|".format(patient, k))
			if(patient == k):
				print("{}|{}|{}|{}".format(img_name,mag,fold_nr,"test")) 
		feats.seek(0)	
#
feats.close()
