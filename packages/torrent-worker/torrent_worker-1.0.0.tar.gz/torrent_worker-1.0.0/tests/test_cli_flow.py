import sys
import unittest
from unittest.mock import patch

from torrent_worker import cli


class CliFlowTester(unittest.TestCase):
    """Test CLI flow."""

    @patch("torrent_worker.cli.prompt")
    def test_command_works(self, mock_prompt) -> None:
        """Test main CLI flow with mocked prompts."""

        def side_effect(msg: str) -> str:
            if "github" in msg:
                return "https://github.com/desonglll/zlibrary"
            if "downloads" in msg:
                return "./downloads"
            if "download all torrents?" in msg:
                return "y"
            raise ValueError(f"Unexpected prompt message: {msg}")

        mock_prompt.side_effect = side_effect
        sys.argv.append("--dry-run")
        cli.main()


if __name__ == "__main__":
    unittest.main()
