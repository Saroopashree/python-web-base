# Python Fast API Boilerplate code

### Requirements
* python 3.9 or above

### How to run locally
1. Create a venv inside the project `python3 -m venv venv/`
1. Source the venv activation script `source venv/bin/activate`
1. Install all python dependencies `pip install -r requirements.txt`
1. Run the app using uvicorn `python3 -m uvicorn src.main:app --host 127.0.0.1 --port 8000`
1. In the browser go to `127.0.0.1:8000/docs` to view the Swagger docs
 
### How to run via Docker
1. Start the docker daemon
1. Perform `docker build --rm --pull -f "./Dockerfile" -t "pythonwebbase:latest"`. This step should build a docker image. Verify it by doing `docker images`
1. Now run the docker image by performing `docker run pythonwebbase`
1. Now the FastAPI server will be started inside the docker container. The port inside the container will be forwared to local port `8000`.
1. In the browser go to `127.0.0.1:8000/docs` to view the Swagger docs
