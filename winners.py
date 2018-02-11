import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import time


# Motion Picture Awards
mAwards = ['Best Motion Picture - Drama','Best Motion Picture - Musical or Comedy','Best Director','Best Actor - Motion Picture Drama','Best Actor - Motion Picture Musical or Comedy',
'Best Actress - Motion Picture Drama','Best Actress - Motion Picture Musical or Comedy','Best Supporting Actor - Motion Picture','Best Supporting Actress - Motion Picture',
'Best Screenplay','Best Original Score','Best Foreign Language Film','Best Animated Feature Film','Cecil B. DeMille Lifetime Achievement Award']

# Television Awards
tAwards = ['Best Drama Series','Best Comedy Series','Best Actor in a Television Drama Series','Best Actor in a Television Comedy Series','Best Actress in a Television Drama Series',
'Best Actress in a Television Comedy Series','Best Limited Series or Motion Picture made for Television','Best Actor in a Series made for Television',
'Best Actress in a Series made for Television','Best Supporting Actor in a Series made for Television',
'Best Supporting Actress in a Series made for Television']

abbreviations = {'television':'tv'}

# List of Award objects that hold information about each award
Award_list = []

# set of keywords relating to the awards
Award_words = set()

class Award:

	def __init__(self,name,presenter,nominees,winner,winner_votes,filtered_sentence):
		self.name = name
		self.presenter = presenter
		self.nominees = nominees
		self.winner = winner
		self.winner_votes = winner_votes
		self.filtered_sentence = filtered_sentence

	def print_award(self):
		print('Award: {}'.format(self.name))
		print('Presented By: {}'.format(self.presenter))
		print('Nominees: {}'.format(', '.join(self.nominees)))
		print('Winner votes: {}'.format(self.winner_votes))
		print('Winner: {}\n'.format(self.winner))


# Initialize awards function that loops through the list of TV and Movie awards and creates Award objects with those names and adds it to Award_list 
# The Function then loops through the award name and creates a list called filtered_sentence which only keeps key words in the award name
def init_awards():

	# Create award objects and add to Award_list
	for mAward in mAwards:
		award_obj = Award(mAward,'',[],'',{},[])
		Award_list.append(award_obj)
	for tAward in tAwards:
		award_obj = Award(tAward,'',[],'',{},[])
		Award_list.append(award_obj)

	# Make a filtered_sentence of key words for each object using stop_words
	stop_words = stopwords.words('english')
	stop_words_custom = ['-','made']
	for award in Award_list:
		filtered_sentence = []
		words = word_tokenize(award.name)
		for word in words:
			if(word not in stop_words and word not in stop_words_custom):
				filtered_sentence.append(word.strip(','))
				Award_words.add(word.strip(',').lower())
		award.filtered_sentence = filtered_sentence
	Award_words.add('golden')
	Award_words.add('globe')


# Opens json file with ~800,000 tweets and returns a list of the tweets
def analyze_tweets(filename):

	# stop_words = ['Best','Golden','Globes','Actor','Actress']
	with open(filename) as data_file:
		tweets = json.load(data_file)

		# for i in range(700000,710000):
		# 	analyze(tweets[i]['text'])


		for tweet in tweets:
			analyze(tweet['text'])


