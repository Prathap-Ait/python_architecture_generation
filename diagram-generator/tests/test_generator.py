import unittest
from src.diagram.generator import create_diagram

class TestDiagramGenerator(unittest.TestCase):

    def test_create_diagram(self):
        # Dummy test to check if create_diagram returns a non-empty output
        output = create_diagram()
        self.assertIsNotNone(output)
        self.assertNotEqual(output, "")

if __name__ == '__main__':
    unittest.main()