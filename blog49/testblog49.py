from PyQt6.QtWidgets import QApplication, QMainWindow

from blog49.MainWindowBlog49Ex import MainWindowBlog49Ex

app=QApplication([])
myWindow=MainWindowBlog49Ex()
myWindow.setupUi(QMainWindow())
myWindow.connectMySQL()
myWindow.selectAllStudent()
myWindow.show()
app.exec()