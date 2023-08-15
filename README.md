# SQL Migration 
MySQL -> PostgreSQL

## Steps to take:

1. Clone repository:\
$ git clone git@bitbucket.org:nixonsparrow/sqlmigration.git\
or\
$ git clone https://nixonsparrow@bitbucket.org/nixonsparrow/sqlmigration.git

2. Create Python 3.11 Virtual Environment:\
$ sudo apt-get install python-pip\
$ pip install virtualenv\
$ virtualenv virtualenv_name\
$ virtualenv -p /usr/bin/python3 virtualenv_name\
$ source virtualenv_name/bin/activate\
$ pip install -r requirements.txt

3. Set environment variables or create `.env` file and set variables there (check `.env_example` file for options);

4. To setup environment use command:\
$ python setup-environment.py

5. To process migration use command:\
$ python migrate.py

6. Enjoy two identical databases in different technologies.

## Time assessments
(based on data from slow Windows computer, 1_000_000 rows)
### setup-environment.py
- Docker setup: 100 seconds
- MySQL setup: 40 seconds (60 seconds with randomized data)
### migrate.py
- Migration: 90 seconds
### TOTAL: 230 seconds (250 seconds with randomized data)

## Assumptions:

- Python (3.11.3) VIRTUAL ENVIRONMENT is created and activated;
- Python environment has to have installed packages given in 'requirements.txt' file;
- I have used default values for environment variables for quickstart purposes;
- If you prefer to try various of options just add environment variables with desired values;
- Used environment variables are visible in '.env_example' file;
- To quickly try different values just rename '.env_example' file to '.env' and modify values;
- I have used Python over Bash because I feel more comfortable with that language;
- I have used standard isort and black for clean code basic rules;
- Time measure left to make easier to count processes' part times.
