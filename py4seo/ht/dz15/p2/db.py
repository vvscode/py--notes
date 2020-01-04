import sys

from aiopg.sa import create_engine
import sqlalchemy as sa

# It allows to switch dsn from local computer to Sergey's one
local_run = False

# For some reason on Sergey's target (on local both options work fine)
# using pool work strange/slow
# On `True` it creates single connection, not uses pool
use_single_connection = False

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

db_settings = {
    "dbname": "library",
    "user": "py4seo",
    "password": "PY1111forSEO",
    "host": "46.30.164.249",
    "port": "5432",
    "table_name": "vasiliy_vanchuk_dz15_p2",
}

dsn = f"postgresql://{db_settings['user']}:{db_settings['password']}@{db_settings['host']}/{db_settings['dbname']}"

if local_run:
    db_settings = {
        "dbname": "tmp",
        # "user": "py4seo",
        # "password": "PY1111forSEO",
        "host": "127.0.0.1",
        "port": "5432",
        "table_name": "vasiliy_vanchuk_dz15_p2",
    }
    dsn = f"postgresql://{db_settings['host']}/{db_settings['dbname']}"


metadata = sa.MetaData()

records_table = sa.Table(
    db_settings["table_name"],
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("page_url", sa.Text),
    sa.Column("url", sa.Text),
    sa.Column("name", sa.Text),
)


engine = sa.create_engine(dsn)
metadata.bind = engine

metadata.create_all()


async def get_data_saver(use_single_connection=use_single_connection):
    print(f"Get data saver for dsn: {dsn}")
    engine = await create_engine(dsn, maxsize=5, timeout=10)
    if use_single_connection:
        shared_conn = await engine.acquire()
    counter = 1

    async def save_data(data):
        nonlocal counter
        save_counter = counter
        counter += 1

        print(f"Start saving data #{save_counter}")
        command = records_table.insert().values(data)
        if not use_single_connection:
            with (await engine) as local_conn:
                print("Execute command")
                await local_conn.execute(command)
        else:
            await shared_conn.execute(command)
        print(f"Stop saving data #{save_counter}")

    async def close_connection():
        engine.close()
        await engine.wait_closed()

    return save_data, close_connection
