import csv
import argparse
import numpy as np

def main():
	parser = argparse.ArgumentParser(description='Process.')
	parser.add_argument('--input', help='input file name')
	args = parser.parse_args()
	count(args.input)


def count(inputfile):
	data = np.genfromtxt(inputfile, delimiter=' ')
	x = np.average(data)
	y = np.std(data)
	print "Average is ", x, " Std is ", y


if __name__ == "__main__":
	main()



