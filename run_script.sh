#!/bin/bash
g++ -std=c++11 C++Codes/*.cpp -o output  -fopenmp

#For Restaurant
 for ((i=4;i<=16;i+=4)) ; 
	do for ((j=1;j<=10; j++));
 		do ./output config_restaurant.txt 1 $i; python pipeline.py --flag 0 --id $i --trainsize 0.5 --input Restaurant_pair.csv --goldstan data/Restaurant.csv --output test ; 
 	done
 done

 python plot.py --input test --gt 753


# For CD
#for ((i=1;i<=10;i++)) ; 
#	do ./output config.txt; python pipeline.py --id 1 --delimiter ';' --trainsize 0.1 --input Restaurant_pair.csv --goldstan data/Cd.csv --output test ; 
#done

#python plot.py --input test --gt 9508
