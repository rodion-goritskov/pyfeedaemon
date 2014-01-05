import configparser
from datetime import datetime
import sys
import os
from feeds import Feed


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
            conf['feeds'].append(config['Feeds'][key])
    else:
        print("Config file does not exist!")
        raise SystemExit(1)
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    return conf
