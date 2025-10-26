from PyQt6.QtWidgets import QApplication, QMainWindow

from blog49.MainWindowBlog49Ex import MainWindowEx

app=QApplication([])
myWindow=MainWindowEx()
myWindow.setupUi(QMainWindow())
myWindow.connectMySQL()
myWindow.selectAllStudent()
myWindow.show()
app.exec()