from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.core.strategy_generator import StrategyGenerator
from app.models.strategy import Strategy, StrategyInput

router = APIRouter()

class StrategyRequest(BaseModel):
    risk_tolerance: float
    trading_session: str
    asset_class: str
    timeframe: str
    indicators: List[str]
    optimization_criteria: Optional[dict] = None

@router.post("/generate")
async def generate_strategy(request: StrategyRequest):
    """Generate a new trading strategy based on user inputs"""
    try:
        generator = StrategyGenerator()
        strategy = generator.create_strategy(
            risk_tolerance=request.risk_tolerance,
            trading_session=request.trading_session,
            asset_class=request.asset_class,
            timeframe=request.timeframe,
            indicators=request.indicators
        )
        return strategy
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate")
async def validate_strategy(strategy_id: int):
    """Validate a strategy using Monte Carlo simulation"""
    try:
        generator = StrategyGenerator()
        validation_results = generator.validate_strategy(strategy_id)
        return validation_results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/deploy")
async def deploy_strategy(strategy_id: int):
    """Deploy a strategy to Deriv's DBot platform"""
    try:
        generator = StrategyGenerator()
        deployment_result = generator.deploy_strategy(strategy_id)
        return deployment_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
