# Unique Entity Estinamtor
A package for Estimating the number of unique eneties for a given input dataset with duplicates and near duplicates. See [our paper](https://arxiv.org/pdf/1709.01190.pdf) for theoretical and benchmarking details. 

## Prerequisites
Python 2, ngram, sklearn, numpy, scipy, matlib

In order to install using pip, one will need to run the following commands if errors arise from the terminal due to recent changes with SSH in pip (Linus and MacOS)

```
pip install --pre subprocess32
pip2 install numpy scipy matplotlib
```

## Tutorial on running Unique Entity Estimation Package

We will present very detailed steps to replicate one result presented in [our paper](https://arxiv.org/pdf/1710.02690.pdf), in particular the restaurant dataset (public dataset). Other results can be replicated in a very similar manner.

Download the dataset from [here](https://hpi.de/naumann/projects/data-quality-and-cleansing/dude-duplicate-detection.html#c114715)
Restaurant.csv is the data file containing all the records with the cluster id in the last column (same cluster id means same entity)

Example:
```
"arnie morton's of chicago","435 s. la cienega blv.","los angeles","american",'0'
```

Use the C++ Package folder in this repository. This is a fast minhash package which will take the dataset as input. It will output candidate pairs which fall in the same buckets. 


By following the instructions in README of minhash pacakge, for input Restaurant.csv, we can get output Restaurant_out.csv. And then Restaurant_out.csv along with Restaurant.csv can be feed in to our estimation package to output unique entity estimation.

We outline these general steps below:

1. Compile the minhash package:
```
cd C++Codes
g++ -std=c++11 *.cpp -fopenmp (on Windows and Linux)
g++-7 *.cpp -fopenmp (on MacOS) 
```

2. Update the Config file for minhash and run the program (Remember to change the outputfile name option to Restaurant_out.csv or the particular name of your data set.)
```
./a.out Config.txt
```
Then it will output Restaurant_out.csv where the output will look like the following```
Rec1 Rec2
1 2
2 3
...
```

3. Feed in Restaurant_out.csv and Restaurant.csv to our unique entity estimation program:

```
Python pipeline.py --input data/Restaurant_out.csv --goldstan data/Restaurant.csv --output any_custom_file_name
```


Other options that one can change include the following:
```
'--trainsize', default='0.1', help='percentage of total pairs to use in training'
'--iter', default='100', help='iterations you want to repeat the process'
'--delimiter', default=',', help='delimeter of input file'
```
*Noted in the delimiter option, the default delimiter for "--goldstan" file is ",", if your file uses different delimiter, which needs to be set here.

The output of this will be the ratio of samples produces from step 2, estimation of the number of unique records in the data set (Restaurant.csv in this example). The output should look like the case below: 


Example output: 
ID RR PRSE LSHE
```
1 0.1 880 742.750000
```

The PRSE refers to the random sampling in [our paper](https://arxiv.org/pdf/1710.02690.pdf) and LSHE is the proposed estimator. RR is the reduction ratio of the number of sampled pairs used in the estimation out of total possible pairs.

An example script: run_script.sh will produce the estimation comparison plot of the in the paper. Note here "--id" option needs to change when the parameters setting for Config.txt changes to produce the plot in the paper.
