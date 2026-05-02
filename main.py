# main.py
# Description: TBD

# Author: Marcin Kaminski

# ---IMPORTS---

import mysql.connector # Importing the mysql.connector module to establish a connection to the MySQL database
# Sourced from: https://www.w3schools.com/python/python_mysql_getstarted.asp

import dbconfig as cfg # Importing the dbconfig module to access the database configuration parameters defined in dbconfig.py

from neo4j import GraphDatabase # Importing the GraphDatabase class from the neo4j module to establish a connection to the Neo4j database
# Sourced from: https://neo4j.com/docs/python-manual/current/

import tkinter as tk # Importing the tkinter module to create a graphical user interface (GUI) for the application
# Sourced from: https://docs.python.org/3/library/tkinter.html

from tkinter import ttk, messagebox, filedialog # Importing specific classes and functions from the tkinter module to create and manage GUI components such as treeview, message boxes, and file dialogs
# Sourced from: https://docs.python.org/3/library/tkinter.ttk.html
# Sourced from: https://docs.python.org/3/library/tkinter.messagebox.html

import csv # Importing the csv module to read and write CSV files for data import/export functionality
# Sourced from: https://docs.python.org/3/library/csv.html

import networkx as nx # Importing the networkx module to create and manipulate complex networks/graphs, which can be used for visualizing connections between attendees or sessions in the conference
# Sourced from: https://networkx.org/documentation/stable/index.html

import matplotlib.pyplot as plt # Importing the pyplot module from matplotlib to create visualizations
# Sourced from: https://www.w3schools.com/python/matplotlib_pyplot.asp



# ---DATABASE CONNECTIONS---

db = mysql.connector.connect(**cfg.mysql) # Unpacking the mysql dictionary from dbconfig.py to create a connection

driver = GraphDatabase.driver(
    cfg.NEO4J_URI,
    auth=(cfg.NEO4J_USER, cfg.NEO4J_PASSWORD)
) # Creating a driver instance to connect to the Neo4j database using the URI and authentication credentials from dbconfig.py



# ---TABLE DISPLAY AND CSV EXPORT---

