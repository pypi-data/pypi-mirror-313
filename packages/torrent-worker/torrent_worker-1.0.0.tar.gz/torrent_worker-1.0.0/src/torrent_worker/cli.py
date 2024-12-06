import argparse
import os
import shutil
import time
from pathlib import Path
from threading import Event, Thread

import requests  # type: ignore

# BittorrentClient
from torrent_worker.client import BittorrentClient
from torrent_worker.config import Config
from torrent_worker.docker_compose_template import render_template
from torrent_worker.github_downloader import clone_or_update
from torrent_worker.paths import PROJECT_ROOT
from torrent_worker.qbittorrent_conf import CONFIG_FILE as qbittorrent_conf


def prompt(msg: str) -> str:
    """Prompt user for input."""
    return input(msg.strip() + " ").strip()


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Torrent worker.")
    parser.add_argument("--downloads", help="Directory where downloads are stored.")
    parser.add_argument(
        "--torrents-source", help="GitHub repo URL or file path containing torrents"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the command without making any changes",
    )
    parser.add_argument(
        "--range",
        help="Range of torrents to download (e.g. 0-10), default is to download all",
    )
    parser.add_argument(
        "--cancel",
        action="store_true",
        help="Cancel the current operation and exit",
    )
    parser.add_argument(
        "--attach",
        action="store_true",
        help="Attaches to the current running instance.",
    )
    return parser.parse_args()


def _get_valid_directory(
    arg_value: str | None, config_key: str, prompt_message: str, config: Config
) -> str:
    """
    Get a valid directory path, trying arg first, then config, then user input.

    Args:
        arg_value: Value from command line argument
        config_key: Key to use in config dictionary
        prompt_message: Message to show user when prompting
        config: Config instance

    Returns:
        Valid directory path as string
    """
    # Try argument first if provided
    if arg_value:
        if not Path(arg_value).exists():
            print(f"Warning: Provided directory {arg_value} does not exist.")
            arg_value = None
        else:
            if config_key == Config.KEY_DOWNLOAD:
                config.download_dir = arg_value
            return arg_value

    # Try config value if it exists
    config_value = config.download_dir if config_key == Config.KEY_DOWNLOAD else None
    if config_value and Path(config_value).exists():
        return config_value

    # Ask user for input until valid
    while True:
        user_input = prompt(prompt_message).strip()
        if not user_input:
            print("Directory path cannot be empty.")
            continue

        if not Path(user_input).exists():
            Path(user_input).mkdir(parents=True, exist_ok=True)
            # print(f"Directory {user_input} does not exist. Please try again.")
            # continue

        if config_key == Config.KEY_DOWNLOAD:
            config.download_dir = user_input
        return user_input


def _get_valid_torrents_source(arg_value: str | None, config: Config) -> str:
    """
    Get a valid torrents source (GitHub URL or file path).

    Args:
        arg_value: Value from command line argument
        config: Config instance

    Returns:
        Valid torrents source as string
    """
    # Try argument first if provided
    if arg_value:
        config.torrents_source = arg_value
        return arg_value

    # Try config value if it exists
    config_value = config.torrents_source
    if config_value:
        return config_value

    # Ask user for input
    while True:
        user_input = prompt(
            "Enter GitHub repo URL or file path containing torrents:"
        ).strip()
        if not user_input:
            print("Torrents source cannot be empty.")
            continue

        config.torrents_source = user_input
        return user_input


def _get_torrent_download_range(arg_value: str | None) -> tuple[int, int] | None:
    """
    Get a valid range of torrents to download.

    Args:
        arg_value: Value from command line argument

    Returns:
        Tuple of start and end range values
    """
    if not arg_value:
        yes = prompt("Do you want to download all torrents? [y/N]: ").lower()[:1] == "y"
        start: int
        end: int
        if yes:
            return None
        while True:
            try:
                start = int(prompt("Enter the start index (starts at 0): "))
                break
            except ValueError:
                print("Invalid start index. Please provide a valid number.")
                continue
        while True:
            try:
                end = int(prompt("Enter the end index (exclusive): "))
                if end <= start:
                    print("End index must be greater than start index.")
                    continue
                break
            except ValueError:
                print("Invalid end index. Please provide a valid number.")
                continue
        return start, end

    if arg_value == "all":
        return None

    try:
        start, end = map(int, arg_value.split("-"))
        if start < 1 or end < start:
            raise ValueError
        return start, end
    except ValueError:
        raise ValueError("Invalid range.")


