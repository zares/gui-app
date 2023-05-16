"""
Dummy coroutine module.
"""

import time

statuses = [
    "\n\nThe first task is done.",
    "\nThe second task is done.",
    "\nThe next task..."
]

class Application:
    def __init__(self, data):
        self.data = data
        self.launched = False

    def run(self):
        """ Launching the program.
        """
        self.launched = True
        # Sleep for simulating the task processing start
        time.sleep(1)
        return f"\n\nLaunched with the following data:\n\nImageFile › {self.data[0]}\nVideoFile › {self.data[1]}"


    def get_status(self):
        """ Get a status of the current task.
        """
        for status in statuses:
            # Sleep for simulating some task
            time.sleep(2)
            if self.launched:
                yield status


    def stop(self):
        """ Stopping the program.
        """
        self.launched = False
        # Sleep for simulating the task processing stop
        time.sleep(1)
        return "\n\nThe process is stopped."