def show_table(columns, data, title="Results"): # Defining a function to display a table of data in a new window with the specified columns, data, and title
    win = tk.Toplevel(root) # Creating a new top-level window (a child window of the main application window) to display the table of data
    win.title(title) # Setting the title of the new window to the specified title parameter (default is "Results")
    win.geometry("900x400") # Setting the size of the new window to 900 pixels in width and 400 pixels in height

    frame = tk.Frame(win) # Creating a Frame widget to hold the Treeview and Scrollbar components within the new window
    frame.pack(fill="both", expand=True) # Packing the frame into the new window, allowing it to fill the available space and expand as needed

    tree = ttk.Treeview(frame, columns=columns, show="headings") # Creating a Treeview widget to display the data in a tabular format, with the specified columns and showing only the headings (no tree structure)

    for col in columns: # Iterating over each column name in the columns parameter to set up the Treeview headings and column widths
        tree.heading(col, text=col) # Setting the heading of each column in the Treeview to the corresponding column name from the columns parameter
        tree.column(col, width=160) # Setting the width of each column in the Treeview to 160 pixels for better visibility

    for row in data: # Iterating over each row of data in the data parameter to insert it into the Treeview
        tree.insert("", tk.END, values=row) # Inserting each row of data into the Treeview, with an empty string as the parent (indicating top-level items) and tk.END to append the row at the end of the Treeview

    tree.pack(side="left", fill="both", expand=True) # Packing the Treeview into the frame, allowing it to fill the available space and expand as needed, and aligning it to the left side of the frame

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview) # Creating a vertical Scrollbar widget and linking it to the Treeview's yview method to allow scrolling through the data when there are more rows than can fit in the visible area of the Treeview
    tree.configure(yscroll=scrollbar.set) # Configuring the Treeview to use the scrollbar for vertical scrolling by setting its yscroll command to the scrollbar's set method
    scrollbar.pack(side="right", fill="y") # Packing the scrollbar into the frame, aligning it to the right side and allowing it to fill the vertical space of the frame

    def export_csv(): # Defining a function to export the displayed data to a CSV file when the user clicks the "Export to CSV" button
        if not data: # Checking if there is no data to export (i.e., if the data list is empty)
            messagebox.showerror("Error", "No data to export") # Displaying an error message box to the user if there is no data to export, with the title "Error" and the message "No data to export"
            return # Returning from the function if there is no data to export, preventing further execution of the export logic

        file_path = filedialog.asksaveasfilename( # Opening a file dialog to allow the user to choose the location and name for the CSV file to be saved, with the following parameters:
            defaultextension=".csv", # Setting the default file extension to ".csv" to ensure that the saved file is recognized as a CSV file
            initialfile=title.replace(" ", "_") + ".csv", # Setting the initial file name in the save dialog to the title of the table with spaces replaced by underscores, followed by the ".csv" extension (e.g., "Results.csv")
            filetypes=[("CSV files", "*.csv")], # Restricting the file types that can be selected in the save dialog to only CSV files, with the description "CSV files" and the file extension filter "*.csv"
            title="Save CSV File" # Setting the title of the file dialog to "Save CSV File" to indicate to the user that they are saving a CSV file
        )

        if not file_path: # Checking if the user did not select a file path (i.e., if the file_path variable is empty or None)
            return # Returning from the function if the user did not select a file path, preventing further execution of the export logic and avoiding errors when trying to write to an invalid file path

        try: # Attempting to write the data to the specified CSV file path using a try-except block to catch any exceptions that may occur during the file writing process
            with open(file_path, mode="w", newline="", encoding="utf-8") as file: # Opening the specified file path in write mode ("w"), with newline set to an empty string to prevent extra blank lines in the CSV file, and encoding set to "utf-8" to support a wide range of characters
                writer = csv.writer(file) # Creating a CSV writer object to write data to the opened file
                writer.writerow(columns) # Writing the column headers to the CSV file as the first row using the writerow method of the CSV writer object, passing in the columns list as the argument
                writer.writerows(data) # Writing the data rows to the CSV file using the writerows method of the CSV writer object, passing in the data list (which contains the rows of data) as the argument

            messagebox.showinfo("Success", "Data exported successfully") # Displaying an information message box to the user indicating that the data was exported successfully, with the title "Success" and the message "Data exported successfully"

        except Exception as e: # Catching any exceptions that occur during the file writing process and storing the exception object in the variable e
            messagebox.showerror("Error", str(e)) # Displaying an error message box to the user if an exception occurs during the file writing process, with the title "Error" and the message containing the string representation of the exception (e.g., the error message)

    tk.Button(win, text="Export to CSV", command=export_csv).pack(pady=8) # Creating a Button widget in the new window to allow the user to export the displayed data to a CSV file, with the text "Export to CSV" and the command set to the export_csv function defined earlier, and packing it into the window with a vertical padding of 8 pixels



# ---OPTIONS---

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


# ---EXIT APPLICATION---

def close_application(): # Defining a function to close the database connections and the main application window when the user chooses to exit the application
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"): # Displaying a confirmation dialog box when the user attempts to close the application, asking if they are sure they want to exit
        try:
           db.close() # Attempting to close the MySQL database connection
           driver.close() # Attempting to close the Neo4j database connection
        except Exception: # Catching any exceptions that occur during the closing of the database connections and ignoring them (e.g., if the connections are already closed or if there is an error during closing)
           pass # Ignoring any exceptions that occur during the closing of the database connections
        
        root.destroy() # If the user confirms, the main application window is destroyed, effectively closing the application



# ---MAIN GUI---

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
   #speakers_sessions() # Calling the speakers_sessions function to execute the logic for viewing speakers and sessions (to be defined later)
   #attendees_by_company() # Calling the attendees_by_company function to execute the logic for viewing attendees by company (to be defined later)
   #add_attendee() # Calling the add_attendee function to execute the logic for adding a new attendee (to be defined later)
   #connected_attendees() # Calling the connected_attendees function to execute the logic for viewing connected attendees (to be defined later)
   #add_connection() # Calling the add_connection function to execute the logic for adding a connection between attendees (to be defined later)
   #view_rooms() # Calling the view_rooms function to execute the logic for viewing rooms (to be defined later)