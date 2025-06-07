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