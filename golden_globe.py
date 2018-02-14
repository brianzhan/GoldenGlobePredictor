import json
import pandas as pd
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

pd.options.display.max_colwidth = 300

# data = json.load(open('gg2018.json'))
df = pd.DataFrame(columns = ['text', 'id_str'])

df = pd.read_json('gg2018.json')

# df['text'] = [str(u)for u in df['text']]
# df['text'] = [u.encode('ascii', 'ignore') for u in df['text']]
# df_count = df.groupby('text').count()
# print(df_count.sort_values('id_strcount'))

# df['text'] = [str(u).lower() for u in df['text']]

def tweet_cleaner(tweet_text):
	tweet_text = str(tweet_text)
	if 'RT' in tweet_text and ":" in tweet_text:
		tweet_text = tweet_text[:tweet_text.index('RT')]+tweet_text[tweet_text.index(':')+1:]

	while '@' in tweet_text:
		startPoint = tweet_text.index('@')
		i = 3
		helper = True
		while helper and startPoint+i < len(tweet_text):
			if tweet_text[startPoint+i].isupper:
				tweet_text = tweet_text[:startPoint] + tweet_text[startPoint+1:startPoint+i] + ' ' + tweet_text[startPoint+i:]
				helper = False
			elif tweet_text[startPoint+i] == ' ':
				tweet_text = tweet_text[:startPoint] + tweet_text[startPoint+1:]
				helper = False
			i+=1
		if startPoint + i == len(tweet_text):
			tweet_text = tweet_text[:startPoint] + tweet_text[startPoint+1:]

	while '#' in tweet_text:
		startPoint = tweet_text.index('#')
		i = 3
		helper = True
		while helper and startPoint+i < len(tweet_text):
			if tweet_text[startPoint+i].isupper:
				tweet_text = tweet_text[:startPoint] + tweet_text[startPoint+1:startPoint+i] + ' ' + tweet_text[startPoint+i:]
				helper = False
			elif tweet_text[startPoint+i] == ' ':
				tweet_text = tweet_text[:startPoint] + tweet_text[startPoint+1:]
				helper = False
			i+=1
		if startPoint + i == len(tweet_text):
			tweet_text = tweet_text[:startPoint] + tweet_text[startPoint+1:]
	return tweet_text

df['text'] = [str(u) for u in df['text']]

def keywordFilter(df, keywordList):
	df_useful = df.copy()
	for keyword in keywordList:
		df_useful = df_useful.loc[df_useful['text'].str.contains(keyword, case = False)]
	df_useful['text'] = [u.encode('ascii', 'ignore') for u in df_useful['text']]
	df_helper = df_useful.groupby('text').count()
	# df_helper['tweet'] = df_helper.index
	df_helper = df_helper.reset_index()
	# print (df_helper)
	return df_helper

def keywordGenerator(keyword):
	keyword.replace(',','')
	keyword = keyword.lower()
	keywordList = keyword.split('-')
	keywordList = [x.strip() for x in keywordList]
	# for key in ['-', 'or', 'in', 'a', 'for']:
	# 	while key in keywordList:
	# 		keywordList.remove(key)
	return keywordList


# # valid = 'nominee' in df['text']
# df['text'] = [str(u).lower() for u in df['text']]
# df_useful = df.loc[df['text'].str.contains('present') & df['text'].str.contains('best motion picture')].dropna()
# df_useful = df.loc[df['text'].str.contains('Congradulation') & df['text'].str.contains('Director') & df['text'].str.contains('Best')].dropna()
# df_useful['text'] = [u.encode('ascii', 'ignore') for u in df_useful['text']]
# print(df_useful['text'])
# print(df_useful.groupby('text').count())

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
# mAward15 = 'Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures'
mAward15 = 'Cecil B. DeMille Award'

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

MovieAwardList = [mAward1,mAward2,mAward3,mAward4,mAward5,mAward6,mAward7,mAward8,mAward9,mAward10,mAward11,mAward12,mAward13,mAward14,mAward15]
TVAwardList = [tAward1,tAward2,tAward3,tAward4,tAward5,tAward6,tAward7,tAward8,tAward9,tAward10,tAward11]

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

WrongNames = ['Best', 'Picture', 'Golden', 'Musical', 'Cecil']
def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    FilteredList = []
    for item in names:
    	if sum([x in item for x in WrongNames]) == 0:
    		FilteredList.append(item)
    return FilteredList

for award in MovieAwardList:
	print(award)
	keywordList = keywordGenerator(award)
	keywordList.append('present')
	print(keywordList)
	df_temp = keywordFilter(df,keywordList)
	df_temp['text'] = df_temp['text'].apply(lambda x: tweet_cleaner(x))
	df_temp['presenter'] = df_temp['text'].apply(lambda x: extract_names(str(x)))
	print(df_temp)
