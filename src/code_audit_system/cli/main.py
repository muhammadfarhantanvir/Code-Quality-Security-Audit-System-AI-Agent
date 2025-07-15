"""
Command-line interface for the audit system
"""

import argparse
import json
import sys
import time
import csv
from datetime import datetime
from dataclasses import asdict
from pathlib import Path

from ..core.auditor import CodeAuditor
from ..core.models import AuditReport


def main():
    """Enhanced CLI interface with comprehensive options"""
    parser = argparse.ArgumentParser(
        description="Code Quality & Security Audit System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --directory ./my-project
  %(prog)s --directory ./my-project --output report.json --format json
  %(prog)s --directory ./my-project --severity HIGH --export-html
  %(prog)s --dashboard
  %(prog)s --version
        """
    )
    
    # Main arguments
    parser.add_argument("--directory", "-d", help="Directory to scan")
    parser.add_argument("--output", "-o", help="Output file for report")
    parser.add_argument("--format", "-f", choices=["json", "csv", "html"], 
                       default="json", help="Output format (default: json)")
    
    # Filtering options
    parser.add_argument("--severity", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                       help="Filter issues by minimum severity")
    parser.add_argument("--type", choices=["security", "quality", "all"], 
                       default="all", help="Type of issues to report")
    parser.add_argument("--exclude", nargs="*", help="Patterns to exclude from scan")
    
    # Export options
    parser.add_argument("--export-html", action="store_true", 
                       help="Export HTML report")
    parser.add_argument("--export-csv", action="store_true", 
                       help="Export CSV report")
    parser.add_argument("--export-pdf", action="store_true", 
                       help="Export PDF report")
    
    # Dashboard and utilities
    parser.add_argument("--dashboard", action="store_true", 
                       help="Launch Streamlit dashboard")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    
    # AI options
    parser.add_argument("--no-ai", action="store_true", 
                       help="Disable AI analysis (pattern-only)")
    parser.add_argument("--ollama-url", default="http://localhost:11434",
                       help="Ollama server URL")
    
    args = parser.parse_args()
    
    # Handle dashboard launch
    if args.dashboard:
        try:
            import subprocess
            subprocess.run(["streamlit", "run", "src/code_audit_system/dashboard/streamlit_app.py"])
        except FileNotFoundError:
            print("❌ Streamlit not found. Install with: pip install streamlit")
            sys.exit(1)
        return
    
    # Validate required arguments
    if not args.directory:
        parser.error("--directory is required (unless using --dashboard)")
    
    # Load configuration
    config = {}
    if args.config:
        try:
            import yaml
            with open(args.config, 'r') as f:
                config = yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            sys.exit(1)
    
    # Initialize auditor
    try:
        if args.ollama_url:
            config.setdefault('ollama', {})['base_url'] = args.ollama_url
        
        auditor = CodeAuditor(config)
    except Exception as e:
        print(f"❌ Failed to initialize auditor: {e}")
        sys.exit(1)
    
    print("🔍 Code Quality & Security Audit System v1.0.0")
    print("=" * 50)
    print(f"📁 Scanning directory: {args.directory}")
    
    if args.verbose:
        print(f"🔧 Configuration:")
        print(f"   - Output format: {args.format}")
        print(f"   - Severity filter: {args.severity or 'ALL'}")
        print(f"   - Issue type: {args.type}")
        print(f"   - AI analysis: {'Disabled' if args.no_ai else 'Enabled'}")
        print(f"   - Ollama URL: {args.ollama_url}")
    
    try:
        # Perform audit
        start_time = time.time()
        report = auditor.scan_directory(args.directory, use_ai=not args.no_ai)
        scan_duration = time.time() - start_time
        
        # Filter results based on arguments
        if args.severity:
            report.security_issues = [i for i in report.security_issues 
                                    if i.severity == args.severity]
            report.quality_issues = [i for i in report.quality_issues 
                                   if i.severity == args.severity]
        
        if args.type == "security":
            report.quality_issues = []
        elif args.type == "quality":
            report.security_issues = []
        
        # Display results
        print(f"\n✅ Audit completed in {scan_duration:.2f} seconds!")
        print(f"📊 Files scanned: {report.total_files}")
        print(f"📏 Total lines: {report.total_lines}")
        print(f"🔐 Security issues: {len(report.security_issues)}")
        print(f"📊 Quality issues: {len(report.quality_issues)}")
        print(f"⚠️  Risk score: {report.risk_score}/100")
        
        # Risk assessment
        if report.risk_score >= 70:
            print("🔴 HIGH RISK - Immediate attention required!")
        elif report.risk_score >= 40:
            print("🟡 MEDIUM RISK - Review and address issues")
        else:
            print("🟢 LOW RISK - Good code quality")
        
        # Save output
        if args.output or args.export_html or args.export_csv:
            output_file = args.output or f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if args.format == "json" or args.output:
                json_file = f"{output_file}.json" if not args.output else args.output
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(asdict(report), f, indent=2, default=str, ensure_ascii=False)
                print(f"📄 JSON report saved: {json_file}")
            
            if args.export_csv or args.format == "csv":
                csv_file = f"{output_file}.csv"
                export_csv_report(report, csv_file)
                print(f"📊 CSV report saved: {csv_file}")
            
            if args.export_html or args.format == "html":
                html_file = f"{output_file}.html"
                export_html_report(report, html_file)
                print(f"🌐 HTML report saved: {html_file}")
        
        # Display top issues
        if report.security_issues and args.verbose:
            print(f"\n🔴 Top Security Issues:")
            for i, issue in enumerate(report.security_issues[:5], 1):
                print(f"  {i}. {issue.severity} - {issue.issue_type}")
                print(f"     📁 {issue.file_path}:{issue.line_number}")
                print(f"     💡 {issue.recommendation}")
        
        if report.quality_issues and args.verbose:
            print(f"\n🟡 Top Quality Issues:")
            for i, issue in enumerate(report.quality_issues[:5], 1):
                print(f"  {i}. {issue.severity} - {issue.issue_type}")
                print(f"     📁 {issue.file_path}:{issue.line_number}")
                print(f"     💡 {issue.recommendation}")
        
        # Recommendations
        if report.recommendations:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(report.recommendations, 1):
                print(f"  {i}. {rec}")
        
        # Exit with appropriate code
        if report.risk_score >= 70:
            sys.exit(2)  # High risk
        elif report.risk_score >= 40:
            sys.exit(1)  # Medium risk
        else:
            sys.exit(0)  # Low risk
    
    except Exception as e:
        print(f"❌ Error during audit: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def export_csv_report(report: AuditReport, filename: str):
    """Export audit report to CSV format"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Type', 'File', 'Line', 'Issue Type', 'Severity', 'Description', 'Recommendation'])
        
        # Write security issues
        for issue in report.security_issues:
            writer.writerow(['Security', issue.file_path, issue.line_number, 
                           issue.issue_type, issue.severity, issue.description, 
                           issue.recommendation])
        
        # Write quality issues
        for issue in report.quality_issues:
            writer.writerow(['Quality', issue.file_path, issue.line_number, 
                           issue.issue_type, issue.severity, issue.description, 
                           issue.recommendation])


def export_html_report(report: AuditReport, filename: str):
    """Export audit report to HTML format"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Code Audit Report - {report.project_path}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
            .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #e9e9e9; border-radius: 3px; }}
            .high {{ color: #d32f2f; }}
            .medium {{ color: #f57c00; }}
            .low {{ color: #388e3c; }}
            .issue {{ margin: 10px 0; padding: 10px; border-left: 4px solid #ccc; }}
            .security {{ border-left-color: #d32f2f; }}
            .quality {{ border-left-color: #f57c00; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔍 Code Audit Report</h1>
            <p><strong>Project:</strong> {report.project_path}</p>
            <p><strong>Scan Date:</strong> {report.scan_date}</p>
            <div class="metric"><strong>Risk Score:</strong> {report.risk_score}/100</div>
            <div class="metric"><strong>Files:</strong> {report.total_files}</div>
            <div class="metric"><strong>Lines:</strong> {report.total_lines}</div>
            <div class="metric"><strong>Security Issues:</strong> {len(report.security_issues)}</div>
            <div class="metric"><strong>Quality Issues:</strong> {len(report.quality_issues)}</div>
        </div>
        
        <h2>🔐 Security Issues</h2>
    """
    
    for issue in report.security_issues:
        severity_class = issue.severity.lower()
        html_content += f"""
        <div class="issue security">
            <h3 class="{severity_class}">{issue.severity} - {issue.issue_type}</h3>
            <p><strong>File:</strong> {issue.file_path}:{issue.line_number}</p>
            <p><strong>Description:</strong> {issue.description}</p>
            <p><strong>Code:</strong> <code>{issue.code_snippet}</code></p>
            <p><strong>Recommendation:</strong> {issue.recommendation}</p>
        </div>
        """
    
    html_content += "<h2>📊 Quality Issues</h2>"
    
    for issue in report.quality_issues:
        severity_class = issue.severity.lower()
        html_content += f"""
        <div class="issue quality">
            <h3 class="{severity_class}">{issue.severity} - {issue.issue_type}</h3>
            <p><strong>File:</strong> {issue.file_path}:{issue.line_number}</p>
            <p><strong>Description:</strong> {issue.description}</p>
            <p><strong>Code:</strong> <code>{issue.code_snippet}</code></p>
            <p><strong>Recommendation:</strong> {issue.recommendation}</p>
        </div>
        """
    
    html_content += """
        <h2>💡 Recommendations</h2>
        <ul>
    """
    
    for rec in report.recommendations:
        html_content += f"<li>{rec}</li>"
    
    html_content += """
        </ul>
    </body>
    </html>
    """
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == "__main__":
    main()