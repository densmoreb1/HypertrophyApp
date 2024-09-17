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
	date_started datetime,
	date_ended datetime,
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

INSERT INTO exercises (name, muscle_group) VALUES ('Incline Bench Press', 'Chest');
INSERT INTO exercises (name, muscle_group) VALUES ('Pec Dec', 'Chest');
INSERT INTO exercises (name, muscle_group) VALUES ('Machine Chest Press', 'Chest');
INSERT INTO exercises (name, muscle_group) VALUES ('Incline Dumbbell Press', 'Chest');
INSERT INTO exercises (name, muscle_group) VALUES ('Low Incline Dumbbell Press', 'Chest');
INSERT INTO exercises (name, muscle_group) VALUES ('Smith Machine Row', 'Back');
INSERT INTO exercises (name, muscle_group) VALUES ('Deadlift', 'Back');
INSERT INTO exercises (name, muscle_group) VALUES ('Machine T-Bar Row', 'Back');
INSERT INTO exercises (name, muscle_group) VALUES ('Assisted Pull-up', 'Back');
INSERT INTO exercises (name, muscle_group) VALUES ('Chest Supported Row', 'Back');
INSERT INTO exercises (name, muscle_group) VALUES ('Freemotion Curl', 'Biceps');
INSERT INTO exercises (name, muscle_group) VALUES ('Leg Press', 'Quads');
INSERT INTO exercises (name, muscle_group) VALUES ('Calf Press Machine', 'Calves');
INSERT INTO exercises (name, muscle_group) VALUES ('Leg Press Calves', 'Calves');
