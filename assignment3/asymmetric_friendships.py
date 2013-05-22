#!/usr/bin/python

import MapReduce
import sys

"""
Problem 4:
The relationship "friend" is often symmetric, meaning that if I am your friend, you are my friend.

Implement a MapReduce algorithm to check whether this property holds.
Generate a list of all non-symmetric friend relationships.
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

	mr.emit_intermediate(pa, [1, pb])	# 1: followers
	mr.emit_intermediate(pb, [2, pa])	# 2: followees

# Part 3: The output should be a list of (person, friend) and (friend, person) tuples for each asymmetric friendship.
def reducer(key, list_of_values):

	# Only one of the (person, friend) or (friend, person) output tuples will exist in the input.
	# This indicates friendship asymmetry.

	# key: person
	# value: list of friends
	
	# create list of followers
	followers_list = []
	for v in list_of_values:
		if v[0] == 1:
			followers_list.append(v[1])

	# loop through followees and check if not followed
	for v in list_of_values:
		if v[0] == 2 and v[1] not in followers_list:
			mr.emit((v[1], key))
			mr.emit((key, v[1]))

# Do not modify below this line
# =============================

if __name__ == '__main__':

	# Part 4: the code loads the json file and executes the MapReduce query which prints the result to stdout.
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)
