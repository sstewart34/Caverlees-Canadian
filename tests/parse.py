from bs4 import BeautifulSoup 
import os
import sys
import json
import re
import sys

def stem(line):
	tokens = re.split("a\t", str(line))
	return tokens	

class Parse(object):
    def __init__(self, dir):
        self.dir = dir
        pass

    def parseFile(self):
        # Need to loop through each directory and each html doc
        # Grab the topic name from the directory
        #topics = os.listdir('./DATA')
        topics = os.listdir(self.dir)
        allPosts = []
        if self.dir == './DATA':
            for topic in topics:
                for entry in os.listdir(self.dir + topic):
                    path = self.dir + topic + '/' + entry
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
    
        else:
            path = self.dir + '/0.html'
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
                dictionary['topic'] = 'testTopic' 
            allPosts.append(dictionary)
            
            file.close()
            #print allPosts
            f = open('jobsTest.json','w')
            for item in allPosts:
                f.write(json.dumps(item))
                f.write('\n')
                f.close()
	    return allPosts[0]
        pass

def main():
    parser = Parse(str(sys.argv[1]));
    parser.parseFile();

if __name__ == "__main__":
	main()
