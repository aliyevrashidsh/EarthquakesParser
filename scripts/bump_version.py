#!/usr/bin/env python3
"""Version bumping and changelog generation script.

This script:
1. Analyzes commits since last tag
2. Determines version bump type (major/minor/patch)
3. Updates version in pyproject.toml and __init__.py
4. Updates CHANGELOG.md
5. Creates a git tag
"""

import argparse
import re
import subprocess  # nosec B404
from datetime import date
from pathlib import Path
from typing import List, Tuple


class VersionBumper:
    """Handle version bumping and changelog generation."""

    def __init__(self, project_root: Path):
        """Initialize version bumper.

        Args:
            project_root: Path to project root directory
        """
        self.project_root = project_root
        self.pyproject_path = project_root / "pyproject.toml"
        self.init_path = project_root / "earthquakes_parser" / "__init__.py"
        self.changelog_path = project_root / "CHANGELOG.md"

    def get_current_version(self) -> str:
        """Get current version from __init__.py."""
        content = self.init_path.read_text()
        match = re.search(r'__version__ = "([^"]+)"', content)
        if not match:
            raise ValueError("Could not find version in __init__.py")
        return match.group(1)

    def get_commits_since_last_tag(self) -> List[str]:
        """Get commits since last tag."""
        try:
            # Get last tag
            result = subprocess.run(  # nosec B603, B607
                ["git", "describe", "--tags", "--abbrev=0"],
                capture_output=True,
                text=True,
                check=True,
            )
            last_tag = result.stdout.strip()

            # Get commits since last tag
            result = subprocess.run(  # nosec B603, B607
                ["git", "log", f"{last_tag}..HEAD", "--pretty=format:%s"],
                capture_output=True,
                text=True,
                check=True,
            )
            commits = result.stdout.strip().split("\n")
            return [c for c in commits if c]

        except subprocess.CalledProcessError:
            # No tags yet, get all commits
            result = subprocess.run(  # nosec B603, B607
                ["git", "log", "--pretty=format:%s"],
                capture_output=True,
                text=True,
                check=True,
            )
            commits = result.stdout.strip().split("\n")
            return [c for c in commits if c]

    def analyze_commits(self, commits: List[str]) -> Tuple[str, dict]:
        """Analyze commits to determine version bump type.

        Args:
            commits: List of commit messages

        Returns:
            Tuple of (bump_type, categorized_commits)
        """
        bump_type = "patch"  # Default to patch
        categories: dict[str, list[str]] = {
            "feat": [],
            "fix": [],
            "docs": [],
            "style": [],
            "refactor": [],
            "perf": [],
            "test": [],
            "build": [],
            "ci": [],
            "chore": [],
            "revert": [],
        }

        for commit in commits:
            # Check for breaking changes
            if "BREAKING CHANGE" in commit or commit.startswith("!"):
                bump_type = "major"

            # Parse commit type
            match = re.match(r"^(\w+)(?:\([\w-]+\))?(!)?:", commit)
            if match:
                commit_type = match.group(1)
                has_breaking = match.group(2) == "!"

                if has_breaking:
                    bump_type = "major"
                elif commit_type == "feat" and bump_type == "patch":
                    bump_type = "minor"

                if commit_type in categories:
                    categories[commit_type].append(commit)

        return bump_type, categories

    def bump_version(self, current: str, bump_type: str) -> str:
        """Bump version number.

        Args:
            current: Current version string
            bump_type: Type of bump (major/minor/patch)

        Returns:
            New version string
        """
        major, minor, patch = map(int, current.split("."))

        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1

        return f"{major}.{minor}.{patch}"

    def update_version_files(self, new_version: str):
        """Update version in project files.

        Args:
            new_version: New version string
        """
        # Update __init__.py
        content = self.init_path.read_text()
        content = re.sub(
            r'__version__ = "[^"]+"',
            f'__version__ = "{new_version}"',
            content,
        )
        self.init_path.write_text(content)
        print(f"✓ Updated {self.init_path}")

        # Update pyproject.toml
        content = self.pyproject_path.read_text()
        content = re.sub(
            r'version = "[^"]+"',
            f'version = "{new_version}"',
            content,
        )
        self.pyproject_path.write_text(content)
        print(f"✓ Updated {self.pyproject_path}")

    def update_changelog(self, version: str, categories: dict):
        """Update CHANGELOG.md with new version.

        Args:
            version: New version string
            categories: Categorized commits
        """
        content = self.changelog_path.read_text()

        # Build changelog entry
        today = date.today().strftime("%Y-%m-%d")
        entry = f"\n## [{version}] - {today}\n\n"

        # Add sections with commits
        section_titles = {
            "feat": "### Added",
            "fix": "### Fixed",
            "docs": "### Documentation",
            "perf": "### Performance",
            "refactor": "### Refactored",
            "style": "### Style",
            "test": "### Tests",
            "build": "### Build",
            "ci": "### CI/CD",
            "chore": "### Chore",
            "revert": "### Reverted",
        }

        for commit_type, title in section_titles.items():
            commits = categories.get(commit_type, [])
            if commits:
                entry += f"\n{title}\n\n"
                for commit in commits:
                    # Extract just the description part
                    desc = re.sub(r"^\w+(?:\([\w-]+\))?!?:\s*", "", commit)
                    entry += f"- {desc}\n"

        # Insert after the "# Changelog" header
        lines = content.split("\n")
        insert_index = next(
            (i for i, line in enumerate(lines) if line.startswith("## [")), 2
        )

        lines.insert(insert_index, entry.strip())
        self.changelog_path.write_text("\n".join(lines))
        print(f"✓ Updated {self.changelog_path}")

    def create_tag(self, version: str, dry_run: bool = False):
        """Create git tag for new version.

        Args:
            version: Version string
            dry_run: If True, don't actually create tag
        """
        tag = f"v{version}"

        if dry_run:
            print(f"[DRY RUN] Would create tag: {tag}")
            return

        subprocess.run(  # nosec B603, B607
            ["git", "tag", "-a", tag, "-m", f"Release version {version}"],
            check=True,
        )
        print(f"✓ Created tag: {tag}")
        print(f"\nTo push the tag, run: git push origin {tag}")


