import configparser
import feedparser
from datetime import datetime
from smtplib import *
import email
from email.mime.text import MIMEText
import sys
import os


class Feed:
    def __init__(self, url):
        self.url = url
        #self.fd = fd
        self.feed = feedparser.parse(self.url)
        self.flag = False

    def feed_write(self):
        fd.write('<h1>' + self.feed.feed.title + '</h1>\n')
        for self.i in self.feed.entries:
            self.published_time = datetime(self.i.published_parsed[0],
                                           self.i.published_parsed[1],
                                           self.i.published_parsed[2],
                                           self.i.published_parsed[3],
                                           self.i.published_parsed[4])
            print(self.published_time)
            if self.published_time >= config['time']:
                self.flag = True
                fd.write('<h2>' + self.i.title + '</h2>')
                fd.write(self.i.published + '</br>')
                fd.write(self.i.description + '</br>')
        return self.flag


def initFile():
    '''Creates feed file and writes proper charser meta to it.
    Returns opened file. '''
    fd = open('feed.html', 'w')
    fd.write(
        '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">\n')
    return fd


def openConfig():
    '''Reads time from pyfeedaemon.conf and writes new time of fetch to it.
    Config path can be passed as an argument to the script.
    Default path is located at $HOME/.config/pyfeedaemon/pyfeedaemon.conf'''
    if len(sys.argv) != 2:
        config_path = os.environ["HOME"] + "/.config/pyfeedaemon/pyfeedaemon.conf"
    else:
        config_path = sys.argv[1]
    config = configparser.ConfigParser()
    curtime = str(datetime.utcnow())
    conf = {'server': 0, 'login': 0, 'password': 0, 'time': 0, 'feeds': []}
    if config.read(config_path):
        conf['time'] = datetime.strptime(config['Last fetch']['Time'],
                                         '%Y-%m-%d %H:%M:%S.%f')
        config['Last fetch']['Time'] = curtime
        conf['server'] = config['Mail']['Server']
        conf['login'] = config['Mail']['Login']
        conf['password'] = config['Mail']['Password']
        conf['sendto'] = config['Mail']['SendTo']
        for key in config['Feeds']:
            temp = Feed(config['Feeds'][key])
            conf['feeds'].append(temp)
    else:
        print("Config file does not exist!")
        raise SystemExit(1)
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    return conf


def sendEmail():
    msg = email.message.Message()
    fp = open('feed.html', 'r')
    msg = MIMEText(fp.read(), 'html')
    fp.close()
    msg['Subject'] = 'Дайджест новостей ' + datetime.now().strftime("%d %B %Y %H:%M")
    mail = SMTP_SSL(config['server'], 465)
    mail.login(config['login'], config['password'])
    mail.send_message(msg, config['login'],
                      config['sendto'])

fd = initFile()
config = openConfig()

print(config['time'])

for i in config['feeds']:
    flag = i.feed_write()
fd.close()

if flag is True:
    sendEmail()
else:
    print("No mail was sent!")