def _start_download(args: argparse.Namespace) -> BittorrentClient:
    config = Config()
    # Get downloads directory
    _download_dir = _get_valid_directory(
        args.downloads,
        Config.KEY_DOWNLOAD,
        "Enter the directory where downloads are stored: ",
        config,
    )

    # Get torrents source
    _torrents_source = _get_valid_torrents_source(args.torrents_source, config)
    print(f"Download directory: {_download_dir}")
    print(f"Torrents source: {_torrents_source}")
    torrents_dir = Path(_torrents_source).name

    download_range = _get_torrent_download_range(args.range)

    appdata = config.app_data
    if not appdata.exists():
        config_dir = appdata / "qBittorrent"
        config_file = config_dir / "qBittorrent.conf"
        config_dir.mkdir(parents=True)
        config_file.write_text(qbittorrent_conf, encoding="utf-8")
        assert config_file.exists()
        print(f"Wrote qBittorrent configuration to {config_file}")

    out_dir = Path("working") / torrents_dir
    if args.dry_run:
        return BittorrentClient()
    clone_or_update(str(_torrents_source), out_dir)
    print("Repository cloned or updated successfully.")

    torrent_out_dir = "torrents"
    if not Path(torrent_out_dir).exists():
        Path(torrent_out_dir).mkdir(parents=True)

    # now search through the directory and find all the torrents and print out the paths
    print(f"Now copying all torrents to {torrent_out_dir}...")
    for torrent in out_dir.rglob("*.torrent"):
        # print(torrent)

        dst = Path(torrent_out_dir) / torrent.name
        already_exists = dst.exists()
        if already_exists:
            continue
        print(f"{torrent} -> {dst}")
        shutil.copy(torrent, dst)

    # now write out the docker-compose file
    compose_file = Path("docker-compose.yml")
    app_data_vol = "./" + appdata.as_posix()
    torrents_path = "./" + torrent_out_dir
    compose_text = render_template(
        appdata_path=app_data_vol,
        downloads_path="./" + str(_download_dir),
        torrents_path=torrents_path,
    )

    # now write out the docker-compose file
    compose_file = Path("docker-compose.yml")
    compose_file.write_text(
        compose_text,
        encoding="utf-8",
    )

    print("Instantiating docker-compose services...")
    os.system("docker-compose up -d")
    # we expect the port to be at 8080

    print("now waiting for the web interface to be available...")

    timeout = time.time() + 60 * 10  # 10 minutes from now
    while time.time() < timeout:
        try:
            response = requests.get("http://localhost:8080", timeout=1)
            if response.status_code == 200:
                print("Successfully connected to the web interface.")
                break
        except requests.exceptions.ConnectionError:
            print("Still waiting for the service to start running. Retrying...")
            time.sleep(5)
    else:
        print(f"Failed to connect to web interface after {timeout} seconds.")
        raise RuntimeError("Failed to connect to web interface.")

    torrent_urls: list[str] = []
    for torrent in Path(torrent_out_dir).rglob("*.torrent"):
        torrent_urls.append(f"http://fileserver:80/{torrent.name}")

    if download_range:
        start, end = download_range
        torrent_urls = torrent_urls[start:end]

    torrent_urls = sorted(torrent_urls)

    # now test that each torrent url is valid
    for url in torrent_urls:
        try:
            # inside the container it's fileserver:80, outside it's localhost:8081.
            url2 = url.replace("fileserver:80", "localhost:8081")
            response = requests.head(url2)
            if response.status_code != 200:
                print(f"Failed to test torrent: {url2}")
                raise RuntimeError("Failed to test torrent.")
        except requests.exceptions.ConnectionError:
            print(f"Failed to connect to torrent server: {url2}")
            raise RuntimeError("Failed to connect to torrent server.")
    client = BittorrentClient()
    client.queue_downloads(torrent_urls)
    return client


def main() -> int:
    """Main entry point."""
    args = _parse_args()

    if args.cancel:
        try:
            client = BittorrentClient()
            client.stop_all()
            print("All downloads cancelled.")
            time.sleep(10)
            return 0
        except Exception as e:
            print(f"Failed to cancel downloads: {e}")
            return 1

    just_attach = args.attach
    if not just_attach:
        client = _start_download(args)
    else:
        client = BittorrentClient()
    if args.dry_run:
        return 0

    try:
        stop_event = Event()
        update_thread = Thread(target=client.update_loop, args=(stop_event,))
        update_thread.start()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_event.set()
        update_thread.join()
        print("Exiting.")
        return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1


def unit_test() -> None:
    os.chdir(PROJECT_ROOT)
    # sys.argv.append("--attach")
    exit(main())


if __name__ == "__main__":
    unit_test()
