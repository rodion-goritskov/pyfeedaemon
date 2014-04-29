PyFeedaemon
===================
pyFeedaemon is NOT a daemon for retrieving RSS feeds and sending them to specified e-mail.

Requirements
-----------------
pyFeedaemon is written on Python.

Required version is >=3.3. Feedparser and configparser modules are 
necessary and could be installed with pip. 

Setup
-----------------
Execute setup.sh script under root. It will put all *.py files into /usr/bin and make pyfeedaemon.py executable.

Before the first start of the script you should edit the configuration file according to your needs and put it either in default path or specify desired path (see "Settings" section below).

Now you can start pyfeedaemon with executing pyfeedaemon.py in your terminal emulator or command run dialog.

Or add pyfeedaemon to crontab.

Or something else (:

Settings
----------------
All settings are stored in settings file. 

Default path to the settings file 
is $HOME/.config/pyfeedaemon/pyfeedaemon.conf.

However, you can specify path with --config when running the pyFeedaemon, i.e. pyfeedaemon.py --config [PATH TO CONFIG].

You can switch on printing timestamps into console by starting pyfeedaemon with --print_log.

Example config
---------------
Example config with comments is included.

Adding feeds
---------------
Also, you can add new feeds into config with --addfeed, i.e. pyfeedaemon.py --addfeed [FEED NAME]=[FEED ADDRESS]

Added feed is stored in config file.

Your code is really bad, dude!
--------------------
Code of the pyFeedaemon a little bit ugly, but this is my first Python program, so any help is highly appreciated.
