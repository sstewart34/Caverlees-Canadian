import utils
import collections
from collections import Counter
import re
import json
from Tkinter import *
import tkMessageBox
import Tkinter
import tkFont
import cluster
from operator import itemgetter

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
	#print self.t, self.clicked

def tokenize(tweet):
	tokens = re.findall("[a-zA-Z.#+]+", tweet.lower())
	return tokens

class RecommenderAlgorithm(object):
    """
	Class variables: 
		- All the job postings
		- An index of all languages from the job postings by:
			-- Topic
				Contains topic (i.e. AI) with a language list, and counts
			-- Language
				Contains language (i.e. C++) with a topic list and counts
		- A list of every language in the knowledge base
		- All the user interface check buttons
		- The actual UI window
    """
    def __init__(self, docs):
	self.jobs = docs
	self.indexByLanguage = {}
	self.indexByTopic = {}
	self.languages = []
	self.buttons = []
	self.window = Tkinter.Tk()
	self.windowVisible = True
	self.listbox = Tkinter.Listbox() 
	self.frames = []
	self.restart = False

    """
	Create the index by language
	   Open the languages file
	   Read in all languages and store in class
	   Go through all jobs and create the index - similar to homework 1/2
    	The index has language -> {unique times, total times, topics -> {topic -> count}}
	   Sorts the index by count (total) 
    """
    def createLanguageList(self):
	f = open('languages.txt','r')
	for line in f.readlines():
		self.languages.append((line.lower()).strip())
	#print len(self.languages)
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
	#print count
        sorted_list = [x for x in self.indexByLanguage.iteritems()]
	sorted_list.sort(key=lambda x: x[1]['count']) # sort by count
	sorted_list.reverse()
	#for item in sorted_list:
	#	print item[0], item[1]['count'], item[1]['topics']
	#for item in sorted_list:
	#	print item[0]
	#for item in sorted_list:
	#	print  item[1]['count']#, item[1]['topics']
	#print len(sorted_list)
	pass

    """
        Create the index by topic
           Go through all jobs and create the index - similar to homework 1/2
        The index has topic -> {languages -> {language -> count}}
           Sorts the index alphabetically
    """
    def createTopicList(self):	# Creates an index by topics
	for language in self.indexByLanguage:
		for topic in self.indexByLanguage[language]['topics']:
			if topic not in self.indexByTopic:
				self.indexByTopic[topic] = {'languages':{}}	
				self.indexByTopic[topic]['languages'][language] = self.indexByLanguage[language]['topics'][topic] 
			else:
				self.indexByTopic[topic]['languages'][language] = self.indexByLanguage[language]['topics'][topic]
	
	sorted_list = [x for x in self.indexByTopic.iteritems()]
	sorted_list.sort(key=lambda x: x[0]) # sort alphabetically by language
	#for item in sorted_list:
	#	print item[0], item[1]
	pass

    # Users provided languages are in userKnownLanguages
    # self.window stuff is the UI
    def recommend(self, howMany):
	userKnownLanguages = {}
	for button in self.buttons:
		if(button.clicked == True):
			if button.t not in userKnownLanguages:
				userKnownLanguages[button.t] = 1
	#print userKnownLanguages

	topicOfChoice = ""
	# Grab the topic the user selected
	try:
		index = self.listbox.curselection()[0]
		topicOfChoice = self.listbox.get(index)
	except IndexError:
		pass
	#print topicOfChoice
        
	nearestCluster = cluster.nearest(userKnownLanguages, self.indexByTopic)
		
	for frame in self.frames:
		frame.pack_forget()
	
	self.displayRecommendations(topicOfChoice, userKnownLanguages)
	pass

    def displayRecommendations(self, topicOfChoice, userKnownLanguages):
	unknownLanguages = []
	self.frames[0].destroy()
	mainFrame = Tkinter.Frame(self.window)
	f = tkFont.Font(size=18)
	if topicOfChoice == "":
            print "Since no topic was selected, it is recommended that you learn one of the top languages across all given topics which are the following: "
            topLanguages = ""
	    for x in dict(sorted(self.indexByLanguage.iteritems(), key=itemgetter(1),reverse=True)[:3]):
                print x,
		topLanguages = topLanguages + " " + x
            print
            print
	    
	    text = Tkinter.Text(mainFrame, height = 2, width = 135, font = f)
            text.insert(INSERT,"Since no topic was selected, it is recommended that you learn one of the top languages across all given topics which are the following:")
            text.grid(row = 0, column = 0)
	    text.insert(INSERT,topLanguages)
	    text.grid(row = 1, column = 0)

        else:
            for key in self.indexByTopic[topicOfChoice]['languages']:
                if key not in userKnownLanguages:
                    unknownLanguages.append({'language':key, 'count':self.indexByTopic[topicOfChoice]['languages'][key]})
            
            sortedList = (sorted(unknownLanguages, key=itemgetter('count')))
            
            if len(sortedList) == 0:
                print
		text = Tkinter.Text(mainFrame, font=f)
		text.insert(INSERT, "You already know all the languages that you need to get a job in ")
		text.insert(INSERT, topicOfChoice)
		text.insert(INSERT, ". You are too smart!")
		text.grid(row = 0, column = 0)
		mainFrame.pack(side = TOP)
                print "You already know all the languages that you need to get a job in ", topicOfChoice, ". You are TOO SMART"
                print
                return ''
            print
            
            topicToLearn = sortedList[len(sortedList)-1]['language']
            if topicToLearn == "office":
                topicToLearn = "microsoft office"
	    text2 = Tkinter.Text(mainFrame, height = 2, font=f)
	    text2.insert(INSERT, "It is recommended that you learn ")
	    text2.insert(INSERT, topicToLearn)
	    text2.insert(INSERT, " to increase your job options when searching for a job in ")
	    text2.insert(INSERT, topicOfChoice + ".")
	    text2.grid(row=3, column=0)
            print "It is recommended that you learn ", topicToLearn, " to increase your job options when searching for a job in ", topicOfChoice, "."
            print
        
    	length = len(userKnownLanguages)
        # Determine how close the user is to each topic currently
        nearestCluster = cluster.nearest(userKnownLanguages, self.indexByTopic)
	text3 = Tkinter.Text(mainFrame, height=2, font=f)
	text3.insert(INSERT, "Based on the languages you already know: ")
        print "Based on the languages you already know, ",
        for x in dict(sorted(userKnownLanguages.iteritems(), key=itemgetter(1),reverse=True)[:length]):
            print x, ",",
	    text3.insert(INSERT, x + ", ")
	text3.insert(INSERT, "you are most capable of working in the field of " + nearestCluster + ".")
	text3.grid(row = 4, column = 0)
	
	restart = Tkinter.Button(mainFrame, text="Choose another selection")
	restart.grid(row=5)
        restart.bind("<Button-1>", lambda e: self.restartFunc())
	self.windowVisible = False
	mainFrame.pack(side = TOP)
	self.frames.append(mainFrame)
    	print " you are most capable of working in the field of ", nearestCluster, "."
	pass

    """
	Restart the GUI
    """
    def restartFunc(self):
	for frame in self.frames:
		frame.pack_forget()
	while len(self.frames) > 0:
		self.frames.pop()
	self.window.unbind("<Button-1>")
	self.buttons.pop()
	self.buttons = []
        self.windowVisible = True
        self.listbox = Tkinter.Listbox()
        self.frames = []
	self.restart = True
	self.windowVisible = False 
	self.userInterface()
	pass
	
    """
	Will print a specific index to a file
    """
    def printToFile(self, fileName):
	file = open(str(fileName), 'w')
	if(fileName == 'indexByTopics.json'):
		file.write(json.dumps(self.indexByTopic))
	else:
		file.write(json.dumps(self.indexByLanguage))
	file.close()
    
    """
	Creates a user interface with check buttons. Allows the user to
	select which languages/skills he/she knows and proceed. The information
	will be captured in the recommend() function.
    """
    def userInterface(self):
	mainFrame = Tkinter.Canvas(self.window)
	mainFrame.pack()
	self.frames.append(mainFrame)

	#swin = Tkinter.Scrollbar(mainFrame, width=10, orient=VERTICAL)
    	#swin.pack(fill=Y,side=RIGHT,padx=0,pady=0)

	textFrame = Tkinter.Frame(mainFrame)
	text = Text(textFrame, height=1, width=37)
	text.insert(INSERT,"Select the language(s) that you know:")
	text.grid(row = 0, column = 0)
	
	textFrame.pack(side = TOP)

	self.languages.sort(key=lambda x: x[0])
	xcol = 5 
	ycol = 5

	checkFrame = Tkinter.Frame(mainFrame)
	for language in self.languages:
		checkVar = IntVar()
		button = Tkinter.Checkbutton(checkFrame, height=1, pady=0, variable = checkVar, width = 14, text = language)
		button.grid(row=xcol, column=ycol)
		button.bind("<Button-1>", lambda e: myButton.pressed())
		myButton = MyClickButton(button, str(language), xcol, ycol)
		self.buttons.append(myButton)
		if xcol > 10:
                        ycol += 1
                        xcol = 5
                else:
                        xcol += 1
	checkFrame.pack(side = TOP)

	spaceFrame = Tkinter.Frame(mainFrame)
	t = Text(spaceFrame, height = 5)
	t.grid(row=0, column=0)
	spaceFrame.pack(side = TOP)

	textFrame2 = Tkinter.Frame(mainFrame)
        text2 = Text(textFrame2, height=1, width=56)
        text2.insert(INSERT,"Select the Computer Science topic you are interested in:")
        text2.grid(row=0, column=0)
	textFrame2.pack(side = TOP)

	xcol += 1
	ycol += 1

        count = 0	
	
	listFrame = Tkinter.Frame(mainFrame)
	self.listbox = Tkinter.Listbox(listFrame, selectmode=SINGLE, width=30)
	topics = []	
	for topic in self.indexByTopic:
		topics.append(str(topic))
	
	topics.sort(key=lambda x: x[0])
	count = 1
	for topic in topics:
		self.listbox.insert(count, topic)
		count += 1

	self.listbox.grid(row = xcol+1, column=0)
	listFrame.pack(side = TOP)

	xcol += 1	
	
	doneFrame = Tkinter.Frame(mainFrame)
	B1 = Tkinter.Button(doneFrame, text = "Done Selecting")
	B1.grid(row=xcol+1,column=ycol-2)
	B1.bind("<Button-1>", lambda e: self.recommend(1))
	doneFrame.pack(side = TOP)

	#swin.config(command=mainFrame.yview)

	while self.windowVisible == True:
		self.window.mainloop()
	pass

def main():   
    docs = utils.read_docs()
    recommend = RecommenderAlgorithm(docs)
    recommend.createLanguageList()              
    recommend.createTopicList()
    recommend.printToFile('indexByTopics.json')
    recommend.printToFile('indexByLanguages.json')
    recommend.userInterface()
             
if __name__=="__main__":
    main()
