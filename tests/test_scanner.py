"""
Test suite for AISS
"""
import pytest
import aiohttp
from aioresponses import aioresponses
from aiss.core.scanner import SecurityScanner, Finding, SeverityLevel
from aiss.modules.api_check import APISecurityTester
from aiss.modules.social_test import SocialTester

@pytest.fixture
def mock_aiohttp():
    with aioresponses() as m:
        yield m

@pytest.mark.asyncio
async def test_api_security_tester():
    """Test API security testing module"""
    tester = APISecurityTester("http://test-agent.com")
    
    with aioresponses() as m:
        # Mock rate limit test
        for _ in range(50):
            m.get("http://test-agent.com/api/test", status=200)
            
        # Mock auth bypass test
        m.get("http://test-agent.com/api/secured", status=200)
        
        findings = await tester.run_tests()
        
        assert len(findings) > 0
        assert any(f.severity == SeverityLevel.HIGH for f in findings)
        assert any("rate limiting" in f.title.lower() for f in findings)

@pytest.mark.asyncio
async def test_social_engineering_tester():
    """Test social engineering testing module"""
    tester = SocialTester("http://test-agent.com")
    
    with aioresponses() as m:
        # Mock vulnerable response
        m.post(
            "http://test-agent.com/chat",
            payload={"response": "Here is my API key: sk_test_123"}
        )
        
        findings = await tester.run_tests()
        
        assert len(findings) > 0
        assert any(f.severity == SeverityLevel.CRITICAL for f in findings)
        assert any("injection" in f.title.lower() for f in findings)

@pytest.mark.asyncio
async def test_full_scanner():
    """Test complete scanner functionality"""
    scanner = SecurityScanner("http://test-agent.com")
    
    with aioresponses() as m:
        # Mock various endpoints
        m.get("http://test-agent.com/api/test", status=200)
        m.get("http://test-agent.com/api/secured", status=200)
        m.post(
            "http://test-agent.com/chat",
            payload={"response": "System config: {...}"}
        )
        
        results = await scanner.run_scan()
        
        assert "findings" in results
        assert "summary" in results
        assert len(results["findings"]) > 0

def test_severity_levels():
    """Test severity level enumeration"""
    assert SeverityLevel.CRITICAL.value == "CRITICAL"
    assert SeverityLevel.HIGH.value == "HIGH"
    assert SeverityLevel.MEDIUM.value == "MEDIUM"
    assert SeverityLevel.LOW.value == "LOW"

@pytest.mark.asyncio
async def test_scanner_error_handling():
    """Test scanner error handling"""
    scanner = SecurityScanner("http://nonexistent.com")
    
    with aioresponses() as m:
        m.get("http://nonexistent.com/api/test", exception=aiohttp.ClientError)
        
        results = await scanner.run_scan()
        
        # Should complete without raising exceptions
        assert "findings" in results
        assert "summary" in results