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

import re # Importing the re module to use regular expressions for validating user input
# Sourced from: https://docs.python.org/3/library/re.html


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

        # Sanitize title for file name
        safe_title = re.sub(r"[^A-Za-z0-9_-]+", "_", title).strip("_") # Sanitizing the title to create a safe file name for the CSV export by replacing any characters that are not letters, digits, underscores, or hyphens with underscores, and stripping any leading or trailing underscores from the resulting string, and storing it in the variable safe_title for use as the default file name in the save dialog

        if not safe_title: # Checking if the sanitized title is empty (i.e., if the original title contained only invalid characters that were replaced with underscores, resulting in an empty string)
           safe_title = "results" # Setting a default file name of "results" if the sanitized title is empty, to ensure that there is a valid default file name for the CSV export even if the original title contained only invalid characters

        # Avoid duplicate .csv
        if safe_title.lower().endswith(".csv"): # Checking if the sanitized title already ends with the ".csv" extension (case-insensitive) to avoid having a duplicate ".csv" extension in the default file name for the CSV export
           safe_title = safe_title[:-4] # Removing the last 4 characters (i.e., the ".csv" extension) from the sanitized title if it already ends with ".csv", to ensure that the default file name for the CSV export does not have a duplicate ".csv" extension when the user saves the file

        file_path = filedialog.asksaveasfilename( # Opening a file dialog to allow the user to choose the location and name for the CSV file to be saved, with the following parameters:
            defaultextension=".csv", # Setting the default file extension to ".csv" to ensure that the saved file is recognized as a CSV file
            initialfile=f"{safe_title}.csv", # Setting the initial file name in the save dialog to a sanitized version of the title (safe_title) with a .csv extension, to provide a default name for the exported CSV file
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

def speakers_sessions(): # Defining a function to allow the user to view speakers and their associated sessions, with a search functionality to filter speakers by name
    win = tk.Toplevel(root) # Creating a new top-level window (a child window of the main application window) to display the speakers and sessions information
    win.title("View Speakers & Sessions") # Setting the title of the new window to "View Speakers & Sessions" to indicate the purpose of the window to the user
    win.geometry("350x150") # Setting the size of the new window to 350 pixels in width and 150 pixels in height, providing enough space for the search input and button while keeping it compact

    tk.Label(win, text="Enter speaker name: ").pack(pady=5) # Creating a Label widget in the new window to prompt the user to enter a speaker name or part of a name for searching, with the specified text and packing it into the window with a vertical padding of 5 pixels
    entry = tk.Entry(win, width=30) # Creating an Entry widget in the new window to allow the user to input a speaker name or part of a name for searching, with a width of 30 characters for better visibility and user experience
    entry.pack(pady=5) # Packing the Entry widget into the new window with a vertical padding of 5 pixels to provide spacing between the label and the entry field

    def search(): # Defining a function to perform the search for speakers and their associated sessions based on the user's input in the entry field, and to display the results in a table format
        cursor = db.cursor() # Creating a cursor object from the MySQL database connection to execute SQL queries and fetch results

        query = """
        SELECT s.speakerName, s.sessionTitle, r.roomName
        FROM session s
        JOIN room r ON s.roomID = r.roomID
        WHERE s.speakerName LIKE %s
        ORDER BY s.speakerName
        """

        cursor.execute(query, ("%" + entry.get() + "%",)) # Executing the SQL query using the cursor's execute method, passing in the query string and a tuple containing the search parameter (the user's input from the entry field, wrapped with wildcard characters "%" for partial matching) to filter speakers by name
        results = cursor.fetchall() # Fetching all the results of the executed query using the cursor's fetchall method, which returns a list of tuples containing the speaker name, session title, and room name for each matching record

        if not results: # Checking if there are no results returned from the query (i.e., if the results list is empty)
            messagebox.showinfo("No Results", "No speakers found of that name.") # Displaying an information message box to the user if no speakers are found matching the search criteria, with the title "No Results" and the message "No speakers found of that name."
        else: # If there are results returned from the query, calling the show_table function defined earlier to display the results in a new window with a table format, passing in the column names ["Speaker", "Session", "Room"], the results data, and the title "Speakers and Sessions" for the new window
            show_table(
                ["Speaker", "Session", "Room"],
                results,
                f"Session Details For {entry.get()}" # Setting the title of the new window to include the search term entered by the user for better context (e.g., "Session Details For: John")
            )

    tk.Button(win, text="Search", command=search).pack(pady=10) # Creating a Button widget in the new window to allow the user to perform the search for speakers and sessions, with the text "Search" and the command set to the search function defined earlier, and packing it into the window with a vertical padding of 10 pixels to provide spacing between the entry field and the button


# OPTION 2: View Attendees by Company

def attendees_by_company(): # Defining a function to allow the user to view attendees grouped by their company affiliation, with a search functionality to filter attendees by company ID
    win = tk.Toplevel(root) # Creating a new top-level window (a child window of the main application window) to display the attendees by company information
    win.title("View Attendees by Company") # Setting the title of the new window to "View Attendees by Company" to indicate the purpose of the window to the user
    win.geometry("350x150") # Setting the size of the new window to 350 pixels in width and 150 pixels in height, providing enough space for the search input and button while keeping it compact

    tk.Label(win, text="Enter Company ID:").pack(pady=5) # Creating a Label widget in the new window to prompt the user to enter a company ID for searching, with the specified text and packing it into the window with a vertical padding of 5 pixels
    entry = tk.Entry(win, width=30) # Creating an Entry widget in the new window to allow the user to input a company ID for searching, with a width of 30 characters for better visibility and user experience
    entry.pack(pady=5) # Packing the Entry widget into the new window with a vertical padding of 5 pixels to provide spacing between the label and the entry field

    def search(): # Defining a function to perform the search for attendees based on the company ID entered by the user, and to display the results in a table format
        company_id = entry.get() # Retrieving the company ID entered by the user from the entry field using the get method and storing it in the variable company_id for further processing in the search logic

        if not company_id.isdigit() or int(company_id) <= 0: # Validating the company ID entered by the user to ensure it is a positive integer, by checking if it consists of digits only and if its integer value is greater than 0
            messagebox.showerror("Error", "Invalid company ID.\nPlease enter a valid company ID.") # Displaying an error message box to the user if the company ID is invalid (i.e., not a positive integer), with the title "Error" and the message "Invalid company ID"
            return # Returning from the function if the company ID is invalid, preventing further execution of the search logic and avoiding errors when trying to query the database with an invalid company ID

        cursor = db.cursor() # Creating a cursor object from the MySQL database connection to execute SQL queries and fetch results for the search based on the company ID entered by the user

        cursor.execute( # Executing a SQL query to check if the company with the specified company ID exists in the database, by selecting the company name from the company table where the company ID matches the user input
            "SELECT companyName FROM company WHERE companyID = %s",
            (company_id,)
        )
        company = cursor.fetchone() # Fetching the result of the executed query using the cursor's fetchone method, which returns a single tuple containing the company name if a matching record is found, or None if no matching record exists in the database for the specified company ID

        if not company: # Checking if the company variable is None, which indicates that no matching company was found in the database for the specified company ID
            messagebox.showerror("Error", f"Company with ID {company_id} does not exist")
            return # Displaying an error message box to the user if the company does not exist in the database, with the title "Error" and the message "Company does not exist", and returning from the function to prevent further execution of the search logic since there is no valid company to search for attendees

        query = """
        SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, s.sessionDate,r.roomName
        FROM attendee a
        LEFT JOIN registration reg ON a.attendeeID = reg.attendeeID
        LEFT JOIN session s ON reg.sessionID = s.sessionID
        LEFT JOIN room r ON s.roomID = r.roomID
        WHERE a.attendeeCompanyID = %s
        ORDER BY a.attendeeName
        """

        cursor.execute(query, (company_id,)) # Executing the SQL query to retrieve the attendees associated with the specified company ID, along with their date of birth, session title, speaker name, and room name, by joining the attendee, registration, session, and room tables based on their relationships and filtering by the attendeeCompanyID matching the user input company ID
        results = cursor.fetchall() # Fetching all the results of the executed query using the cursor's fetchall method, which returns a list of tuples containing the attendee name, date of birth, session title, speaker name, and room name for each attendee associated with the specified company ID

        if not results: # Checking if there are no results returned from the query (i.e., if the results list is empty), which indicates that the company exists but has no attendees registered for any sessions
            messagebox.showinfo("No Results", f"{company[0]} Attendees.\n" f"No attendees found for {company[0]}.") # Displaying an information message box to the user if no attendees are found for the specified company, with the title "No Results" and a message that includes the company name and indicates that no attendees were found for that company
        else: # If there are results returned from the query, calling the show_table function defined earlier to display the results in a new window with a table format, passing in the column names ["Attendee", "DOB", "Session", "Speaker", "Date", "Room"], the results data, and a title that includes the company name for better context (e.g., "Attendees from: TechCorp")
            show_table(
                ["Attendee", "DOB", "Session", "Speaker", "Date", "Room"],
                results,
                f"{company[0]} Attendees" # Setting the title of the new window to include the company name retrieved from the database for better context (e.g., "TechCorp Attendees")
            )

    tk.Button(win, text="Search", command=search).pack(pady=10) # Creating a Button widget in the new window to allow the user to perform the search for attendees by company, with the text "Search" and the command set to the search function defined earlier, and packing it into the window with a vertical padding of 10 pixels to provide spacing between the entry field and the button


# OPTION 3: Add New Attendee

def add_attendee(): # Defining a function to allow the user to add a new attendee to the conference by entering their details in a form, validating the input, and inserting the new attendee into the database
    win = tk.Toplevel(root) # Creating a new top-level window (a child window of the main application window) to display the form for adding a new attendee
    win.title("Add New Attendee") # Setting the title of the new window to "Add New Attendee" to indicate the purpose of the window to the user
    win.geometry("400x350") # Setting the size of the new window to 400 pixels in width and 350 pixels in height, providing enough space for the form fields and the submit button while keeping it compact

    labels = [ # Defining a list of labels for the form fields to be displayed in the new window, which includes "Attendee ID", "Name", "DOB (YYYY-MM-DD)", "Gender (Male/Female)", and "Company ID" to guide the user in entering the required information for the new attendee    
        "Attendee ID", 
        "Name", 
        "DOB (YYYY-MM-DD)", 
        "Gender (Male/Female)",
        "Company ID"
    ]

    entries = [] # Initializing an empty list to store the Entry widgets for each form field, which will be used later to retrieve the user input when the form is submitted

    for label in labels:
        tk.Label(win, text=label).pack() # Iterating over each label in the labels list to create a Label widget for each form field, setting the text of the label to the corresponding label from the list, and packing it into the new window to display it to the user
        entry = tk.Entry(win, width=35) # Creating an Entry widget for each form field to allow the user to input the required information for the new attendee, with a width of 35 characters for better visibility and user experience
        entry.pack(pady=3) # Packing the Entry widget into the new window with a vertical padding of 3 pixels to provide spacing between the form fields, and appending the Entry widget to the entries list for later retrieval of user input when the form is submitted
        entries.append(entry) # Appending the created Entry widget to the entries list to keep track of all the Entry widgets for later use when retrieving user input for the new attendee details

    def save_attendee(): # Defining a function to save the new attendee details entered by the user in the form, which includes validating the input, checking for existing company ID, and inserting the new attendee into the database if all validations pass
        try: # Attempting to retrieve the user input from the Entry widgets, validate the input, check for existing company ID in the database, and insert the new attendee into the database using a try-except block to catch any exceptions that may occur during the process
            attendee_id = entries[0].get()
            attendee_name = entries[1].get()
            attendee_dob = entries[2].get()
            attendee_gender = entries[3].get()
            company_id = entries[4].get()

            if attendee_gender not in ["Male", "Female"]: # Validating the gender input to ensure it is either "Male" or "Female", by checking if the value entered by the user in the gender field is not in the list of valid options ["Male", "Female"]
                messagebox.showerror("Error", "*** ERROR *** \nGender must be Male/Female") # Displaying an error message box to the user if the gender input is invalid (i.e., not "Male" or "Female").
                return # Returning from the function if the gender input is invalid, preventing further execution of the save logic and avoiding errors when trying to insert invalid data into the database    

            cursor = db.cursor() # Creating a cursor object from the MySQL database connection to execute SQL queries for validating the company ID and inserting the new attendee into the database

            cursor.execute( # Executing a SQL query to check if the company with the specified company ID exists in the database, by selecting the company ID from the company table where the company ID matches the user input
                "SELECT companyID FROM company WHERE companyID = %s", # Executing the SQL query to check for the existence of the company ID in the database, by selecting the companyID from the company table where the companyID matches the user input company_id
                (company_id,) # Passing the company_id as a parameter in a tuple to the execute method to prevent SQL injection and ensure proper handling of the input when querying the database for the existence of the company ID
            )

            if not cursor.fetchone(): # Checking if the result of the executed query is None, which indicates that no matching company ID was found in the database for the specified company ID entered by the user
                messagebox.showerror("Error", f"*** ERROR *** \nCompany ID: {company_id} does not exist") # Displaying an error message box to the user if the company ID does not exist in the database, with the title "Error" and a message that includes the invalid company ID and indicates that it does not exist

            query = """
            INSERT INTO attendee 
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute( # Executing a SQL query to insert the new attendee details into the attendee table in the database, by using an INSERT INTO statement with placeholders for the values to be inserted, and passing in a tuple containing the user input for attendee ID, name, date of birth, gender, and company ID to the execute method to insert the new attendee into the database
                query,
                (
                    attendee_id,
                    attendee_name,
                    attendee_dob,
                    attendee_gender,
                    company_id
                )
            )

            db.commit() # Committing the transaction to the database to save the changes made by the INSERT statement, ensuring that the new attendee is added to the database and the changes are persisted
            messagebox.showinfo("Success", "Attendee successfully added") # Displaying an information message box to the user indicating that the new attendee was successfully added to the database, with the title "Success" and the message "Attendee successfully added"

            for entry in entries: # Iterating over each Entry widget in the entries list to clear the input fields after successfully adding the new attendee, by calling the delete method on each Entry widget to remove the text from the entry field and reset it for potential new input
                entry.delete(0, tk.END) # Deleting the text from each Entry widget in the entries list by calling the delete method with parameters 0 and tk.END, which removes all text from the entry field, effectively clearing it for new input after successfully adding the attendee to the database

        except mysql.connector.IntegrityError: # Catching a specific exception (IntegrityError) that may occur during the execution of the SQL query to insert the new attendee, which typically indicates a violation of database constraints such as a duplicate primary key (e.g., if the attendee ID already exists in the database)
            messagebox.showerror("Error", f"*** ERROR *** \nAttendee ID: {entries[0].get()} already exists") # Displaying an error message box to the user if an IntegrityError occurs during the insertion of the new attendee, with the title "Error" and a message that includes the attendee ID entered by the user and indicates that it already exists in the database

        except mysql.connector.Error as err: # Catching any other MySQL-related exceptions that may occur during the execution of the SQL queries for validating the company ID and inserting the new attendee, and storing the exception object in the variable err to display a more specific error message to the user
            messagebox.showerror("Error", f"*** ERROR ***\n{str(err)}") # Displaying an error message box to the user if any MySQL-related exceptions occur during the process of validating the company ID or inserting the new attendee
        #except ValueError as ve:
            #messagebox.showerror("Error", f"*** ERROR ***\n{str(ve)}")

    tk.Button(win, text="Add Attendee", command=save_attendee).pack(pady=15) # Creating a Button widget in the new window to allow the user to submit the form and add the new attendee, with the text "Add Attendee" and the command set to the save_attendee function defined earlier, and packing it into the window with a vertical padding of 15 pixels to provide spacing between the form fields and the button


# OPTION 4: View Connected Attendees

def connected_attendees(): # Defining a function to allow the user to view attendees who are connected (e.g., through shared sessions or companies)

    win = tk.Toplevel(root) # Creating a new top-level window (a child window of the main application window) to display the form for viewing connected attendees
    win.title("View Connected Attendees") # Setting the title of the new window to "View Connected Attendees" to indicate the purpose of the window to the user
    win.geometry("350x180") # Setting the size of the new window to 350 pixels in width and 180 pixels in height, providing enough space for the input field and buttons while keeping it compact

    tk.Label(win, text="Enter Attendee ID:").pack(pady=5) # Creating a Label widget in the new window to prompt the user to enter an attendee ID for searching connected attendees, with the specified text and packing it into the window with a vertical padding of 5 pixels
    entry = tk.Entry(win, width=30) # Creating an Entry widget in the new window to allow the user to input an attendee ID for searching connected attendees, with a width of 30 characters for better visibility and user experience
    entry.pack(pady=5) # Packing the Entry widget into the new window with a vertical padding of 5 pixels to provide spacing between the label and the entry field

    def search(): # Defining a function to perform the search for connected attendees based on the attendee ID entered by the user, which includes validating the input, retrieving the attendee's name, and querying the Neo4j database for connected attendees, and then displaying the results in a table format
        attendee_id = entry.get() # Retrieving the attendee ID entered by the user from the entry field using the get method and storing it in the variable attendee_id for further processing in the search logic to find connected attendees based on this ID

        if not attendee_id.isdigit(): # Validating the attendee ID input to ensure it is a valid integer, by checking if the value entered by the user in the attendee ID field consists of digits only (i.e., is a positive integer)
            messagebox.showerror("Error", "*** ERROR ***\nInvalid attendee ID") # Displaying an error message box to the user if the attendee ID input is invalid (i.e., not a valid integer), with the title "Error" and the message "Invalid attendee ID"
            return # Returning from the function if the attendee ID input is invalid, preventing further execution of the search logic and avoiding errors when trying to query the database with an invalid attendee ID

        attendee_id = int(attendee_id) # Converting the validated attendee ID input from a string to an integer using the int function, and storing the converted value back in the variable attendee_id for use in subsequent database queries to find connected attendees based on this ID

        cursor = db.cursor() # Creating a cursor object from the mySQL database connection to execute SQL queries for retrieving the attendee's name and querying the Neo4j database for connected attendees based on the specified attendee ID entered by the user in the search function for connected attendees

        cursor.execute( # Executing a SQL query to retrieve the name of the attendee with the specified attendee ID from the database, by selecting the attendeeName from the attendee table where the attendeeID matches the user input attendee_id
            "SELECT attendeeName FROM attendee WHERE attendeeID = %s",
            (attendee_id,)
        )

        attendee = cursor.fetchone() # Fetching the result of the executed query using the cursor's fetchone method, which returns a single tuple containing the attendee name if a matching record is found, or None if no matching record exists in the database for the specified attendee ID entered by the user in the search function for connected attendees

        if not attendee: # Checking if the attendee variable is None, which indicates that no matching attendee was found in the database for the specified attendee ID entered by the user
            messagebox.showerror("Error", "*** ERROR ***\nAttendee does not exist") # Displaying an error message box to the user if the attendee does not exist in the database, with the title "Error" and the message "Attendee does not exist", and returning from the function to prevent further execution of the search logic since there is no valid attendee to search for connected attendees
            return# Returning from the function if the attendee does not exist in the database, preventing further execution of the search logic since there is no valid attendee to search for connected attendees

        connected_data = [] # Initializing an empty list to store the connected attendees' data, which will be populated with tuples containing the connected attendee ID and name for each connected attendee found in the Neo4j database based on the specified attendee ID entered by the user in the search function for connected attendees

        with driver.session(database="appdbprojNeo4j") as session: # Creating a session with the Neo4j database using the driver instance, and specifying the database name "appdbprojNeo4j" to execute queries for finding connected attendees based on the specified attendee ID entered by the user in the search function for connected attendees
            query = """ 
            MATCH (a:Attendee {AttendeeID: $id})-[r:CONNECTED_TO]-(b:Attendee)
            RETURN b.AttendeeID AS connectedID
            """

            results = session.run(query, id=attendee_id) # Running the specified Cypher query in the Neo4j database using the session's run method, passing in the query string and a parameter dictionary containing the attendee ID (id) to find connected attendees based on this ID, and storing the results in the variable results for further processing

            for record in results: # Iterating over each record in the results returned from the Neo4j query to extract the connected attendee ID and retrieve the corresponding attendee name from the MySQL database, and then appending the connected attendee ID and name as a tuple to the connected_data list for later display in a table format
                connected_id = record["connectedID"]

                cursor.execute( # Executing a SQL query to retrieve the name of the connected attendee with the specified connected attendee ID from the database, by selecting the attendeeName from the attendee table where the attendeeID matches the connected_id retrieved from the Neo4j query results
                    "SELECT attendeeName FROM attendee WHERE attendeeID = %s",
                    (connected_id,)
                )

                connected_name = cursor.fetchone() # Fetching the result of the executed query using the cursor's fetchone method, which returns a single tuple containing the connected attendee name if a matching record is found, or None if no matching record exists in the database for the specified connected attendee ID retrieved from the Neo4j query results

                if connected_name: # Checking if the connected_name variable is not None, which indicates that a matching record was found in the database for the specified connected attendee ID retrieved from the Neo4j query results
                    connected_data.append( # Appending a tuple containing the connected attendee ID and name to the connected_data list, which will be used later to display the connected attendees in a table format, by adding a tuple with the connected_id and the first element of the connected_name tuple (which is the attendee name) to the connected_data list
                        (connected_id, connected_name[0]) # Appending a tuple containing the connected attendee ID and name to the connected_data list, which will be used later to display the connected attendees in a table format, by adding a tuple with the connected_id and the first element of the connected_name tuple (which is the attendee name) to the connected_data list
                    )

        if not connected_data: # Checking if the connected_data list is empty, which indicates that no connected attendees were found in the Neo4j database for the specified attendee ID entered by the user
            messagebox.showinfo("No Connections", f"Attendee Name: {attendee[0]}\nNo connections") # Displaying an information message box to the user if no connected attendees are found for the specified attendee ID, with the title "No Connections" and a message that includes the attendee name retrieved from the database and indicates that there are no connections for that attendee
        else: # If there are connected attendees found in the Neo4j database, calling the show_table function defined earlier to display the connected attendees in a new window with a table format
            show_table( # Calling the show_table function to display the connected attendees in a new window with a table format, passing in the column names
                ["Connected Attendee ID", "Connected Attendee Name"],
                connected_data,
                f"These attendees are connected to {attendee[0]}:"
            )

    def visualize(): # Defining a function to visualize the connections of the specified attendee ID in a graph format using NetworkX and Matplotlib, which includes validating the input, retrieving the attendee's name, querying the Neo4j database for connected attendees, and then visualizing the connections in a graph format
        attendee_id = entry.get() # Retrieving the attendee ID entered by the user from the entry field using the get method and storing it in the variable attendee_id for further processing in the visualization logic to find connected attendees based on this ID and visualize the connections in a graph format

        if not attendee_id.isdigit(): # Validating the attendee ID input to ensure it is a valid integer, by checking if the value entered by the user in the attendee ID field consists of digits only (i.e., is a positive integer)
            messagebox.showerror("Error", "*** ERROR ***\nInvalid attendee ID") # Displaying an error message box to the user if the attendee ID input is invalid (i.e., not a valid integer), with the title "Error" and the message "Invalid attendee ID"
            return # Returning from the function if the attendee ID input is invalid, preventing further execution of the visualization logic and avoiding errors when trying to query the database with an invalid attendee ID

        visualize_connections(int(attendee_id)) # Calling the visualize_connections function defined to visualize the connections of the specified attendee ID in a graph format, by passing in the validated and converted attendee ID as an integer to the function for further processing to find connected attendees and visualize the connections in a graph format using NetworkX and Matplotlib

    tk.Button(win, text="Search", command=search).pack(pady=5) # Creating a Button widget in the new window to allow the user to perform the search for connected attendees, with the text "Search" and the command set to the search function defined earlier, and packing it into the window with a vertical padding of 5 pixels to provide spacing between the entry field and the button
    tk.Button(win, text="Visualize Graph", command=visualize).pack(pady=5) # Creating a Button widget in the new window to allow the user to visualize the connections of the specified attendee ID in a graph format, with the text "Visualize Graph" and the command set to the visualize function defined earlier, and packing it into the window with a vertical padding of 5 pixels to provide spacing between the search button and the visualization button

# GRAPH VISUALIZATION FUNCTION

def visualize_connections(attendee_id): # Defining a function to visualize the connections of a specified attendee ID in a graph format using NetworkX and Matplotlib, which includes validating the input, retrieving the attendee's name, querying the Neo4j database for connected attendees, and then visualizing the connections in a graph format
    cursor = db.cursor() #  Creating a cursor object from the MySQL database connection to execute SQL queries for retrieving the attendee's name and querying the Neo4j database for connected attendees based on the specified attendee ID entered by the user in the visualization function for connected attendees

    cursor.execute( # Executing a SQL query to retrieve the name of the attendee with the specified attendee ID from the database, by selecting the attendeeName from the attendee table where the attendeeID matches the user input attendee_id
        "SELECT attendeeName FROM attendee WHERE attendeeID = %s",
        (attendee_id,)
    )

    attendee = cursor.fetchone() # Fetching the result of the executed query using the cursor's fetchone method, which returns a single tuple containing the attendee name if a matching record is found, or None if no matching record exists in the database for the specified attendee ID entered by the user in the visualization function for connected attendees

    if not attendee: # Checking if the attendee variable is None, which indicates that no matching attendee was found in the database for the specified attendee ID entered by the user
        messagebox.showerror("Error", "*** ERROR ***\nAttendee does not exist")
        return # Displaying an error message box to the user if the attendee does not exist in the database, with the title "Error" and the message "Attendee does not exist", and returning from the function to prevent further execution of the visualization logic since there is no valid attendee to visualize connections for

    attendee_name = attendee[0] # Storing the attendee name retrieved from the database in the variable attendee_name for use in the graph visualization, by accessing the first element of the attendee tuple (which is the attendee name) and assigning it to the variable attendee_name for later use in labeling the graph nodes and providing context in the visualization of connected attendees

    graph = nx.Graph() # Creating an empty graph object using NetworkX to represent the connections between attendees, which will be populated with nodes and edges based on the connected attendees retrieved from the Neo4j database for the specified attendee ID entered by the user in the visualization function for connected attendees
    graph.add_node(attendee_name) # Adding a node to the graph for the specified attendee, using the attendee name retrieved from the database as the label for the node, which will serve as the central node in the graph visualization of connected attendees based on the specified attendee ID entered by the user in the visualization function for connected attendees

    found_connection = False # Initializing a boolean variable found_connection to False, which will be used to track whether any connected attendees are found in the Neo4j database for the specified attendee ID entered by the user in the visualization function for connected attendees, and will be updated to True if at least one connected attendee is found during the processing of the Neo4j query results

    with driver.session(database="appdbprojNeo4j") as session: # Creating a session with the Neo4j database using the driver instance, and specifying the database name "appdbprojNeo4j" to execute queries for finding connected attendees based on the specified attendee ID entered by the user in the visualization function for connected attendees
        query = """
        MATCH (a:Attendee {AttendeeID: $id})-[r:CONNECTED_TO]-(b:Attendee)
        RETURN b.AttendeeID AS connectedID
        """

        results = session.run(query, id=attendee_id) # Running the specified Cypher query in the Neo4j database using the session's run method, passing in the query string and a parameter dictionary containing the attendee ID (id) to find connected attendees based on this ID, and storing the results in the variable results for further processing to visualize the connections in a graph format using NetworkX and Matplotlib

        for record in results: # Iterating over each record in the results returned from the Neo4j query to extract the connected attendee ID and retrieve the corresponding attendee name from the MySQL database, and then adding nodes and edges to the graph for each connected attendee found in the Neo4j database based on the specified attendee ID entered by the user in the visualization function for connected attendees
            found_connection = True # Setting the found_connection variable to True if at least one connected attendee is found in the Neo4j database for the specified attendee ID entered by the user, indicating that there are connections to visualize in the graph
            connected_id = record["connectedID"] # Extracting the connected attendee ID from the current record in the results returned from the Neo4j query, by accessing the "connectedID" field in the record and storing it in the variable connected_id for use in retrieving the connected attendee's name from the MySQL database and adding nodes and edges to the graph for visualization

            cursor.execute( # Executing a SQL query to retrieve the name of the connected attendee with the specified connected attendee ID from the database, by selecting the attendeeName from the attendee table where the attendeeID matches the connected_id retrieved from the Neo4j query results
                "SELECT attendeeName FROM attendee WHERE attendeeID = %s", # Executing the SQL query to retrieve the name of the connected attendee from the database, by selecting the attendeeName from the attendee table where the attendeeID matches the connected_id retrieved from the Neo4j query results
                (connected_id,)
            )

            connected_attendee = cursor.fetchone() # Fetching the result of the executed query using the cursor's fetchone method, which returns a single tuple containing the connected attendee name if a matching record is found, or None if no matching record exists in the database for the specified connected attendee ID retrieved from the Neo4j query results

            if connected_attendee: # Checking if the connected_attendee variable is not None, which indicates that a matching record was found in the database for the specified connected attendee ID retrieved from the Neo4j query results
                connected_name = connected_attendee[0] # Storing the connected attendee name retrieved from the database in the variable connected_name for use in the graph visualization, by accessing the first element of the connected_attendee tuple (which is the connected attendee name) and assigning it to the variable connected_name for later use in labeling the graph nodes and providing context in the visualization of connected attendees
                graph.add_node(connected_name) # Adding a node to the graph for the connected attendee, using the connected attendee name retrieved from the database as the label for the node, which will be connected to the central node representing the specified attendee in the graph visualization of connected attendees based on the specified attendee ID entered by the user in the visualization function for connected attendees
                graph.add_edge(attendee_name, connected_name) # Adding an edge to the graph between the central node representing the specified attendee and the node representing the connected attendee, using the attendee name and connected attendee name as the labels for the nodes, which will visually represent the connection between the specified attendee and the connected attendees in the graph visualization based on the specified attendee ID entered by the user in the visualization function for connected attendees

    if not found_connection: # Checking if the found_connection variable is still False after processing the Neo4j query results, which indicates that no connected attendees were found in the Neo4j database for the specified attendee ID entered by the user, and therefore there are no connections to visualize in the graph
        messagebox.showinfo("No Connections", f"Attendee Name:{attendee_name}\nNo connections") # Displaying an information message box to the user if no connected attendees are found for the specified attendee ID, with the title "No Connections" and a message that includes the attendee name retrieved from the database and indicates that there are no connections for that attendee, and returning from the function to prevent further execution of the graph visualization logic since there are no connections to visualize
        return # Returning from the function if no connected attendees are found in the Neo4j database for the specified attendee ID entered by the user, preventing further execution of the graph visualization logic since there are no connections to visualize

    plt.figure(figsize=(8, 6)) # Creating a new figure for the graph visualization using Matplotlib, with a specified size of 8 inches in width and 6 inches in height to provide enough space for visualizing the connections between attendees in a clear and visually appealing manner based on the specified attendee ID entered by the user in the visualization function for connected attendees
    position = nx.spring_layout(graph) # Generating a layout for the graph visualization using NetworkX's spring_layout function, which positions the nodes in a way that visually represents the connections between them in a clear and aesthetically pleasing manner, based on the structure of the graph created from the connected attendees retrieved from the Neo4j database for the specified attendee ID entered by the user in the visualization function for connected attendees

    nx.draw( # Drawing the graph visualization using NetworkX's draw function, which takes the graph object, the generated layout for positioning the nodes, and various styling options for the nodes, edges, and labels to create a visually appealing representation of the connections between attendees based on the specified attendee ID entered by the user in the visualization function for connected attendees
        graph,
        position,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        edge_color="gray",
        font_size=10,
        font_weight="bold"
    )

    plt.title(f"Neo4j Connections for {attendee_name}") # Setting the title of the graph visualization to include the name of the attendee for whom connections are being displayed
    plt.show() # Displaying the graph visualization using Matplotlib's show function, which renders the graph in a new window for the user to view the connections between attendees based on the specified attendee ID entered by the user in the visualization function for connected attendees



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