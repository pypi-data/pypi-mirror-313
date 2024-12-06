from setuptools import setup, find_packages

setup(
    name="desktop-icon-maker",
    version="0.1.0",
    description="Create .desktop shortcuts for any URL",
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
