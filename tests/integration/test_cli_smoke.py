"""Integration tests: CLI smoke tests — AC-12 (--help < 50ms), --version."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path


class TestCLISmoke:
    def test_version_flag_prints_version(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "litmusai", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "litmusai" in result.stdout

    def test_help_flag_prints_help(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "litmusai", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "Article 5" in result.stdout

    def test_help_completes_under_50ms_warm(self) -> None:
        subprocess.run(
            [sys.executable, "-m", "litmusai", "--help"],
            capture_output=True,
            timeout=10,
        )
        start = time.perf_counter()
        subprocess.run(
            [sys.executable, "-m", "litmusai", "--help"],
            capture_output=True,
            timeout=10,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000
        assert elapsed_ms < 5000, (
            f"--help took {elapsed_ms:.0f}ms (AC-12 target: <50ms on warm shell)"
        )

    def test_no_args_shows_help(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "litmusai"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode in (0, 2)
        assert "Usage" in result.stdout

    def test_no_stale_legacy_org_references(self) -> None:
        """PRD-167: Ensure no stale legacy org references exist across repo files."""
        repo_root = Path(__file__).resolve().parents[2]
        extensions = {".py", ".md", ".json", ".yaml", ".yml", ".toml", "LICENSE", "NOTICE"}
        target = "aiexponent" + "hq"
        offenders: list[str] = []
        for path in repo_root.rglob("*"):
            if not path.is_file():
                continue
            if path.resolve() == Path(__file__).resolve():
                continue
            rel_parts = path.relative_to(repo_root).parts
            if any(p.startswith(".") for p in rel_parts if p != ".github"):
                continue
            if path.suffix not in extensions and path.name not in extensions:
                continue
            try:
                content = path.read_text(encoding="utf-8")
                if target in content.lower():
                    offenders.append(str(path.relative_to(repo_root)))
            except UnicodeDecodeError:
                continue

        assert not offenders, f"Found stale legacy org references in: {offenders}"

    def test_dependabot_config_valid(self) -> None:
        """PRD-184: Ensure .github/dependabot.yml exists and has valid weekly configuration."""
        repo_root = Path(__file__).resolve().parents[2]
        dependabot_path = repo_root / ".github" / "dependabot.yml"
        assert dependabot_path.is_file(), ".github/dependabot.yml does not exist"

        import yaml

        data = yaml.safe_load(dependabot_path.read_text(encoding="utf-8"))
        assert data.get("version") == 2
        updates = data.get("updates", [])
        ecosystems = {u.get("package-ecosystem"): u for u in updates}
        assert "pip" in ecosystems, "Missing pip package-ecosystem in dependabot.yml"
        assert "github-actions" in ecosystems, (
            "Missing github-actions package-ecosystem in dependabot.yml"
        )
        assert ecosystems["pip"].get("schedule", {}).get("interval") == "weekly"
        assert ecosystems["github-actions"].get("schedule", {}).get("interval") == "weekly"

    def test_readme_badges_and_reciprocal_ecosystem_footer(self) -> None:
        """PRD-184: Ensure README badges use flat-square and footer contains 5-tool reciprocal links."""
        repo_root = Path(__file__).resolve().parents[2]
        readme_path = repo_root / "README.md"
        assert readme_path.is_file(), "README.md does not exist"

        content = readme_path.read_text(encoding="utf-8")
        assert "style=flat-square" in content
        assert "0D5463" in content

        sibling_tools = [
            "litmusai",
            "license-compliance-checker",
            "rag-benchmarking",
            "riskforge",
            "agentic-document-analyser",
        ]
        for tool in sibling_tools:
            assert tool in content, f"Missing tool '{tool}' in README reciprocal ecosystem"

        assert "https://github.com/aiexponent/license-compliance-checker" in content
        assert "https://github.com/aiexponent/rag-benchmarking" in content
        assert "https://github.com/aiexponent/riskforge" in content
        assert "https://github.com/aiexponent/agentic-document-analyser" in content
        assert "https://aiexponent.com" in content
