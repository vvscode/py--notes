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
        db_table = "sergey_che2_dz15_p1"


if __name__ == '__main__':
    psql_db.connect()
    psql_db.drop_tables([LinkRecord])
    psql_db.create_tables([LinkRecord], safe=True)
