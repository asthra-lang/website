#!/usr/bin/env python3

"""
Versioned documentation sync script
Usage: python sync-docs.py <source_repo_path>
Example: python sync-docs.py ../asthra (for local)
Example: python sync-docs.py temp-asthra (for CI)

This script:
1. Fetches all git tags from the source repository
2. Filters for semantic version tags (removes 'v' prefix)
3. Groups by minor versions and selects latest patch for each
4. Excludes pre-release versions (beta, rc, etc.)
5. Creates versioned documentation directories
6. Creates 'latest' symlink pointing to the most recent stable release
7. Updates index.md with links to recent versions
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import semver


def run_git_command(repo_path: Path, command: List[str]) -> str:
    """Run a git command in the specified repository."""
    try:
        result = subprocess.run(
            ["git"] + command,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        print(f"Error output: {e.stderr}")
        return ""


def get_git_tags(repo_path: Path) -> List[str]:
    """Get all git tags from the repository."""
    output = run_git_command(repo_path, ["tag", "-l"])
    if not output:
        return []
    return [tag.strip() for tag in output.split('\n') if tag.strip()]


def parse_version_tags(tags: List[str]) -> List[semver.VersionInfo]:
    """Parse version tags, removing 'v' prefix and filtering valid semver."""
    versions = []
    for tag in tags:
        # Remove 'v' prefix if present
        version_str = tag[1:] if tag.startswith('v') else tag
        
        try:
            # Parse as semantic version
            version = semver.VersionInfo.parse(version_str)
            # Skip pre-release versions (beta, rc, etc.)
            if version.prerelease is None:
                versions.append(version)
        except ValueError:
            # Skip invalid version tags
            continue
    
    return versions


def group_by_minor_version(versions: List[semver.VersionInfo]) -> Dict[str, semver.VersionInfo]:
    """Group versions by minor version and return the latest patch for each."""
    minor_versions = {}
    
    for version in versions:
        minor_key = f"{version.major}.{version.minor}"
        
        if minor_key not in minor_versions or version > minor_versions[minor_key]:
            minor_versions[minor_key] = version
    
    return minor_versions


def checkout_version(repo_path: Path, version: semver.VersionInfo) -> bool:
    """Checkout a specific version tag in the repository."""
    tag = f"v{version}"
    
    # First check if the tag exists
    tags = run_git_command(repo_path, ["tag", "-l", tag])
    if not tags:
        print(f"  ⚠ Tag {tag} not found in repository")
        return False
    
    # Try to checkout the tag
    result = run_git_command(repo_path, ["checkout", tag, "--quiet"])
    if not result and result is not None:
        # Check if checkout was successful by verifying current HEAD
        current_tag = run_git_command(repo_path, ["describe", "--tags", "--exact-match"])
        return current_tag == tag
    return result != ""


def copy_docs_for_version(repo_path: Path, version_key: str, doc_dirs: List[str]) -> bool:
    """Copy documentation for a specific version."""
    docs_dir = Path("_docs")
    version_dir = docs_dir / version_key
    
    # Create version directory
    version_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove existing docs in version directory
    for dir_name in doc_dirs:
        target_dir = version_dir / dir_name
        if target_dir.exists():
            shutil.rmtree(target_dir)
    
    # Copy documentation directories
    success = True
    for dir_name in doc_dirs:
        source_dir = repo_path / "docs" / dir_name
        target_dir = version_dir / dir_name
        
        if source_dir.exists() and source_dir.is_dir():
            shutil.copytree(source_dir, target_dir)
            print(f"✓ Copied {dir_name} docs for version {version_key}")
        else:
            print(f"⚠ Warning: {dir_name} docs not found for version {version_key}")
            success = False
    
    return success


def create_latest_symlink(latest_version: str):
    """Create or update the 'latest' symlink."""
    docs_dir = Path("_docs")
    latest_link = docs_dir / "latest"
    
    # Remove existing symlink if it exists
    if latest_link.is_symlink() or latest_link.exists():
        latest_link.unlink()
    
    # Create new symlink
    latest_link.symlink_to(latest_version)
    print(f"✓ Created 'latest' symlink pointing to {latest_version}")


def update_index_page(recent_versions: List[str]):
    """Update the index.md page with links to recent versions."""
    index_path = Path("_docs/index.md")
    
    if not index_path.exists():
        print("⚠ Warning: _docs/index.md not found, skipping update")
        return
    
    # Read current content
    with open(index_path, 'r') as f:
        content = f.read()
    
    # Generate version links section
    version_links = []
    version_links.append("## 📚 Documentation Versions")
    version_links.append("")
    version_links.append("- **[Latest (Stable)](/docs/latest/)** - Most recent stable release")
    
    for version in recent_versions[:7]:  # Maximum 7 versions
        version_links.append(f"- **[Version {version}](/docs/{version}/)** - Documentation for v{version}")
    
    version_links.append("")
    version_section = "\n".join(version_links)
    
    # Replace or add version section
    # Look for existing version section and replace it
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
    
    # If no version section was found, add it after the welcome section
    if "## 📚 Documentation Versions" not in content:
        # Find where to insert (after the welcome paragraph)
        insert_index = -1
        for i, line in enumerate(new_lines):
            if line.startswith("## ⚡ Quick Start Guide"):
                insert_index = i
                break
        
        if insert_index > 0:
            new_lines.insert(insert_index, version_section)
            new_lines.insert(insert_index, "")
    
    # Write updated content
    with open(index_path, 'w') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✓ Updated index.md with {len(recent_versions[:7])} recent versions")


def main():
    if len(sys.argv) != 2:
        print("Error: Source repository path is required")
        print(f"Usage: {sys.argv[0]} <source_repo_path>")
        sys.exit(1)
    
    source_repo_path = Path(sys.argv[1])
    
    if not source_repo_path.exists() or not source_repo_path.is_dir():
        print(f"Error: Source repository not found at {source_repo_path}")
        sys.exit(1)
    
    # Check if it's a git repository
    if not (source_repo_path / ".git").exists():
        print(f"Error: {source_repo_path} is not a git repository")
        sys.exit(1)
    
    print("Starting versioned documentation sync...")
    
    # Create _docs directory if it doesn't exist
    docs_dir = Path("_docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Get all git tags
    print("Fetching git tags...")
    tags = get_git_tags(source_repo_path)
    if not tags:
        print("No git tags found in repository")
        sys.exit(1)
    
    print(f"Found {len(tags)} tags")
    
    # Parse version tags
    versions = parse_version_tags(tags)
    if not versions:
        print("No valid semantic version tags found")
        sys.exit(1)
    
    print(f"Found {len(versions)} valid semantic version tags")
    
    # Group by minor version and get latest patch for each
    minor_versions = group_by_minor_version(versions)
    
    # Sort versions (newest first)
    sorted_versions = sorted(minor_versions.items(), key=lambda x: minor_versions[x[0]], reverse=True)
    
    print(f"Processing {len(sorted_versions)} minor versions...")
    
    # Documentation directories to sync
    doc_dirs = ["contributor", "spec", "stdlib", "user-manual"]
    
    # Store current branch/commit to restore later
    current_ref = run_git_command(source_repo_path, ["rev-parse", "HEAD"])
    
    successful_versions = []
    
    try:
        # Process each minor version
        for version_key, version in sorted_versions:
            print(f"\nProcessing version {version_key} (tag: v{version})...")
            
            # Checkout the specific version
            if checkout_version(source_repo_path, version):
                # Copy documentation
                if copy_docs_for_version(source_repo_path, version_key, doc_dirs):
                    successful_versions.append(version_key)
                    print(f"✓ Successfully processed version {version_key}")
                else:
                    print(f"⚠ Partial success for version {version_key}")
            else:
                print(f"✗ Failed to checkout version {version_key}")
    
    finally:
        # Restore original branch/commit
        if current_ref:
            run_git_command(source_repo_path, ["checkout", current_ref])
            print(f"\n✓ Restored repository to original state")
    
    if successful_versions:
        # Create 'latest' symlink pointing to the most recent version
        latest_version = successful_versions[0]
        create_latest_symlink(latest_version)
        
        # Update index.md with recent versions
        update_index_page(successful_versions)
        
        print(f"\n✓ Documentation sync completed successfully!")
        print(f"✓ Processed {len(successful_versions)} versions")
        print(f"✓ Latest version: {latest_version}")
        print(f"✓ Available versions: {', '.join(successful_versions[:7])}")
    else:
        print("\n✗ No versions were successfully processed")
        sys.exit(1)


if __name__ == "__main__":
    main() 