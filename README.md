pyFeedaemon is NOT a daemon for retrieving RSS feeds and sending them to specified e-mail.

Requirements
======================
pyFeedaemon is written on Python.
Required version is >=3.3. Feedparser and configparser modules are 
necessary and could be installed with pip. 

Settings
=============
All settings are stored in settings file. Default path to settings file 
is $HOME/.config/pyfeedaemon/pyfeedaemon.conf.
However, you can specify path with --config when running the pyFeedaemon, i.e. pyfeedaemon.py --config [PATH TO CONFIG].

Example config
================
Example config with comments is included.

Adding feeds
================
Also, you can add new feeds into config with --addfeed, i.e. pyfeedaemon.py --addfeed [FEED NAME]=[FEED ADDRESS]
Added feed is stored in config file.

Your code is really bad, dude!
=====================
Code of the pyFeedaemon a little bit ugly, but this is my first Python program, so any help is highly appreciated.
