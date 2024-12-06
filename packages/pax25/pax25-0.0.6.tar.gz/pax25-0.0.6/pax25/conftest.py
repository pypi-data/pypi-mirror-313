"""
This file runs before tests are collected in order to set up the repository for tests.
"""

from os import sep
from pathlib import Path

# Delete all test output files before beginning so we don't pass a test based on a
# previous run's output.
for path in Path(".").rglob(f"**{sep}tests{sep}output{sep}*.txt"):
    path.unlink()
for path in Path(".").rglob(f"**{sep}tests{sep}output{sep}*.json"):
    path.unlink()
