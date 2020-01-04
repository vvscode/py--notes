from sqlalchemy import *
import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa


metadata = sa.MetaData()


db_config = {
    'user': 'py4seo',
    'database': 'library',
    'host': '46.30.164.249',
    'password': 'PY1111forSEO'
}


Links = sa.Table(
    'stas_async', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(1024)),
    sa.Column('url', sa.String(1024))
)


async def create_table(engine):
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS stas_async')
        await conn.execute('''CREATE TABLE stas_async (
                                  id serial PRIMARY KEY,
                                  name varchar(1024),
                                  url varchar(1024))''')


async def go():
    async with create_engine(**db_config) as engine:
        await create_table(engine)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())
