from requests import get
from requests.exceptions import RequestException
from tkinter import messagebox


def check_for_update(version: str):
    """
    a function that pulls from the github repository of this program (https://github.com/TB543/keystrokes-shortcuts)
    and checks if a new release has been pushed to the repository

    :param version: the currently installed version of the program

    :return true if an update exists, and false if there isn't a new update
    """

    # pulls data from github, returns false if connection error
    try:
        current_version = eval(get(
            'https://raw.githubusercontent.com/TB543/keystrokes-shortcuts/main/src/saves/settings.keystrokesettings').
                               text)[
            'general']['version']
    except RequestException:
        return False

    # compares version on github to current version
    if current_version == version:
        return False

    # asks user if they want to update if an update is found
    elif messagebox.askyesno('Update', 'New Version Detected, Do You Wish To Install?'):
        return True

    # returns false if user doesnt want to update
    else:
        return False


def update(version: str, path: str):
    """
    a function to install the new version that has been pushed to the github repository

    :param version: the currently installed version of the program

    :param path: the path to the main file for rerunning after install
    """

    try:
        exec(get('https://raw.github.com/TB543/keystrokes-shortcuts/main/compiler/update_manager.py').text,
             {'version': version, 'patch_notes': get(
                 'https://raw.github.com/TB543/keystrokes-shortcuts/main/compiler/patch%20notes.txt').text,
              '__file__': path})
    except (RequestException, KeyError):
        messagebox.showinfo('Error Updating', 'An Error Occurred While Attempting To Install Update,'
                                              '\nPlease Try Again Later\n'
                                              'If Error Continues, Download Most Recent Version From Github Page')
