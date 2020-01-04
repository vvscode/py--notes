import datetime
import peewee

psql_db = peewee.PostgresqlDatabase(
    "library",
    user="py4seo",
    host="46.30.164.249",
    password="PY1111forSEO",
    autorollback=True,
)


class UrlRecord(peewee.Model):
    id = peewee.AutoField()
    time_stamp = peewee.DateTimeField(default=datetime.datetime.now)
    url = peewee.TextField()
    depth = peewee.IntegerField()
    status_code = peewee.IntegerField()
    response_time = peewee.FloatField()
    h1 = peewee.TextField()
    title = peewee.TextField()
    images = peewee.TextField()
    price = peewee.TextField()
    body = peewee.TextField()

    class Meta:
        database = psql_db
        db_table = "vasiliy_vanchuk"


psql_db.connect()
psql_db.create_tables([UrlRecord], safe=True)
