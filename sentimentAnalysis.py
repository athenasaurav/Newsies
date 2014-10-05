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

def topicsAndSentiments(i, url, verbose=False):
    print "URL:", url
    if verbose:
        print "removing junk from page"
    content = removeBoiler(i, url)
    print "Content:", content
    t = topics(content)
    s = sentiments(content)
    return t, s

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
    print d

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
    print d

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        topicsAndSentiments(0, arg)
