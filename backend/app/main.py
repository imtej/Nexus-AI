"""
Nexus AI — FastAPI Main Application
Entry point for the backend server.
"""

import structlog
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.utils.logging import setup_logging
from app.api.routes import auth, chat, conversations, profile, evolution
from app.agents.graph import get_orchestration_graph
from app.agents.insight_distiller import run_insight_distillation_cycle
from app.agents.evolution_engine import run_personality_evolution_cycle
from app.agents.user_profiler import run_user_profiling_cycle

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    # Startup
    setup_logging()
    
    # Query database for true evolved version
    from app.services.supabase_client import get_supabase_admin
    db = get_supabase_admin()
    app_version = get_settings().app_version
    try:
        evolution_result = db.table("system_evolution").select("personality_version").eq("id", 1).single().execute()
        db_version = evolution_result.data.get("personality_version")
        if db_version:
            app_version = db_version
    except Exception:
        pass
        
    if app_version:
        logger.info("nexus_starting", version=app_version)
    else:
        logger.info("nexus_starting", version=get_settings().app_version)  
        
          
    # Pre-compile the LangGraph workflow
    get_orchestration_graph()
    logger.info("langgraph_workflow_compiled")

    # Native Background Task loops
    async def run_insight_distiller():
        await asyncio.sleep(10)  # Gentle 10s wait for full server boot
        while True:
            try:
                await run_insight_distillation_cycle()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("insight_distiller_loop_error", error=str(e))
            await asyncio.sleep(10 * 60)  # Sleep exactly 10 minutes

    async def run_evolution_engine():
        await asyncio.sleep(60)  # Gentle 1 min stagger so they don't fire exactly together
        while True:
            try:
                await run_personality_evolution_cycle()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("evolution_engine_loop_error", error=str(e))
            await asyncio.sleep(25 * 60)  # Sleep exactly 25 minutes

    async def run_user_profiler():
        await asyncio.sleep(30)  # Gentle 30s stagger
        while True:
            try:
                await run_user_profiling_cycle()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("user_profiler_loop_error", error=str(e))
            await asyncio.sleep(30 * 60)  # Sleep exactly 30 minutes

    curator_task = asyncio.create_task(run_insight_distiller())
    evolver_task = asyncio.create_task(run_evolution_engine())
    identity_task = asyncio.create_task(run_user_profiler())
    logger.info("background_schedules_started", insight_distiller="10m", evolution_engine="25m", user_profiler="30m")

    yield

    # Shutdown
    curator_task.cancel()
    evolver_task.cancel()
    identity_task.cancel()
    logger.info("nexus_shutting_down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Nexus AI — The Collective Knowledge Base. An evolving AI companion.",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(chat.router, prefix="/api/v1")
    app.include_router(conversations.router, prefix="/api/v1")
    app.include_router(profile.router, prefix="/api/v1")
    app.include_router(evolution.router, prefix="/api/v1")

    # Health check (for UptimeRobot)
    @app.get("/health")
    async def health_check():
        return {
            "status": "alive",
            "name": "Nexus AI",
            "version": settings.app_version,
        }

    @app.get("/warmup")
    async def warmup():
        get_orchestration_graph()
        return {"status": "warm"}

    return app


app = create_app()
