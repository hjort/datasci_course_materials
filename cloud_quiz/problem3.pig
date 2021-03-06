/*
Problem 3: Compute a Join on chunk-000

In this problem we will consider the subgraph consisting of triples whose subject matches rdfabout.com: for that, filter on subject matches '.*rdfabout\\.com.*'.

Find all chains of lengths 2 in this subgraph. More precisely, return all sextuples (subject, predicate, object, subject2, predicate2, object2) where object=subject2.

What you need to turn in:
How many records are generated by the join for the cse-344-test-file dataset?
For the btc-2010-chunk-000 dataset?
*/

REGISTER myudfs.jar
--REGISTER s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
raw = LOAD 'cse344-test-file' USING TextLoader AS (line:chararray);
--raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader AS (line:chararray);
-- later you will load to other files, example:
--raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader AS (line:chararray); 
--DESCRIBE raw; -- raw: {line: chararray}

-- parse each line into ntriples
ntriples = FOREACH raw GENERATE FLATTEN(myudfs.RDFSplit3(line)) AS (subject:chararray, predicate:chararray, object:chararray);
--DESCRIBE ntriples; -- ntriples: {subject: chararray,predicate: chararray,object: chararray}

-- filter the data so you only have tuples whose subject matches 'rdfabout.com'
filtered = FILTER ntriples BY subject MATCHES '.*business.*';
--filtered = FILTER ntriples BY subject MATCHES '.*rdfabout\\.com.*';

-- make another copy of the filtered collection
filtered2 = FOREACH filtered GENERATE * AS (subject2:chararray, predicate2:chararray, object2:chararray);
--filtered2 = filtered AS (subject2:chararray, predicate2:chararray, object2:chararray);

-- join the two copies on object = subject2
joined = JOIN filtered BY subject, filtered2 BY subject2 PARALLEL 50;
--joined = JOIN filtered BY object, filtered2 BY subject2 PARALLEL 50;

-- remove duplicate tuples from the result of the join
result = DISTINCT joined PARALLEL 50;

-- count based on http://stackoverflow.com/questions/9900761/pig-how-to-count-a-number-of-rows-in-alias
grouped = GROUP result ALL;
counted = FOREACH grouped GENERATE COUNT (result);

-- store the results in the folder /user/hadoop/example-results
STORE result INTO 'problem3/result';
STORE counted INTO 'problem3/count';
--store count_by_object_ordered into '/user/hadoop/example-results' using PigStorage();
--STORE cbo_count INTO 's3n://hjort-mapreduce/problem2a';

/*
REGISTER s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader AS (line:chararray); 

ntriples = FOREACH raw GENERATE FLATTEN(myudfs.RDFSplit3(line)) AS (subject:chararray, predicate:chararray, object:chararray);

filtered = FILTER ntriples BY subject MATCHES '.*rdfabout\\.com.*';

filtered2 = FOREACH filtered GENERATE * AS (subject2:chararray, predicate2:chararray, object2:chararray);

joined = JOIN filtered BY object, filtered2 BY subject2 PARALLEL 10;

result = DISTINCT joined PARALLEL 10;

grouped = GROUP result ALL;
counted = FOREACH grouped GENERATE COUNT (result);

STORE result INTO 's3n://hjort-mapreduce/problem3/result';
STORE counted INTO 's3n://hjort-mapreduce/problem3/count';
*/

-- hadoop fs -getmerge s3n://hjort-mapreduce/problem3/result/ problem3-results.txt
