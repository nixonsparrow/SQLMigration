import datetime
import os

import pandas as pd
from sqlalchemy import create_engine


def migrate_mysql_to_postgresql():
    migration_init_time = datetime.datetime.now()

    mysql_engine = create_engine(
        "mysql+pymysql://root:root@127.0.0.1/db_mysql", pool_recycle=3600
    )
    psql_engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@127.0.0.1/postgres_db",
        pool_recycle=3600,
    )

    len_mysql = pd.read_sql("select count(*) from students;", mysql_engine).iloc[0, 0]

    batch_size = int(os.getenv("BATCH_SIZE") or 50_000)
    n_batches = (len_mysql // batch_size) + 2

    columns = ["ID", "FirstName", "LastName", "Token", "Grade"]
    cols_str = ", ".join(columns)

    for i in range(1, n_batches):
        max_idx = i * batch_size
        min_idx = max_idx - batch_size
        query = (
            f"select {cols_str} from students where id > {min_idx} and id <= {max_idx};"
        )
        df = pd.read_sql(query, mysql_engine)
        df.to_sql(
            "students", psql_engine, schema="public", if_exists="append", index=False
        )

        print(
            f"Inserted rows with indexes {min_idx + 1} - {max_idx if max_idx < len_mysql else len_mysql} to PostgreSQL"
        )

    print("Migration finished in:", datetime.datetime.now() - migration_init_time)


if __name__ == "__main__":
    migrate_mysql_to_postgresql()
