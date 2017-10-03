#!/usr/bin/python
#
import arff
import sys
#
f = open(sys.argv[1],"r")
#
arff_obj = {
        'description': u'',
        'relation': 'breakhis',
        }
list_attr = []
for i in range(162):
    nm_attr = 'attr'+str(i)
    type_attr = 'REAL'
    list_attr.append((nm_attr, type_attr))
#list_attr.append(('imgname','STRING'))
list_attr.append(('class',['0','1','2','3','4','5','6','7']))
arff_obj['attributes'] = list_attr
list_attr = []
#
for i in f:
    linha = i[:-1].split(";")
    x_tmp = list()
    for j in linha[2:-1]:
        x_tmp.append(float(j))
    if(len(x_tmp) != 162):
        continue
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
#    x_tmp.append(linha[1])
    x_tmp.append(class_line)
    list_attr.append(x_tmp)
arff_obj['data'] = list_attr
#
f.close()
#
print(arff.dumps(arff_obj))
#
