#!/bin/bash
# g++-5 -std=c++11 C++Codes/*.cpp -o output -fopenmp

# For Restaurant
# for ((i=6;i<=25;i+=6)) ; 
# 	do for ((j=1;j<=10; j++));
#  		do ./output config_restaurant.txt 1 $i; python pipeline.py --flag 0 --id $i --trainsize 0.3 --input Restaurant_pair.csv --goldstan data/Restaurant.csv --output test ; 
# 	done
# done

# python plot.py --input test --gt 753

#For CD
for ((i=6;i<=20;i+=4)) ; 
	do for ((j=1;j<=3; j++));
 		do ./output config_cd.txt 1 $i; python pipeline.py --flag 0 --id $i --trainsize 0.5 --input Cd_pair.csv --goldstan replicate/cd.csv --delimiter ';' --output test ; 
	done
done

python plot.py --input test --gt 9508

#For Voter
# for ((i=25;i<=40;i+=5)) ; 
# 	do for ((j=1;j<=10; j++));
#  		do ./output config_voter.txt 4 $i; python pipeline.py --flag 0 --id $i --trainsize 0.1 --input Voter_pair.csv --goldstan replicate/voter_processed.csv --delimiter ',' --c 0.0001 --output test ; 
# 	done
# done

# python plot.py --input test --gt 255447
