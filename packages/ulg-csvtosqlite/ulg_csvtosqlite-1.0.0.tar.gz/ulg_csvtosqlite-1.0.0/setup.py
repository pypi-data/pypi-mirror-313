from setuptools import setup, find_packages

setup(
    name="ulg-csvtosqlite",  # New name
    version="1.0.0",
    description="A library for importing CSV files into SQLite databases with optional GUI support",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="MMPDF Collection",
    author_email="mmpdfcollection@gmail.com",
    url="https://github.com/mmpdfcollection/ulg-csv-to-sqlite",  # Update this URL as well
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[  # Base dependencies
        # List your core dependencies here
    ],
    extras_require={  # Optional dependencies
        'gui': ['tkinter'],  # Optional GUI support
    },
    entry_points={
        "console_scripts": [
            "csv-to-sqlite-gui = csv_to_sqlite.gui:run_gui",  # GUI command
        ],
    },
)

