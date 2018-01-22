# LSH Unique Entity Estinamtor
A package for Estimating the number of unique eneties for a given input dataset with duplicates and near duplicates. See [our paper](https://arxiv.org/pdf/1709.01190.pdf) for theoretical and benchmarking details. 

## Prerequisites
Python 2, ngram, sklearn, numpy, scipy

## Tutorial

We will present very detailed steps to replicate one result presented in [our paper](https://arxiv.org/pdf/1710.02690.pdf), in particular the restaurant dataset (Becasue it is a public dataset). Other results can be replicated in a very similar manner.

Download the dataset from [here](https://hpi.de/naumann/projects/data-quality-and-cleansing/dude-duplicate-detection.html#c114715)
Restaurant.csv is the data file containing all the records with the cluster id in the last column (same cluster id means same entity)
Like:
```
"arnie morton's of chicago","435 s. la cienega blv.","los angeles","american",'0'
```

Use the C++ Package from [here](http://rush.rice.edu/large-scale.html) and also in C++ folder in this repository. This is a fast minhash package which will take dataset as input. It will output candidate pairs which fall in the same buckets. Details in [here] () 
By following the instructions in Readme of minhash pacakge, for input Restaurant.csv, we can get output Restaurant_out.csv. And then Restaurant_out.csv along with Restaurant.csv can be feed in to our estimation package to output unique entity estimation.
Genereal steps would be:

1. Compile the minhash package:
```
cd C++Codes
g++ -std=c++11 *.cpp -fopenmp (on Windows and Linux)
g++-7 *.cpp -fopenmp (on MacOS)
ATTN: Currently, the code is sometimes not compiling. This needs to be fixed. Also, the version on Anshu's webpage has errors in it and it outdated. Let's fix this ASAP. 
```
2. Update the Config file for minhash and run the program (Remember to change the outputfile name option to Restaurant_out.csv)
```
./a.out Config.txt
```
Then it will output Restaurant_out.csv which look like 
```
Rec1 Rec2
1 2
2 3
...
```
3. Feed in Restaurant_out.csv and Restaurant.csv to our estimation program:

```
Python pipeline.py --input data/Restaurant_out.csv --goldstan data/Restaurant.csv --output any_custom_file_name
```

```
Python pipeline.py --input data/Cd_out.csv --goldstan data/Cd.csv --output any_custom_file_name
```

There are other options:
```
'--trainsize', default='0.1', help='percentage of total pairs to use in training'
'--iter', default='100', help='iterations you want to repeat the process'
'--delimiter', default=',', help='delimeter of input file'
```
*Noted in the delimiter option, the default delimiter for "--goldstan" file is ",", if your file uses different dilimiter, you need to set it here.

Then you will get an estimation of the number of unique records in Restaurant dataset.
Like:
```
2018-01-19 04:00:12,364 - INFO - Iteration 76 : PRSE is inf ; LSHE is 742.750000
2018-01-19 04:00:13,203 - INFO - Iteration 77 : PRSE is inf ; LSHE is 755.110634
```
PRSE refers to the random sampling in [our paper](https://arxiv.org/pdf/1710.02690.pdf) and LSHE is the proposed estimator.

# Preview of Results 
We used three real-world dataset for testing: [Resaurant](), [CD]() and Voter Registration dataset.
