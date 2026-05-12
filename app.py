from src.generator import ImageGenerator
from src.prompts import ASSETS, NEGATIVE_PROMPT
from src.utils import create_output_directory, print_banner


def main():
    create_output_directory()
    print_banner()

    generator = ImageGenerator()

    for asset in ASSETS:
        print(f"Generating {asset['name']}...")

        output_path = generator.generate_image(
            prompt=asset["prompt"].strip(),
            negative_prompt=NEGATIVE_PROMPT,
            filename=asset["filename"],
            width=asset["width"],
            height=asset["height"]
        )

        print(f"Saved: {output_path}\n")

    print("All Images Generated Successfully!")


if __name__ == "__main__":
    main()
