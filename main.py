# main.py
# Description: TBD
# Author: Marcin Kaminski

import mysql.connector # Importing the mysql.connector module to establish a connection to the MySQL database
import dbconfig as cfg # Importing the dbconfig module to access the database configuration parameters defined in dbconfig.py
from neo4j import GraphDatabase # Importing the GraphDatabase class from the neo4j module to establish a connection to the Neo4j database

import tkinter as tk # Importing the tkinter module to create a graphical user interface (GUI) for the application
from tkinter import ttk, messagebox, filedialog # Importing specific classes and functions from the tkinter module to create and manage GUI components such as treeview, message boxes, and file dialogs
import csv # Importing the csv module to read and write CSV files for data import/export functionality


# DATABASE CONNECTIONS

db = mysql.connector.connect(**cfg.mysql) # Unpacking the mysql dictionary from dbconfig.py to create a connection

driver = GraphDatabase.driver(
    cfg.NEO4J_URI,
    auth=(cfg.NEO4J_USER, cfg.NEO4J_PASSWORD)
) # Creating a driver instance to connect to the Neo4j database using the URI and authentication credentials from dbconfig.py


# OPTION 1: View Speakers & Sessions

def speakers_sessions():
    print("Not implemented yet")

# OPTION 2: View Attendees by Company

def attendees_by_company():
    print("Not implemented yet")

# OPTION 3: Add New Attendee

def add_attendee():
    print("Not implemented yet")

# OPTION 4: View Connected Attendees

def connected_attendees():
    print("Not implemented yet")

# OPTION 5: Add Attendee Connection

def add_connection():
    print("Not implemented yet")

# OPTION 6: View Rooms

def view_rooms():
    print("Not implemented yet")

# EXIT APPLICATION

def close_application():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"): # Displaying a confirmation dialog box when the user attempts to close the application, asking if they are sure they want to exit
        root.destroy() # If the user confirms, the main application window is destroyed, effectively closing the application



# MAIN GUI

root = tk.Tk() # Creating the main application window using Tkinter
root.title("Conference Manager") # Setting the title of the main application window to "Conference Manager"
root.geometry("420x420") # Setting the size of the main application window to 420 pixels in width and 420 pixels in height

style = ttk.Style() # Creating a Style object to customize the appearance of the GUI components
style.theme_use("clam") # Setting the theme of the GUI to "clam" for a modern look and feel

title_label = tk.Label( # Creating a Label widget to display the title of the application
    root, # Setting the parent of the label to the main application window
    text="Conference Manager", # Setting the text of the label to "Conference Manager"
    font=("Arial", 18, "bold") # Setting the font of the label to Arial, size 18, and bold style
)
title_label.pack(pady=15) # Packing the label into the main application window with a vertical padding of 15 pixels

tk.Button(
    root,
    text="1. View Speakers & Sessions", # Creating a Button widget to allow the user to view speakers and sessions
    width=35,
    command=speakers_sessions # Setting the command to be executed when the button is clicked to the speakers_sessions function (to be defined later)
).pack(pady=5)

tk.Button(
    root,
    text="2. View Attendees by Company", # Creating a Button widget to allow the user to view attendees grouped by their company affiliation
    width=35,
    command=attendees_by_company # Setting the command to be executed when the button is clicked to the attendees_by_company function (to be defined later)
).pack(pady=5)

tk.Button(
    root,
    text="3. Add New Attendee", # Creating a Button widget to allow the user to add a new attendee to the conference
    width=35,
    command=add_attendee # Setting the command to be executed when the button is clicked to the add_attendee function (to be defined later)
).pack(pady=5)

tk.Button(
    root,
    text="4. View Connected Attendees", # Creating a Button widget to allow the user to view attendees who are connected (e.g., through shared sessions or companies)
    width=35,
    command=connected_attendees # Setting the command to be executed when the button is clicked to the connected_attendees function (to be defined later)
).pack(pady=5)

tk.Button( 
    root,
    text="5. Add Attendee Connection", # Creating a Button widget to allow the user to add a connection between two attendees (e.g., indicating that they know each other or have attended the same session)
    width=35,
    command=add_connection # Setting the command to be executed when the button is clicked to the add_connection function (to be defined later)
).pack(pady=5)

tk.Button(
    root,
    text="6. View Rooms", # Creating a Button widget to allow the user to view the rooms available for the conference sessions
    width=35,
    command=view_rooms # Setting the command to be executed when the button is clicked to the view_rooms function (to be defined later)
).pack(pady=5)

tk.Button(
    root,
    text="Exit", # Creating a Button widget to allow the user to exit the application
    width=35,
    command=close_application # Setting the command to be executed when the button is clicked to the close_application function (to be defined later)
).pack(pady=20)

root.protocol("WM_DELETE_WINDOW", close_application) # Setting the protocol for the window close event (when the user clicks the "X" button on the window) to execute the close_application function (to be defined later)

root.mainloop() # Starting the main event loop of the application, which waits for user interactions and updates the GUI accordingly
 





#if __name__ == "__main__": # Checking if the script is being run directly (as the main program) rather than imported as a module
    #print("To be continued...")