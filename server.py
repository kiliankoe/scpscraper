from flask import Flask, jsonify
from scrape import scp

app = Flask(__name__)


@app.route('/scp/<scp_id>')
def get_scp(scp_id):
    scp_dict = scp(scp_id)
    return jsonify(scp_dict)


app.run(debug=True, host='127.0.0.1', port=8080)
