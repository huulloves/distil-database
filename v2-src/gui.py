import tkinter as tk
from controller import handle_file_select, handle_query

def build_gui():
    root = tk.Tk()
    root.title("distill-database-prototype")
    root.geometry("800x600")

    text_widget = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
    text_widget.pack(fill=tk.BOTH, expand=True)

    btn_frame = tk.Frame(root)
    btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

    select_btn = tk.Button(btn_frame, text="Select and Inject Dataset", command=lambda: handle_file_select(text_widget))
    select_btn.pack(side=tk.LEFT, padx=5, pady=5)

    query_btn = tk.Button(btn_frame, text="Query Data", command=lambda: handle_query(text_widget))
    query_btn.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()