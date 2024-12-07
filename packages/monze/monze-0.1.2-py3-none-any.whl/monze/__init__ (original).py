from flask import Flask, redirect, request, render_template
import logging
import sys
import os
import webbrowser
import tkinter as tk
from tkinter import filedialog
import pathlib
import requests
import psutil
from colorama import Fore, Style

version = "0.1.0"
devdev = True

# for stopping process via prompt
try:
	if sys.argv[1] in ["-q", "-Q", "--q", "--Q"]:
		for proc in psutil.process_iter():
			if "Python" in proc.name():
				psutil.Process(proc.pid).terminate()
	if sys.argv[1] in ["-v", "-V", "--v", "--V"]:
		sys.exit(f"Monze version: {version}")
except:
	pass

# for checking correct version

githuburl = "https://raw.githubusercontent.com/jeex/jeex_public/refs/heads/main/monze_version.txt"
r = requests.get(githuburl)
if r.status_code == 200:
	monze_version = r.content.decode("utf-8").strip()
	if monze_version > version:
		sys.exit(f"{Style.BRIGHT}{Fore.RED}This version is {version}. Upgrade with newer version {monze_version}: pip install monze --upgrade{Style.RESET_ALL}")

monzepad = str(pathlib.Path(__file__).parent.resolve())
sys.path.insert(0, monzepad)

from general import (
	Casting,
	Timetools,
	Mainroad
)
from singletons import (
	Sysls,
	UserSettings,
)

# check if settings and onedrive is known
# makes new settings file with onedrive path in it
odpath = Mainroad.get_onedrive_path()
while odpath is None:
	root = tk.Tk()
	root.withdraw()
	odpath = filedialog.askdirectory(title='Open OneDrive dir _BUTTERFLY')
	print("OD PATH", odpath, type(odpath))
	if odpath is None :  # cancel
		# sys.exit_message(')
		sys.exit(f'{Style.BRIGHT}{Fore.RED}No Open OneDrive dir _BUTTERFLY given.{Style.RESET_ALL}')
	if odpath.strip() == '':
		sys.exit(f'{Style.BRIGHT}{Fore.RED}No Open OneDrive dir _BUTTERFLY given.{Style.RESET_ALL}')
	if not odpath.endswith('_BUTTERFLY'):
		sys.exit(f'{Style.BRIGHT}{Fore.RED}No Open OneDrive dir _BUTTERFLY given.{Style.RESET_ALL}')

	# correct path, test it, EXIT if wrong
	Mainroad.force_access('onedrive', odpath)
	if not os.path.isdir(odpath):
		odpath = None
	# make new settings file
	Mainroad.set_new_props(odpath)
	break

app = Flask(__name__, template_folder='templates', static_folder='static', root_path=monzepad)
app.config['FLASK_DEBUG'] = app.config['DEBUG'] = devdev
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'nq023489cnJGH#F!'
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'cookieboogle'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['PERMANENT_SESSION_LIFETIME'] = 24 * 60 * 60
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_DOMAIN'] = None
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
app.config['initialized'] = False
app.config['version'] = version

app.url_map.strict_slashes = False
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# ============= JINJA FILTERS =============
@app.template_filter('gradecss')
def gradecss(grade):
	grade = Casting.int_(grade, default=0)
	if grade >= 55:
		return 'grade-passed'
	elif grade >= 10:
		return 'grade-failed'
	return 'grade-not'

@app.template_filter('filtername')
def filtername(name):
	fnames = {
		'registratie': 'register',
		'studenten': 'students',
		'beoordelen': 'grading',
		'alumni': 'alumni',
		'niet': 'not',
		'noshow': 'noshow',
		'alle': 'all'
	}
	if name in fnames.keys():
		return fnames[name]
	return name

@app.template_filter('gender')
def gender(name):
	if name.lower() in ['m']:
		return '&#9794;'
	elif name.lower() in ['v', 'f']:
		return '&#9792;'
	else:
		return '&#9893;'

@app.template_filter('initials')
def initials(name):
	name = name.split(' ')
	eruit = ''
	for n in name:
		eruit = f"{eruit}{n.upper()}"
	return eruit

@app.template_filter('circ')
def circular_color(val):
	val = Casting.int_(val, 0)
	try:
		sysls = Sysls()
		cees = sysls.get_sysl('s_circular')
		return cees[val]['color']
	except:
		return '#eeeeee'

@app.template_filter('nonone')
def nonone(s):
	if s is None:
		return ''
	elif s in ['None', 'none']:
		return ''
	else:
		return s

from urllib.parse import quote
@app.template_filter('urlsafe')
def urlsafe(s):
	try:
		return quote(str(s))
	except:
		return s

