from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

from review.ListProducts import Ui_MainWindow
from review.test_products import lp


class MainWindowListProductExt(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
    def showWindow(self):
        self.MainWindow.show()
    def load_products(self,lp):
        self.tableWidgetproduct.setRowCount(0)
        for i in range(0,len(lp.products)):
            p=lp.products[i]
            number_row=self.tableWidgetproduct.rowCount()
            #insert new row
            self.tableWidgetproduct.insertRow(number_row)
            #fill attributes product into Listview
            self.tableWidgetproduct.setItem(number_row,0,QTableWidgetItem(p.id))
            self.tableWidgetproduct.setItem(number_row, 1, QTableWidgetItem(p.name))
            self.tableWidgetproduct.setItem(number_row, 2, QTableWidgetItem(str(p.quantity)))
            self.tableWidgetproduct.setItem(number_row, 3, QTableWidgetItem(str(p.price)))


