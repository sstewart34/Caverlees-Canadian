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
       			dictionary = {'topic':"", 'jobDescription':""}
			file = open(path)
			page = BeautifulSoup(file)

			jobDescription = page.findAll(id="jobBodyContent")
			for descrip in jobDescription:
      				#print descrip.get_text()
				description = stem(str(descrip.get_text().strip().encode('utf8')))
			        #print descrip.get_text()
				dictionary['jobDescription'] = description[0]
				dictionary['topic'] = topic.replace('+',' ')
		       	allPosts.append(dictionary)
			file.close()	
	#print allPosts
	f = open('jobs.json','w')
	for item in allPosts:
		f.write(json.dumps(item))
		f.write('\n')
	f.close()

if __name__ == "__main__":
	main()
