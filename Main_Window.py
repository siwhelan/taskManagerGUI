import customtkinter
import tkinter
from tkinter import *
import pymongo
from datetime import datetime
from pymongo import MongoClient


class SuccessFrame(customtkinter.CTkFrame):
    def __init__(self, master=None, message=""):
        # Call the parent class constructor
        super().__init__(master=master, height=100)
        # Set the appearance mode to dark
        customtkinter.set_appearance_mode("dark")
        # Pack the frame
        self.pack(fill="both", expand=True)
        # Create a label to display the success message
        self.label = customtkinter.CTkLabel(
            self, text=message, justify=tkinter.CENTER
        )
        self.label.pack(pady=10, padx=10)
        # Create a button to close the success frame
        self.button = customtkinter.CTkButton(
            self, text="Ok", command=self.master.destroy
        )
        self.button.pack()


class ErrorFrame(customtkinter.CTkFrame):
    def __init__(self, master=None, message=""):
        # Call the parent class constructor
        super().__init__(master=master, height=100)
        # Set the appearance mode to dark
        customtkinter.set_appearance_mode("dark")
        # Pack the frame
        self.pack(fill="both", expand=True)
        # Create a label to display the error message
        self.label = customtkinter.CTkLabel(
            self, text=message, justify=tkinter.CENTER
        )
        self.label.pack(pady=10, padx=10)
        # Create a button to close the error frame
        self.button = customtkinter.CTkButton(
            self, text="Ok", command=self.destroy
        )
        self.button.pack()


# Mode
customtkinter.set_appearance_mode("dark")
# Theme
customtkinter.set_default_color_theme("dark-blue")


class Add_task(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        w = 500  # width
        h = 500  # height

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the CTk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.title("Add Task")

        self.frame_3 = customtkinter.CTkFrame(master=self)
        self.frame_3.pack(pady=20, padx=60, fill="both", expand=True)

        self.label_3 = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Please input new Task Info",
            justify=tkinter.LEFT,
        )
        self.label_3.pack(pady=10, padx=10)

        self.entry_3 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="User assigned to task",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_3.pack(pady=10, padx=10)

        self.entry_4 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Task Title",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_4.pack(pady=10, padx=10)

        self.entry_5 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Task Description",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_5.pack(pady=10, padx=10)

        self.entry_6 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Due - e.g. 21 Feb 2023",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_6.pack(pady=10, padx=10)

        self.button = customtkinter.CTkButton(
            self, text="Add Task", command=self.add_task_func
        )
        self.button.place(relx=0.5, rely=0.68, anchor=tkinter.CENTER)
        self.bind("<Return>", lambda event: self.button.invoke())

        self.mainloop()

    def add_task_func(self):

        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db_name = "task_manager"
        # check db doesn't already exist
        if db_name not in client.list_database_names():
            client.create_database(db_name)

        db = client[db_name]
        collection = db["tasks"]
        users = db["login_info"]

        # Get the values entered in the entry widgets
        username = self.entry_3.get()
        task_title = self.entry_4.get()
        task_description = self.entry_5.get()
        due_date = self.entry_6.get()
        due_date = datetime.strptime(due_date, "%d %b %Y")
        date_assigned = datetime.now().strftime("%d %b %Y")
        completed = "No"

        # check if the username exists
        if not users.find_one({"username": username}):
            # If not, create an instance of the Error
            self.error_frame = ErrorFrame(
                self, message="User does not exist, please try again."
            )
            return
        # If the user does exist
        else:
            # Check how many tasks there are already for task_id
            tasks_count = collection.count_documents({})
            new_task = [
                {
                    "task_id": tasks_count + 1,
                    "assigned_to": username,
                    "task_title": task_title,
                    "task_description": task_description,
                    "due_date": due_date,
                    "date_assigned": date_assigned,
                    "completed": completed,
                }
            ]

            collection.insert_many(new_task)

            # Create an instance of the SuccessFrame
            self.success_frame = SuccessFrame(
                self, message="Successfully added new task!"
            )


