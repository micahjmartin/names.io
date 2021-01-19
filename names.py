import sqlite3
import os
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
  

class Names(object):
    def __init__(self, database):
        # Open the DB
        if not os.path.exists(database):
            raise FileNotFoundError(database)
        self.conn = sqlite3.connect(database)
        self.curr = self.conn.cursor()
        nltk.download('punkt')
        self.stop_words = set(stopwords.words('english'))



    
    def is_first_name(self, name):
        self.curr.execute("SELECT count(name) FROM firstname WHERE name == ? LIMIT 1", (name,))
        res = self.curr.fetchone()
        try:
            return res[0] != 0
        except:
            return False
    
    def is_last_name(self, name):
        self.curr.execute("SELECT count(name) FROM lastname WHERE name == ? LIMIT 1", (name,))
        res = self.curr.fetchone()
        try:
            return res[0] != 0
        except:
            return False
    
    def is_name(self, name):
        if self.is_first_name(name):
            return True
        return self.is_last_name(name)
    
    def get_names(self, data):
        names = []
        tokens = word_tokenize(data)
        for tok in tokens:
            # Stop words arent in the name, move on
            if tok in self.stop_words:
                names = []
                continue
            if names:
                if self.is_name(tok):
                    names.append(tok)
                    continue
                else:
                    if len(names) > 1:
                        yield " ".join(names).title()
                    names = []
                    continue
    
            if self.is_first_name(tok):
                # we got a name, now lets find the last name (up to two characters)
                names.append(tok)
                continue

    def is_name(self, name):
        """Name can be either many names or one"""