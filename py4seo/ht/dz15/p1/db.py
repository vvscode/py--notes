import peewee

psql_db = peewee.PostgresqlDatabase(
    "library",
    user="py4seo",
    host="46.30.164.249",
    password="PY1111forSEO",
    autorollback=True,
)


class LinkRecord(peewee.Model):
    id = peewee.AutoField()
    page_url = peewee.TextField()
    url = peewee.TextField()
    name = peewee.TextField()

    class Meta:
        database = psql_db
        db_table = "vasiliy_vanchuk_dz15_p1"


psql_db.connect()
psql_db.create_tables([LinkRecord], safe=True)
