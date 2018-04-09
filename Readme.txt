##############################################################
# LSH Unique Entity Estimator Package
##############################################################

All the parameters (including the input files) for MinHash are passed using config.txt files.

To run the package (command line linux)

g++ -std=c++11 *.cpp output -fopenmp

for ((i=1;i<=1;i++)) ; do ./output config.txt; python pipeline.py --input Syria_output.csv --goldstan Syria.csv --pair train.csv >>raw_results.csv; done

Input file Syria.csv format example:

Firtname,Lastname,M,2013-06-07,Rural Damascus,مسرابا

Intermediate output Syria_output.csv format will look like 

```
Rec1 Rec2
1 2
2 3
...
```

raw_results.csv will have 100 estimation of unqiue number of records in input dataset and therefore we can get a final estimation and corresponding Std.

```
'--input', help='input the output file after running ./output config.txt'
'--goldstan', help='the raw input data record file, like the Syrian dataset'
'--pair',  help='partial labels for the input dataset, eg. the handmatching matches/nonmatches'
```


for ((i=1;i<=1;i++)) ; do ./output config.txt; python pipeline.py --input Syria_output.csv --goldstan Syria.csv --pair train.csv >>raw_results.csv; done
