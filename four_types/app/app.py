from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app, multiprocess, CollectorRegistry, Counter, Info, Gauge, Histogram, Summary

app = FastAPI(debug=False)

c = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
g = Gauge('gauge_requests', 'Gauge')
h = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
s = Summary('http_request_summary_seconds', 'HTTP request summary', ['method', 'endpoint'])
Info('build_version', 'Build version').info({'version': '1.0.0'})


@app.get("/")
def read_root():
    c.labels('GET', '/', '200').inc()
    h.labels('GET', '/').observe(0.5)
    s.labels('GET', '/').observe(0.5)
    return {"Hello": "World"}

@app.get("/root")
def root():
    c.labels('GET', '/root', '200').inc()
    h.labels('GET', '/root').observe(1.5)
    s.labels('GET', '/root').observe(1.5)
    return {"Hello": "World"}


@app.get("/gauge/increase/{increase_by}")
def gauge_increase_by(increase_by: int):
    g.inc(increase_by)
    return increase_by

@app.get("/gauge/decrement/{decrement_by}")
def gauge_decrement_by(decrement_by: int):
    g.dec(decrement_by)
    return decrement_by

@app.get("/gauge/set/{set_by}")
def gauge_decrement_by(set_by: int):
    g.set(set_by)
    return set_by

@app.get("/fail")
def fail():
    c.labels('GET', '/fail', '500').inc()
    return HTTPException(status_code=500)

def make_metrics_app():
    registry = CollectorRegistry()
    return make_asgi_app(registry=registry)


metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
