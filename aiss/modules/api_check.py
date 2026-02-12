"""
API Security Test Module
"""
from typing import List
from ..core.scanner import Finding, SeverityLevel
import aiohttp
import asyncio

class APISecurityTester:
    def __init__(self, target_url: str):
        self.target = target_url
        
    async def run_tests(self) -> List[Finding]:
        findings = []
        
        # Rate Limiting Test
        async with aiohttp.ClientSession() as session:
            start_time = asyncio.get_event_loop().time()
            requests = [session.get(f"{self.target}/api/test") for _ in range(50)]
            responses = await asyncio.gather(*requests, return_exceptions=True)
            end_time = asyncio.get_event_loop().time()
            
            if end_time - start_time < 1.0:  # Too many requests succeeded too quickly
                findings.append(Finding(
                    severity=SeverityLevel.HIGH,
                    title="Missing Rate Limiting",
                    description="API lacks proper rate limiting protection",
                    proof=f"Made 50 requests in {end_time - start_time:.2f} seconds",
                    remediation="Implement rate limiting using token bucket or similar algorithm",
                    timestamp=""
                ))
                
        # Auth Bypass Test
        auth_vectors = [
            "",  # No auth
            "null",  # Null auth
            "undefined",  # Undefined auth
            "guest:guest",  # Default credentials
        ]
        
        for vector in auth_vectors:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": vector} if vector else {}
                resp = await session.get(f"{self.target}/api/secured", headers=headers)
                
                if resp.status == 200:
                    findings.append(Finding(
                        severity=SeverityLevel.CRITICAL,
                        title="Authentication Bypass",
                        description=f"Successful auth bypass using: {vector}",
                        proof=f"Request succeeded with auth: {vector}",
                        remediation="Implement proper authentication checks",
                        timestamp=""
                    ))
                    
        return findings