from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMessageBox
from qt_housepriceprediction.HousePricePrediction import Ui_MainWindow
from FileUtil import FileUtil


class HousePricePredictionEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.model = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        self.loadModelOnStartup()
        self.pushButtonPrediction.clicked.connect(self.onPredictionButtonClicked)
        self.lineEditHousePricingPrediction.setReadOnly(True)

    def loadModelOnStartup(self):
        try:
            self.model = FileUtil.loadmodel("housingmodel.zip")
            if self.model is None:
                QMessageBox.warning(
                    self.MainWindow,
                    "Lỗi",
                    "Không thể tải mô hình. Vui lòng kiểm tra file 'housingmodel.zip'"
                )
        except Exception as e:
            QMessageBox.critical(
                self.MainWindow,
                "Lỗi",
                f"Có lỗi xảy ra khi tải mô hình: {str(e)}"
            )

    def onPredictionButtonClicked(self):
        try:
            # Lấy giá trị từ các input field
            area_income = float(self.lineEditAreaIncome.text())
            area_house_age = float(self.lineEditAreaHouseAge.text())
            area_number_of_rooms = float(self.lineEditAreaNumberofRoom.text())
            area_number_of_bedrooms = float(self.lineEditAreaNumberofBedroom.text())
            area_population = float(self.lineEditAreaPopulation.text())

            # Kiểm tra mô hình đã tải
            if self.model is None:
                QMessageBox.warning(
                    self.MainWindow,
                    "Lỗi",
                    "Mô hình chưa được tải. Vui lòng khởi động lại ứng dụng."
                )
                return

            # Thực hiện dự đoán
            result = self.model.predict([[
                area_income,
                area_house_age,
                area_number_of_rooms,
                area_number_of_bedrooms,
                area_population
            ]])

            # Hiển thị kết quả
            predicted_price = result[0]
            self.lineEditHousePricingPrediction.setText(f"{predicted_price:.2f}")

        except ValueError:
            QMessageBox.warning(
                self.MainWindow,
                "Lỗi",
                "Vui lòng nhập các giá trị số hợp lệ vào tất cả các trường."
            )
        except Exception as e:
            QMessageBox.critical(
                self.MainWindow,
                "Lỗi",
                f"Có lỗi xảy ra khi dự đoán: {str(e)}"
            )

    def show(self):
        self.MainWindow.show()