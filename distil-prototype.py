"""aimee distill functionality viewer with SQLite database integration"""
import tkinter as tk
import sqlite3 as sql3

def connect_to_db():
    try:
        conn = sql3.connect('database-content.db')
        cursor = conn.cursor()
         # ensure the table exists using database-content.db
        cursor.execute('''CREATE TABLE IF NOT EXISTS dataset
                          (setID INTEGER PRIMARY KEY, content TEXT)''')
        return conn, cursor
    except sql3.Error as e:
        print(f"[database] database error: {e}")
        return None, None
    except Exception as e:
        print(f"[database] unexpected error: {e}")
        return None, None

def distill_event(canvas, canvas_width, canvas_height):
    conn, cursor = connect_to_db()
    output_text = "[distill] content will appear here..."
    if conn and cursor:
        try:
            user_data = cursor.execute("SELECT content FROM dataset")
            content = [row[0] for row in user_data]
            if content:
                output_text = "\n".join(content)
            print("[distill] content retrieved from database...")
            print("[distill] content:")
            for info in content:
                print(info)
        except sql3.Error as e:
            print(f"[distill] error retrieving from database: {e}")
        finally:
            conn.close()
    # update canvas display
    canvas.delete("all")
    canvas.create_text(canvas_width // 2, canvas_height // 2, text=output_text, fill='black', font=('Arial', 12))

def main():
    root = tk.Tk()
    root.title("distill-database-prototype")
    root.geometry("800x600")

    canvas_width = 600
    canvas_height = 500
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack()

    # initial output text
    output_text = "[main] distilled content will appear here..."
    canvas.create_text(canvas_width // 2, canvas_height // 2, text=output_text, fill='black', font=('Arial', 12))

    # button frame
    frame = tk.Frame(root)
    frame.pack(side=tk.BOTTOM, fill=tk.X)

    distill_btn = tk.Button(frame, text="distill", command=lambda: distill_event(canvas, canvas_width, canvas_height))
    distill_btn.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()

main()