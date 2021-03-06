import json
import math

def cosine(vec1,vec2):
    """
    Takes in 2 dicts of languages -> int (represents a topic/user)
    returns a float representing their cosine similarity
    """
    mag1 = 0
    mag2 = 0
    dotp = 0
    for lang in vec1:
        mag1 += vec1[lang]**2
    for lang in vec2:
        mag2 += vec2[lang]**2
    mag1 = math.sqrt(mag1)
    mag2 = math.sqrt(mag2)

    if mag1 * mag2 == 0:
	return 0.0
 
    for lang in vec1:
        if lang in vec2:
            dotp += ( vec1[lang] * vec2[lang] )
    
    return float( dotp / ( mag1 * mag2 ) )

def nearest(usr, data):
    """
    takes in a dict of languages -> int representing a user
    returns a unicode string which is the nearest topic

    this uses K-nn clusters with a K of 1, where each topic is a cluster
    """
    max = -1.0
    top = ''
    for topic in data:
        sim = cosine(data[topic]['languages'], usr)
        if sim > max:
            max = sim
            top = topic
    return top

def difference(topic, usr):
    """
    take in 2 dicts of languages ->int representing a topic and user
    returns a sorted dict of languages->count the user does not know, from most needed to least
    """
    final = {}
    for lang in topic:
        if lang not in usr:
            final[lang] = topic[lang]
    return [(k, final[k]) for k in sorted(final, key=final.get, reverse=True)]
