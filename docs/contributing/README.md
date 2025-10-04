## `hades`
If you want to develop and/or contribute to `hades`, follow the instructions below in the order they are listed (again, these instructions assume you already have `git`, `make`, and `docker` installed as well as a valid OpenAI API key).
* [Setting up the `rabbitmq` Microservice](#setting-up-the-rabbitmq-microservice)
* [Setting Up a Local Development Environment to Contribute to the `backend` Microservice](#setting-up-a-local-development-environment-to-contribute-to-the-backend-microservice)
* [Setting Up a Local Development Environment to Contribute to the `frontend` Microservice](#setting-up-a-local-development-environment-to-contribute-to-the-frontend-microservice)

### Setting Up the `rabbitmq` Microservice
Open a terminal window and enter the commands below.
```bash
make DOCKER_COMPOSE_PROFILE=rabbitmq start
```

### Setting Up a Local Development Environment to Contribute to the `backend` Microservice
Open a _new_ terminal window, replace the `sk-...` string in the command below with a valid OpenAI API key, and then, paste the command in your second terminal window (not the one running the `rabbitmq` container). 
```bash
export OPENAI_API_KEY="sk-..."
```

In the same terminal window, enter the commands below (from the root of the project directory).
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt 
export RABBITMQ_ADDRESS="localhost"
export RABBITMQ_PASSWORD="hades"
export RABBITMQ_PORT=5672
export RABBITMQ_REPORT_EXCHANGE_NAME="hades.injects.reports"
export RABBITMQ_USERNAME="hades"
uvicorn hades.main:api --host 0.0.0.0 --port 8888
```

### Setting Up a Local Development Environment to Contribute to the `frontend` Microservice
Open a _new_ terminal window and enter the commands below (again, from the root of the project directory).
```bash
cd frontend/hades
npm install
npm run dev
```
