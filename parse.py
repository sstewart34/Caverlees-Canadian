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
	allPosts = []
	json = {'topic':"", 'jobDescription':""}
	file = open(sys.argv[1])
	page = BeautifulSoup(file)
	print page
	jobDescription = page.findAll(id="jobBodyContent")
	for descrip in jobDescription:
		descrip = stem(str(descrip.get_text().rstrip()))
		#print descrip.get_text()
		json['jobDescription'] = descrip
	allPosts.append(json)
	file.close()	
	print allPosts	
if __name__ == "__main__":
	main()
