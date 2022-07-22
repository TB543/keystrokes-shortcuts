from keyboard import *
from keyboard import _Event as Event


def load(data: list[dict]):
    """
    note: keyboard needs to be used before playing back actions for program to 'recognise' keyboard
    loads a list saved keyboard actions by creating a list of KeyboardEvents from these actions

    :param data: a list of dictionaries containing all of the required class attributes for KeyboardEvents

    :return: a list of KeyboardEvents that can be easily replayed
    """

    # creates KeyboardEvent class instances and adds them to list
    actions = []
    for event in data:
        actions.append(KeyboardEvent(event['event_type'], event['scan_code'], event['name'], event['time'],
                                     event['device'], event['modifiers'], event['is_keypad']))

    # returns list of actions
    return actions


def process_hotkey(hotkey: str, wrapper: object):
    """
    processes a hotkey that is pressed that is assigned to this function

    :param hotkey: the hotkey that is pressed and will be set to the wrapper

    :param wrapper the class that holder the blocker and hotkey pressed variables
    """

    wrapper.hotkey_pressed = hotkey
    wrapper.blocker.set()
    wrapper.blocker = Event()
