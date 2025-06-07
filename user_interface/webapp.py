"""
webapp.py – Flask Web Application Entry Point for OpenSpace Seating Management

Location:
---------
Located in: user_interface/webapp.py  
Executed via: root script ./run-web.sh

Description:
------------
This file defines the Flask web application used to interact with the OpenSpace seating tool.
It acts as a controller between user-uploaded data (Excel files) and the backend logic implemented
in the Openspace, Table, and Seat classes under the 'model' package.

Purpose:
--------
This application allows users to:
- Upload an Excel file containing a list of colleagues
- Automatically organize individuals into tables and seats based on configurable parameters
- Avoid lonely seating when possible using redistribution logic
- Visualize the seating plan in a browser-friendly format (via Jinja templates)
- Download the result as a CSV file, if generated

Key Features Used from Backend Classes:
---------------------------------------
- Dynamic seat assignment: Openspace.assign_person()
- Grouping logic to reduce lonely seating: Openspace.eliminate_lonely_tables()
- Detection of unseated individuals: Openspace.get_unseated_people()
- Configuration-driven setup: JSON file loaded via utils.file_utils.load_config()
- Storage support for exporting the result: Openspace.store()

Flask Routes:
-------------
- '/'         → Renders the HTML upload form (templates/upload.html)
- '/upload'   → Handles Excel upload, runs seat assignment, and renders the result page (templates/result.html)
- '/download' → (Optional) Serves a generated CSV file (data/output.csv)

Execution Flow:
---------------
1. The user runs `run-web.sh` from the root project directory.
2. The Flask app (`webapp.py`) is launched in development mode.
3. The user accesses `http://127.0.0.1:5000` in a browser.
4. The user uploads a `.xlsx` file containing names.
5. Flask:
   - Saves the file in the 'uploads/' directory
   - Loads configuration from 'config.json'
   - Initializes an Openspace object and organizes seating
   - Eliminates lonely seating where possible
   - Displays the final layout in the browser
6. The user can optionally download the seating plan as a CSV file

Usage:
------
To run the web application:
>>> ./run-web.sh

Make sure dependencies are installed using:
>>> pip install -r requirements.txt
"""


import os
import sys


from utils.file_utils import load_colleagues_from_excel
from model.openspace import Openspace
from flask import Flask, request, render_template, redirect, url_for, send_file
from utils.file_utils import load_config

from flask import send_file
from io import BytesIO
import pandas as pd

global room


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = Flask(__name__)

# Global variable to hold the Openspace instance
global room

# Folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#
@app.route('/', methods=['GET'])
def index():
    """
    Render the upload page.
    """
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle the uploaded Excel file:
    - Save the file to the uploads folder
    - Load names and configuration
    - Initialize the Openspace object
    - Organize seating and eliminate lonely seats
    - Redirect to the interactive dashboard
    """
    global room

    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    if file and file.filename.endswith('.xlsx'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        names = load_colleagues_from_excel(filepath)
        config = load_config()
        tables = config.get("tables", 6)
        seats_per_table = config.get("seats_per_table", 4)

        room = Openspace(tables, seats_per_table)
        room.organize(names)

        #if room.is_there_lonely_person():
        #    room.eliminate_lonely_tables()

        return redirect(url_for('dashboard'))

    return "Invalid file format. Please upload an .xlsx file.", 400

    

@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard page showing all tables and current seating status.
    Also displays unassigned people and controls for adding/removing.
    """
    global room
    if not room:
        return redirect(url_for('index'))

    tables_data = []
    for i, table in enumerate(room.tables, start=1):
        seats = [(idx + 1, seat.occupant if not seat.free else "Free") for idx, seat in enumerate(table.seats)]
        tables_data.append({"table_num": i, "seats": seats})

    unseated = room.get_unseated_people()
    return render_template('dashboard.html', tables=tables_data, unseated=unseated)



@app.route('/add_person', methods=['POST'])
def add_person():
    """
    Add a person to the unassigned list without assigning them to a table.
    """
    global room
    name = request.form.get('name')
    if room and name:
        if not room.is_person_seated(name) and name not in room.unassigned:
            room.unassigned.append(name)
            print(f"{name} has been added to the unassigned list.")
    return redirect(url_for('dashboard'))



@app.route('/remove_person_from_table/<int:table_id>/<name>')
def remove_person_from_table(table_id, name):
    """
    Remove a person from a table and add them to the unassigned list.
    """
    global room
    if room:
        room.remove_person_from_table(table_id, name)
        if name not in room.unassigned:
            room.unassigned.append(name)  # Re-add to unassigned
            print(f"{name} was removed from table {table_id} and added to the unassigned list.")
    return redirect(url_for('dashboard'))

@app.route('/remove_person_from_room/<name>')
def remove_person_from_room(name):
    """
    Completely remove a person from the room, whether seated or unassigned.
    The person is removed from any table and also from the unassigned list.
    """
    global room
    if room:
        room.remove_person_from_room(name)
    return redirect(url_for('dashboard'))

@app.route('/add_table', methods=['POST'])
def add_table():
    """
    Add a new table to the openspace with specified capacity.
    Capacity is taken from the form; default is 4 if not specified.
    """
    global room
    capacity = int(request.form.get('capacity', 4))
    if room:
        room.add_table(capacity)
    return redirect(url_for('dashboard'))


@app.route('/remove_table/<int:index>')
def remove_table(index):
    """
    Remove a table from the openspace if it is empty.
    Index is 1-based, as shown to the user.
    """
    global room
    if room:
        room.remove_table(index)
    return redirect(url_for('dashboard'))


@app.route('/download')
def download():
    """
    Allow downloading the output CSV file if implemented.
    """
    output_path = 'data/output.csv'
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return "No output file available.", 404


@app.route('/store_csv')
def store_csv():
    """
    Export the current seating plan to an Excel file (XLSX) and send it as a download.
    """
    global room
    if not room:
        return "No seating data to export.", 400

    rows = []

    # Collect seating information from all tables
    for table_index, table in enumerate(room.tables, start=1):
        for seat_number, seat in enumerate(table.seats, start=1):
            if seat.occupant and seat.occupant != "Free":
                rows.append({
                    "Table": table_index,
                    "Seat": seat_number,
                    "Name": seat.occupant
                })

    # Create a DataFrame with the seating data
    df = pd.DataFrame(rows)

    # Export to Excel in-memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Seating')
    output.seek(0)

    # Send file as a downloadable Excel attachment
    return send_file(
        output,
        as_attachment=True,
        download_name='seating_plan.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@app.route('/assign_to_table', methods=['POST'])
def assign_to_table():
    """
    Assign a specific person to a specific table manually.
    """
    global room
    name = request.form.get('name')
    table_index = int(request.form.get('table_index'))

    if room and name and 1 <= table_index <= len(room.tables):
        table = room.tables[table_index - 1]
        success = table.assign_seat(name)
        if success:
            if name in room.unassigned:
                room.unassigned.remove(name)
            print(f"{name} has been manually assigned to table {table_index}.")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Run Flask app in debug mode for development
    app.run(debug=True)
