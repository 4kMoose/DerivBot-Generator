from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="DBot Strategy Generator",
             description="A platform for generating and optimizing trading strategies")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Import routers
from app.api import strategy, backtest, optimization, auth

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(strategy.router, prefix="/strategy", tags=["Strategy"])
app.include_router(backtest.router, prefix="/backtest", tags=["Backtesting"])
app.include_router(optimization.router, prefix="/optimization", tags=["Optimization"])

@app.get("/")
async def root():
    return {"message": "Welcome to DBot Strategy Generator API"}
