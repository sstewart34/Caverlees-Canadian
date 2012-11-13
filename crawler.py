import requests
import html5lib
import unicodedata
import os

from bs4 import BeautifulSoup
from collections import defaultdict

# Get a file-like object for the Python Web site's home page.
urls = defaultdict(list)
#populate the topics with all the topics

topics = [line.strip() for line in open('topics.txt')]
for i in range(len(topics)):
    topics[i] = topics[i].replace(' ', '+')

for topic in topics:
    print topic
url = "http://m.monster.com/JobSearch?searchType=1&addToRecentSearch=True&jobtitle=&keywords="

for topic in topics:
    the_page = requests.get(url + topic).text
    
    soup = BeautifulSoup(the_page)
    spans = soup.find_all(id='LabelJobTitle')
    for span in spans:
        sub_directory = unicodedata.normalize('NFKD', span.parent.get("href")).encode('ascii','ignore') #changes unicode to str
        urls[topic].append('http://m.monster.com' + sub_directory)

if not os.path.exists('DATA'):
    os.makedirs('DATA')
for topic in urls:
    if not os.path.exists('DATA/' + topic):
        os.makedirs('DATA/' + topic)
    for post_url , i in zip(urls[topic] , range(len(urls[topic]))):
        f = open('./DATA/' + topic + '/' + str(i) + '.html', 'w+')
        text = requests.get(post_url).text
        data = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
        f.write(data)
