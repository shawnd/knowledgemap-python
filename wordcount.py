"""WordCount class, used to count number of occurences of a particular word."""
from operator import itemgetter


class WordCount:
    """Counts Word Occurences."""

    def __init__(self):
        """Constructor."""
        self.words = {}

    def add(self, word):
        """Add a word to the dict."""
        if word in self.words:
            self.words[word] = self.words[word] + 1
        else:
            self.words[word] = 1

    def count(self):
        """Print all counts."""
        for word in self.words:
            print(word, self.words[word])

    def top(self, n):
        """Get top n words."""
        return sorted(self.words.items(),
                      key=itemgetter(1), reverse=True)[0:n]
