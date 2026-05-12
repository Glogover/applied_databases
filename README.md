# Applied Databases Project

*Please note that both the MySQL server and the Neo4j server must be running in order to run the application (main.py).*

## Overview

This project is a desktop-based Python application developed for the **Applied Databases** module.  
The application integrates both **MySQL** and **Neo4j** databases and provides a graphical user interface (GUI) using **Tkinter**.

The system allows users to:

- View conference speakers and sessions
- View attendees by company
- Add new attendees
- View attendee connections stored in Neo4j
- Add attendee connections
- View rooms
- Visualize graph relationships using NetworkX and Matplotlib
- Export query results to CSV files

The project demonstrates the practical integration of:

- Relational databases (MySQL)
- Graph databases (Neo4j)
- Python GUI development
- Data visualization
- CSV export functionality
- Database error handling

---

# Technologies Used

- Python
- MySQL
- Neo4j
- Tkinter
- NetworkX
- Matplotlib
- CSV
- Regular Expressions (re)

---

# Project Structure

```text
applied_databases/
│
├── main.py
├── dbconfig.py              # NOT pushed to GitHub (security reasons)
├── appdbproj.txt
├── appdbprojNeo4j.txt
├── requirements.txt
├── innovation.pdf
└── README.md
```

---

# Main Application

## `main.py`

The main Python application file.

This file contains:

- Database connections to MySQL and Neo4j
- Tkinter graphical user interface (GUI)
- SQL query execution
- Neo4j Cypher query execution
- CSV export functionality
- Graph visualization functionality
- Input validation
- Database error handling

### Main Functionalities

#### 1. View Speakers & Sessions
Allows users to search for speakers and display:
- Speaker names
- Session titles
- Room information

#### 2. View Attendees by Company
Displays attendees registered under a selected company together with:
- Session details
- Speaker details
- Room information

#### 3. Add New Attendee
Allows users to insert new attendees into the MySQL database.

Includes:
- Validation
- Foreign key checks
- Duplicate prevention
- Error handling

#### 4. View Connected Attendees
Uses Neo4j graph relationships to display attendee connections.

#### 5. Graph Visualization
Uses:
- NetworkX
- Matplotlib

to visualize Neo4j attendee relationships as interactive graphs.

#### 6. CSV Export
Allows exporting table data to CSV files directly from the GUI.

#### 7. Database Error Handling
Handles:
- MySQL connection failures
- Neo4j connection failures
- Invalid input errors
- Database integrity errors

---

# Configuration File

## `dbconfig.py`

Database configuration file used to store connection settings for:

- MySQL
- Neo4j

This file is intentionally **NOT included in the GitHub repository** for security reasons.

### Example Configuration

```python
mysql = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "********",
    "database": "appdbproj",
    "connection_timeout": 5,
    "use_pure": True
}

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "********"
NEO4J_DATABASE = "appdbprojneo4j"
```

---

# Database Files

## `appdbproj.txt`

MySQL database creation script.

This file contains:

- Database creation
- Table creation
- Primary keys
- Foreign keys
- Sample data inserts

### Main Tables

- `company`
- `attendee`
- `room`
- `session`
- `registration`

The database stores conference-related information including:
- attendees
- sessions
- rooms
- companies
- registrations

---

## `appdbprojNeo4j.txt`

Neo4j graph database script.

This file contains:
- Graph node creation
- Relationship creation
- Attendee networking data

### Graph Relationships

```cypher
(:Attendee)-[:CONNECTED_TO]->(:Attendee)
```

Used for:
- attendee networking
- graph visualization
- connection analysis

---

# Dependencies

## `requirements.txt`

Contains all Python package dependencies required to run the application.

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

# Additional Documentation

## `innovation.pdf`

Project documentation describing:

- Installation instructions
- Database configuration
- GUI enhancements
- CSV export functionality
- Neo4j graph visualization
- Error handling implementation

---

# Installation Guide

## 1. Install Python

Download Python from:

https://www.python.org/downloads/

During installation:
- Enable **"Add Python to PATH"**

---

## 2. Install Required Packages

Run:

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
python -m pip install mysql-connector-python
python -m pip install neo4j
python -m pip install networkx
python -m pip install matplotlib
```

---

# Database Setup

## MySQL Setup

1. Open MySQL
2. Run:

```sql
appdbproj.txt
```

This will create:
- database
- tables
- sample data

---

## Neo4j Setup

1. Open Neo4j Browser
2. Create a database named:

```text
appdbprojneo4j
```

3. Run:

```cypher
appdbprojNeo4j.txt
```

This will create:
- attendee nodes
- attendee relationships

---

# Running the Application

Run:

```bash
python main.py
```

The Tkinter GUI will open automatically.

---

# Features

## Tkinter GUI
- User-friendly graphical interface
- Popup windows
- Structured tables

## Treeview Tables
- Improved readability
- Scrollable query results

## Neo4j Graph Visualization
- Interactive relationship graphs
- Network visualization

## CSV Export
- Export query results
- Includes column headers

## Error Handling
- Prevents silent crashes
- Displays user-friendly messages

---


# References

## Python Documentation
- https://docs.python.org/3/

## Tkinter
- https://docs.python.org/3/library/tkinter.html
- https://docs.python.org/3/library/tkinter.ttk.html
- https://docs.python.org/3/library/tkinter.messagebox.html

## MySQL Connector
- https://www.w3schools.com/python/python_mysql_getstarted.asp
- https://dev.mysql.com/doc/connector-python/en/

## Neo4j
- https://neo4j.com/docs/python-manual/current/
- https://neo4j.com/docs/cypher-manual/current/

## NetworkX
- https://networkx.org/documentation/stable/

## Matplotlib
- https://matplotlib.org/stable/
- https://www.w3schools.com/python/matplotlib_intro.asp

## CSV Module
- https://docs.python.org/3/library/csv.html

---

# Author

**Marcin Kaminski**
  
Atlantic Technological University (ATU), Galway (Ireland)

