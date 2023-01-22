
# Task Manager 📝📤📆



Task Manager - A graphical user interface for a task management program built using the customtkinter library. 

This project was initially a capstone project for a software engineering bootcamp, and was later transformed into a personal project to enhance the usability of the program. The GUI includes features such as a dark mode, UI scaling, and the ability to view, add, edit, and delete tasks. Additionally, the program includes a login system that utilizes a MongoDB database to store and verify user credentials.

The app is composed of three python files: Main_Window.py, Add_task.py, and Login_page.py. Main_Window.py includes the main window of the app, which features a sidebar with buttons for different functions such as viewing all tasks, adding new tasks, editing tasks, and generating reports. Add_task.py features a window for adding new tasks to the app and Login_page.py provides the login page for the app, which utilizes a MongoDB database to check the validity of the entered username and password.

The app also employs pymongo to connect to the MongoDB database storing information on tasks and user login information. Passwords are hashed using SHA-256 for added security. 

Overall, this app provides a user-friendly interface for managing tasks and is an example of a complete software project that includes a GUI, database, and security features.

## Features    

-> Graphical user interface built using the customtkinter library 🖥️

-> Dark mode, UI scaling, and the ability to view, add, edit, and delete tasks 📝

-> Login system that utilizes a MongoDB database to store and check user credentials 🔒

-> Error handling frames for displaying error messages to the user 💬

-> Utilizes pymongo to connect to a MongoDB database that stores information on tasks and user login information 🗄️

-> Passwords are hashed using SHA-256 for added security 🔑

-> An admin account with the username "admin" and password "adm1n" is automatically added to the MongoDB instance upon installation

-> Ability to generate reports on tasks 📈

-> Option menu to switch between different task views and functions 📊

-> Customizable appearance and color theme 🎨

-> Login page with placeholder text and an option to clear the input fields.


## Installation

In order to run this program, the following dependencies and libraries need to be installed:

-> [customtkinter](https://github.com/TomSchimansky/CustomTkinter): This library is used for creating the GUI elements of the program. It can be installed using the command:

    pip install customtkinter

-> [pymongo](https://pymongo.readthedocs.io/en/stable/): This library is used for connecting to and interacting with a MongoDB database. It can be installed using the command 
    
    pip install pymongo

-> [hashlib](https://pypi.org/project/hashlib/): This library is used for hashing passwords for added security. It is included in the python standard library and does not need to be installed separately.

Additionally, a [MongoDB](https://www.mongodb.com/) server should be set up and running on the localhost on port 27017 before running the file. MongoDB is a popular NoSQL, document-oriented, open-source database management system that is known for its scalability, high performance and ease of use. Port 27017 is the default localhost configuration for MongoDB, but it can be configured to listen on a different port or IP address if needed.

You can install MongoDB using the installer [here](https://www.mongodb.com/try/download/community)

A database called "task_manager" should be created and a collection called "login_info" should be created within it to store user login information. You can achieve this with the following steps:


-> Start the MongoDB server by running the `mongod` command in your terminal.

-> Connect to the MongoDB shell by running the `mongosh` command in your terminal.

-> Create the "task_manager" database by running the following command: `use task_manager`

The collection 'login_info' will be created inside this database upon running the file.

## Run Locally

Once all of the dependencies and libraries are installed and the MongoDB server is set up, the program can be run by executing the file "Login_page.py" in the command line.
    
The app comes with a default admin account that you can use to log in and manage tasks. The username is "admin" and the password is "adm1n".

Additionally, you can also create a user account on your local MongoDB instance by running the following code:


    # Connect to the MongoDB server and the "login_info" collection

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["task_manager"]
    collection = db["login_info"]

    # Insert the admin account with hashed password

    collection.insert_one({"username": "admin", "password": hashlib.sha256("adm1n".encode("utf-8")).hexdigest()})


Once you have logged in, you can use the sidebar buttons to view, add, edit, and delete tasks, as well as generate reports. The app also includes a dark mode and UI scaling options that can be accessed from the sidebar.

## More Info

A short series of blogs documenting the build process and explaining some of the features in more detail can be found [here](https://dev.to/siwhelan/task-manager-47jh). 

## Acknowledgements

 - [@TomSchimansky](https://github.com/TomSchimansky) for the awesome work on [customTkinter](https://github.com/TomSchimansky/CustomTkinter), a python UI-library based on [Tkinter](https://docs.python.org/3/library/tkinter.html), which provides new, modern and fully customizable widgets.


## Feedback

If you have any feedback, suggestions/feature requests or notice any bugs please reach out to simon@swhelan.dev


 
 

