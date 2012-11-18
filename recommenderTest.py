
from operator import itemgetter


class RecommenderAlgorithm(object):
    
    #def topRecommendation(y, knownLanguages, topicLanguages)
        y = 'database'
        knownLanguages = ['c++', 'java', 'xml']
        topicLanguages = {'languages': {'sql': 10, 'java': 30, 'c':5, 'mysql':20}}
        
        unknownLanguages = []
        
        for keys in topicLanguages['languages']:
            if keys not in knownLanguages:
                unknownLanguages.append({'language':keys, 'count':topicLanguages['languages'][keys]})
        
        sortedList = (sorted(unknownLanguages, key=itemgetter('count')))
        
        print    
        print "It is recommended that you learn ", sortedList[len(sortedList)-1]['language'], " to increase your job options when searching for a job in ", y
        print

def main():   
    
    RecommenderAlgorithm()
                 
if __name__=="__main__":
    main()
