#!/bin/bash

RESDIR="results"	# results directory

# clean it up
rm -rf $RESDIR
mkdir -p $RESDIR

# ...

# pairs of "script:data_file"
SCRIPTS="wordcount:books inverted_index:books join:records"
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

	if ! diff $res $sol > /dev/null
	then
		echo "Wrong results..."
	else
		echo "Well done!"
	fi
}

for pair in $SCRIPTS
do
	script=`echo $pair | cut -d: -f1`.py
	data=`echo $pair | cut -d: -f2`.json
	run_it
	let number++
done