@app.template_filter('nbsp')
def nbsp(s):
	try:
		return s.replace(' ', '&nbsp;')
	except:
		return s

@app.template_filter('vier')
def vier(i):
	try:
		return f'{i:04d}'
	except:
		return i

@app.template_filter('date')
def asdate(i):
	try:
		if i < 1:
			return ''
		return Timetools.ts_2_td(i, rev=True, withtime=False)
	except:
		return i

@app.template_filter('datetime')
def asdatetime(i):
	try:
		if i < 1:
			return ''
		return Timetools.ts_2_td(i, rev=True, withtime=True)
	except:
		return i

@app.template_filter('datetimelocal')
def asdatetime(i):
	try:
		if i < 1:
			return ''
		return Timetools.ts_2_td(i, rev=True, local=True)
	except:
		return i

@app.before_request
def before_request():
	# check if mainroad is complete,
	# if not goto login page
	rp = request.full_path

	if not '/login' in rp:
		if not Mainroad.test_settings():
			return redirect("/login")

	if '/static/' in rp or '/favicon.ico' in rp or '/generate/' in rp:
		return
	'''
	jus = UserSettings()

	# print('Before request', request.path)
	# handling the first request, restarting where we left of
	rp = rp.rstrip('?')
	rp = rp.rstrip('/')

	if jus.is_new():
		# after startup of butterfly, go to last url
		jus._started = False
		jus.set_prop('prev_url', '')
		# get the previouw url and go there (so it is current as well)
		lasturl = jus.get_prop('last_url', default='/home')
		if lasturl in ['', '/', '/home']:
			return redirect('/home')
		else:
			jus.set_prop('prev_url', '')
			return redirect(lasturl)
	else:
		# don't store paths with args
		if len(request.args) > 0:
			pass
		elif len(request.form) > 0:
			pass
		else:
			lasturl = jus.get_prop('last_url', default='')
			if lasturl == rp:
				pass
			elif lasturl in ['', '/', '/home']:
				jus.set_prop('prev_url', '')
			else:
				jus.set_prop('prev_url', lasturl)
			# remember the current url
			jus.set_prop('last_url', rp)
	'''

@app.after_request
def add_header(res):
	res.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
	res.headers["Pragma"] = "no-cache"
	res.headers["Expires"] = "0"
	res.headers['X-Content-Type-Options'] = ''
	res.headers['Access-Control-Allow-Origin'] = '*'
	res.headers['Access-Control-Allow-Methods'] = 'get, post'
	res.cache_control.public = True
	res.cache_control.max_age = 0
	return res


@app.get('/')
def index():
	return redirect('/home')

@app.get('/login')
def login():
	return render_template(
		'login.html',
		ofpath=odpath,
	)

@app.post("/login")
def index_post():
	if not "password" in request.form:
		return redirect("/login")

	password = Casting.str_(request.form["password"], default="")
	user = Mainroad.login(password)
	if user is None:
		return redirect("/login")

	# now check if same user as in usersettings
	jus = UserSettings()
	props = jus.get_props()
	props["alias"] = user["alias"]
	props["password"] = user["password"]
	props["magda"] = user["magda"]
	jus.set_props(props)
	return redirect("/home")

@app.get("/logoff")
def logoff():
	jus = UserSettings()
	jus.logoff()
	return redirect("/login")

from home import ep_home
app.register_blueprint(ep_home)

from studenten import ep_studenten
app.register_blueprint(ep_studenten)

from groepen import ep_groepen
app.register_blueprint(ep_groepen)

from views import ep_views
app.register_blueprint(ep_views)

from editviews import ep_editviews
app.register_blueprint(ep_editviews)

# from endpoint.hunts import ep_hunts
# app.register_blueprint(ep_hunts)

from emails import ep_email
app.register_blueprint(ep_email)

from beheer import ep_beheer
app.register_blueprint(ep_beheer)

from website import ep_website
app.register_blueprint(ep_website)

if not app.config['DEBUG']:
	@app.errorhandler(Exception)
	def handle_error(e):
		Mainroad.loglog(f"error {e}")
		Mainroad.loglog(f"\t{request.full_path}")
		return redirect('/home')

def run():
	if not app.config['initialized']:
		startup = os.path.join(monzepad, "startup.html")
		app.config['initialized'] = True
		if not app.config['DEBUG']:
			webbrowser.open_new(f"file://{startup}")
		print(f"Served cold on http://127.0.0.1:5000/, version {app.config['version']}")

	app.run(port=5000, debug=app.config['DEBUG'], use_reloader=False)

if __name__ == '__main__':
	run()