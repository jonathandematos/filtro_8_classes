#!/bin/bash
#
#arquivos=("pftas_filtro_150.txt" "svm_tissues/pftas_file_150.txt")
arquivos=("pftas_filtro_150_3.txt")
ampliacao=(40 100 200 400)
fold=(1 2 3 4 5)
#
for k in ${arquivos[@]};
do
	for i in ${ampliacao[@]};
	do
		for j in ${fold[@]};
		do
			./generate_sets.py $k "svm_tissues/dsfold"$j".txt" $i
		done
	done
done
