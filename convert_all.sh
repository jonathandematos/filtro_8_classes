#!/bin/bash
#
diretorios=("train_test_files_all_patches" "train_test_files_empty_tumor" "train_test_files_filtro_all_tissues")
#ampliacao=(40 100 200 400)
#fold=(1 2 3 4 5)
#
for k in ${diretorios[@]};
do
	echo $k
	for i in `ls -1 $k`;
	do
		a=$(basename -s ".txt" $k"/"$i)
	        out=$a".arff"
		./convert_to_arff.py $k"/"$i > $k"/"$out
	done
done
