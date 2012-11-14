import utils
import collections
from collections import Counter
import re

def tokenize(tweet):
	tokens = re.findall("[a-zA-Z]+", tweet.lower())
	return tokens

class RecommenderAlgorithm(object):
    def __init__(self, docs):
	self.jobs = docs
	self.index = {}
	self.languages = []

    def retrieve_docs(self):
	f = open('languages.txt','r')
	for line in f.readlines():
		self.languages.append((line.lower()).strip())
	print len(self.languages)
	count = 0
	for job in self.jobs:
		topic = job['topic']
		if topic == "":
			continue
		text = job['jobDescription']
		for word in tokenize(text.encode('utf8')):
			if word in self.index:
				if topic not in self.index[word]['topics']:
					self.index[word]['topics'][topic] = 0

				self.index[word]['topics'][topic] += 1
				self.index[word]['count'] += 1
			else:
				if word in self.languages:
					self.index[word] = {'count':1, 'topics':{}}
					self.index[word]['topics'][topic] = 1
		count += 1
	print count
        sorted_list = [x for x in self.index.iteritems()]
	sorted_list.sort(key=lambda x: x[1]['count']) # sort by count
	sorted_list.reverse()
	for item in sorted_list:
		print item[0], item[1]['count'], item[1]['topics']
	print len(sorted_list)
 
def main():   
    docs = utils.read_docs()
    recommend = RecommenderAlgorithm(docs)
    recommend.retrieve_docs()              
                   
if __name__=="__main__":
    main()
