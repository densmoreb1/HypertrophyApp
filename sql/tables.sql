create database if not exists fitness;

use fitness;

create table if not exists exercises (
	id int auto_increment primary key,
	name varchar(100),
	muscle_group varchar(100)
);

create table if not exists users (
	id int auto_increment primary key,
	name varchar(100)
);

create table if not exists mesos (
	id int auto_increment primary key,
	name varchar(100),
	user_id int,
	date_started date,
	date_ended date,
	foreign key (user_id) references users(id)
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

-- INSERT INTO users (name) VALUES ('brandon');
-- INSERT INTO exercises (name, muscle_group) VALUES ('Incline Bench Press', 'Chest');
-- INSERT INTO exercises (name, muscle_group) VALUES ('Smith Machine Row', 'Back');
