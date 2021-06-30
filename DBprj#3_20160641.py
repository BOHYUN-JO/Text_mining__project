#-*- coding: utf-8 -*-
import datetime
import time
import sys
import MeCab
import operator
from pymongo import MongoClient
from bson import ObjectId
from itertools import combinations
import re
import math

def printMenu():
	print "1. WordCount"
	print "2. TF-IDF( 6. Calculating TF-IDF should be preceded ) "
	print "3. Similarity"
	print "4. MorpAnalysis"
	print "5. CopyData"
   	print "6. Calculating TF-IDF"
#In this project, we assume a word seperated by a space is a morpheme.
def MorphAnalysis(docs, col_tfidf):
	print("MorpAnalysis")

	# Step(1) Read stopword list from file named stopwrod_list.txt
	stop_word = {}
	f = open("stopword_list.txt", "r")
	while True:
		line = f.readline()
		if not line: break
		stop_word[line.strip('\n')] = line.strip('\n')
	f.close()

	# Step(2) Anlaysis Morpheme in given text and delete stopword
	for doc in docs:
		content = doc['text']
		#Delete non-alphabetical characters
		content = re.sub('[^a-zA-Z]', ' ', content)
		#change all capital letter to small letter
		content = content.lower().split()

		#delete stopword in a given text dataset
		MorpList = []

		for arg in content:
			if not arg in stop_word:
				MorpList.append(arg)
	# Step(3) Store processed morpheme data into MongoDB
		col_tfidf.update({'_id':doc['_id']}, {'$set': {'morph': MorpList}}, True)

	objId = raw_input("insert objectId : ")
	for doc in col_tfidf.find():
		oId = str(doc['_id'])
		if objId == oId:
			print doc['morph']
	
def WordCount(docs, col_tfidf):
	print("WordCount")
		
	# Step(1) Read stopword list from file named stopwrod_list.txt
	stop_word = {}
	f = open("stopword_list.txt", "r")
	while True:
		line = f.readline()
		if not line: break
		stop_word[line.strip('\n')] = line.strip('\n')
	f.close()

	# Step(2) Anlaysis Morpheme in given text and delete stopword
	for doc in docs:
		content = doc['text']
		#Delete non-alphabetical characters
		content = re.sub('[^a-zA-Z]', ' ', content)
		#change all capital letter to small letter
		content = content.lower().split()

		#delete stopword in a given text dataset
		MorpCount = {}

		for arg in content:
			if not arg in stop_word:
				if arg in MorpCount:
					MorpCount[arg] += 1
				else:
					MorpCount[arg] = 1				
	# Step(3) Store processed morpheme data into MongoDB
		col_tfidf.update({'_id':doc['_id']}, {'$set': {'word_count': MorpCount}}, True)

	objId = raw_input("insert objectId : ")
	for doc in col_tfidf.find():
		oId = str(doc['_id'])
		if objId == oId:
			print doc['word_count']

def calculTfIdf(docs, col_tfidf):
	print("wait...calculating TF-IDF...")
    	#objId = raw_input("insert object Id : ")
	sum = 0
	docCnt = col_tfidf.find().count()
	idf = {}
	tf = {}
	for doc in col_tfidf.find():
		oId = str(doc['_id'])
		sum = 0
		tf.clear()
		tf = doc['word_count']
		idf.clear()
		if len(tf) > 0:						
			for arg in tf:
				idf[arg] = 0
				sum += tf[arg]
			for x in tf:
				tf[x] = float(tf[x])/float(sum)
				idf[x] = col_tfidf.find({"morph":x}).count()	
		
			for x in idf:	
				if idf[x] != 0:
					idf[x] = math.log(float(docCnt)/float(idf[x]))
			for x in tf:
				tf[x] = tf[x]*idf[x]
		else:
			tf['tf_idf'] = 0
		col_tfidf.update({'_id':doc['_id']}, {'$set': {'tf_idf': tf}}, True)
	print "Done!"

def TfIdf(docs, col_tfidf):
	objId = raw_input("insert object Id : ")
	for doc in col_tfidf.find():
		oId = str(doc['_id'])
		if objId == oId:	
			res = sorted(doc['tf_idf'].items(), key=(lambda x:x[1]), reverse=True)
			cnt = 0	
			for item in res:
				cnt += 1
				if cnt > 10:
					break
				print('%-15s %.12f'%(item[0], item[1]))  


def Similarity(docs, col_tfidf):
	print("Similiarity")
	objId1 = raw_input("insert object Id(1) : ")
	objId2 = raw_input("insert object Id(2) : ")
	for doc in col_tfidf.find():
		oId = str(doc['_id'])
		if objId1 == oId:
			doc1 = doc
		elif objId2 == oId:
			doc2 = doc
	tfidf1 = doc1['tf_idf']
	tfidf2 = doc2['tf_idf']
	numerator = 0.0
	denominator = 0.0
	for x in tfidf1:
		if x in tfidf2:
			numerator += tfidf1[x]*tfidf2[x]
	temp1 = 0.0
	temp2 = 0.0
	for x in tfidf1:
		temp1 += tfidf1[x]**2
	temp1 = math.sqrt(temp1)
	for x in tfidf2:
		temp2 += tfidf2[x]**2
	temp2 = math.sqrt(temp2)
	denominator = temp1*temp2
	print numerator/denominator


def copyData(docs, col_tfidf):
	col_tfidf.drop()
	for doc in docs:
		contentDic = {}
		for key in doc.keys():
			if key != "_id":
				contentDic[key] = doc[key]
		col_tfidf.insert(contentDic)

#Access MongoDB
conn = MongoClient('localhost')

#fill it with your DB name - db+studentID ex) db20120121
db = conn['db20160641']

#fill it with your MongoDB( db + Student ID) ID and Password(default : 1234)
db.authenticate('db20160641', '1234')

col = db['tweet']
col_tfidf = db['tweet_tfidf']

if __name__ == "__main__":
	printMenu()
	selector = input()

	if selector == 1:
		docs = col_tfidf.find()
        	WordCount(docs, col_tfidf)

	elif selector == 2:
        	docs = col_tfidf.find()
		TfIdf(docs, col_tfidf)

	elif selector == 3:
		docs = col_tfidf.find()
		Similarity(docs, col_tfidf)

	elif selector == 4:
		docs = col_tfidf.find()
		MorphAnalysis(docs, col_tfidf)

	elif selector == 5:
		docs = col.find()
		copyData(docs,col_tfidf)
	elif selector == 6:
		docs = col_tfidf.find()
		calculTfIdf(docs, col_tfidf)
