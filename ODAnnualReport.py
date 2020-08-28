import mysql.connector
from datetime import date
from collections import namedtuple
import csv
import os
from enum import Enum
from Person import *

conn = os.environ["MYCONN"]
u_name = os.environ['MYU']
u_pass = os.environ['MYP']
key = os.environ['MYK']

def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

Gender = enum('MALE', 'FEMALE', 'N_A')
count = 0
students = {}

studentRecord = namedtuple('StudentRecord', ' startDate, lastName, firstName, birthdate, ssID, districtID')
for s in map(studentRecord._make, csv.reader(open("districtList.csv", "r"))):
    p = Person(s.firstName, s.lastName, s.ssID, s.districtID, Gender.MALE, datetime.date(1950,5,12))
    students[p.ssid] = p

# Using readlines() ProgramStartDate,LastName,FirstName,BirthDate,Ssid,DistrictStudentCode
#file1 = open('districtList.csv', 'r')
# Lines = file1.readlines()
#
# count = 0
# students = {}
# # Strips the newline character
# for line in Lines:
#     #print("Line{}: {}".format(count, line.strip()))
#     fields = line.split(",")
#     last_name = fields[2]
#     first_name = fields[1]
#     ssid = fields[4]
#     did = fields[5]
#     p = Person(first_name, last_name, ssid, did, Gender.MALE, datetime.date(1950,5,12))
#     students[p.ssid] = p

con = mysql.connector.connect(user=u_name, password=u_pass, host=conn, database='cmsdb')

cur = con.cursor(prepared=True)

today = date.today()

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
    o.outcomeDate,
    r.regionName,
    ad.city
FROM 
	lcenroll e
JOIN person p ON p.personDBNum = e.learnerDBNum
JOIN personaddit a ON a.personDBNum = e.learnerDBNum
JOIN lcenrolloutcome o ON o.lcenrolldbnum = e.lcenrolldbnum
JOIN lcoutcome c ON c.lcoutcomedbnum = o.lcoutcomedbnum
JOIN region r ON r.regionID = p.region
JOIN address ad ON ad.personDBNum = p.personDBNum
WHERE
	e.learnerDBNum in ({idString})
    AND o.outcomeDate >= {school_start}
    AND ad.status = 'A'
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

# sql_delete = f"""
# SELECT lcenrollgroupdbnum FROM lcenroll WHERE learnerDBNum IN ({idString})
# -- UPDATE lcenroll SET lcenrollgroupdbnum = 0 WHERE learnerDBNum IN ({idString})
# """
# cur.execute(sql_delete)
#
# rows = cur.fetchall()
# for row in rows:
#     print(*row, sep=", ")
# con.commit()

con.close()