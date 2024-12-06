from setuptools import setup, find_packages

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="desktop-icon-maker",
    version="0.1.1",
    description="Create .desktop shortcuts for any URL",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify that the long description is in Markdown
    author="Himanshu Kumar Jha",
    author_email="himanshukrjha004@gmail.com",
    url="https://github.com/himanshu-kr-jha",
    packages=find_packages(),
    install_requires=[
        # No additional dependencies needed
    ],
    entry_points={
        'console_scripts': [
            'desktop-icon-maker=desktop_icon_maker.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
