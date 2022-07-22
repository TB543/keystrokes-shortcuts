"""
todo: add way to change key binds
 add mouse recording
 note: record data with up, down, time to indicate action
 list should be in form ['up <key>', 'down <key>', 'time .1244'] ** example
 where key is the key for keycodes in dict
 -----------------------------------------------------------------------------------------------------------------------
 to do for first release:
 need to implement mouse recording
    --> mouse should record all movements, might create memory issues so skip some short movements, replace with jumps
    --> record time
 -----------------------------------------------------------------------------------------------------------------------
 to do for later releases:
 need to add more instructions to readme
 need to implement way to change settings/record key bind
    --> in settings window, possibly button that opens new window
    --> save this data in settings file
    --> prevent duplicate actions
    --> mutate readme to contain accurate key binds
    --> prevent automations to have same key binds as settings/record key bind, also check when changing these key binds
 need to add option in settings to open readme when code starts
    --> maybe add second page to settings, change page with buttons labeled "-->" or "<--"
"""
from tkinter import *
import time
from multiprocessing import Process, Manager
import os
try:
    import win32api
    import win32con
except ModuleNotFoundError:
    os.system("pip install pywin32")
    import win32api
    import win32con


# attempts to open files and creates files if they don't exist
def read_file(name: str):
    try:
        with open(DIRECTORY + name, 'r') as file:
            data = file.read()
    except FileNotFoundError:
        try:
            os.mkdir(os.path.join(os.getenv("LOCALAPPDATA"), "KeystrokeShortcut"))
        except FileExistsError:
            pass
        with open(DIRECTORY + name, 'w') as file:
            if name == 'Settings.txt':
                data = '{\'Keyboard\': True, \'Mouse\': False, \'MouseRecording\': \'actual\'}'
                file.write(data)
            else:
                data = '[]'
                file.write(data)
    try:
        return eval(data)
    except SyntaxError:
        os.remove(DIRECTORY + name)
        read_file(name)


# writes data to a file
def write_file(data, file: str):
    try:
        with open(DIRECTORY + file, 'w') as file:
            file.write(str(data))
    except FileNotFoundError:
        try:
            os.mkdir(os.path.join(os.getenv("LOCALAPPDATA"), "KeystrokeShortcut"))
        except FileExistsError:
            pass
        with open(DIRECTORY + file, 'w') as file:
            file.write(str(data))


# runs the actions given
def run_actions(actions, delay=False, repetitions=1):
    for _ in range(repetitions):
        for raw_action in actions:
            action = raw_action.split(' ')
            if action[0] == 'down':
                win32api.keybd_event(KEY_CODES[action[1]], 0, 0, 0)
            elif action[0] == 'up':
                win32api.keybd_event(KEY_CODES[action[1]], 0, win32con.KEYEVENTF_KEYUP, 0)
            elif action[0] == 'file':
                Process(target=os.system, args=[f'start cmd /c \"{str(raw_action[5:])}\"']).start()
            if (not delay) and (action[0] == 'time'):
                time.sleep(float(action[1]))
            elif delay:
                time.sleep(.001)


# gets keys that are pressed
def key_logger(shm_keys_pressed, shm_key_codes):
    while True:
        time.sleep(.001)
        for shm_key_code in shm_key_codes:
            if win32api.GetKeyState(shm_key_codes[shm_key_code]) < 0:
                if shm_keys_pressed.count(shm_key_code) == 0:
                    shm_keys_pressed.append(shm_key_code)
            else:
                try:
                    shm_keys_pressed.remove(shm_key_code)
                except ValueError:
                    pass


# class for the recording icon
class RecordingOverlay(Tk):

    # creates widgets
    def __init__(self):
        super().__init__()
        self.title('Recording')
        self.attributes('-fullscreen', True)
        self.wm_attributes('-transparentcolor', self['bg'])
        self.attributes('-topmost', True)
        self.frame = Frame(self)
        self.label = Label(self.frame, text='Recording', fg='white', font=('Times New Roman', 18))
        self.label.pack(side=LEFT)
        self.canvas = Canvas(self.frame, height=25, width=25)
        self.canvas.create_oval(5, 5, 25, 25, fill='red')
        self.canvas.pack(side=RIGHT)
        self.frame.pack(anchor=NE)
        self.time = time.time()
        self.on = True

    # updates recording icon to make it flash
    def update(self):
        if time.time() - self.time > 1 and self.on:
            self.canvas.delete('all')
            self.time = time.time()
            self.on = False
        elif time.time() - self.time > 1 and not self.on:
            self.canvas.create_oval(5, 5, 25, 25, fill='red')
            self.time = time.time()
            self.on = True
        super().update()

    # closes the window
    def destroy(self):
        self.frame.destroy()
        self.label.destroy()
        self.canvas.destroy()
        super().destroy()


