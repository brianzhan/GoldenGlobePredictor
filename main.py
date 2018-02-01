#! /usr/bin/python

# need function to read tweets, scrape data, pair winners with movies

# award names

# list of years
import nltk
from nltk.corpus import stopwords
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


def predictWinner(category, tweets, parsedList):
	if category == mAward1:
		keywords = ['best', 'picture']
	res = countMatchingTweets(tweets, keywords)


def countMatchingTweets(tweets, keywords):
	d = defaultdict(int)
	for i in range(0, len(tweets)):
		if findMatches(tweets[i], keywords):
			print("ok")


def findMatches(tweet, keywords):
    for word in keywords:
        if word not in tweet:
            return False
    return True


	

# each tweet has 2 attributes, tweets[0]['text'] and tweets[0]['id_str']
# I suspect id_str is useless so will not include it in the array for now
def readTweets():
	tweetsList = []
	with open('test1.json') as data_file:
		print('hi')
		tweets = json.load(data_file)
		for i in range(0, 10000):
			tweetsList.append(tweets[i]['text'])
		# print(tweets[0]['text'])
	return tweetsList

def getBestMotion(tweetsList):
	keywords = ['best', 'picture']
	# d = defaultdict(int)
	foundone = False
	for i in range(0, len(tweetsList)):
		if findMatches(tweetsList, keywords):
			print pos_tag(tweetsList[i]['text'])
			foundone = True
	print foundone
	


def getMoviesList():
	print "get movies"
	movieList = getMoviesList()
	tvList = getTvList()
	presenterList = getPresenterList()

def getMoviesList():
	tree = ElementTree.parse('2018GGData.xml')
	root = tree.getroot()
	body = tree.find('body')
	print 'body is ', body
	content_div = body.findall('div')
	print 'content is ', content_div
	return []

def getTvList():
	return []

def getPresenterList():
	return []
# Television Awards

def main():
	tweetsList = readTweets()
	print len(tweetsList)
	print getBestMotion(tweetsList)

if __name__ == "__main__":
	main()
	
# getMoviesList()

