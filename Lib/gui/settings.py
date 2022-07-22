from window import *
from tkinter import Listbox
from webbrowser import open_new


class Settings(Window):
    """
    custom tkinter window subclass to represent the settings menu

    there are 4 groups of settings:
        --> automations/shortcut settings: create and delete automations/shortcuts, turn automations on/off,
            load shortcuts/automations
        --> recording settings: change which actions are recorded and key-binds
        --> miscellaneous settings: change ui theme, change startup settings, create desktop shortcut, check for update
        --> info: open readme/folder, donate, links to tutorials and github
        todo add password protected shortcuts/automations, add open readme on startup, add run repetitions to run
         shortcuts add send crash reports option
         optimize # of widgets
    """

    def __init__(self):
        """
        creates the settings window and all of its pages

        also configures some settings for the theme of the ui
        """

        # initializes super class, settings and class variables
        super().__init__(450)
        set_default_color_theme('blue')
        self.title('Settings')
        self.mouse_record_method = StringVar(value=Window.settings['recording']['actions recorded']['mouse type'])
        self.listbox = []

        # ------------------------------------------ Far Left Settings Frame ------------------------------------------

        # creates and places the groups of settings frame
        self.settings_group = [[CTkFrame(self.all_widgets[0][0]), 0, 5, LEFT, Y]]
        self.settings_group.extend([[CTkLabel(self.settings_group[-1][0], text='Select Settings To View',
                                              text_font=('Roboto Medium', -16)), 10, 10], [
                                        CTkFrame(self.settings_group[-1][0],
                                                 fg_color=vars(self.settings_group[-1][0])['fg_color']), 10, 10]])
        self.settings_group.extend([[CTkButton(self.settings_group[-1][0], text='Shortcut/Automation',
                                               command=lambda: self.load(
                                                   self.automations_shortcuts, 'Selected Settings Group',
                                                   self.settings_group[3][0], 'Shortcut/Automation')), 10, 10],
                                    # [CTkButton(self.settings_group[-1][0], text='Recording', command=lambda: self.load( todo
                                    #                   self.recording, 'Selected Settings Group',
                                    #                   self.settings_group[4][0], 'Recording')), 10, 10],
                                    [CTkButton(self.settings_group[-1][0], text='Miscellaneous',
                                               command=lambda: self.load(
                                                   self.miscellaneous, 'Selected Settings Group',
                                                   self.settings_group[4][0], 'Miscellaneous')), 10, 10],  # todo change 4 to 5
                                    [CTkButton(self.settings_group[-1][0], text='Information',
                                               command=lambda: self.load(
                                                   self.information, 'Selected Settings Group',
                                                   self.settings_group[5][0], 'Information')), 10, 10], # todo change 5 to 6
                                    [CTkFrame(self.all_widgets[0][0]), 0, 5, LEFT, Y]])
        self.settings_group.extend(
            [[CTkLabel(self.settings_group[-1][0], text='Select Setting', text_font=('Roboto Medium', -16)), 10, 10],
             [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10, 10],
             [CTkFrame(self.all_widgets[0][0]), 0, 5, LEFT, BOTH, True]])

        # ------------------------------------------- Center Settings Frame -------------------------------------------

        # creates the automations/shortcuts settings frame
        self.automations_shortcuts = [[CTkButton(self.settings_group[-2][0], text='Run Shortcuts',
                                                 command=lambda: self.load(self.run_shortcuts, 'Shortcut/Automation',
                                                                           self.automations_shortcuts[0][0])), 10, 10],
                                      [CTkButton(self.settings_group[-2][0], text='Create Automations',
                                                 command=lambda: self.load(self.create_automations,
                                                                           'Shortcut/Automation',
                                                                           self.automations_shortcuts[1][0])), 10, 10],
                                      # [CTkButton(self.settings_group[-2][0], text='Automations on/off', todo
                                      #            command=lambda: self.load(self.automations_on_off,
                                      #                                      'Shortcut/Automation',
                                      #                                      self.automations_shortcuts[2][0])), 10, 10],
                                      [CTkButton(self.settings_group[-2][0], text='Delete Shortcuts',
                                                 command=lambda: self.load(self.delete_shortcuts, 'Shortcut/Automation',
                                                                           self.automations_shortcuts[2][0])), 10, 10],  # todo change 2 to 3
                                      [CTkButton(self.settings_group[-2][0], text='Delete Automations',
                                                 command=lambda: self.load(self.delete_automations,
                                                                           'Shortcut/Automation',
                                                                           self.automations_shortcuts[3][0])), 10, 10],  # todo change 3 to 4
                                      # [CTkButton(self.settings_group[-2][0], text='Share/Load Files', todo
                                      #            command=lambda: self.load(self.share_load,
                                      #                                      'Shortcut/Automation',
                                      #                                      self.automations_shortcuts[5][0])), 10, 10]
                                      ]

        # creates the recording settings frame
        self.recording = [[CTkButton(self.settings_group[-2][0], text='Actions Recorded',
                                     command=lambda: self.load(self.actions_recorded, 'Recording',
                                                               self.recording[0][0])), 10, 10], [
                              CTkButton(self.settings_group[-2][0], text='Key-bind Settings',
                                        command=lambda: self.load(self.key_binds, 'Recording', self.recording[1][0])),
                              10, 10]]

        # creates the miscellaneous settings frame
        self.miscellaneous = [[CTkButton(self.settings_group[-2][0], text='Display Settings',
                                         command=lambda: self.load(self.display, 'Miscellaneous',
                                                                   self.miscellaneous[0][0])), 10, 10],
                              # [CTkButton(self.settings_group[-2][0], text='Startup Settings', todo
                              #            command=lambda: self.load(self.startup, 'Miscellaneous',
                              #                                      self.miscellaneous[1][0])), 10, 10],
                              [CTkButton(self.settings_group[-2][0], text='File Settings',
                                         command=lambda: self.load(self.file, 'Miscellaneous',
                                                                   self.miscellaneous[1][0])), 10, 10]]  # todo change 1 to 2

        # creates the information settings frame
        self.information = [
            # [CTkButton(self.settings_group[-2][0], text='Open Readme/Folder', todo
            #                            command=lambda: self.load(self.open_readme_folder, 'Information',
            #                                                      self.information[0][0])), 10, 10],
                            [CTkButton(self.settings_group[-2][0], text='External Links',
                                       command=lambda: self.load(self.links, 'Information',
                                                                 self.information[0][0])), 10, 10]]  # todo change first 0 to 1

        # ------------------------------------ Shortcut/Automations Settings Frame ------------------------------------

        # creates the run shortcuts page
        self.run_shortcuts = [
            [CTkLabel(self.settings_group[-1][0], text='Run Shortcuts:', text_font=('Roboto Medium', -16)), 10],
            [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.run_shortcuts.extend(
            [[CTkLabel(self.run_shortcuts[-1][0], text='Select Shortcut:', text_font=('Roboto Medium', -16))],
             [CTkOptionMenu(self.run_shortcuts[-1][0])],
             [CTkLabel(self.run_shortcuts[-1][0], text='Repetitions:', text_font=('Roboto Medium', -16))],
             [CTkEntry(self.run_shortcuts[-1][0], placeholder_text='Enter An Integer')],
             [CTkCheckBox(self.run_shortcuts[-1][0], text='No Delay', onvalue=True, offvalue=False,
                          variable=BooleanVar(value=True)), 20],
             [CTkButton(self.run_shortcuts[-1][0], text='Run', command=lambda: self.run(
                 Window.shortcuts_loaded[self.run_shortcuts[3][0].get()]['actions'], self.run_shortcuts[5][0].get(),
                 self.run_shortcuts[6][0].get()))]])
        Window.shortcut_option_menus.append(self.run_shortcuts[3][0])

        # creates the create automations page
        self.create_automations = [
            [CTkLabel(self.settings_group[-1][0], text='Create Automations:', text_font=('Roboto Medium', -16)), 10],
            [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.create_automations.extend(
            [[CTkLabel(self.create_automations[-1][0], text='Automation Name:', text_font=('Roboto Medium', -16))],
             [CTkEntry(self.create_automations[-1][0], placeholder_text='Enter Name')],
             [CTkFrame(self.create_automations[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color'])],
             [CTkFrame(self.create_automations[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color'])]])
        self.create_automations.extend([[CTkFrame(self.create_automations[-2][0],
                                                  fg_color=vars(self.settings_group[-1][0])['fg_color']), 10, 5, LEFT],
                                        [CTkFrame(self.create_automations[-2][0],
                                                  fg_color=vars(self.settings_group[-1][0])['fg_color']), 10, 5, RIGHT],
                                        [CTkFrame(self.create_automations[-1][0],
                                                  fg_color=vars(self.settings_group[-1][0])['fg_color']), 10, 5, LEFT],
                                        [CTkFrame(self.create_automations[-1][0],
                                                  fg_color=vars(self.settings_group[-1][0])['fg_color']), 10, 5, RIGHT]
                                        ])
        self.create_automations.extend(
            [[CTkLabel(self.create_automations[-4][0], text='Start Actions:', text_font=('Roboto Medium', -16))],
             [CTkButton(self.create_automations[-4][0], text='Click To Record', command=lambda: self.record_hotkey(
                 self.create_automations[10][0]))],
             [CTkLabel(self.create_automations[-3][0], text='Actions Performed:', text_font=('Roboto Medium', -16))],
             [CTkOptionMenu(self.create_automations[-3][0])],
             # [CTkLabel(self.create_automations[-2][0], text='Automation Group:', text_font=('Roboto Medium', -16))], todo
             # [CTkOptionMenu(self.create_automations[-2][0])],
             # [CTkLabel(self.create_automations[-1][0], text='Or Create New Group:', text_font=('Roboto Medium', -16))],
             # [CTkButton(self.create_automations[-1][0], text='Press To Create Group')],
             [CTkCheckBox(self.create_automations[-9][0], onvalue=0, offvalue=1, text='No Delay'), 20],
             [CTkButton(self.create_automations[-9][0], text='Create', command=lambda: self.create_automation(
                 self.create_automations[3][0].get(), self.create_automations[10][0].text,
                 self.create_automations[12][0].get(), self.create_automations[13][0].get()))]])
        Window.shortcut_option_menus.append(self.create_automations[13][0])
        self.create_automations.pop(-11)  # todo remove this line and change button function list indices as well above ^^

        # creates the automations on/off page
        self.automations_on_off = [
            [CTkLabel(self.settings_group[-1][0], text='Turn Automations On/Off:', text_font=('Roboto Medium', -16)),
             10], [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.automations_on_off.extend(
            [[CTkLabel(self.automations_on_off[-1][0], text='Select Automation:', text_font=('Roboto Medium', -16))],
             [CTkFrame(self.automations_on_off[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color'])],
             [CTkButton(self.settings_group[-1][0], text='Turn On'), 10],
             [CTkButton(self.settings_group[-1][0], text='Turn Off')],
             [CTkFrame(self.settings_group[-1][0], height=50, fg_color=vars(self.settings_group[-1][0])['fg_color'])],
             [CTkButton(self.settings_group[-1][0], text='Turn All On'), 10],
             [CTkButton(self.settings_group[-1][0], text='Turn All Off')]])
        scrollbar = CTkScrollbar(self.automations_on_off[-6][0], height=5, cursor='hand2')
        listbox = Listbox(self.automations_on_off[-6][0], font=('Roboto Medium', -16), height=5, highlightthickness=0,
                          yscrollcommand=scrollbar.set, selectmode=MULTIPLE, relief=FLAT, cursor='hand2')
        scrollbar.config(command=listbox.yview)
        self.listbox.append(listbox)
        self.automations_on_off.extend([[scrollbar, 0, 0, RIGHT, Y], [listbox, 0, 0, LEFT]])
        Window.automations_listbox.append(listbox)

        # creates the delete shortcuts page
        self.delete_shortcuts = [
            [CTkLabel(self.settings_group[-1][0], text='Delete Shortcuts:', text_font=('Roboto Medium', -16)), 10],
            [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.delete_shortcuts.extend(
            [[CTkLabel(self.delete_shortcuts[-1][0], text='Select Shortcut:', text_font=('Roboto Medium', -16))],
             [CTkFrame(self.delete_shortcuts[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color'])],
             [CTkButton(self.settings_group[-1][0], text='Delete', command=lambda: self.delete_save(
                 [self.delete_shortcuts[7][0].get(index) for index in self.delete_shortcuts[7][0].curselection()],
                 'shortcuts')), 10],
             [CTkButton(self.settings_group[-1][0], text='Delete All', command=lambda: self.delete_save(
                 list(Window.shortcuts_loaded.keys()), 'shortcuts'))]])
        scrollbar = CTkScrollbar(self.delete_shortcuts[-3][0], height=5, cursor='hand2')
        listbox = Listbox(self.delete_shortcuts[-3][0], font=('Roboto Medium', -16), height=5, highlightthickness=0,
                          yscrollcommand=scrollbar.set, selectmode=MULTIPLE, relief=FLAT, cursor='hand2')
        scrollbar.config(command=listbox.yview)
        self.listbox.append(listbox)
        self.delete_shortcuts.extend([[scrollbar, 0, 0, RIGHT, Y], [listbox, 0, 0, LEFT]])
        Window.shortcut_listbox = listbox

        # creates the delete automations page
        self.delete_automations = [
            [CTkLabel(self.settings_group[-1][0], text='Delete Automations:', text_font=('Roboto Medium', -16)), 10],
            [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.delete_automations.extend(
            [[CTkLabel(self.delete_automations[-1][0], text='Select Automation:', text_font=('Roboto Medium', -16))],
             [CTkFrame(self.delete_automations[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color'])],
             [CTkButton(self.settings_group[-1][0], text='Delete', command=lambda: self.delete_save(
                 [self.delete_automations[7][0].get(index) for index in self.delete_automations[7][0].curselection()],
                 'automations')), 10],
             [CTkButton(self.settings_group[-1][0], text='Delete All', command=lambda: self.delete_save(
                 list(Window.automations_unloaded.keys()), 'automations'))]])
        scrollbar = CTkScrollbar(self.delete_automations[-3][0], height=5, cursor='hand2')
        listbox = Listbox(self.delete_automations[-3][0], font=('Roboto Medium', -16), height=5, highlightthickness=0,
                          yscrollcommand=scrollbar.set, selectmode=MULTIPLE, relief=FLAT, cursor='hand2')
        scrollbar.config(command=listbox.yview)
        self.listbox.append(listbox)
        self.delete_automations.extend([[scrollbar, 0, 0, RIGHT, Y], [listbox, 0, 0, LEFT]])
        Window.automations_listbox.append(listbox)

        # creates share/load files page todo
        self.share_load = [[CTkLabel(self.settings_group[-1][0], text='Share/Load Automations/Shortcuts:',
                                     text_font=('Roboto Medium', -16)), 10],
                           [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']),
                            10]]

        # ------------------------------------------ Recording Settings Frame ------------------------------------------

        # creates the actions recorded frame
        self.actions_recorded = [
            [CTkLabel(self.settings_group[-1][0], text='Actions Recording Settings:', text_font=('Roboto Medium', -16)),
             10],
            [CTkLabel(self.settings_group[-1][0], text='Actions Recorded:', text_font=('Roboto Medium', -16)), 10],
            [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.actions_recorded.extend(
            [[CTkCheckBox(self.actions_recorded[-1][0], text='Keyboard', onvalue=True, offvalue=False,
                          variable=BooleanVar(value=Window.settings['recording']['actions recorded']['keyboard'])),
              10, 0, TOP, None, False, W],
             [CTkCheckBox(self.actions_recorded[-1][0], text='Mouse', onvalue=True, offvalue=False,
                          variable=BooleanVar(value=Window.settings['recording']['actions recorded']['mouse'])),
              10, 0, TOP, None, False, W],
             [CTkLabel(self.settings_group[-1][0], text='Mouse Record Method:', text_font=('Roboto Medium', -16)), 10],
             [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10, 0]])
        self.actions_recorded.extend([[CTkRadioButton(self.actions_recorded[-1][0], text='Actual Position',
                                                      variable=self.mouse_record_method, value='actual',
                                                      command=lambda: self.update_settings(
                                                          ['recording', 'actions recorded', 'mouse type'],
                                                          self.mouse_record_method.get())), 10, 0, TOP,
                                       None, False, W], [
                                          CTkRadioButton(self.actions_recorded[-1][0], text='Relative Position',
                                                         variable=self.mouse_record_method, value='relative',
                                                         command=lambda: self.update_settings(
                                                             ['recording', 'actions recorded', 'mouse type'],
                                                             self.mouse_record_method.get())), 10, 0,
                                          TOP, None, False, W]])
        self.actions_recorded[3][0].config(command=lambda: self.update_settings(
            ['recording', 'actions recorded', 'keyboard'], self.actions_recorded[3][0].get()))
        self.actions_recorded[4][0].config(command=lambda: self.update_settings(
            ['recording', 'actions recorded', 'mouse'], self.actions_recorded[4][0].get()))

        # creates key binds setting page
        self.key_binds = [
            [CTkLabel(self.settings_group[-1][0], text='Key-bind Settings:', text_font=('Roboto Medium', -16)), 10], [
                CTkLabel(self.settings_group[-1][0], text='Record: Ctrl + Shift + R\nSettings: Ctrl + Shift + S',
                         text_font=('Roboto Medium', -16)), 20],
            [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.key_binds.extend(
            [[CTkLabel(self.key_binds[-1][0], text='Change Record Key-bind:', text_font=('Roboto Medium', -16))],
             [CTkButton(self.key_binds[-1][0], text='Click To Record')],
             [CTkButton(self.key_binds[-1][0], text='Change'), 10],
             [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]])
        self.key_binds.extend(
            [[CTkLabel(self.key_binds[-1][0], text='Change Settings Key-bind:', text_font=('Roboto Medium', -16))],
             [CTkButton(self.key_binds[-1][0], text='Click To Record')],
             [CTkButton(self.key_binds[-1][0], text='Change'), 10]])

        # ---------------------------------------- Miscellaneous Settings Frame ----------------------------------------

        # creates display settings page
        self.display = [
            [CTkLabel(self.settings_group[-1][0], text='Display Settings:', text_font=('Roboto Medium', -16)), 10],
            [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.display.extend([[CTkLabel(self.display[-1][0], text='Appearance Mode:', text_font=('Roboto Medium', -16))],
                             [CTkOptionMenu(self.display[-1][0], values=['Light', 'Dark', 'System'],
                                            command=set_appearance_mode)],
                             [CTkFrame(self.settings_group[-1][0],
                                       fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]])
        self.display.extend([[CTkLabel(self.display[-1][0], text='Color Theme:', text_font=('Roboto Medium', -16))], [
            CTkOptionMenu(self.display[-1][0], values=['blue', 'green', 'dark-blue', 'sweetkind'],
                          command=self.set_default_color_theme)]])

        # creates startup settings page
        self.startup = [
            [CTkLabel(self.settings_group[-1][0], text='Startup Settings:', text_font=('Roboto Medium', -16)), 10],
            [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.startup.extend([[CTkSwitch(self.startup[-1][0], text='Run On System Startup', onvalue=True, offvalue=False,
                                        variable=BooleanVar(
                                            value=Window.settings['miscellaneous']['startup']['run on system start'])),
                              10, 0, TOP, None, False, W],
                             [CTkSwitch(self.startup[-1][0], text='Check For Update On Startup', onvalue=True,
                                        offvalue=False, variable=BooleanVar(
                                     value=Window.settings['miscellaneous']['startup']['check for update on start'])),
                              10, 0, TOP, None, False, W],
                             [CTkSwitch(self.startup[-1][0], text='Open Readme On Startup', onvalue=True,
                                        offvalue=False, variable=BooleanVar(
                                     value=Window.settings['miscellaneous']['startup']['open readme on start'])), 10,
                              0, TOP, None, False, W]])
        self.startup[2][0].config(
            command=lambda: self.update_settings(['miscellaneous', 'startup', 'run on system start'],
                                                 self.startup[2][0].get()))
        self.startup[3][0].config(
            command=lambda: self.update_settings(['miscellaneous', 'startup', 'check for update on start'],
                                                 self.startup[3][0].get()))
        self.startup[4][0].config(
            command=lambda: self.update_settings(['miscellaneous', 'startup', 'open readme on start'],
                                                 self.startup[4][0].get()))

        # creates file save settings page
        self.file = [
            [CTkLabel(self.settings_group[-1][0], text='File Settings:', text_font=('Roboto Medium', -16)), 10],
            [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.file.extend([[CTkSwitch(self.file[-1][0], text='Compress Data', onvalue=True, offvalue=False,
                                     variable=BooleanVar(value=Window.settings['miscellaneous']['file']['compress'])),
                           10, 0, TOP, None, False, W],
                          [CTkSwitch(self.file[-1][0], text='Encrypt Data', onvalue=True, offvalue=False,
                                     variable=BooleanVar(value=Window.settings['miscellaneous']['file']['encrypt'])),
                           10, 0, TOP, None, False, W],
                          # [CTkSwitch(self.file[-1][0], text='Anonymously Send Crash Reports', onvalue=True, todo
                          #            offvalue=False, variable=BooleanVar(value=Window.settings['miscellaneous']['file']
                          # #            ['send crash reports'])), 10, 0, TOP, None, False, W],
                          # [CTkButton(self.file[-1][0], text='Check For Update', width=160), 10],
                          # [CTkButton(self.file[-1][0], text='Create Desktop Shortcut', width=160), 10]
                          ])
        self.file[2][0].config(
            command=lambda: self.update_settings(['miscellaneous', 'file', 'compress'],
                                                 self.file[2][0].get(), True))
        self.file[3][0].config(
            command=lambda: self.update_settings(['miscellaneous', 'file', 'encrypt'],
                                                 self.file[3][0].get(), True))
        # self.file[4][0].config( todo
        #     command=lambda: self.update_settings(['miscellaneous', 'file', 'send crash reports'],
        #                                          self.file[4][0].get(), True))

        # ----------------------------------------- Information Settings Frame -----------------------------------------

        # creates the open readme/folder page
        self.open_readme_folder = [
            [CTkLabel(self.settings_group[-1][0], text='Open Readme Or Folder:', text_font=('Roboto Medium', -16)), 10],
            [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.open_readme_folder.extend([[CTkButton(self.open_readme_folder[-1][0], text='Open Readme'), 10],
                                        [CTkButton(self.open_readme_folder[-1][0], text='Open Folder'), 10]])

        # creates external links page
        self.links = [
            [CTkLabel(self.settings_group[-1][0], text='External Links:', text_font=('Roboto Medium', -16)), 10],
            [CTkFrame(self.settings_group[-1][0], fg_color=vars(self.settings_group[-1][0])['fg_color']), 10]]
        self.links.extend([[CTkButton(self.links[-1][0], text='Github Link', command=lambda: open_new(
            'https://github.com/TB543/keystrokes-shortcut-2')), 10],
                           [CTkButton(self.links[-1][0], text='YouTube Tutorial'), 10],
                           [CTkButton(self.links[-1][0], text='Support Developer', command=lambda: open_new(
                               'https://account.venmo.com/u/TB543')), 10],
                           # [CTkButton(self.links[-1][0], text='Report Bug', command=lambda: open_new( todo
                           #     'https://github.com/TB543/keystrokes-shortcut-2' '/issues')), 10],
                           # [CTkButton(self.links[-1][0], text='Request Feature', command=lambda: open_new(
                           #     'https://github.com/TB543/keystrokes-shortcut-2/discussions/1')), 10]
                           ])

        # ------------------------------------------ Class Variables and Load ------------------------------------------

        # loads the all widgets variable and sets them to theme saved in settings
        for page in [self.settings_group, self.automations_shortcuts, self.recording, self.miscellaneous,
                     self.information, self.run_shortcuts, self.create_automations, self.automations_on_off,
                     self.delete_shortcuts, self.delete_automations, self.share_load, self.actions_recorded,
                     self.key_binds, self.display, self.startup, self.file, self.open_readme_folder, self.links]:
            for widget in page:
                self.all_widgets.append(widget)
        self.set_default_color_theme()

        # creates dictionary of selections on each page
        self.selected_pages = {'Selected Settings Group': {'Page Data': self.automations_shortcuts,
                                                           'Page Button': self.settings_group[3][0],
                                                           'Selected Setting': 'Shortcut/Automation'},
                               'Shortcut/Automation': {'Page Data': self.run_shortcuts,
                                                       'Page Button': self.automations_shortcuts[0][0]},
                               'Recording': {'Page Data': self.actions_recorded, 'Page Button': self.recording[0][0]},
                               'Miscellaneous': {'Page Data': self.display, 'Page Button': self.miscellaneous[0][0]},
                               'Information': {'Page Data': self.links,  # todo change to self.open_readme_folder
                                               'Page Button': self.information[0][0]}}

        # configures buttons and selection options of listbox/option menus
        self.update_widgets()
        for button in self.selected_pages.values():
            button['Page Button'].config(state=DISABLED, fg_color=None)

        # loads initial page
        self.place_widgets(self.settings_group)
        self.place_widgets(self.selected_pages['Selected Settings Group']['Page Data'])
        self.place_widgets(
            self.selected_pages[self.selected_pages['Selected Settings Group']['Selected Setting']]['Page Data'])

    def load(self, new_page: list[list[CTkBaseClass, int, int, str, str, bool]] or list[list[None]], change_path: str,
             button: CTkButton, new_selected_setting: str = None):
        """
        unloads the previous page and loads a new one as well as enables/disables buttons

        :param button: the button that is clicked, this will button will be disabled

        :param change_path: the path in self.selected_pages to the page/button that will be changed

        :param new_page: the new page that will be loaded
        lists should be in this form: [<Widget>, <pad-x>, <pad-y>, <side>, <fill>, <expand>]
        note: these parameters are organized from most used to least used, so the ones that arent used can be skipped
        be aware that it is based on index, so all parameters up until the last one needed should be listed
        note: default values are [<Widget>, 0, 0, TOP, None, False, None]

        :param new_selected_setting: an optional parameter that is used when settings group buttons are pressed to load
        a new setting page as well as selected settings group page
        """

        # unloads previous page and loads new page
        self.remove_widgets(self.selected_pages[change_path]['Page Data'])
        self.place_widgets(new_page)

        # enables old button and disables new button
        self.selected_pages[change_path]['Page Button'].config(state=NORMAL,
                                                               fg_color=ThemeManager.theme['color']['button'])
        button.config(state=DISABLED, fg_color=None)

        # saves data
        self.selected_pages[change_path]['Page Data'] = new_page
        self.selected_pages[change_path]['Page Button'] = button

        # loads setting page if new_selected setting is given
        if new_selected_setting:

            # unload old page and load new one
            self.remove_widgets(self.selected_pages[self.selected_pages[change_path]['Selected Setting']]['Page Data'])
            self.place_widgets(self.selected_pages[new_selected_setting]['Page Data'])

            # saves data
            self.selected_pages[change_path]['Selected Setting'] = new_selected_setting

    def set_appearance_mode(self, mode_string):
        """
        a modified set appearance mode function to also change the appearance of the listbox/scrollbars

        :param mode_string: the new appearance mode to be changed to represented as a string. can be light, dark or
        system. if None is given only appearance mode of listbox will be changed
        """

        # changes appearance mode if mode string is given
        if mode_string:
            super().set_appearance_mode(mode_string)

            # updates appearance mode in settings
            self.update_settings(['miscellaneous', 'display', 'appearance'], mode_string)

        # changes appearance mode of listbox if in light mode
        if self.appearance_mode == 0:
            for listbox in self.listbox:
                listbox.config(background=ThemeManager.theme['color']['scrollbar_button'][0], fg='black',
                               selectbackground=ThemeManager.theme['color']['button'][0])

        # changes appearance mode of listbox if in dark mode
        else:
            for listbox in self.listbox:
                listbox.config(bg=ThemeManager.theme['color']['scrollbar_button'][1], fg='white',
                               selectbackground=ThemeManager.theme['color']['button'][1])

    def record_hotkey(self, button: CTkButton):
        """
        records a hotkey to be set for either an automation, new actions to open settings window, or record hotkey

        :param button: the button object, this will change the text on the button
        """

        button.config(text='Recording')
        self.update()
        button.config(text=read_hotkey(False))

    def create_automation(self, name: str, start: str, shortcut: str, delay: int):
        """
        creates a new automation

        :param name: the name of the new automation

        :param start: the start hotkey for the automation

        :param shortcut: the name of the shortcut containing the actions for the automation

        :param delay: multiplier of how fast shortcut should run, 0 is fast as possible, 1 is normal speed
        """

        # checks for errors todo error and success widgets (error for no selected actions)
        if not name:
            raise NameError('enter a name')
        elif list(Window.automations_unloaded.keys()).count(name) > 0:
            raise NameError('name already exists')
        elif list(Window.running_hotkeys.keys()).count(start) > 0:
            raise KeyError('start key already exists')

        # saves new hotkey to file
        Window.automations_unloaded[name] = {'start': start,
                                             'delay': delay,
                                             'actions': Window.shortcuts_unloaded[shortcut]['actions']}
        self.write_to_file('saves/automations.keystrokeautomations', Window.automations_unloaded)

        # loads new hotkey into memory
        Window.running_hotkeys[start] = add_hotkey(start, play,
                                                   [Window.shortcuts_loaded[shortcut]['actions'], delay])

        # updates widgets containing automations
        self.update_widgets('automations')

    def delete_save(self, names: tuple, delete_type: str):
        """
        deletes either a shortcut or automation from memory and save files

        :param names: the selected names of the shortcut/automations to be deleted

        :param delete_type: determines if the save being removed is a shortcut or automation
        can be 'shortcuts' for shortcut or 'automations' for automation, otherwise an error will be raised
        """

        # deletes shortcuts
        if delete_type == 'shortcuts':
            for name in names:
                Window.shortcuts_loaded.pop(name)
                Window.shortcuts_unloaded.pop(name)
            self.write_to_file('saves/shortcuts.keystrokeshortcuts', Window.shortcuts_unloaded)

        # deletes automations
        elif delete_type == 'automations':
            for name in names:
                remove_hotkey(Window.running_hotkeys[Window.automations_unloaded[name]['start']])
                Window.running_hotkeys.pop(Window.automations_unloaded[name]['start'])
                Window.automations_unloaded.pop(name)
            self.write_to_file('saves/automations.keystrokeautomations', Window.automations_unloaded)

        # raises error if wrong type is given
        else:
            raise TypeError(f'{delete_type} is not a valid update type, see function docstring for more info')

        # updates widgets displaying shortcut/automation information
        self.update_widgets(delete_type)

    def update_settings(self, setting_path: list, value, update_files: bool = False):
        """
        updates the settings file as well as loaded settings

        :param setting_path: the path to the setting to be changed (ex. 'recording/actions recorded/keyboard')

        :param value: the nre value of this setting

        :param update_files: determines if shortcut and automation files need to be updated due to
        encryption/compression default is false
        """

        # updates loaded settings and settings file
        Window.settings[setting_path[0]][setting_path[1]][setting_path[2]] = value
        self.write_to_file('saves/settings.keystrokesettings', Window.settings)

        # updates other save files if needed
        if update_files:
            self.write_to_file('saves/shortcuts.keystrokeshortcuts', Window.shortcuts_unloaded)
            self.write_to_file('saves/automations.keystrokeautomations', Window.automations_unloaded)
