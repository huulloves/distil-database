from inject import ask
from database import query_all_data
from tkinter import filedialog
import tkinter as tk

def handle_file_select(text_widget):
    # Open file dialog to select file
    filepath = filedialog.askopenfilename(
        title="Select dataset file",
        filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
    )
    if filepath:
        success = ask(filepath)
        output_text = "[ask] dataset injected from file!" if success else "[ask] failed to inject dataset."
    else:
        output_text = "[ask] no file selected."
    update_text_widget(text_widget, output_text)

def handle_query(text_widget):
    # Query and display data
    data = query_all_data()
    update_text_widget(text_widget, data)

def update_text_widget(text_widget, text):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, text)
    text_widget.config(state=tk.DISABLED)