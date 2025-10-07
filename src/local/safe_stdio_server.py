# stdio_server_secure.py
from mcp.server.fastmcp import FastMCP
from typing import Annotated
import time
import threading

app = FastMCP("Calculator")   # stdio only; no network surface

# --- Tunables / “controls you can remove” for experiments ---
MAX_ABS = 1_000_000           # bound big ints to avoid CPU blowups
RATE_LIMIT = 10               # max calls per 10s (crude local DoS guard)
WINDOW_SEC = 10
TOOL_TIMEOUT_SEC = 2          # per-call budget

# Simple in-proc rate limiter (per server process)
_call_times = []
_lock = threading.Lock()

def _rate_limit():
    now = time.time()
    with _lock:
        # drop old entries
        while _call_times and now - _call_times[0] > WINDOW_SEC:
            _call_times.pop(0)
        if len(_call_times) >= RATE_LIMIT:
            raise RuntimeError("Too many requests; slow down.")
        _call_times.append(now)

# Simple per-call timeout (cross-platform safe enough for CPU-bound ops)
def _run_with_timeout(fn, *args, timeout=TOOL_TIMEOUT_SEC):
    result = {}
    exc = {}

    def _target():
        try:
            result["v"] = fn(*args)
        except Exception as e:
            exc["e"] = e

    t = threading.Thread(target=_target, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        raise TimeoutError("Tool execution exceeded time limit.")
    if "e" in exc:
        raise exc["e"]
    return result.get("v")

def _as_int(x, name):
    if not isinstance(x, int):
        raise ValueError(f"{name} must be an integer")
    if abs(x) > MAX_ABS:
        raise ValueError(f"{name} out of allowed range")
    return x

def _guarded(op, a, b):
    _rate_limit()
    a = _as_int(a, "a"); b = _as_int(b, "b")
    return _run_with_timeout(op, a, b)

@app.tool()
def add(a: Annotated[int, "int | bounded"], b: Annotated[int, "int | bounded"]) -> int:
    return _guarded(lambda x, y: x + y, a, b)

@app.tool()
def multiply(a: Annotated[int, "int | bounded"], b: Annotated[int, "int | bounded"]) -> int:
    return _guarded(lambda x, y: x * y, a, b)

if __name__ == "__main__":
    # stdio is right for “local server” threat model
    app.run(transport="stdio")
