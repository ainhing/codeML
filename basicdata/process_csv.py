import pandas as pd

from basicdata.MyStatistic import MyStatistic

df = pd.read_csv("../dataset/SalesTransactions/SalesTransactions.csv",
                 sep=',', encoding='utf-8', low_memory=False)

# da phan la \t
print(df)
print('='*50)
min_value=50
max_value=250
ms=MyStatistic()
df_filter=ms.find_orders_within_range(df, min_value, max_value)
print(df_filter)

print('='*50)
sorted_invoices = ms.get_invoices_within_range(df, min_value, max_value, sortType=True)

print(f"Danh sách hóa đơn có tổng tiền từ {min_value} đến {max_value}, sắp xếp {'tăng' if True else 'giảm'}:")
for order_id, total in sorted_invoices:
    print(f"OrderID: {order_id}, Tổng tiền: {total:.2f}")

