#!/usr/bin/python

import MapReduce
import sys

"""
Problem 2:
Implement a relational join as a MapReduce query.

Consider the query:

SELECT *
FROM Orders, LineItem
WHERE Order.order_id = LineItem.order_id

Your MapReduce query should produce the same information as this SQL query.
You can consider the two input tables, Order and LineItem, as one big concatenated bag of records which gets fed into the map function record by record.
"""

# Part 1: we create a MapReduce object that is used to pass data between the map function and the reduce function; you won't need to use this object directly.
mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

# Part 2: The input will be database records formatted as lists of Strings.
def mapper(record):

	table = record[0]
	order_id = record[1]

	mr.emit_intermediate(order_id, record)

# Part 3: The output should be a joined record.
def reducer(key, list_of_values):

   	# find order line
	order_line = None
	for v in list_of_values:
		if v[0] == 'order':
			order_line = v
			break

	# loop through line items
	for v in list_of_values:
		if v[0] == 'line_item':
			output = []
			output.extend(order_line)
			output.extend(v)
			mr.emit(output)

# Do not modify below this line
# =============================

if __name__ == '__main__':

	# Part 4: the code loads the json file and executes the MapReduce query which prints the result to stdout.
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)
