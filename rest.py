"""KnowledgeMap REST API."""

import falcon
import json

from wikipedia import Wikipedia


class Search:
    """Primary Class for KnowledgeMap."""

    def on_get(self, req, resp, search_term):
        """Handle search requests."""
        w = Wikipedia()

        try:
            resp.body = json.dumps(w.search([search_term]))
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.body = json.dumps({"Error": "Something went wrong, sorry!",
                                    "Exception": e})
            resp.status = falcon.HTTP_500


app = falcon.API()

search = Search()

app.add_route('/search/{search_term}', search)
