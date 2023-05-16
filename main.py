"""---------------------------
Main file of GUI Application
---------------------------"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from ttkbootstrap.scrolled import ScrolledFrame

from async_tkinter_loop import async_handler, async_mainloop

from controllers import *
from config.gui import *

from coroutine import Application


class AppWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        style = ttk.Style()
        style.configure("cufon.TButton", font=("Sans-serif", 10))

        self.image_path = ttk.StringVar(value="Not selected yet...")
        self.video_path = ttk.StringVar(value="Not selected yet...")

        self.started = False
        self.app = None

        self.photoimages = []
        for key, val in IMAGE_FILES.items():
            _file = IMAGES_PATH / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_file))

        # Buttonbar - top bar with title and buttons
        buttonbar = ttk.Frame(self, style="primary.TFrame")
        buttonbar.pack(fill=X, ipady=3, pady=0, side=TOP)

        # App title with logo
        title = ttk.Label(
            master=buttonbar,
            text=APP_NAME,
            image="app-logo",
            compound=LEFT,
            bootstyle="primary inverse",
            font="-size 14 -weight normal"
        )
        title.pack(side=LEFT, padx=(8, 160))
        _func = lambda e, p=self: HelpController.main(e, p)
        title.bind('<Button-1>', _func)

        # Button "Starting"
        _func = lambda: self.starting_process()
        btn = ttk.Button(
            master=buttonbar,
            text="Starting",
            style="cufon.TButton",
            image="start-process",
            compound=LEFT,
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=8)

        # Button "Stopping"
        _func = lambda: self.stopping_process()
        btn = ttk.Button(
            master=buttonbar,
            text="Stopping",
            style="cufon.TButton",
            image="stop-process",
            compound=LEFT,
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=8)

        # Button "Add video"
        _func = lambda: self.add_video()
        btn = ttk.Button(
            master=buttonbar,
            text="Add video",
            style="cufon.TButton",
            image="add-video",
            compound=LEFT,
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=8)

        # Button "Add image"
        _func = lambda: self.add_image()
        btn = ttk.Button(
            master=buttonbar,
            text="Add image",
            style="cufon.TButton",
            image="add-image",
            compound=LEFT,
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=8)

        # Button "Settings"
        _func = lambda: SettingsController.main()
        btn = ttk.Button(
            master=buttonbar,
            text="Settings",
            style="cufon.TButton",
            image="settings",
            compound=LEFT,
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=8)

        # Output container
        output_container = ttk.Frame(self)
        output_container.pack(fill=BOTH, expand=YES, padx=(6, 0), pady=7)

        # Scroll implementation
        scrolled_frame = ScrolledFrame(
            output_container,
            autohide=True,
            bootstyle="default",
            scrollheight=9999
        )
        scrolled_frame.pack(fill=BOTH, expand=YES, padx=(1, 2))

        # Image frame block ---------------------

        self.image_widget = ttk.Labelframe(
            master=scrolled_frame,
            text=" CONTROL IMAGE ",
            style="LIGHT"
        )

        ttk.Label(
            master=self.image_widget,
            text="File location  ›",
            style="INFO",
            font=("Sans-serif", 11, "bold")
        ).pack(side=LEFT, padx=10, pady=(8, 12))

        ttk.Label(
            master=self.image_widget,
            textvariable=self.image_path,
            style="LIGHT",
            font=("Sans-serif", 11)
        ).pack(side=LEFT, padx=2, pady=(11, 15))

        _func = lambda: ImagePreviewController.main()
        self.image_btn = ttk.Button(
            master=self.image_widget,
            text="Image Preview",
            bootstyle="OUTLINE",
            command=_func
        )

        # Video frame block ---------------------

        self.video_widget = ttk.Labelframe(
            master=scrolled_frame,
            text=" VIDEO TRACK ",
            style="LIGHT"
        )

        ttk.Label(
            master=self.video_widget,
            text="File location  ›",
            style="INFO",
            font=("Sans-serif", 11, "bold")
        ).pack(side=LEFT, padx=10, pady=(8, 12))

        ttk.Label(
            master=self.video_widget,
            textvariable=self.video_path,
            style="LIGHT",
            font=("Sans-serif", 11)
        ).pack(side=LEFT, padx=2, pady=(11, 15))

        _func = lambda: VideoPreviewController.main()
        self.video_btn = ttk.Button(
            master=self.video_widget,
            text="Video Preview",
            bootstyle="OUTLINE",
            command=_func
        )

        # Execution status block ----------------

        self.execstatus = ttk.Labelframe(
            master=scrolled_frame,
            text=" EXECUTION STATUS ",
            style="LIGHT"
        )

        self.status_label = ttk.Label(
            master=self.execstatus,
            text="...",
            style="INFO",
            font=("Sans-serif", 11, "bold")
        )
        self.status_label.pack(side=LEFT, padx=10, pady=(8, 12))


    @async_handler
    async def stopping_process(self):
        """ Call to controller to stop process.
        """
        if self.started == False:
            return

        if stopping := StoppingController.main():
            self.status_label['text'] += await self.app.stop()
            self.started = False
        else:
            self.started = True


    @async_handler
    async def starting_process(self):
        """ Call to controller to start process.
        """
        if self.started == True:
            return

        if starting := StartingController.main():
            self.started = True
            self.status_label['text'] = "Launching..."
            # Load image widget
            self.image_path.set(starting[0])
            self.image_widget.pack(fill=X, padx=(7, 11), pady=10)
            # Load video widget
            self.video_path.set(starting[1])
            self.video_widget.pack(fill=X, padx=(7, 11), pady=10)
            # Load execution status widget
            self.execstatus.pack(fill=X, padx=(7, 11), pady=10)
            # Run the app and load starting data
            self.app = Application(data=starting)
            self.status_label['text'] += await self.app.run()
            # Load the current process status
            async for status in self.app.get_status():
                self.status_label['text'] += status
        else:
            self.started = False


    def add_video(self):
        """ Call to controller to recieve video track path.
        """
        if vidpath := AddVideoController.main():
            self.video_path.set(vidpath)
            self.video_btn.pack(side=RIGHT, padx=10, pady=(4, 12))
            self.video_widget.pack(fill=X, padx=(7, 11), pady=10)
        else:
            self.video_path.set("Nothing selected")
            self.video_btn.pack_forget()


    def add_image(self):
        """ Call to controller to recieve image source path.
        """
        if imgpath := AddImageController.main():
            self.image_path.set(imgpath)
            self.image_btn.pack(side=RIGHT, padx=10, pady=(4, 12))
            self.image_widget.pack(fill=X, padx=(7, 11), pady=10)
        else:
            self.image_path.set("Nothing selected")
            self.image_btn.pack_forget()


if __name__ == "__main__":
    """ Configure and open the main window.
    """
    app = ttk.Window(
        title=APP_NAME,
        themename="superhero",
        size=(950, 600),
        resizable=(False, True)
    )
    AppWindow(app)
    async_mainloop(app)
    # app.mainloop()


