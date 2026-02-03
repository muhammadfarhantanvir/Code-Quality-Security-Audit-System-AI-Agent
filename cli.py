import argparse
import requests
import json
import time
import sys
from typing import Optional

class AegisCLI:
    def __init__(self, api_url: str = "http://localhost:8005/api/v1"):
        self.api_url = api_url

    def run_scan(self, github_url: str, use_ai: bool = False):
        print(f"[SCAN] Starting audit for: {github_url}")
        print(f"[AI] AI Analysis: {'Enabled' if use_ai else 'Disabled'}")
        
        try:
            response = requests.post(
                f"{self.api_url}/scan",
                json={"github_url": github_url, "use_ai": use_ai}
            )
            response.raise_for_status()
            scan_id = response.json()["id"]
            print(f"[OK] Scan accepted. ID: {scan_id}")
            
            return self.poll_results(scan_id)
        except Exception as e:
            print(f"[ERROR] Error initiating scan: {e}")
            sys.exit(1)

    def poll_results(self, scan_id: str):
        print("[PROGRESS] Processing...")
        while True:
            try:
                response = requests.get(f"{self.api_url}/scan/{scan_id}")
                response.raise_for_status()
                data = response.json()
                
                if data["status"] == "completed":
                    print("\n[AUDIT] Audit Complete!")
                    self.print_summary(data["results"]["summary"])
                    return data
                elif data["status"] == "failed":
                    print(f"\n[AUDIT] Audit failed: {data.get('error', 'Unknown error')}")
                    sys.exit(1)
                
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(3)
            except Exception as e:
                print(f"\n[CONNECTION] Connection error: {e}")
                sys.exit(1)

    def print_summary(self, summary: dict):
        print("\n" + "="*40)
        print("AUDIT SUMMARY")
        print("="*40)
        print(f"Risk Score:    {summary['risk_score']}/100")
        print(f"Total Issues:  {summary['total_issues']}")
        print(f"Files Scanned: {summary['files_scanned']}")
        print(f"Total Lines:   {summary['total_lines']}")
        print(f"Duration:      {summary['duration']}s")
        print("="*40 + "\n")

    def list_history(self):
        try:
            response = requests.get(f"{self.api_url}/scans")
            response.raise_for_status()
            scans = response.json()
            
            print("\n📜 RECENT SCAN HISTORY")
            print(f"{'ID':<18} {'Score':<8} {'Issues':<8} {'URL'}")
            print("-" * 60)
            for s in scans:
                print(f"{s['id']:<18} {s['score']:<8.1f} {s['issues']:<8} {s['url']}")
        except Exception as e:
            print(f"[ERROR] Error fetching history: {e}")

def main():
    parser = argparse.ArgumentParser(description="Code audit ai Code Security Auditor CLI")
    parser.add_argument("url", nargs="?", help="GitHub Repository URL to scan")
    parser.add_argument("--ai", action="store_true", help="Enable Ollama AI analysis")
    parser.add_argument("--history", action="store_true", help="List recent scan history")
    parser.add_argument("--api", default="http://localhost:8005/api/v1", help="API base URL")

    args = parser.parse_args()
    cli = AegisCLI(args.api)

    if args.history:
        cli.list_history()
    elif args.url:
        cli.run_scan(args.url, args.ai)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
