"""---------------
App config data
---------------"""

from pathlib import Path


# Application name string
APP_NAME = " Application Name"
# Base application path
BASE_PATH = Path(__file__).resolve().parent.parent
# Path to storage directory
STORAGE_PATH = BASE_PATH / "store"
# Path to assets directory
ASSETS_PATH = BASE_PATH / "assets"
# Path to sounds directory
SOUNDS_PATH = ASSETS_PATH / "sounds"
# Path to images directory
IMAGES_PATH = ASSETS_PATH / "images"

# GUI images
IMAGE_FILES = {
    "app-logo"      : "app-logo-24.png",
    "start-process" : "play-circled-light-24.png",
    "stop-process"  : "stop-circled-light-24.png",
    "add-image"     : "add-image-light-24.png",
    "add-video"     : "add-video-light-24.png",
    "settings"      : "settings-light-24.png",
}

# Allowed image file extensions
ALLOWED_IMAGE = [".bmp", ".png", ".jpg", ".jpeg"]
# Allowed video file extensions
ALLOWED_VIDEO = [".mov", ".mp4", ".wmv", ".avi"]

# Help content
HEPL_TEXT = """
Single line of help text
""" * 50

