/*
Problem 2A: Compute a Histogram on cse344-test-file

Using the 'cse344-test-file' file, write a Pig script that groups tuples by the subject column, and creates/stores histogram data showing the distribution of counts per subject, then generate a scatter-plot of this histogram.

Problem 2B: Compute a Histogram on chunk-000

Now run your script from Problem 2A on 'btc-2010-chunk-000' file.
Please use a 5-node cluster of small instances.

What you need to turn in:
How many (x, y) points are generated in the histogram?
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

-- group the n-triples by object column
--objects = GROUP ntriples BY (object) PARALLEL 50;
--DESCRIBE objects;
-- objects: {group: chararray,ntriples: {(subject: chararray,predicate: chararray,object: chararray)}}

-- group the n-triples by subject column
subjects = GROUP ntriples BY (subject) PARALLEL 50;
DESCRIBE subjects;
-- subjects: {group: chararray,ntriples: {(subject: chararray,predicate: chararray,object: chararray)}}

-- flatten the objects out (because group by produces a tuple of each object
-- in the first column, and we want each object ot be a string, not a tuple),
-- and count the number of tuples associated with each object
--count_by_object = FOREACH objects GENERATE FLATTEN($0), COUNT($1) AS count PARALLEL 50;
--DESCRIBE count_by_object; -- count_by_object: {group: chararray,count: long}

count_by_subject = FOREACH subjects GENERATE FLATTEN($0), COUNT($1) AS count PARALLEL 50;
DESCRIBE count_by_subject; -- count_by_subject: {group: chararray,count: long}
ILLUSTRATE count_by_subject;

-- a scatter-plot of this histogram
nums_by_count = GROUP count_by_subject BY (count) PARALLEL 50;
scatter_plot = FOREACH nums_by_count GENERATE group AS x, COUNT($1) AS y;

ILLUSTRATE scatter_plot;
DESCRIBE nums_by_count;
DESCRIBE scatter_plot;

-- based on http://stackoverflow.com/questions/9900761/pig-how-to-count-a-number-of-rows-in-alias
sp_group = GROUP scatter_plot ALL;
sp_count = FOREACH sp_group GENERATE COUNT (scatter_plot);

ILLUSTRATE sp_count;
DESCRIBE sp_group; -- sp_group: {group: chararray,scatter_plot: {(x: long,y: long)}}
DESCRIBE sp_count; -- sp_count: {long}

--order the resulting tuples by their count in descending order
--count_by_object_ordered = ORDER count_by_object BY (count) PARALLEL 50;

-- store the results in the folder /user/hadoop/example-results
STORE sp_count INTO 'problem2a';
--store count_by_object_ordered into '/user/hadoop/example-results' using PigStorage();
-- alternatively, you can store the results in S3, see instructions:
--store count_by_object_ordered into 's3n://superman/example-results';
--STORE cbo_count INTO 's3n://hjort-mapreduce/problem2a';

