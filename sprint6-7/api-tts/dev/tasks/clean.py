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


if __name__ == "__main__":
    clean_cache()