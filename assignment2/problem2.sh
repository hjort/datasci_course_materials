#!/bin/bash

# Problem 2: Matrix Multiplication in SQL

echo "Running queries..."

function runsql {
	sqlite3 matrix.db "$@"
}

# (g) multiply: Express A X B as a SQL query, referring to the class lecture for hints.
# What to turn in: On the assignment site, turn in a text document, multiply.txt, which is value of the cell (2,3)

sql="
SELECT value
FROM (
  SELECT a.row_num, b.col_num, sum(a.value * b.value) AS value
  FROM a JOIN b ON (a.col_num = b.row_num)
  GROUP BY a.row_num, b.col_num
) c
WHERE row_num = 2 AND col_num = 3
"

echo "g) $sql"
runsql "$sql" > multiply.txt

# -- forma direta de resolução:
# SELECT sum(a.value * b.value) AS value
# FROM a JOIN b ON (a.col_num = b.row_num)
# WHERE a.row_num = 2 AND b.col_num = 3;

echo
echo "Showing results..."
cat multiply.txt

