CSV to SQLite
CSV to SQLite is a Python library for importing CSV files into SQLite databases with optional GUI support. It allows users to quickly convert CSV files into SQLite database tables with a simple graphical interface.

Features
Import multiple CSV files into a single SQLite database.
Automatically create SQLite tables based on CSV headers.
Clean and validate column names for compatibility.
Optional GUI for easy file selection and output configuration.
Installation
You can install csv-to-sqlite using pip:

pip install csv-to-sqlite
Alternatively, you can clone the repository and install it manually:

git clone https://github.com/mmpdfcollection/csv-to-sqlite.git
cd csv-to-sqlite
python setup.py install
Usage
Command Line Interface (CLI)
Run the following command to launch the GUI for the library:

csv-to-sqlite-gui
Example Usage in Python
If you want to use this library programmatically, here's an example:

from csv_to_sqlite import csv_to_db

# Example of converting a single CSV file to an SQLite database
csv_to_db.import_csv_files(["example.csv"], "output.db")
Requirements
Python 3.6 or newer
tkinter (included with most Python distributions)
How It Works
Select CSV Files: You can select multiple CSV files that you want to convert.
Choose Output Folder: Specify where the SQLite database file should be saved.
Click Import: The GUI or library handles creating tables and inserting data automatically.
Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit them (git commit -m "Add new feature").
Push to your branch (git push origin feature-branch).
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Author
MMPDF Collection
mmpdfcollection@gmail.com
Acknowledgments
Special thanks to all contributors and Python enthusiasts who made this project possible.

