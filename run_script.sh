#!/bin/bash
 g++-7 -std=c++11 C++Codes/*.cpp -o output -fopenmp

# For Restaurant
# for ((i=6;i<=25;i+=6)) ; 
# 	do for ((j=1;j<=10; j++));
#  		do ./output config_restaurant.txt 1 $i; python pipeline.py --flag 0 --id #$i --trainsize 0.3 --input data/Restaurant_pair.csv --goldstan data/data.csv --output #log-restaurant ; 
# 	done
# done

# python plot.py --input log-restaurant --gt 753

#For CD
for ((i=6;i<=20;i+=4)) ; 
	do for ((j=1;j<=3; j++));
 		do ./output config_cd.txt 1 $i; python pipeline.py --flag 0 --id $i --trainsize 0.5 --input data/CD.csv --goldstan data/cd.csv --delimiter ';' --output log-cd ; 
	done
done

python plot.py --input log-cd --gt 9508

#For Voter
# for ((i=25;i<=40;i+=5)) ; 
# 	do for ((j=1;j<=10; j++));
#  		do ./output config_voter.txt 4 $i; python pipeline.py --flag 0 --id $i --trainsize 0.1 --input Voter_pair.csv --goldstan data/voter_processed.csv --delimiter ',' --c 0.0001 --output log-voter ; 
# 	done
# done

# python plot.py --input log-voter --gt 255447
