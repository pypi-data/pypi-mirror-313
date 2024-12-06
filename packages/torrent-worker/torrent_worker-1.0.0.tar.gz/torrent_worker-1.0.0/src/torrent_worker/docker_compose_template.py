from jinja2 import Template

TEMPLATE = Template(
    """

services:
  qbittorrent:
    privileged: true
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/Chicago
      - WEBUI_PORT=8080
      - TORRENTING_PORT=6881
    volumes:
      - {{ appdata_path }}:/config
      - {{ downloads_path }}:/downloads #optional
    ports:
      - 8080:8080
      - 6881:6881
      - 6881:6881/udp
    restart: unless-stopped

  fileserver:
    image: nginx:alpine
    container_name: fileserver
    volumes:
      - {{ torrents_path }}:/usr/share/nginx/html:ro
    ports:
      - "8081:80"
    restart: unless-stopped
"""
)


def render_template(
    appdata_path: str = "./bittorrent/appdata",
    downloads_path: str = "./bittorrent/downloads",
    torrents_path: str = "./bittorrent/torrents",
) -> str:
    """Render the docker-compose template with the given parameters."""
    return TEMPLATE.render(
        appdata_path=appdata_path,
        downloads_path=downloads_path,
        torrents_path=torrents_path,
    )
