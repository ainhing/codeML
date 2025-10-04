import pandas as pd

class MyStatistic:
        def find_orders_within_range(self, df, minValue, maxValue):
            # Tính tổng giá trị từng đơn hàng
            order_totals = df.groupby('OrderID').apply(
                lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum()
            )
            # Trả về Series đã lọc
            return order_totals[(order_totals >= minValue) & (order_totals <= maxValue)]

        def get_invoices_within_range(self, df, minValue, maxValue, sortType=True):
            # Nhận Series từ hàm trên
            filtered = self.find_orders_within_range(df, minValue, maxValue)
            # Sắp xếp theo sortType
            sorted_filtered = filtered.sort_values(ascending=sortType)
            # Trả về danh sách tuple (OrderID, TotalValue)
            return list(sorted_filtered.items())


if __name__ == "__main__":
    # Đọc dữ liệu
    df = pd.read_csv('dataset/SalesTransactions.csv')

    # Nhập khoảng giá trị
    minValue = float(input("Nhập giá trị min: "))
    maxValue = float(input("Nhập giá trị max: "))

    # Gọi hàm xử lý
    result = MyStatistic.find_orders_within_range(df, minValue, maxValue)

    # In kết quả
    print(f"Danh sách các hóa đơn trong phạm vi giá trị từ {minValue} đến {maxValue} là: {result}")


