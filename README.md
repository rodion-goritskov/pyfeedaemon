pyFeedaemon is NOT a daemon for retrieving RSS feeds and sending them to specified e-mail.

All settings are stored in setting file. Default path to settings file is $HOME/.config/pyfeedaemon/pyfeedaemon.conf.
However, you can specify path with --config when running the pyFeedaemon, i.e. pyfeedaemon.py --config [PATH TO CONFIG].

Example config with comments is included.

Also, you can add new feeds into config with --addfeed, i.e. pyfeedaemon.py --addfeed [FEED NAME]=[FEED ADDRESS]
Added feed is stored in config file.

Code of the pyFeedaemon a little bit ugly, but this is my first Python program, so any help is highly appreciated.