
# -*- coding: utf-8 -*-
import requests
import json

#Add your search term here. Spaces are allowed. The searches will be performed using exact match in both The Guardian and NYT systems.
#Currently, it is populated with a search for articles about fraud in advertising. See the output of this search in the file, SAMPLEarticle_data.csv
SEARCH_TERM = 'ad fraud'

CACHE_FILEN = "cache_file_name.json"

#Assign the below two variables with your API keys **IN STRING TYPE** from the guardian and New York Times. THE CODE WILL NOT RUN WITHOUT THESE.
NYT_API_KEY =
GUARDIAN_API_KEY =

#Below section looks for the cache dictionary in the cache file and sets it up if it is not found.
try:
    cache_file = open(CACHE_FILEN, 'r')
    cache_contents = cache_file.read()
    cache_diction = json.loads(cache_contents)
    cache_file.close()
except:
    cache_diction = {}

#Below function is a cacheing system that uses the dictionary in the cache folder, creating a distinct key for each search.
def params_unique_combination(baseurl, params_d, private_keys=["api-key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)


# The below function takes the search query as an input and looks for it in the cache dictionary.
# If it does not find the search query in the dictionary, it will use the Requests module to get the data from the New York Times API and then cache it
def get_from_nyt_caching(search_query):

    baseurl = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params_diction = {}
    params_diction["q"] = search_query
    params_diction["api-key"] = NYT_API_KEY


    unique_ident = params_unique_combination(baseurl,params_diction)

    if unique_ident in cache_diction:
        return cache_diction[unique_ident]
    else:
        resp = requests.get(baseurl, params_diction)
        cache_diction[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(cache_diction, indent=4)
        fw = open(CACHE_FILEN,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return cache_diction[unique_ident]

# The below function takes the search query as an input and looks for it in the cache dictionary.
# If it does not find the search query in the dictionary, it will use the Requests module to get the data from the Guardian API and then cache it
def get_from_guardian_caching(search_query):

    baseurl = "https://content.guardianapis.com/search"
    params_diction = {}
    params_diction["q"] = search_query
    params_diction["api-key"] = GUARDIAN_API_KEY
    params_diction["show-fields"] = "headline,trailText,byline"
    params_diction["show-tags"] = "keyword"

    unique_ident = params_unique_combination(baseurl,params_diction)

    if unique_ident in cache_diction:
        return cache_diction[unique_ident]
    else:
        resp = requests.get(baseurl, params_diction)
        cache_diction[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(cache_diction, indent=4)
        fw = open(CACHE_FILEN,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return cache_diction[unique_ident]


#The below section creates a class for data on a single article from the New York Times retreived from the API
#The NYT returns a JSON file for each search containing data on many articles
#This will allow me to pull data for a specific article out of that JSON and create an object for it
class NYTArticle:

    def __init__(self,article_diction):
        self.article_title = article_diction["headline"]["main"]
        self.author = article_diction["byline"]["original"]
        if "news_desk" in article_diction:
            self.section = article_diction["news_desk"]
        else:
            self.section = article_diction["document_type"]
        self.url = article_diction["web_url"]
        self.publication = "New York Times"
        self.snippet = article_diction["snippet"]
        self.keywords = []
        key_list = article_diction["keywords"]
        for key in key_list:
            self.keywords.append(key["value"])

    def __str__(self):
        return "{}: {}".format(self.article_title, self.snippet)

    def headline_wordcount(self):
        headline_list = self.article_title.split()
        return len(headline_list)

#The below section creates a class for data on a single article from the Guardian retreived from the API
#The Guardian returns a JSON file for each search containing data on many articles
#This will allow me to pull data for a specific article out of that JSON and create an object for it
class GuardianArticle:

    def __init__(self,article_diction):
        self.article_title = article_diction["fields"]["headline"]
        self.author = article_diction["fields"]["byline"]
        self.section = article_diction["pillarName"]
        self.url = article_diction["webUrl"]
        self.snippet = article_diction["fields"]["trailText"]
        self.publication = "The Guardian"
        self.keywords = []
        key_list = article_diction["tags"]
        for key in key_list:
            self.keywords.append(key["webTitle"])

    def __str__(self):
        return "{}: {}".format(self.article_title, self.snippet)

    def headline_wordcount(self):
        headline_list = self.article_title.split()
        return len(headline_list)

#This part creates lists of the nyt and guardian articles. each item in the list is an nyt or guardian article
#The code loops through the JSON response from NYT and The Guardian and pulls out data for each individual article and stores it as an article in the list
#There is one list for NYT articles and another list for Guardian articles
nyt_result = get_from_nyt_caching('"'+SEARCH_TERM+'"~0')

nyt_article_insts = []

for article_diction in nyt_result["response"]["docs"]:
    nyt_article_insts.append(NYTArticle(article_diction))


guardian_result = get_from_guardian_caching('"'+SEARCH_TERM+'"')

guardian_article_insts = []

for article_diction in guardian_result["response"]["results"]:
    guardian_article_insts.append(GuardianArticle(article_diction))

#This opens the CSV file into which the output data on the articles will go
article_data = open("article_data.csv","w")
article_data.write("ARTICLE_TITLE,AUTHOR,SECTION,NUMBER_OF_WORDS_IN_TITLE,PUBLICATION,URL,KEYWORDS")
article_data.write("\n")

#This function writes data into the CSV file. This function will work for both NYT and The Guardian articles.
def write_articles(article_list):
    for article in article_list:
        #I used a replacement that I found about here http://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Writing_Data_to_a_CSV_With_Python.php
        write_title =  "\"" + article.article_title + "\""
        semicolon_keys = ""
        for keyword in article.keywords:
            semicolon_keys += keyword + ";"
        outstring = '{},{},{},{},{},{},{}'.format(write_title, article.author, article.section, str(article.headline_wordcount()), article.publication, article.url, semicolon_keys)
        article_data.write(outstring)
        article_data.write("\n")
    return print("printed to article_data.csv")

write_articles(nyt_article_insts)
write_articles(guardian_article_insts)

article_data.close()
