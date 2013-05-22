#!/usr/bin/python

import MapReduce
import sys

"""
Problem 6:

Assume you have two matrices A and B in a sparse matrix format, where each record is of the form i, j, value.

Design a MapReduce algorithm to compute matrix multiplication: A x B
"""

# Part 1: we create a MapReduce object that is used to pass data between the map function and the reduce function; you won't need to use this object directly.
mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

# Part 2: The input to the map function will be matrix row records formatted as lists.
def mapper(record):

	# Each list will have the format [matrix, i, j, value] where matrix is a string and i, j, and value are integers.

	matrix = record[0]
	i = record[1]
	j = record[2]
	value = record[3]

	DIMENSION = 5	# matrix dimension was hardcoded! :O

	if matrix == 'a':
		for x in range(DIMENSION):
			mr.emit_intermediate((i, x), [matrix, j, value])
	elif matrix == 'b':
		for x in range(DIMENSION):
			mr.emit_intermediate((x, j), [matrix, i, value])

# Part 3: The output from the reduce function will also be matrix row records formatted as tuples.
def reducer(key, list_of_values):

	# Each tuple will have the format (i, j, value) where each element is an integer.

	# key: (row, column)
	# value: list of tuples related to the key

	row = key[0]
	col = key[1]

	value = 0
	for v in list_of_values:
		for w in list_of_values:
			if v[0] == 'a' and w[0] == 'b' and v[1] == w[1]:
				value += v[2] * w[2]

	mr.emit((row, col, value))

# Do not modify below this line
# =============================

if __name__ == '__main__':

	# Part 4: the code loads the json file and executes the MapReduce query which prints the result to stdout.
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)
