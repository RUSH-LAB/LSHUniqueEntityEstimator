#!/bin/bash
g++-7 C++Codes/*.cpp -o output  -fopenmp

for ((i=1;i<=10;i++)) ; 
	do ./output config.txt; python pipeline.py --id 1 --input Restaurant_pair.csv --goldstan data/Restaurant.csv --output test ; 
done

python plot.py --input test --gt 753


# for ((i=1;i<=10;i++)) ; 
# 	do ./output config.txt; python pipeline.py --id 1 --delimiter ';' --input Restaurant_pair.csv --goldstan data/Cd.csv --output test ; 
# done

# python plot.py --input test --gt 753