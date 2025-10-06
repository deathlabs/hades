## How the `llama` microservice was Initialized Locally
The steps below describe how the `llama` service was initialized locally before it was containerized.

**Step 1.** Create a folder called `llama` and change directories to it. 
```bash
mkdir llama
```

**Step 2.** Create a Python virtual environment.
```bash
python -m venv .venv
```

**Step 2.** Activate the Python virtual environment you just created.
```bash
source .venv/bin/activate
```

**Step 3.** Install the Python dependencies.
```bash
pip install -r requirements.txt 
```

**Step 4.** Download a model.
```bash
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q6_K.gguf
```

**Step 5.** Create a folder called `hades`.  
```bash
mkdir hades
```

**Step 6.** Create two files in the folder you just created: `__init__.py` and `main.py`. Then, add the following content to `main.py`.
```python
# Code goes here.
```

**Step 7.** Start the `llama` microservice.
```bash
uvicorn hades.main:api --host 0.0.0.0 --port 9999
```
