#!/bin/bash

# Problem 1: Inspecting the Reuters Dataset; Relational Algebra

echo "Running queries..."

# (a) select: Write a query that is equivalent to the following relational algebra expression.
sqlite3 reuters.db "select count(1) from frequency where docid = '10398_txt_earn'" > select.txt

# (b) select project: Write a SQL statement that is equivalent to the following relational algebra expression.


