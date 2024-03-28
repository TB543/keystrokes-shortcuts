from customtkinter import *
from customtkinter.widgets.widget_base_class import CTkBaseClass
from gui_functions import *
from time import sleep


class Window(CTk):
    """
    custom tkinter window subclass that will be used as a superclass for the settings and done recording window
    todo optimize imports when guis are complete, reset all error widgets and user selections after save, page refresh
     and window close
    """

    # loads save data from files
    settings = read_file('saves/settings.keystrokesettings')
    shortcuts_unloaded = read_file('saves/shortcuts.keystrokeshortcuts')
    automations_unloaded = read_file('saves/automations.keystrokeautomations')
    set_appearance_mode(settings['miscellaneous']['display']['appearance'])

    # loads shortcut data into memory
    shortcuts_loaded = read_file('saves/shortcuts.keystrokeshortcuts')
    for name in shortcuts_loaded.keys():
        shortcuts_loaded[name]['actions'] = load(shortcuts_loaded[name]['actions'])

    # loads automation data into memory
    running_hotkeys = {}
    for name in automations_unloaded.keys():
        running_hotkeys[automations_unloaded[name]['start']] = add_hotkey(
            automations_unloaded[name]['start'], play, [
                load(automations_unloaded[name]['actions']), automations_unloaded[name]['delay']])

    # loads additional class data
    subclasses = []
    hotkey_pressed = None
    blocker = Event()
    shortcut_option_menus = []
    shortcut_listbox = None
    automations_listbox = []

    def __init__(self, height: int):
        """
        creates the window with required settings

        :param height: the desired height of the window
        width is calculated using the display ratio of 1.75
        """

        # initializes super class
        super().__init__()

        # sets class variables
        self.width = int(height * 1.75 * self.window_scaling)
        self.height = int(height * self.window_scaling)
        self.all_widgets = [[CTkFrame(self, fg_color=vars(self)['fg_color']), 10, 5, None, BOTH, True]]
        self.place_widgets(self.all_widgets)
        Window.subclasses.append(self)
        self.active_error_widgets = {'run shortcut': None, 'create automations': None, 'save shortcut': None}
        self.select_shortcut_error = None  # placeholder variable

        # configures settings for window
        self.protocol('WM_DELETE_WINDOW', self.hide)
        self.attributes('-topmost', True)
        self.window_scaling = 1
        self.resizable(0, 0)
        self.hide()

    def hide(self):
        """
        exits the windows mainloop (without destroying it) and hides the window
        """

        self.withdraw()
        self.quit()

    def mainloop(self):
        """
        a modified mainloop method from the super class that shows the window before starting the mainloop and resets
        window placement/geometry
        """

        self.geometry(f'{self.width}x{self.height}+{self.winfo_screenwidth() - (self.width + 25)}+'
                      f'{self.winfo_screenheight() - (self.height + 100)}')
        self.deiconify()
        super().mainloop()

    def set_default_color_theme(self, color_theme: str = None):
        """
        changes the color theme of all widgets

        :param color_theme: a string representing the color theme to be changed to if not given, theme saved in settings
        will be loaded todo exclude color updates to error widgets
        """

        # loads the new theme, saves it in settings, and prepares all subclass windows to be modified
        if color_theme:
            set_default_color_theme(color_theme)
            Window.settings['miscellaneous']['display']['theme'] = color_theme
            write_file('saves/settings.keystrokesettings', Window.settings,
                       Window.settings['miscellaneous']['file']['encrypt'],
                       Window.settings['miscellaneous']['file']['compress'])
            windows = Window.subclasses

        # loads single window to theme saved in settings if no color theme is given
        else:
            set_default_color_theme(Window.settings['miscellaneous']['display']['theme'])
            windows = [self]

        # changes the color of every widget in every window
        for window in windows:
            for widget in window.all_widgets:

                # gets widget type from widget data
                widget = widget[0]
                widget_type = str(vars(widget)['_name']).lower().replace('!', '').replace('0', '').replace('1', '').\
                    replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').\
                    replace('7', '').replace('8', '').replace('9', '').replace('ctk', '')

                # configures widget text
                widget.text_color_disabled = ThemeManager.theme["color"]["text_disabled"]
                widget.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"])
                widget.text_color = ThemeManager.theme["color"]["text"]

                # changes color of button
                if widget_type == 'button':
                    widget.corner_radius = ThemeManager.theme["shape"]["button_corner_radius"]
                    widget.border_width = ThemeManager.theme["shape"]["button_border_width"]
                    widget.config(hover_color=ThemeManager.theme["color"]["button_hover"],
                                  border_color=ThemeManager.theme["color"]["button_border"],
                                  text_color=ThemeManager.theme["color"]["text"])
                    if vars(widget)['state'] == 'normal':
                        widget.config(fg_color=ThemeManager.theme['color']['button'])

                # changes color of frame
                elif widget_type == 'frame':
                    widget.config(border_color=ThemeManager.theme["color"]["frame_border"],
                                  fg_color=ThemeManager.theme["color"]["frame_low"],
                                  corner_radius=ThemeManager.theme["shape"]["frame_corner_radius"],
                                  border_width=ThemeManager.theme["shape"]["frame_border_width"])

                # changes color of label
                elif widget_type == 'label':
                    widget.corner_radius = ThemeManager.theme["shape"]["label_corner_radius"]
                    widget.config(fg_color=ThemeManager.theme["color"]["label"],
                                  text_color=ThemeManager.theme["color"]["text"])

                # changes color of option menu
                elif widget_type == 'optionmenu':
                    widget.corner_radius = ThemeManager.theme["shape"]["button_corner_radius"]
                    widget.config(fg_color=ThemeManager.theme["color"]["button"],
                                  button_color=ThemeManager.theme["color"]["optionmenu_button"],
                                  button_hover_color=ThemeManager.theme["color"]["optionmenu_button_hover"],
                                  text_color=ThemeManager.theme["color"]["text"])

                # changes color of switch
                elif widget_type == 'switch':
                    widget.corner_radius = ThemeManager.theme["shape"]["switch_corner_radius"]
                    widget.button_length = ThemeManager.theme["shape"]["switch_button_length"]
                    widget.config(fg_color=ThemeManager.theme["color"]["switch"],
                                  progress_color=ThemeManager.theme["color"]["switch_progress"],
                                  button_color=ThemeManager.theme["color"]["switch_button"],
                                  button_hover_color=ThemeManager.theme["color"]["switch_button_hover"],
                                  border_width=ThemeManager.theme["shape"]["switch_border_width"])

                # changes color of scrollbar
                elif widget_type == 'scrollbar':
                    widget.scrollbar_hover_color = ThemeManager.theme["color"]["scrollbar_button_hover"]
                    widget.fg_color = ThemeManager.theme["color"]["frame_high"]
                    widget.scrollbar_color = ThemeManager.theme["color"]["scrollbar_button"]
                    try:
                        widget.corner_radius = ThemeManager.theme["shape"]["scrollbar_corner_radius"]
                    except KeyError:
                        pass
                    try:
                        widget.border_spacing = ThemeManager.theme["shape"]["scrollbar_border_spacing"]
                    except KeyError:
                        pass

                # changes color of checkbox
                elif widget_type == 'checkbox':
                    widget.checkmark_color = ThemeManager.theme["color"]["checkmark"]
                    widget.corner_radius = ThemeManager.theme["shape"]["checkbox_corner_radius"]
                    widget.border_width = ThemeManager.theme["shape"]["checkbox_border_width"]
                    widget.config(fg_color=ThemeManager.theme["color"]["button"],
                                  hover_color=ThemeManager.theme["color"]["button_hover"],
                                  border_color=ThemeManager.theme["color"]["checkbox_border"],
                                  text_color=ThemeManager.theme["color"]["text"])

                # changes color of radiobutton
                elif widget_type == 'radiobutton':
                    widget.corner_radius = ThemeManager.theme["shape"]["radiobutton_corner_radius"]
                    widget.border_width_unchecked = ThemeManager.theme["shape"]["radiobutton_border_width_unchecked"]
                    widget.border_width_checked = ThemeManager.theme["shape"]["radiobutton_border_width_checked"]
                    widget.ext_color = ThemeManager.theme["color"]["text"]
                    widget.config(fg_color=ThemeManager.theme["color"]["button"],
                                  hover_color=ThemeManager.theme["color"]["button_hover"],
                                  border_color=ThemeManager.theme["color"]["checkbox_border"])

                # changes color of entry
                elif widget_type == 'entry':
                    widget.border_width = ThemeManager.theme["shape"]["entry_border_width"]
                    widget.config(fg_color=ThemeManager.theme["color"]["entry"],
                                  placeholder_text_color=ThemeManager.theme["color"]["entry_placeholder_text"],
                                  border_color=ThemeManager.theme["color"]["entry_border"],
                                  corner_radius=ThemeManager.theme["shape"]["button_corner_radius"])

                # passes if given a listbox (color will be changed later)
                elif widget_type == 'listbox':
                    pass

                # raises error if its a different widget
                else:
                    raise NotImplementedError(f'a widget type was given that could not be parsed: {widget_type}')

            # changes color of master window and base frame
            window.config(fg_color=ThemeManager.theme["color"]["window_bg_color"])
            window.all_widgets[0][0].config(fg_color=vars(window)['fg_color'])

            # updates appearance mode (same method where listbox color is changed)
            window.set_appearance_mode(None)

    def update_widgets(self, update_type: str = 'both'):
        """
        updates changes to shortcuts/automations (new shortcut/automation or deleted shortcut/automation) within widgets
        that display shortcuts and automations

        :param update_type: the type of widgets to be updated can be 'shortcuts', 'automations' or 'both', default value
        is both
        """

        # updates shortcut widgets
        if update_type == 'shortcuts':

            # updates shortcut option menus
            for option_menu in Window.shortcut_option_menus:
                option_menu.config(values=Window.shortcuts_loaded.keys())

            # updates shortcut listbox
            Window.shortcut_listbox.delete(0, END)
            Window.shortcut_listbox.config(listvariable=StringVar(value=list(Window.shortcuts_loaded.keys())))

        # updates automation widgets todo, also add default selections
        elif update_type == 'automations':
            for listbox in self.automations_listbox:
                listbox.delete(0, END)
                listbox.config(listvariable=StringVar(value=list(Window.automations_unloaded.keys())))

        # calls function twice to update with both options
        elif update_type == 'both':
            self.update_widgets('shortcuts')
            self.update_widgets('automations')

        # raises error if invalid type is given
        else:
            raise TypeError(f'{update_type} is not a valid update type, see function docstring for more info')

    def run(self, actions: list[str], repetitions: int, no_delay: bool):
        """
        runs a recorded shortcut

        :param actions: a list of actions to perform

        :param repetitions: the number of times to repeat the actions

        :param no_delay: determines if the actions should be run as quickly as possible for exactly as they were
        recorded
        """

        # makes sure valid int is given todo none selected error
        self.remove_widgets(self.active_error_widgets['run shortcut'])
        try:
            if repetitions == str(int(repetitions)) and int(repetitions) > 0:
                repetitions = int(repetitions)
            else:
                raise ValueError
        except ValueError:
            self.place_widgets(self.enter_valid_int_error)
            self.active_error_widgets['run shortcut'] = self.enter_valid_int_error
            return

        # hides window
        self.withdraw()
        sleep(.001)

        # sets speed factor
        if no_delay:
            speed = 0
        else:
            speed = 1

        # plays back actions
        for _ in range(repetitions):
            play(actions, speed)

        # shows window
        self.deiconify()

    @staticmethod
    def place_widgets(widgets: list[list[CTkBaseClass, int, int, str, str, bool]] or list[list[None]]):
        """
        places a list of widgets on the screen

        :param widgets: a list list containing widgets and pack settings to be placed on the screen

        lists should be in this form: [<Widget>, <pad-y>, <pad-x>, <side>, <fill>, <expand>, <anchor>]

        note: these parameters are organized from most used to least used, so the ones that arent used can be skipped
        be aware that it is based on index, so all parameters up until the last one needed should be listed

        note: default values are [<Widget>, 0, 0, TOP, None, None, False, CENTER]
        """

        # loops through every widget
        for widget in widgets:

            # makes sure list is right length
            for i in range(6):
                try:
                    widget[i]
                except IndexError:
                    widget.append(None)
            widget.append(CENTER)

            # places widget
            widget[0].pack(pady=widget[1], padx=widget[2], side=widget[3],
                           fill=widget[4], expand=widget[5], anchor=widget[6])

    @staticmethod
    def remove_widgets(widgets: list[list[CTkBaseClass, int, int, str, str, bool]] or None):
        """
        unpacks a list of widgets from the screen does nothing if none is given

        :param widgets: a list list containing widgets and pack settings to be removed from the screen
        lists should be in this form: [<Widget>, <pad-y>, <pad-x>, <side>, <fill>, <expand>, <anchor>]
        note that only the <Widget> will be used, but this form makes it easy for place_widgets()
        """
        if widgets:
            for widget in widgets:
                widget[0].pack_forget()

    @staticmethod
    def write_to_file(file_path: str, data: dict):
        """
        saves the data to the selected file with the correct encryption/compression settings

        :param file_path: the path to the save file

        :param data: the data to be written to the file, note: this will override old data
        """
        write_file(file_path, data, Window.settings['miscellaneous']['file']['encrypt'],
                   Window.settings['miscellaneous']['file']['compress'])


# sets some of the class variables that could not be set during loaded of class
Window.running_hotkeys[Window.settings['recording']['key binds']['record']] = add_hotkey(
    Window.settings['recording']['key binds']['record'], process_hotkey, args=[
        Window.settings['recording']['key binds']['record'], Window])
Window.running_hotkeys[Window.settings['recording']['key binds']['settings']] = add_hotkey(
    Window.settings['recording']['key binds']['settings'], process_hotkey, args=[
        Window.settings['recording']['key binds']['settings'], Window])
