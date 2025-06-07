# Openspace Project

## Prerequisites

Before running this project, ensure that Python 3.12.10 is installed on your system.

- You can download Python 3.12.10 from the official website:  
https://www.python.org/downloads/release/python-31210/

- Make sure the `python.exe` path is added to your system environment variables (`PATH`) so it can be accessed via terminal:
-  On Windows, this is typically located at:  
`C:\Users\<YourUserName>\AppData\Local\Programs\Python\Python312\python.exe`

> ⚠️ This project is configured to create a virtual environment using Python 3.12.10. Other versions may lead to compatibility issues.

## Python Environment Setup

This project uses a **virtual environment** to manage Python dependencies in isolation from your system installation.  
This is done using the `.venv/` folder, which contains a local version of Python and all required packages for the project.

> **Why use a virtual environment?**  
> It ensures:
> - Your project runs with the exact versions of libraries it needs.
> - No conflicts with other Python projects or your system installation.
> - Clean and reproducible development environments.

### Step-by-step setup

To initialize the Python environment for this project, follow these steps:

1. **Open a Bash-compatible terminal**  
   Use Git Bash (recommended on Windows) or WSL if you're on Linux/macOS.

2. **Make the setup script executable**  
   Run the following command once to make the script executable:
   ```bash
   chmod +x setup-env.sh
   ```

3. **Run the setup script**
   ```bash
   ./setup-env.sh
   ```

This script will:
- Remove any existing `.venv/` folder.
- Create a new virtual environment using **Python 3.12.10**.
- Automatically activate the environment.
- Upgrade `pip`.
- Install all required packages from `requirements.txt`.
- Create a new `.venv/` folder in the project root to isolate dependencies.

> After those steps, your environment is fully set up and ready for development or testing.

## Running the Application

You can run this project in two different modes depending on your use case:

- **Command-line interface (CLI)** — for quick testing or automation
- **Web interface** — for a more user-friendly experience via a browser

### Run the main.py in the shell
To start the main.py from your Git Bash terminal in Visual Studio Code, execute:

1. **Make the setup script executable** 
    ```bash
    chmod +x run-main.sh
    ```

2. **Run the setup script**
   ```bash
   ./run-main.sh
   ```

This will:

- Activate the Python virtual environment
- Launch main.py
- Load the Excel file (data/colleagues.xlsx)
- Assign people to tables and seats
- Save the output to data/output.csv
- Display any unseated persons in the terminal

### Run the Web Inerface

To start the web application from your Git Bash terminal in Visual Studio Code, execute:

1. **Make the setup script executable** 
    ```bash
    chmod +x run-web.sh
    ```

2. **Run the setup script**
   ```bash
   ./run-web.sh
   ```
Then open your browser and navigate to:
   ```bash
   http://127.0.0.1:5000
   ```
From there you can:
- Upload a .xlsx file with names (in data folder, use **colleagues.xlsx** file)
- View the seating arrangement by table and seat
- Download the output as a .csv file
- Re-upload another file for a new plan

>The web mode uses the config.json file to determine parameters like number of tables and seats per table.

### Dynamic Configuration via config.json
The program automatically reads its setup from a `config.json` file located in the project root. This allows you to easily configure the room layout and input/output paths without modifying the Python code.

Example content of `config.json`:

```json
{
  "input_csv": "data/colleagues.xlsx",
  "output_csv": "data/output.csv",
  "output_excel": "data/colleagues.xlsx",
  "tables": 6,
  "seats_per_table": 4
}
```

### Parameter Breakdown

- **`input_csv`** *(string)*  
  Path to the Excel file that contains the list of colleagues. This file will be used to load the names to assign.

- **`output_csv`** *(string)*  
  Path where the program will write the final seating arrangement as a `.csv` file. Useful for external sharing or historical tracking.

- **`output_excel`** *(string)*  
  *(Optional)* If present, the program will also export the final seating arrangement to an Excel file at this location.

- **`tables`** *(integer)*  
  Number of tables available in the open space. For example, `6` tables.

- **`seats_per_table`** *(integer)*  
  Number of seats per table. For example, `4` seats per table means a total capacity of 24 people.

*By editing this file, you can adapt the room layout and input/output behavior without changing a single line of Python code.*


## Feature Implementation Checklist

| Feature Category            | Feature Description                                                                                      | Status      |
|-----------------------------|----------------------------------------------------------------------------------------------------------|-------------|
| **Core Logic**              | Load colleagues from Excel file                                                                          | ✅ Done     |
|                             | Randomly assign colleagues to available seats                                                            | ✅ Done     |
|                             | Show number of seats left                                                                                | ✅ Done     |
|                             | Handle case with too many people                                                                         | ✅ Done     |
| **OOP & Architecture**      | Use clean OOP structure (Seat, Table, Openspace classes)                                                 | ✅ Done     |
|                             | Add proper typing for all methods                                                                        | ✅ Done     |
|                             | Include docstrings in every function/class                                                               | ✅ Done     |
|                             | Use proper import statements                                                                             | ✅ Done     |
|                             | Clean architecture with modular folders                                                                  | ✅ Done     |
| **Basic CLI Features**      | Display tables and occupants                                                                             | ✅ Done     |
|                             | Save seating plan to `.csv`                                                                              | ✅ Done     |
| **Advanced CLI Features**   | Add new colleague dynamically                                                                            | ✅ Done     |
|                             | Add new table dynamically                                                                                | ✅ Done     |
|                             | Remove a colleague from a table or room                                                                  | ✅ Done     |
|                             | Prevent lonely people at a table (eliminate lonely tables)                                               | ✅ Done     |
|                             | Show number of people, free seats, and total capacity                                                    | ✅ Done     |
| **Config Support**          | Use `config.json` to dynamically configure number of tables/seats                                        | ✅ Done     |
| **Web Interface**           | Upload Excel file via web form                                                                           | ✅ Done     |
|                             | Display seating plan in HTML                                                                             | ✅ Done     |
|                             | Allow download of result `.csv` from browser                                                             | ✅ Done     |
|                             | Use Flask web server                                                                                     | ✅ Done     |
| **UI Features (HTML)**      | Display tables and seats clearly                                                                         | ✅ Done     |
|                             | Show unseated colleagues (if any)                                                                        | ✅ Done     |
|                             | Allow uploading another file                                                                             | ✅ Done     |
| **Bonus Features (Not Yet)**| Use blacklist/whitelist seating preferences from Excel (e.g., X wants to sit next to Y)                  | ❌ Not done |
|                             | More advanced UI interaction (e.g., drag/drop seats)                                                     | ❌ Not done |
|                             | Dynamic seat/table reordering from UI                                                                    | ❌ Not done |
| **Code Quality & Git**      | Black formatting                                                                                         | ✅ Done     |
|                             | Remove unused code and comments                                                                          | ✅ Done     |
|                             | Proper GitHub repo setup                                                                                 | ✅ Done     |
|                             | Git feature branching & PRs (if in team)                                                                 | ✅ Done     |
|                             | README file with structure and visuals                                                                   | ✅ Done     |



