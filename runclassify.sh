#!/bin/bash
#
diretorios=("train_test_files_all_patches" "train_test_files_empty_tumor")
#arquivos=("pftas_filtro_150_3.txt")
#ampliacao=(40 100 200 400)
#fold=(1 2 3 4 5)
#
for k in ${diretorios[@]};
do
	echo $k
	for i in `ls -1 $k | grep -v "test" | grep "arff"`;
	do
		treino=$i
		teste=$(echo $i | sed 's/train/test/g')
		echo $k"/"$treino" $k"/""$teste
	        #out=$a".arff"
		#./classify_paciente_simple.py $k"/"$i > $k"/"$out
	done
done
