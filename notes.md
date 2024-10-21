# Hypertrophy App

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
    - `docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=rootpassword -d -p 3306:3306 mysql:latest`
- Finding the IP of the docker container
    - `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id`
- When creating on machine, use the service name in the docker compose file for address
- Volumes in docker go to /var/lib/docker/volumes

### Docker Compose

- `docker compose up -d`
    - starts the containers detached from the terminal
- `docker compose logs`
- `docker compose start` and `stop`
- `docker compose down`
    - stops and deletes the containers
    - adding -v deletes the volumes

