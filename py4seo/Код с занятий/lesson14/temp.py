from db import Ad, Category, Author


cat = Category.get(Category.id == 4)

for ad in cat.ads:
    print(ad.name, ad.price)
