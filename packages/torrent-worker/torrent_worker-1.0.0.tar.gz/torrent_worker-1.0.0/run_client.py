import time
import sys

from torrent_worker.client import BittorrentClient



def unit_test() -> None:
    client = BittorrentClient()
    try:
        yes = input("Start the download? [y/N]: ").strip().lower()[:1] == "y"
        if yes:
            client.queue_downloads(["http://fileserver:80/pilimi-zlib-0-119999.torrent"])
        #client.queue_downloads("https://0158-98-97-27-15.ngrok-free.app/pilimi-zlib-0-119999.torrent")
        # client.print_info()

        while True:
            client.update()
            client.print_download_info()
            time.sleep(10)
    except KeyboardInterrupt:
        stop_torrents = input("Do you want to stop all torrents? (y/n): ").strip().lower()[:1] == "y"
        if stop_torrents:
            client.stop_all()
        print("Exiting.")

if __name__ == "__main__":
    unit_test()
    sys.exit(0)