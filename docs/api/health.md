# Health Endpoints

No auth required.

## GET /health

Liveness probe.

```json
{ "status": "ok" }
```

## GET /ready

Readiness probe (dependencies ready).

```json
{ "status": "ready" }
```

Used by Docker HEALTHCHECK and Kubernetes probes.
