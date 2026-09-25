import json
import subprocess

ALLOWED_NAMESPACES = None  # None = no restriction; set e.g. {"default", "kube-system"} to lock it down


def _run_kubectl(args):
    """Run kubectl with a fixed set of args. Never accepts a raw shell string."""
    result = subprocess.run(
        ["kubectl"] + args,
        capture_output=True, text=True, timeout=15,
    )
    if result.returncode != 0:
        return f"ERROR: {result.stderr.strip()}"
    return result.stdout


def get_pods(namespace: str = "default") -> str:
    """List pods and their status in a namespace."""
    out = _run_kubectl(["get", "pods", "-n", namespace, "-o", "json"])
    if out.startswith("ERROR"):
        return out
    data = json.loads(out)
    pods = [
        {
            "name": p["metadata"]["name"],
            "status": p["status"].get("phase"),
            "restarts": sum(c.get("restartCount", 0) for c in p["status"].get("containerStatuses", [])),
        }
        for p in data.get("items", [])
    ]
    return json.dumps(pods)


def get_logs(pod: str, namespace: str = "default", tail: int = 50) -> str:
    """Get the last N lines of logs for a pod."""
    return _run_kubectl(["logs", pod, "-n", namespace, f"--tail={tail}"])


def describe_pod(pod: str, namespace: str = "default") -> str:
    """Get full describe output for a pod (events, conditions, etc.)."""
    return _run_kubectl(["describe", "pod", pod, "-n", namespace])


def get_events(namespace: str = "default") -> str:
    """Get recent cluster events in a namespace."""
    return _run_kubectl(["get", "events", "-n", namespace, "--sort-by=.lastTimestamp"])