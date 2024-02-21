from flask import Flask
from flask_cors import CORS

from indexer import br, retrieve_exp

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/query/<query>', methods=['GET'])
def resolve_query(query):
    res = br.search(query)
    return retrieve_exp(res).to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)


