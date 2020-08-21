import mysql.connector
from datetime import date
import os
from enum import Enum
from Person import *

conn = os.environ["MYCONN"]
u_name = os.environ['MYU']
u_pass = os.environ['MYP']
key = os.environ['MYK']

con = mysql.connector.connect(user=u_name, password=u_pass, host=conn, database='cmsdb')

cur = con.cursor(prepared=True)

today = date.today()

def calculate_age(dob):
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

start_date = '2018-01-01'
end_date = '2020-08-07'
school_start = '2019-08-27'

sql = f"""
SELECT
	p.personDBNum as cmsID,
    p.lastName,
    p.firstName,
    p.mainphone,
    p.cellphone,
    p.otherphone,
    p.currentemail
FROM
    person p
JOIN personaddit a ON a.personDBNum = p.personDBNum
WHERE
    p.personStatus = 'A'
    AND a.aleopd IN ('D','A','H')
ORDER BY
	p.lastname, p.firstname
"""

cur.execute(sql)
rows = cur.fetchall()

columns = [tuple[0] for tuple in cur.description]
for column in columns:
    print(column, end=",")
print()
for row in rows:
    print(*row, sep=", ")

print(len(rows))
