#! /usr/bin/python

import nltk
from nltk.tag import pos_tag
from collections import Counter
import json
import xml.etree.ElementTree as ElementTree


# Motion Picture Awards
mAward1 = 'Best Motion Picture - Drama'
mAward2 = 'Best Motion Picture - Musical or Comedy'
mAward3 = 'Best Director'
mAward4 = 'Best Actor - Motion Picture Drama'
mAward5 = 'Best Actor - Motion Picture Musical or Comedy'
mAward6 = 'Best Actress - Motion Picture Drama'
mAward7 = 'Best Actress - Motion Picture Musical or Comedy'
mAward8 = 'Best Supporting Actor - Motion Picture'
mAward9 = 'Best Supporting Actress - Motion Picture'
mAward10 = 'Best Screenplay'
mAward11 = 'Best Original Score'
mAward12 = 'Best Original Song'
mAward13 = 'Best Foreign Language Film'
mAward14 = 'Best Animated Feature Film'
mAward15 = 'Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures'

# Television Awards
tAward1 = 'Best Drama Series'
tAward2 = 'Best Comedy Series'
tAward3 = 'Best Actor in a Television Drama Series'
tAward4 = 'Best Actor in a Television Comedy Series'
tAward5 = 'Best Actress in a Television Drama Series'
tAward6 = 'Best Actress in a Television Comedy Series'
tAward7 = 'Best Limited Series or Motion Picture made for Television'
tAward8 = 'Best Actor in a Limited Series or Motion Picture made for Television'
tAward9 = 'Best Actress in a Limited Series or Motion Picture made for Television'
tAward10 = 'Best Supporting Actor in a Series, Limited Series or Motion Picture made for Television'
tAward11 = 'Best Supporting Actress in a Series, Limited Series or Motion Picture made for Television'

ignore_list = ['golden', 'globes', 'globe', 'goldenglobes', '#goldenglobes', 'oscars']
# stopwords = snltk.corpus.stopwords.words('english')

# main function for finding the winner in a category
def findWinner(tweetsList):
	for i in range(0, 1000):
		if "Congratulations to" in tweetsList[i]:
			print tweetsList[i]
	print "done"


# function to find nominees, given keywords that relate to a category
def findNominee(keywords, tweets):
	print "entered findNominee"
	relevantList = relevantTweets(keywords, tweets)
	nomineeList = {}
	accurateList = []
	for tweet in relevantList:
		print "a tweet is ", tweet
		tweetUnigram = tweet.split()
		pnoun = []
		taggedTweets = pos_tag(tweetUnigram)
		for word, tag in taggedTweets:
			print 'tag is ', tag
			if tag == 'NNP':
				pnoun.append(word)
		print "pnoun list is ", pnoun
		for unigram in tweetUnigram:
			# idea is find an at to the nominee
			if unigram[0]=='@' and nomineeList.has_key(unigram):
				nomineeList[unigram] +=1
			else:
				nomineeList[unigram] = 1
	for nominee in nomineeList:
		if nomineeList[nominee] > 3:
			accurateList.append(nominee)
		else:
			print "ignored ", nominee
	return accurateList

# helper function for main(), to extract tweets in a array
def readTweets():
	tweetsList = []
	with open('test1.json') as data_file:
		tweets = json.load(data_file)
		for i in range(0, 1000):
			tweetsList.append(tweets[i]['text'])
		# print(tweets[0]['text'])
	return tweetsList

# helper function for relevantTweets()
def findMatches(tweet, keywords):
    for word in keywords:
        if word not in tweet:
            return False
    return True

# helper function for findNominee()
def relevantTweets(keywords, tweetList):
	relevantList = []
	for tweet in tweetList:
		if findMatches(tweet, keywords):
			print "found match between ", tweet, " and ", keywords
			relevantList.append(tweet)
	return relevantList

def main():
	tweetsList = readTweets()
	# find nominees
	nomineeToFind = mAward1
	if nomineeToFind == mAward1:
		keywords = ['best']
		print findNominee(keywords, tweetsList)

if __name__ == "__main__":
	main()
	
# getMoviesList()

