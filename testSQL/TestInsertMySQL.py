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
sql="insert into student (code,name,age) values (%s,%s,%s)"
val=("sv07","Nguyễn Thị Ái Nhi",20)
cursor.execute(sql,val)
conn.commit()
print(cursor.rowcount," record inserted")
cursor.close()
print('='*50)
cursor = conn.cursor()
sql="insert into student (code,name,age) values (%s,%s,%s)"
val=[
    ("sv08","Trần Thông Biển",28),
    ("sv09","Hồ Hà",22),
    ("sv10","SOoooo",27),
     ]
cursor.executemany(sql,val)
conn.commit()
print(cursor.rowcount," record inserted")
cursor.close()