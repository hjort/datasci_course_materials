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

# (e) big documents Write a SQL statement to find all documents that have more than 300 total terms, including duplicate terms.
sql="SELECT a.docid FROM frequency a JOIN frequency b ON (a.docid = b.docid) WHERE a.term = 'transactions' AND b.term = 'world'"
echo "e) $sql"
runsql "$sql" > big_documents.data
countsql "$sql" > big_documents.txt

# (f) two words: Write a SQL statement to count the number of unique documents that contain both the word 'transactions' and the word 'world'. 
sql="SELECT a.docid FROM frequency a JOIN frequency b ON (a.docid = b.docid) WHERE a.term = 'transactions' AND b.term = 'world'"
echo "f) $sql"
runsql "$sql" > two_words.data
countsql "$sql" > two_words.txt

echo
echo "Showing results..."
head *.txt

