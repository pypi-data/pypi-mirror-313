import os
import unittest

COMMAND = "torrent-worker --help"


class CliTester(unittest.TestCase):
    """Example tester."""

    def test_command_works(self) -> None:
        """Example tester."""
        rtn = os.system(COMMAND)
        self.assertEqual(rtn, 0)


if __name__ == "__main__":
    unittest.main()
