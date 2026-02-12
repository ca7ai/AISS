"""
Core scanner implementation
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
from .config import AISSConfig
from .models import Finding, SeverityLevel
from ..modules.api_test import APISecurityTester
from ..modules.agent_test import AgentResponseTester

class SecurityScanner:
    def __init__(self, target: Optional[str] = None, config: Optional[AISSConfig] = None):
        self.target = target
        self.config = config or AISSConfig()
        
    async def run_scan(self) -> Dict[str, Any]:
        """Run all security tests"""
        if not self.target:
            raise ValueError("Target URL is required for scanning")
            
        findings = []
        
        # Run API Security Tests
        api_tester = APISecurityTester(self.target)
        api_findings = await api_tester.run_tests()
        findings.extend(api_findings)
        
        # Run Agent Response Tests
        agent_tester = AgentResponseTester(self.target)
        agent_findings = await agent_tester.run_tests()
        findings.extend(agent_findings)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "target": self.target,
            "findings": findings,
            "summary": self._generate_summary(findings)
        }
    
    def _generate_summary(self, findings: List[Finding]) -> Dict[str, int]:
        """Generate severity summary"""
        summary = {level: 0 for level in SeverityLevel}
        for finding in findings:
            summary[finding.severity] += 1
        return summary