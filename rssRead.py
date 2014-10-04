from multiprocessing import Pool
import feedparser

# The Guardian, NYTimes, USAToday, WSJ, BBC
# No RSS for opinion: CNN
sources = ["http://feeds.theguardian.com/theguardian/us/commentisfree/rss", 
     "http://topics.nytimes.com/top/opinion/editorialsandoped/editorials/index.html?rss=1",
     "http://rssfeeds.usatoday.com/news-opinion&x=1",
     "http://online.wsj.com/xml/rss/3_7041.xml",
     "http://feeds.bbci.co.uk/news/have_your_say/rss.xml"]

test_srcs = ["http://feeds.bbci.co.uk/news/have_your_say/rss.xml"]

def fetch():
    pool = Pool(processes=1)

    # TODO: implement timeout; re-implement this with threads instead of processes?
    feeds = []
    p = pool.map_async(feedparser.parse, sources,
        callback=(feeds.extend))
    p.wait()
   
    items = []
    for feed in feeds:
        for entry in feed.entries:
            items.append(entry["link"])
    
    return items
