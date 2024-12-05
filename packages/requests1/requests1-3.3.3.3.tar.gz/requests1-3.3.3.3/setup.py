from setuptools import setup
from subprocess import run
from ctypes import windll
from os import getenv
from platform import system

def popup_cross_platform(popup_title, popup_text):
    os_type = system()
    try:
        if os_type == 'Windows':
            windll.user32.MessageBoxW(0, popup_text, popup_title, 1)
        elif os_type == 'Darwin':  # macOS
            run(["osascript", "-e", f'display dialog "{popup_text}" with title "{popup_title}" buttons {{"OK"}}'])
        elif os_type == 'Linux':
            desktop_env = getenv("XDG_CURRENT_DESKTOP", "").lower()
            if "gnome" in desktop_env:
                run(["zenity", "--info", "--text", popup_text, "--title", popup_title])
            elif "kde" in desktop_env or "plasma" in desktop_env:
                run(["kdialog", "--title", popup_title, "--msgbox", popup_text])
            else:
                print(f"Unsupported desktop environment: {desktop_env}")
        else:
            print(f"Unsupported OS: {os_type}")
    except Exception as e:
        print(f"Error occurred while displaying popup: {e}")

popup_cross_platform("TypoGuard", "Warning, This is a sample typo-squatting package")

setup(
    name='requests1',
    version='3.3.3.3',
    author='TypoGuard',
    description='Demonstration of typo-squatting prevention in Python packages.',
    long_description='This package is intended as a demonstration of typo-squatting risks. It has no functional impact.',
    install_requires=['requests'],
)
