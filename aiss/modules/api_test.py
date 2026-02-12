"""
API Security Test Module
"""
from typing import List, Dict
import aiohttp
import asyncio
from datetime import datetime
from ..core.models import Finding, SeverityLevel

class APISecurityTester:
    def __init__(self, target_url: str):
        self.target = target_url
        
    async def run_tests(self) -> List[Finding]:
        findings = []
        
        # Test 1: Basic API Accessibility
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(self.target)
                if response.status != 200:
                    findings.append(Finding(
                        severity=SeverityLevel.HIGH,
                        title="API Endpoint Inaccessible",
                        description=f"API endpoint returned status code {response.status}",
                        proof=f"GET {self.target} -> {response.status}",
                        remediation="Verify API endpoint is accessible and properly configured",
                        timestamp=datetime.utcnow().isoformat()
                    ))
            except Exception as e:
                findings.append(Finding(
                    severity=SeverityLevel.HIGH,
                    title="API Connection Failed",
                    description=f"Could not connect to API: {str(e)}",
                    proof=f"Connection error: {str(e)}",
                    remediation="Ensure API endpoint is accessible and SSL certificates are valid",
                    timestamp=datetime.utcnow().isoformat()
                ))
        
        # Test 2: Rate Limiting
        async with aiohttp.ClientSession() as session:
            tasks = [session.get(self.target) for _ in range(10)]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            if not any(isinstance(r, Exception) for r in responses):
                findings.append(Finding(
                    severity=SeverityLevel.MEDIUM,
                    title="Potential Rate Limiting Issue",
                    description="Multiple rapid requests succeeded without rate limiting",
                    proof=f"10 simultaneous requests all succeeded",
                    remediation="Implement rate limiting to prevent abuse",
                    timestamp=datetime.utcnow().isoformat()
                ))
        
        # Test 3: Security Headers
        async with aiohttp.ClientSession() as session:
            response = await session.get(self.target)
            headers = response.headers
            
            security_headers = {
                'X-Frame-Options': 'Missing X-Frame-Options header',
                'X-Content-Type-Options': 'Missing X-Content-Type-Options header',
                'X-XSS-Protection': 'Missing X-XSS-Protection header',
                'Content-Security-Policy': 'Missing Content-Security-Policy header'
            }
            
            for header, message in security_headers.items():
                if header not in headers:
                    findings.append(Finding(
                        severity=SeverityLevel.MEDIUM,
                        title=f"Missing Security Header: {header}",
                        description=message,
                        proof=f"Headers present: {dict(headers)}",
                        remediation=f"Add {header} header to API responses",
                        timestamp=datetime.utcnow().isoformat()
                    ))
        
        return findings