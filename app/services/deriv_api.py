import os
import json
import asyncio
import websockets
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class DerivAPI:
    def __init__(self):
        self.app_id = os.getenv('DERIV_APP_ID')
        self.api_token = os.getenv('DERIV_API_TOKEN')
        self.api_url = "wss://ws.binaryws.com/websockets/v3"
        self.websocket = None

    async def connect(self):
        """Establish WebSocket connection to Deriv API"""
        self.websocket = await websockets.connect(self.api_url)
        
        # Authorize connection
        auth_request = {
            "authorize": self.api_token,
            "app_id": self.app_id
        }
        await self.websocket.send(json.dumps(auth_request))
        response = await self.websocket.recv()
        return json.loads(response)

    async def get_available_symbols(self) -> Dict[str, Any]:
        """Get list of available trading symbols"""
        request = {
            "active_symbols": "brief",
            "product_type": "basic"
        }
        await self.websocket.send(json.dumps(request))
        response = await self.websocket.recv()
        return json.loads(response)

    async def get_candles(self, symbol: str, interval: str, count: int = 1000) -> Dict[str, Any]:
        """Get historical candles for a symbol"""
        request = {
            "ticks_history": symbol,
            "style": "candles",
            "granularity": interval,
            "count": count
        }
        await self.websocket.send(json.dumps(request))
        response = await self.websocket.recv()
        return json.loads(response)

    async def create_contract(self, contract_type: str, symbol: str, duration: int, 
                            duration_unit: str, amount: float) -> Dict[str, Any]:
        """Create a new contract"""
        request = {
            "proposal": 1,
            "contract_type": contract_type,
            "symbol": symbol,
            "duration": duration,
            "duration_unit": duration_unit,
            "amount": amount,
            "basis": "stake",
            "currency": "USD"
        }
        await self.websocket.send(json.dumps(request))
        response = await self.websocket.recv()
        return json.loads(response)

    async def buy_contract(self, proposal_id: str, price: float) -> Dict[str, Any]:
        """Buy a contract"""
        request = {
            "buy": proposal_id,
            "price": price
        }
        await self.websocket.send(json.dumps(request))
        response = await self.websocket.recv()
        return json.loads(response)

    async def deploy_strategy(self, strategy_code: str) -> Dict[str, Any]:
        """Deploy a strategy to DBot"""
        # This is a placeholder for the actual DBot deployment
        # Implementation will depend on DBot's API specifications
        request = {
            "dbot": {
                "strategy": strategy_code,
                "action": "deploy"
            }
        }
        await self.websocket.send(json.dumps(request))
        response = await self.websocket.recv()
        return json.loads(response)

    async def close(self):
        """Close WebSocket connection"""
        if self.websocket:
            await self.websocket.close()
