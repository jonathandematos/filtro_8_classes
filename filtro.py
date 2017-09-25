#!/usr/bin/python
#
# 01_TUMOR;1349E_CRC-Prim-HE-01_027.tif_Row_151_Col_151.png;0.89314;0
f = open("tissue_pftas.txt","r")
#
X = list()
Y = list()
for i in f:
	linha = i[:-1].split(";")
	c = int(linha[0][0:2])
	#
	# 0 - importante
	# 1 - irrelevante
	#
	if(c > 4):
		print(1)
	else:
		print(0)
#
f.close()
#
exit(0)
