import sys
from cx_Freeze import setup, Executable

setup(
    name = "Marco's Test GAme",
    version = "0.1",
    description = "Game",
    executables = [Executable("main.py", base = "Win32GUI")])