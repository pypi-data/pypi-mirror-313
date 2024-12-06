from pathlib import Path

# Relative to the appdata folder
QB_CONFIG_PATH = Path("qBittorrent/qBittorrent.conf")

CONFIG_FILE = r"""
[Application]
FileLogger\Age=1
FileLogger\AgeType=1
FileLogger\Backup=true
FileLogger\DeleteOld=true
FileLogger\Enabled=true
FileLogger\MaxSizeBytes=66560
FileLogger\Path=/config/qBittorrent/logs
MemoryWorkingSetLimit=4096

[AutoRun]
enabled=false
program=

[BitTorrent]
MergeTrackersEnabled=true
Session\AddTorrentStopped=false
Session\DefaultSavePath=/downloads/
Session\ExcludedFileNames=
Session\Port=6881
Session\QueueingSystemEnabled=true
Session\SSL\Port=33551
Session\ShareLimitAction=Stop
Session\TempPath=/downloads/incomplete/

[Core]
AutoDeleteAddedTorrentFile=Never

[LegalNotice]
Accepted=true

[Meta]
MigrationVersion=8

[Network]
Cookies=@Invalid()
PortForwardingEnabled=false
Proxy\HostnameLookupEnabled=false
Proxy\Profiles\BitTorrent=true
Proxy\Profiles\Misc=true
Proxy\Profiles\RSS=true

[Preferences]
Connection\PortRangeMin=6881
Connection\UPnP=false
Downloads\SavePath=/downloads/
Downloads\TempPath=/downloads/incomplete/
General\Locale=en
MailNotification\req_auth=true
WebUI\Address=*
WebUI\AuthSubnetWhitelist=@Invalid()
WebUI\Password_PBKDF2="@ByteArray(GE+1J3UvHPfuy2BkDMteUQ==:azWvz+bSKNLvd1W/KCE4vJLskIyP6MFvU8WgTWAp8VxFXEk3v1+ynV2IFQxhjlFm/d49J2WRuZv18ZtSoGqzrQ==)"
WebUI\ServerDomains=*

[RSS]
AutoDownloader\DownloadRepacks=true
AutoDownloader\SmartEpisodeFilter=s(\\d+)e(\\d+), (\\d+)x(\\d+), "(\\d{4}[.\\-]\\d{1,2}[.\\-]\\d{1,2})", "(\\d{1,2}[.\\-]\\d{1,2}[.\\-]\\d{4})"
"""
