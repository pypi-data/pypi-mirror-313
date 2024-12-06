import unittest

from torrent_worker.paths import PROJECT_ROOT


class PathTester(unittest.TestCase):
    """Example tester."""

    def test_command_works(self) -> None:
        """Example tester."""
        print(PROJECT_ROOT)
        pyproject = PROJECT_ROOT / "pyproject.toml"
        self.assertTrue(pyproject.exists())


if __name__ == "__main__":
    unittest.main()
