#!/usr/bin/python

import MapReduce
import sys

"""
Problem 5:

Consider a set of key-value pairs where each key is sequence id and each value is a string of nucleotides, e.g., GCTTCCGAAATGCTCGAA....

Write a MapReduce query to remove the last 10 characters from each string of nucleotides, then remove any duplicates generated.
"""

# Part 1: we create a MapReduce object that is used to pass data between the map function and the reduce function; you won't need to use this object directly.
mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

# Part 2: The input is a 2 element list: [sequence id, nucleotides]
def mapper(record):

	# sequence id: Unique identifier formatted as a string
	key = record[0]

	# nucleotides: Sequence of nucleotides formatted as a string
	value = record[1]

	mr.emit_intermediate(value[:-10], 1)

# Part 3: The output from the reduce function should be the unique trimmed nucleotide strings.
def reducer(key, list_of_values):

	# key: sequence of nucleotides already trimmed
	# value: list of occurrence counts

	mr.emit(key)

# Do not modify below this line
# =============================

if __name__ == '__main__':

	# Part 4: the code loads the json file and executes the MapReduce query which prints the result to stdout.
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)
