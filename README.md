Simple backuping system with **web interfaces** for your sites and related with the sites MySQL DBs.
Coded on Python with Flask and Fabric.

Installation
============
* Requirements
    `pip install -r requirements.txt`

* Deploy as a standard Flask app. For more inforamtion go to http://flask.pocoo.org/docs/deploying/

Config
======
Change `backup.conf` for your needs. After that add cron job for the `fabfile.py` 
on a period of time you need.

Generate secret_key for your app
--------------------------------
    >>> import os
    >>> os.urandom(24)
    '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
Paste the generated secret_key in your `backup.conf` with quotes.


