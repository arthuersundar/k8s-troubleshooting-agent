import requests
from schemas import TOOLS

r = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.2:3b",
    "stream": False,
    "messages": [{"role": "user", "content": "What pods are running in the default namespace?"}],
    "tools": TOOLS,
})
print(r.json()["message"])