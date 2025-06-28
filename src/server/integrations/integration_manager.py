import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
import aiohttp

class IntegrationType(Enum):
    DEEPSEEK = "deepseek"
    OPENWEBUI = "openwebui"

@dataclass
class IntegrationResult:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class IntegrationManager:
    def __init__(self, api_key: str = None):
        self.logger = logging.getLogger("integration_manager")
        self._setup_logger()
        self.api_key = api_key
        self.webui_session = None
        
    def _setup_logger(self):
        """Configure logging"""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    async def initialize(self):
        """
        Initialize integrations
        
        Returns:
            IntegrationResult indicating success/failure
            
        Raises:
            ValueError: If API key is not provided
        """
        try:
            if not self.api_key:
                raise ValueError("API key required for integrations")
            
            # Close existing session if any
            await self.close()
            
            # Initialize aiohttp session for WebUI communication
            self.webui_session = aiohttp.ClientSession()
            self.logger.info("Integrations initialized successfully")
            
            return IntegrationResult(success=True)
            
        except ValueError as ve:
            self.logger.error(f"Initialization failed: {str(ve)}")
            return IntegrationResult(success=False, error=str(ve))
        except Exception as e:
            self.logger.error(f"Failed to initialize integrations: {str(e)}")
            return IntegrationResult(success=False, error=str(e))

    async def close(self):
        """Cleanup integration resources"""
        try:
            if self.webui_session:
                await self.webui_session.close()
                self.webui_session = None
            self.logger.info("Integration resources cleaned up")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")
            raise RuntimeError(f"Failed to cleanup resources: {str(e)}")

    async def analyze_with_deepseek(self, data: Dict[str, Any]) -> IntegrationResult:
        """Analyze data using Deepseek API"""
        try:
            if not self.api_key:
                raise ValueError("Deepseek API key not configured")

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare analysis request
            request_data = {
                "model": "deepseek-reasoner",
                "max_tokens": 256,
                "messages": [
                    {
                        "role": "system",
                        "content": "Analyze this SQL query or vulnerability data"
                    },
                    {
                        "role": "user",
                        "content": json.dumps(data)
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers=headers,
                    json=request_data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return IntegrationResult(
                            success=False,
                            error=f"Deepseek API error: {error_text}"
                        )
                    
                    result = await response.json()
                    return IntegrationResult(success=True, data=result)
                    
        except Exception as e:
            self.logger.error(f"Deepseek analysis failed: {str(e)}")
            return IntegrationResult(success=False, error=str(e))

    async def analyze_vulnerability(self, data: Dict[str, Any]) -> IntegrationResult:
        """Analyze vulnerability using Deepseek"""
        try:
            result = await self.analyze_with_deepseek({
                "type": "vulnerability_analysis",
                "data": data
            })
            
            if not result.success:
                return IntegrationResult(success=False, error=result.error)
                
            return IntegrationResult(success=True, data=result.data)
            
        except Exception as e:
            return IntegrationResult(success=False, error=str(e))

    async def analyze_payload(self, payload: str) -> IntegrationResult:
        """Analyze SQL injection payload using Deepseek"""
        try:
            result = await self.analyze_with_deepseek({
                "type": "payload_analysis",
                "payload": payload
            })
            
            if not result.success:
                return IntegrationResult(success=False, error=result.error)
                
            return IntegrationResult(success=True, data=result.data)
            
        except Exception as e:
            return IntegrationResult(success=False, error=str(e))

    async def analyze_waf_bypass(self, data: Dict[str, Any]) -> IntegrationResult:
        """Analyze WAF bypass techniques using Deepseek"""
        try:
            result = await self.analyze_with_deepseek({
                "type": "waf_bypass_analysis",
                "data": data
            })
            
            if not result.success:
                return IntegrationResult(success=False, error=result.error)
                
            return IntegrationResult(success=True, data=result.data)
            
        except Exception as e:
            return IntegrationResult(success=False, error=str(e))

    async def update_webui(self, data: Dict[str, Any]) -> IntegrationResult:
        """Send updates to Open WebUI"""
        try:
            if not self.webui_session:
                raise RuntimeError("WebUI session not initialized")

            # Send update to WebUI
            async with self.webui_session.post(
                "http://172.245.232.168:3000/api/update",
                json=data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return IntegrationResult(success=True, data=result)
                else:
                    error = await response.text()
                    return IntegrationResult(
                        success=False,
                        error=f"WebUI update failed: {error}"
                    )
                    
        except Exception as e:
            return IntegrationResult(
                success=False,
                error=f"Failed to update WebUI: {str(e)}"
            )

    async def close(self):
        """
        Cleanup integration resources
        
        This method should be called when the integration manager is no longer needed
        to properly close any open sessions and cleanup resources.
        """
        try:
            if self.webui_session:
                await self.webui_session.close()
                self.webui_session = None
            self.logger.info("Integration resources cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")
            raise RuntimeError(f"Failed to cleanup resources: {str(e)}")
            
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    def get_available_integrations(self) -> List[str]:
        """Return list of available integrations"""
        return [integration.value for integration in IntegrationType]
