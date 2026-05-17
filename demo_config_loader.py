"""Demo script to explore config data structure."""

import json
from pathlib import Path

from nbry_lifting_website.lib.config_loader import ConfigLoader


def main():
    loader = ConfigLoader("src/nbry_lifting_website/configs")

    print("=" * 60)
    print("PROGRAM.TOML")
    print("=" * 60)
    program = loader.load("program.toml")
    print(json.dumps(program, indent=2))

    print("\n" + "=" * 60)
    print("BLOCKS/ACCUMULATION.TOML (First Day Only)")
    print("=" * 60)
    block = loader.load("blocks/accumulation.toml")
    print(f"Block Name: {block['name']}")
    print(f"Number of Days: {len(block['days'])}")
    print(f"\nFirst Day ({block['days'][0]['name']}):")
    print(json.dumps(block["days"][0], indent=2))

    print("\n" + "=" * 60)
    print("EXERCISES.TOML (First 3 Exercises)")
    print("=" * 60)
    exercises = loader.load("exercises.toml")
    for i, (name, data) in enumerate(list(exercises.items())[:3]):
        print(f"\n{name}:")
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
