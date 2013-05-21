#!/usr/bin/python

import MapReduce
import sys

"""
Problem 3:
Consider a simple social network dataset consisting of key-value pairs where each key is a person and each value is a friend of that person.

Describe a MapReduce algorithm to count he number of friends each person has.
"""

# Part 1: we create a MapReduce object that is used to pass data between the map function and the reduce function; you won't need to use this object directly.
mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

# Part 2: The input is a 2 element list: [personA, personB]
def mapper(record):

	# This implies that personB is a friend of personA, but it does not imply that personA is a friend of personB.

	# personA: Name of a person formatted as a string
	pa = record[0]

	# personB: Name of one of personA's friends formatted as a string
	pb = record[1]

	mr.emit_intermediate(pa, 1)

# Part 3: The output should be a (person, friend count) tuple.
def reducer(key, list_of_values):

	# key: person
	# value: list of occurrence counts

	total = 0
	for v in list_of_values:
		total += v

	# the list of occurrence counts is summed
	mr.emit((key, total))

# Do not modify below this line
# =============================

if __name__ == '__main__':

	# Part 4: the code loads the json file and executes the MapReduce query which prints the result to stdout.
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)
