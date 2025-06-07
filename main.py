import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from utils.file_utils import create_excel_from_csv, load_colleagues_from_excel, load_config
from model.openspace import Openspace


# === Define color codes ===
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def main() -> None:
    # Clear terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # File paths and config
    input_file = "problem-statement/collegues.csv"
    excel_file = "data/colleagues.xlsx"
    output_file = "data/output.csv"
    config = load_config()
    tables = config["tables"]
    seats_per_table = config["seats_per_table"]

    # Create Excel file from CSV
    create_excel_from_csv(input_file, excel_file)
    print(f"\n{BLUE}>>> Excel file created at: {excel_file}{RESET}")

    # Load names from Excel file
    names = load_colleagues_from_excel(excel_file)
    print(f"{BLUE}>>> Loaded {len(names)} names from: {excel_file}{RESET}\n")

    # Set up the room
    room = Openspace(tables, seats_per_table)
    print(f"{BLUE}>>> Assigning colleagues to seats...{RESET}\n")
    room.organize(names)

    # Display the seating arrangement (with lonely persons highlighted)
    room.display()

    
    # Manage and eliminate lonely persons at tables 
    
    if room.is_there_lonely_person():
        print(">>> Lonely persons detected. Eliminating lonely tables...\n")
        room.eliminate_lonely_tables()
        print(">>> Re-displaying seating arrangement after elimination:\n")
        room.display()
    else:
        print(">>> No lonely persons detected.\n")
    

    
    # Display number of remaining seats
    print(f"{BLUE}>>> {room.seats_left()} seats left in the room.{RESET}\n")

    print(f"\n{BLUE}>>> Saving seating plan to: {output_file}{RESET}\n")
    room.store(output_file)

    #Launch user interaction menu
    handle_user_choice(room)

    print(f"{GREEN}>>> Program completed successfully.{RESET}\n")


def display_menu() -> None:
    """
    Display the main interaction menu for the OpenSpace organizer.
    """
    print(BLUE + "\nOpenSpace Organizer Menu")
    print("1. Show current seating")
    print("2. Show number of seats / people / free spots")
    print("3. Add a new colleague")
    print("4. Add a new table")
    print("5. Save seating plan to Excel")
    print("6. Remove a table (must be empty)")
    print("7. Remove a person from the room")
    print("8. Remove a person from a specific table")
    print("9. Exit" + RESET)


def handle_user_choice(openspace: Openspace) -> None:
    """
    Handle the user's menu choices and trigger corresponding actions.
    """
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

    while True:
        display_menu()
        choice = input(BLUE + "\nSelect an option (1-9): " + RESET).strip()

        if choice == "1":
            openspace.display()

        elif choice == "2":
            print(f"Total seats: {sum(len(t.seats) for t in openspace.tables)}")
            print(f"People in room: {openspace.total_people_in_room()}")
            print(f"Free seats: {openspace.seats_left()}")

        elif choice == "3":
            name = input("Enter the new colleague's name: ").strip()
            success = openspace.assign_person(name)
            if not success:
                print(RED + "No available seat. Please add a new table first." + RESET)
            else:
                print(GREEN + f"{name} added to a table." + RESET)

        elif choice == "4":
            try:
                capacity = int(input("Enter number of seats for the new table: "))
                openspace.add_table(capacity)
                print(GREEN + "New table added." + RESET)
            except ValueError:
                print(RED + "Please enter a valid number." + RESET)


        elif choice == "5":
            filename_input = input(
                "Enter filename to save (e.g., 'seating' — '.xlsx' will be automatically added): "
            ).strip()

            if not filename_input:
                filename_input = "seating_plan"

            # Ensure data/ directory exists
            os.makedirs("data", exist_ok=True)

            # Construct full path with .xlsx extension
            full_path = os.path.join("data", f"{filename_input}.xlsx")

            openspace.store(full_path)
            print(GREEN + f"Seating plan saved to {os.path.abspath(full_path)}" + RESET)


        elif choice == "6":
            try:
                index = int(input("Enter the table number to remove (e.g., 3): "))
                success = openspace.remove_table(index)
                if not success:
                    print(RED + "Table could not be removed (either not empty or invalid index)." + RESET)
            except ValueError:
                print(RED + "Please enter a valid number." + RESET)

        elif choice == "7":
            name = input("Enter the name of the person to remove from the room: ").strip()
            success = openspace.remove_person_from_room(name)
            if success:
                print(f"{name} has been removed from their seat.")
                openspace.display()
                unseated = openspace.get_unseated_people()

            else:
                print(RED + "Person not found in the room." + RESET)

        elif choice == "8":
            try:
                table_index = int(input("Enter table number (e.g., 2): "))
                name = input("Enter the name of the person to remove: ").strip()
                success = openspace.remove_person_from_table(table_index, name)
                if success:
                    openspace.display()

                else:
                    print(RED + "Person not found at that table or invalid table number." + RESET)
            except ValueError:
                print(RED + "Please enter a valid table number." + RESET)

        elif choice == "9":
            print("Exiting!")
            break


if __name__ == "__main__":
    main()
