#!/usr/bin/python

# Problem 0: Query Twitter with Python
# Usage: python print.py

import urllib
import json
import re

# TODO: retrieve from command arguments
term = "microsoft"

page = 0
while page in range(0, 10):

        page += 1
        #print page

        response = urllib.urlopen("http://search.twitter.com/search.json?q=" + term + "&page=" + str(page))
        dict = json.load(response)

        results = dict['results']
        for res in results:
                text = res['text'].encode('utf-8')
                text = re.sub(r'\s+', ' ', text)
                #print "[%s]" % text
                print text

