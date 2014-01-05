import configparser
from datetime import datetime
import sys
import os


class Config():
    def __init__(self):
        if len(sys.argv) != 2:
            self.config_path = os.environ["HOME"] + "/.config/pyfeedaemon/pyfeedaemon.conf"
            if sys.argv[1] == "addfeed" & sys.argv[2] & sys.argv[3]:
                self.new_feed_name = sys.argv[2]
                self.new_feed_address = sys.argv[3]
        else:
            self.config_path = sys.argv[1]
        
        self.config = configparser.ConfigParser()
        self.conf = {'server': 0, 'login': 0, 'password': 0, 'time': 0, 'feeds': []}
        if self.config.read(self.config_path):
            self.conf['time'] = datetime.strptime(self.config['Last fetch']['Time'], '%Y-%m-%d %H:%M:%S.%f')            
            self.conf['server'] = self.config['Mail']['Server']
            self.conf['login'] = self.config['Mail']['Login']
            self.conf['password'] = self.config['Mail']['Password']
            self.conf['sendto'] = self.config['Mail']['SendTo']
            if self.new_feed_name * self.new_feed_address:
                self.config['Feeds'][self.new_feed_name] = self.new_feed_address
                with open(self.config_path, 'w') as configfile:
                    self.config.write(configfile)
            for key in self.config['Feeds']:
                self.conf['feeds'].append(self.config['Feeds'][key])
        else:
            print("Config file does not exist!")
            raise SystemExit(1)
                    
    def config_read(self):
        return self.conf

    def write_last_fetch(self):
        self.curtime = str(datetime.utcnow())
        self.config['Last fetch']['Time'] = self.curtime
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
