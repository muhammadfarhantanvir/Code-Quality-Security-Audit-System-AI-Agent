"""
GitHub repository analysis functionality
"""

import os
import tempfile
import shutil
import subprocess
import re
from pathlib import Path
from typing import Optional, Tuple
import requests
from urllib.parse import urlparse


class GitHubAnalyzer:
    """Handles GitHub repository cloning and analysis"""
    
    def __init__(self):
        self.temp_dirs = []  # Track temp directories for cleanup
    
    def is_valid_github_url(self, url: str) -> bool:
        """Validate if the URL is a valid GitHub repository URL"""
        patterns = [
            r'^https://github\.com/[\w\-\.]+/[\w\-\.]+/?$',
            r'^https://github\.com/[\w\-\.]+/[\w\-\.]+\.git/?$',
            r'^git@github\.com:[\w\-\.]+/[\w\-\.]+\.git$',
        ]
        
        return any(re.match(pattern, url.strip()) for pattern in patterns)
    
    def normalize_github_url(self, url: str) -> str:
        """Normalize GitHub URL to HTTPS format"""
        url = url.strip()
        
        # Convert SSH to HTTPS
        if url.startswith('git@github.com:'):
            url = url.replace('git@github.com:', 'https://github.com/')
        
        # Remove .git suffix if present
        if url.endswith('.git'):
            url = url[:-4]
        
        # Remove trailing slash
        url = url.rstrip('/')
        
        return url
    
    def get_repo_info(self, github_url: str) -> Optional[dict]:
        """Get repository information from GitHub API"""
        try:
            # Extract owner and repo name from URL
            parsed = urlparse(github_url)
            path_parts = parsed.path.strip('/').split('/')
            
            if len(path_parts) >= 2:
                owner, repo = path_parts[0], path_parts[1]
                
                # Call GitHub API
                api_url = f"https://api.github.com/repos/{owner}/{repo}"
                response = requests.get(api_url, timeout=10)
                
                if response.status_code == 200:
                    repo_data = response.json()
                    return {
                        'name': repo_data.get('name'),
                        'full_name': repo_data.get('full_name'),
                        'description': repo_data.get('description'),
                        'language': repo_data.get('language'),
                        'size': repo_data.get('size'),  # in KB
                        'stars': repo_data.get('stargazers_count'),
                        'forks': repo_data.get('forks_count'),
                        'private': repo_data.get('private'),
                        'default_branch': repo_data.get('default_branch', 'main'),
                        'clone_url': repo_data.get('clone_url'),
                    }
        except Exception as e:
            print(f"Error getting repo info: {e}")
        
        return None
    
    def clone_repository(self, github_url: str, max_size_mb: int = 100) -> Tuple[Optional[str], Optional[str]]:
        """
        Clone GitHub repository to temporary directory
        Returns: (temp_directory_path, error_message)
        """
        try:
            # Normalize URL
            clone_url = self.normalize_github_url(github_url)
            
            # Get repo info first
            repo_info = self.get_repo_info(clone_url)
            if not repo_info:
                return None, "Repository not found or not accessible"
            
            # Check if repository is too large
            repo_size_mb = repo_info.get('size', 0) / 1024  # Convert KB to MB
            if repo_size_mb > max_size_mb:
                return None, f"Repository too large ({repo_size_mb:.1f}MB). Maximum allowed: {max_size_mb}MB"
            
            # Check if repository is private
            if repo_info.get('private'):
                return None, "Private repositories are not supported in the public demo"
            
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix='github_repo_')
            self.temp_dirs.append(temp_dir)
            
            # Clone repository with depth limit for faster cloning
            clone_command = [
                'git', 'clone', 
                '--depth', '1',  # Shallow clone
                '--single-branch',
                clone_url,
                temp_dir
            ]
            
            # Execute git clone
            result = subprocess.run(
                clone_command,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )
            
            if result.returncode == 0:
                return temp_dir, None
            else:
                error_msg = result.stderr or "Failed to clone repository"
                self.cleanup_temp_dir(temp_dir)
                return None, f"Clone failed: {error_msg}"
                
        except subprocess.TimeoutExpired:
            return None, "Clone timeout - repository may be too large"
        except Exception as e:
            return None, f"Clone error: {str(e)}"
    
    def cleanup_temp_dir(self, temp_dir: str):
        """Clean up a specific temporary directory"""
        try:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                if temp_dir in self.temp_dirs:
                    self.temp_dirs.remove(temp_dir)
        except Exception as e:
            print(f"Warning: Failed to cleanup {temp_dir}: {e}")
    
    def cleanup_all(self):
        """Clean up all temporary directories"""
        for temp_dir in self.temp_dirs.copy():
            self.cleanup_temp_dir(temp_dir)
    
    def get_repo_stats(self, repo_path: str) -> dict:
        """Get basic statistics about the cloned repository"""
        try:
            repo_path = Path(repo_path)
            
            # Count files by extension
            file_counts = {}
            total_files = 0
            total_lines = 0
            
            # Supported extensions for analysis
            supported_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', 
                                  '.cpp', '.c', '.php', '.rb', '.go', '.rs', '.cs', '.swift'}
            
            for file_path in repo_path.rglob('*'):
                if file_path.is_file() and not self._should_ignore_file(file_path):
                    ext = file_path.suffix.lower()
                    file_counts[ext] = file_counts.get(ext, 0) + 1
                    total_files += 1
                    
                    # Count lines for supported files
                    if ext in supported_extensions:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                total_lines += len(f.readlines())
                        except:
                            pass
            
            return {
                'total_files': total_files,
                'total_lines': total_lines,
                'file_counts': file_counts,
                'supported_files': sum(count for ext, count in file_counts.items() 
                                     if ext in supported_extensions)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored during analysis"""
        ignore_patterns = [
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            'build', 'dist', '.pytest_cache', '.mypy_cache',
            '.DS_Store', 'Thumbs.db'
        ]
        
        # Check if any part of the path contains ignore patterns
        path_str = str(file_path)
        return any(pattern in path_str for pattern in ignore_patterns)
    
    def __del__(self):
        """Cleanup on object destruction"""
        self.cleanup_all()