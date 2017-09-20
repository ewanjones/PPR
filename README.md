# PPR
A project management web app

TO DO:
- Add user system
  * Connect user to project request
  * Add users alloctation
- Add OCR mapping (and questions) to request page


PROJECTS TABLE
+--------------+---------------+------+-----+---------+----------------+
| Field        | Type          | Null | Key | Default | Extra          |
+--------------+---------------+------+-----+---------+----------------+
| pid          | int(10)       | NO   | PRI | NULL    | auto_increment |
| uid          | int(10)       | YES  |     | NULL    |                |
| title        | varchar(30)   | YES  |     | NULL    |                |
| type         | varchar(50)   | YES  |     | NULL    |                |
| product      | varchar(50)   | YES  |     | NULL    |                |
| activity     | varchar(50)   | YES  |     | NULL    |                |
| exchange     | varchar(50)   | YES  |     | NULL    |                |
| pcp          | int(6)        | YES  |     | NULL    |                |
| dps          | int(6)        | YES  |     | NULL    |                |
| dateReceived | date          | YES  |     | NULL    |                |
| dateRequired | date          | YES  |     | NULL    |                |
| priority     | varchar(50)   | YES  |     | NULL    |                |
| leadCustomer | varchar(50)   | YES  |     | NULL    |                |
| thp          | int(6)        | YES  |     | NULL    |                |
| other        | varchar(4000) | YES  |     | NULL    |                |
+--------------+---------------+------+-----+---------+----------------+
15 rows


STATUS TABLE
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| pid           | int(10)      | NO   | PRI | NULL    | auto_increment |
| uid           | int(10)      | YES  |     | NULL    |                |
| dateCreated   | date         | YES  |     | NULL    |                |
| custStatus    | varchar(30)  | YES  |     | NULL    |                |
| custName      | varchar(20)  | YES  |     | NULL    |                |
| custComplete  | date         | YES  |     | NULL    |                |
| spineStatus   | varchar(30)  | YES  |     | NULL    |                |
| spineName     | varchar(20)  | YES  |     | NULL    |                |
| spineComplete | date         | YES  |     | NULL    |                |
| commStatus    | varchar(30)  | YES  |     | NULL    |                |
| commName      | varchar(20)  | YES  |     | NULL    |                |
| commComplete  | date         | YES  |     | NULL    |                |
| summary       | json         | YES  |     | NULL    |                |
| notes         | varchar(500) | YES  |     | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+
14 rows


TRACKING TABLE
+-------------+-------------+------+-----+---------+-------+
| Field       | Type        | Null | Key | Default | Extra |
+-------------+-------------+------+-----+---------+-------+
| pid         | int(10)     | NO   | PRI | NULL    |       |
| estSurvey   | varchar(15) | YES  |     | NULL    |       |
| estCust     | varchar(15) | YES  |     | NULL    |       |
| estSpine    | varchar(15) | YES  |     | NULL    |       |
| estCivils   | varchar(15) | YES  |     | NULL    |       |
| plannedCost | int(15)     | YES  |     | NULL    |       |
| finalCost   | int(15)     | YES  |     | NULL    |       |
+-------------+-------------+------+-----+---------+-------+
7 rows
