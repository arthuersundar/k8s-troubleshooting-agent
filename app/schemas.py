TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_pods",
            "description": "List pods and their status (Running, Pending, CrashLoopBackOff, etc.) and restart counts in a namespace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "Kubernetes namespace"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_logs",
            "description": "Get recent logs for a specific pod.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pod": {"type": "string", "description": "Pod name"},
                    "namespace": {"type": "string"},
                    "tail": {"type": "integer", "description": "Number of log lines to fetch"}
                },
                "required": ["pod"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "describe_pod",
            "description": "Get full describe output for a pod, including events like ImagePullBackOff, OOMKilled, failed mounts, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pod": {"type": "string", "description": "Pod name"},
                    "namespace": {"type": "string"}
                },
                "required": ["pod"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_events",
            "description": "Get recent cluster events for a namespace, useful for spotting scheduling or pulling failures.",
            "parameters": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                },
                "required": []
            }
        }
    },
]