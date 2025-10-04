from review.product import Product

p1=Product("p1","coca",15,80)
print(p1)

p2=Product()#lúc này thuộc tính k có gan giá trị => nên bị none => khồn được sài
# => bắt buộc phải làm thủ công
p2.id='p2'
p2.name='pepsi'
print(p2)