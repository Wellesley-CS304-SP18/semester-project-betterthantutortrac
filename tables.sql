-- filename: tables.sql --
-- author: Kate Kenneally --
-- last modified: 05/01/2018 --
-- description: SQL table DDL --

drop table if exists sessions;
drop table if exists courses_taught;
drop table if exists courses_taken;
-- drop table if exists tutors; --
drop table if exists courses;
drop table if exists users;

create table users(
       pid integer auto_increment primary key,
       name varchar(50) not null,
       email varchar(50) not null,
       password varchar(50) not null,
       permissions varchar(100) not null,
       year integer,
       bnumber char(9),
       usertype enum('student', 'professor', 'admin', 'other')
)
ENGINE = InnoDB;

create table courses(
       cid integer auto_increment primary key,
       dept varchar(10) not null,
       coursenum varchar(10) not null,
       section varchar(10) not null,
       year integer not null,
       semester enum('Spring', 'Summer I', 'Summer II', 'Fall', 'Winter')
)
ENGINE = InnoDB;

/*
create table tutors(
       tutor_id integer not null,
       tutee_id integer not null,
       courseId integer not null,
       type varchar(50),
       foreign key (tutor_id) references users(pid) on delete cascade,
       foreign key (tutee_id) references users(pid) on delete cascade,
       foreign key (courseId) references courses(cid) on delete cascade
) 
ENGINE = InnoDB;
*/

create table courses_taken(
       studentId integer not null,
       courseId integer not null,
       foreign key (studentId) references users(pid) on delete cascade,
       foreign key (courseId) references courses(cid) on delete cascade
)
ENGINE = InnoDB;

create table courses_taught(
       profId integer not null,
       courseId integer not null,
       foreign key (profId) references users(pid) on delete cascade,
       foreign key (courseId) references courses(cid) on delete cascade
)
ENGINE = InnoDB;

create table sessions(
       userId integer not null,
       courseId integer not null,
       isTutor enum('y','n'),
       beginTime datetime,
       endTime datetime,
       sessiontype varchar(50),
       foreign key (userId) references users(pid) on delete cascade,
       foreign key (courseId) references courses(cid) on delete cascade
)
ENGINE = InnoDB;