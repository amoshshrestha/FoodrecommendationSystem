from math import ceil
from flask import Flask, render_template, request, url_for

from algoliasearch.search_client import SearchClient
#from api import fetch_poster, fetch_overview, fetch_trailers, fetch_recommend_posters
from api import ALGOLIA_APP_ID, ALGOLIA_API_KEY, ALGOLIA_INDEX_NAME
import requests

# Algolia Search
client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
index = client.init_index(ALGOLIA_INDEX_NAME)

app = Flask(__name__)

# Static location config
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = 'static'
app.secret_key = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/')
def home():
    
    return render_template('home.html' )


@app.route('/foodrecommend')
def foodrecommend():
    diseases = ["AcidReflux", "Anemia",  "FattyLiver", "Gastritis",
                                       "Obesity", "Pancreatitis", "Type1Diabetes", "Urinary-tract",
                                       "Hypertension", "Low Blood Pressure", "Kidney Stone",
                                       "coronary artery disease", "bronchitis", "asthma",
                                       "common cold", "influenza", "corona virus", "diarrhoea", "cholera","Cavities"]
    
    return render_template('foodrecommend.html',diseases=diseases )

@app.route('/foodavoid')
def foodavoid():
    diseases = [
    "AcidReflux",
    "FattyLiver",
    "Gastritis",
    "Obesity",
    "Pancreatitis",
    "Type1Diabetes",
    "Hypertension",
    "Low Blood Pressure",
    "Kidney Stone",
    "coronary artery disease",
    "bronchitis",
    "asthma",
    "common cold",
    "influenza",
    "corona virus",
    "diarrhoea",
    "cholera",
    "Cavities"
]
    
    return render_template('foodavoid.html',diseases=diseases )

# Algolia Search
client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
index = client.init_index(ALGOLIA_INDEX_NAME)

# Search function
@app.route('/category')

def search():
    query = request.args.get('query')
    format = request.args.get('format', 'html')

    if not query:
        if format == 'json':
            return jsonify({'error': 'query parameter is required'})
        else:
            return render_template('search.html', error='query parameter is required')

    results = index.search(query)
    hits = results['hits']

    if format == 'json':
        return jsonify(hits)
    return render_template('search.html', hits=hits, query=query)

if __name__ == '__main__':
    app.run(debug=True)