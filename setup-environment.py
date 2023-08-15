import datetime
import os
import random
import time
import uuid

from dotenv import load_dotenv

from mysql import connector as mysql_connector

load_dotenv()

MYSQL_DATABASE = {
    "host": "localhost",
    "database": "db_mysql",
    "user": "root",
    "password": "root",
    "port": "3306",
}


def prepare_docker_databases():
    os.system("docker-compose build --no-cache")
    os.system("docker-compose up -d")


def connect_do_mysql(db_data):
    docker_init_time = datetime.datetime.now()
    attempt = 1
    wait_time = 10
    connection = None
    while not connection:
        try:
            connection = mysql_connector.connect(**db_data)
        except mysql_connector.errors.DatabaseError:
            if attempt >= 20:
                raise ConnectionError(
                    f"Connection to MySQL has failed after {attempt} attempts!"
                )

            print(f"Waiting for MySQL container (attempt: {attempt})")
            attempt += 1
            time.sleep(wait_time)

    print("Docker setup time:", datetime.datetime.now() - docker_init_time)
    print("CONNECTED TO MYSQL!\nProcessing data creation...")
    mysql_init_time = datetime.datetime.now()

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")

    if cursor.fetchall():
        raise IndexError("Table already filled with students! Aborting...")

    random_uuid = True if os.getenv("RANDOM_UUID") == "True" else False
    random_grade = True if os.getenv("RANDOM_GRADE") == "True" else False
    students_to_create = int(os.getenv("STUDENTS_TO_CREATE") or 1_000_000)
    batch_size = int(os.getenv("BATCH_SIZE") or 50_000)
    students_created = 0

    while students_to_create > 0:
        batch_range = (
            batch_size if students_to_create >= batch_size else students_to_create
        )
        students_created += batch_range

        cursor = connection.cursor()
        command = "INSERT INTO students(FirstName, LastName, Token, Grade) VALUES"
        for _ in range(batch_range):
            command += (
                f'("Jan", "Kowalski", "{uuid.uuid4() if random_uuid else "x"}", '
                f"{round(random.uniform(2.00, 5.00), 2) if random_grade else 4.75}), "
            )
        command = command[:-2] + ";"
        cursor.execute(command)
        connection.commit()

        print(f"{students_created} students created, {students_to_create} to go...")
        students_to_create -= batch_size

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    students_count = len(cursor.fetchall())

    connection.close()

    print("Data have been created!\n")

    print("MySQL database init time:", datetime.datetime.now() - mysql_init_time)
    print("Students created:", students_count)


if __name__ == "__main__":
    prepare_docker_databases()
    connect_do_mysql(MYSQL_DATABASE)
