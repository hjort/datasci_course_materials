#!/usr/bin/python

# Problem 6: Top ten hash tags
# Usage: python top_ten.py <tweet_file>
# Sample: ./top_ten.py output.txt | less

import sys
import json
import re

tags = {} # dict to hold hashtags

'''
normalize the given text
'''
def normalize(text):
	# awk '{print$1}' AFINN-111.txt | sed 's/[a-z]\+//g' | sort -u
	return re.sub('[^a-z0-9 #-]', '', text.lower())
	#return text.lower()

'''
process the tweets in the JSON file
'''
def read_tweets(fp):
	#count = 0
	for line in fp:
		tweet = json.loads(line)
		if 'created_at' in tweet:

			text = tweet['text'].encode('utf-8')
			norm = normalize(text)

			# retrieve hashtags in the tweet
			for token in norm.split():
				if token[0] == '#' and len(token) > 2:
					tag = token[1:]
					if tag not in tags:
						tags[tag] = 0.0
					tags[tag] += 1.0
					#print token

		#count += 1
		#if count > 100:
		#	break 

'''
print all hashtags found and their number of occurrencies
'''
def print_tags_count(max):
	c = 0
	for w in sorted(tags, key = tags.get, reverse = True):
		print w, tags[w]
		c += 1
		if c > max:
			break
	#for tag, count in tags.iteritems():
		#print "%s %.1f" % (tag, count)
		#print "%d\t%s" % (count, tag)

def main():
	tweet_file = open(sys.argv[1])
	read_tweets(tweet_file)
	print_tags_count(10)

if __name__ == '__main__':
	main()
