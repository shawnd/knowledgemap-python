"""KnowledgeMap search class."""

import json
import requests
import re

from wordcount import WordCount


class Wikipedia:
    """Primary Class for KnowledgeMap."""

    LEFT_BRACKET = "[["
    RIGHT_BRACKET = "]]"
    TOP_WORD_COUNT = 5

    def search(self, terms):
        """Search Wikipedia for the list terms."""
        if len(terms) <= 0:
            return {}

        response = json.loads(requests.get(
            'https://en.wikipedia.org/w/api.php?format=json&action=query' +
            '&titles=' + self._join_search_terms(terms) +
            '&prop=revisions&rvprop=content').text)

        # response['query']['pages']

        return self._handle_response(response)

    def _join_search_terms(self, terms):
        """Join search terms with '|' character for Wikipedia API."""
        joined = ""
        for term in terms:
            joined = joined + term + "|"
        return joined[:-1]

    def _get_top_words(self, content, n):
        """Return top n links from content."""
        left = [m.start() for m in re.finditer(
                re.escape(self.LEFT_BRACKET), content)]
        right = [m.start() for m in re.finditer(
                 re.escape(self.RIGHT_BRACKET), content)]

        wc = WordCount()
        for i in range(0, len(left)):
            wc.add(content[left[i] + len(self.LEFT_BRACKET):right[i]])
        return [key[0] for key in wc.top(n)]

    def _handle_response(self, response):
        """Handle the response from Wikipedia API."""
        # Check if search term is redirected to another article
        redirects = []

        top_words = {}

        pages = response['query']['pages']
        for page in pages:
            title = pages[page]['title']
            if 'missing' in pages[page]:
                top_words[title] = []
            else:
                cp = pages[page]['revisions'][0]['*']

                if cp.lower().startswith("#redirect"):
                    left = cp.find(self.LEFT_BRACKET) + len(self.LEFT_BRACKET)
                    right = cp.find(self.RIGHT_BRACKET)
                    redirects.append(cp[left:right])
                else:
                    # Count links to other articles in Wiki text
                    top_words[title] = self._get_top_words(
                        cp, self.TOP_WORD_COUNT)

        return dict(list(top_words.items()) +
                    list(self.search(redirects).items()))

# Usage Examples
# km = Wikipedia()
# print(km.search(["nhl", "Elon Musk"]))
# print(km.search(["asdasjioudasjois"]))
