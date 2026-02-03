import os
import re
import time
import json
from pathlib import Path
from typing import List, Dict, Any
from .patterns import get_all_patterns

class CodeAuditor:
    def __init__(self, use_ai: bool = False):
        self.patterns = get_all_patterns()
        self.use_ai = use_ai

    def scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        issues = []
        try:
            # Try to read with utf-8 first, fallback to other encodings if needed
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            content = "".join(lines)
        except UnicodeDecodeError:
            try:
                # Try with latin-1 as fallback
                with open(file_path, 'r', encoding='latin-1') as f:
                    lines = f.readlines()
                content = "".join(lines)
            except:
                # If all encodings fail, return empty issues list
                return []
        except:
            # If any other error occurs, return empty issues list
            return []

        try:
            for pattern in self.patterns:
                matches = re.finditer(pattern.pattern, content)
                for match in matches:
                    # Find line number
                    line_no = content[:match.start()].count('\n') + 1
                    snippet = lines[line_no-1].strip() if line_no <= len(lines) else ""

                    # Ensure compliance is always a list
                    compliance_value = getattr(pattern, 'compliance', None)
                    if compliance_value is None:
                        compliance_value = []

                    issues.append({
                        "id": pattern.id,
                        "name": pattern.name,
                        "description": pattern.description,
                        "severity": pattern.severity,
                        "category": pattern.category,
                        "line": line_no,
                        "snippet": snippet,
                        "recommendation": pattern.recommendation,
                        "file": str(file_path),
                        "owasp": getattr(pattern, 'owasp_tag', None),
                        "compliance": compliance_value
                    })
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")

        return issues

    def scan_directory(self, directory_path: str) -> Dict[str, Any]:
        try:
            start_time = time.time()
            all_issues = []
            files_scanned = 0
            total_lines = 0

            path = Path(directory_path)
            supported_exts = {'.py', '.js', '.ts', '.java', '.c', '.cpp', '.go', '.rs'}

            for file_path in path.rglob('*'):
                # Ignore hidden dirs and dependencies
                if any(part.startswith('.') or part in ['node_modules', 'venv', 'env', 'dist', 'build'] for part in file_path.parts):
                    continue

                if file_path.is_file() and file_path.suffix.lower() in supported_exts:
                    files_scanned += 1
                    file_issues = self.scan_file(file_path)

                    # Relative path for cleaner reports
                    for issue in file_issues:
                        issue['file'] = str(file_path.relative_to(path))

                    all_issues.extend(file_issues)

                    try:
                        # Try to read with utf-8 first, fallback to other encodings if needed
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            total_lines += len(f.readlines())
                    except UnicodeDecodeError:
                        try:
                            # Try with latin-1 as fallback
                            with open(file_path, 'r', encoding='latin-1') as f:
                                total_lines += len(f.readlines())
                        except:
                            pass  # Skip if all encodings fail
                    except:
                        pass  # Skip for any other errors

            duration = time.time() - start_time

            # Calculate risk score (0-100)
            severity_weights = {"CRITICAL": 25, "HIGH": 15, "MEDIUM": 7, "LOW": 3}
            total_weight = sum(severity_weights.get(i['severity'], 0) for i in all_issues)

            # Density based score
            risk_score = min(100, (total_weight / (total_lines / 200 + 1)) * 5) if total_lines > 0 else 0

            # Compliance mapping
            # Ensure all_issues is not None
            all_issues = all_issues if all_issues is not None else []
            compliance_summary = {}
            for issue in all_issues:
                compliance_list = issue.get('compliance') or []
                if compliance_list is None:
                    compliance_list = []
                for standard in compliance_list:
                    compliance_summary[standard] = compliance_summary.get(standard, 0) + 1

            return {
                "summary": {
                    "files_scanned": files_scanned,
                    "total_lines": total_lines,
                    "risk_score": round(risk_score, 1),
                    "duration": round(duration, 2),
                    "total_issues": len(all_issues),
                    "compliance_summary": compliance_summary
                },
                "issues": all_issues
            }
        except Exception as e:
            print(f"Error in scan_directory: {e}")
            # Return a valid structure even if there's an error
            return {
                "summary": {
                    "files_scanned": 0,
                    "total_lines": 0,
                    "risk_score": 0,
                    "duration": 0,
                    "total_issues": 0,
                    "compliance_summary": {}
                },
                "issues": []
            }
