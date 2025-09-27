from fastapi import FastAPI

from ..config import settings
from ..logging import setup_logging
from .routes import health as health_router
from .routes import resume as resume_router

# Initialize logging and settings
setup_logging(level=settings.LOG_LEVEL)

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Matrix Guardian AI Control Plane"
)

# Include API routers
app.include_router(health_router.router, tags=["Health"])
app.include_router(resume_router.router, tags=["Workflows"])

@app.on_event("startup")
async def startup_event():
    # Placeholder for startup logic, e.g., connecting to a message queue
    pass

# >>> AUTOPILOT: include router (feature-flagged)
try:
    from ..autopilot_settings import AutopilotSettings
    _ap_cfg = AutopilotSettings()
    if _ap_cfg.api_enabled:
        from .routes import autopilot as autopilot_router
        app.include_router(autopilot_router.router, tags=["Autopilot"])
except Exception as _e:
    # log only if you want: print(f"Autopilot router not loaded: {_e}")
    pass
# <<< AUTOPILOT: include router (feature-flagged)
