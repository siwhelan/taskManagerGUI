import tkinter
import tkinter.messagebox
import customtkinter
import hashlib
import pymongo
from Main_Window import App


# Function to check if the username and password are correct


def check_login(username, entered_password):
    # Connect to the MongoDB server and the "login_info" collection
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["task_manager"]
    collection = db["login_info"]

    # Find the document with the matching username
    document = collection.find_one({"username": username})

    if document:
        # Check if the entered password matches the stored password hash
        return entered_password == document["password"]
    else:
        return False


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
w = 400  # width for the CTk root
h = 400  # height for the CTk root

# get screen width and height
ws = app.winfo_screenwidth()  # width of the screen
hs = app.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the CTk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
# and where it is placed
app.geometry("%dx%d+%d+%d" % (w, h, x, y))
app.title("Login Page")

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)


def button_function():
    # Get the values entered in the entry widgets
    username = entry_1.get()
    entered_password = entry_2.get()

    # Destroy the current window
    app.destroy()

    # Create a new identical window
    app2 = customtkinter.CTk()
    app2.geometry("%dx%d+%d+%d" % (w, h, x, y))
    app2.title("Login Page")

    # Hash the entered password using SHA-256
    hashed_password = hashlib.sha256(
        entered_password.encode("utf-8")
    ).hexdigest()

    # Check if the username and password are correct
    if check_login(username, hashed_password):
        button2 = customtkinter.CTkButton(
            master=app2,
            text="Authorised! Click to continue",
            command=lambda: run_third_window(app2),
        )
        app2.bind("<Return>", lambda event: button2.invoke())
        button2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        app2.mainloop()
    else:
        # Create a button with the text "Incorrect info"
        button2 = customtkinter.CTkButton(
            master=app2, text="Access Denied", command=app2.destroy
        )
        app2.bind("<Return>", lambda event: button2.invoke())

        button2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        app2.mainloop()


def run_third_window(app2):
    # Destroy the current window
    app2.destroy()

    # Create a new window
    app3 = App()

    app3.mainloop()


text_var = tkinter.StringVar(value="Welcome!")
label_1 = customtkinter.CTkLabel(
    master=frame_1, textvariable=text_var, justify=tkinter.LEFT
)
label_1.pack(pady=10, padx=10)

entry_1 = customtkinter.CTkEntry(
    master=frame_1, placeholder_text="Username", justify=tkinter.CENTER
)
entry_1.pack(pady=10, padx=10)

entry_2 = customtkinter.CTkEntry(
    master=frame_1,
    placeholder_text="Password",
    justify=tkinter.CENTER,
    show="*",
)
entry_2.pack(pady=10, padx=10)

button = customtkinter.CTkButton(
    master=app, text="Log In", command=button_function
)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
app.bind("<Return>", lambda event: button.invoke())

app.mainloop()
# Create admin account
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["task_manager"]
collection = db["login_info"]

# Hash the password using SHA-256
hashed_password = hashlib.sha256("adm1n".encode("utf-8")).hexdigest()

# Create the admin account document
admin_account = {"username": "admin", "password": hashed_password}

# Insert the admin account document into the collection
collection.insert_one(admin_account)
