"""
Enhanced reporting system for AISS
"""
from typing import List, Dict, Any
from datetime import datetime
import json
from pathlib import Path
import jinja2
from rich.console import Console
from rich.table import Table
from ..core.scanner import Finding, SeverityLevel
from ..core.config import ReportConfig
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class ReportGenerator:
    def __init__(self, config: ReportConfig):
        self.config = config
        self.console = Console()
        self.template_loader = jinja2.FileSystemLoader(
            searchpath=str(Path(__file__).parent / "templates")
        )
        self.template_env = jinja2.Environment(loader=self.template_loader)
        
    def generate(self, findings: List[Finding], scan_metadata: Dict[str, Any]) -> str:
        """Generate report based on configured format"""
        if self.config.output_format == "json":
            return self._generate_json(findings, scan_metadata)
        elif self.config.output_format == "html":
            return self._generate_html(findings, scan_metadata)
        else:
            return self._generate_text(findings, scan_metadata)
            
    def _generate_text(self, findings: List[Finding], metadata: Dict[str, Any]) -> str:
        """Generate text report"""
        table = Table(title="AISS Security Assessment Report")
        
        # Add metadata
        self.console.print(f"Scan completed at: {metadata['timestamp']}")
        self.console.print(f"Target: {metadata['target']}\n")
        
        # Summary
        summary_table = Table(title="Summary")
        summary_table.add_column("Severity")
        summary_table.add_column("Count")
        
        for severity in SeverityLevel:
            count = len([f for f in findings if f.severity == severity])
            if count > 0:
                summary_table.add_row(
                    severity.value,
                    str(count),
                    style=self._get_severity_style(severity)
                )
                
        self.console.print(summary_table)
        self.console.print("\nDetailed Findings:")
        
        # Detailed findings
        findings_table = Table()
        findings_table.add_column("Severity")
        findings_table.add_column("Title")
        findings_table.add_column("Description")
        if self.config.detail_level == "detailed":
            findings_table.add_column("Proof")
        findings_table.add_column("Remediation")
        
        for finding in findings:
            row = [
                finding.severity.value,
                finding.title,
                finding.description,
                finding.remediation
            ]
            if self.config.detail_level == "detailed":
                row.insert(3, finding.proof)
                
            findings_table.add_row(*row, style=self._get_severity_style(finding.severity))
            
        self.console.print(findings_table)
        return self.console.export_text()
        
    def _generate_json(self, findings: List[Finding], metadata: Dict[str, Any]) -> str:
        """Generate JSON report"""
        report = {
            "metadata": metadata,
            "summary": self._generate_summary(findings),
            "findings": [self._finding_to_dict(f) for f in findings]
        }
        return json.dumps(report, indent=2)
        
    def _generate_html(self, findings: List[Finding], metadata: Dict[str, Any]) -> str:
        """Generate HTML report with visualizations"""
        template = self.template_env.get_template("report.html")
        
        # Generate charts
        severity_chart = self._create_severity_chart(findings)
        timeline_chart = self._create_timeline_chart(findings)
        
        context = {
            "metadata": metadata,
            "findings": findings,
            "summary": self._generate_summary(findings),
            "severity_chart": severity_chart.to_html(full_html=False),
            "timeline_chart": timeline_chart.to_html(full_html=False),
            "company_name": self.config.company_name,
            "logo_path": self.config.logo_path
        }
        
        return template.render(**context)
        
    def _create_severity_chart(self, findings: List[Finding]) -> go.Figure:
        """Create severity distribution chart"""
        severity_counts = {}
        for severity in SeverityLevel:
            count = len([f for f in findings if f.severity == severity])
            severity_counts[severity.value] = count
            
        fig = px.pie(
            values=list(severity_counts.values()),
            names=list(severity_counts.keys()),
            title="Findings by Severity"
        )
        return fig
        
    def _create_timeline_chart(self, findings: List[Finding]) -> go.Figure:
        """Create findings timeline chart"""
        df = pd.DataFrame([
            {
                "timestamp": datetime.fromisoformat(f.timestamp),
                "severity": f.severity.value,
                "title": f.title
            }
            for f in findings
        ])
        
        fig = px.timeline(
            df,
            x_start="timestamp",
            y="severity",
            color="severity",
            hover_data=["title"],
            title="Findings Timeline"
        )
        return fig
        
    def _finding_to_dict(self, finding: Finding) -> Dict[str, Any]:
        """Convert finding to dictionary"""
        return {
            "severity": finding.severity.value,
            "title": finding.title,
            "description": finding.description,
            "proof": finding.proof if self.config.include_proof else None,
            "remediation": finding.remediation,
            "timestamp": finding.timestamp
        }
        
    def _generate_summary(self, findings: List[Finding]) -> Dict[str, int]:
        """Generate severity summary"""
        return {
            severity.value: len([f for f in findings if f.severity == severity])
            for severity in SeverityLevel
        }
        
    def _get_severity_style(self, severity: SeverityLevel) -> str:
        """Get rich console style for severity"""
        styles = {
            SeverityLevel.CRITICAL: "bold red",
            SeverityLevel.HIGH: "red",
            SeverityLevel.MEDIUM: "yellow",
            SeverityLevel.LOW: "blue",
            SeverityLevel.INFO: "green"
        }
        return styles.get(severity, "")