class Edit_task(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        w = 500  # width
        h = 500  # height

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the CTk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.title("Edit Task")

        self.frame_3 = customtkinter.CTkFrame(master=self)
        self.frame_3.pack(pady=20, padx=60, fill="both", expand=True)

        self.label_3 = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Please input updated Task Info",
            justify=tkinter.LEFT,
        )
        self.label_3.pack(pady=10, padx=10)

        self.entry_2 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Relevant Task ID",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_2.pack(pady=10, padx=10)

        self.entry_3 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="User assigned to task",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_3.pack(pady=10, padx=10)

        self.entry_4 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Task Title",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_4.pack(pady=10, padx=10)

        self.entry_5 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Task Description",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_5.pack(pady=10, padx=10)

        self.entry_6 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Due - e.g. 21 Feb 2023",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_6.pack(pady=10, padx=10)

        self.checkbox_2 = customtkinter.CTkCheckBox(
            master=self.frame_3, text="Task Completed"
        )
        self.checkbox_2.pack(pady=10, padx=20)

        self.button = customtkinter.CTkButton(
            self, text="Edit Task", command=self.update_task
        )
        self.button.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)
        self.bind("<Return>", lambda event: self.button.invoke())

        self.mainloop()

    def update_task(self):
        # Connect to the MongoDB server
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db_name = "task_manager"

        db = client[db_name]
        collection = db["tasks"]
        users = db["login_info"]

        # Get the values from the entry widgets
        task_id = int(self.entry_2.get())
        assigned_to = self.entry_3.get()
        task_title = self.entry_4.get()
        task_description = self.entry_5.get()
        due_date = self.entry_6.get()
        due_date = datetime.strptime(due_date, "%d %b %Y")
        completed = self.checkbox_2.get()

        # print(type(due_date))

        if collection.find_one({"task_id": task_id}):

            # Check to skip blank entries and leave them as they are
            # Update the task info with inputted data
            if assigned_to != "":
                # check if the new assigned_to username exists
                if users.find_one({"username": assigned_to}):
                    collection.update_one(
                        {"task_id": task_id},
                        {"$set": {"assigned_to": assigned_to}},
                    )
                else:
                    self.error_frame = ErrorFrame(
                        self, message="User does not exist"
                    )
                    return

            if task_title != "":
                collection.update_one(
                    {"task_id": task_id}, {"$set": {"task_title": task_title}}
                )

            if task_description != "":
                collection.update_one(
                    {"task_id": task_id},
                    {"$set": {"task_description": task_description}},
                )

            if due_date != "":
                collection.update_one(
                    {"task_id": task_id}, {"$set": {"due_date": due_date}}
                )

            if completed == 1:
                collection.update_one(
                    {"task_id": task_id}, {"$set": {"completed": "Yes"}}
                )

            # Create an instance of the SuccessFrame
            self.success_frame = SuccessFrame(self, message="Task edited")

        else:

            self.error_frame = ErrorFrame(
                self, message="Task ID does not exist"
            )
            return


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        w = 900  # width
        h = 400  # height

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.title("swhelan.dev - Task Manager")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="swhelan.dev",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Button 1
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        # Button 2
        optionmenu_var = customtkinter.StringVar(value="Task Menu")
        self.sidebar_button_2 = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            variable=optionmenu_var,
            anchor="center",
            values=["View All", "Add Task", "Edit Task", "Delete Task"],
            command=self.task_menu,
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # Button 3
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.generate_reports
        )
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # Label
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Theme:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(10, 10)
        )
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter Data"
        )
        self.entry.grid(
            row=3,
            column=1,
            columnspan=2,
            padx=(20, 0),
            pady=(20, 20),
            sticky="nsew",
        )

        # Clears search term from entry box and resets it to original text
        def clear_entry():
            self.entry.delete(0, "end")

        self.main_button_1 = customtkinter.CTkButton(
            master=self,
            text="Search",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.search,
        )
        self.main_button_1.grid(
            row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=600)
        self.textbox.grid(
            row=0,
            column=1,
            padx=(20, 20),
            pady=(20, 0),
            sticky="nsew",
            columnspan=3,
        )

        # set default values
        self.sidebar_button_1.configure(text="Add User")
        # self.sidebar_button_2.configure(text="Add/View Tasks")
        self.sidebar_button_3.configure(text="Generate Reports")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0", "Task Manager\n\n")

        # Add an instance variable to store the Add_Task class
        self.add_task = None

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):

        # Import the App4 class from Add_User_UI.py
        from Add_User_UI import App4

        # Create an instance of the App4 class
        app4 = App4()
        app4.mainloop()

    def search(self):

        # Connect to the MongoDB database
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        task_manager = client["task_manager"]

        # Retrieve the 'tasks' collection
        tasks = task_manager["tasks"]

        # Initialize an empty dictionary to store the search query
        search_query = {}

        # Check if the input in the entry field is a digit
        if self.entry.get().isdigit():
            # If it is a digit, add the task_id field to the search query
            search_query["task_id"] = int(self.entry.get())

        else:
            # If the input is not an int, string, check the db usernames for a match
            search_query["assigned_to"] = self.entry.get()

        # Perform the search using the search query
        task_count = tasks.count_documents(search_query)

        # Check if any tasks are found
        if task_count > 0:
            task_cursor = tasks.find(search_query)
            self.textbox.delete(1.0, END)
            for task in task_cursor:

                # Iterate through the cursor and display the details of each task
                self.textbox.insert(
                    "end", "\nTask ID: " + str(task["task_id"]) + "\n"
                )
                self.textbox.insert(
                    "end", "\nTask Title: " + task["task_title"] + "\n"
                )
                self.textbox.insert(
                    "end", "Assigned To: " + task["assigned_to"] + "\n"
                )
                self.textbox.insert(
                    "end",
                    "Task Description: " + task["task_description"] + "\n",
                )
                self.textbox.insert(
                    "end", "Due Date: " + task["due_date"] + "\n"
                )
                self.textbox.insert(
                    "end", "Date Assigned: " + task["date_assigned"] + "\n"
                )
                self.textbox.insert(
                    "end", "Completed: " + task["completed"] + "\n"
                )
        else:
            self.textbox.delete(1.0, END)
            self.textbox.insert("end", "\nNo Tasks Found\n")

    def generate_reports(self):

        self.textbox.delete(1.0, END)

        # Connect to the MongoDB server
        client = MongoClient()

        # Get the 'login_info' collection from the 'task_manager' database
        login_info_collection = client["task_manager"]["login_info"]
        # Get the count of unique usernames in the collection
        num_users = len(
            set(
                [
                    login_info["username"]
                    for login_info in login_info_collection.find()
                ]
            )
        )
        # Get the 'tasks' collection from the 'task_manager' database
        tasks_collection = client["task_manager"]["tasks"]

        # Get the count of tasks in the collection
        num_tasks = tasks_collection.count_documents({})

        # Count the number of completed and not completed tasks
        completed_count = tasks_collection.count_documents(
            {"completed": "Yes"}
        )
        not_completed_count = tasks_collection.count_documents(
            {"completed": "No"}
        )

        # Find the tasks that are overdue and not completed
        today = datetime.now().strftime("%d %b %Y")
        overdue_count = tasks_collection.count_documents(
            {"due_date": {"$lt": today}, "completed": "No"}
        )

        # Calculate the percentage of tasks that are incomplete and overdue
        incomplete = round((not_completed_count / num_tasks) * 100, 2)
        overdue = round((overdue_count / num_tasks) * 100, 2)

        # Output the report to the textbox widget
        self.textbox.insert(END, f"Total number of users: {num_users}\n")
        self.textbox.insert(END, f"Total number of tasks: {num_tasks}\n")
        self.textbox.insert(END, f"Total completed tasks: {completed_count}\n")
        self.textbox.insert(
            END, f"Total uncompleted tasks: {not_completed_count}\n"
        )
        self.textbox.insert(
            END, f"Percentage of tasks incomplete: {incomplete}%\n"
        )
        self.textbox.insert(END, f"Percentage of tasks overdue: {overdue}%\n")

    def view_all(self):

        self.textbox.delete(1.0, END)

        # Connect to the MongoDB database
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        task_manager = client["task_manager"]

        # Retrieve the 'tasks' collection
        tasks = task_manager["tasks"]

        # Find all tasks in the collection
        all_tasks = tasks.find()

        for task in all_tasks:

            self.textbox.insert(
                "end", "\nTask ID: " + str(task["task_id"]) + "\n"
            )
            self.textbox.insert(
                "end", "\nTask Title: " + task["task_title"] + "\n"
            )
            self.textbox.insert(
                "end", "Assigned To: " + task["assigned_to"] + "\n"
            )
            self.textbox.insert(
                "end",
                "Task Description: " + task["task_description"] + "\n",
            )
            self.textbox.insert("end", "Due Date: " +
                                str(task["due_date"]) + "\n")
            self.textbox.insert(
                "end", "Date Assigned: " + task["date_assigned"] + "\n"
            )
            self.textbox.insert(
                "end", "Completed: " + task["completed"] + "\n"
            )

    def task_menu(self, value):
        self.command(value)

        self.textbox.delete(1.0, END)

        # Connect to the MongoDB database
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        task_manager = client["task_manager"]

        # Retrieve the 'tasks' collection
        tasks = task_manager["tasks"]

        # Find all tasks in the collection
        all_tasks = tasks.find()

        menu_choice = self.sidebar_button_2.get()

        if menu_choice == "View All":

            for task in all_tasks:

                self.textbox.insert(
                    "end", "\nTask ID: " + str(task["task_id"]) + "\n"
                )

                self.textbox.insert(
                    "end", "\nTask Title: " + task["task_title"] + "\n"
                )
                self.textbox.insert(
                    "end", "Assigned To: " + task["assigned_to"] + "\n"
                )
                self.textbox.insert(
                    "end",
                    "Task Description: " + task["task_description"] + "\n",
                )
                self.textbox.insert(
                    "end", "Due Date: " + str(task["due_date"]) + "\n"
                )
                self.textbox.insert(
                    "end", "Date Assigned: " + task["date_assigned"] + "\n"
                )
                self.textbox.insert(
                    "end", "Completed: " + task["completed"] + "\n"
                )

        elif menu_choice == "Add Task":

            Add_task()

        elif menu_choice == "Edit Task":

            self.view_all()
            Edit_task()

        elif menu_choice == "Delete Task":

            dialog = customtkinter.CTkInputDialog(
                text="Please enter the Task ID you'd like to delete",
                title="Delete Task",
            )
            task_id = int(dialog.get_input())

            if task_id:
                # Connect to the MongoDB server
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db_name = "task_manager"
                db = client[db_name]
                collection = db["tasks"]

                # Find the task with the matching task_id
                task = collection.find_one({"task_id": task_id})

                if task:
                    # Delete the task
                    collection.delete_one({"task_id": task_id})
                    self.textbox.insert("0.0", "Task Deleted\n\n")
                else:
                    self.textbox.insert("0.0", "Task ID does not exist\n\n")
            else:
                self.textbox.insert("0.0", "Task ID does not exist\n\n")


if __name__ == "__main__":
    app = App()
    app.mainloop()
