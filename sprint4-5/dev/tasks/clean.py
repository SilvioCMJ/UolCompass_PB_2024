import os
import shutil


def clean_cache() -> None:
    """Remove __pycache__ and .pytest_cache directories."""
    cache_dirs = ["__pycache__", ".pytest_cache"]
    for root, dirs, _ in os.walk("."):
        [
            shutil.rmtree(os.path.join(root, cache_dir))
            for cache_dir in cache_dirs
            if cache_dir in dirs
        ]


def clean_coverage() -> None:
    """Remove .coverage file and htmlcov directory."""
    if os.path.exists(".coverage"):
        os.remove(".coverage")
    if os.path.exists("htmlcov"):
        shutil.rmtree("htmlcov")


def clean_all() -> None:
    """Clean both cache and coverage files."""
    clean_coverage()
    clean_cache()
    print("Cleaned Cache.")
