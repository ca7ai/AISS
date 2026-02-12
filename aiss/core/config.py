"""
Configuration management for AISS
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import yaml
import os
from pathlib import Path

class ScanConfig(BaseModel):
    """Scan configuration settings"""
    max_requests: int = Field(default=50, description="Maximum requests per test")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    user_agent: str = Field(default="AISS-Scanner/1.0", description="User agent string")
    follow_redirects: bool = Field(default=True, description="Follow HTTP redirects")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")

class ReportConfig(BaseModel):
    """Reporting configuration"""
    detail_level: str = Field(
        default="standard",
        description="Report detail level (minimal, standard, detailed)"
    )
    include_proof: bool = Field(default=True, description="Include proof details")
    output_format: str = Field(default="text", description="Output format (text, json, html)")
    save_path: Optional[str] = Field(default=None, description="Path to save reports")
    company_name: Optional[str] = Field(default=None, description="Company name for reports")
    logo_path: Optional[str] = Field(default=None, description="Path to logo for HTML reports")

class AISSConfig(BaseModel):
    """Main configuration"""
    scan: ScanConfig = Field(default_factory=ScanConfig)
    report: ReportConfig = Field(default_factory=ReportConfig)
    log_level: str = Field(default="INFO")
    api_base_url: Optional[str] = Field(default=None)
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> 'AISSConfig':
        """Load configuration from file"""
        if not config_path:
            config_path = os.getenv('AISS_CONFIG', '~/.config/aiss/config.yml')
            
        config_path = os.path.expanduser(config_path)
        
        if os.path.exists(config_path):
            with open(config_path) as f:
                config_data = yaml.safe_load(f)
                return cls.parse_obj(config_data)
        
        return cls()  # Return default config if file doesn't exist
    
    def save(self, config_path: Optional[str] = None) -> None:
        """Save configuration to file"""
        if not config_path:
            config_path = os.path.expanduser('~/.config/aiss/config.yml')
            
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w') as f:
            yaml.dump(self.dict(), f)
            
    @property
    def report_path(self) -> str:
        """Get report save path"""
        if self.report.save_path:
            return os.path.expanduser(self.report.save_path)
        return os.path.expanduser('~/aiss-reports')