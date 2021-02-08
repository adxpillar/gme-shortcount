import requests 
import re

"""
MediaWiki API Demo of 'Parse' module:
Parse content of a page 
"""

s = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

params = {
    "action": "parse",
    "page": "GameStop short squeeze",
    "format": "json"
}

r = s.get(url=URL,params=params)
data = r.json()
# print(data["parse"]["text"]["*"])

# encode and strip
convert_to_string = str(data["parse"]["text"]["*"].encode('utf-8').strip())

# remove everything within an html tag
convert_to_string = re.sub('<[^<]+?>', '', convert_to_string)
convert_to_string = re.sub('&#[^<]+?;[^<]+?;', '', convert_to_string)

# split on punctuations 
convert_to_string = re.sub('[?., %-()"^;:/]', ' ', convert_to_string)

# remove multiple spaces
convert_to_string = re.sub('\\n', ' ', convert_to_string)
convert_to_string = re.sub(' +', ' ', convert_to_string)

# convert to lower 
convert_to_string = convert_to_string.lower()

end = convert_to_string.rfind("See also")
convert_to_string = convert_to_string[:end]

convert_to_string = convert_to_string.replace("the", '')


word_list = []
word_list = convert_to_string.split(' ')

word_dict = {}
for word in word_list:
    word_dict[word] = word_dict.get(word, 0) + 1

sorted_word_dict = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)

short_count = word_dict["short"]
most_popular_word = sorted_word_dict[0][0]


epoch = str(time.time()).split('.')[0]

Query = """
        INSERT INTO gme_wiki_count(datetime_checked, short_count, most_popular_word) VALUES('{datetime_checked}',{short_count},'{most_popular_word}');
        """.format(datetime_checked=epoch,short_count=short_count,most_popular_word=most_popular_word)




print(short_count)
