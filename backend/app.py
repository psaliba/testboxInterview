from flask import Flask

app = Flask(__name__)

@app.route('/submit/')
def submit():

	# This would be a good place to do something with the data you are
	# submitting from the front-end!

	return {'hello': 'world'}

