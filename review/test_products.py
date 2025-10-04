from review.product import Product
from review.products import ListProduct

lp=ListProduct()
lp.add_product(Product('p1','coca',15,25))
lp.add_product(Product('p2','pepsi',20,35))
lp.add_product(Product('p3','sting',25,30))
lp.add_product(Product('p4','fanta',15,30))
print("Ban đầu:")
lp.print_products()
print("---List products - Sort Desc Price:---")
lp.sort_desc_price()
lp.print_products()
lp.sort_asc_price()
print("\nCâu 2")
lp.print_products()
