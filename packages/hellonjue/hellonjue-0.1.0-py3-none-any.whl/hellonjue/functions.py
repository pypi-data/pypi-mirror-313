"""
ascii_art_library.py

A simple Python library for generating and displaying ASCII art patterns.
"""

class ASCIIArt:
    """
    A class to generate and display various ASCII art patterns.
    """

    def __init__(self):
        """
        Initializes the ASCIIArt library.
        """
        pass

    @staticmethod
    def generate_pyramid(height: int) -> str:
        """
        Generates a pyramid pattern.

        Args:
            height (int): The height of the pyramid.

        Returns:
            str: The pyramid pattern as a string.
        """
        pyramid = ""
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            stars = "*" * (2 * i - 1)
            pyramid += spaces + stars + "\n"
        return pyramid

    @staticmethod
    def generate_diamond(size: int) -> str:
        """
        Generates a diamond pattern.

        Args:
            size (int): The size of the diamond (half the height).

        Returns:
            str: The diamond pattern as a string.
        """
        diamond = ""
        # Top half
        for i in range(1, size + 1):
            spaces = " " * (size - i)
            stars = "*" * (2 * i - 1)
            diamond += spaces + stars + "\n"
        # Bottom half
        for i in range(size - 1, 0, -1):
            spaces = " " * (size - i)
            stars = "*" * (2 * i - 1)
            diamond += spaces + stars + "\n"
        return diamond

    @staticmethod
    def generate_spiral(size: int) -> str:
        """
        Generates a simple ASCII spiral pattern.

        Args:
            size (int): The size of the spiral (side length).

        Returns:
            str: The spiral pattern as a string.
        """
        grid = [[" " for _ in range(size)] for _ in range(size)]
        x, y = 0, 0
        dx, dy = 0, 1  # Start direction: right
        for i in range(1, size * size + 1):
            grid[x][y] = str(i % 10)
            if grid[(x + dx) % size][(y + dy) % size] != " ":
                dx, dy = dy, -dx  # Change direction
            x += dx
            y += dy
        return "\n".join("".join(row) for row in grid)

    @staticmethod
    def display_pattern(pattern: str) -> None:
        """
        Displays the given ASCII art pattern.

        Args:
            pattern (str): The ASCII art pattern to display.
        """
        print(pattern)


if __name__ == "__main__":
    # Example usage of the library
    art = ASCIIArt()

    print("Pyramid:")
    pyramid = art.generate_pyramid(5)
    art.display_pattern(pyramid)

    print("\nDiamond:")
    diamond = art.generate_diamond(5)
    art.display_pattern(diamond)

    print("\nSpiral:")
    spiral = art.generate_spiral(5)
    art.display_pattern(spiral)
