import os
import time
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response 
from starlette.responses import Response as StarletteResponse


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
APP_NAME = os.getenv("APP_NAME", "k8s-argocd-demo")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "Hello from Kubernetes!")
FAIL_RATE = float(os.getenv("FAIL_RATE", "0.0"))  # 0.0 - 1.0

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(APP_NAME)

app = FastAPI(title=APP_NAME)

REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["path"])
START_TIME = time.time()

def maybe_fail():
    # En enkel “feil-injeksjon” for å se readiness/metrics oppføre seg
    # (kontrollert med FAIL_RATE)
    if FAIL_RATE <= 0:
        return
    # deterministic-ish: “feil” i korte pulser
    if int(time.time()) % 10 < int(10 * FAIL_RATE):
        raise HTTPException(status_code=503, detail="Injected failure")

@app.middleware("http")
async def metrics_middleware(request, call_next):
    path = request.url.path
    method = request.method
    start = time.time()
    status_code = 500
    try:
        resp: StarletteResponse = await call_next(request)
        status_code = resp.status_code
        return resp
    finally:
        duration = time.time() - start
        LATENCY.labels(path=path).observe(duration)
        REQUESTS.labels(method=method, path=path, status=str(status_code)).inc()

@app.get("/healthz")
def healthz():
    return {"status": "ok", "app": APP_NAME, "env": ENVIRONMENT}

@app.get("/readyz")
def readyz():
    maybe_fail()
    return {"status": "ready", "app": APP_NAME, "env": ENVIRONMENT}

@app.get("/")
def root():
    uptime = round(time.time() - START_TIME, 2)
    return {
        "app": APP_NAME,
        "env": ENVIRONMENT,
        "message": WELCOME_MESSAGE,
        "uptime_seconds": uptime,
    }

@app.get("/work")
def work(ms: Optional[int] = 50):
    """
    Simuler litt “arbeid” så vi ser latency i metrics.
    """
    ms = max(0, min(ms or 0, 2000))
    time.sleep(ms / 1000.0)
    return {"slept_ms": ms}

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
