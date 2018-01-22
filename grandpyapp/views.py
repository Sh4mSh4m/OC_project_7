from flask import Flask, render_template, request
import json
import grandpyapp.myparser as ps
import grandpyapp.myrequestapi as rq

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
# app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/dialog', methods = ['POST'])
def postJsonHandler():
    msgJson = request.get_json()
    # retrieves the user input
    msg = msgJson['dialogContent']
    # Parse and treats user input
    msgResponse = ps.msgProcessor(ps.msgParser(msg))
    # Cleans up and format the keyword to match GMaps API request from client
    tmpKeyWord = msgResponse['keyWord']
    msgResponse['keyWord'] = "%20".join(tmpKeyWord.split())
    # JSON response formatting before sending to the client
    if msgResponse['keyWord'] != '':
        msgResponse['response'] = rq.getJsonApiWiki(msgResponse['keyWord'])
        if msgResponse['response'] != '':
            msgResponse['complement'] = "D'ailleurs, savais-tu que "
            msgResponse['complement'] += msgResponse['response']
        else:
            msgResponse['complement'] = "Désolé je n'ai rien trouvé"
    responseJson = json.dumps(msgResponse)
    return responseJson
