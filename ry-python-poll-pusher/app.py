from flask import Flask, render_template, request, jsonify, make_response
from dbsetup import create_connection, select_all_items, update_item
from flask_cors import CORS, cross_origin
from pusher import Pusher
import simplejson
#init flask object
#cross origin resource sharing allowed for flask obj
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

    # configure pusher object
pusher = Pusher(
    app_id="1099784",
    key="0ceeb401a51730c17945",
    secret= "2ccca9725a231ccf5eee",
    cluster="us2",
    ssl=True)
#called database
#May NEED to change it
database = "./pythonsqlite.db"
conn = create_connection(database)
c = conn.cursor()
#main method.. defines global variables connection & c
def main():
        global conn, c
#backslash triggers function
@app.route('/')
def index():
        return render_template('index.html')

@app.route('/admin')
def admin():
        return render_template('admin.html')

@app.route('/vote', methods=['POST'])
def vote():
        data = simplejson.loads(request.data)
        update_item(c, [data['member']])
        output = select_all_items(c, [data['member']])
        pusher.trigger(u'poll', u'vote', output)
        return request.data

if __name__ == '__main__':
        main()
        app.run(debug=True)