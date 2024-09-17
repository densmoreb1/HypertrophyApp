drop database if exists fitness;
create database if not exists fitness;

use fitness;

create table if not exists exercises (
	id int auto_increment primary key,
	name varchar(100),
	muscle_group varchar(100),
	unique (name)
);

create table if not exists users (
	id int auto_increment primary key,
	name varchar(100)
);

create table if not exists mesos (
	id int auto_increment primary key,
	name varchar(100),
	user_id int,
	exercise_id int,
	day_id int,
	order_id int,
	date_created datetime,
	foreign key (user_id) references users(id),
	foreign key (exercise_id) references exercises(id),
	unique (name, user_id, exercise_id, day_id)
);

create table if not exists workouts (
	id int auto_increment primary key,
	exercise_id int,
	meso_id int, 
	reps int,
	date_finished date,
	foreign key (exercise_id) references exercises(id),
	foreign key (meso_id) references mesos(id)
);

INSERT INTO users (name) VALUES ('brandon');

INSERT INTO exercises (name, muscle_group) VALUES ('incline bench press', 'chest');
INSERT INTO exercises (name, muscle_group) VALUES ('pec dec', 'chest');
INSERT INTO exercises (name, muscle_group) VALUES ('machine chest press', 'chest');
INSERT INTO exercises (name, muscle_group) VALUES ('incline dumbbell press', 'chest');
INSERT INTO exercises (name, muscle_group) VALUES ('low incline dumbbell press', 'chest');
INSERT INTO exercises (name, muscle_group) VALUES ('smith machine row', 'back');
INSERT INTO exercises (name, muscle_group) VALUES ('deadlift', 'back');
INSERT INTO exercises (name, muscle_group) VALUES ('machine t-bar row', 'back');
INSERT INTO exercises (name, muscle_group) VALUES ('assisted pull-up', 'back');
INSERT INTO exercises (name, muscle_group) VALUES ('chest supported row', 'back');
INSERT INTO exercises (name, muscle_group) VALUES ('freemotion curl', 'biceps');
INSERT INTO exercises (name, muscle_group) VALUES ('leg press', 'quads');
INSERT INTO exercises (name, muscle_group) VALUES ('calf press machine', 'calves');
INSERT INTO exercises (name, muscle_group) VALUES ('leg press calves', 'calves');
