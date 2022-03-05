# Python Fast API Boilerplate code

## Requirements

- python 3.9 or above

## How to run locally

1. Create a venv inside the project `python3 -m venv venv/`
1. Source the venv activation script `source venv/bin/activate`
1. Install all python dependencies `pip install -r requirements.txt`
1. Run the app using uvicorn `python3 -m uvicorn src.main:app --host 127.0.0.1 --port 8000`
1. In the browser go to `127.0.0.1:8000/docs` to view the Swagger docs

---

## How to run via Docker

### Using docker-compose

This is the recommended method as the container, network and volume configurations are provided once. And the application can be started and stopped by just single commands.

1. Perform `docker-compose up`. Wait for the application to startup. You can check the logs to verify this.
1. Go to `127.0.0.1:8000/docs` to view the Swagger docs.
1. If you make any changes to the code, you need to perform `docker-compose down` and then `docker-compose up --build` to build the docker image with new changes and to up the application.
1. If the containerized application is not required anymore do `docker-compose down` to bring down the container.

> **Note:** `docker-compose down` will not delete the volume that was attached to the `mysqldb` container. This is not a bug, but a well thought feature. By not deleting the volume, the volume will be reused when the application is started again. And you won't lose any data stored in the database. If you want to delete the volume, you can do it by running `docker volume rm <volume_name>`

---

### Not using docker-compose

The docker image, network, volume and containers have to created manually by separate commands in this method.

1. `docker pull mysql:latest`
1. `docker network create --driver bridge app-network`
1. `docker volume create db-data`
1. `docker run -dit --name mysqldb --network app-network --volume db-data:/var/lib/mysql --publish 3306:3306 --restart always --platform linux/x86_64 --env MYSQL_DATABASE=dev --env MYSQL_USER=admin --env MYSQL_ROOT_PASSWORD=<provide-root-password-here> --env MYSQL_PASSWORD=<provide-password-here> mysql:latest`
1. `docker build -t=pythonwebbase .`
1. `docker run -dit --name app --network app-network --publish 8000:8000 --env MYSQL_DATABASE=dev --env MYSQL_USER=admin --env MYSQL_PASSWORD=<provider-password-here> pythonwebbase:latest`
1. Now go to `127.0.0.1:8000/docs` to view the Swagger docs.

#### To stop the containarized application

1. Perform `docker stop app && docker rm app` to stop and destroy the `app` container. Similarly, for the `mysqldb` container, do `docker stop mysqldb && docker rm mysqldb`.
1. To remove the network `docker network rm app-network`.
1. Finally remove the created volume by doing `docker volume rm db_data`.
