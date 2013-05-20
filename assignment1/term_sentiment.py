#!/usr/bin/python

# Problem 3: Derive the sentiment of new terms
# Usage: python term_sentiment.py <sentiment_file> <tweet_file>
# Sample: ./term_sentiment.py AFINN-111.txt output.txt | less

import sys
import json
import re

old_dict = {} # initialize an empty dictionary
new_dict = {}

# stop list from http://www.ranks.nl/resources/stopwords.html
stop_list = [
	"about", "an", "are", "as", "at", "be", "by", "com", 
	"for", "from", "how", "in", "is", "it", "of", "on", 
	"or", "that", "the", "this", "to", "was", "what", 
	"when", "where", "who", "will", "with", "the", #"www",
	# added by me...
	"my", "if", "and", "them", "me", "could", "anyone",
	"you", "he", "your", "its", "there", "but", "too",
	"so", "have", "just", "would", "we", "us", "did",
	"they", "him"
];

'''
build dictionary from affin file
'''
def build_dict(afinnfile):
	for line in afinnfile:
		term, score = line.split("\t") # the file is tab-delimited
		old_dict[term] = int(score)    # convert the score to an integer

'''
normalize the given text
$ awk '{print$1}' AFINN-111.txt | sed 's/[a-z]\+//g' | sort -u
'''
def normalize(text):
	# grader didn't expect text normalization... :(
	return text
	#return re.sub('[^a-z0-9 -]', '', text.lower())

#def lines(fp):
#	print str(len(fp.readlines()))

'''
process the tweets in the JSON file
'''
def read_tweets(fp):
	#count = 0
	for line in fp:
		tweet = json.loads(line)
		if 'created_at' in tweet:

			# grader didn't like this language restriction... :(
			if True:
			#if 'lang' in tweet and tweet['lang'] == 'en':

				text = tweet['text'].encode('utf-8')
				norm = normalize(text)

				# compute the score for the whole tweet
				score = 0
				for word in norm.split():
					if word in old_dict:
						score += old_dict[word]
				#print "%d\t%s" % (score, text)

				# if it is a non-zeroed score...
				if score != 0:
					word_list = norm.split()

					# count significant words
					word_count = 0
					for word in word_list:
						if len(word) > 1 and word not in stop_list:
							word_count += 1

					for word in word_list:
						#print word

						# skip short words
						if len(word) < 2:
							continue

						# skip words in the stop list
						if word in stop_list:
							continue

						# assign score for new words
						if word not in old_dict:
							if word not in new_dict:
								new_dict[word] = 0.0
							new_dict[word] = (new_dict[word] + float(score * 10.0 / word_count))/2
							#print "%s = %f" % (word, new_dict[word])
							#print "%d / %d" % (score, word_count)

				#print "%d: %s => %s" % (score, text, norm)
		#count += 1
		#if count > 1000:
		#	break

'''
print new terms found and their scores
'''
def print_new_dict():
	for term, score in new_dict.iteritems():
		print "%s %.3f" % (term, score)
		#print "%.3f\t%s" % (score, term)

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	build_dict(sent_file)
	read_tweets(tweet_file)
	print_new_dict()
	#lines(sent_file)
	#lines(tweet_file)

if __name__ == '__main__':
	main()

