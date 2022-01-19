create database insurence;
use insurence;

create table customer(
cus_id int AUTO_INCREMENT PRIMARY KEY,
name varchar(50) 
);

CREATE TABLE claims(
 claim_id INT AUTO_INCREMENT PRIMARY KEY,
 expensise int,
 description TEXT,
 resolved TINYINT DEFAULT 0,
 cus_id int not null, 
 benficary varchar(100),
 health_care_provider varchar(100),
 foreign key(cus_id) references customer(cus_id) ON DELETE CASCADE,
 date_of_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

insert into claims(expensise, description, cus_id, benficary,health_care_provider) values(10, 'lorem dolar episum', 1, 'mohamed', 'hospital123')


--select * from claims where resolved=0; 
--update claims set resolved=1 where claim_id=1;

create table dependants(
dep_name varchar(100),
cus_id int not null,
primary key(cus_id, dep_name),
foreign key(cus_id) references customer(cus_id) ON DELETE CASCADE
);

create table plan_type(
type_id int auto_increment primary key,
type_name enum('basic', 'premium', 'golden') not null
);

insert into plan_type(type_name) values('basic'),('premium'), ('golden');


create table plan(
plan_id int auto_increment primary key,
type_id int not null ,
cus_id int not null , 
benficary varchar(100),
foreign key(cus_id) references customer(cus_id) on delete cascade,
foreign key(type_id) references plan_type(type_id) on delete cascade
);

insert into plan(type_id,cus_id,benficary) values(2,1,'ahmed')
insert into plan(type_id,cus_id,benficary) values(1,1,'tamer')
insert into plan(type_id,cus_id,benficary) values(1,1,'mazen')
--select * from plan where cus_id = 1


create table hospital(
hos_id int auto_increment primary key,
hos_name varchar(100),
location varchar(100),
type_id int not null,
foreign key(type_id) references plan_type(type_id) on delete cascade
);

--select * from hospital where type_id = 3
insert into hospital(hos_name,location, type_id) values('hos02', 'cairo',3);