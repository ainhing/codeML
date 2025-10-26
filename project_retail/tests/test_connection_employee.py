from project_retail.models.Employee import Employee
from project_retail.tests.test_connnection import conn

def get_all_employee():
    cursor = conn.cursor()
    sql = "SELECT * FROM employee"
    cursor.execute(sql)
    dataset = cursor.fetchall()
    for item in dataset:
        print(item)
    #print(dataset)
    cursor.close()
def login(uid,pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM employee " \
          "where Email='"+uid+"' and Password='"+pwd+"' "

    cursor.execute(sql)

    dataset = cursor.fetchone()
    if dataset != None:
        print(dataset)
    else:
        print("login failed")
    cursor.close()
def login2(uid,pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM employee " \
          "where Email=%s and Password=%s "
    val=(uid,pwd)
    cursor.execute(sql,val)

    dataset = cursor.fetchone()
    if dataset != None:
        print(dataset)
    else:
        print("login failed")
    cursor.close()
def login3(uid,pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM employee " \
          "where Email=%s and Password=%s "
    val=(uid,pwd)
    cursor.execute(sql,val)

    dataset = cursor.fetchone()
    emp=None
    if dataset != None:
        emp=Employee(dataset[0],dataset[1],dataset[2],
                     dataset[3],dataset[4],dataset[5])
    cursor.close()
    return emp
le=login3("teo@gmail.com","123")
if le==None:
    print("Login Failed")
else:
    print(le)
#get_all_employee()
#login("teo@gmail.com","123")
#login2("teo@gmail.com","123")