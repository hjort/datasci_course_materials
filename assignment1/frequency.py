#!/usr/bin/python

# Problem 4: Compute Term Frequency
# Usage: python frequency.py <tweet_file>
# Sample: ./frequency.py output.txt | less

import sys
import json
import re

terms = {} # initialize an empty dictionary

'''
normalize the given text
'''
def normalize(text):
	# awk '{print$1}' AFINN-111.txt | sed 's/[a-z]\+//g' | sort -u
	return re.sub('[^a-z0-9 -]', '', text.lower())

'''
process the tweets in the JSON file
'''
def read_tweets(fp):
	#count = 0
	for line in fp:
		tweet = json.loads(line)
		if 'created_at' in tweet:
			if 'lang' in tweet and tweet['lang'] == 'en':

				text = tweet['text'].encode('utf-8')
				norm = normalize(text)

				# increment the count of the given term in the dict
				for word in norm.split():
					if len(word) > 1:
						if word not in terms:
							terms[word] = 0
						terms[word] += 1
						#print "%s: %d" % (word, terms[word])

		#count += 1
		#if count > 1000:
		#	break

'''
print the histogram of found terms
'''
def print_terms_frequency():

	# count number of occurrences of all terms in all tweets
	total = 0
	for count in terms.itervalues():
		total += count
	#print "total=", total

	# calculate and print the frequency of each term
	for term, count in terms.iteritems():
		freq = count / float(total)
		print "%s %f" % (term, freq)

def main():
	tweet_file = open(sys.argv[1])
	read_tweets(tweet_file)
	print_terms_frequency()

if __name__ == '__main__':
	main()

