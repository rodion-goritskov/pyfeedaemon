import feedparser
from datetime import datetime


class Feed:
    def __init__(self, url, feed_file, last_time):
        self.url = url
        self.fd = feed_file
        self.feed = feedparser.parse(self.url)
        self.config_time = last_time
        self.flag = False

    def feed_write(self):
        self.fd.write('<h1>' + self.feed.feed.title + '</h1>\n')
        for self.i in self.feed.entries:
            self.published_time = datetime(self.i.published_parsed[0],
                                           self.i.published_parsed[1],
                                           self.i.published_parsed[2],
                                           self.i.published_parsed[3],
                                           self.i.published_parsed[4])
            print(self.published_time)
            if self.published_time >= self.config_time:
                self.flag = True
                self.fd.write('<h2>' + self.i.title + '</h2>')
                self.fd.write(self.i.published + '</br>')
                self.fd.write(self.i.description + '</br>')
        return self.flag
