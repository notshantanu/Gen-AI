"""
FastAPI main application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, personalities, trades, parlays, ml

app = FastAPI(
    title="Aura Points API",
    description="Blockchain-based digital currency market for personality aura points",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(personalities.router)
app.include_router(trades.router)
app.include_router(parlays.router)
app.include_router(ml.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Aura Points API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

