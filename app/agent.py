import json

import requests

from schemas import TOOLS
from tools import get_pods, get_logs, describe_pod, get_events

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"
MAX_STEPS = 6

FUNCTIONS = {
    "get_pods": get_pods,
    "get_logs": get_logs,
    "describe_pod": describe_pod,
    "get_events": get_events,
}

SYSTEM_PROMPT = (
    "You are a Kubernetes troubleshooting assistant. You have exactly four tools: "
    "get_pods, get_logs, describe_pod, get_events. These only work on Pods and "
    "cluster Events — they cannot inspect ConfigMaps, Secrets, Services, Nodes, "
    "Deployments, or any other resource type. "
    "If the user asks about something these tools cannot provide, do NOT call a "
    "tool with a guessed or made-up name — instead, clearly say you don't have a "
    "tool for that and state exactly what information or tool would be needed. "
    "Only call a tool when you have a real, known pod name and namespace to use, "
    "for example one already seen in a prior tool result. Call one tool at a time. "
    "Once you have enough information, give a final plain-text answer explaining "
    "what's wrong and how to fix it."
)


def call_model(messages):
    r = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "stream": False,
        "messages": messages,
        "tools": TOOLS,
    }, timeout=120)
    r.raise_for_status()
    return r.json()["message"]


def run_agent(question):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(MAX_STEPS):
        message = call_model(messages)
        messages.append(message)

        tool_calls = message.get("tool_calls")
        if not tool_calls:
            return message["content"]

        for call in tool_calls:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            print(f"  [step {step+1}] calling {name}({args})")

            fn = FUNCTIONS.get(name)
            if fn is None:
                result = f"ERROR: unknown tool {name}"
            else:
                result = fn(**args)

            messages.append({
                "role": "tool",
                "content": result,
            })

    return "Stopped after max steps without a final answer."


if __name__ == "__main__":
    question = "show me the ConfigMap for this app"
    print(f"Question: {question}\n")
    answer = run_agent(question)
    print(f"\nFinal answer:\n{answer}")