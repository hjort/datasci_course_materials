#!/usr/bin/python

# Problem 5: Which State is happiest?
# Usage: python happiest_state.py <sentiment_file> <tweet_file>
# Sample: ./happiest_state.py AFINN-111.txt output.txt | less

import sys
import json
import re

sent_dict = {} # initialize an empty dictionary
states = {}

def build_dict(afinnfile):
	for line in afinnfile:
		term, score = line.split("\t") # the file is tab-delimited
		sent_dict[term] = int(score)   # convert the score to an integer

def normalize(text):
	# awk '{print$1}' AFINN-111.txt | sed 's/[a-z]\+//g' | sort -u
	return re.sub('[^a-z0-9 -]', '', text.lower())

def read_tweets(fp):
	count = 0
	for line in fp:
		#print line
		tweet = json.loads(line)
		#print tweet
		if 'created_at' in tweet:
			if 'lang' in tweet and tweet['lang'] == 'en':
				text = tweet['text'].encode('utf-8')
				norm = normalize(text)

				# compute the score for the tweet
				score = 0
				for word in norm.split():
					if word in sent_dict:
						score += sent_dict[word]
				#print score

				#coord = tweet['coordinates']
				place = tweet['place']
				cc = None
				pfn = None
				if place is not None:
					cc = place['country_code']
					pfn = place['full_name']
				#user = tweet['user']
				#tz = user['time_zone']
				#geo = bool(user['geo_enabled'])
				#loc = user['location']

				if cc == 'US':

					# retrieve the state code
					sc = pfn[pfn.rfind(", ") + 2 : ]
					if sc not in states:
						states[sc] = 0
					states[sc] += score

					#print "%d\t%s" % (score, pfn)

				#print "%d: %s => %s" % (score, text, norm)
		count += 1
		#if count > 100:
		#	break 

def print_state_scores():
	for state, score in states.iteritems():
		print "%s %d" % (state, score)

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	build_dict(sent_file)
	read_tweets(tweet_file)
	print_state_scores()

if __name__ == '__main__':
	main()
