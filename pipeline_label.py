import argparse
import jellyfish
import csv
from sklearn import linear_model, ensemble, svm
import random
import os.path
import pickle
import ngram
from math import sqrt, floor, factorial
from sympy import Symbol, Rational, binomial


def main():
	parser = argparse.ArgumentParser(description='Process.')
	parser.add_argument('--input', help='an integer for the accumulator')
	parser.add_argument('--output', help='an integer for the accumulator')
	parser.add_argument('--goldstan', help='an integer for the accumulator')
	parser.add_argument('--num', help='an integer for the accumulator')

	args = parser.parse_args()

	#similarity stage
	candidates,matrix, Allpair, Total, raw, goldPairs = calculate_sim(args.input, args.goldstan)

	#random forests stage
	predict_random = []
	predict_hashing = []

	with open(args.output, 'a') as write:
		writer = csv.writer(write, delimiter=' ')
		for i in range(100):
			estimate_random, estimate_hashing, estimate_bfs, estimate_classic = random_forest(matrix, candidates, Allpair, Total, raw, goldPairs)
			if estimate_random<1000000:
				predict_random.append(estimate_random)
			predict_hashing.append(estimate_hashing)
			writer.writerow([args.num, estimate_random, estimate_hashing, estimate_bfs, estimate_classic])
			print args.num, estimate_random, estimate_hashing, estimate_bfs, estimate_classic


def calculate_sim(inputf, standard):
	raw = {}
	#read raw data
	Allpair = {}
	with open(standard, 'rb') as pairs:
		pairs.readline()
		reader = csv.reader(pairs, delimiter=';')
		i=1
		for row in reader:
			if row[-1] in Allpair:
				Allpair[row[-1]].append(i)
			else:
				Allpair[row[-1]] = [i]

			raw[i] = row
			i+=1
	Total = len(raw)

	#creat all pairs
	goldPairs = []
	for cluster in Allpair:
		if len(Allpair[cluster])>1:
			values = Allpair[cluster]
			for i in range(len(values)):
				for j in range(i+1, len(values)):
					goldPairs.append((values[i], values[j]))
	#read candidate pairs
	matrix = {}
	candidates = []
	with open(inputf, 'rb') as candidate:
		reader = csv.reader(candidate, delimiter=',')
		reader.next()
		for row in reader:
			candidates.append((int(row[0]),int(row[1])))

	return  candidates, matrix, Allpair, Total, raw, goldPairs


def random_forest(matrix, candidates, Allpair, Total, raw, goldPairs):

	for i in range(len(candidates)):
		datapoint = cal_score(candidates[i][0], candidates[i][1], raw)
		hashinglist.append(datapoint)
		hashinglabels.append(datapoint[0])
		hashing_pair.append(candidates[i])

	for i in range(len(candidates)):
		a = random.randint(1, len(raw)-1)
		b = random.randint(1, len(raw)-1)
		if (a==b):
			b = random.randint(1, len(raw)-1)
		amax = max(a, b)
		bmin = min(a, b)
		datapoint = cal_score(bmin, amax, raw)
		randomresultlist.append(datapoint)
		randomresultlabels.append(datapoint[0])
		random_pair.append((bmin, amax))


	estimate_random = calculate_random( trainlabels+testlabels, train_pair+test_pair, random_pair, raw)
	
	hashing_recall = calculate_pr( trainlabels+testlabels, train_pair+test_pair, hashing_pair, raw)
	estimate_hashing = probability(hashing_recall, hashing_pair, raw)

	estimate_random=0
	estimate_hashing=0

	estimate_bfs = bfs(raw, len(candidates))
	estimate_classic = classic(raw, len(candidates))
	return estimate_random, estimate_hashing, estimate_bfs, estimate_classic