# Analyze algorithm that first finds which award it matches if any
def analyze(tweet):

	tweet_lowercase = tweet.lower()

	# Looking for the winner so filters tweets by 'win' or 'congratulations'
	if('win' in tweet_lowercase or 'congratulations' in tweet_lowercase):

		# We made the assumption that each tweet references at most 1 award (could reference 0)
		# This loop goes through each word of the award name after it was filtered for key words
		# and counts the number of words that match in the tweet
		# We only consider awards where all the keywords are in the tweet
		# Since it is possible that multiple award names could have all its keywords in the tweet,
		# we decided to take the longest award name that has all its keywords in the tweet
		# For instance, the tweet could reference the award name 'Best Actress - Motion Picture Drama'
		# However, both that award and the award 'Best Motion Picture - Drama' would be a match
		# So pick the longer one ('Best Actress - Motion Picture Drama') which is the correct one 
		max_count = 0
		award_guess = None
		for award in Award_list:
			count = 0
			check = True
			for word in award.filtered_sentence:
				word_lowercase = word.lower()
				if word_lowercase not in tweet_lowercase and (word_lowercase not in abbreviations or abbreviations[word_lowercase] not in tweet_lowercase):
					check = False
				else:
					count += 1
			if(count>max_count and check):
				award_guess = award
				max_count = count

		# Only execute if the tweet relates to an award
		if(award_guess != None):

			# Tokenize the words in the tweet and put in list of filtered_sentence
			# Get part of speech tags for each word
			# Find noun chunks for the tweet
			filtered_sentence = word_tokenize(tweet)
			filtered_sentence_pos = pos_tag(filtered_sentence)
			chunked = nltk.ne_chunk(filtered_sentence_pos)
			
			# Named Entity Recognition:
			# Traverse chunk subtrees and search for a noun chunk with the label 'PERSON' and set it equal to winner
			# For our algorithm, we take the first person that shows up in the tweet
			winner = ""
			check = True
			for chunk in chunked.subtrees(filter=lambda t: t.label()=='PERSON'):
				for item in chunk.subtrees():
					for word in item.leaves():
						# If the algorithm is confused and things the award is a persons name then forget it
						if(word[0].lower() in Award_words):
							check = False
							break
						winner += word[0] + ' '
				break
			winner = winner.strip()
			print('First Guess: {}'.format(winner))

			# If the Named Entity Recognition from NLTK doesn't work then find next best possible name
			# Assuming an award is given 'to' someone, then concatenate all captialized words after 'to' if in the tweet
			# If not, then move on to another tweet and ignore this one
			if(check == False or winner == ''):
				winner = ''
				i = None
				print(filtered_sentence)
				for index,word in enumerate(filtered_sentence):
					if(word == 'to'):
						i = index + 1
						break
				if(i != None):
					check = True
					while(i<len(filtered_sentence) and (filtered_sentence[i][0].isupper() or filtered_sentence[i][0] == "'")):
						# If the algorithm is confused and things the award is a persons name then forget it
						if(filtered_sentence[i].lower() in Award_words):
							check = False
							break
						winner += filtered_sentence[i] + ' '
						i += 1
					winner = winner.strip()
					print('Second Guess: {}'.format(winner))		

			print(award_guess.name)
			print(winner)
			print(tweet)
			print('\n')

			# If we found a potential winner, then add 1 to the awards winner dictionary with the person's name as the key
			# If that person's name is not in the dictionary yet then initialize it with a count of 1
			if(check and winner != ""):
				if(winner in award_guess.winner_votes):
					award_guess.winner_votes[winner] += 1
				else:
					award_guess.winner_votes[winner] = 1


# Loops through award objects and looks at the voting lists for each award and picks the appropriate winner with most votes
# Then prints results for each award
def get_results():

	# Sometimes people tweet in all lower case or all upper case, so if a key matches another one in an upper or lower case then add it its value to that one
	# and remove it from the dictionary
	for award in Award_list:
		new_winner_votes = dict(award.winner_votes)
		for person,val in award.winner_votes.items():
			for person2,val2 in award.winner_votes.items():
				if(person != person2):
					if(person.lower() == person2 or person.upper() == person2):
						new_winner_votes[person] += val2
						del new_winner_votes[person2]
		award.winner_votes = dict(new_winner_votes)

	# Finds the person who got the most votes in the winner votes dictionary and sets the award winner to be that person
	for award in Award_list:
		max_votes = 0
		for person,val in award.winner_votes.items():
			if(val>max_votes):
				award.winner = person
				max_votes = val

		award.print_award()



def main():
	t0 = time.time()
	init_awards()
	analyze_tweets('gg2018.json')
	get_results()
	t1 = time.time()
	print("\nTotal Running Time: {}".format(t1-t0))


if __name__ == "__main__":
	main()

