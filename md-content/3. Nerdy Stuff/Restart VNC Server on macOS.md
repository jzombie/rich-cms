# Restart VNC Server on macOS

To reset the VNC server on macOS from the command line, you can use the following steps:

1. **Stop the VNC server:**
   First, you need to stop the VNC server service. You can do this by unloading the `screensharing` launch daemon:

   ```bash
   sudo launchctl unload /System/Library/LaunchDaemons/com.apple.screensharing.plist
   ```

2. **Start the VNC server:**
   To restart the VNC server, you simply need to load the `screensharing` launch daemon again:

   ```bash
   sudo launchctl load /System/Library/LaunchDaemons/com.apple.screensharing.plist
   ```

This process will effectively reset the VNC server on your Mac. If you're experiencing issues, this can help to restart the service cleanly.
