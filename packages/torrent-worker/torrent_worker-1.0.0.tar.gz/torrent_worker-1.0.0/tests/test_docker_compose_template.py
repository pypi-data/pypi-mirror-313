import unittest

from torrent_worker.docker_compose_template import render_template


class DockerComposeTemplateTester(unittest.TestCase):
    """Test the docker compose template rendering."""

    def test_render_with_default_values(self) -> None:
        """Test that rendering with default values produces expected output."""
        result = render_template()
        # Check that default values are present in the rendered template
        self.assertIn("WEBUI_PORT=8080", result)
        self.assertIn("- 8080:8080", result)
        self.assertIn("- 6881:6881", result)
        self.assertIn("- 6881:6881/udp", result)
        self.assertIn('- "8081:80"', result)
        self.assertIn("- ./bittorrent/appdata:/config", result)
        self.assertIn("- ./bittorrent/downloads:/downloads", result)
        self.assertIn("- ./bittorrent/torrents:/usr/share/nginx/html:ro", result)

    def test_render_with_custom_values(self) -> None:
        """Test that rendering with custom values produces expected output."""
        result = render_template(
            appdata_path="/custom/appdata",
            downloads_path="/custom/downloads",
            torrents_path="/custom/torrents",
        )
        self.assertIn("- /custom/appdata:/config", result)
        self.assertIn("- /custom/downloads:/downloads", result)
        self.assertIn("- /custom/torrents:/usr/share/nginx/html:ro", result)


if __name__ == "__main__":
    unittest.main()
