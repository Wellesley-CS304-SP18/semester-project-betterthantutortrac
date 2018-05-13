-- filename: tables.sql --
-- authors: Kate Kenneally, Angelina Li --
-- last modified: 05/13/2018 --
-- description: SQL table DDL --

use kkenneal_db;

drop table if exists sessions;
drop table if exists coursesTaught;
drop table if exists coursesTaken;
drop table if exists tutors;
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
       userType enum('student', 'professor', 'admin', 'other')
)
ENGINE = InnoDB;

create table courses(
       cid integer auto_increment primary key,
       dept varchar(10) not null,
       courseNum varchar(10) not null,
       section varchar(10) not null,
       year integer not null,
       semester enum('Spring', 'Summer I', 'Summer II', 'Fall', 'Winter')
)
ENGINE = InnoDB;

create table tutors(
        pid integer not null,
        cid integer not null,
        foreign key(pid) references users(pid) on delete cascade,
        foreign key(cid) references courses(cid) on delete cascade
)
ENGINE = InnoDB;

create table coursesTaken(
       pid integer not null,
       cid integer not null,
       foreign key (pid) references users(pid) on delete cascade,
       foreign key (cid) references courses(cid) on delete cascade
)
ENGINE = InnoDB;

create table coursesTaught(
       pid integer not null,
       cid integer not null,
       foreign key (pid) references users(pid) on delete cascade,
       foreign key (cid) references courses(cid) on delete cascade
)
ENGINE = InnoDB;

create table sessions(
       pid integer not null,
       cid integer not null,
       isTutor enum('y','n'),
       beginTime datetime,
       endTime datetime,
       sessionType enum(
            'ASC (Academic Success Coordinator)', 
            'Help Room',
            'PLTC Assigned Tutoring',
            'Public Speaking Tutoring',
            'SI (Supplemental Instruction)'
        ),
       foreign key (pid) references users(pid) on delete cascade,
       foreign key (cid) references courses(cid) on delete cascade
)
ENGINE = InnoDB;
