import mysql.connector
from datetime import date
import os
from Person import Person

conn = os.environ["MYCONN"]
u_name = os.environ['MYU']
u_pass = os.environ['MYP']
key = os.environ['MYK']

# Using readlines() ProgramStartDate,LastName,FirstName,BirthDate,Ssid,DistrictStudentCode
file1 = open('districtList.csv', 'r')
Lines = file1.readlines()

count = 0
students = {}
# Strips the newline character
for line in Lines:
    #print("Line{}: {}".format(count, line.strip()))
    fields = line.split(",")
    p = Person(fields[2], fields[1], fields[4], fields[5])
    students[p.ssid] = p

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
    p.firstName,
    a.registerDate,
    a.cedars_id
--    p.birthDate,
--    e.startDate as enrollStart
FROM
    lcenroll e
JOIN person p ON p.personDBNum = e.learnerDBNum
JOIN personaddit a ON a.personDBNum = p.personDBNum
WHERE
	e.startDate BETWEEN '{start_date}' AND '{end_date}'
    -- AND a.registerDate >= '{school_start}'
    AND e.officeDBNum = 10
    AND e.lcenrollGroupDBNum = 32
    AND e.lcenrollstatus = 'A'
    -- AND e.dropdate < '{school_start}'
    -- AND NOT EXISTS (SELECT lcenrollDBNum FROM lcenrolloutcome WHERE lcenrollDBNum = e.lcenrollDBNum)
ORDER BY
	p.lastname, p.firstname
"""

cur.execute(sql)
rows = cur.fetchall()

print(len(rows))
idList = []
ssid_list = {}

for row in rows:
    print(*row, sep=", ")
    idList.append(str(row[0]))
    ssid_list[str(row[0])] = row[4]

for id in idList:
    ssid = ssid_list.get(str(id))
    student : Person = students.get(ssid)
    print(student)

    #if student != "X":
        #name = students.get(str(id)).full_name()
        #print(f"{id} {ssid} {name}")


#print(*idList, sep=",")
idString = ','.join(idList)

sql = f"""
SELECT distinct
	e.learnerDBNum as cmsID,
    p.lastName,
    p.firstName
FROM
    lcenroll e
JOIN person p ON p.personDBNum = e.learnerDBNum
WHERE
    e.learnerDBNum in ({idString})
ORDER BY
    p.lastName, p.firstName
"""

#cur.execute(sql)
#rows = cur.fetchall()

#for row in rows:
    #print(*row, sep=", ")

sql = f"""
SELECT
	e.learnerDBNum as cmdID,
    p.lastName,
    p.firstName,
    e.startDate as enrollStart,
    c.lcoutcomeCode as outcomeCode,
    o.outcomeDate
FROM 
	lcenroll e
JOIN person p ON p.personDBNum = e.learnerDBNum
JOIN personaddit a ON a.personDBNum = e.learnerDBNum
JOIN lcenrolloutcome o ON o.lcenrolldbnum = e.lcenrolldbnum
JOIN lcoutcome c ON c.lcoutcomedbnum = o.lcoutcomedbnum
WHERE
	e.learnerDBNum in ({idString})
    AND o.outcomeDate >= {school_start}
    -- AND o.outcomeDate < {end_date}
    -- AND o.outcomeDate BETWEEN {school_start} AND {end_date}
ORDER BY
	e.learnerDBNum, e.startDate
"""

print(sql)
cur.execute(sql)
rows = cur.fetchall()

for row in rows:
    print(*row, sep=", ")

print(len(rows))
con.close()