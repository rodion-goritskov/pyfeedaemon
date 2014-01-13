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

import configparser
from datetime import datetime
import os


class Config():
    '''Class for operating config file'''
    def __init__(self, config_path):
        '''Object is created with only one parameter - path to the config.'''
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.conf = {'server': 0, 'login': 0, 'password': 0,
                     'time': 0, 'feeds': []}
        if os.path.exists(self.config_path) is False:
            print("Config file " + self.config_path + " doesn't exist!")
            raise SystemExit(1)
        else:
            self.config.read(self.config_path)

    def config_read(self):
        '''Parses config. Returns a parsed configuration object.'''
        self.conf['time'] = datetime.strptime(
            self.config['Last fetch']['Time'], '%Y-%m-%d %H:%M:%S.%f')
        self.conf['server'] = self.config['Mail']['Server']
        self.conf['login'] = self.config['Mail']['Login']
        self.conf['password'] = self.config['Mail']['Password']
        self.conf['sendto'] = self.config['Mail']['SendTo']
        for key in self.config['Feeds']:
            self.conf['feeds'].append(self.config['Feeds'][key])
        return self.conf

    def write_last_fetch(self):
        '''Writes current time as fetch time to config'''
        self.curtime = str(datetime.utcnow())
        self.config['Last fetch']['Time'] = self.curtime
        with open(self.config_path, 'w') as self.configfile:
            self.config.write(self.configfile)

    def new_feed(self, feed_name, feed_address):
        '''method new_feed(feed_name, feed_address).
        Adds new feed with name feed_name and address feed_address to config
        file, if the same feed doesnt exist.'''
        self.feed_name = feed_name
        self.feed_address = feed_address
        self.duplicate = False
        for key in self.config['Feeds']:
            if ((self.config['Feeds'][key] ==
                 self.feed_address) or (key == self.feed_name)):
                self.duplicate = True
        if self.duplicate is False:
            self.config['Feeds'][self.feed_name] = self.feed_address
            with open(self.config_path, 'w') as self.configfile:
                self.config.write(self.configfile)
        else:
            print("Feed already exists!")
