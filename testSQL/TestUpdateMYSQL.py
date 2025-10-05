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
cursor = conn.cursor()
sql="update student set name='Hoàng Lão Tà' where Code='sv09'"
cursor.execute(sql)
conn.commit()
print(cursor.rowcount," record(s) affected")