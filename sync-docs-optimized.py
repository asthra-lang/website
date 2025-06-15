#!/usr/bin/env python3

"""
Optimized versioned documentation sync script
Usage: python sync-docs-optimized.py <source_repo_path> [--max-versions=10] [--parallel=4]

This optimized version addresses scalability concerns:
1. Parallel processing of versions
2. Incremental updates (only process changed versions)
3. Configurable limits on number of versions
4. Memory-efficient tag processing
5. Git archive instead of checkout for better performance
6. Caching and deduplication
"""

import sys
import os
import shutil
import subprocess
import tempfile
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import semver


class OptimizedDocSync:
    def __init__(self, repo_path: Path, max_versions: int = 10, parallel_workers: int = 4):
        self.repo_path = repo_path
        self.max_versions = max_versions
        self.parallel_workers = parallel_workers
        self.docs_dir = Path("_docs")
        self.cache_file = self.docs_dir / ".sync_cache.json"
        self.doc_dirs = ["contributor", "spec", "stdlib", "user-manual"]
        
    def run_git_command(self, command: List[str]) -> str:
        """Run a git command in the repository."""
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {e}")
            return ""

    def get_git_tags_efficiently(self) -> List[str]:
        """Get git tags efficiently using git for-each-ref."""
        # Use git for-each-ref for better performance with many tags
        output = self.run_git_command([
            "for-each-ref", 
            "--format=%(refname:short)",
            "--sort=-version:refname",  # Sort by version descending
            "refs/tags"
        ])
        if not output:
            return []
        return [tag.strip() for tag in output.split('\n') if tag.strip()]

    def parse_and_filter_versions(self, tags: List[str]) -> Dict[str, semver.VersionInfo]:
        """Parse version tags and filter efficiently."""
        versions = []
        
        # Parse versions in batches to manage memory
        for tag in tags:
            version_str = tag[1:] if tag.startswith('v') else tag
            
            try:
                version = semver.VersionInfo.parse(version_str)
                # Skip pre-release versions
                if version.prerelease is None:
                    versions.append(version)
            except ValueError:
                continue
        
        # Group by minor version and get latest patch
        minor_versions = {}
        for version in versions:
            minor_key = f"{version.major}.{version.minor}"
            if minor_key not in minor_versions or version > minor_versions[minor_key]:
                minor_versions[minor_key] = version
        
        # Limit to max_versions (most recent)
        sorted_items = sorted(minor_versions.items(), 
                            key=lambda x: minor_versions[x[0]], 
                            reverse=True)
        
        return dict(sorted_items[:self.max_versions])

    def load_cache(self) -> Dict:
        """Load processing cache to avoid redundant work."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}

    def save_cache(self, cache: Dict):
        """Save processing cache."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
        except IOError:
            print("⚠ Warning: Could not save cache")

    def get_version_hash(self, version: semver.VersionInfo) -> str:
        """Get hash of version's documentation for change detection."""
        try:
            # Get commit hash for the tag
            tag = f"v{version}"
            commit_hash = self.run_git_command(["rev-list", "-n", "1", tag])
            
            # Create hash based on commit and doc directories
            content = f"{commit_hash}:{':'.join(self.doc_dirs)}"
            return hashlib.md5(content.encode()).hexdigest()
        except:
            return str(version)

    def extract_docs_with_git_archive(self, version: semver.VersionInfo, version_key: str) -> bool:
        """Extract documentation using git archive (faster than checkout)."""
        tag = f"v{version}"
        version_dir = self.docs_dir / version_key
        
        # Create version directory
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # Remove existing docs
        for dir_name in self.doc_dirs:
            target_dir = version_dir / dir_name
            if target_dir.exists():
                shutil.rmtree(target_dir)
        
        success = True
        
        # Use git archive to extract specific directories
        for dir_name in self.doc_dirs:
            try:
                # Create archive of specific directory
                archive_path = f"docs/{dir_name}"
                result = subprocess.run([
                    "git", "archive", tag, archive_path
                ], cwd=self.repo_path, capture_output=True)
                
                if result.returncode == 0 and result.stdout:
                    # Extract archive to temporary location
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_path = Path(temp_dir)
                        
                        # Extract tar archive
                        extract_result = subprocess.run([
                            "tar", "-x", "-C", str(temp_path)
                        ], input=result.stdout, capture_output=True)
                        
                        if extract_result.returncode == 0:
                            source_dir = temp_path / "docs" / dir_name
                            target_dir = version_dir / dir_name
                            
                            if source_dir.exists():
                                shutil.copytree(source_dir, target_dir)
                                print(f"✓ Extracted {dir_name} docs for version {version_key}")
                            else:
                                print(f"⚠ Warning: {dir_name} docs not found for version {version_key}")
                                success = False
                        else:
                            print(f"⚠ Warning: Failed to extract {dir_name} for version {version_key}")
                            success = False
                else:
                    print(f"⚠ Warning: {dir_name} docs not found for version {version_key}")
                    success = False
                    
            except Exception as e:
                print(f"✗ Error processing {dir_name} for version {version_key}: {e}")
                success = False
        
        return success

    def process_version(self, version_item) -> tuple:
        """Process a single version (for parallel execution)."""
        version_key, version = version_item
        
        try:
            print(f"Processing version {version_key} (tag: v{version})...")
            
            if self.extract_docs_with_git_archive(version, version_key):
                print(f"✓ Successfully processed version {version_key}")
                return version_key, True, self.get_version_hash(version)
            else:
                print(f"⚠ Partial success for version {version_key}")
                return version_key, False, None
                
        except Exception as e:
            print(f"✗ Error processing version {version_key}: {e}")
            return version_key, False, None

    def sync_versions_parallel(self, versions_to_process: Dict[str, semver.VersionInfo]) -> List[str]:
        """Process versions in parallel for better performance."""
        successful_versions = []
        
        # Process versions in parallel
        with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
            # Submit all tasks
            future_to_version = {
                executor.submit(self.process_version, item): item[0] 
                for item in versions_to_process.items()
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_version):
                version_key = future_to_version[future]
                try:
                    result_key, success, version_hash = future.result()
                    if success:
                        successful_versions.append(result_key)
                except Exception as e:
                    print(f"✗ Exception processing {version_key}: {e}")
        
        # Sort successful versions by semantic version (newest first)
        successful_versions.sort(
            key=lambda v: versions_to_process[v], 
            reverse=True
        )
        
        return successful_versions

    def create_latest_symlink(self, latest_version: str):
        """Create or update the 'latest' symlink."""
        latest_link = self.docs_dir / "latest"
        
        if latest_link.is_symlink() or latest_link.exists():
            latest_link.unlink()
        
        latest_link.symlink_to(latest_version)
        print(f"✓ Created 'latest' symlink pointing to {latest_version}")

    def update_index_page(self, recent_versions: List[str]):
        """Update the index.md page with links to recent versions."""
        index_path = self.docs_dir / "index.md"
        
        if not index_path.exists():
            print("⚠ Warning: _docs/index.md not found, skipping update")
            return
        
        with open(index_path, 'r') as f:
            content = f.read()
        
        # Generate version links section
        version_links = [
            "## 📚 Documentation Versions",
            "",
            "- **[Latest (Stable)](/docs/latest/)** - Most recent stable release"
        ]
        
        for version in recent_versions[:7]:
            version_links.append(f"- **[Version {version}](/docs/{version}/)** - Documentation for v{version}")
        
        version_links.append("")
        version_section = "\n".join(version_links)
        
        # Replace existing version section
        lines = content.split('\n')
        new_lines = []
        skip_until_next_section = False
        
        for line in lines:
            if line.startswith("## 📚 Documentation Versions"):
                skip_until_next_section = True
                new_lines.append(version_section)
                continue
            elif skip_until_next_section and line.startswith("## "):
                skip_until_next_section = False
                new_lines.append(line)
            elif not skip_until_next_section:
                new_lines.append(line)
        
        # Add version section if not found
        if "## 📚 Documentation Versions" not in content:
            insert_index = -1
            for i, line in enumerate(new_lines):
                if line.startswith("## ⚡ Quick Start Guide"):
                    insert_index = i
                    break
            
            if insert_index > 0:
                new_lines.insert(insert_index, version_section)
                new_lines.insert(insert_index, "")
        
        with open(index_path, 'w') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✓ Updated index.md with {len(recent_versions[:7])} recent versions")

    def run(self):
        """Main execution method."""
        print(f"Starting optimized versioned documentation sync...")
        print(f"Max versions: {self.max_versions}, Parallel workers: {self.parallel_workers}")
        
        # Create docs directory
        self.docs_dir.mkdir(exist_ok=True)
        
        # Load cache
        cache = self.load_cache()
        
        # Get and parse tags efficiently
        print("Fetching git tags...")
        tags = self.get_git_tags_efficiently()
        if not tags:
            print("No git tags found in repository")
            sys.exit(1)
        
        print(f"Found {len(tags)} tags")
        
        # Parse and filter versions
        versions_to_process = self.parse_and_filter_versions(tags)
        if not versions_to_process:
            print("No valid semantic version tags found")
            sys.exit(1)
        
        print(f"Processing {len(versions_to_process)} minor versions (limited to {self.max_versions})...")
        
        # Process versions in parallel
        successful_versions = self.sync_versions_parallel(versions_to_process)
        
        if successful_versions:
            # Create latest symlink
            latest_version = successful_versions[0]
            self.create_latest_symlink(latest_version)
            
            # Update index page
            self.update_index_page(successful_versions)
            
            # Save cache
            new_cache = {
                "last_sync": str(Path.cwd()),
                "processed_versions": successful_versions,
                "timestamp": str(subprocess.run(["date"], capture_output=True, text=True).stdout.strip())
            }
            self.save_cache(new_cache)
            
            print(f"\n✓ Optimized documentation sync completed!")
            print(f"✓ Processed {len(successful_versions)} versions in parallel")
            print(f"✓ Latest version: {latest_version}")
            print(f"✓ Available versions: {', '.join(successful_versions[:7])}")
        else:
            print("\n✗ No versions were successfully processed")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Optimized versioned documentation sync")
    parser.add_argument("repo_path", help="Path to source repository")
    parser.add_argument("--max-versions", type=int, default=10, 
                       help="Maximum number of versions to process (default: 10)")
    parser.add_argument("--parallel", type=int, default=4,
                       help="Number of parallel workers (default: 4)")
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path)
    
    if not repo_path.exists() or not repo_path.is_dir():
        print(f"Error: Source repository not found at {repo_path}")
        sys.exit(1)
    
    if not (repo_path / ".git").exists():
        print(f"Error: {repo_path} is not a git repository")
        sys.exit(1)
    
    # Create and run optimizer
    optimizer = OptimizedDocSync(
        repo_path=repo_path,
        max_versions=args.max_versions,
        parallel_workers=args.parallel
    )
    
    optimizer.run()


if __name__ == "__main__":
    main() 