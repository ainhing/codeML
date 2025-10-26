from project_retail.connectors.employee_connector import EmployeeConnector
from project_retail.models.Employee import Employee

ec=EmployeeConnector()
ec.connect()

emp=Employee()
emp.Name="Tommy"
emp.Email="tommy@gmail.com"
emp.Phone="09876123456"
emp.Password="321"
emp.IsDeleted=0
result=ec.insert_employee(emp)
if result>0:
    print("insert Ok Ok Ok")
else:
    print("insert FAILED")