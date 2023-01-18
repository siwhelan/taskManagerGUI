import tkinter
import hashlib
import pymongo
import customtkinter

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("dark-blue")
# Create a custom ErrorFrame class that inherits from CTkFrame


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


class App4(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        w = 400  # width
        h = 400  # height

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the CTk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.title("Add User")

        self.frame_3 = customtkinter.CTkFrame(master=self)
        self.frame_3.pack(pady=20, padx=60, fill="both", expand=True)

        self.label_3 = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Please input new Username and Password",
            justify=tkinter.LEFT,
        )
        self.label_3.pack(pady=10, padx=10)

        self.entry_3 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Username",
            justify=tkinter.CENTER,
        )
        self.entry_3.pack(pady=10, padx=10)

        self.entry_4 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Password",
            justify=tkinter.CENTER,
            show="*",
        )
        self.entry_4.pack(pady=10, padx=10)

        self.entry_5 = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Confirm Password",
            justify=tkinter.CENTER,
            show="*",
        )

        self.entry_5.pack(pady=10, padx=10)

        self.button = customtkinter.CTkButton(
            self, text="Add User", command=self.button_one_function
        )

        self.button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        self.bind("<Return>", lambda event: self.button.invoke())

        self.mainloop()

    def button_one_function(self):

        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db_name = "task_manager"
        # check db doesn't already exist
        if db_name not in client.list_database_names():
            client.create_database(db_name)

        db = client[db_name]
        collection = db["login_info"]

        # Get the values entered in the entry widgets
        username = self.entry_3.get()
        password = self.entry_4.get()
        pass_check = self.entry_5.get()

        # check if the username already exists
        if collection.find_one({"username": username}):
            # Create an instance of the Error

            self.error_frame = ErrorFrame(
                self,
                message="This username is already taken, please choose a different one.",
            )
            return

        # Check if the username and password are empty strings
        elif (username == "") or (password == "") or (password != pass_check):
            # Create a new window with a button saying
            # "incorrect info, please try again"
            self.error_frame = ErrorFrame(
                self, message="Incorrect info, please try again."
            )
            return
        else:
            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Insert the username and hashed password
            # into the MongoDB collection
            collection.insert_one(
                {"username": username, "password": hashed_password}
            )
            # Create an instance of the SuccessFrame
            self.success_frame = SuccessFrame(
                self, message="Successfully added new user!"
            )
        # remove the error frame if the input is correct
        if hasattr(self, "error_frame"):
            self.error_frame.destroy()


if __name__ == "__main__":
    App4()