def bfs(raw, budget):
	check = {}
	C = []

	for i in range(len(raw)):
		if budget<0:
			break
		vertex = random.randint(1, len(raw))
		if vertex not in check:
			check[vertex] = 1
			cn = 1
			for other in raw:
				if vertex!=other:
					budget -=1
					if raw[vertex][-1]==raw[other][-1]:
						cn+=1
						check[other] = 1
			C.append(cn)
	s = len(C)
	estimation = [1.0/x for x in C]
	result = sum(estimation)/s*len(raw)
	return result


def classic(raw, budget):
	check = {}
	xlength = sqrt(budget*2)
	C={}
	# for i in range(1, len(raw)+1):
	# 	C[i] = 0
	P = xlength*1.0/len(raw)
	Q = 1-P

	vertices = random.sample(range(1, len(raw)), int(floor(xlength)))

	for vertex in vertices:
		if vertex not in check:
			check[vertex] = 1
			cn = 1
			for other in vertices:
				if vertex!=other:
					if raw[vertex][-1]==raw[other][-1]:
						cn+=1
						check[other] = 1
			if cn in C:
				C[cn]+=1
			else:
				C[cn]=1
	result = 0
	for i in range(1, len(raw)+1):
		K = 0
		for r in C:
			if r>=i:
				K+= binomial(r, i)*(P**(-r))*((-Q)**(r-i))*C[r]
		result+=K

	return result


def nCr(n,r):
    f = factorial
    return f(n) / f(r) / f(n-r)


def cal_score(i, j, raw):
	result = [int(raw[i][-1]==raw[j][-1])]
	return result


def calculate_random(labels, test_pair, random_pair, raw):
	TP = 0
	FP = 0
	P = sum(labels)

	for i in range(len(random_pair)):
		if raw[random_pair[i][0]][-1]==raw[random_pair[i][1]][-1]:
			TP+=1
	a=0
	for i in range(len(labels)):
		if labels[i]==1:
			if test_pair[i] in random_pair:
				a+=1
	if a==0:
		return 'inf'
	else:
		return TP/(a*1.0/P)


def probability(p, c_pair, raw):
	cluster = {}
	neighbors = {}
	checklist = []
	j = 0

	for pair in c_pair:
		if raw[pair[0]][-1]==raw[pair[1]][-1]:
			checklist.append(pair)
		j+=1

	checklist = sorted(checklist)

	i = 1
	for real in checklist:
		one = real[0]
		two = real[1]
		if one in cluster:
			ids = cluster[one]
			cluster[two] = ids
			if two not in neighbors[ids]:
				neighbors[ids].append(two)
		else:
			cluster[one] = i
			cluster[two] = i
			neighbors[i] = [one, two]
			i+=1
	
	n2 = 0
	n3 = 0
	n4 = 0
	nn = 0
	track = 0
	for neighbor in neighbors:
		track+=len(neighbors[neighbor])
		if len(neighbors[neighbor])==2:
			n2+=1
		elif len(neighbors[neighbor])==3:
			n3+=1
		else:
			nn+=1
			

#	n4o = 1.0*n4/(1-((1-p)**3)*(p**3)*4-((1-p)**4)*(p**2)*15- ((1-p)**5)*(p)*6)
	n1 = len(raw) - track
	n3o = 1.0*n3/(1 - 3*(1-p)**2*p - (1-p)**3)
	n2o = 1.0*(n2 - n3o*(3*(1-p)**2*p))/p
	n1o = n1 - 2*n2o*(1-p) - 3*n3o*(1-p)**3 - n3o*p*(1-p)**2
	return n1o+n3o+n2o+nn


def calculate_pr(labels, test_pair, c_pair, raw):
	TP = 0
	FP = 0
	P = sum(labels)

	for i in range(len(c_pair)):
		if raw[c_pair[i][0]][-1]==raw[c_pair[i][1]][-1]:
			TP+=1
	a=0
	for i in range(len(labels)):
		if labels[i]==1:
			if test_pair[i] in c_pair:
				a+=1
	hashing_recall = (a*1.0/P)
	return hashing_recall


if __name__ == "__main__":
	main()
