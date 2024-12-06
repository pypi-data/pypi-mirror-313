import _thread
import time
from threading import Event

import qbittorrentapi
from rich.console import Console
from rich.progress import BarColumn, Progress, TaskID, TextColumn, TimeRemainingColumn

_DEFAULT_HOST = "localhost"
_DEFAULT_PORT = 8080
_DEFAULT_USERNAME = "admin"
_DEFAULT_PASSWORD = "adminadmin"
_DEFAULT_MAX_WORKERS = 5

console = Console()

# Create a progress object
progress = Progress(
    TextColumn("[bold cyan]{task.description}"),  # Task description in cyan
    BarColumn(),  # Progress bar
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),  # Percentage
    TextColumn("[bold blue]{task.fields[status]}"),  # Add status column
    TimeRemainingColumn(),  # Time remaining
    console=console,
)


class TorrentProgress:
    total_downloads = 0
    completed_downloads = 0

    @classmethod
    def reset_counts(cls):
        cls.total_downloads = 0
        cls.completed_downloads = 0

    def __init__(self, filename: str, torrent_hash: str) -> None:
        self.filename = filename
        self.hash = torrent_hash
        self.progress = 0
        self.task_id: TaskID | None = None
        TorrentProgress.total_downloads += 1

    def start(self) -> None:
        self.task_id = progress.add_task(self.filename, total=100, status="")

    def update(self, progress_value: float, status: str = "") -> None:
        if self.task_id is not None:
            progress.update(self.task_id, completed=progress_value * 100, status=status)

    def complete(self) -> None:
        if self.task_id is not None:
            progress.remove_task(self.task_id)
            self.task_id = None


def _format_size(size: float) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def _format_speed(speed: int) -> str:
    return f"{_format_size(speed)}/s"


class BittorrentClient:
    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        max_workers: int | None = None,
    ):
        self.host = host or _DEFAULT_HOST
        self.port = port or _DEFAULT_PORT
        self.username = username or _DEFAULT_USERNAME
        self.password = password or _DEFAULT_PASSWORD
        self.max_workers = max_workers or _DEFAULT_MAX_WORKERS
        self.client = qbittorrentapi.Client(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
        )
        self.client.auth_log_in()
        self.queued_torrents: list[str] = []
        self.active_torrents: set[str] = set()
        self.torrent_progress: dict[str, TorrentProgress] = {}
        self.overall_progress_task: TaskID | None = None
        # self.print_system_info()

    def queue_downloads(self, torrent_urls: list[str]) -> None:
        """Initialize or add to download queue with torrents."""
        if self.overall_progress_task is None:
            # First time initialization
            TorrentProgress.reset_counts()
            self.overall_progress_task = progress.add_task(
                "[bold green]Overall Progress", total=len(torrent_urls), status=""
            )
        else:
            # Adding more torrents - update the total
            current_task = progress.tasks[self.overall_progress_task]
            if current_task.total is not None:
                progress.update(
                    self.overall_progress_task,
                    total=current_task.total + len(torrent_urls),
                    status="",
                )

        self.queued_torrents.extend(torrent_urls)
        self._process_queue()

    def _process_queue(self) -> None:
        """Process the torrent queue, adding new torrents up to max_workers."""
        while len(self.active_torrents) < self.max_workers and self.queued_torrents:
            torrent_url = self.queued_torrents.pop(0)
            ok = self.client.torrents_add(urls=torrent_url)
            if ok != "Ok.":
                print(f"Failed to add torrent: {torrent_url}")
                continue
            self.active_torrents.add(torrent_url)

    def stop_all(self) -> None:
        self.client.torrents.stop.all()

    def print_system_info(self) -> None:
        for k, v in self.client.app.build_info.items():
            print(f"{k}: {v}")

    def _update(self) -> None:
        """Process completed torrents and update queue."""
        torrents = self.client.torrents_info()
        if not torrents:
            return

        completed_hashes = [
            torrent.hash for torrent in torrents if "completed" in torrent.state.lower()
        ]

        if completed_hashes:
            self.client.torrents_delete(
                delete_files=False, torrent_hashes=completed_hashes
            )
            for hash_value in completed_hashes:
                if hash_value in self.torrent_progress:
                    self.torrent_progress[hash_value].complete()
                    del self.torrent_progress[hash_value]
                    TorrentProgress.completed_downloads += 1
                    if self.overall_progress_task is not None:
                        progress.update(
                            self.overall_progress_task,
                            completed=TorrentProgress.completed_downloads,
                        )
                self.active_torrents.remove(hash_value)
            self._process_queue()

    def _print_download_info(self) -> None:
        """Print current download information for all torrents."""
        torrents = self.client.torrents_info()
        if not torrents:
            print("No torrents yet.")
            return

        # Remove progress bars for completed/missing torrents
        current_hashes = {t.hash for t in torrents}
        completed_hashes = {t.hash for t in torrents if "completed" in t.state.lower()}

        # Remove progress bars that are no longer needed
        for torrent_hash in list(self.torrent_progress.keys()):
            if torrent_hash not in current_hashes or torrent_hash in completed_hashes:
                self.torrent_progress[torrent_hash].complete()
                del self.torrent_progress[torrent_hash]

        # Update existing progress bars and create new ones if needed
        for torrent in torrents:
            if "completed" in torrent.state.lower():
                continue

            if torrent.hash not in self.torrent_progress:
                self.torrent_progress[torrent.hash] = TorrentProgress(
                    torrent.name, torrent.hash
                )
                self.torrent_progress[torrent.hash].start()

            self.torrent_progress[torrent.hash].update(torrent.progress, torrent.state)

            # Refresh to update display
            # progress.refresh()

    def update_loop(self, stop_event: Event) -> None:
        try:
            with progress:
                while not stop_event.is_set():
                    self._update()
                    self._print_download_info()
                    progress.refresh()
                    time.sleep(0.1)
        except KeyboardInterrupt:
            _thread.interrupt_main()
