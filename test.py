import json
import sys
from pprint import pprint 


with open('test1.json', encoding='utf-8') as data_file:
	print('hi')
	tweets = json.load(data_file)
	print(tweets[0])


	# json.load(data_file)
	# data = json.loads(data_file.read())




# with open("gg2018.json") as f:
#     z = json.load(f)


# f = open('gg2018.json','r').read()
# json.loads(f)


