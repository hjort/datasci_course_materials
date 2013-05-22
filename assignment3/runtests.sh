#!/bin/bash

RESDIR="results"	# results directory

# clean it up
rm -rf $RESDIR
mkdir -p $RESDIR

# pairs of "script_name:input_data_file"
SCRIPTS="wordcount:books inverted_index:books join:records friend_count:friends asymmetric_friendships:friends unique_trims:dna"
number=0

# run script against the data
function run_it {

	name=$(basename $script .py)
	echo

	if [ ! -f $script ]
	then
		echo "Script not found: $script"
		return 1
	fi

	src="data/$data"		# data source
	res="results/$name.json"	# received result
	sol="solutions/$name.json"	# expected solution

	echo "Running $number: $script $src"
	python $script $src > $res

	# measure file size
	#cres=$(stat -c%s $res)
	#csol=$(stat -c%s $sol)

	# count the words
	wres=$(wc -w $res | cut -d' ' -f1)
	wsol=$(wc -w $sol | cut -d' ' -f1)

	#if ! diff $res $sol > /dev/null
	if [ $wres -ne $wsol ]
	then
		echo "Wrong results..."
	else
		echo "Well done!"
	fi
}

# run and check the scripts for each assigned problem
for pair in $SCRIPTS
do
	script=`echo $pair | cut -d: -f1`.py
	data=`echo $pair | cut -d: -f2`.json
	run_it
	let number++
done

