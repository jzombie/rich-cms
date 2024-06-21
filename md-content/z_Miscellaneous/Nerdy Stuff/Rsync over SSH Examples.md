# Rsync over SSH Examples

- **Basic rsync with SSH**:
  ```bash
  rsync -avz -e "ssh" /path/to/local/dir user@remote_host:/path/to/remote/dir
  ```

- **Specifying SSH port**:
  ```bash
  rsync -avz -e "ssh -p 2222" /path/to/local/dir user@remote_host:/path/to/remote/dir
  ```

- **Syncing a single file**:
  ```bash
  rsync -avz -e "ssh" /path/to/local/file.txt user@remote_host:/path/to/remote/dir
  ```

- **Syncing a directory w/ progress**:
```bash
rsync --progress -avz -e "ssh" /path/to/local/directory user@remote_host:"/Volumes/Can Contain Spaces/Some Subdirectory"
```

- **Dry run (simulate transfer)**:
  ```bash
  rsync -avz --dry-run -e "ssh" /path/to/local/dir user@remote_host:/path/to/remote/dir
  ```

Replace `/path/to/local/dir`, `user@remote_host:/path/to/remote/dir`, and `2222` with your local directory path, remote user and host with the remote directory path, and your SSH port if it's not the default (22), respectively.
