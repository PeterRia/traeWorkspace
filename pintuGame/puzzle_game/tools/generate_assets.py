import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src import asset_generator


def main():
    generated = asset_generator.ensure_assets(force="--force" in sys.argv)
    if generated:
        print("generated:")
        for path in generated:
            print(path)
    else:
        print("assets already exist")


if __name__ == "__main__":
    main()
