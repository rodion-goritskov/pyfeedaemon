#!/bin/sh

case "$(python --version 2>&1)" in
    *" 3.3"*)
        echo "Python version is fine!"
	cp pyfeedaemon.py /usr/bin/
	cp feeds.py /usr/bin/
	cp config.py /usr/bin/
	chmod +x /usr/bin/pyfeedaemon.py
        ;;
    *)
        echo "Your Python version should be >=3.3. Installation aborted!"
        ;;
esac

