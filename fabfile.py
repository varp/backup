from __future__ import with_statement
import ConfigParser
import os
import os.path
import datetime

from fabric.api import *


env['tars'] = []
env['dumps'] = []





cfg = ConfigParser.ConfigParser()
try:
    cfg.read('backup.conf')
except IOError:
    print("Cannot read config file. Aborting.")
    exit(1)


def _files():
    files = []; files.extend(env.dumps); files.extend(env.tars)
    return files


def backup_folders():
    www_root = cfg.get('general','www_root', None)
    folders = cfg.get('folder', 'folders', None)
    if not folders or not www_root:
        exit(1)
    for f in folders.split(","):
        with cd("/tmp"):
            tar_name = "%s.tar.gz" %  f
            run("tar czvf %s %s" % (tar_name, os.path.join(www_root, f)))
            env.tars.append(tar_name)


def dump_dbs():
    dbs = cfg.get('db', 'dbs', None)
    dbuser = cfg.get('db', 'user', None)
    passw = cfg.get('db', 'password', None)
    if not dbs or not dbuser or not passw:
        exit(1)
    for d in dbs.split(","):
        with cd("/tmp"):
            dump_cmd = "mysqldump --add-drop-database --add-drop-table --comments --user=%s --password=%s %s > %s.dump.sql" % (dbuser, passw, d, d)
            run(dump_cmd)
            env.dumps.append("%s.dump.sql" % d)


def collect():
    with cd("/tmp"):
        files = _files()
        tar_name = "%s.tar.gz" % datetime.date.today().strftime("%d%m%Y")
        run("tar czvf %s %s" % (tar_name, " ".join([f for f in files])))
        env.tars.append(tar_name)


def retrive():
    download_dir = cfg.get('general', 'download_dir', None)
    if not download_dir:
        exit(1)

    if not os.path.exists(download_dir):
        print("general.download_dir does not exists")
        exit(1)

    with cd("/tmp"):
        arch_name = "%s.tar.gz" % datetime.date.today().strftime("%d%m%Y")
        get(arch_name, os.path.join(download_dir, arch_name))


def clean():
    files = _files()
    with cd("/tmp"):
        run("rm -vf %s" % " ".join([f for f in files]))


def backup():
    backup_folders()
    dump_dbs()
    collect()
    retrive()
    clean()
