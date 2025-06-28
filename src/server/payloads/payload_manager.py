import os
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class PayloadSource(Enum):
    FUZZDB = "fuzzdb"
    PAYLOADSALLTHETHINGS = "payloadsallthethings"
    NOSQL = "nosql"
    CUSTOM = "custom"

@dataclass
class Payload:
    content: str
    source: str
    category: str
    description: Optional[str] = None

class PayloadManager:
    def __init__(self):
        self.logger = logging.getLogger("payload_manager")
        self._setup_logger()
        
        self.payloads: Dict[str, List[Payload]] = {
            PayloadSource.FUZZDB.value: [],
            PayloadSource.PAYLOADSALLTHETHINGS.value: [],
            PayloadSource.NOSQL.value: [],
            PayloadSource.CUSTOM.value: []
        }
        
        
        self.sources = {
            PayloadSource.FUZZDB.value: {
                "base": "/project/sandbox/user-workspace/fuzzdb-master/attack/sql-injection",
                "files": [
                    "detect/generic_sql.txt",
                    "detect/xplatform.txt",
                    "exploit/db2.txt",
                    "exploit/mysql.txt",
                    "exploit/mssql.txt",
                    "exploit/oracle.txt",
                    "exploit/postgres.txt"
                ]
            },
            PayloadSource.PAYLOADSALLTHETHINGS.value: {
                "base": "/project/sandbox/user-workspace/PayloadsAllTheThings-master",
                "files": [
                    "Account Takeover/mfa-bypass.md",
                    "Account Takeover/README.md",
                    "API Key Leaks/IIS-Machine-Keys.md",
                    "API Key Leaks/README.md",
                    "Business Logic Errors/README.md",
                    "Clickjacking/README.md",
                    "Client Side Path Traversal/README.md",
                    "Command Injection/README.md",
                    "CORS Misconfiguration/README.md",
                    "CRLF Injection/README.md",
                    "Cross-Site Request Forgery/README.md",
                    "CSV Injection/README.md",
                    "CVE Exploits/README.md",
                    "Denial of Service/README.md",
                    "Dependency Confusion/README.md",
                    "Directory Traversal/README.md",
                    "DNS Rebinding/README.md",
                    "DOM Clobbering/README.md",
                    "External Variable Modification/README.md",
                    "File Inclusion/README.md",
                    "Google Web Toolkit/README.md",
                    "GraphQL Injection/README.md",
                    "Headless Browser/README.md",
                    "Hidden Parameters/README.md",
                    "HTTP Parameter Pollution/README.md",
                    "Insecure Deserialization/README.md",
                    "Insecure Direct Object References/README.md",
                    "Insecure Management Interface/README.md",
                    "Insecure Randomness/README.md",
                    "Insecure Source Code Management/README.md",
                    "Java RMI/README.md",
                    "JSON Web Token/README.md",
                    "LaTeX Injection/README.md",
                    "LDAP Injection/README.md",
                    "Mass Assignment/README.md",
                    "Methodology and Resources/README.md",
                    "NoSQL Injection/README.md",
                    "OAuth Misconfiguration/README.md",
                    "Open Redirect/README.md",
                    "ORM Leak/README.md",
                    "Prompt Injection/README.md",
                    "Prototype Pollution/README.md",
                    "Race Condition/README.md",
                    "Regular Expression/README.md",
                    "Request Smuggling/README.md",
                    "SAML Injection/README.md",
                    "Server Side Include Injection/README.md",
                    "Server Side Request Forgery/README.md",
                    "Server Side Template Injection/README.md",
                    "SQL Injection/README.md",
                    "Tabnabbing/README.md",
                    "Type Juggling/README.md",
                    "Upload Insecure Files/README.md",
                    "Web Cache Deception/README.md",
                    "Web Sockets/README.md",
                    "XPATH Injection/README.md",
                    "XSLT Injection/README.md",
                    "XSS Injection/README.md",
                    "XXE Injection/README.md",
                    "Zip Slip/README.md"
                ]
             },
            PayloadSource.NOSQL.value: {
                "base": "/project/sandbox/user-workspace/nosqlinjection_wordlists-master",
                "files": [
                    "mongodb_nosqli.txt",
                    "README.md"
                ]
            }
        }
        
        # Removed synchronous call to async _load_payloads()
        # self._load_payloads()

    async def initialize(self):
        """Async initialization to load payloads"""
        await self._load_payloads()

    def _setup_logger(self):
        """Configure logging"""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def _load_payloads(self):
        """Load payloads from all sources"""
        self.logger.info("Loading payloads from all sources...")
        
        # Load from online sources
        for source in PayloadSource:
            if source != PayloadSource.CUSTOM:
                await self._load_from_source(source)
        
        # Load custom payloads
        await self._load_custom_payloads()
        
        self.logger.info("Finished loading payloads")

    async def _load_from_source(self, source: PayloadSource):
        """Load payloads from a specific source using local file system"""
        if source.value not in self.sources:
            self.logger.warning(f"Source {source.value} not configured")
            return

        source_config = self.sources[source.value]
        base_path = source_config["base"]

        if not os.path.exists(base_path):
            self.logger.error(f"Base directory not found: {base_path}")
            return

        # Walk through the directory recursively
        for root, _, files in os.walk(base_path):
            for file in files:
                # Only process text files
                if not file.lower().endswith(('.txt', '.md', '.json')):
                    continue

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    # Use relative path from base_path as category
                    rel_dir = os.path.relpath(root, base_path)
                    category = rel_dir.replace(os.sep, '/')
                    
                    payloads = text.splitlines()
                    for content in payloads:
                        if content.strip():  # Skip empty lines
                            self.payloads[source.value].append(
                                Payload(
                                    content=content.strip(),
                                    source=source.value,
                                    category=category
                                )
                            )
                    
                    self.logger.info(f"Loaded {len(payloads)} payloads from {file_path}")
                    
                except Exception as e:
                    self.logger.error(f"Error loading payloads from {file_path}: {str(e)}")
                    continue

    async def _load_custom_payloads(self):
        """Load custom payloads from local storage"""
        custom_path = os.path.join(os.path.dirname(__file__), "custom_payloads.json")
        
        try:
            if os.path.exists(custom_path):
                try:
                    with open(custom_path, 'r') as f:
                        custom_data = json.load(f)
                        
                    if not isinstance(custom_data, list):
                        self.logger.error("Custom payloads data must be a list")
                        return
                        
                    for item in custom_data:
                        try:
                            if "content" not in item:
                                self.logger.error(f"Missing required 'content' field in payload: {item}")
                                continue
                                
                            self.payloads[PayloadSource.CUSTOM.value].append(
                                Payload(
                                    content=item["content"],
                                    source=PayloadSource.CUSTOM.value,
                                    category=item.get("category", "custom"),
                                    description=item.get("description")
                                )
                            )
                        except Exception as e:
                            self.logger.error(f"Error processing payload item: {str(e)}")
                            continue
                            
                    self.logger.info(f"Loaded {len(self.payloads[PayloadSource.CUSTOM.value])} custom payloads")
                except json.JSONDecodeError as e:
                    self.logger.error(f"Invalid JSON in custom payloads file: {str(e)}")
                except Exception as e:
                    self.logger.error(f"Error reading custom payloads file: {str(e)}")
            else:
                self.logger.info("No custom payloads file found")
                
        except Exception as e:
            self.logger.error(f"Error accessing custom payloads file: {str(e)}")

    async def _load_fuzzdb_payloads(self):
        """Load payloads from FuzzDB repository"""
        await self._load_from_source(PayloadSource.FUZZDB)

    async def _load_pat_payloads(self):
        """Load payloads from PayloadsAllTheThings repository"""
        await self._load_from_source(PayloadSource.PAYLOADSALLTHETHINGS)

    async def _load_nosql_payloads(self):
        """Load NoSQL injection payloads"""
        await self._load_from_source(PayloadSource.NOSQL)

    async def analyze_with_deepseek(self, payload: str, api_key: str) -> Dict[str, Any]:
        """
        Analyze payload using Deepseek API
        
        Args:
            payload: The payload to analyze
            api_key: Deepseek API key for authentication
            
        Returns:
            Dict containing analysis results from Deepseek
            
        Raises:
            ValueError: If API key is invalid or missing
            RuntimeError: If API request fails
        """
        try:
            if not api_key or not api_key.startswith('sk-'):
                raise ValueError("Invalid Deepseek API key")

            self.logger.info(f"Analyzing payload with Deepseek: {payload[:50]}...")
            
            # Mock response for now - in production this would make a real API call
            analysis = {
                "analysis": {
                    "type": "union_based",
                    "risk_level": "high",
                    "target_tables": ["users"],
                    "explanation": "This payload attempts to extract passwords",
                    "recommendations": [
                        "Use parameterized queries",
                        "Implement input validation",
                        "Add WAF protection"
                    ]
                }
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Deepseek analysis failed: {str(e)}")
            raise RuntimeError(f"Failed to analyze payload: {str(e)}")

    def add_custom_payload(self, content: str, category: str = "custom", description: str = None) -> bool:
        """Add a new custom payload"""
        if content is None or not isinstance(content, str) or not content.strip():
            raise ValueError("Content must be a non-empty string")
        try:
            payload = Payload(
                content=content,
                source=PayloadSource.CUSTOM.value,
                category=category,
                description=description
            )
            
            self.payloads[PayloadSource.CUSTOM.value].append(payload)
            self._save_custom_payloads()
            
            self.logger.info(f"Added new custom payload: {content}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding custom payload: {str(e)}")
            return False

    def _save_custom_payloads(self):
        """Save custom payloads to local storage"""
        custom_path = os.path.join(os.path.dirname(__file__), "custom_payloads.json")
        
        try:
            custom_data = [
                {
                    "content": p.content,
                    "category": p.category,
                    "description": p.description
                }
                for p in self.payloads[PayloadSource.CUSTOM.value]
            ]
            
            with open(custom_path, 'w') as f:
                json.dump(custom_data, f, indent=2)
                
            self.logger.info("Saved custom payloads")
            
        except Exception as e:
            self.logger.error(f"Error saving custom payloads: {str(e)}")
            raise  # Re-raise the exception after logging it

    def get_payloads(self, 
                     source: Optional[str] = None, 
                     category: Optional[str] = None) -> List[Payload]:
        """Get payloads filtered by source and/or category"""
        if source and source not in [s.value for s in PayloadSource]:
            raise ValueError("Invalid source")
        
        result = []
        
        # Determine which sources to include
        sources = [source] if source else [s.value for s in PayloadSource]
        
        for src in sources:
            if src in self.payloads:
                for payload in self.payloads[src]:
                    if not category or payload.category == category:
                        result.append(payload)
        
        return result

    def get_available_sources(self) -> List[str]:
        """Return list of available payload sources"""
        return [source.value for source in PayloadSource]

    def get_available_categories(self, source: Optional[str] = None) -> List[str]:
        """Return list of available payload categories"""
        categories = set()
        
        sources = [source] if source else [s.value for s in PayloadSource]
        
        for src in sources:
            if src in self.payloads:
                for payload in self.payloads[src]:
                    categories.add(payload.category)
        
        return list(categories)

    def search_payloads(self, query: str) -> List[Payload]:
        """
        Search payloads by content
        
        Args:
            query: Search string to match against payload content
            
        Returns:
            List of matching Payload objects
        """
        if not query:
            return []
            
        result = []
        query = query.lower()
        
        for source_payloads in self.payloads.values():
            for payload in source_payloads:
                if query in payload.content.lower():
                    result.append(payload)
        
        return result


