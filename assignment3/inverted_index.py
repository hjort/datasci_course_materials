#!/usr/bin/python

import MapReduce
import sys

"""
Problem 1:
Create an Inverted index. Given a set of documents, an inverted index is a dictionary where each word is associated with a list of the document identifiers in which that word appears.
"""

# Part 1: we create a MapReduce object that is used to pass data between the map function and the reduce function; you won't need to use this object directly.
mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

# Part 2: The input is a 2 element list: [document_id, text]
def mapper(record):

	# key: document identifier (formatted as a string)
	key = record[0]

	# value: document contents (text of the document formatted as a string)
	value = record[1]

	# The document text may have words in various cases or elements of punctuation.
	# Do not modify the string, and treat each token as if it was a valid word.
	# (That is, just use value.split())
	words = value.split()

	for w in words:
		mr.emit_intermediate(w, key)

# Part 3: The output should be a (word, document ID list) tuple where word is a String and document ID list is a list of Strings.
def reducer(key, list_of_values):

	# key: word
	# value: list of documents

	doc_list = []
	for v in list_of_values:
		if v not in doc_list:
			doc_list.append(v)

	mr.emit((key, doc_list))

# Do not modify below this line
# =============================

if __name__ == '__main__':

	# Part 4: the code loads the json file and executes the MapReduce query which prints the result to stdout.
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)
