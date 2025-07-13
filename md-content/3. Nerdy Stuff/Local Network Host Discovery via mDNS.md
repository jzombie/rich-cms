#  Local Network Host Discovery via mDNS (`.local`)

This guide explains how to configure macOS and Linux machines to **advertise and resolve `.local` hostnames** on your local network using **Multicast DNS (mDNS)**.

> Use case: IP addresses change often on home networks. With mDNS, you can access machines via names like `mymachine.local` instead of tracking dynamic IPs.

## Overview

| Platform | mDNS Support       | Required Setup  |
| -------- | ------------------ | --------------- |
| macOS    | Built-in (Bonjour) | None            |
| Linux    | Requires `avahi`   | Install + setup |

## macOS Setup (Zero Config)

macOS comes with **Bonjour** pre-installed. It automatically advertises your hostname on the `.local` domain.

### View macOS Hostname

```sh
scutil --get LocalHostName
```

### Test from another device

```sh
ping <mac-hostname>.local
```

Example:

```sh
ping Jeremy-MacBook.local
```

## Linux Setup (Ubuntu, Debian, Arch, etc.)

Linux systems require `avahi-daemon` and proper NSS configuration.

### 1. Install Required Packages

```sh
sudo apt install avahi-daemon avahi-utils libnss-mdns
```

### 2. Enable and Start Avahi

```sh
sudo systemctl enable --now avahi-daemon
```

### 3. Configure NSS (`/etc/nsswitch.conf`)

Ensure this line includes `mdns4_minimal`:

```text
hosts: files mdns4_minimal [NOTFOUND=return] dns
```

### 4. Optional: Set a Friendly Hostname

```sh
sudo hostnamectl set-hostname mymachine
```

This will advertise your machine as `mymachine.local`.

### 5. Test From Another Host

```sh
ping mymachine.local
```

Or resolve the name:

```sh
avahi-resolve-host-name mymachine.local
```

## Firewall Requirements

Ensure your firewall allows:

* **UDP port 5353**
* **Multicast address** `224.0.0.251`


## Optional: List `.local` Devices on the Network

```sh
avahi-browse -at
```

Or just scan for hostnames:

```sh
avahi-browse -a | grep '^+.*IPv4' | awk '{print $4}' | sort -u
```

## Notes

* mDNS is **peer-to-peer** — no DNS server needed.
* Hostnames are dynamically discoverable even if the machine's IP changes.
* Works reliably on home networks, especially when DHCP is in use.
