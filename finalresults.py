#Sample code snippets for working with psycopg


#Connecting to a database
#Note: If the database does not exist, then this command will create the database


import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import sys

args = sys.argv
if len(args) < 2:
   quit()

word = args[1]
print(word)

conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")

#Select
cur = conn.cursor()
cur.execute("SELECT word, count FROM tweetwordcount WHERE word = \'%s\';" % word)
records = cur.fetchall()
for rec in records:
   print "Total number of occurences of \"%s\": %d" % (rec[0], rec[1])
conn.commit()

conn.close()
