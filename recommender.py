import utils
import collections
from collections import Counter
import re

def tokenize(tweet):
	tokens = re.findall("[a-zA-Z.#+]+", tweet.lower())
	return tokens

class RecommenderAlgorithm(object):
    def __init__(self, docs):
	self.jobs = docs
	self.indexByLanguage = {}
	self.indexByTopic = {}
	self.languages = []

    def createLanguageList(self):	# Creates an index by languages
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
			if word in self.indexByLanguage:
				if topic not in self.indexByLanguage[word]['topics']:
					self.indexByLanguage[word]['topics'][topic] = 0

				self.indexByLanguage[word]['topics'][topic] += 1
				self.indexByLanguage[word]['count'] += 1
			else:
				if word in self.languages:
					self.indexByLanguage[word] = {'count':1, 'topics':{}}
					self.indexByLanguage[word]['topics'][topic] = 1
		count += 1
	print count
        sorted_list = [x for x in self.indexByLanguage.iteritems()]
	sorted_list.sort(key=lambda x: x[1]['count']) # sort by count
	sorted_list.reverse()
	for item in sorted_list:
		print item[0], item[1]['count'], item[1]['topics']
	#for item in sorted_list:
	#	print item[0]
	#for item in sorted_list:
	#	print  item[1]['count']#, item[1]['topics']
	print len(sorted_list)
	pass

    def createTopicList(self):	# Creates an index by topics
	for language in self.indexByLanguage:
		for topic in self.indexByLanguage[language]['topics']:
			if topic not in self.indexByTopic:
				self.indexByTopic[topic] = {'languages':{}}	
				self.indexByTopic[topic]['languages'][language] = self.indexByLanguage[language]['topics'][topic] 
			else:
				#if language not in self.indexByTopic[topic]['languages']:
					#self.indexByTopic[topic]['languages'][language] = 0
				self.indexByTopic[topic]['languages'][language] = self.indexByLanguage[language]['topics'][topic]
	
	sorted_list = [x for x in self.indexByTopic.iteritems()]
	sorted_list.sort(key=lambda x: x[0]) # sort alphabetically by language
	for item in sorted_list:
		print item[0], item[1]
	pass

    def recommend(self, howMany):
	pass
 
def main():   
    docs = utils.read_docs()
    recommend = RecommenderAlgorithm(docs)
    recommend.createLanguageList()              
    recommend.createTopicList()
    recommend.recommend(1)  
                 
if __name__=="__main__":
    main()
