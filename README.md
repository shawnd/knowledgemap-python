# Knowledge Map

REST API which uses Wikipedia as a datasource, extracts all links from article, and returns the top n number of words.

## Usage
* `pip install virtualenv`
* `virtualenv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`
* `gunicorn rest:app`

Once your gunicorn server is running (default: http://127.0.0.1:8000) make a request to the search endpoint.
ie: `GET http://127.0.0.1:8000/search/nhl|elon%20musk|taco%20bell`