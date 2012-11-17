import utils
import collections
from collections import Counter
import re
import json
from Tkinter import *
import tkMessageBox
import Tkinter

def tokenize(tweet):
	tokens = re.findall("[a-zA-Z.#+]+", tweet.lower())
	return tokens

class RecommenderAlgorithm(object):
    def __init__(self, docs):
	self.jobs = docs
	self.indexByLanguage = {}
	self.indexByTopic = {}
	self.languages = []
	self.buttons = []

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
					self.indexByLanguage[word] = {'unique':1, 'count':1, 'topics':{}}
					self.indexByLanguage[word]['topics'][topic] = 1
		count += 1
	for language in self.indexByLanguage:
		self.indexByLanguage[language]['unique'] = len(self.indexByLanguage[language]['topics'])
	print count
        sorted_list = [x for x in self.indexByLanguage.iteritems()]
	sorted_list.sort(key=lambda x: x[1]['count']) # sort by count
	sorted_list.reverse()
	#for item in sorted_list:
	#	print item[0], item[1]['count'], item[1]['topics']
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
	#for item in sorted_list:
	#	print item[0], item[1]
	pass

    def recommend(self, howMany):
	for button in self.buttons:
		print type(button)
		#text = button.text
		#var = button.var
		#if var == 1:
		#	print text, " was pressed!" 
	pass

    def printToFile(self, fileName):
	file = open(str(fileName), 'w')
	if(fileName == 'indexByTopics.json'):
		file.write(json.dumps(self.indexByTopic))
	else:
		file.write(json.dumps(self.indexByLanguage))
	file.close()

    def userInterface(self):
	top = Tkinter.Tk()
	text = Text(top, height=1)
	text.insert(INSERT,"Select the language(s) that you know:")
	#text.grid(row = 0, column = 5)
	self.languages.sort(key=lambda x: x[0])
	xcol = 5
	ycol = 0
	for language in self.languages:
		checkVar = IntVar()
		self.buttons.append(Tkinter.Checkbutton(top, variable = checkVar, width = 14, text = language, onvalue = 1, offvalue = 0, height=5).grid(row = xcol, column = ycol))
		if ycol > 10:
			xcol += 1
			ycol = 0 
		else:
			ycol += 1

	B1 = Tkinter.Button(top, text = "Done Selecting", command = self.recommend(1)).grid(row = xcol+1, column = ycol-2)
	top.mainloop()
	pass

def main():   
    docs = utils.read_docs()
    recommend = RecommenderAlgorithm(docs)
    recommend.createLanguageList()              
    recommend.createTopicList()
    #recommend.printToFile('indexByTopics.json')
    #recommend.printToFile('indexByLanguages.json')
    recommend.userInterface();    
             
if __name__=="__main__":
    main()
