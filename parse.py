import requests 
import re
import logging 
import time
import sys 
import json 



pages_to_search = ["Gamestop short squeeze"]
"""
MediaWiki API Demo of 'Parse' module:
https://www.mediawiki.org/wiki/API:Parsing_wikitext#GET_request
"""
URL = "https://en.wikipedia.org/w/api.php"

for page in pages_to_search:
    epoch = str(time.time()).split('.')[0]
    word_list = []
    word_dict = {}
    sorted_word_dict = {}

    S = requests.Session()

    params = {
    "action": "parse",
    "page": page,
    "format": "json"
    }

    wiki_request = S.get(url=URL,params=params)
    data = wiki_request.json()

    # validate page == page 
    if data['parse']["title"] != page:
        print("incorrect page title")
        sys.exit(-1)

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
    convert_to_string = convert_to_string.lower()

    end = convert_to_string.rfind("See also")
    convert_to_string = convert_to_string[:end]
    convert_to_string = convert_to_string.replace(r"\\u", "")
    convert_to_string = convert_to_string.replace("the", '')

    word_list = convert_to_string.split(' ')

    for word in word_list:
        if word.isalpha():
            word_dict[word] = word_dict.get(word, 0) + 1

    word_dict = json.dumps(word_dict)
print(word_dict)


    # insert_query = """
    #                 INSERT INTO wiki_word_count (datetime_checked, page_name, word_count_json)
    #                 (SELECT '{datetime_checked}', '{page}', PARSE_JSON('word_count'));
    #                 """.format(datetime_checked = epoch, page=page.lower, word_count=word_dict)

