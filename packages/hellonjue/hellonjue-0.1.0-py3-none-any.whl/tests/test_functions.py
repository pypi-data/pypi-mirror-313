import unittest
from hellonjue import ASCIIArt
from unittest.mock import patch
from io import StringIO
class TestASCIIArt(unittest.TestCase):
    """
    Unit tests for the ASCIIArt library.
    """

    def setUp(self):
        """
        Sets up an instance of the ASCIIArt class for testing.
        """
        self.art = ASCIIArt()

    def test_generate_pyramid(self):
        """
        Tests the generate_pyramid method with a specific height.
        """
        expected_output = (
            "    *\n"
            "   ***\n"
            "  *****\n"
            " *******\n"
            "*********\n"
        )
        self.assertEqual(self.art.generate_pyramid(5), expected_output)

    def test_generate_diamond(self):
        """
        Tests the generate_diamond method with a specific size.
        """
        expected_output = (
            "    *\n"
            "   ***\n"
            "  *****\n"
            " *******\n"
            "*********\n"
            " *******\n"
            "  *****\n"
            "   ***\n"
            "    *\n"
        )
        self.assertEqual(self.art.generate_diamond(5), expected_output)

    def generate_spiral(self, size: int) -> str:
        matrix = [[0] * size for _ in range(size)]
        num = 1
        top, left = 0, 0
        bottom, right = size - 1, size - 1

        while top <= bottom and left <= right:
            for i in range(left, right + 1):
                matrix[top][i] = num
                num += 1
            top += 1
            for i in range(top, bottom + 1):
                matrix[i][right] = num
                num += 1
            right -= 1
            for i in range(right, left - 1, -1):
                matrix[bottom][i] = num
                num += 1
            bottom -= 1
            for i in range(bottom, top - 1, -1):
                matrix[i][left] = num
                num += 1
            left += 1

        return "\n".join("".join(f"{x or ' '}" for x in row) for row in matrix)

    def test_display_pattern(self):
        """
        Tests the display_pattern method to ensure it prints correctly.
        """
        pattern = "*\n**\n***\n"
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.art.display_pattern(pattern)
            self.assertEqual(mock_stdout.getvalue().strip(), pattern.strip())

if __name__ == "__main__":
    unittest.main()
