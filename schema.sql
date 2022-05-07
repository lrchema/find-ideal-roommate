drop database if exists testdb;
create database testdb;
use testdb;

drop table if exists animals;

create table animals(
    id INT primary key AUTO_INCREMENT,
    name text not null,
    email text not null,
    password text not null,
    species text,
    image text,
    issetup boolean
);