import argparse
import jellyfish
import csv
from sklearn import linear_model, ensemble, svm
import random
import os.path
import pickle
import ngram
import datetime


def main():
	parser = argparse.ArgumentParser(description='Process.')
	parser.add_argument('--input', help='an integer for the accumulator')
	parser.add_argument('--output', help='an integer for the accumulator')
	parser.add_argument('--goldstan', help='an integer for the accumulator')
	parser.add_argument('--num', help='an integer for the accumulator')

	args = parser.parse_args()

	#similarity stage
	candidates,matrix, Allpair, Total, raw, goldPairs = calculate_sim(args.input, args.goldstan, args.sim)

	#random forests stage
	predict_random = []
	predict_hashing = []

	with open(args.output, 'a+') as write:
		writer = csv.writer(write, delimiter=' ')
		for i in range(100):
			#print "-------------------------------------------------------------"
			estimate_random, estimate_hashing = random_forest(matrix, candidates, Allpair, Total, raw, goldPairs)
			if estimate_random<1000000:
				predict_random.append(estimate_random)
			predict_hashing.append(estimate_hashing)
			writer.writerow([args.num, estimate_random, estimate_hashing])
			print args.num, estimate_random, estimate_hashing


def calculate_sim(inputf, standard, sim):
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
			matrix[(int(row[0]), int(row[1]))] = cal_score(int(row[0]), int(row[1]), raw)
	return  candidates, matrix, Allpair, Total, raw, goldPairs


def random_forest(matrix, candidates, Allpair, Total, raw, goldPairs):
	#split train and test
	posnum = 1000
	negnum = 1000
	poslist = []
	poslabels = []
	pospair = []

	neglist = []
	neglabels = []
	negpair = []

	trainlist = []
	trainlabels = []
	testlist = []
	testlabels = []

	train_pair = []
	test_pair = []

	randomresultlist = []
	randomresultlabels = []
	random_pair = []

	hashinglist = []
	hashinglabels = []
	hashing_pair = []


	randomlist = {}
	random.shuffle(goldPairs)
	for i in range(posnum):
		datapoint = cal_score(goldPairs[i][0], goldPairs[i][1], raw)
		poslist.append(datapoint)
		poslabels.append(datapoint[0])
		pospair.append((goldPairs[i][0], goldPairs[i][1]))

	count = 0
	for i in range(len(raw)**2):
		if count==negnum:
			break
		a = random.randint(1, len(raw)-1)
		b = random.randint(1, len(raw)-1)
		amax = max(a, b)
		bmin = min(a, b)
		if raw[a][-1]!=raw[b][-1]:
			count+=1
			datapoint = cal_score(bmin, amax, raw)
			neglist.append(datapoint)
			neglabels.append(datapoint[0])
			negpair.append((bmin, amax))

	trainlist = poslist[:posnum/2]+neglist[:negnum/2]
	trainlabels = poslabels[:posnum/2]+neglabels[:negnum/2]
	train_pair = pospair[:posnum/2]+negpair[:negnum/2]

	testlist = poslist[posnum/2:]+neglist[negnum/2:]
	testlabels = poslabels[posnum/2:]+neglabels[negnum/2:]
	test_pair = pospair[posnum/2:]+negpair[negnum/2:]
	t=0
	a = datetime.datetime.now()
	for i in range(len(candidates)):
		t+=1
		datapoint = cal_score(candidates[i][0], candidates[i][1], raw)
		if t==10000:
			print datetime.datetime.now()-a

	for i in range(len(candidates)):
		a = random.randint(1, len(raw)-1)
		b = random.randint(1, len(raw)-1)
		if (a==b):
			b = random.randint(1, len(raw)-1)
		amax = max(a, b)
		bmin = min(a, b)
		datapoint = cal_score(bmin, amax, raw)
		randomresultlist.append(datapoint[1:81])
		randomresultlabels.append(datapoint[0])
		random_pair.append((bmin, amax))

	#train svm
	svmt = svm.SVC(C=100)
	svmt.fit(trainlist, trainlabels)

	#test on testing data
	testresultlist = svmt.predict(trainlist+testlist)

	#test on random selection
	randomselection = svmt.predict(randomresultlist)
	Predict_pairs_random = sum(randomselection)

	#test on hashing selection
	hashingselection = svmt.predict(hashinglist)
	Predict_pairs_hashing = sum(hashingselection)

	random_recall = calculate_pr(randomselection,testresultlist, trainlabels+testlabels, train_pair+test_pair, random_pair, raw)
	if random_recall == 'inf':
		estimate_random = random_recall
	else:
		estimate_random = probability(randomselection, random_recall, random_pair, raw)

	hashing_recall = calculate_pr( hashingselection, testresultlist,trainlabels+testlabels, train_pair+test_pair, hashing_pair, raw)
	estimate_hashing = probability(hashingselection, hashing_recall, hashing_pair, raw)

	return estimate_random, estimate_hashing


def cal_score(i, j, raw):
	result = [int(raw[i][-1]==raw[j][-1])]
	candidate1 = raw[i]
	candidate2 = raw[j]
	for i in range(min(len(candidate1), len(candidate2))-1):
		score = ngram.NGram.compare(candidate1[i], candidate2[i], N=3)
		result.append(score)
	return result


def probability(result, p, c_pair, raw):
	cluster = {}
	neighbors = {}
	checklist = []
	j = 0

	for i in range(len(c_pair)):
		if result[i]==1:
			checklist.append(c_pair[i])
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


def calculate_pr(resultlist, testresultlist, labels, test_pair, c_pair, raw):
	TP = 0
	FP = 0
	P = sum(labels)

	for i in range(len(testresultlist)):
		if testresultlist[i]==1:
			if labels[i]==1:
				TP+=1
			else:
				FP+=1

	recall = TP*1.0/P
	a=0
	for i in range(len(labels)):
		if labels[i]==1:
			if test_pair[i] in c_pair:
				if resultlist[c_pair.index(test_pair[i])]==1:
					a+=1

	if a==0:
		return 'inf'
	else:
		return (a*1.0/P)


if __name__ == "__main__":
	main()
