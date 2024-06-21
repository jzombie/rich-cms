# Setting Up CUPS Network Printer on Ubuntu

Setting up CUPS (Common Unix Printing System) for network printing on Ubuntu involves several steps. Here's a guide to help you through the process:

## Step 1: Install CUPS
First, ensure that CUPS is installed on your Ubuntu system. You can install it using the terminal. Open a terminal window and type the following command:

```bash
sudo apt-get update
sudo apt-get install cups
```

## Step 2: Start and Enable CUPS Service
Once CUPS is installed, start the CUPS service and enable it to start on boot with the following commands:

```bash
sudo systemctl start cups
sudo systemctl enable cups
```

## Step 3: Configure CUPS
To configure CUPS, you need to edit its configuration file. Open the file in a text editor with root privileges:

```bash
sudo nano /etc/cups/cupsd.conf
```

Make the following changes in the `cupsd.conf` file:

- Find the line that says `Listen localhost:631` and change it to `Port 631` to allow remote access to the CUPS server.
- Modify the `<Location />`, `<Location /admin>`, and `<Location /admin/conf>` sections to allow remote access. You can do this by adding `Allow @LOCAL` to each section.

For example:

```conf
<Location />
  # existing settings...
  Allow @LOCAL
</Location>

<Location /admin>
  # existing settings...
  Allow @LOCAL
</Location>

<Location /admin/conf>
  AuthType Default
  Require user @SYSTEM
  # existing settings...
  Allow @LOCAL
</Location>
```

Save and close the file.

## Step 4: Allow CUPS Through the Firewall
If you have a firewall enabled, allow CUPS through the firewall:

```bash
sudo ufw allow 631
```

## Step 5: Restart CUPS
After making changes to the configuration file, restart the CUPS service to apply the changes:

```bash
sudo systemctl restart cups
```

## Step 6: Access CUPS Web Interface
You can now access the CUPS web interface by going to `http://your-server-ip:631` from any computer in your network. Replace `your-server-ip` with the IP address of the Ubuntu server where CUPS is installed.

## Step 7: Add a Printer
To add a network printer:

1. Go to the CUPS web interface.
2. Click on “Administration” and then “Add Printer.”
3. Enter your Ubuntu username and password if prompted.
4. Follow the on-screen instructions to add your network printer.

## Step 8: Configure Client Computers
On each client computer, you need to install CUPS and configure it to use the CUPS server you set up. Repeat the installation process on each client and point them to your CUPS server.

Make sure the client computers are on the same network as the CUPS server. You may need to adjust their CUPS configuration files (`/etc/cups/client.conf`) to point to your server.

By following these steps, you should be able to set up CUPS for network printing on your Ubuntu system. If you encounter any issues, refer to the CUPS documentation or Ubuntu community forums for further assistance.

## Additional Setup for HP Printers

The log information you've provided indicates that the system is having trouble recognizing the HP Smart Tank 520/540 series printer attributes from the HPLIP (HP Linux Imaging and Printing) database. The `hpmud` (HP Multi-Point Transport Driver) subsystem is not finding the necessary data for this printer model.

Here are the steps to resolve this issue:

1. **Update HPLIP**: The version of HPLIP installed on your system may not have the necessary data for your printer model. You should update HPLIP to the latest version available. Open a terminal and run:

   ```bash
   sudo apt-get update
   sudo apt-get install --reinstall hplip
   ```

   After updating, you can check the installed version with `hp-check -v`.

2. **HP Device Manager**: Sometimes, using the HP Device Manager (`hp-toolbox`) can help in resolving printer issues. Run `hp-setup` to configure the printer.

   ```bash
   hp-setup
   ```

3. **Check for Additional Driver Support**: Not all printers are supported out of the box by the HPLIP database included with your Linux distribution. You might need to download a plugin or additional drivers from HP.

   ```bash
   sudo hp-plugin
   ```

4. **Manual Driver Installation**: If `hp-plugin` doesn't automatically fix the issue, you might need to manually download the plugin or driver from HP's website.

5. **Permissions**: Ensure that your user is part of the `lpadmin` group which is typically required for printer administration tasks.

   ```bash
   sudo usermod -a -G lpadmin your_username
   ```

   Replace `your_username` with your actual username.

6. **Restart CUPS**: After making changes, restart the CUPS service.

   ```bash
   sudo systemctl restart cups
   ```

7. **Check Connectivity**: Verify that your printer is connected via USB and is turned on. Sometimes the connection can be intermittent.

8. **Reconnect the Printer**: Disconnect and reconnect the printer and see if it's recognized.

9. **Consult Logs**: Check `/var/log/cups/error_log` for more detailed error messages that can help diagnose the issue.

   ```bash
   less /var/log/cups/error_log
   ```

10. **Seeking Further Help**: If none of the above resolves the issue, consider seeking help from the Ubuntu community forums, as users there may have encountered similar issues with the same printer model.

By following these steps, you should be able to address the issue of the printer not being recognized by your Ubuntu system.