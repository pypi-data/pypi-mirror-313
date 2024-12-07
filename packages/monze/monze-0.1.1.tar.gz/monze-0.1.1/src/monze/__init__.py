import time

from flask import Flask, redirect, request, render_template
import logging
import sys
import os
import webbrowser
# import tkinter as tk
# from tkinter import filedialog, simpledialog
import pathlib
import requests
from colorama import Fore, Style, Back

from general import (
	Casting,
	Timetools,
	Mainroad
)

version = "0.1.1"
devdev = False

# for stopping process via prompt
print(sys.argv)
if '--version' in sys.argv:
	sys.exit(f"Monze version: {version}")
if '--logoff' in sys.argv:
	Mainroad.delete_settings()
	sys.exit(f"User settings deleted. Restart server")
if '--logging' in sys.argv:
	Mainroad.logging = True

# for checking correct version

githuburl = "https://raw.githubusercontent.com/jeex/jeex_public/refs/heads/main/monze_version.txt"
r = requests.get(githuburl)
if r.status_code == 200:
	monze_version = r.content.decode("utf-8").strip()
	if monze_version > version:
		sys.exit(f"{Style.BRIGHT}{Fore.RED}This version is {version}. Upgrade with newer version {monze_version}: pip install monze --upgrade{Style.RESET_ALL}")

monzepad = str(pathlib.Path(__file__).parent.resolve())
if not monzepad in sys.path:
	sys.path.insert(0, monzepad)

# check if settings and onedrive is known
# makes new settings file with onedrive path in it
Mainroad.version = version
odpath = Mainroad.get_onedrive_path(firstrun=True)
while odpath is None:
	print(f"{Back.WHITE}{Fore.BLUE}{Style.BRIGHT} You have to assign the _BUTTERFLY folder. Return = Cancel. {Style.RESET_ALL}")
	# root = tk.Tk()
	# root.withdraw()
	# odpath = filedialog.askdirectory(title='Open OneDrive dir _BUTTERFLY')
	odpath = input(f"{Back.WHITE}{Fore.BLUE}{Style.BRIGHT} Path: {Style.RESET_ALL}").strip()
	# filtering out Onedrive path stuff
	odpath = odpath.replace(r"\ -", r" -").replace(r"-\ ", r"- ")
	if odpath is None:
		sys.exit(f'{Back.WHITE}{Style.BRIGHT}{Fore.GREEN} Exit with Cancel. {Style.RESET_ALL}')
	if len(odpath) == 0:  # cancel
		sys.exit(f'{Back.WHITE}{Style.BRIGHT}{Fore.GREEN} Exit with Cancel. {Style.RESET_ALL}')

	if odpath.strip() == '':
		print(f'{Back.WHITE}{Style.BRIGHT}{Fore.RED} This is an empty path [empty]. {Style.RESET_ALL}')
		odpath = None

	if not odpath.endswith('_BUTTERFLY'):
		print(f'{Back.WHITE}{Style.BRIGHT}{Fore.RED} This path {odpath} is not a working path to _BUTTERFLY [_BUTTERFLY]. {Style.RESET_ALL}')
		odpath = None
	# correct path, test it, EXIT if wrong
	# Mainroad.force_access('onedrive', odpath)
	if not odpath is None:
		if not os.path.isdir(odpath):
			print(f'{Back.WHITE}{Style.BRIGHT}{Fore.RED} This is path {odpath} not a working path to _BUTTERFLY [isdir]. {Style.RESET_ALL}')
			odpath = None

	if not odpath is None:
		print(f"{Back.WHITE}{Fore.GREEN}{odpath} is OK. {Style.RESET_ALL}")

# now we have a proper odpath.
while not Mainroad.test_settings():
	# remove settings file because it contains errors
	Mainroad.delete_settings()
	# start new
	print(f"{Back.WHITE}{Fore.BLUE}{Style.BRIGHT} You have to login. Return == Cancel. {Style.RESET_ALL}")
	# root = tk.Tk()
	# root.withdraw()
	# pw = simpledialog.askstring("Input", "Enter your password")
	pw = input(f"{Back.WHITE}{Fore.BLUE}{Style.BRIGHT} Password: {Style.RESET_ALL}")
	if pw is None:  # cancel
		sys.exit(f'{Back.WHITE}{Style.BRIGHT}{Fore.GREEN} Exit with Cancel. {Style.RESET_ALL}')
	if len(pw) == 0:  # cancel
		sys.exit(f'{Back.WHITE}{Style.BRIGHT}{Fore.GREEN} Exit with Cancel. {Style.RESET_ALL}')

	pw = pw.strip()
	user = Mainroad.try_to_login(pw, odpath)
	if user is None:
		print(f"{Back.WHITE}{Fore.RED}{Style.BRIGHT} No valid login: {pw}. {Style.RESET_ALL}")
		continue
	# set usersettings in user's pc
	newuser = Mainroad.get_empty_settings()
	newuser["onedrive"] = odpath
	newuser["magda"] = user["magda"]
	newuser["alias"] = user["alias"]
	newuser["password"] = pw
	newuser["version"] = Mainroad.version,
	newuser["logging"] = False

	# log user in in sysls
	Mainroad.login(newuser)
	if Mainroad.test_settings():
		print(f"{Back.WHITE}{Fore.BLUE}{Style.BRIGHT} Login OK. {Style.RESET_ALL}", flush=True)
		break
	else:
		print(f"{Back.WHITE}{Fore.RED}{Style.BRIGHT} Login Failed. {Style.RESET_ALL}", flush=True)

from singletons import (
	Sysls,
	UserSettings,
)

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
	if '/static/' in rp or '/favicon.ico' in rp or '/generate/' in rp:
		return

	jus = UserSettings()
	# print('Before request', request.path)
	# handling the first request, restarting where we left of
	rp = rp.rstrip('?')
	rp = rp.rstrip('/')

	if jus.is_new():
		# after startup of butterfly, go to last url
		jus.set_prop('isnew', False)
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
		print(f"Butterfly is served on http://127.0.0.1:5000/, version {app.config['version']}")

	app.run(port=5000, debug=app.config['DEBUG'], use_reloader=False)

if __name__ == '__main__':
	run()