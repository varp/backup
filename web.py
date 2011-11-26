import os
import os.path
import re
import ConfigParser
from flask import (Flask, request, redirect, url_for, send_from_directory,
                    render_template, session)
from werkzeug import secure_filename


cfg = ConfigParser.ConfigParser()
try:
    cfg.read(os.path.join("backup.conf")
except IOError:
    print("Cannot read config file. Aborting.")
    exit(1)    


PASSWORD = cfg.get('web', 'password', None)
DOWNLOAD_FOLDER = cfg.get('general', 'download_dir', None)

if not DOWNLOAD_FOLDER:
    print("Application error! Download not found in config")
    exit(1)


app = Flask(__name__)
app.config.from_object(__name__)
#app.use_x_sendfile = True
app.secret_key = "(?\x97\xf7z`;'\x02\xdc\x0fB\x19s\xd7 \xdaQ\xc5<y\x7fGt"

class Backup(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return os.path.join(DOWNLOAD_FOLDER, self._name)
    
    @property
    def size(self):
        return os.path.getsize(os.path.join(DOWNLOAD_FOLDER, self._name)) / 1024


def _get_files():
    files = os.listdir(DOWNLOAD_FOLDER)
    files = [f for f in files if re.match('\d+\.tar\.gz', f)]

    backups = []
    for f in files:
        backups.append(Backup(f)) 
    backups.sort(cmp = lambda x, y: cmp(x.name.lower(), y.name.lower()), reverse=True)  

    return backups


@app.route('/login', methods=['GET', 'POST'])
def login(password=None):
    error = None
    if request.method == 'POST':
        if request.form['password'] == app.config['PASSWORD']:
            session['logged_in'] = True
            return redirect(url_for("home"))
        else:
            error = "Inavalid password!"
            return render_template("login.html", error=error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['logged_in']
    return redirect(url_for('login'))


@app.route("/", methods=['GET'])
def home():
    if not session.get('logged_in', None):
        return redirect(url_for("login"))
    files = _get_files()
    return render_template('backups.html', files=files)


@app.route("/backup/<filename>", methods=['GET'])
def send(filename):
    if not session.get('logged_in', None):
        return redirect(url_for('login'))
    
    backups = _get_files() and backups = [b.name for b in backups]
    if filename in backups:
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)
    else:
        return "Application Error"


if __name__ == '__main__':
    app.run(debug=True)
