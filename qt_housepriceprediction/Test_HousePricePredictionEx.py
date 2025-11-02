from PyQt6.QtWidgets import QApplication, QMainWindow


from qt_housepriceprediction.HousePricePredictionEx import HousePricePredictionEx

app=QApplication([])
myWindow=HousePricePredictionEx()
myWindow.setupUi(QMainWindow())
myWindow.show()
app.exec()