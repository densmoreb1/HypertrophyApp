# Hypertrophy App

## High Level Goal

- Web app that tracks workouts
- Docker container
- 5 or 6 week meso cycles
- Feedback on each mucsle group
    - Soreness from last time
    - Pump
    - Workload
- Add sets, weights, and reps each week
    - Only adds sets if the feedback meets the criteria
- Able to see how many sets per muscle group in a meso cycle
- Able to see how many sets per muscle group all time
- Graph to see progression of exercises

<<<<<<< HEAD
=======
## Design Research

### Research into different options

- Streamlit
    - Best option
    - No HTML , all markdown and python
- Flask
    - HTMl and all paths
- Django
    - HTMl and all paths

### Environment

- Make conda env
    conda env create hype
- Install dependencies

### Design the Database

- Meso table
- Exercises table
- Users 
- Workout table

### Create the database

- Using mysql
    - Docker command
        - `docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=rootpassword -d -p 3306:3306 mysql:latest`
- Finding the IP of the docker container
    - `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id`
- When creating on machine, use the service name in the docker compose file for address

## TODO

- Insert in all exercises
    - Include in a sql script
- Create a way to insert new exercises
    - A page with text boxes
- Create the create meso cycle page
    - Pull from the database
    - Button at the end to save meso to the database
- Design what the meso table will be inserting
- Create some kinda of text to show if the meso was created
- Design what the current workout will be pulling from


>>>>>>> 930d56e (adding readme)
