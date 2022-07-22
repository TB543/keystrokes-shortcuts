from tkinter import Tk, Frame, Label, Canvas, LEFT, RIGHT
from keyboard import record
from threading import Thread
from window import Window


class RecordingOverlay(Tk):
    """
    a class for a recording overlay that flashes the recording icon to indicate to the user when
    their actions are being recorded
    """

    def __init__(self):
        """
        creates the recording overlay object
        """

        # initializes super class and configures class variables
        super().__init__()
        self.is_on = False
        self.timer = None
        self.actions = None
        self.thread = None

        # configures settings for window
        self.title('Recording')
        self.protocol('WM_DELETE_WINDOW', self.hide)
        self.attributes('-topmost', True)
        self.geometry(f'165x45+{self.winfo_screenwidth() - 165}+0')
        self.overrideredirect(True)
        self.config(bg='black')

        # creates widgets for window
        self.frame = Frame(self, bg='black')
        self.label = Label(self.frame, text='Recording', bg='black', fg='white', font=('Times New Roman', 18))
        self.canvas = Canvas(self.frame, bg='black', highlightthickness=0, height=30, width=30)

        # places widgets
        self.frame.pack()
        self.label.pack(side=LEFT)
        self.canvas.pack(side=RIGHT)

        # hides window
        self.withdraw()
        self.quit()

    def hide(self):
        """
        exits the windows mainloop (with destroying it), hides the window and closes after loop
        """

        self.after_cancel(self.timer)
        self.is_on = False
        self.withdraw()
        self.quit()

    def mainloop(self, until: str):
        """
        a modified mainloop method from the super class that shows the window before starting the mainloop, starts the
        flash animation and starts recording keyboard actions

        :param until the actions to end the recording

        :return the record actions
        """

        # queues up update and record functions
        self.thread = Thread(target=self.record, args=[until])
        self.thread.start()
        self.flash()
        self.is_recording()

        # shows window and returns value when done
        self.deiconify()
        super().mainloop()
        return self.actions

    def flash(self):
        """
        a function to flash (flicker on and off after 1 sec) the red recording icon to indicate that the program is
        recording
        """

        # prepares for next flash action if overlay is open
        self.timer = self.after(1000, self.flash)

        # turns red light off if it is on
        if self.is_on:
            self.canvas.delete('all')
            self.is_on = False

        # turns light on if it is off
        else:
            self.canvas.create_oval(4, 4, 30, 30, fill='red')
            self.is_on = True

    def is_recording(self):
        """
        checks to see if the thread is still recording, if it is the thread is closed and the actions are saved
        otherwise another check is queued
        """

        # queues another check if still recording
        if self.thread.is_alive():
            self.after(100, self.is_recording)

        # closes window if done recording
        else:
            self.hide()

    def record(self, until):
        """
        a modified record function to also save the value to the self.actions attribute and remove unnecessary actions
        """

        # sets variables
        self.actions = []
        pressed = []

        # removes unnecessary actions
        for action in record(until):

            # adds action to self.actions if it has not already been pressed
            if action.event_type == 'down' and pressed.count(action.name) == 0:
                pressed.append(action.name)
                self.actions.append(action)

            # adds action if it is an up event matched with a down event
            elif action.event_type == 'up':
                try:
                    pressed.remove(action.name)
                    self.actions.append(action)
                except ValueError:
                    pass

        # removes end actions
        for _ in range(len(Window.settings['recording']['key binds']['record'].split('+'))):
            self.actions.pop()
