#!/usr/bin/python

# Problem 2: Derive the sentiment of each tweet
# Usage: python tweet_sentiment.py <sentiment_file> <tweet_file>
# Sample: ./tweet_sentiment.py AFINN-111.txt output.txt | less

import sys
import json
import re

sent_dict = {} # initialize an empty dictionary

def lines(fp):
	print str(len(fp.readlines()))

def build_dict(afinnfile):
	for line in afinnfile:
		term, score = line.split("\t") # the file is tab-delimited
		sent_dict[term] = int(score)   # convert the score to an integer
	#print sent_dict.items() # print every (term, score) pair in the dictionary

def normalize(text):
	# awk '{print$1}' AFINN-111.txt | sed 's/[a-z]\+//g' | sort -u
	return re.sub('[^a-z0-9 -]', '', text.lower())

def read_tweets(fp):
	count = 0
	for line in fp:
		tweet = json.loads(line)
		if 'created_at' in tweet:
			if 'lang' in tweet and tweet['lang'] == 'en':

				text = tweet['text'].encode('utf-8')
				norm = normalize(text)
				
				score = 0
				for word in norm.split():
					if word in sent_dict:
						score += sent_dict[word]
				print score

				#print "%d: %s => %s" % (score, text, norm)
		count += 1
		#if count > 100:
			#break 

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	build_dict(sent_file)
	read_tweets(tweet_file)

if __name__ == '__main__':
	main()
