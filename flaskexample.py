#from yourapplication import app as application
from flask import Flask
from flask import render_template
from time import time
app = Flask(__name__)

markers = []
last_updated_time = 0

import headline

@app.route('/')

def hello_world():
    return 'Hello World!'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/phil/')
def xyz():
	return 'Mark and Phil'

@app.route('/earth/')
def earth():
	global markers
	global last_updated_time
	current_time = time()
	if current_time - last_updated_time > 3600:
		markers = headline.get_all_markers()
		last_updated_time = current_time
	return render_template('index.html', markers=markers)


if __name__ == '__main__':
	app.run(debug=True) 