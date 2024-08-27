"""Main entry point for the NeuroWallpaper application"""
import argparse

import app

parser = argparse.ArgumentParser(
    description="NeuroWallpaper is a tool to set desktop wallpapers using AI generated images"
)
parser.add_argument(
    "-s", "--startup",
    dest="startup",
    help="Flag if application has been run at system startup",
    action="store_true",
    default=False
)
args = parser.parse_args()

if __name__ == '__main__':
    app.run(on_startup=args.startup)
