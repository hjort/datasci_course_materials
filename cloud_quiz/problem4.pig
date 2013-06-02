/*
Problem 4: Compute a Histogram on the Entire Dataset

Compute the histogram in Problem 2 on the entire 0.5TB dataset.
Use as many nodes as you like up to 19 small nodes.

When you are done, appreciate how relatively quick and easy it was to analyze a 0.5TB graph!

What you need to turn in:
How many (x, y) points are generated in the histogram?
*/

/*
Just want to share my setup. Total runtime for the last task (0.5TB) was 14min, 24sec.

MASTER: c1.medium
CORE: c1.xlarge x9 (High-CPU Instance)
SPOT: c1.xlarge x10 (High-CPU Instance), bid $0.2

All of the above using PARALLEL 19

I guess it's important to use Oregon zone.

Normalized instance hours: 173.
*/

REGISTER s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-*' USING TextLoader as (line:chararray);

-- parse each line into ntriples
ntriples = FOREACH raw GENERATE FLATTEN(myudfs.RDFSplit3(line)) AS (subject:chararray, predicate:chararray, object:chararray);

-- group the n-triples by subject column
subjects = GROUP ntriples BY (subject) PARALLEL 19;

-- flatten the objects out (because group by produces a tuple of each object
-- in the first column, and we want each object ot be a string, not a tuple),
-- and count the number of tuples associated with each object
count_by_subject = FOREACH subjects GENERATE FLATTEN($0), COUNT($1) AS count PARALLEL 19;

-- a scatter-plot of this histogram
nums_by_count = GROUP count_by_subject BY (count) PARALLEL 19;
scatter_plot = FOREACH nums_by_count GENERATE group AS x, COUNT($1) AS y;

--sp_group = GROUP scatter_plot ALL;
--sp_count = FOREACH sp_group GENERATE COUNT (scatter_plot);

-- store the results
STORE scatter_plot INTO 's3n://hjort-mapreduce/problem4/result';
--STORE sp_count INTO 's3n://hjort-mapreduce/problem4/count';

-- hadoop fs -getmerge s3n://hjort-mapreduce/problem4/result/ problem4-results.txt
-- scp hadoop@ec2-50-112-25-166.us-west-2.compute.amazonaws.com:problem4-results.txt .