# super class for windows, contains methods that all windows will contain
class Window(Tk):

    # creates screen
    def __init__(self, actions):
        super().__init__()
        self.geometry(f'400x250+{self.winfo_screenwidth() - 425}+{self.winfo_screenheight() - 350}')
        self.attributes('-topmost', True)
        self.actions = actions
        self.no_delay = BooleanVar()
        self.no_name_error = Label(self, text='Missing Field', font=('Times New Roman', 18), fg='red')
        self.same_name_error = Label(self, text='This Name Already Exists', font=('Times New Roman', 18), fg='red')
        self.invalid_name_error = Label(self, text='Invalid Name or Character', font=('Times New Roman', 18), fg='red')
        self.success = Label(self, text='Saved', font=('Times New Roman', 18), fg='green')
        self.widgets = []  # list of list for widget placement [widget, padx, pady, side]
        self.not_an_int_error = Label(self, text='Repetitions Must be an Integer', font=('Times New Roman', 18),
                                      fg='red')
        self.select_shortcut_error = Label(self, text='Select a Shortcut', font=('Times New Roman', 18), fg='red')

    # code to place widgets on screen
    def place_widgets(self):
        for widget in self.widgets:
            widget[0].pack(padx=widget[1], pady=widget[2], side=widget[3])

    # code to remove all widgets from screen
    def remove_widgets(self):
        self.success.pack_forget()
        self.no_name_error.pack_forget()
        self.invalid_name_error.pack_forget()
        self.same_name_error.pack_forget()
        self.not_an_int_error.pack_forget()
        self.select_shortcut_error.pack_forget()
        for widget in self.widgets:
            widget[0].pack_forget()
            widget[0].destroy()
        self.widgets.clear()

    # closes window
    def cancel(self):
        self.remove_widgets()
        self.no_name_error.destroy()
        self.same_name_error.destroy()
        self.success.destroy()
        self.invalid_name_error.destroy()
        self.not_an_int_error.destroy()
        self.select_shortcut_error.destroy()
        self.destroy()

    # code to run actions
    def run(self):
        if not self.actions:
            self.not_an_int_error.pack_forget()
            self.select_shortcut_error.pack()
        else:
            self.select_shortcut_error.pack_forget()
            try:
                int(self.widgets[-6][0].get())
                self.withdraw()
                run_actions(self.actions, self.no_delay.get(), int(self.widgets[-6][0].get()))
                self.not_an_int_error.pack_forget()
                self.deiconify()
            except ValueError:
                self.not_an_int_error.pack()


# class for window when done recording
class DoneRecording(Window):

    # prepares widgets
    def __init__(self, actions: list):
        super().__init__(actions)
        self.create_home()

    # creates home screen
    def create_home(self):
        self.title('Done Recording')
        self.no_delay.set(False)
        self.remove_widgets()
        self.widgets.append([Frame(self), 0, 20, TOP])
        self.widgets.append([Label(self.widgets[-1][0], text='Repetitions:', font=('Times New Roman', 18)), 0, 0, LEFT])
        self.widgets.append([Entry(self.widgets[-2][0], font=('Times New Roman', 12), width=10), 0, 0, RIGHT])
        self.widgets.append([Checkbutton(self, text='No Delay', font=('Times New Roman', 18), onvalue=True,
                                         offvalue=False, variable=self.no_delay), 0, 0, TOP])
        self.widgets.append([Frame(self), 0, 20, TOP])
        self.widgets.append(
            [Button(self.widgets[-1][0], text='Save', font=('Times New Roman', 18), command=lambda: self.create_save()),
             10, 0, LEFT])
        self.widgets.append(
            [Button(self.widgets[-2][0], text='Cancel', font=('Times New Roman', 18), command=lambda: self.cancel()),
             10, 0, RIGHT])
        self.widgets.append(
            [Button(self.widgets[-3][0], text='Run', font=('Times New Roman', 18), command=lambda: self.run()), 10, 0,
             TOP])
        self.place_widgets()

    # code to create save window
    def create_save(self):
        self.title('Save Shortcut')
        self.remove_widgets()
        self.widgets.append([Frame(self), 0, 30, TOP])
        self.widgets.append(
            [Label(self.widgets[-1][0], text='Shortcut Name:', font=('Times New Roman', 18)), 0, 0, LEFT])
        self.widgets.append([Entry(self.widgets[-2][0], font=('Times New Roman', 12)), 0, 0, RIGHT])
        self.widgets.append([Frame(self), 0, 20, TOP])
        self.widgets.append(
            [Button(self.widgets[-1][0], text='Save', font=('Times New Roman', 18), command=lambda: self.save()), 10, 0,
             LEFT])
        self.widgets.append(
            [Button(self.widgets[-2][0], text='Back', font=('Times New Roman', 18), command=lambda: self.create_home()),
             10, 0, RIGHT])
        self.place_widgets()

    # saves shortcut
    def save(self):
        global saved_shortcuts
        if ('\'' in self.widgets[-4][0].get()) or ('\\' in self.widgets[-4][0].get()) or (
                '\"' in self.widgets[-4][0].get()) or ('Select Shortcut' in self.widgets[-4][0].get()) or (
                'No Shortcuts' in self.widgets[-4][0].get()) or (self.widgets[-4][0].get() == 'Run File'):
            self.success.pack_forget()
            self.same_name_error.pack_forget()
            self.no_name_error.pack_forget()
            self.invalid_name_error.pack()
            return
        elif self.widgets[-4][0].get() == '':
            self.success.pack_forget()
            self.same_name_error.pack_forget()
            self.invalid_name_error.pack_forget()
            self.no_name_error.pack()
            return
        for shortcut in saved_shortcuts:
            if shortcut['name'] == self.widgets[-4][0].get():
                self.success.pack_forget()
                self.no_name_error.pack_forget()
                self.invalid_name_error.pack_forget()
                self.same_name_error.pack()
                return
        saved_shortcuts.append(
            eval('{\'name\': \'' + str(self.widgets[-4][0].get()) + '\', \'actions\': ' + str(self.actions) + '}'))
        write_file(saved_shortcuts, SAVED_SHORTCUTS_FILE)
        self.no_name_error.pack_forget()
        self.same_name_error.pack_forget()
        self.invalid_name_error.pack_forget()
        self.success.pack()


