import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from data_module import *
from ai_module import *

current_user_id = None

# ---------------- GUI ---------------- #

def login_screen():
    def login():
        global current_user_id
        username = username_entry.get()
        password = password_entry.get()
        user_id = login_user(username, password)
        if user_id:
            current_user_id = user_id
            root.destroy()
            task_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def register():
        username = username_entry.get()
        password = password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "User registered. You can log in now.")
        else:
            messagebox.showerror("Error", "Username already exists.")

    root = tk.Tk()
    root.title("AI Task Manager - Login")

    tk.Label(root, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(root)
    username_entry.grid(row=0, column=1)

    tk.Label(root, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(root, show='*')
    password_entry.grid(row=1, column=1)

    tk.Button(root, text="Login", command=login).grid(row=2, column=0)
    tk.Button(root, text="Register", command=register).grid(row=2, column=1)

    root.mainloop()

def task_dashboard():
    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        tasks = get_tasks(current_user_id)
        for task in tasks:
            status = suggest_status(task[4]) if task[6] == "To Do" else task[6]
            tree.insert("", "end", iid=task[0], values=(task[2], task[3], task[4], task[5], status))

    def add_task():
        title = simpledialog.askstring("Add Task", "Title:")
        if not title: return
        description = simpledialog.askstring("Description", "Enter description:")
        deadline = simpledialog.askstring("Deadline (YYYY-MM-DD):", "Optional")
        priority = simpledialog.askstring("Priority (Low/Medium/High):", "Optional")
        create_task(current_user_id, title, description or "", deadline, priority or "Medium")
        refresh()

    def add_nlp_task():
        text = simpledialog.askstring("NLP Task", "Describe your task (e.g. 'Submit report by Friday'):")
        if not text: return
        title, description, deadline = parse_task_from_text(text)
        priority = suggest_priority(title, description)
        create_task(current_user_id, title, description, deadline, priority)
        refresh()

    def update_priority():
        task_id = tree.focus()
        if not task_id: return
        item = tree.item(task_id)
        suggested = suggest_priority(item['values'][0], item['values'][1])
        update_task(task_id, priority=suggested)
        messagebox.showinfo("AI Suggestion", f"Suggested Priority: {suggested}")
        refresh()

    def mark_done():
        task_id = tree.focus()
        if not task_id: return
        update_task(task_id, status="Done")
        refresh()

    window = tk.Tk()
    window.title("AI Task Manager")

    tree = ttk.Treeview(window, columns=("Title", "Description", "Deadline", "Priority", "Status"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, minwidth=0, width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add Task", command=add_task).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Add via AI (NLP)", command=add_nlp_task).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="AI Suggest Priority", command=update_priority).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Mark Done", command=mark_done).pack(side=tk.LEFT, padx=5)

    refresh()
    window.mainloop()

# ---------------- Entry Point ---------------- #

if __name__ == "__main__":
    init_db()
    login_screen()
