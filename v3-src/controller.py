from database import inject_dataset, query_all_data, query_table
from tkinter import filedialog
import tkinter as tk
import sqlite3

def handle_file_select(text_widget):
    filepath = filedialog.askopenfilename(
        title="select dataset file",
        filetypes=[("CSV files", "*.csv"), ("text files", "*.txt"), ("all files", "*.*")]
    )
    if filepath:
        db_path = 'database-content.db'
        conn = sqlite3.connect(db_path)
        success = inject_dataset(conn, filepath)
        conn.close()
        output_text = "[controller-get_file] dataset injected from file!" if success else "[ask] failed to inject dataset."
    else:
        output_text = "[controller-get_file] no file selected."
    update_text_widget(text_widget, output_text)

def handle_query(text_widget):
    # query and display data
    data = query_all_data()
    update_text_widget(text_widget, data)

def handle_table_query(text_widget, table_listbox):
    selection = table_listbox.curselection()
    if selection:
        table_name = table_listbox.get(selection[0])
        data = query_table(table_name)
        update_text_widget(text_widget, data)
    else:
        update_text_widget(text_widget, "[controller-update] no table selected.")

def update_text_widget(text_widget, text):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, text)
    text_widget.config(state=tk.DISABLED)