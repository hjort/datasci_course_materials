#!/usr/bin/python

# Problem 5: Which State is happiest?
# Usage: python happiest_state.py <sentiment_file> <tweet_file>
# Sample: ./happiest_state.py AFINN-111.txt output.txt | less

import sys
import json
import re

sent_dict = {} # initialize an empty dictionary
states = {}

'''
build dictionary from affin file
'''
def build_dict(afinnfile):
	for line in afinnfile:
		term, score = line.split("\t") # the file is tab-delimited
		sent_dict[term] = int(score)   # convert the score to an integer

'''
normalize the given text
'''
def normalize(text):
	# awk '{print$1}' AFINN-111.txt | sed 's/[a-z]\+//g' | sort -u
	return re.sub('[^a-z0-9 -]', '', text.lower())

# retrieved from http://www.census.gov/geo/www/ansi/statetables.html
# awk 'BEGIN{FS="\t"}{print "\""$1"\""": \""$3"\""", "}' us-states.txt
us_codes = {
	"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", 
	"California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", 
	"District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
	"Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", 
	"Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", 
	"Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", 
	"Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
	"New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", 
	"North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", 
	"Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", 
	"South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
	"Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", 
	"Wisconsin": "WI", "Wyoming": "WY"
}

'''
retrieve the state abbreviation relative to the state name passed
'''
def get_state_code(name):
	if name in us_codes:
		return us_codes[name]
	else:
		return None

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

				# compute the score for the tweet
				score = 0
				for word in norm.split():
					if word in sent_dict:
						score += sent_dict[word]
				#print score

				# retrieve location of the tweet
				place = tweet['place']
				cc = None
				pfn = None
				if place is not None:
					cc = place['country_code']
					pfn = place['full_name']

				# these fields were not helpful... :(
				#coord = tweet['coordinates']
				#user = tweet['user']
				#tz = user['time_zone']
				#geo = bool(user['geo_enabled'])
				#loc = user['location']

				# restrict tweets made in US
				if cc == 'US':

					# retrieve the state code (e.g., "Los Angeles, CA")
					sc = pfn[pfn.rfind(", ") + 2 : ]

					# sometimes it has another format (e.g., "Florida, US")
					if sc == 'US':
						sc = get_state_code(pfn[ : pfn.rfind(", ")])
					#print "%s => %s" % (pfn, sc)
					if sc is None:
						continue

					# append or sum the state to the dict
					if sc not in states:
						states[sc] = 0
					states[sc] += score

					#print "%d\t%s" % (score, pfn)

				#print "%d: %s => %s" % (score, text, norm)
		#count += 1
		#if count > 100:
		#	break 

'''
print the scores for all the states found
'''
def print_state_scores():
	for state, score in states.iteritems():
		print "%s %d" % (state, score)

'''
return the abbreviation for the happiest state
'''
def happiest_state():
	happiest = None
	greatest = 0
	for state, score in states.iteritems():
		if score > greatest or happiest is None:
			happiest = state
			greatest = score
	return happiest 

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	build_dict(sent_file)
	read_tweets(tweet_file)
	#print_state_scores()
	print happiest_state()

if __name__ == '__main__':
	main()
