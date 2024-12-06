# Desktop Shortcut Maker

`desktop-shortcut-maker` is a Python library that helps you create `.desktop` shortcuts for URLs, making it easy to create shortcuts for websites or web applications on your desktop.

With this library, you can create a clickable shortcut for any URL and specify an optional icon to use for the shortcut. The shortcut is created in the standard location for application shortcuts on Linux: `~/.local/share/applications/`.

## Features

- Create `.desktop` shortcuts for any URL.
- Optionally specify an icon URL for the shortcut.
- Automatically set the shortcut to open the URL in the default web browser.
- Make the shortcut executable to be used from the application menu or desktop.

## Installation

You can install `desktop-shortcut-maker` using `pip`:

```bash
pip install desktop-shortcut-maker
```
## Usage
Once installed, you can create a shortcut by running the following command in your terminal:

```bash
desktop-shortcut-maker
```

Example: 
You will be prompted to enter the following:

- Name: The name of the shortcut (e.g., ChatGPT).
- URL: The URL to open when the shortcut is clicked (e.g., https://chat.openai.com).
- Icon URL: Optionally, you can provide a URL for the icon to display in the shortcut (e.g., https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg).

Output
- A .desktop file will be created in ~/.local/share/applications/ with the given name, URL, and icon. 
  
This file will be executable and can be used to launch the URL in your web browser.

Example
```bash Copy code
Welcome to the Desktop Shortcut Maker!
Enter the name of the shortcut: ChatGPT Chrome
Enter the URL: https://chat.openai.com
Enter the icon URL (optional): https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg
Shortcut 'ChatGPT Chrome' created successfully!
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Feel free to fork the repository, submit issues, and make pull requests. Contributions are welcome!

Author
Your Name - [himanshukrjha004@gmail.com]

## Summary:
- **LICENSE**: MIT License, allowing free usage and modification of the code.
- **README.md**: Contains details on the package, installation instructions, usage, and an example.