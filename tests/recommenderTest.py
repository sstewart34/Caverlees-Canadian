from operator import itemgetter
import unittest
import parse
import utils

# Case1: User knows language not in the list of languages needed for that topic
# Case2: User knows all languages for the given topic

class RecommenderAlgorithm(object):
    def recommend(self, knownLanguages, topicLanguages, y = 'database'):
        unknownLanguages = []

        for keys in topicLanguages['languages']:
	    if keys not in knownLanguages:
                unknownLanguages.append({'language':keys, 'count':topicLanguages['languages'][keys]})
        
        sortedList = (sorted(unknownLanguages, key=itemgetter('count')))
       
	if len(sortedList) == 0:
		print
		print "You already know all the languages that you need to get a job in ", y, ". You are TOO SMART"
		print 
		return ''
        print    
        print "It is recommended that you learn ", sortedList[len(sortedList)-1]['language'], " to increase your job options when searching for a job in ", y
        print
	return sortedList[len(sortedList)-1]['language']

TESTJSON = {"topic": "testTopic", "jobDescription": "This is just a test content file. This should output that C, C++, and Java are all required languages. Once again, C, C++, and Java. If I put C/C++ together, it will appear as well. There should be a total of four elements in the file."}
 
class TestRecommender(unittest.TestCase):
    def setUp(self):
	self.recommender = RecommenderAlgorithm()
	self.known = []
	self.topicLanguages = {'languages': {'sql': 10, 'java': 30, 'c':5, 'mysql':20}}
	self.parser = parse.Parse('./testHTML')

    def test_recommendOne(self):
	self.known = ["c++", "java", "xml"]
	language = self.recommender.recommend(self.known, self.topicLanguages)
	self.assertEqual(language, 'mysql')
	pass

    # User knows all languages for a topic
    def test_cannotRecommend(self):
	self.known = ['sql', 'java', 'c', 'mysql']
	language = self.recommender.recommend(self.known, self.topicLanguages)
        self.assertEqual(language, '')
	pass    

    # Test the parser
    def test_parserTest(self):
	dictionary = self.parser.parseFile()
	self.assertEqual(len(dictionary), 2)	

if __name__=="__main__":
    unittest.main()