# class for settings window
class Options(Window):

    # creates widgets
    def __init__(self):
        global settings
        super().__init__([])
        self.same_start_error = Label(self, text='Start Shortcut Already Exists', font=('Times New Roman', 18),
                                      fg='red')
        self.duplicate_actions_error = Label(self, text='Invalid Shortcut: Duplicate Start Actions',
                                             font=('Times New Roman', 18), fg='red')
        self.invalid_file_error = Label(self, text='Invalid File', font=('Times New Roman', 18), fg='red')
        self.keyboard = BooleanVar(self, settings['Keyboard'])
        self.mouse = BooleanVar(self, settings['Mouse'])
        self.mouse_recording = StringVar(self, settings['MouseRecording'])
        self.selected_shortcut = StringVar(self)
        self.delete_automation_selection = StringVar(self)
        self.start_automation_selection = StringVar(self)
        self.automation_actions_selection = StringVar(self)
        self.automation_name = StringVar(self)
        self.file_path = StringVar(self)
        self.widgets = []
        self.create_home()
        self.do_not_change = False
        self.file = False

    # creates home screen
    def create_home(self):
        self.title('Options')
        self.do_not_change = False
        self.remove_widgets()
        self.widgets.append(
            [Button(self, text='Saves', font=('Times New Roman', 18), command=lambda: self.create_saves()), 0, 5, TOP])
        self.widgets.append(
            [Button(self, text='Settings', font=('Times New Roman', 18), command=lambda: self.create_settings()), 0, 5,
             TOP])
        self.widgets.append(
            [Button(self, text='Automations', font=('Times New Roman', 18), command=lambda: self.create_automations()),
             0, 5, TOP])
        self.widgets.append(
            [Button(self, text='Cancel', font=('Times New Roman', 18), command=lambda: self.cancel()), 0, 5, TOP])
        self.place_widgets()

    # creates saves screen
    def create_saves(self):
        global saved_shortcuts
        names = []
        for shortcut in saved_shortcuts:
            names.append(shortcut['name'])
        if not names:
            names.append('No Shortcuts')
        self.title('Saves')
        self.no_delay.set(False)
        self.selected_shortcut.set("Select Shortcut")
        self.remove_widgets()
        self.widgets.append([Label(self, text='Select a Shortcut:', font=('Times New Roman', 18)), 0, 0, TOP])
        self.widgets.append([OptionMenu(self, self.selected_shortcut, *names, command=self.set_actions), 0, 0, TOP])
        self.widgets[-1][0].config(width=15, font=("Times New Roman", 13))
        self.widgets.append([Frame(self), 0, 10, TOP])
        self.widgets.append([Label(self.widgets[-1][0], text='Repetitions:', font=('Times New Roman', 18)), 0, 0, LEFT])
        self.widgets.append([Entry(self.widgets[-2][0], font=('Times New Roman', 12), width=10), 0, 0, RIGHT])
        self.widgets.append([Checkbutton(self, text='No Delay', font=('Times New Roman', 18), onvalue=True,
                                         offvalue=False, variable=self.no_delay), 0, 0, TOP])
        self.widgets.append([Frame(self), 0, 0, TOP])
        self.widgets.append(
            [Button(self.widgets[-1][0], text='Run', font=('Times New Roman', 18), command=lambda: self.run()), 10, 0,
             LEFT])
        self.widgets.append(
            [Button(self.widgets[-2][0], text='Back', font=('Times New Roman', 18), command=lambda: self.create_home()),
             10, 0, RIGHT])
        self.widgets.append([Button(self.widgets[-3][0], text='Delete Shortcut', font=('Times New Roman', 18),
                                    command=lambda: self.delete_save()), 10, 0, TOP])
        self.place_widgets()

    # creates settings screen
    def create_settings(self):
        self.title('Settings')
        self.remove_widgets()
        self.keyboard = BooleanVar(self, settings['Keyboard'])
        self.mouse = BooleanVar(self, settings['Mouse'])
        self.mouse_recording = StringVar(self, settings['MouseRecording'])
        self.widgets.append([Frame(self), 0, 0, TOP])
        self.widgets.append([Label(self.widgets[-1][0], text='Record:', font=('Times New Roman', 18)), 0, 0, TOP])
        self.widgets.append([Frame(self.widgets[-2][0]), 0, 0, TOP])
        self.widgets.append([Checkbutton(self.widgets[-1][0], text='Keyboard', font=('Times New Roman', 18), onvalue=1,
                                         offvalue=0, variable=self.keyboard), 10, 0, LEFT])
        self.widgets.append([Checkbutton(self.widgets[-2][0], text='Mouse', font=('Times New Roman', 18), onvalue=1,
                                         offvalue=0, variable=self.mouse), 10, 0, RIGHT])
        self.widgets.append([Frame(self), 0, 0, TOP])
        self.widgets.append(
            [Label(self.widgets[-1][0], text='Mouse Position Recording:', font=('Times New Roman', 18)), 0, 0, TOP])
        self.widgets.append([Frame(self.widgets[-2][0]), 0, 0, TOP])
        self.widgets.append([Radiobutton(self.widgets[-1][0], text='Actual Position', font=('Times New Roman', 18),
                                         variable=self.mouse_recording, value='actual'), 5, 0, LEFT])
        self.widgets.append([Radiobutton(self.widgets[-2][0], text='Relative Position', font=('Times New Roman', 18),
                                         variable=self.mouse_recording, value='relative'), 5, 0, RIGHT])
        self.widgets.append([Frame(self), 0, 0, TOP])
        self.widgets.append([Button(self.widgets[-1][0], text='Save', font=('Times New Roman', 14),
                                    command=lambda: self.save_settings()), 15, 0, LEFT])
        self.widgets.append(
            [Button(self.widgets[-2][0], text='Back', font=('Times New Roman', 14), command=lambda: self.create_home()),
             15, 0, RIGHT])
        self.widgets.append([Button(self.widgets[-3][0], text='Open Readme', font=('Times New Roman', 14),
                                    command=lambda: self.open_readme()), 15, 0, TOP])
        self.widgets.append([Frame(self), 0, 10, TOP])
        self.widgets.append([Button(self.widgets[-1][0], text='Delete all shortcuts', font=('Times New Roman', 14),
                                    command=lambda: self.delete_all_shortcuts()), 5, 0, LEFT])
        self.widgets.append([Button(self.widgets[-2][0], text='Delete all automations', font=('Times New Roman', 14),
                                    command=lambda: self.delete_all_automations()), 5, 0, RIGHT])
        self.place_widgets()

    # creates automations screen
    def create_automations(self):
        global automations, saved_shortcuts
        automations_names = []
        for automation in automations:
            automations_names.append(automation['name'])
        if not automations_names:
            automations_names.append('No Automations')
        shortcuts = []
        for shortcut in saved_shortcuts:
            shortcuts.append(shortcut['name'])
        if not shortcuts:
            shortcuts.append('No Shortcuts')
        self.title('Automations')
        if not self.do_not_change:
            self.no_delay.set(False)
            self.delete_automation_selection.set("Select Automation")
            self.start_automation_selection.set("Select Shortcut")
            self.automation_actions_selection.set("Select Shortcut")
            self.automation_name.set('')
            self.file_path.set('')
        self.remove_widgets()
        self.widgets.append([Frame(self), 0, 0, TOP])
        self.widgets.append(
            [Label(self.widgets[-1][0], text='Automation to Delete:', font=('Times New Roman', 15)), 0, 0, LEFT])
        self.widgets.append(
            [OptionMenu(self.widgets[-2][0], self.delete_automation_selection, *automations_names), 0, 0, RIGHT])
        self.widgets[-1][0].config(width=15, font=("Times New Roman", 13))
        self.widgets.append([Frame(self), 0, 0, TOP])
        self.widgets.append([Label(self.widgets[-1][0], text='Create Automation:', font=('Times New Roman', 14)), 0, 0,
                             LEFT])
        self.widgets.append([Checkbutton(self.widgets[-2][0], text='No Delay', font=('Times New Roman', 12),
                                         onvalue=True, offvalue=False, variable=self.no_delay), 0, 10, RIGHT])
        self.widgets.append([Frame(self), 0, 0, TOP])
        self.widgets.append(
            [Label(self.widgets[-1][0], text='Name of Automation:', font=('Times New Roman', 15)), 0, 0, LEFT])
        self.widgets.append([Entry(self.widgets[-2][0], font=('Times New Roman', 12), width=20,
                                   textvariable=self.automation_name), 0, 0, RIGHT])
        self.widgets.append([Frame(self), 0, 0, TOP])
        self.widgets.append([Frame(self.widgets[-1][0]), 10, 0, LEFT])
        self.widgets.append(
            [Label(self.widgets[-1][0], text='Start Keystrokes:', font=('Times New Roman', 15)), 0, 0, TOP])
        self.widgets.append([OptionMenu(self.widgets[-2][0], self.start_automation_selection, *shortcuts), 0, 0, TOP])
        self.widgets[-1][0].config(width=15, font=("Times New Roman", 13))
        self.widgets.append([Frame(self.widgets[-4][0]), 10, 0, RIGHT])
        if self.file:
            self.widgets.append([Label(self.widgets[-1][0], text='File Path:', font=('Times New Roman', 15)), 0, 0,
                                 TOP])
            self.widgets.append([Entry(self.widgets[-2][0], textvariable=self.file_path), 0, 0, LEFT])
            self.widgets.append([Button(self.widgets[-3][0], text='Undo', font=('Times New Roman', 14),
                                        command=lambda: self.undo()), 0, 0, RIGHT])
        else:
            self.widgets.append([Label(self.widgets[-1][0], text='Actions:', font=('Times New Roman', 15)), 0, 0, TOP])
            try:
                shortcuts.remove('No Shortcuts')
            except ValueError:
                pass
            shortcuts.append('Run File')
            self.widgets.append([OptionMenu(self.widgets[-2][0], self.automation_actions_selection, *shortcuts,
                                            command=self.run_file), 0, 0, TOP])
            self.widgets[-1][0].config(width=15, font=("Times New Roman", 13))
        self.widgets.append([Frame(self), 0, 0, TOP])
        self.widgets.append([Button(self.widgets[-1][0], text='Create Automation', font=('Times New Roman', 14),
                                    command=lambda: self.create_automation()), 5, 0, LEFT])
        self.widgets.append(
            [Button(self.widgets[-2][0], text='Back', font=('Times New Roman', 14), command=lambda: self.create_home()),
             5, 0, RIGHT])
        self.widgets.append([Button(self.widgets[-3][0], text='Delete Automation', font=('Times New Roman', 14),
                                    command=lambda: self.delete_automation()), 5, 0, TOP])
        self.place_widgets()

    # sets the actions to the selected shortcut
    def set_actions(self, selected_shortcut):
        global saved_shortcuts
        self.actions = []
        for shortcut in saved_shortcuts:
            if shortcut['name'] == selected_shortcut:
                self.actions = shortcut['actions']

    # deletes a saved shortcut
    def delete_save(self):
        global saved_shortcuts
        index = 0
        for shortcut in saved_shortcuts:
            if shortcut['name'] == self.selected_shortcut.get():
                saved_shortcuts.pop(index)
                break
            index += 1
        write_file(saved_shortcuts, SAVED_SHORTCUTS_FILE)
        self.remove_widgets()
        self.create_saves()

    # saves the settings
    def save_settings(self):
        global settings
        settings = eval('{\'Keyboard\': ' + str(self.keyboard.get()) + ', \'Mouse\': ' + str(
            self.mouse.get()) + ', \'MouseRecording\': \'' + str(self.mouse_recording.get()) + '\'}')
        write_file(settings, SETTINGS_FILE)

    # creates automation
    def create_automation(self):
        global automations, saved_shortcuts
        if (self.automation_name.get() == '') or (self.start_automation_selection.get() == 'Select Shortcut') or (
                self.automation_actions_selection.get() == 'Select Shortcut') or (
                self.start_automation_selection.get() == 'No Shortcuts') or (
                self.automation_actions_selection.get() == 'No Shortcuts'):
            self.success.pack_forget()
            self.same_name_error.pack_forget()
            self.invalid_name_error.pack_forget()
            self.same_start_error.pack_forget()
            self.duplicate_actions_error.pack_forget()
            self.invalid_file_error.pack_forget()
            self.no_name_error.pack()
            return
        elif ('\'' in self.automation_name.get()) or ('\\' in self.automation_name.get()) or (
                '\"' in self.automation_name.get()) or ('Select Automation' in self.automation_name.get()) or (
                'No Automations' in self.automation_name.get()):
            self.success.pack_forget()
            self.same_name_error.pack_forget()
            self.no_name_error.pack_forget()
            self.same_start_error.pack_forget()
            self.duplicate_actions_error.pack_forget()
            self.invalid_file_error.pack_forget()
            self.invalid_name_error.pack()
            return
        for automation in automations:
            if automation['name'] == self.automation_name.get():
                self.success.pack_forget()
                self.no_name_error.pack_forget()
                self.invalid_name_error.pack_forget()
                self.same_start_error.pack_forget()
                self.duplicate_actions_error.pack_forget()
                self.invalid_file_error.pack_forget()
                self.same_name_error.pack()
                return
        start = []
        actions = []
        if self.file:
            if os.path.isfile(self.file_path.get()):
                actions.append(f'file {self.file_path.get()}')
            else:
                self.success.pack_forget()
                self.no_name_error.pack_forget()
                self.invalid_name_error.pack_forget()
                self.same_start_error.pack_forget()
                self.duplicate_actions_error.pack_forget()
                self.same_name_error.pack_forget()
                self.invalid_file_error.pack()
                return
        for shortcut in saved_shortcuts:
            if shortcut['name'] == self.start_automation_selection.get():
                for action in shortcut['actions']:
                    if not (action.split(' ')[0] == 'time' or action.split(' ')[0] == 'up'):
                        start.append(action.split(' ')[1])
            if (not self.file) and (shortcut['name'] == self.automation_actions_selection.get()):
                if self.no_delay.get():
                    for action in shortcut['actions']:
                        if not action.split(' ')[0] == 'time':
                            actions.append(action)
                else:
                    actions = shortcut['actions']
        for automation in automations:
            if automation['start'] == start:
                self.no_name_error.pack_forget()
                self.same_name_error.pack_forget()
                self.invalid_name_error.pack_forget()
                self.success.pack_forget()
                self.duplicate_actions_error.pack_forget()
                self.invalid_file_error.pack_forget()
                self.same_start_error.pack()
                return
        for action in start:
            if start.count(action) > 1:
                self.no_name_error.pack_forget()
                self.same_name_error.pack_forget()
                self.invalid_name_error.pack_forget()
                self.success.pack_forget()
                self.same_start_error.pack_forget()
                self.invalid_file_error.pack_forget()
                self.duplicate_actions_error.pack()
                return
        automations.append(eval(
            '{\'name\': \'' + self.automation_name.get() + '\', \'start\': ' + str(start) + ', \'actions\': ' +
            str(actions) + '}'))
        write_file(automations, AUTOMATIONS_FILE)
        self.no_name_error.pack_forget()
        self.same_name_error.pack_forget()
        self.invalid_name_error.pack_forget()
        self.same_start_error.pack_forget()
        self.invalid_file_error.pack_forget()
        self.remove_widgets()
        self.do_not_change = False
        self.file = False
        self.create_automations()
        self.success.pack()

    # deletes an automation
    def delete_automation(self):
        global automations
        self.do_not_change = False
        index = 0
        for automation in automations:
            if automation['name'] == self.delete_automation_selection.get():
                automations.pop(index)
                break
            index += 1
        write_file(automations, AUTOMATIONS_FILE)
        self.remove_widgets()
        self.create_automations()

    # changes option menu to entry for file path
    def run_file(self, selection):
        if selection == 'Run File':
            self.do_not_change = True
            self.file = True
            self.create_automations()

    # undoes run file action
    def undo(self):
        self.do_not_change = True
        self.file = False
        self.create_automations()

    # opens instructions file
    def open_readme(self):
        self.withdraw()
        os.system(DIRECTORY + README_FILE)
        self.deiconify()

    # removes widgets with same start error
    def remove_widgets(self):
        self.same_start_error.pack_forget()
        self.duplicate_actions_error.pack_forget()
        self.invalid_file_error.pack_forget()
        super().remove_widgets()

    # cancels and also deletes same start error
    def cancel(self):
        self.same_start_error.destroy()
        self.duplicate_actions_error.destroy()
        self.invalid_file_error.destroy()
        super().cancel()

    # deletes all automations
    @staticmethod
    def delete_all_shortcuts():
        global saved_shortcuts
        saved_shortcuts = []
        write_file(saved_shortcuts, SAVED_SHORTCUTS_FILE)

    # deletes all saved shortcuts
    @staticmethod
    def delete_all_automations():
        global automations
        automations = []
        write_file(automations, AUTOMATIONS_FILE)


