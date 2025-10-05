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
# (2.1) Truy vấn toàn bộ Sinh viên:
cursor = conn.cursor()
sql="select * from student"
cursor.execute(sql)
dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id = item[0]
    code = item[1]
    name = item[2]
    age = item[3]
    avatar = item[4]
    intro = item[5]
    print(align.format(id, code, name, age))
"""" 
    id = item[0] if item[0] is not None else ''
    code = item[1] if item[1] is not None else ''
    name = item[2] if item[2] is not None else ''
    age = item[3] if item[3] is not None else ''
    avatar = item[4] if item[4] is not None else ''
    intro = item[5] if item[5] is not None else ''
    print(align.format(id, code, name, age))
"""
cursor.close()
print('='*50)
#(2.2) Truy vấn các Sinh viên có độ tuổi từ 22 tới 26:
cursor=conn.cursor()
sql1="SELECT * FROM student where Age>=22 and Age<=26"
cursor.execute(sql1)
dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id = item[0]
    code = item[1]
    name = item[2]
    age = item[3]
    avatar = item[4]
    intro = item[5]
    print(align.format(id, code, name, age))
cursor.close()
print('='*50)
#(2.3) Truy vấn toàn bộ sinh viên và sắp xếp theo tuổi tăng dần:
cursor = conn.cursor()
sql2="SELECT * FROM student " \
    "order by Age asc"
cursor.execute(sql2)
dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))
cursor.close()
print('='*50)
#(2.4) Truy vấn các Sinh viên có độ tuổi từ 22 tới 26 và sắp xếp theo tuổi giảm dần:
cursor = conn.cursor()
sql3="SELECT * FROM student " \
    "where Age>=22 and Age<=26 " \
    "order by Age desc "
cursor.execute(sql3)
dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))
cursor.close()
print('='*50)
# (2.5) Truy vấn chi tiết thông tin Sinh viên khi biết Id:
cursor = conn.cursor()
sql4="SELECT * FROM student " \
    "where ID=1 "
cursor.execute(sql4)
dataset=cursor.fetchone()
if dataset!=None:
    id,code,name,age,avatar,intro=dataset
    print("Id=",id)
    print("code=",code)
    print("name=",name)
    print("age=",age)
cursor.close()
print('='*50)

cursor = conn.cursor()
sql5="SELECT * FROM student LIMIT 3 OFFSET 0"
cursor.execute(sql5)
dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))
cursor.close()
print('='*50)

cursor = conn.cursor()
sql6="SELECT * FROM student LIMIT 3 OFFSET 3"
cursor.execute(sql6)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()

print('='*50)
print('PADDDDDDDDDD'*10)
cursor =conn.cursor()
sql7='SELECT count(*) FROM student'
cursor.execute(sql7)
dataset=cursor.fetchone()
rowcount=dataset[0]
limit=3
step=3
for offset in range(0,rowcount,step):
    sql8=f'SELECT * FROM student limit {limit} OFFSET {offset}'
    cursor.execute(sql8)
    dataset = cursor.fetchall()
    align = '{0:<3} {1:<6} {2:<15} {3:<10}'
    print(align.format('ID', 'Code', 'Name', "Age"))
    for item in dataset:
        id = item[0]
        code = item[1]
        name = item[2]
        age = item[3]
        avatar = item[4]
        intro = item[5]
        print(align.format(id, code, name, age))

cursor.close()