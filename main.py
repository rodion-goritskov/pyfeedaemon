import configparser
import feedparser
from datetime import datetime
from smtplib import *
import email
from email.mime.text import MIMEText


class Feed:
    def __init__(self, url, fd):
        self.url = url
        self.fd = fd
        self.feed = feedparser.parse(self.url)
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
            if self.published_time >= config['time']:
                self.flag = True
                self.fd.write('<h2>' + self.i.title + '</h2>')
                self.fd.write(self.i.published + '</br>')
                self.fd.write(self.i.description + '</br>')
        return self.flag


def initFile():
    '''Creates feed file and writes proper charser meta to it.
    Returns opened file. '''
    fd = open('feed.html', 'w')
    fd.write(
        '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">\n')
    return fd


def openConfig():
    '''Reads time from example.ini and writes new time of fetch to it.
    Creates new config file if current is empty
    Returns time of the last fetch
    or current time if there is no config file.'''

    config = configparser.ConfigParser()
    curtime = str(datetime.utcnow())
    conf = {'server': 0, 'login': 0, 'password': 0, 'time': 0}
    if config.read('example.ini'):
        conf['time'] = datetime.strptime(config['Last fetch']['Time'],
                                         '%Y-%m-%d %H:%M:%S.%f')
        config['Last fetch']['Time'] = curtime
        conf['server'] = config['Mail']['Server']
        conf['login'] = config['Mail']['Login']
        conf['password'] = config['Mail']['Password']
    else:
        config['Last fetch'] = {}
        config['Last fetch']['Time'] = curtime
        conf['time'] = datetime.utcnow()
    with open('example.ini', 'w') as configfile:
        config.write(configfile)
    return conf


def sendEmail():
    msg = email.message.Message()
    fp = open('feed.html', 'r')
    msg = MIMEText(fp.read(), 'html')
    fp.close
    msg['Subject'] = 'Дайджест новостей ' + datetime.now().strftime("%d %B %Y %H:%M")
    mail = SMTP_SSL(config['server'], 465)
    mail.login(config['login'], config['password'])
    mail.send_message(msg, 'rodion.goritskov@gmail.com',
                      'rodion@goritskov.com')


fd = initFile()
config = openConfig()

print(config['time'])

habr = Feed('http://habrahabr.ru/rss/hubs/', fd)
lor = Feed('http://feeds.feedburner.com/org/LOR', fd)

feeds_list = {habr, lor}
for i in feeds_list:
    flag = i.feed_write()
fd.close()

if flag is True:
    sendEmail()
