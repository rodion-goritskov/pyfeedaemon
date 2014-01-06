import configparser
from datetime import datetime
import sys
import os


class Config():
    def __init__(self, config_path=os.environ["HOME"] + "/.config/pyfeedaemon/pyfeedaemon.conf"):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.conf = {'server': 0, 'login': 0, 'password': 0, 'time': 0, 'feeds': []}
        if self.config.read(self.config_path):
            pass
        else:
            print("Config file does not exist!")
            raise SystemExit(1)
                    
    def config_read(self):
        self.conf['time'] = datetime.strptime(self.config['Last fetch']['Time'], '%Y-%m-%d %H:%M:%S.%f')            
        self.conf['server'] = self.config['Mail']['Server']
        self.conf['login'] = self.config['Mail']['Login']
        self.conf['password'] = self.config['Mail']['Password']
        self.conf['sendto'] = self.config['Mail']['SendTo']
        for key in self.config['Feeds']:
            self.conf['feeds'].append(self.config['Feeds'][key])
        return self.conf

    def write_last_fetch(self):
        self.curtime = str(datetime.utcnow())
        self.config['Last fetch']['Time'] = self.curtime
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

    def new_feed(self, feed_name, feed_address):
        self.feed_name = feed_name
        self.feed_address = feed_address
        #if (self.feed_name) & (self.feed_address):
        self.config['Feeds'][self.feed_name] = self.feed_address
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
