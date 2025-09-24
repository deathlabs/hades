## `hades`
To develop HADES locally, you will need to setup a few terminal windows as described below. 
* [`rabbitmq`](#rabbitmq)
* [`backend`](#backend)
* [`frontend-proxy`](#frontend-proxy)
* [`frontend`](#frontend)

### `rabbitmq`
Open a new terminal window and enter the commands below.
```bash
make DOCKER_COMPOSE_PROFILE=rabbitmq start
```

### `backend`
Replace `""` in the command below with your `OPENAI_API_KEY` and then, copy the command to a new terminal window.
```bash
export OPENAI_API_KEY=""
```

In the same terminal window, enter the commands below.
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt 
export RABBITMQ_BROKER_ADDRESS="127.0.0.1"
export RABBITMQ_BROKER_PORT="5672" 
export RABBITMQ_USERNAME="hades"
export RABBITMQ_PASSWORD="hades"
python -m hades.main server
```

### `frontend`
Open a new terminal window and enter the commands below.
```bash
cd frontend/hades
npm install
npm run dev
```