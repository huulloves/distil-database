"""Aimee distill functionality viewer with SQLite database integration"""

import tkinter as tk
from tkinter import filedialog
import sqlite3
from inject import ask
from display import display_output

DB_PATH = 'database-content.db'

def connect_to_db():
    """Connect to the SQLite database and ensure the dataset table exists."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS dataset
                          (setID INTEGER PRIMARY KEY, content TEXT)''')
        return conn, cursor
    except sqlite3.Error as e:
        print(f"[database] database error: {e}")
        return None, None

def ask_event(text_widget):
    """Handle file selection and dataset injection."""
    filetypes = [("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
    filename = filedialog.askopenfilename(title="Select dataset file", filetypes=filetypes)
    if filename:
        success = ask(filename)
        output_text = "[ask] Dataset injected from file!" if success else "[ask] Failed to inject dataset."
    else:
        output_text = "[ask] No file selected."
    update_text_widget(text_widget, output_text)

def distill_event(text_widget):
    """Retrieve and display dataset content from the database."""
    conn, cursor = connect_to_db()
    output_text = "[distill] content will appear here..."
    if conn and cursor:
        try:
            cursor.execute("SELECT content FROM dataset")
            content = [row[0] for row in cursor.fetchall()]
            if content:
                output_text = display_output(content)
            print("[distill] content retrieved from database...")
        except sqlite3.Error as e:
            print(f"[distill] error retrieving from database: {e}")
        finally:
            conn.close()
    update_text_widget(text_widget, output_text)

def update_text_widget(text_widget, text):
    """Update the output text widget safely."""
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, text)
    text_widget.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    root.title("distill-database-prototype")
    root.geometry("800x600")

    # Output text widget with scrollbar
    text_frame = tk.Frame(root)
    text_frame.pack(fill=tk.BOTH, expand=True)
    text_widget = tk.Text(text_frame, wrap=tk.WORD, state=tk.DISABLED)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # File picker button
    ask_btn = tk.Button(root, text="Select and Inject Dataset", command=lambda: ask_event(text_widget))
    ask_btn.pack(pady=10)

    # Initial output text
    update_text_widget(text_widget, "[main] distilled content will appear here...")

    # Button frame for distill
    frame = tk.Frame(root)
    frame.pack(side=tk.BOTTOM, fill=tk.X)
    distill_btn = tk.Button(frame, text="distill", command=lambda: distill_event(text_widget))
    distill_btn.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()