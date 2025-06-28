import os
import sys
import logging
import subprocess
from typing import Dict, Any
from fastapi import FastAPI, HTTPException

class MCPServer:
    def __init__(self):
        self.app = FastAPI(title="Advanced MCP SQLMap Server")
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Configure logging for the MCP server"""
        logger = logging.getLogger("mcp_server")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _execute_sqlmap_command(self, target_url: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Execute SQLMap command using subprocess"""
        try:
            cmd = ["sqlmap"]
            cmd.extend(["-u", target_url])
            
            # Add options to command
            for key, value in options.items():
                if isinstance(value, bool):
                    if value:
                        cmd.append(f"--{key}")
                else:
                    cmd.extend([f"--{key}", str(value)])
            
            # Run SQLMap
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"SQLMap execution failed: {stderr}")
            
            return {
                "status": "success",
                "output": stdout,
                "command": " ".join(cmd)
            }
            
        except Exception as e:
            self.logger.error(f"SQLMap execution error: {str(e)}")
            raise RuntimeError(f"SQLMap execution failed: {str(e)}")

    async def start_scan(self, target_url: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new SQLMap scan"""
        try:
            self.logger.info(f"Starting scan for target: {target_url}")
            
            # Validate URL
            if not target_url.startswith(("http://", "https://")):
                raise ValueError("Invalid URL format. Must start with http:// or https://")
            
            # Execute SQLMap
            result = self._execute_sqlmap_command(target_url, options)
            
            return {
                "status": "scan_started",
                "target": target_url,
                "options": options,
                "sqlmap_result": result
            }
            
        except ValueError as e:
            self.logger.error(f"Validation error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            self.logger.error(f"Scan failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def analyze_with_deepseek(self, query: str, api_key: str) -> Dict[str, Any]:
        """Analyze SQL query using Deepseek API"""
        try:
            import aiohttp
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-sql",
                "messages": [
                    {
                        "role": "system",
                        "content": "Analyze this SQL query for potential vulnerabilities"
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(f"Deepseek API error: {error_text}")
                    
                    result = await response.json()
                    return result
                    
        except Exception as e:
            self.logger.error(f"Deepseek analysis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

def create_server():
    """Create and configure the MCP server instance"""
    return MCPServer()
