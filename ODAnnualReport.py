import mysql.connector
from datetime import date
import os

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
	e.learnerDBNum as cmsID,
    p.lastName,
    p.firstName
--    p.birthDate,
--    e.startDate as enrollStart
FROM
    lcenroll e
JOIN person p ON p.personDBNum = e.learnerDBNum
WHERE
	e.startDate BETWEEN '{start_date}' AND '{end_date}'
    AND e.officeDBNum = 10
    AND e.lcenrollGroupDBNum = 32
    AND e.lcenrollstatus = 'A'
    AND e.dropdate < '{school_start}'
    AND NOT EXISTS (SELECT lcenrollDBNum FROM lcenrolloutcome WHERE lcenrollDBNum = e.lcenrollDBNum)
ORDER BY
	p.lastname, p.firstname
"""
IN = '2019-07-01', '2020-08-07'
input = (IN)

cur.execute(sql)
rows = cur.fetchall()

print(len(rows))

for row in rows:
    print(row)
    #for field in row:
     #   print(field)

con.close()
