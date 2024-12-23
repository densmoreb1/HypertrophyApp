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
	meso_id int,
	name varchar(100),
	user_id int,
	completed int,
	set_id int,
	reps int,
	weight numeric(15, 1),
	order_id int,
	exercise_id int,
	day_id int,
	week_id int,
	date_created datetime,
	date_completed datetime,
	foreign key (user_id) references users(id),
	foreign key (exercise_id) references exercises(id),
	unique (meso_id, name, user_id, exercise_id, day_id, week_id, set_id)
);

create table if not exists ranking (
	id int auto_increment primary key,
	sorness int,
	pump int
);

INSERT INTO users (name) VALUES ('brandon');
INSERT INTO users (name) VALUES ('ivy');

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
insert into exercises (name, muscle_group) values ('incline bench press','chest');
insert into exercises (name, muscle_group) values ('pec dec','chest');
insert into exercises (name, muscle_group) values ('machine chest press','chest');
insert into exercises (name, muscle_group) values ('incline dumbbell press','chest');
insert into exercises (name, muscle_group) values ('low incline dumbbell press','chest');
insert into exercises (name, muscle_group) values ('smith machine row','back');
insert into exercises (name, muscle_group) values ('deadlift','back');
insert into exercises (name, muscle_group) values ('machine t-bar row','back');
insert into exercises (name, muscle_group) values ('assisted pull-up','back');
insert into exercises (name, muscle_group) values ('chest supported row','back');
insert into exercises (name, muscle_group) values ('freemotion curl','biceps');
insert into exercises (name, muscle_group) values ('leg press','quads');
insert into exercises (name, muscle_group) values ('calf press machine','calves');
insert into exercises (name, muscle_group) values ('leg press calves','calves');
insert into exercises (name, muscle_group) values ('machine lateral raise','shoulders');
insert into exercises (name, muscle_group) values ('cable tricep pushdown','triceps');
insert into exercises (name, muscle_group) values ('machine preacher curl','biceps');
insert into exercises (name, muscle_group) values ('straight arm pulldown','back');
insert into exercises (name, muscle_group) values ('barbell skullcrusher','triceps');
insert into exercises (name, muscle_group) values ('machine crunch','abs');
insert into exercises (name, muscle_group) values ('leg extension','quads');
insert into exercises (name, muscle_group) values ('cross body cable lateral raise','shoulders');
insert into exercises (name, muscle_group) values ('single arm tricep pushdown','triceps');
insert into exercises (name, muscle_group) values ('incline dumbbell curl','biceps');
insert into exercises (name, muscle_group) values ('lying leg raise','abs');
insert into exercises (name, muscle_group) values ('ez bar preacher curl','biceps');
insert into exercises (name, muscle_group) values ('cable overhead extension','triceps');
insert into exercises (name, muscle_group) values ('dumbbell lateral raise','shoulders');
insert into exercises (name, muscle_group) values ('back raise','hamstrings');
insert into exercises (name, muscle_group) values ('barbell squat','quads');
insert into exercises (name, muscle_group) values ('walking lunges','quads');
insert into exercises (name, muscle_group) values ('sissy squat','quads');

--select concat(
--	'insert into exercises (name, muscle_group) values (',
--	'''',
--	name,
--	'''',
--	',',
--	'''',
--	muscle_group,
--	'''',
--	');'
--	)
--from fitness.exercises;
