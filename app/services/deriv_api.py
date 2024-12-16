import os
import json
import asyncio
import websockets
import aiohttp
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class DerivAPI:
    def __init__(self):
        self.app_id = os.getenv('DERIV_APP_ID', '1089')  # Using default app_id for testing
        self.api_url = "wss://ws.binaryws.com/websockets/v3?app_id={}".format(self.app_id)
        self.session = None
        self.websocket = None

    async def connect(self):
        """Establish WebSocket connection to Deriv API"""
        try:
            self.websocket = await websockets.connect(self.api_url)
            return {"status": "connected"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_available_symbols(self) -> Dict[str, Any]:
        """Get list of available trading symbols"""
        if not self.websocket:
            await self.connect()
        
        request = {
            "active_symbols": "brief",
            "product_type": "basic"
        }
        
        try:
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            return json.loads(response)
        except Exception as e:
            return {"error": str(e)}

    async def get_ticks(self, symbol: str) -> Dict[str, Any]:
        """Get latest ticks for a symbol"""
        if not self.websocket:
            await self.connect()
        
        request = {
            "ticks": symbol
        }
        
        try:
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            return json.loads(response)
        except Exception as e:
            return {"error": str(e)}

    async def get_candles(self, symbol: str, interval: str = "60", count: int = 1000) -> Dict[str, Any]:
        """Get historical candles for a symbol"""
        if not self.websocket:
            await self.connect()
        
        request = {
            "ticks_history": symbol,
            "style": "candles",
            "granularity": interval,
            "count": count
        }
        
        try:
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            return json.loads(response)
        except Exception as e:
            return {"error": str(e)}

    async def close(self):
        """Close WebSocket connection"""
        if self.websocket:
            await self.websocket.close()
