import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def run_script(script_name):
    """Run a Python script and stop if it fails."""
    script_path = BASE_DIR / script_name

    print("\n" + "=" * 70)
    print(f"Running {script_name}")
    print("=" * 70)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{script_name} failed with exit code {result.returncode}"
        )


def main():
    run_script("scraper.py")
    run_script("database.py")
    run_script("queries.py")

    print("\n" + "=" * 70)
    print("FULL DATA PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()