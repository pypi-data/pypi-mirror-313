import os

def create_desktop_shortcut(name, url, icon_url=None):
    """
    Creates a .desktop shortcut for a given URL.

    :param name: The name of the shortcut.
    :param url: The URL to open when the shortcut is clicked.
    :param icon_url: The URL of the icon (optional).
    """
    # Ensure the directory exists
    desktop_path = os.path.expanduser("~/.local/share/applications/")
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)

    # Define the path for the .desktop file
    shortcut_filename = f"{name.lower().replace(' ', '-')}-chrome.desktop"
    shortcut_path = os.path.join(desktop_path, shortcut_filename)

    # Create .desktop file content
    desktop_content = f"""
    [Desktop Entry]
    Version=1.0
    Name={name}
    Comment={name} Shortcut
    Exec=xdg-open {url}
    Icon={icon_url if icon_url else 'web-browser'}
    Terminal=false
    Type=Application
    Categories=Network;WebBrowser;
    """

    # Write content to the .desktop file
    with open(shortcut_path, "w") as shortcut_file:
        shortcut_file.write(desktop_content.strip())

    # Make the .desktop file executable
    os.chmod(shortcut_path, 0o755)

    print(f"Shortcut created at: {shortcut_path}")
