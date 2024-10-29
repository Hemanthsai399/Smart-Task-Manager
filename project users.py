import tkinter as tk
from tkinter import messagebox
import json
import os
import hashlib
from datetime import datetime

# Path to store user data
USER_DATA_DIR = "user_data"
os.makedirs(USER_DATA_DIR, exist_ok=True)

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Save user data in JSON format
def save_user_data(username, data):
    filepath = os.path.join(USER_DATA_DIR, f"{username}.json")
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

# Load user data from JSON format
def load_user_data(username):
    filepath = os.path.join(USER_DATA_DIR, f"{username}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    return None

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.username = None
        self.user_data = None
        self.setup_login_screen()

    # Clear current screen widgets
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Login Screen
    def setup_login_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Task Manager", font=("Arial", 24)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        self.login_username = tk.Entry(self.root)
        self.login_username.pack()
        tk.Label(self.root, text="Password").pack()
        self.login_password = tk.Entry(self.root, show="*")
        self.login_password.pack()
        
        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Sign Up", command=self.setup_signup_screen).pack()
    
    # Sign Up Screen
    def setup_signup_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Sign Up", font=("Arial", 24)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        self.signup_username = tk.Entry(self.root)
        self.signup_username.pack()
        tk.Label(self.root, text="Password").pack()
        self.signup_password = tk.Entry(self.root, show="*")
        self.signup_password.pack()
        
        tk.Label(self.root, text="Name").pack()
        self.signup_name = tk.Entry(self.root)
        self.signup_name.pack()
        
        tk.Label(self.root, text="Address").pack()
        self.signup_address = tk.Entry(self.root)
        self.signup_address.pack()
        
        tk.Label(self.root, text="Age").pack()
        self.signup_age = tk.Entry(self.root)
        self.signup_age.pack()
        
        tk.Button(self.root, text="Create Account", command=self.signup).pack(pady=5)
        tk.Button(self.root, text="Back to Login", command=self.setup_login_screen).pack()
    
    # Sign-up Process
    def signup(self):
        username = self.signup_username.get()
        password = self.signup_password.get()
        name = self.signup_name.get()
        address = self.signup_address.get()
        age = self.signup_age.get()
        
        if load_user_data(username):
            messagebox.showerror("Error", "Username already exists!")
            return
        
        # Save hashed password and user data
        hashed_password = hash_password(password)
        self.user_data = {
            "password": hashed_password,
            "name": name,
            "address": address,
            "age": age,
            "tasks": []
        }
        
        save_user_data(username, self.user_data)
        messagebox.showinfo("Success", "Account created successfully!")
        self.setup_login_screen()

    # Login Process
    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        
        self.user_data = load_user_data(username)
        if self.user_data and self.user_data["password"] == hash_password(password):
            self.username = username
            self.setup_main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    # Main Screen after Login
    def setup_main_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text=f"Welcome, {self.user_data['name']}", font=("Arial", 20)).pack(pady=10)
        
        tk.Button(self.root, text="View Profile", command=self.view_profile).pack(pady=5)
        tk.Button(self.root, text="Add Task", command=self.add_task_screen).pack(pady=5)
        tk.Button(self.root, text="View Tasks", command=self.view_tasks).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.setup_login_screen).pack(pady=5)
    
    # View Profile Screen
    def view_profile(self):
        profile = f"Name: {self.user_data['name']}\nAddress: {self.user_data['address']}\nAge: {self.user_data['age']}"
        messagebox.showinfo("Profile Information", profile)

    # Add Task Screen
    def add_task_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Add New Task", font=("Arial", 18)).pack(pady=10)
        
        tk.Label(self.root, text="Task Title").pack()
        self.task_title_entry = tk.Entry(self.root)
        self.task_title_entry.pack()
        
        tk.Label(self.root, text="Task Target").pack()
        self.task_target_entry = tk.Entry(self.root)
        self.task_target_entry.pack()
        
        tk.Button(self.root, text="Add Task", command=self.add_task).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.setup_main_screen).pack()

    # Save Task
    def add_task(self):
        title = self.task_title_entry.get()
        target = self.task_target_entry.get()
        
        new_task = {
            "title": title,
            "target": target,
            "status": "Pending",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.user_data["tasks"].append(new_task)
        save_user_data(self.username, self.user_data)
        messagebox.showinfo("Success", "Task added successfully!")
        self.setup_main_screen()
    
    # View All Tasks
    def view_tasks(self):
        tasks = self.user_data.get("tasks", [])
        if not tasks:
            messagebox.showinfo("Tasks", "No tasks added yet.")
        else:
            tasks_str = ""
            self.task_buttons = []  # Store buttons for marking status
            for idx, task in enumerate(tasks, 1):
                tasks_str += f"{idx}. {task['title']} - {task['status']} (Added on {task['timestamp']})\n"
                button = tk.Button(self.root, text=f"Toggle Status for Task {idx}", command=lambda i=idx-1: self.toggle_task_status(i))
                self.task_buttons.append(button)
                button.pack(pady=2)
            messagebox.showinfo("All Tasks", tasks_str)
            for button in self.task_buttons:
                button.pack()

    # Toggle Task Status
    def toggle_task_status(self, task_index):
        task = self.user_data["tasks"][task_index]
        if task["status"] == "Pending":
            task["status"] = "Completed"
        else:
            task["status"] = "Pending"
        save_user_data(self.username, self.user_data)
        messagebox.showinfo("Success", f"Task '{task['title']}' marked as {task['status']}.")
         # Refresh task list to show updated statuses


# Start the application
root = tk.Tk()
app = TaskManagerApp(root)
root.mainloop()

