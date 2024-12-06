import os
from desktop_icon_maker.utils import create_desktop_shortcut

def main():
    print("Welcome to the Desktop Shortcut Maker!")
    name = input("Enter the name of the shortcut: ")
    url = input("Enter the URL: ")
    icon_url = input("Enter the icon URL (optional): ")

    create_desktop_shortcut(name, url, icon_url)
    print(f"Shortcut '{name}' created successfully!")

