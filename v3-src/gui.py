import tkinter as tk
from controller import handle_file_select, handle_query, handle_table_query
import sqlite3

DB_PATH = 'database-content.db'

def get_table_names():
    """fetch all table names from the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        return []

def build_gui():
    root = tk.Tk()
    root.title("distill-database-prototype")
    root.geometry("800x600")

    text_widget = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
    text_widget.pack(fill=tk.BOTH, expand=True)

    # table selection frame
    table_frame = tk.Frame(root)
    table_frame.pack(side=tk.TOP, fill=tk.X)

    table_label = tk.Label(table_frame, text="select table:")
    table_label.pack(side=tk.LEFT, padx=5)

    table_listbox = tk.Listbox(table_frame, height=4, exportselection=False)
    table_listbox.pack(side=tk.LEFT, padx=5)
    # for general select * statement
    table_listbox.insert(tk.END, "all")
    # populate listbox with table names
    for table in get_table_names():
        table_listbox.insert(tk.END, table)

    def refresh_tables():
        table_listbox.delete(0, tk.END)
        table_listbox.insert(tk.END, "all")  # always add "all" first
        for table in get_table_names():
            table_listbox.insert(tk.END, table)

    btn_frame = tk.Frame(root)
    btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

    select_btn = tk.Button(btn_frame, text="select and inject Dataset", command=lambda: [handle_file_select(text_widget), refresh_tables()])
    select_btn.pack(side=tk.LEFT, padx=5, pady=5)

    query_btn = tk.Button(btn_frame, text="query data", command=lambda: handle_query(text_widget))
    query_btn.pack(side=tk.LEFT, padx=5, pady=5)

    query_table_btn = tk.Button(btn_frame, text="query selected table", command=lambda: handle_table_query(text_widget, table_listbox))
    query_table_btn.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()