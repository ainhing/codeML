import mysql.connector

server='localhost'
port=3306
database='studentmanagement'
username="root"
password="123456789"

conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)
""""
cursor = conn.cursor()
sql="DELETE from student where ID=10"
cursor.execute(sql)
conn.commit()
print(cursor.rowcount," record(s) affected")
"""
cursor = conn.cursor()
sql = "DELETE from student where ID=%s"
val = (13,)
cursor.execute(sql, val)
conn.commit()
print(cursor.rowcount," record(s) affected")