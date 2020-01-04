from peewee import *


db = PostgresqlDatabase(
    'library', user='py4seo',
    password='PY1111forSEO',
    host='46.30.164.249', port=5432
)


class Category(Model):
    name = CharField(max_length=1024, index=True)
    link = CharField(max_length=1024)
    parent = CharField(max_length=1024)

    class Meta:
        database = db


class Author(Model):
    name = CharField(max_length=1024)
    profile_link = CharField(max_length=1024)
    phone = CharField(max_length=1024)

    class Meta:
        database = db


class Ad(Model):

    author = ForeignKeyField(Author, backref='ads')
    categories = ManyToManyField(Category, backref='ads')

    url = CharField(max_length=1024)
    name = CharField(max_length=1024)
    price = CharField(max_length=1024)
    image = CharField(max_length=1024)
    date = DateTimeField()

    class Meta:
        database = db


AdCategory = Ad.categories.get_through_model()


if __name__ == '__main__':
    db.connect()
    db.drop_tables([Ad, Author, Category, AdCategory])
    db.create_tables([Ad, Author, Category, AdCategory])
