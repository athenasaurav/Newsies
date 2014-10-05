import rssRead
import sentimentAnalysis
import app.manage

def derp_derp():
    Newsies.rssRead.fetch()
    urlList = []
    with open('urlFile', 'r') as f:
        for line in f:
            urlList.append(line)

    ts = Newsies.sentimentAnalysis.repeatABunch(urlList)
    
    for url, (topics, sents) in zip(urlList, ts):
        Newsies.app.manage.addArticle(url, topics, sents)


