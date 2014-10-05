#!/usr/bin/python
# Get those sentiments!

import subprocess
import sys


import urllib
import urllib2
import json

HPAPIkey = "40d526f5-0d9c-4f9a-b288-fc79c181ad77"
sentimentURL = "https://api.idolondemand.com/1/api/sync/detectsentiment/v1"

CalaisAPIkey = "whavuymcpufba7f6q5d7ph2r"
CalaisURL = "http://api.opencalais.com/tag/rs/enrich"

def repeatABunch(urls):
    ts = []
    for i, line in enumerate(urls):
        ts.append(topicsAndSentiments(i, line))
    return ts

def topicsAndSentiments(i, url, verbose=False):
    if verbose:
        print "URL:", url
        print "removing junk from page"
    content = removeBoiler(i, url)
    if verbose:
        print "Content:", content
    t = topics(content)
    s = sentiments(content)
    return t, s 

def resolveReferences(db):
    for elem in db:
        for attrib in db[elem]:
            val = db[elem][attrib]
            if type(val) == unicode:
                if val in db:
                    db[elem][attrib] = db[val]
    return db

def createHierarchy(db):
    newdb = {}
    for elem in db:
        elemType = db[elem].get(u'_type')
        elemGroup = db[elem].get(u'_typeGroup')
        if elemGroup is not None:
            if elemGroup not in newdb:
                newdb[elemGroup] = {}
            if elemType is not None:
                if elemType not in newdb[elemGroup]:
                    newdb[elemGroup][elemType] = {}
                newdb[elemGroup][elemType][elem] = db[elem]
            else:
                newdb[elemGroup][elem] = db[elem]
        else:
            newdb[elem] = db[elem]
    return newdb

def extractRelevance(db):
    termList = []
    simpleDB = createHierarchy(resolveReferences(db)).get(u'entities')
    for group in simpleDB:
        for hash_val in simpleDB[group]:
            topvals = simpleDB[group][hash_val]
            if u'name' in topvals and u'relevance' in topvals:
                tupl = (topvals[u'name'], topvals[u'relevance'])
                termList.append(tupl)
    return termList

def computeSentiment(s, c):
    evaluate = lambda d : d[u'score'] * d[u'normalized_length']
    pos = sum(map(evaluate, s[u'positive']))
    neg = sum(map(evaluate, s[u'negative']))

    l = max(len(c), 1)
    return pos * 50.0 / l , neg * 50.0 / l


def removeBoiler(i, url):
    filepath = "out" + str(i) + ".txt"
    with open(filepath, "w") as f:
        return_code = subprocess.call(['java', 'RemoveBoiler', url], stdout=f)
        if return_code != 0:
            print "boiler removal failed..."
            exit(return_code)
    with open(filepath, "r") as f: 
        return f.read()

# identifier, URL
def sentiments(content, verbose=False):
    if verbose:
        print "running sentiment analysis"
    params = {'apikey' : HPAPIkey, 'text' : content } 
    data = urllib.urlencode(params)

    req = urllib2.Request(sentimentURL, data)
    response = urllib2.urlopen(req)

    s = response.read()
    d = json.loads(s)
    return computeSentiment(d, content)

def topics(content, verbose=False):
    if verbose:
        print "Annotating topics"
    params = { "x-calais-licenseID" :  CalaisAPIkey,
               "content-type" : "TEXT/RAW",
               "outputFormat" : "Application/JSON" } 

    data = urllib.urlencode(params)

    req = urllib2.Request(CalaisURL, content, params)
    response = urllib2.urlopen(req)

    s = response.read()
    d = json.loads(s)
    return extractRelevance(d)

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print topicsAndSentiments(0, arg)
