# Get all the words whose count falls within the given range.

import psycopg2
import sys

args = sys.argv
if len(args) < 3:
   quit()

min = args[1]
max = args[2]

#Connecting to a database
#Note: If the database does not exist, then this command will create the database
conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")

cur = conn.cursor()

#Select
cur.execute("SELECT word, count from Tweetwordcount where count BETWEEN %s and %s;" % (min, max))
records = cur.fetchall()
for rec in records:
   print "%s: %d " % (rec[0], rec[1])
conn.commit()

conn.close()
