import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.components.database import Database
from app.components.embedder import Embedder
from app.components.generator import Generator
from app.components.retriever import Retriever
from app.config.configuration import ConfigurationManager
from app.dependencies import limiter
from app.pipeline.ingestion import IngestionPipeline
from app.pipeline.query import QueryPipeline
from app.router import documents, feedback, health, ingest, query
from core.logger import get_logger

log = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("server_starting")
    cm = ConfigurationManager()

    embedder = Embedder(cm.get_embedder_config().model_name)
    retriever = Retriever(cm.get_qdrant_config())

    nv_cfg = cm.get_nvidia_config()
    groq_cfg = cm.get_groq_config()
    has_key = nv_cfg.api_key or groq_cfg.api_key
    generation = Generator(nvidia=nv_cfg, groq=groq_cfg) if has_key else None
    database = Database(cm.get_postgres_config())
    await database.connect()

    ing_pipeline = IngestionPipeline(
        embedder,
        retriever,
        database,
        cm.get_redpanda_config(),
        cm.get_chunker_config(),
    )
    q_pipeline = (
        QueryPipeline(
            embedder,
            retriever,
            database,
            generation,
            cm.get_inference_config(),
        )
        if generation
        else None
    )

    app.state.cm = cm
    app.state.embedder = embedder
    app.state.retriever = retriever
    app.state.generation = generation
    app.state.database = database
    app.state.ingestion = ing_pipeline
    app.state.query = q_pipeline

    consumer_task = asyncio.create_task(ing_pipeline.run_consumer())

    if generation:
        log.info("llm_ready: %s", generation.model)
    else:
        log.warning("no LLM API key set — query endpoint disabled")

    log.info("server_ready")
    yield
    consumer_task.cancel()
    await database.close()
    log.info("server_shutdown")


app = FastAPI(
    title="LibraryRAG API",
    description="Real-Time AI Librarian — RAG pipeline for campus library",
    version="0.1.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

_cors = os.environ.get("CORS_ORIGINS", "")
if _cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in _cors.split(",")],
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["X-API-Key", "Content-Type"],
    )

@app.get("/metrics")
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(health.router)
app.include_router(query.router)
app.include_router(ingest.router)
app.include_router(documents.router)
app.include_router(feedback.router)
