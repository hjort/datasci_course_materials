#!/bin/bash

# Problem 3: Working with a Term-Document Matrix

echo "Running queries..."

function runsql {
	sqlite3 reuters2.db "$@"
}

# (h) similarity matrix: Write a query to compute the similarity matrix DDT.
sql="
SELECT val AS value
FROM SimilarityFrequency
WHERE row = '17035_txt_earn' AND col = '10080_txt_crude';
"
echo "h) $sql"
runsql "$sql" > similarity_matrix.txt

echo
echo "Showing results..."
head similarity_matrix.txt

