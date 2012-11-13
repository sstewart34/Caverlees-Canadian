from bs4 import BeautifulSoup 
import os
import sys
import json
import re

def stem(line):
	tokens = re.split("a\t", str(line))
	return tokens	

def main():
	# Need to loop through each directory and each html doc
	# Grab the topic name from the directory
	topics = os.listdir('./DATA')
	allPosts = []
	for topic in topics:
		for entry in os.listdir('./DATA/' + topic):
			path = './DATA/' + topic + '/' + entry
			print path
       			json = {'topic':"", 'jobDescription':""}
			file = open(path)
			page = BeautifulSoup(file)

			jobDescription = page.findAll(id="jobBodyContent")
			for descrip in jobDescription:
      				description = stem(str(descrip.get_text().rstrip()))
			        #print descrip.get_text()
				json['jobDescription'] = description
				json['topic'] = topic.replace('+',' ')
		       	allPosts.append(json)
			file.close()	
	print allPosts


if __name__ == "__main__":
	main()
