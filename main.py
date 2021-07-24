
import yake
import json
import requests
import time
import feedparser
from collections import Counter
import re

# Yake configurations
kw_extractor = yake.KeywordExtractor()
language = "en"
max_ngram_size = 1
deduplication_threshold = 0.1
numOfKeywords = 5

def remove_html_tags(text):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', text)
    return cleantext

def feed_parser(url):
    feeds = feedparser.parse(url)
    keywords_list = ""
    ret_val = []
    lines = ""
    category_tags = ""
    for k in feeds.entries:
        title_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=2, features=None)
        summary_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=10, features=None)
        keywords = title_extractor.extract_keywords(remove_html_tags(k.title))
        keywords += summary_extractor.extract_keywords(remove_html_tags(k.summary))
        for kw in keywords:
            keywords_list += kw[0] + ","
        try:
            for t in k.tags:
                category_tags += t.term + ','
        except:
            print("no tags")
        lines += keywords_list
        keywords_list = ""
    ret_val.append(lines)

    if(len(category_tags)>0):
        category_tags = list(dict.fromkeys(category_tags[1].split(',')))
    else:
        category_tags = []
    ret_val.append(category_tags)
    return ret_val

custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
result = feed_parser("https://danluu.com/atom.xml")

w = custom_kw_extractor.extract_keywords(result[0].replace(',', ' '))
words = [word for word, word_count in Counter(([item.lower() for item in result[0].split(',')])).most_common(10)]
print(result[1]+words)