def main():
    """Run version bump and changelog update."""
    parser = argparse.ArgumentParser(description="Bump version and update changelog")
    parser.add_argument(
        "--type",
        choices=["major", "minor", "patch", "auto"],
        default="auto",
        help="Version bump type (default: auto-detect from commits)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--no-tag",
        action="store_true",
        help="Don't create git tag",
    )
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    bumper = VersionBumper(project_root)

    # Get current version
    current_version = bumper.get_current_version()
    print(f"Current version: {current_version}")

    # Get commits and analyze
    commits = bumper.get_commits_since_last_tag()
    print(f"\nFound {len(commits)} commits since last tag")

    if not commits:
        print("No commits to process!")
        return

    # Determine bump type
    if args.type == "auto":
        bump_type, categories = bumper.analyze_commits(commits)
        print(f"Auto-detected bump type: {bump_type}")
    else:
        bump_type = args.type
        _, categories = bumper.analyze_commits(commits)
        print(f"Using specified bump type: {bump_type}")

    # Calculate new version
    new_version = bumper.bump_version(current_version, bump_type)
    print(f"New version: {new_version}")

    if args.dry_run:
        print("\n[DRY RUN MODE - No changes will be made]\n")
        print(f"Would update version: {current_version} → {new_version}")
        print(f"Would update: {bumper.init_path}")
        print(f"Would update: {bumper.pyproject_path}")
        print(f"Would update: {bumper.changelog_path}")
        if not args.no_tag:
            print(f"Would create tag: v{new_version}")
        return

    # Update files
    print("\nUpdating files...")
    bumper.update_version_files(new_version)
    bumper.update_changelog(new_version, categories)

    # Create tag
    if not args.no_tag:
        print("\nCreating git tag...")
        bumper.create_tag(new_version)

    print("\n✅ Version bump complete!")
    print("\nNext steps:")
    print("1. Review changes: git diff")
    commit_msg = f"chore: bump version to {new_version}"
    print(f"2. Commit changes: git add . && git commit -m '{commit_msg}'")
    if not args.no_tag:
        print(f"3. Push tag: git push origin v{new_version}")


if __name__ == "__main__":
    main()
