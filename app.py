from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from markupsafe import escape
from core.Setup import Setup
import sys
sys.path.insert(0, "..")

# Flask imports


# Create server
app = Flask(__name__, static_url_path='/static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

setup = Setup()

# -----------------
# --- API REST ---
# -----------------
"""
/conversation/sessions
Returns a list of all conversation sessions
"""


@app.route('/conversations', methods=['POST', 'GET'])
@cross_origin()
def getSessions():
    sessions = setup.database.get_all_conversation_sessions()

    if not sessions:
        return []
    else:
        return sessions


"""
/conversation/:id
Returns a conversation
"""


@app.route('/conversation/', methods=['POST', 'GET'])
@cross_origin()
def getConversation():
    conversation_id = request.args.get('conversation_id')
    conversation = setup.database.get_conversation(conversation_id)
    return conversation


"""
/firstrun
Returns a list of all conversation sessions
"""


@app.route('/firstrun', methods=['POST', 'GET'])
@cross_origin()
def firstRun():
    first_run = setup.is_first_run()
    if first_run:
        return '{"first_run": true}'
    else:
        return '{"first_run": false}'


"""
/checkpath/:path
Checks rasa installation paths
"""


@app.route('/checkpath/', methods=['POST', 'GET'])
@cross_origin()
def checkPath():
    path = request.args.get('path')
    rasa_installation = setup.check_installation_path(path)

    if rasa_installation:
        return '{"install": true}'
    else:
        return '{"install": false}'


"""
/install
Checks rasa installation paths
"""


@app.route('/install/', methods=['POST', 'GET'])
@cross_origin()
def install():
    password = request.args.get('password')
    install_result = setup.install_conversa(password)

    if install_result:
        return '{"install": true}'
    else:
        return '{"install": false}'


"""
/login/:password
Returns auth token
"""


@app.route('/login', methods=['POST', 'GET'])
@cross_origin()
def auth():
    password = request.args.get('password')

    is_valid = setup.database.login(password)

    if len(is_valid) <= 0:
        return '{"auth": false}'
    else:
        #auth_token = "Zxc324ghjas"
        return '{"auth": true}'
