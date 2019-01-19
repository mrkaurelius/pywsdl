from flask import Flask # => wsgi itself

app = Flask(__name__)

@app.route('/')
def hello():
	return 'merhaba zalım dunya'
	pass