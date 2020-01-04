import datetime
import peewee

psql_db = peewee.PostgresqlDatabase(
    "library",
    user="py4seo",
    host="46.30.164.249",
    password="PY1111forSEO",
    autorollback=True,
)

class OzonCategory(peewee.Model):
    id = peewee.AutoField()
    name = peewee.TextField(unique=True)

    class Meta:
        database = psql_db
        db_table = "vasiliy_vanchuk__ozon_category"

class OzonProduct(peewee.Model):
    id = peewee.AutoField()
    url = peewee.TextField()
    price = peewee.TextField()
    title = peewee.TextField()
    images = peewee.TextField()

    categories = peewee.ManyToManyField(OzonCategory, backref='goods')

    class Meta:
        database = psql_db
        db_table = "vasiliy_vanchuk__ozon_product"

# class ProductToCategory(Model):
#     product = peewee.ForeignKeyField(OzonProduct)
#     category = peewee.ForeignKeyField(OzonCategory)

#     class Meta:
#         database = psql_db
#         db_table = "vasiliy_vanchuk__ozon_product2category"

psql_db.connect()
psql_db.create_tables([OzonCategory, OzonProduct, OzonProduct.categories.get_through_model()], safe=True)
