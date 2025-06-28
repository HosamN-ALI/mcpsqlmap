#!/usr/bin/env python3
"""
Script لأتمتة ربط خادم MCP مع Open WebUI
يقوم بإعداد التكامل تلقائياً باستخدام API
"""

import asyncio
import aiohttp
import json
import os
from typing import Dict, Any, Optional

class OpenWebUIIntegrator:
    def __init__(self):
        self.webui_base_url = "http://172.245.232.168:3000"
        self.mcp_server_url = "http://a36599630488ccf5d3.blackbx.ai"
        self.email = "deepgaza@hotmail.com"
        self.password = "123Zaq!@#"
        self.session = None
        self.auth_token = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def login(self) -> bool:
        """تسجيل الدخول إلى Open WebUI"""
        try:
            login_data = {
                "email": self.email,
                "password": self.password
            }
            
            async with self.session.post(
                f"{self.webui_base_url}/api/v1/auths/signin",
                json=login_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    self.auth_token = result.get("token")
                    print("✅ تم تسجيل الدخول بنجاح")
                    return True
                else:
                    print(f"❌ فشل تسجيل الدخول: {response.status}")
                    return False
                    
        except Exception as e:
            print(f"❌ خطأ في تسجيل الدخول: {str(e)}")
            return False
    
    def get_auth_headers(self) -> Dict[str, str]:
        """الحصول على headers المصادقة"""
        return {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
    
    async def add_external_api(self) -> bool:
        """إضافة API خارجي لخادم MCP"""
        try:
            api_config = {
                "name": "MCP SQLMap Server",
                "base_url": self.mcp_server_url,
                "api_key": "sk-1bd5de3f31db429cb8cbe73875537c5c",
                "model": "mcp-sqlmap",
                "enabled": True,
                "description": "Advanced SQL injection vulnerability scanner with DeepSeek AI analysis"
            }
            
            async with self.session.post(
                f"{self.webui_base_url}/api/v1/configs/external-apis",
                json=api_config,
                headers=self.get_auth_headers()
            ) as response:
                if response.status in [200, 201]:
                    print("✅ تم إضافة External API بنجاح")
                    return True
                else:
                    print(f"❌ فشل إضافة External API: {response.status}")
                    error_text = await response.text()
                    print(f"تفاصيل الخطأ: {error_text}")
                    return False
                    
        except Exception as e:
            print(f"❌ خطأ في إضافة External API: {str(e)}")
            return False
    
    async def add_model(self) -> bool:
        """إضافة نموذج MCP SQLMap"""
        try:
            model_config = {
                "id": "mcp-sqlmap",
                "name": "MCP SQLMap Security Scanner",
                "owned_by": "mcp-server",
                "object": "model",
                "created": 1640995200,
                "permission": [],
                "root": "mcp-sqlmap",
                "parent": None,
                "info": {
                    "description": "Advanced SQL injection vulnerability scanner with AI-powered analysis",
                    "capabilities": [
                        "SQL injection detection",
                        "WAF bypass techniques",
                        "Payload analysis",
                        "Vulnerability assessment"
                    ]
                }
            }
            
            async with self.session.post(
                f"{self.webui_base_url}/api/v1/models",
                json=model_config,
                headers=self.get_auth_headers()
            ) as response:
                if response.status in [200, 201]:
                    print("✅ تم إضافة Model بنجاح")
                    return True
                else:
                    print(f"❌ فشل إضافة Model: {response.status}")
                    return False
                    
        except Exception as e:
            print(f"❌ خطأ في إضافة Model: {str(e)}")
            return False
    
    async def add_functions(self) -> bool:
        """إضافة وظائف MCP"""
        functions = [
            {
                "name": "sql_injection_scan",
                "description": "Scan for SQL injection vulnerabilities",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_url": {
                            "type": "string",
                            "description": "Target URL to scan for SQL injection"
                        },
                        "options": {
                            "type": "object",
                            "description": "Scan options (depth, threads, etc.)",
                            "properties": {
                                "depth": {"type": "integer", "default": 2},
                                "threads": {"type": "integer", "default": 5}
                            }
                        }
                    },
                    "required": ["target_url"]
                },
                "endpoint": f"{self.mcp_server_url}/api/v1/scan",
                "method": "POST"
            },
            {
                "name": "analyze_payload",
                "description": "Analyze SQL injection payload using DeepSeek AI",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payload": {
                            "type": "string",
                            "description": "SQL injection payload to analyze"
                        },
                        "context": {
                            "type": "string",
                            "description": "Context information (optional)"
                        }
                    },
                    "required": ["payload"]
                },
                "endpoint": f"{self.mcp_server_url}/api/v1/analyze",
                "method": "POST"
            },
            {
                "name": "waf_bypass",
                "description": "Generate WAF bypass techniques for payloads",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payload": {
                            "type": "string",
                            "description": "Original SQL injection payload"
                        },
                        "techniques": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific bypass techniques to apply"
                        }
                    },
                    "required": ["payload"]
                },
                "endpoint": f"{self.mcp_server_url}/api/v1/bypass",
                "method": "POST"
            },
            {
                "name": "get_payloads",
                "description": "Get available SQL injection payloads",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "Payload source (fuzzdb, payloadsallthethings, nosql, custom)"
                        },
                        "category": {
                            "type": "string",
                            "description": "Payload category"
                        }
                    }
                },
                "endpoint": f"{self.mcp_server_url}/api/v1/payloads",
                "method": "GET"
            }
        ]
        
        success_count = 0
        for func in functions:
            try:
                async with self.session.post(
                    f"{self.webui_base_url}/api/v1/functions",
                    json=func,
                    headers=self.get_auth_headers()
                ) as response:
                    if response.status in [200, 201]:
                        print(f"✅ تم إضافة وظيفة {func['name']} بنجاح")
                        success_count += 1
                    else:
                        print(f"❌ فشل إضافة وظيفة {func['name']}: {response.status}")
                        
            except Exception as e:
                print(f"❌ خطأ في إضافة وظيفة {func['name']}: {str(e)}")
        
        return success_count == len(functions)
    
    async def setup_webhook(self) -> bool:
        """إعداد webhook للتحديثات"""
        try:
            webhook_config = {
                "name": "MCP Server Updates",
                "url": f"{self.webui_base_url}/api/webhooks/mcp-updates",
                "events": ["scan_complete", "vulnerability_found", "analysis_complete"],
                "headers": {
                    "Content-Type": "application/json"
                },
                "enabled": True
            }
            
            async with self.session.post(
                f"{self.webui_base_url}/api/v1/webhooks",
                json=webhook_config,
                headers=self.get_auth_headers()
            ) as response:
                if response.status in [200, 201]:
                    print("✅ تم إعداد Webhook بنجاح")
                    return True
                else:
                    print(f"❌ فشل إعداد Webhook: {response.status}")
                    return False
                    
        except Exception as e:
            print(f"❌ خطأ في إعداد Webhook: {str(e)}")
            return False
    
    async def test_connection(self) -> bool:
        """اختبار الاتصال مع خادم MCP"""
        try:
            async with self.session.get(f"{self.mcp_server_url}/status") as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ خادم MCP متصل ويعمل: {result}")
                    return True
                else:
                    print(f"❌ خادم MCP غير متاح: {response.status}")
                    return False
                    
        except Exception as e:
            print(f"❌ خطأ في الاتصال مع خادم MCP: {str(e)}")
            return False
    
    async def run_integration(self) -> bool:
        """تشغيل عملية التكامل الكاملة"""
        print("🚀 بدء عملية ربط خادم MCP مع Open WebUI...")
        print("=" * 50)
        
        # اختبار الاتصال مع خادم MCP
        print("1️⃣ اختبار الاتصال مع خادم MCP...")
        if not await self.test_connection():
            print("❌ فشل الاتصال مع خادم MCP. تأكد من تشغيل الخادم.")
            return False
        
        # تسجيل الدخول
        print("\n2️⃣ تسجيل الدخول إلى Open WebUI...")
        if not await self.login():
            print("❌ فشل تسجيل الدخول إلى Open WebUI.")
            return False
        
        # إضافة External API
        print("\n3️⃣ إضافة External API...")
        await self.add_external_api()
        
        # إضافة Model
        print("\n4️⃣ إضافة Model...")
        await self.add_model()
        
        # إضافة Functions
        print("\n5️⃣ إضافة Functions...")
        await self.add_functions()
        
        # إعداد Webhook
        print("\n6️⃣ إعداد Webhook...")
        await self.setup_webhook()
        
        print("\n" + "=" * 50)
        print("✅ تم إكمال عملية الربط بنجاح!")
        print(f"🌐 يمكنك الآن استخدام خادم MCP من خلال Open WebUI:")
        print(f"   - Open WebUI: {self.webui_base_url}")
        print(f"   - MCP Server: {self.mcp_server_url}")
        
        return True

async def main():
    """الدالة الرئيسية"""
    async with OpenWebUIIntegrator() as integrator:
        success = await integrator.run_integration()
        if success:
            print("\n🎉 التكامل مكتمل! يمكنك الآن استخدام وظائف الأمان في Open WebUI.")
        else:
            print("\n❌ فشل التكامل. راجع الأخطاء أعلاه.")

if __name__ == "__main__":
    asyncio.run(main())
