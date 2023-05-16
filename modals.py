"""--------------------------------------------------
1. HelpModal      -  for displaying the help text
2. VideoModal     -  for a preview of the selected video
3. ImageModal     -  for a preview of the selected image
4. SettingsModal  -  for managing the application settings
-------------------------------------------------- """

import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Dialog
from ttkbootstrap.scrolled import ScrolledText

from PIL import ImageTk, Image, ImageOps
import imageio.v3 as iio
from math import sqrt
import threading
import time
import sys


class HelpModal(Dialog):
    """ Messagebox with ScrolledText widget.
    """
    def __init__(self, parent, title, text):
        super().__init__(parent, title)
        self._text = text

    def create_body(self, master):
        """ Overridden from Dialog.
        """
        self._toplevel.geometry("350x600")

        scrolled_text = ScrolledText(
            master,
            autohide=True,
            font=("Sans-serif", 10)
        )
        scrolled_text.pack(fill=BOTH, expand=YES)
        scrolled_text.insert(END, self._text)
        scrolled_text._text.configure(state=DISABLED)

    def create_buttonbox(self, master):
        """ Overridden from Dialog.
        """
        pass


class VideoModal(Dialog):
    """ Modal window for a video preview.
    """
    def __init__(self, parent, title, path):
        super().__init__(parent, title)
        self.title = title
        self.path = path
        self.meta = {}

    def get_resizes(self, master):
        """ Determines if there is a need for resizing and new frame sizes.
        """
        # Get screen dimensions
        screen_w = master.winfo_screenwidth()
        screen_h = master.winfo_screenheight()

        # Get original video frame dimensions
        metadata = iio.immeta(self.path, exclude_applied=False)
        frame_w, frame_h = metadata.get('size', (0, 0))

        self.meta = {
            'size': (frame_w, frame_h),
            'fps': metadata.get('fps', 0),
            'duration': metadata.get('duration', 0)
        }

        # The area covered by the window on the screen
        window_area = .35
        vector = sqrt(window_area)

        # Calc the modal window dimensions
        window_w = int(screen_w * vector)
        window_h = int(screen_h * vector)

        # If at least one of the dimensions exceeds the window size
        if frame_w > window_w or frame_h > window_h:
            # Calc the ratio of image resizing
            if (frame_w / window_w) >= (frame_h / window_h):
                ratio = round((window_w / frame_w), 6)
            else:
                ratio = round((window_h / frame_h), 6)
            # Calculating new image size
            width = round(frame_w * ratio)
            height = round(frame_h * ratio)
            return True, (width, height)
        else:
            return False, (None, None)

    def create_body(self, master):
        """ Overridden from Dialog.
        """
        # Get data for resizing
        toresize, sizes = self.get_resizes(master)

        # Label text (at top of the window)
        sep = " | "
        text = f"Original size: {self.meta['size']}" \
               f" {sep} Fps: {self.meta['fps']}" \
               f" {sep} Duration: {self.meta['duration']}"

        # Label for displaying video as frame images
        image_label = ttk.Label(
            master,
            text = text,
            compound=BOTTOM,
            font=("Sans-serif", 10, "bold")
        )
        image_label.pack()

        # Thread function
        def stream(label):
            # Time in frame, sec
            if self.meta['fps'] >= 24:
                fsec = 1 / 24
            else:
                fsec = 1 / self.meta['fps']
            # Loop start time
            now = time.time()
            for frame in iio.imiter(self.path, plugin="pyav"):
                then = time.time()
                if (then - now) < fsec:
                    time.sleep(fsec - (then - now))
                now = then
                # Frame to image convert
                image = Image.fromarray(frame)
                # Кesize the image if necessary
                if toresize:
                    w = sizes[0]
                    h = sizes[1]
                    image = ImageOps.contain(image, (w, h), Image.NEAREST)
                try:
                    imgtk = ImageTk.PhotoImage(image)
                    label.config(image=imgtk)
                    label.image = imgtk
                except:
                    sys.exit(1)

        # Starting the thread
        thread = threading.Thread(target=stream, args=(image_label,))
        thread.setDaemon(True)
        thread.start()


    def create_buttonbox(self, master):
        """ Overridden from Dialog.
        """
        pass


class ImageModal(Dialog):
    """ Modal window for image preview.
    """
    def __init__(self, parent, title, path):
        super().__init__(parent, title)
        self.title = title
        self.path = path

    def create_body(self, master):
        """ Overridden from Dialog.
        """
        image = Image.open(self.path)
        image_w, image_h = image.size

        # Get screen dimensions
        screen_w = master.winfo_screenwidth()
        screen_h = master.winfo_screenheight()

        # The area covered by the window on the screen
        window_area = .35
        vector = sqrt(window_area)

        # Calc the modal window dimensions
        window_w = int(screen_w * vector)
        window_h = int(screen_h * vector)

        # If at least one of the image dimensions exceeds the window size
        if image_w > window_w or image_h > window_h:
            # Calc the ratio of image resizing
            if (image_w / window_w) >= (image_h / window_h):
                ratio = round((window_w / image_w), 6)
            else:
                ratio = round((window_h / image_h), 6)
            # Calculating new image size
            w = round(image_w * ratio)
            h = round(image_h * ratio)
            image = image.resize((w, h), Image.Resampling.LANCZOS)

        imgtk = ImageTk.PhotoImage(image)
        text = f"Original size: {image_w} x{image_h} px"

        label = ttk.Label(
            master,
            text=text,
            image=imgtk,
            compound=BOTTOM,
            font=("Sans-serif", 10, "bold")
        )
        label.image = imgtk
        label.pack()

    def create_buttonbox(self, master):
        """ Overridden from Dialog.
        """
        pass


