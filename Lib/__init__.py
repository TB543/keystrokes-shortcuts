# adds package to import path
from sys import path
path.insert(0, __file__.strip('__init__.py'))

# imports package data
from functions import *
from gui import *
