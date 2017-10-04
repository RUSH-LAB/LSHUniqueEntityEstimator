# LSH Unique Entity Estinamtor
A package for Estimating the number of unique eneties for a given input dataset with duplicates and near duplicates. See [our paper](https://arxiv.org/pdf/1709.01190.pdf) for theoretical and benchmarking details. 

## Prerequisites
Python 2, ngram, sklearn

## Tutorial

We will present very detailed steps to replicate one result presented in [our paper](), in particular the restaurant dataset (Becasue it is a public dataset). Other results can be replicated in a very similar manner.

Download the dataset from [here](https://hpi.de/naumann/projects/data-quality-and-cleansing/dude-duplicate-detection.html#c114715)
Restaurant.csv is the data file containing all the records with the cluster id in the last column (same cluster id means same entity)
Restaurant_gold.csv is the gold standard file containing all the ground truth pairs.

Use the C++ Package from [here](http://rush.rice.edu/large-scale.html) and also in C++ folder in this repository. This is a fast minhash package which will take dataset as input. It will output candidate pairs which fall in the same buckets. Details in [here] () 
By following the instructions of minhash pacakge, for input Restaurant.csv, we can get output Restaurant_out.csv.

```
Python pipeline.py --input Restaurant_out.csv --goldstan Restaurant.csv --output any_custom_file_name
```
There are other options:
```
'--trainsize', default='0.1', help='percentage of total pairs to use in training'
'--iter', default='100', help='iterations you want to repeat the process'
```
Then you will get an estimation of the number of unique records in Restaurant dataset.

# Preview of Results 
We used three real-world dataset for testing: [Resaurant](), [CD]() and Voter Registration dataset.
