import random
from typing import List
from model.table import Table



class Openspace:
    def __init__(self, number_of_tables: int, table_capacity: int) -> None:
        # Create tables based on the given configuration
        self.number_of_tables: int = number_of_tables
        self.tables: List[Table] = [Table(table_capacity) for _ in range(number_of_tables)]
        self.unassigned: List[str] = []
        self.to_group: List[str] = []
        self.sat_alone: List[str] = []


    def organize(self, names: List[str]) -> None:
        """
        Randomly assign each person using assign_person().
        Unassigned people are stored in self.unassigned.
        """
        random.shuffle(names)
        self.unassigned = []
        self.sat_alone = []

        for name in names:
            if not self.assign_person(name):
                self.unassigned.append(name)

        # If there are people in self.to_group, try to assign them to empty tables
        if self.to_group:
            tables_empty = [t for t in self.tables if all(seat.free for seat in t.seats)]
            group_index = 0
            i = 0

            while i < len(self.to_group) and group_index < len(tables_empty):
                table = tables_empty[group_index]
                seats = table.seats
                for seat in seats:
                    if i >= len(self.to_group):
                        break
                    seat.set_occupant(self.to_group[i])
                    i += 1
                group_index += 1

        if i < len(self.to_group):
            for name in self.to_group[i:]:
                if name not in self.unassigned:
                    self.unassigned.append(name)

            self.to_group = []

        # Analyse finale : personnes seules
        self.sat_alone = []
        for table in self.tables:
            occupants = [seat.occupant for seat in table.seats if not seat.free]
            if len(occupants) == 1:
                self.sat_alone.append(occupants[0])

        # Affichage final propre
        print("\n>>> Assigning colleagues to seats...")

        if self.sat_alone:
            print("\n>>> The following people had to sit alone (no other option):")
            for name in self.sat_alone:
                print(f" - {name}")
        else:
            print("\n>>> No lonely persons detected.")

        free_seats = self.seats_left()
        print(f"\n>>> {free_seats} seat{'s' if free_seats != 1 else ''} left in the room.")

        # Nettoyage des noms déjà assis
        self.unassigned = [name for name in self.unassigned if not self.is_person_seated(name)]

        if self.unassigned:
            print("\n>>> Could not assign the following people (no available seats):")
            for name in self.unassigned:
                print(f" - {name}")



    def display(self) -> None:
        """
        Print the seating arrangement.
        """
        for index, table in enumerate(self.tables, start=1):
            print(f"Table {index}:")
            for seat_index, seat in enumerate(table.seats, start=1):
                status = seat.occupant if not seat.free else "Free"
                print(f"  Seat {seat_index}: {status}")
            
            occupants = [seat.occupant for seat in table.seats if not seat.free]
            if len(occupants) == 1:
                print(f"> Note: {occupants[0]} is sitting alone at this table.")

            print("")

        # Ajoute ceci à la fin pour afficher les personnes non assises
        unseated = self.get_unseated_people()
        if unseated:
            print(">>> The following person(s) are not currently seated:")
            for name in unseated:
                print(f" - {name}")

    def store(self, filename: str) -> None:
        """
        Save the current seating plan to a CSV file.

        :param filename: Output file path
        """
        import csv
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Table', 'Seat', 'Occupant'])

            for table_index, table in enumerate(self.tables, start=1):
                for seat_index, seat in enumerate(table.seats, start=1):
                    writer.writerow([table_index, seat_index, seat.occupant if not seat.free else "Free"])

    def seats_left(self) -> int:
        """
        Calculate the total number of free seats in the openspace.

        :return: Number of unoccupied seats
        """
        return sum(table.left_capacity() for table in self.tables)

    def is_there_lonely_person(self) -> bool:
        """
        Check if at least one table has exactly one person sitting alone.
        """
        for table in self.tables:
            occupied = [seat for seat in table.seats if not seat.free]
            if len(occupied) == 1:
                return True
        return False

    # Remove lonely people from tables and redistribute them to other tables    
    # In the 'assign_person', new people are only added to tables that already 
    # have at least one occupant, if possible
    def eliminate_lonely_tables(self) -> None:
        """
        Redistribute individuals sitting alone to other tables with free seats.
        Ensures no one is left sitting alone.
        """
        lonely_tables = []
        receiving_tables = []

        for table in self.tables:
            occupied = [seat for seat in table.seats if not seat.free]
            free = [seat for seat in table.seats if seat.free]

            if len(occupied) == 1:
                lonely_tables.append((table, occupied[0]))  # table + lone seat
            elif len(free) >= 1:
                receiving_tables.append(table)

        for _, lonely_seat in lonely_tables:
            lonely_person = lonely_seat.occupant

            for target_table in receiving_tables:
                for seat in target_table.seats:
                    if seat.free:
                        # Reassign person
                        seat.occupant = lonely_person
                        seat.free = False

                        # Free old seat
                        lonely_seat.occupant = None
                        lonely_seat.free = True

                        print(f"{lonely_person} was moved from a lonely table to a new table.")
                        break
                else:
                    continue
                break

    
    def assign_person(self, name: str) -> bool:
        """
        Assign a person to a non-empty table with free seats if possible.
        Avoid placing someone alone unless no other option exists.

        :param name: The name of the person to assign
        :return: True if assigned, False otherwise
        """
        preferred_tables = []
        fallback_tables = []

        for table in self.tables:
            if table.has_free_spot():
                occupied_count = sum(1 for seat in table.seats if not seat.free)
                if occupied_count >= 1:
                    preferred_tables.append(table)
                else:
                    fallback_tables.append(table)

        for table in preferred_tables:
            if table.assign_seat(name):
                return True

        for table in fallback_tables:
            self.to_group.append(name)
            return False

        return False

    
    def add_table(self, capacity: int) -> None:
        """
        Add a new table with the specified capacity.
        Does not automatically assign any unseated people.
        """
        from model.table import Table
        new_table = Table(capacity)
        self.tables.append(new_table)
        self.number_of_tables += 1
        print(f"New table with {capacity} seats added. No one has been assigned automatically.")


    def remove_table(self, index: int) -> bool:
        """
        Remove a table from the openspace if it is empty.

        :param index: Index of the table to remove (1-based index as seen by user)
        :return: True if table removed, False if not empty or invalid index
        """
        if 1 <= index <= len(self.tables):
            table = self.tables[index - 1]
            if all(seat.free for seat in table.seats):
                del self.tables[index - 1]
                self.number_of_tables -= 1
                print(f"Table {index} has been removed.")
                return True
            else:
                print(f"Table {index} is not empty and cannot be removed.")
                return False
        else:
            print(f"Invalid table number: {index}")
            return False

    def remove_person_from_table(self, table_index: int, name: str) -> bool:
        """
        Remove a person from a specific table.

        :param table_index: Index of the table (1-based)
        :param name: Name of the person to remove
        :return: True if removed successfully, False if not found or invalid table
        """
        if 1 <= table_index <= len(self.tables):
            table = self.tables[table_index - 1]
            for seat in table.seats:
                if seat.occupant == name:
                    seat.remove_occupant()
                    self.unassigned.append(name)
                    print(f"{name} has been removed from Table {table_index}.")
                    return True
            print(f"{name} not found at Table {table_index}.")
            return False
        else:
            print(f"Invalid table number: {table_index}")
            return False
        
    def remove_person_from_room(self, name: str) -> bool:
        """
        Completely remove a person from the room, whether seated or unassigned.

        :param name: Name of the person to remove
        :return: True if the person was removed, False otherwise
        """        
        #1. Frtst check if they are seated at a table
        for table in self.tables:
            for seat in table.seats:
                if seat.occupant == name:
                    seat.remove_occupant()
                    print(f"{name} has been removed from their seat.")
                    return True

        # 2. Then, check if they are in the unassigned list
        if name in self.unassigned:
            self.unassigned.remove(name)
            print(f"{name} was not seated but has been removed from the room.")
            return True

        return False  # Not faund in either case

    def get_unseated_people(self) -> List[str]:
        """
        Return a list of all people not seated at any table.
        """
        seated = {seat.occupant for table in self.tables for seat in table.seats if seat.occupant}
        all = set(seated).union(set(self.unassigned))  # inclut ceux encore en self.unassigned
        return list(set(self.unassigned + [name for name in seated if not self.is_person_seated(name)]))

    def is_person_seated(self, name: str) -> bool:
        """
        Check if a person is currently seated at a table.
        """
        for table in self.tables:
            for seat in table.seats:
                if seat.occupant == name:
                    return True
        return False

    def total_people_in_room(self) -> int:
        seated = {seat.occupant for table in self.tables for seat in table.seats if seat.occupant}
        return len(seated.union(self.unassigned))

    def __str__(self) -> str:
        return f"Openspace with {self.number_of_tables} tables"
