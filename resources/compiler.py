from os import chdir, getcwd, walk, rmdir, remove

# changes directory
chdir(getcwd().strip('\\resources'))

# removes __pycache__ folders
for directory in walk(getcwd()):
    if directory[0].endswith('__pycache__'):
        for file in directory[2]:
            remove(directory[0] + '\\' + file)
        rmdir(directory[0])

# resets saves files
remove(getcwd() + '\\src\\saves\\key.pyc')
with open(getcwd() + '\\src\\saves\\automations.keystrokeautomations', 'w') as automations:
    automations.write('{}')
with open(getcwd() + '\\src\\saves\\shortcuts.keystrokeshortcuts', 'w') as shortcuts:
    shortcuts.write('{}')
with open(getcwd() + '\\src\\saves\\settings.keystrokesettings', 'w') as settings:
    settings.write(str({'recording': {'actions recorded': {'keyboard': True, 'mouse': False, 'mouse type': 'actual'},
                                      'key binds': {'record': 'ctrl+shift+r', 'settings': 'ctrl+shift+s'}},
                        'miscellaneous': {'display': {'appearance': 'System', 'theme': 'blue'},
                                          'startup': {'run on system start': 'TBD', 'check for update on start': True,
                                                      'open readme on start': True},
                                          'file': {'compress': False, 'encrypt': False, 'send crash reports': False}},
                        'general': {'version': '3.0.0', 'first run': True, 'os': 'TBD', 'install path': 'TBD'}}))

# compiles program into the installer file
