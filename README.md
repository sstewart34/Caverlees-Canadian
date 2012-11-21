Caverlees-Canadian
==================

CSCE 470 Project "C" What's Trending Now

How to run the program:
	Type python recommender.py jobs.json into a terminal. This will boot a window with checkbuttons. The user should check off each of the language(s) that he/she knows and click done. The user should also choose an area of Computer Science they are interested in (i.e. information storage and retrieval). Our program will recommend a programming language to the user that they should learn in order to qualify for more jobs.

Dependencies:
	BeautifulSoup (html parsing, web crawling)
	requests library
	html5lib
	unicodedata
	json
	re (regular expressions)
	Tkinter
	tkMessageBox

File Descriptions:

C What's Trending - Checkpoint 1.docx
	Checkpoint 1 document. This word document contains a graph of the top languages used in job descriptions from m.monster.com for 50 topics - 20 documents (or less) per topic.

C What's Trending - Checkpoint 1.pdf
	Checkpoint 1.docx as a pdf
	
DATA/
	Folder which contains all of the job postings for each topic from m.monster.com. This folder contains subfolders, one for each topic. Each of the folders for the topics contain all the job description pages (html), labeled 0-n.html.

crawler.py
	This file crawls m.monster.com. It will grab the file topics.txt to query m.monster.com with each of the topics. The output of crawler.py will be to create the DATA/ folder.

indexByLanguages.json
	This file contains a dictionary of languages. The dictionary is as follows:
	language -> {unique times, total times, topics -> {topic -> count}}

indexByTopics.json
	This file contains a dictionary of topics (the ones we provide). The dictionary is as follows:
	topic -> {languages -> {language -> count}}
	Each topic may also contain urls to pages; not sure yet on the final output.

jobs.json
	This is a json file of all of the job descriptions that we crawled from m.monster.com for all of the topics.
	The format of the file is as follows:
	{topic -> name, jobdescription -> description}

langaugedata.xlsx
	The top langauges are stored in this excel spreadsheet, and a long tailed distribution graph is shown. This is up to and including checkpoint 1 (~850 job postings).

laguagedatac2.xlsx
	The top langauges are stored in this excel spreadsheet, and a long tailed distributio
n graph is shown. This is up to and including checkpoint 2 (~1650 job postings).

languages.txt
	A list of the programming languages of interest. I manually searched through about 50 job descriptions and added more languages that I didn't include the first time. Our program cannot determine more programming languaes on its own, because not all of the job postings have a required skills section with languages only listed. Another problem is that some languages appear in different ways: rubyonrails, ruby-on-rails. Our program cannot capture those correctly (without having two seperate entries for them).

parse.py

recommender.py

tests/

todo.txt

topics.txt

utils.py
