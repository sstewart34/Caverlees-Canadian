
import utils
import collections

from collections import Counter

class RecommenderAlgorithm(object):
    
    def retrieve_docs(self, docs):  
        for doc in docs:
            topic = doc['topic']
            text = doc['jobDescription']
            
       
def main():
   
    docs = utils.read_docs()
    recommend = RecommenderAlgorithm()
    recommend.retrieve_docs(docs)              
                   
if __name__=="__main__":
    main()
