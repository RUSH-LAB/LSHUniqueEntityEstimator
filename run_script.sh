#!/bin/bash
g++ -std=c++11 C++Codes/*.cpp -o output -fopenmp

For Restaurant
for ((i=4;i<=16;i+=4)) ; 
	do for ((j=1;j<=10; j++));
 		do ./output config_restaurant.txt 1 $i; python pipeline.py --flag 0 --id $i --trainsize 0.5 --input Restaurant_pair.csv --goldstan data/Restaurant.csv --output test ; 
	done
done

python plot.py --input test --gt 753

#For CD
# for ((i=5;i<=12;i+=2)) ; 
# 	do for ((j=1;j<=10; j++));
#  		do ./output config_cd.txt 1 $i; python pipeline.py --flag 0 --id $i --trainsize 0.1 --input Cd_pair.csv --goldstan replicate/cd.csv --delimiter ';' --c 0.1 --output test ; 
# 	done
# done

# python plot.py --input test --gt 9508

#For Voter
# for ((i=25;i<=40;i+=5)) ; 
# 	do for ((j=1;j<=10; j++));
#  		do ./output config_voter.txt 4 $i; python pipeline.py --flag 0 --id $i --trainsize 0.1 --input Voter_pair.csv --goldstan replicate/voter.csv --delimiter ',' --c 0.0001 --output test ; 
# 	done
# done

# python plot.py --input test --gt 255447