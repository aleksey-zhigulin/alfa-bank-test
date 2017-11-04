# -*- coding: utf-8 -*-

import MySQLdb, re
from optparse import OptionParser

usage = "usage: %prog [options] DateFrom DateTo\n\tDates in format YYYY-MM-DD\n\tDateFrom <= DateTo"
parser = OptionParser(usage=usage)
(options, args) = parser.parse_args()

if len(args) != 2:
    parser.error("incorrect number of arguments")
dateFrom = args[0]
dateTo = args[1]
pattern = re.compile("^\d{4}-\d{2}-\d{2}$")
if not re.match(pattern, dateFrom) or not re.match(pattern, dateTo):
    parser.error("wrong date format")
if dateFrom > dateTo:
    parser.error("invalid date interval")


db = MySQLdb.connect(host="localhost",
                     user="admin",
                     passwd="passw",
                     db="mydb",
                     charset='utf8')

cur = db.cursor()

cur.execute("SHOW COLUMNS FROM credit_request WHERE Field = 'rejection_reason'")
reasons = eval(cur.fetchall()[0][1].replace('enum', ''))
result = {}

query = """
SELECT idclient, first_name, last_name 
FROM credit_request
  LEFT JOIN client on idclient=client  
WHERE (date(credit_request.date) BETWEEN date('{}') AND date('{}'))""".format(dateFrom, dateTo)

for reason in reasons:
    cur.execute(query + " AND rejection_reason='{}'".format(reason))
    print u"Причина отказа: {}".format(reason)
    result[reason] = cur.fetchall()
    for id, first_name, last_name in result[reason]:
        print id, first_name, last_name

# print result
db.close()