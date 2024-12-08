from tkinter import Tk, Label, Button, Listbox, filedialog, Entry, StringVar, messagebox, END
from .core import import_csv_to_db

def run_gui():
    """Launch the GUI for CSV to SQLite conversion."""
    def add_csv_files():
        files = filedialog.askopenfilenames(
            title="Select CSV Files",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        for file in files:
            csv_list.insert(END, file)

    def remove_csv_files():
        selected_files = csv_list.curselection()
        for index in reversed(selected_files):
            csv_list.delete(index)

    def choose_output_folder():
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            db_path = filedialog.asksaveasfilename(
                title="Save SQLite Database As",
                initialdir=folder,
                defaultextension=".db",
                filetypes=[("SQLite Database", "*.db")]
            )
            db_name.set(db_path)

    def import_csv_files_gui():
        csv_files = list(csv_list.get(0, END))
        db_file = db_name.get()

        try:
            import_csv_to_db(csv_files, db_file)
            messagebox.showinfo("Success", "CSV files have been successfully imported.")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the main GUI window
    root = Tk()
    root.title("ULG CSV to SQLite Converter")
    root.geometry("500x600")

    Label(root, text="Selected CSV Files:").pack(pady=5)
    csv_list = Listbox(root, selectmode="multiple", width=60, height=10)
    csv_list.pack(pady=5)

    Button(root, text="Add CSV Files", command=add_csv_files).pack(pady=5)
    Button(root, text="Remove Selected Files", command=remove_csv_files).pack(pady=5)

    Label(root, text="Output SQLite Database:").pack(pady=5)
    db_name = StringVar()
    Entry(root, textvariable=db_name, width=50).pack(pady=5)
    Button(root, text="Choose Output Folder", command=choose_output_folder).pack(pady=5)

    Button(root, text="Create SQLite(.db)", command=import_csv_files_gui, bg="green", fg="white").pack(pady=20)

    root.mainloop()
