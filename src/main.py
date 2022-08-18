try:
    from os import system
    from Lib import *
except ModuleNotFoundError:
    system('pip install -r saves/requirements.txt')


# runs code if main file is run
if __name__ == '__main__':

    # creates program classes and variables
    settings = Settings()
    done_recording = DoneRecording()
    recording_overlay = RecordingOverlay()

    # checks for updates
    if check_for_update(Window.settings['general']['version']):
        update(Window.settings['general']['version'], __file__)

    # program mainloop
    else:
        while True:

            # waits for user input
            Window.blocker.wait()

            # records actions if record keys are pressed
            if Window.hotkey_pressed == Window.settings['recording']['key binds']['record']:
                done_recording.mainloop(recording_overlay.mainloop(Window.hotkey_pressed))

            # opens settings if settings keys are pressed
            else:
                settings.mainloop()
