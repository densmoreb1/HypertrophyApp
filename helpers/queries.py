exercise_query = '''
select distinct e.name, e.id, m.order_id
from mesos m
inner join exercises e
    on m.exercise_id = e.id
where m.day_id = %s and m.week_id = %s and m.name = %s
order by m.order_id
'''

workout_query = '''
select m.set_id, m.reps, m.weight, m.completed, m.order_id
from mesos m
inner join exercises e
    on m.exercise_id = e.id
where m.day_id = %s and m.week_id = %s and exercise_id = %s
and m.name = %s
'''

update_set_query = '''
update mesos
set reps = %s
, weight = %s
, completed = 1
, date_completed = now()
where set_id = %s and day_id = %s and week_id = %s and exercise_id = %s
and name = %s
'''

add_set_query = '''
insert into fitness.mesos
(meso_id, name, user_id, completed, set_id, reps, weight, order_id
, exercise_id, day_id, week_id, date_created)
values (%s, %s, %s, 0, %s, %s, %s, %s, %s, %s, %s, now())
'''
