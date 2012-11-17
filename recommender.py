import utils
import collections
from collections import Counter
import re
import json
from Tkinter import *
import tkMessageBox
import Tkinter

class MyClickButton():
    def __init__(self, Button, label, row, column):
	self.clicked = False
	self.Button = Button
        self.Button.bind("<Button-1>", lambda e:self.pressed())
	self.t = label 
	self.r = row
	self.c = column
    
    def pressed(self):
	if self.clicked == True: 
		self.clicked = False 
	else: 
		self.clicked = True
	print self.t, self.clicked

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
	self.window = Tkinter.Tk()
	self.windowVisible = True

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

    # Users provided languages are in userKnownLanguages
    # self.window stuff is the UI
    def recommend(self, howMany):
	userKnownLanguages = []
	for button in self.buttons:
		if(button.clicked == True):
			userKnownLanguages.append(button.t)
	print userKnownLanguages
	self.window.destroy()
	self.windowVisible = False
	input = raw_input("")
	pass

    """
    def recommend(self, howMany):
	pass
    """
    def printToFile(self, fileName):
	file = open(str(fileName), 'w')
	if(fileName == 'indexByTopics.json'):
		file.write(json.dumps(self.indexByTopic))
	else:
		file.write(json.dumps(self.indexByLanguage))
	file.close()
    
    def userInterface(self):
	text = Text(self.window, height=1)
	text.insert(INSERT,"Select the language(s) that you know:")
	#text.grid(row = 0, column = 5)
	self.languages.sort(key=lambda x: x[0])
	xcol = 5
	ycol = 0
	for language in self.languages:
		checkVar = IntVar()
		button = Tkinter.Checkbutton(self.window, variable = checkVar, width = 14, text = language, height=5)
		button.grid(row=xcol, column=ycol)
		button.bind("<Button-1>", lambda e: myButton.pressed())
		myButton = MyClickButton(button, str(language), xcol, ycol)
		self.buttons.append(myButton)
		if ycol > 10:
                        xcol += 1
                        ycol = 0
                else:
                        ycol += 1
        count = 0
	B1 = Tkinter.Button(self.window, text = "Done Selecting")
	B1.grid(row=xcol+1,column=ycol-2)
	B1.bind("<Button-1>", lambda e: self.recommend(1))
	while self.windowVisible == True:
		self.window.mainloop()
	pass

def main():   
    docs = utils.read_docs()
    recommend = RecommenderAlgorithm(docs)
    recommend.createLanguageList()              
    recommend.createTopicList()
    #recommend.printToFile('indexByTopics.json')
    #recommend.printToFile('indexByLanguages.json')
    recommend.userInterface()
    #recommend.recommend(1)    
             
if __name__=="__main__":
    main()
