from requests import get
from tkinter import messagebox


def check_for_update(version: str):
    """
    a function that pulls from the github repository of this program (https://github.com/TB543/keystrokes-shortcuts)
    and checks if a new release has been pushed to the repository

    :param version: the currently installed version of the program

    :return true if an update exists, and false if there isn't a new update
    """

    return False  # github has changed the link to repo, code will say no update until I can fix

    # # pulls data and compares version to current version
    # if eval(get('https://raw.githubusercontent.com/TB543/keystrokes-shortcuts/main/src/saves/settings.keystrokesettings'
    #             ).text)['general']['version'] == version:
    #     return False
    #
    # # # asks user if they want to update if an update is found todo
    # # elif messagebox.askyesno('Update', 'New Version Detected, Do You Wish To Install?'):
    # #     return True
    #
    # # returns false if user doesnt want to update
    # else:
    #     messagebox.showinfo('Update Available', 'An Update Is Available, Navigate To The Github Link To Install')  # todo remove line
    #     return False


def update():
    """
    a function to install the new version that has been pushed to the github repository todo
    """
    # print('updating')
    pass
