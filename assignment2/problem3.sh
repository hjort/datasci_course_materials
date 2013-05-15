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

# (i) keyword search: Find the best matching document to the keyword query "washington taxes treasury". 
sql="
SELECT max(similarity)
FROM (
  SELECT b.docid, sum(a.count * b.count) AS similarity
  FROM Frequency AS a
  JOIN (
    SELECT d.term, c.docid, c.count
    FROM Frequency AS c
      JOIN Frequency AS d ON (c.rowid = d.rowid)
  ) AS b ON (a.term = b.term)
  WHERE a.docid = 'q'
  GROUP BY b.docid
);
"
echo "i) $sql"
runsql "$sql" > keyword_search.txt

echo
echo "Showing results..."
head similarity_matrix.txt keyword_search.txt

