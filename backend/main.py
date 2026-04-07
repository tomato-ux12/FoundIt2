from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes_auth import router as auth_router
from routes_opportunities import router as opportunities_router
from routes_tests import router as tests_router
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Idea Validator API",
    description="Validation Engine for Freelance SaaS Ideas",
    version="0.1.0",
)

# ===== MIDDLEWARE =====

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip compression

# ===== ROUTES =====

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Idea Validator API",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


# Include routers
app.include_router(auth_router)
app.include_router(opportunities_router)
app.include_router(tests_router)

# ===== ERROR HANDLERS =====

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"General error: {exc}")
    return {
        "error": "Internal server error",
        "detail": str(exc) if settings.ENVIRONMENT == "development" else "Server error"
    }


# ===== STARTUP/SHUTDOWN =====

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting up... Environment: {settings.ENVIRONMENT}")
    logger.info(f"CORS origins: {settings.cors_origins_list}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False,
    )
