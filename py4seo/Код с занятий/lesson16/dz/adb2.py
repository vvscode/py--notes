import sqlalchemy as sa


db_settings = {
    "dbname": "library",
    "user": "py4seo",
    "password": "PY1111forSEO",
    "host": "46.30.164.249",
    "port": "5432",
}

dsn = "postgresql://{user}:{password}@{host}/{dbname}".format(**db_settings)


metadata = sa.MetaData()


Link = sa.Table(
    'sergey_che_links', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('href', sa.String(255)),
    sa.Column('name', sa.String(255))
)


if __name__ == '__main__':
    engine = sa.create_engine(dsn)
    metadata.drop_all(engine)
    metadata.create_all(engine)
