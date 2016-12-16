from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()
#        conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")
#        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#        cur = conn.cursor()
#        cur.execute("DROP DATABASE IF EXISTS Tcount;")
#        cur.close()
#        cur = conn.cursor()
#        cur.execute("CREATE DATABASE Tcount;")
#        cur.close()
#        conn.commit()
#        conn.close()

        conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
        
        #Create a Table
        #The first step is to create a cursor. 

        cur = conn.cursor()
        try:
            cur.execute('''CREATE TABLE Tweetwordcount 
                (word TEXT PRIMARY KEY     NOT NULL,
                count INT     NOT NULL);''')
            conn.commit()
        except:
            # Continue on if the table already exists.
            pass

       

    def process(self, tup):
        word = tup.values[0]

        # Write codes to increment the word count in Postgres
        # Use psycopg to interact with Postgres
        # Database name: Tcount 
        # Table name: Tweetwordcount 
        # you need to create both the database and the table in advance.
        

        # Increment the local count
        count = self.counts[word] + 1
        self.counts[word] = count
        self.emit([word, self.counts[word]])

        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))

        cur = conn.cursor()

        if (count == 1):
            cur.execute("INSERT INTO Tweetwordcount (word,count) \
                VALUES (word, 1);")
        else:
            cur.execute("UPDATE Tweetwordcount SET count=%d WHERE word=%s", (count, word))
        conn.commit()

        #Select
#        cur.execute("SELECT word, count from Tweetwordcount")
#        records = cur.fetchall()
#        for rec in records:
#            print "word = ", rec[0]
#            print "count = ", rec[1], "\n"
#        conn.commit()

        conn.close()
