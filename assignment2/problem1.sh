#!/bin/bash

# Problem 1: Inspecting the Reuters Dataset; Relational Algebra

echo "Running queries..."

function runsql {
	sqlite3 reuters.db "$@"
}

function countsql {
	sqlite3 reuters.db "SELECT count(1) FROM ($@)"
}

# (a) select: Write a query that is equivalent to the following relational algebra expression.
sql="SELECT * FROM frequency WHERE docid = '10398_txt_earn'"
echo "a) $sql"
runsql "$sql" > select.data
countsql "$sql" > select.txt

# (b) select project: Write a SQL statement that is equivalent to the following relational algebra expression.
sql="SELECT term FROM frequency WHERE docid = '10398_txt_earn' AND count = 1"
echo "b) $sql"
runsql "$sql" > select_project.data
countsql "$sql" > select_project.txt

# (c) union: Write a SQL statement that is equivalent to the following relational algebra expression.
sql="SELECT term FROM frequency WHERE docid = '10398_txt_earn' AND count = 1
UNION
SELECT term FROM frequency WHERE docid = '925_txt_trade' AND count = 1"
echo "c) $sql"
runsql "$sql" > union.data
countsql "$sql" > union.txt

# (d) count: Write a SQL statement to count the number of documents containing the word “parliament”
sql="SELECT count FROM frequency WHERE term = 'parliament'"
echo "d) $sql"
runsql "$sql" > count.data
countsql "$sql" > count.txt


echo
echo "Showing results..."
head *.{txt,data}

