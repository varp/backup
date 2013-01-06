Simple backuping system for your sites and related with the sites MySQL DBs.
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

