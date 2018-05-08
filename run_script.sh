#!/bin/bash
g++ -std=c++11 C++Codes/*.cpp -o output -fopenmp

#For Restaurant
for ((i=4;i<=16;i+=4)) ; 
	do for ((j=1;j<=10; j++));
 		do ./output config_restaurant.txt 1 $i; python pipeline.py --flag 0 --id $i --trainsize 0.5 --input Restaurant_pair.csv --goldstan data/Restaurant.csv --output test ; 
	done
done

python plot.py --input test --gt 753

