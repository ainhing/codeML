from PyQt6.QtWidgets import QApplication, QMainWindow

from review.MainWindowListProductsExt import MainWindowListProductExt
from review.product import Product
from review.products import ListProduct

app=QApplication([])
qmain=QMainWindow()
my_window=MainWindowListProductExt()
my_window.setupUi(qmain)
lp=ListProduct()
lp.add_product(Product('p1','coca',15,25))
lp.add_product(Product('p2','pepsi',20,35))
lp.add_product(Product('p3','sting',25,30))
lp.add_product(Product('p4','fanta',15,30))
my_window.load_products(lp)
my_window.showWindow()
app.exec()
