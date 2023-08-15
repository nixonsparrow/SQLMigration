use db_mysql;

CREATE TABLE students(
    ID int not null AUTO_INCREMENT,
    FirstName varchar(100) NOT NULL,
    LastName varchar(100) NOT NULL,
    Token varchar(100) NOT NULL,
    Grade float(2) NOT NULL,
    PRIMARY KEY (ID)
);
