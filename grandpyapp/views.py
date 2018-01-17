from flask import Flask, render_template, request
import json
import grandpyapp.myparser as ps

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
#app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/dialog', methods = ['POST'])
def postJsonHandler():
    msgJson = request.get_json()
    msg = msgJson['dialogContent']
    response = ps.msgProcessor(ps.msgParser(msg))
    responseJson = json.dumps(response)
    return responseJson

#@app.route('/confirm', methods = ['POST'])
#def confirmationHandler():
