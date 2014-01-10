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

from datetime import datetime
from smtplib import *
import email
from email.mime.text import MIMEText
import config
from feeds import Feed
import argparse
import os

# Hardcoding default data folder and config name
DATA_FOLDER_PATH = os.environ["HOME"] + "/.config/pyfeedaemon/"
CONFIG_FILE_NAME = "pyfeedaemon.conf"


def initFile():
    '''Creates feed file and writes proper charser meta to it.
    Returns opened file. '''
    fd = open(DATA_FOLDER_PATH + 'feed.html', 'w')
    fd.write(
        '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">\n')
    return fd


def sendEmail():
    '''Sends file feed.html to the email specified
    in configuration file using SMTP server,
    username and password from config file'''
    msg = email.message.Message()
    fp = open(DATA_FOLDER_PATH + 'feed.html', 'r')
    msg = MIMEText(fp.read(), 'html')
    fp.close()
    msg['Subject'] = 'Дайджест новостей ' + datetime.now().strftime("%d %B %Y %H:%M")
    mail = SMTP_SSL(config['server'], 465)
    mail.login(config['login'], config['password'])
    mail.send_message(msg, config['login'],
                      config['sendto'])


if __name__ == '__main__':
    # Parsing command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    parser.add_argument("--addfeed")
    parser.add_argument("--print_log", action='store_true')
    args = parser.parse_args()

    # If config folder doesn't exist - create it!
    if os.path.exists(DATA_FOLDER_PATH) is False:
        if os.makedirs(DATA_FOLDER_PATH) is False:
            print("Failed to create program data folder. Exiting!")
            raise SystemExit()

    # Openin config file, default or specified in argument
    if args.config:
        config_file = config.Config(args.config)
    else:
        config_file = config.Config(DATA_FOLDER_PATH + CONFIG_FILE_NAME)

    if args.print_log:
        print_log = True
    else:
        print_log = False

    if args.addfeed:
        new_feed_list = args.addfeed.replace(" ", "").split("=")
        config_file.new_feed(new_feed_list[0], new_feed_list[1])

    fd = initFile()
    config = config_file.config_read()

    if print_log:
        print(config['time'])

    for i in config['feeds']:
        temp = Feed(i, fd, config['time'], print_log)
        flag = temp.feed_write()
    fd.close()

    config_file.write_last_fetch()

    if flag is True:
        sendEmail()
    else:
        print("No mail was sent!")
