from peewee import SqliteDatabase, PostgresqlDatabase, Model, CharField, DateTimeField

# SQLite database using WAL journal mode and 64MB cache.
# sqlite_db = SqliteDatabase('my_database.db')


db = PostgresqlDatabase(
    'library', user='py4seo',
    password='PY1111forSEO',
    host='46.30.164.249', port=5432
)


class GoogleImage(Model):

    keyword = CharField()
    image_url = CharField(max_length=1024)
    date = DateTimeField()

    class Meta:
        database = db
        table_name = 'images_from_google'


if __name__ == '__main__':
    db.connect()
    db.drop_tables([GoogleImage])
    db.create_tables([GoogleImage])
