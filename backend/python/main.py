from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.user_api import user_api_router
from api.login_api import login_api_router
from core.bootstrap import startup_event_handler, shutdown_event_handler
from core.logger import Logger

logger = Logger.get_logger(__name__)

# Create FastAPI app instance
logger.info("Initializing FastAPI application.")
app = FastAPI()

# Add CORS middleware
logger.info("Adding CORS middleware.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
logger.info("Including user API router.")
app.include_router(user_api_router, prefix="/api/v1")
logger.info("Including login API router.")
app.include_router(login_api_router, prefix="/api/v1")

# Add event handlers
logger.info("Adding startup and shutdown event handlers.")
app.add_event_handler("startup", startup_event_handler)
app.add_event_handler("shutdown", shutdown_event_handler)

logger.info("FastAPI application setup completed.")