from multiprocessing import Pool
from app import manage
import feedparser

# The Guardian, NYTimes, USAToday, WSJ, BBC
# No RSS for opinion: CNN
sources = ["http://feeds.theguardian.com/theguardian/us/commentisfree/rss", 
     "http://rssfeeds.usatoday.com/news-opinion&x=1",
     "http://feeds.bbci.co.uk/news/have_your_say/rss.xml"]

test_srcs = ["http://feeds.bbci.co.uk/news/have_your_say/rss.xml"]

def fetch():
    pool = Pool(processes=1)

    # TODO: implement timeout; re-implement this with threads instead of processes?
    feeds = []
    p = pool.map_async(feedparser.parse, test_srcs,
        callback=(feeds.extend))
    p.wait()
    for key in feeds[0].entries[0].keys():
        print key
   
    items = []
    for feed in feeds:
        for entry in feed.entries:
            items.append(entry["link"])
            manage.write_db(entry)
    
    f = open('urlFile', 'w')
    
    for item in items:
        f.write(item + '\n')

    f.close()