class SettingsModal(Dialog):
    """ Form for application settings.
    """
    def __init__(self, parent, title, data={}):
        super().__init__(parent, title)
        self._play_sound = ttk.StringVar(value=data.get('play_sound', 'off'))
        self._s2 = ttk.StringVar(value=data.get('s2', 'off'))
        self._s3 = ttk.StringVar(value=data.get('s3', '10'))
        self._s4 = ttk.StringVar(value=data.get('s4', 'Option A'))

    def create_body(self, master):
        """ Overridden from Dialog.
        """
        self._toplevel.geometry('350x600')

        # Body container
        frame = ttk.Frame(master)
        frame.pack(fill=X, padx=10)

        # Form header
        ttk.Label(
            master=frame,
            text=self._title,
            font="-weight bold"
        ).pack(pady=(10, 15), anchor=CENTER)

        # 1. Settings item
        ttk.Separator(frame).pack(fill=X)
        item = ttk.Frame(frame)
        item.pack(fill=X, padx=15, pady=(10, 15))

        ttk.Label(
            master=item,
            text="Allow sounds",
        ).pack(side=LEFT)

        ttk.Checkbutton(
            master=item,
            bootstyle="default-round-toggle",
            variable=self._play_sound,
            onvalue="on",
            offvalue="off"
        ).pack(side=RIGHT)

        # 2. Settings item
        ttk.Separator(frame).pack(fill=X)
        item = ttk.Frame(frame)
        item.pack(fill=X, padx=15, pady=(10, 15))

        ttk.Label(
            master=item,
            text="Settings item with Checkbutton",
        ).pack(side=LEFT)

        ttk.Checkbutton(
            master=item,
            bootstyle="default-round-toggle",
            variable=self._s2,
            onvalue="on",
            offvalue="off"
        ).pack(side=RIGHT)

        # 3. Settings item
        ttk.Separator(frame).pack(fill=X)
        item = ttk.Frame(frame)
        item.pack(fill=X, padx=15, pady=(6, 8))

        ttk.Label(
            master=item,
            text="Settings item with Spinbox",
        ).pack(side=LEFT, pady=(3, 6))

        ttk.Spinbox(
            master=item,
            bootstyle="default",
            state="readonly",
            width=10,
            from_=1.0,
            to=20.0,
            textvariable=self._s3
        ).pack(side=RIGHT, padx=(0, 2))

        # 4. Settings item
        ttk.Separator(frame).pack(fill=X)
        item = ttk.Frame(frame)
        item.pack(fill=X, padx=15, pady=(6, 8))

        ttk.Label(
            master=item,
            text="Settings item with Combobox",
        ).pack(side=LEFT, pady=(3, 6))

        cbo = ttk.Combobox(
            master=item,
            bootstyle="default",
            state="readonly",
            width=12,
            textvariable=self._s4
        )
        cbo['values'] = ('Option A', 'Option B', 'Option C')
        cbo.current(cbo['values'].index(self._s4.get()))
        cbo.pack(side=RIGHT, padx=(0, 2))
        # Bind the virtual event
        # cbo.bind('<<ComboboxSelected>>', lambda e: print("Selected:", cbo.get()))

    def create_buttonbox(self, master):
        """ Overridden from Dialog.
        """
        frame = ttk.Frame(master, padding=(5, 10))

        # Submit button
        submit = ttk.Button(
            master=frame,
            text="Submit",
            bootstyle="primary",
            command=self.on_submit,
            width=15
        )
        submit.pack(padx=5, side=RIGHT)
        submit.lower()

        # Cancel button
        cancel = ttk.Button(
            master=frame,
            text="Cancel",
            bootstyle="outline",
            command=self.on_cancel,
            width=15
        )
        cancel.pack(padx=5, side=RIGHT)
        cancel.lower()

        ttk.Separator(self._toplevel).pack(fill=X, padx=10)
        frame.pack(side=BOTTOM, fill=X, anchor=S)

    def on_submit(self, *_):
        """ Save result, destroy the toplevel, and apply data.
        """
        self._toplevel.destroy()
        self.apply()

    def on_cancel(self, *_):
        """ Close the toplevel and return empty.
        """
        self._toplevel.destroy()
        return

    def apply(self):
        """ Preparing result to return.
        """
        self._result = {
            'play_sound': self._play_sound.get(),
            's2': self._s2.get(),
            's3': self._s3.get(),
            's4': self._s4.get(),
        }




