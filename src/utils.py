import re
from pathlib import Path

OUTPUT_DIR = Path("generated_assets")


def create_output_directory():
    output_path = OUTPUT_DIR
    if output_path.exists() and not output_path.is_dir():
        raise RuntimeError(
            f"Expected '{output_path}' to be a directory, but found a file. "
            "Rename or remove it, then try again."
        )
    output_path.mkdir(exist_ok=True)


def print_banner():

    print("\n")
    print("=" * 50)
    print("CYBERPUNK BRAND IMAGE GENERATOR")
    print("=" * 50)
    print("\n")


def slugify_filename(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    normalized = normalized.strip("_")
    return normalized or "asset"
