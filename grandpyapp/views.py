from flask import Flask, render_template, request

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
#app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/dialog', methods = ['POST'])
def postJsonHandler():
    print (request.is_json)
    content = request.get_json()
    print (content['dialContent'])
    return content['dialContent']
