from project_retail.connectors.employee_connector import EmployeeConnector
from project_retail.models.Employee import Employee

ec=EmployeeConnector()
ec.connect()

#emp=ec.get_detail(5)
emp=Employee()
emp.ID=6
result=ec.delete_employee(emp)
if result>0:
    print("DELETE OK")
else:
    print("DELETE FAILED")