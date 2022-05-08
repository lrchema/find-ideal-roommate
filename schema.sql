create database if not exists roommate;

use roommate;

drop table if exists user_info;

Create table if not exists user_info 
(userid int auto_increment primary key,
username varchar(50) not null,
email varchar(50) not null,
password varchar(10) not null,
is_profile_setup boolean  default 0,
name varchar(150),
gender varchar(1),
age  int,
lang varchar(100),
room_city varchar(200),
room_area varchar(200),
dist_to_transport int,
food_pref varchar(50),
drinker boolean,
shift varchar(50),
profile_picture varchar(200),
en_suite_bathroom  boolean,
passions varchar(400),
have_roof boolean);

drop table if exists city_areas;

create table if not exists city_areas
(id int auto_increment primary key,
city varchar(200),
area varchar(300));

drop table if exists passions;

create table if not exists passions
(id int auto_increment primary key,
passion varchar(200));