if __name__ == '__main__':

    # creates variables for file paths
    DIRECTORY = str(os.getenv("LOCALAPPDATA")) + '\\KeystrokeShortcut\\'
    AUTOMATIONS_FILE = 'Automations.txt'
    SAVED_SHORTCUTS_FILE = 'Saved Shortcuts.txt'
    SETTINGS_FILE = 'Settings.txt'
    README_FILE = 'readme.txt'
    README_TXT = 'Keystrokes Shortcuts, How to Use:\n\n    Recording Actions:\n        --> Press ctrl + shift + r to ' \
                 'start recording keyboard/mouse\n        --> Press ctrl + shift + r again to stop recording\n\n    ' \
                 'Finished Recording Window\n        --> Enter a number for number of times to run recording ' \
                 'actions\n        --> Check the no delay button to run actions instantly\n        --> Click the save' \
                 ' button and enter a name to save the shortcut for later\n        ** You will need saved shortcuts t' \
                 'o make automations **\n\n    Settings Window:\n        --> Click ctrl + shift + s to open settings ' \
                 'menu\n        --> Click the saves window to manage/run your saved shortcuts\n        --> Click the ' \
                 'settings button to change what is recording and how mouse is recorded\n        ** Actual position ' \
                 'means mouse will record exact coordinates **\n        ** Relative position means mouse will move ' \
                 'relative to starting mouse position when running **\n        --> Automations menu is where you can ' \
                 'manage your automations\n        --> With automations you can create hotkeys to perform keystroke ' \
                 'action or run files\n        ** Key up and time events from shortcuts will be ignored when ' \
                 'selecting start actions **\n\n    Things to keep in mind\n        --> This app provides support for' \
                 ' most keys on the average keyboard, so if you do not have an average keyboard there is a chance not' \
                 ' all keys will be recognised\n        --> Program cannot tell the difference between 2 keys that ar' \
                 'e the same (ie. right/left alt)\n        --> Keys are not being listened to while a window is open ' \
                 'or an action is running\n        --> There is a .001 second delay between all actions and checks fo' \
                 'r recording as to not drain your computers resources\n        --> Windows defender and other ' \
                 'anti-malware might flag this program as a keylogger (which it is), you can just create an exception' \
                 ' in settings\n        --> When an automation runs a file, it will run in a new thread, be aware of ' \
                 'how many of these files you have running, it could drain your computers resources\n        --> The ' \
                 'folder with all this applications data is located at ' \
                 'C:\\Users\\<USER>\\AppData\\Local\\KeystrokeShortcut\n        --> If for whatever reason this ' \
                 'application fails to run like it used to delete the folder above for a fresh start (this will ' \
                 'delete all shortcuts, automations and settings)\n\n    Upcoming Features:\n        --> Mouse ' \
                 'recording (it is not implemented yet)\n       --> Ability to change keybindings to start recording ' \
                 'and open settings window\n        --> Bug fixes '
    TEMP_WINDOW_THRESHOLD = 100

    # dictionary of every keycode
    KEY_CODES = {'backspace': 0x08,
                 'tab': 0x09,
                 'clear': 0x0C,
                 'enter': 0x0D,
                 'shift': 0x10,
                 'ctrl': 0x11,
                 'alt': 0x12,
                 'pause': 0x13,
                 'caps_lock': 0x14,
                 'esc': 0x1B,
                 'spacebar': 0x20,
                 'page_up': 0x21,
                 'page_down': 0x22,
                 'end': 0x23,
                 'home': 0x24,
                 'left_arrow': 0x25,
                 'up_arrow': 0x26,
                 'right_arrow': 0x27,
                 'down_arrow': 0x28,
                 'select': 0x29,
                 'print': 0x2A,
                 'execute': 0x2B,
                 'print_screen': 0x2C,
                 'ins': 0x2D,
                 'del': 0x2E,
                 'help': 0x2F,
                 '0': 0x30,
                 '1': 0x31,
                 '2': 0x32,
                 '3': 0x33,
                 '4': 0x34,
                 '5': 0x35,
                 '6': 0x36,
                 '7': 0x37,
                 '8': 0x38,
                 '9': 0x39,
                 'a': 0x41,
                 'b': 0x42,
                 'c': 0x43,
                 'd': 0x44,
                 'e': 0x45,
                 'f': 0x46,
                 'g': 0x47,
                 'h': 0x48,
                 'i': 0x49,
                 'j': 0x4A,
                 'k': 0x4B,
                 'l': 0x4C,
                 'm': 0x4D,
                 'n': 0x4E,
                 'o': 0x4F,
                 'p': 0x50,
                 'q': 0x51,
                 'r': 0x52,
                 's': 0x53,
                 't': 0x54,
                 'u': 0x55,
                 'v': 0x56,
                 'w': 0x57,
                 'x': 0x58,
                 'y': 0x59,
                 'z': 0x5A,
                 'numpad_0': 0x60,
                 'numpad_1': 0x61,
                 'numpad_2': 0x62,
                 'numpad_3': 0x63,
                 'numpad_4': 0x64,
                 'numpad_5': 0x65,
                 'numpad_6': 0x66,
                 'numpad_7': 0x67,
                 'numpad_8': 0x68,
                 'numpad_9': 0x69,
                 'multiply_key': 0x6A,
                 'add_key': 0x6B,
                 'separator_key': 0x6C,
                 'subtract_key': 0x6D,
                 'decimal_key': 0x6E,
                 'divide_key': 0x6F,
                 'F1': 0x70,
                 'F2': 0x71,
                 'F3': 0x72,
                 'F4': 0x73,
                 'F5': 0x74,
                 'F6': 0x75,
                 'F7': 0x76,
                 'F8': 0x77,
                 'F9': 0x78,
                 'F10': 0x79,
                 'F11': 0x7A,
                 'F12': 0x7B,
                 'F13': 0x7C,
                 'F14': 0x7D,
                 'F15': 0x7E,
                 'F16': 0x7F,
                 'F17': 0x80,
                 'F18': 0x81,
                 'F19': 0x82,
                 'F20': 0x83,
                 'F21': 0x84,
                 'F22': 0x85,
                 'F23': 0x86,
                 'F24': 0x87,
                 'num_lock': 0x90,
                 'scroll_lock': 0x91,
                 'browser_back': 0xA6,
                 'browser_forward': 0xA7,
                 'browser_refresh': 0xA8,
                 'browser_stop': 0xA9,
                 'browser_search': 0xAA,
                 'browser_favorites': 0xAB,
                 'browser_start_and_home': 0xAC,
                 'volume_mute': 0xAD,
                 'volume_Down': 0xAE,
                 'volume_up': 0xAF,
                 'next_track': 0xB0,
                 'previous_track': 0xB1,
                 'stop_media': 0xB2,
                 'play/pause_media': 0xB3,
                 'start_mail': 0xB4,
                 'select_media': 0xB5,
                 'start_application_1': 0xB6,
                 'start_application_2': 0xB7,
                 'attn_key': 0xF6,
                 'crsel_key': 0xF7,
                 'exsel_key': 0xF8,
                 'play_key': 0xFA,
                 'zoom_key': 0xFB,
                 'clear_key': 0xFE,
                 '+': 0xBB,
                 ',': 0xBC,
                 '-': 0xBD,
                 '.': 0xBE,
                 '/': 0xBF,
                 '`': 0xC0,
                 ';': 0xBA,
                 '[': 0xDB,
                 '\\': 0xDC,
                 ']': 0xDD,
                 "'": 0xDE,
                 'windows_key': 0x5B}

    # creates readme
    try:
        with open(DIRECTORY + README_FILE, 'w') as readme:
            readme.write(README_TXT)
    except FileNotFoundError:
        os.mkdir(os.path.join(os.getenv("LOCALAPPDATA"), "KeystrokeShortcut"))
        with open(DIRECTORY + README_FILE, 'w') as readme:
            readme.write(README_TXT)
        os.system(DIRECTORY + README_FILE)

    # gets data from files
    automations = read_file(AUTOMATIONS_FILE)
    saved_shortcuts = read_file(SAVED_SHORTCUTS_FILE)
    settings = read_file(SETTINGS_FILE)

    # starts keylogger process
    keys_pressed = Manager().list()
    p = Process(target=key_logger, args=[keys_pressed, KEY_CODES])
    p.start()

    # waits for start/automations actions
    while True:
        time.sleep(.001)

        # checks if any automation start keys have been pressed
        for automation_start in automations:
            if list(keys_pressed) == automation_start['start']:
                for key in automation_start['start']:
                    win32api.keybd_event(KEY_CODES[key], 0, win32con.KEYEVENTF_KEYUP, 0)
                run_actions(automation_start['actions'])

        # opens settings window
        if list(keys_pressed) == ['ctrl', 'shift', 's']:
            Options().mainloop()

        # starts recording if right keys are pressed
        if list(keys_pressed) == ['ctrl', 'shift', 'r']:
            temp_keys_pressed = []
            recorded_keys = []
            win32api.keybd_event(KEY_CODES['ctrl'], 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(KEY_CODES['shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(KEY_CODES['r'], 0, win32con.KEYEVENTF_KEYUP, 0)
            window = RecordingOverlay()
            run = True
            t = time.time()

            while run:
                time.sleep(.001)
                window.update()

                for key_code in KEY_CODES:
                    if win32api.GetKeyState(KEY_CODES[key_code]) < 0 and temp_keys_pressed.count(key_code) == 0:
                        recorded_keys.append(f'time {time.time() - t}')
                        recorded_keys.append(f'down {key_code}')
                        temp_keys_pressed.append(key_code)
                        t = time.time()
                    elif win32api.GetKeyState(KEY_CODES[key_code]) >= 0 and temp_keys_pressed.count(key_code) == 1:
                        recorded_keys.append(f'time {time.time() - t}')
                        recorded_keys.append(f'up {key_code}')
                        temp_keys_pressed.remove(key_code)
                        t = time.time()

                try:
                    if temp_keys_pressed == ['ctrl', 'shift', 'r']:
                        recorded_keys.pop()
                        recorded_keys.pop()
                        recorded_keys.pop()
                        recorded_keys.pop()
                        recorded_keys.pop()
                        recorded_keys.pop()
                        win32api.keybd_event(KEY_CODES['ctrl'], 0, win32con.KEYEVENTF_KEYUP, 0)
                        win32api.keybd_event(KEY_CODES['shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
                        win32api.keybd_event(KEY_CODES['r'], 0, win32con.KEYEVENTF_KEYUP, 0)
                        run = False
                except IndexError:
                    pass

            window.destroy()
            if recorded_keys:
                window = DoneRecording(recorded_keys)
                window.mainloop()
