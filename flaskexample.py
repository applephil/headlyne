from flask import Flask
from flask import render_template
from time import time
app = Flask(__name__)

markers = []
last_updated_time = 0

import headline

@app.route('/')

def earth():
	global markers
	global last_updated_time
	current_time = time()
	if current_time - last_updated_time > 7200:
		markers = headline.get_all_markers()
		last_updated_time = current_time
	return render_template('index.html', markers=markers)

if __name__ == '__main__':
	app.run(debug=True) 