import configparser
import feedparser
from datetime import datetime

class Feed:
    def __init__(self,url,fd):
        self.url = url
        self.fd = fd
        self.feed = feedparser.parse(self.url)

    def feed_write(self):
        self.fd.write('<h1>' + self.feed.feed.title + '</h1>\n')
        for self.i in self.feed.entries:
            self.published_time = datetime(self.i.published_parsed[0],self.i.published_parsed[1],self.i.published_parsed[2],self.i.published_parsed[3],self.i.published_parsed[4])
            print(self.published_time)
            if self.published_time >= time:
                self.fd.write('<h2>' + self.i.title + '</h2>')
                self.fd.write(self.i.published + '</br>')
                self.fd.write(self.i.description + '</br>')
        

def initFile():
    '''Creates feed file and writes proper charser meta to it. Returns opened file. '''
    fd = open('feed.html','w')
    fd.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n')
    return fd
    

def openConfig():
    '''Reads time from example.ini and writes new time of fetch to it. Creates new config file if current is empty
    Returns time of the last fetch or current time if there is no config fiel.'''
    config = configparser.ConfigParser()
    curtime = str(datetime.utcnow())
    if config.read('example.ini'):
        time = datetime.strptime(config['Last fetch']['Time'],'%Y-%m-%d %H:%M:%S.%f')
        config['Last fetch']['Time'] = curtime
    else:
        config['Last fetch'] = {}
        config['Last fetch']['Time'] = curtime
        time = datetime.utcnow()
    with open('example.ini', 'w') as configfile:
        config.write(configfile)
    return time

fd = initFile()
time = openConfig()

#print(time)

habr = Feed('http://habrahabr.ru/rss/hubs/',fd)
lor = Feed('http://feeds.feedburner.com/org/LOR',fd)

feeds_list = {habr,lor}
for i in feeds_list:
    i.feed_write()
