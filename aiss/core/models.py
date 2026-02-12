"""
Core data models for AISS
"""
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional

class SeverityLevel(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

@dataclass
class Finding:
    severity: SeverityLevel
    title: str
    description: str
    proof: str
    remediation: str
    timestamp: str