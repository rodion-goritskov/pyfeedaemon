from datetime import datetime
from smtplib import *
import email
from email.mime.text import MIMEText
import config
from feeds import Feed
import argparse


def initFile():
    '''Creates feed file and writes proper charser meta to it.
    Returns opened file. '''
    fd = open('feed.html', 'w')
    fd.write(
        '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">\n')
    return fd


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

parser = argparse.ArgumentParser()
parser.add_argument("--config")
parser.add_argument("--addfeed")
args = parser.parse_args()
if args.config:
    config_file = config.Config(args.config)
else:
    config_file = config.Config()
if args.addfeed:
    config_file.new_feed("new", args.addfeed)


fd = initFile()
config = config_file.config_read()

print(config['time'])

for i in config['feeds']:
    temp = Feed(i, fd, config['time'])
    flag = temp.feed_write()
fd.close()

config_file.write_last_fetch()

if flag is True:
    sendEmail()
else:
    print("No mail was sent!")
