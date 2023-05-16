"""----------------------
Application Controllers:
1. HelpController
2. StartingController
3. StoppingController
4. AddVideoController
5. VideoPreviewController
6. AddImageController
7. ImagePreviewController
8. SettingsController
----------------------"""

import os

from tkinter import filedialog
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.dialogs import MessageDialog

from config.gui import STORAGE_PATH, HEPL_TEXT, ALLOWED_IMAGE, ALLOWED_VIDEO
from sounds import AppSound
import jsondata as store
from modals import *


class HelpController:
    """ Show the help popup window.
    """
    def main(event=None, master=None):
        """ Congfigures and opens the modal window.
        """
        hmodal = HelpModal(
            master,
            title="Help",
            text=HEPL_TEXT
        )
        hmodal.show()


class StartingController:
    """ Starts the main process.
        Return: tuple|False
    """
    def main(master=None):
        store.FILE_PATH = STORAGE_PATH / "image.json"
        image = store.get_data('source_path')
        if not image:
            Messagebox.show_warning(
                title="Missing Image File",
                message="First click <Add image> button to choose a file"
            )
            return False
        store.FILE_PATH = STORAGE_PATH / "video.json"
        video = store.get_data('source_path')
        if not video:
            Messagebox.show_warning(
                title="Missing Video File",
                message="First click <Add video> button to choose a file"
            )
            return False
        return (image, video)


class StoppingController:
    """ Stops the main process.
    """
    def main(master=None):
        store.FILE_PATH = STORAGE_PATH / "settings.json"
        if store.get_data("play_sound") == "on":
            sound = AppSound()
            sound.scaner_sound.play()
        return True


class AddVideoController:
    """ Gets the path to video file.
    """
    def main(master=None):
        """ Opens the modal window (dialog).
        """
        store.FILE_PATH = STORAGE_PATH / "video.json"
        if source_path := store.get_data('source_path'):
            message = f"You have a previously selected video file that can be reused:\n <{source_path}>"
            buttons = ['Choose Another File:outline', 'Use Existing File:primary']
            dialog = MessageDialog(
                message,
                title="Select an Action",
                buttons=buttons,
                width=40
            )
            dialog.show()
            response = dialog.result
            if response.lower() == "choose another file":
                source_path = filedialog.askopenfilename()
        else:
            source_path = filedialog.askopenfilename()
        if source_path:
            # Check file type (extension)
            _, file_extension = os.path.splitext(source_path)
            if file_extension not in ALLOWED_VIDEO:
                Messagebox.show_error(
                    title="Wrong File Type",
                    message=f"Only {ALLOWED_VIDEO} file extensions allowed!"
                )
                return False
            # Save file path in data storage
            store.set_data({'source_path':source_path})
        return source_path


class VideoPreviewController:
    """ Preview of the selected video
    """
    def main(master=None):
        """ Opens video in the modal window.
        """
        store.FILE_PATH = STORAGE_PATH / "video.json"
        source_path = store.get_data('source_path')
        # Check if file exists
        if not os.path.exists(source_path):
            Messagebox.show_error(
                title="Video File is Not Found",
                message=f"Can't find <{source_path}>\n!"
            )
            return False

        # Configure and open the modal window
        vim = VideoModal(master, "Video Preview", source_path)
        vim.show()


class AddImageController:
    """ Getting the path to image source file.
    """
    def main(master=None):
        """ Opens the modal window (dialog).
        """
        store.FILE_PATH = STORAGE_PATH / "image.json"
        if source_path := store.get_data('source_path'):
            message = f"You have a previously selected image source that can be reused:\n <{source_path}>"
            buttons = ["Сhoose Another File:outline", "Use Existing File:primary"]
            dialog = MessageDialog(
                message,
                title="Select an Action",
                buttons=buttons,
                width=40
            )
            dialog.show()
            response = dialog.result
            if response == "Сhoose Another File":
                source_path = filedialog.askopenfilename()
        else:
            source_path = filedialog.askopenfilename()
        if source_path:
            # Check file type (extension)
            _, file_extension = os.path.splitext(source_path)
            if file_extension not in ALLOWED_IMAGE:
                Messagebox.show_error(
                    title="Wrong File Type",
                    message=f"Only {ALLOWED_IMAGE} file extensions allowed!"
                )
                return False
            # Save file path in data storage
            store.set_data({'source_path':source_path})
        return source_path


class ImagePreviewController:
    """ Preview of the selected image
    """
    def main(master=None):
        """ Opens image in the modal window.
        """
        store.FILE_PATH = STORAGE_PATH / "image.json"
        source_path = store.get_data('source_path')
        # Check if file exists
        if not os.path.exists(source_path):
            Messagebox.show_error(
                title="Image File is Not Found",
                message=f"Can't find <{source_path}>\n!"
            )
            return False
        # Configure and open the modal window
        imm = ImageModal(master, "Image Preview", source_path)
        imm.show()


class SettingsController:
    """ App settings controls
    """
    def main(master=None):
        """ Opens the modal window (dialog).
        """
        store.FILE_PATH = STORAGE_PATH / "settings.json"
        settings = SettingsModal(
            master,
            "Application Settings",
            data=store.get_data()
        )
        settings.show()
        if data := settings.result:
            store.set_data(data)

