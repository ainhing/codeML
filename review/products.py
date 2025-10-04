class ListProduct:
    def __init__(self):
        self.products=[] #có câps phát ô nhớ nhưng chưa có dữ liệu
    def add_product(self,p):
        self.products.append(p)
    def print_products(self):
        for p in self.products:
            print(p)
    def sort_desc_price(self):
        #self.products.sort(key=lambda p: p.price, reverse=True)
        for i in range(0,len(self.products)):
            for j in range(i+1,len(self.products)):
                pi=self.products[i]
                pj=self.products[j]
                if pi.price < pj.price:
                    self.products[i]= pj
                    self.products[j]= pi
    def sort_asc_price(self):
        self.products.sort(key=lambda p: (p.price, p.quantity))

