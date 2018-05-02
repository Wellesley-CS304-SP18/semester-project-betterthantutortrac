drop table if exists sessions;
drop table if exists courses_taught;
drop table if exists courses_taken;
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

create table tutors(
       tutor_id integer not null,
       tutee_id integer not null,
       course_id integer not null,
       type varchar(50),
       foreign key (tutor_id) references users(pid) on delete cascade,
       foreign key (tutee_id) references users(pid) on delete cascade,
       foreign key (course_id) references courses(cid) on delete cascade
)
ENGINE = InnoDB;

create table courses_taken(
       student_id integer not null,
       course_id integer not null,
       foreign key (student_id) references users(pid) on delete cascade,
       foreign key (course_id) references courses(cid) on delete cascade
)
ENGINE = InnoDB;

create table courses_taught(
       prof_id integer not null,
       course_id integer not null,
       foreign key (prof_id) references users(pid) on delete cascade,
       foreign key (course_id) references courses(cid) on delete cascade
)
ENGINE = InnoDB;

create table sessions(
       user_id integer not null,
       course_id integer not null,
       is_tutor enum('y','n'),
       begin_time datetime,
       end_time datetime,
       foreign key (user_id) references users(pid) on delete cascade,
       foreign key (course_id) references courses(cid) on delete cascade
)
ENGINE = InnoDB;