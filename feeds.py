'''============================================================
* pyFeedaemon - small thing for sending RSS feeds to e-mail
* Copyright (C) 2013,2014 Rodion Goritskov <rodion@goritskov.com>
*
* This file is part of pyFeedaemon.
* pyFeedaemon program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program. If not, see <http://www.gnu.org/licenses/>.
* ============================================================'''

import feedparser
from datetime import datetime


class Feed:
    def __init__(self, url, feed_file, last_time, print_log=False):
        self.url = url
        self.fd = feed_file
        self.feed = feedparser.parse(self.url)
        self.config_time = last_time
        self.print_log = print_log
        self.flag = False

    def feed_write(self):
        self.fd.write('<h1>' + self.feed.feed.title + '</h1>\n')
        for self.i in self.feed.entries:
            self.published_time = datetime(self.i.published_parsed[0],
                                           self.i.published_parsed[1],
                                           self.i.published_parsed[2],
                                           self.i.published_parsed[3],
                                           self.i.published_parsed[4])
            if self.print_log is True:
                print(self.published_time)
            if self.published_time >= self.config_time:
                self.flag = True
                self.fd.write('<h2>' + self.i.title + '</h2>')
                self.fd.write(self.i.published + '</br>')
                self.fd.write(self.i.description + '</br>')
        return self.flag
