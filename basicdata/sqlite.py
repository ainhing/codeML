import sqlite3
import pandas as pd
from pyarrow._substrait import run_query

try:
    pd.options.mode.pandas_sql_engine = "sqlite"
except Exception:
    pass

DB_PATH = r"../databases/databases/Chinook_Sqlite.sqlite"

# Giữ nguyên flow: run_query nhận SQL string và trả về DataFrame
def run_query(sql: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(sql, conn)
    return df

try:
    sqliteConnection = sqlite3.connect('../databases/databases/Chinook_Sqlite.sqlite')
    cursor=sqliteConnection.cursor()
    print('DB Init')
    query='SELECT * FROM InvoiceLine LIMIT 5;'
    cursor.execute(query)
    df=pd.DataFrame(cursor.fetchall())
    print(df)
    cursor.close()
except sqlite3.Error as error:
    print('Error occurered - ', error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection Closed')
# (1) GIỮ NGUYÊN: trả về chuỗi SQL
def get_top_invoices_by_total(a, b, N):
    query = f"""
        SELECT InvoiceId, CustomerId, InvoiceDate, Total
        FROM Invoice
        WHERE Total BETWEEN {a} AND {b}
        ORDER BY Total DESC
        LIMIT {N};
    """
    return query

# (2) GIỮ NGUYÊN: trả về chuỗi SQL
def get_top_customers_by_invoice_count(N):
    query = f"""
        SELECT c.CustomerId, c.FirstName || ' ' || c.LastName AS CustomerName,
               COUNT(i.InvoiceId) AS InvoiceCount
        FROM Customer c
        JOIN Invoice i ON c.CustomerId = i.CustomerId
        GROUP BY c.CustomerId
        ORDER BY InvoiceCount DESC
        LIMIT {N};
    """
    return query

# (3) GIỮ NGUYÊN: trả về chuỗi SQL
def get_top_customers_by_total_invoice(N):
    query = f"""
        SELECT c.CustomerId, c.FirstName || ' ' || c.LastName AS CustomerName,
               SUM(i.Total) AS TotalInvoiceValue
        FROM Customer c
        JOIN Invoice i ON c.CustomerId = i.CustomerId
        GROUP BY c.CustomerId
        ORDER BY TotalInvoiceValue DESC
        LIMIT {N};
    """
    return query


# --- GỌI Y HỆT CÁCH BẠN ĐANG GỌI ---
print('='*50)
print(run_query(get_top_invoices_by_total(5, 15, 5)))
print('='*50)
print(run_query(get_top_customers_by_invoice_count(5)))
print('='*50)
print(run_query(get_top_customers_by_total_invoice(5)))