import time
import fnmatch
import paramiko
from navconfig.logging import logging
from .watch import BaseWatchdog, BaseWatcher
from ...interfaces import CacheSupport

logging.getLogger("paramiko").setLevel(logging.WARNING)


class SFTPWatcher(BaseWatcher):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        path: str,
        interval=300,
        **kwargs,
    ):
        super(SFTPWatcher, self).__init__(**kwargs)
        self.host = host
        self.port = port
        self.user = username
        self.password = password
        self.interval = interval
        self.path = path
        self._expiration = kwargs.pop("every", None)

    def close_watcher(self):
        pass

    def run(self, *args, **kwargs):
        while not self.stop_event.is_set():
            try:
                # Connect to the SSH server
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(
                    self.host,
                    port=self.port,
                    username=self.user,
                    password=self.password,
                )
                # Connect to the SFTP server
                sftp_client = ssh_client.open_sftp()
                # Check if the file or directory exists
                try:
                    # Split the path into directory and filename
                    directory, pattern = self.path.rsplit("/", 1)

                    # List all files in the directory
                    files = sftp_client.listdir(directory)

                    # Filter the files based on the wildcard pattern
                    matching_files = fnmatch.filter(files, pattern)

                    files = []
                    with CacheSupport(every=self._expiration) as cache:
                        for file in matching_files:
                            filepath = f"{directory}/{file}"
                            # Check if file is already processed
                            if cache.exists(filepath):
                                continue
                            stat = sftp_client.stat(filepath)
                            file_args = {
                                "filename": file,
                                "directory": directory,
                                "path": filepath,
                                "host": self.host,
                                "size": stat.st_size,
                                "perms": oct(stat.st_mode),
                                "modified": time.ctime(stat.st_mtime),
                            }
                            self._logger.notice(f"Found {self.path} on {self.host}:")
                            files.append(file_args)
                            # Add file to the cache
                            cache.setexp(filepath, value=filepath)
                        if files:
                            # Mail was detected, call actions.
                            args = {"files": files, **kwargs}
                            self.parent.call_actions(**args)
                except FileNotFoundError:
                    pass
                # Disconnect
                sftp_client.close()
                ssh_client.close()
            except Exception as e:
                print(f"An error occurred while checking the server: {e}")
                continue

            # Wait for the interval, but check the stop_event every second
            for _ in range(self.interval):
                if self.stop_event.is_set():
                    break
                time.sleep(1)


class SFTPWatchdog(BaseWatchdog):
    def create_watcher(self, *args, **kwargs) -> BaseWatcher:
        credentials = kwargs.pop("credentials", {})
        interval = kwargs.pop("interval", 300)
        self.mask_start(**kwargs)
        self.credentials = self.set_credentials(credentials)
        self.path = self.mask_replacement(kwargs.pop("path", None))
        return SFTPWatcher(
            **self.credentials, path=self.path, interval=interval, **kwargs
        )
