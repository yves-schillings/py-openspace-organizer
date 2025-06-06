from typing import List

# Note: Both Seat and Table are defined here as per challenge instructions.
# For better structure, each class should ideally be in its own file.

class Seat:
    def __init__(self) -> None:
        # Seat is initially free and unoccupied
        self.free: bool = True
        self.occupant: str = ""

    def set_occupant(self, name: str) -> bool:
        """
        Assign someone to the seat if it's free.

        :param name: Person to assign
        :return: True if successful, False otherwise
        """
        if self.free:
            self.occupant = name
            self.free = False
            return True
        return False

    def remove_occupant(self) -> str:
        """
        Remove the current occupant.

        :return: Name of the removed occupant
        """
        name = self.occupant
        self.occupant = ""
        self.free = True
        return name

    def __str__(self) -> str:
        return self.occupant if not self.free else "Free"


class Table:
    def __init__(self, capacity: int) -> None:
        # Table with a fixed number of seats
        self.capacity: int = capacity
        self.seats: List[Seat] = [Seat() for _ in range(capacity)]

    def has_free_spot(self) -> bool:
        """
        Check if at least one seat is available.

        :return: True if a seat is free
        """
        return any(seat.free for seat in self.seats)

    def assign_seat(self, name: str) -> bool:
        """
        Place someone at the first available seat.

        :param name: Person to assign
        :return: True if assigned, False if full
        """
        for seat in self.seats:
            if seat.set_occupant(name):
                return True
        return False

    def left_capacity(self) -> int:
        """
        Count the number of available seats.

        :return: Number of free seats
        """
        return sum(1 for seat in self.seats if seat.free)

    def __str__(self) -> str:
        seat_list = ", ".join(str(seat) for seat in self.seats)
        return f"Table ({self.capacity}): {seat_list}"
