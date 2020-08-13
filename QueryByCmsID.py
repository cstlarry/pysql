import mysql.connector
from datetime import date
import os

conn = os.environ["MYCONN"]
u_name = os.environ['MYU']
u_pass = os.environ['MYP']
key = os.environ['MYK']

con = mysql.connector.connect(user=u_name, password=u_pass, host=conn,  database='cmsdb')

cur = con.cursor(prepared=True)

today = date.today()
def calculate_age(dob):
  return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

sql = """
SELECT
   personDBNum, 
   firstName, 
   lastName,
   userid,
   CAST(AES_DECRYPT(`password`, %s) AS CHAR) as passStr,
   birthdate
FROM 
   person
WHERE 
   personDBNum in (%s, %s)
ORDER BY 
   lastName, firstName
"""
IN = key, 149257, 149247
input = (IN)

cur.execute(sql, input)
rows = cur.fetchall()

print(len(rows))

for row in rows:
  print(row)
  counter = 0
  for item in row:
    print(item)
    if 'birthdate' == cur.column_names[counter]:
      print(calculate_age(item))
    counter += 1

con.close()



