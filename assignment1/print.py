#!/usr/bin/python

# Problem 0: Query Twitter with Python
# Usage: python print.py

import urllib
import json
import re

# TODO: retrieve term from command arguments
term = "microsoft"

# loop 10 times
page = 0
while page in range(0, 10):
	page += 1

	# perform request and parse JSON response
	response = urllib.urlopen("http://search.twitter.com/search.json?q=" + term + "&page=" + str(page))
	dict = json.load(response)

	# extract result list
	results = dict['results']
	for res in results:
		text = res['text'].encode('utf-8')
		text = re.sub(r'\s+', ' ', text)
		#print "[%s]" % text
		print text

