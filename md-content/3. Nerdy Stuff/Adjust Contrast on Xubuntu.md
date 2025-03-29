# Adjust Contrast on Xubuntu

A washed-out screen on Xubuntu is usually caused by incorrect color settings or a driver issue. Here’s how you can adjust contrast and color levels:

## Quick Fix: Use `xrandr` to adjust contrast/brightness/gamma

You can use `xrandr` to tweak display settings. First, open a terminal and run:

```bash
xrandr
```

This lists your connected displays. Look for something like `eDP-1`, `HDMI-1`, etc.

Then try adjusting gamma and brightness:

### Example (adjusting gamma and brightness):

```bash
xrandr --output eDP-1 --brightness 0.9 --gamma 1.0:0.9:0.9
```

- `--brightness`: Default is 1.0. Try values like 0.9 or 1.1.
- `--gamma R:G:B`: Adjust these to tweak contrast. Lower G/B can reduce the washed-out look.

You can test different combinations live—no need to reboot.


## More Persistent Fix: Use `.xprofile` or autostart script

To apply this fix at boot:

1. Edit your `.xprofile` in your home directory:

```bash
nano ~/.xprofile
```

2. Add your `xrandr` command, e.g.:

```bash
xrandr --output eDP-1 --brightness 0.9 --gamma 1.0:0.9:0.9
```

3. Save and reboot.

### If still not fixed: Check GPU drivers

If you’re on Intel, AMD, or NVIDIA, ensure you're using the correct drivers:

- For **NVIDIA**, use `nvidia-settings` and make sure the proprietary driver is installed (`Software & Updates > Additional Drivers`).
- For **Intel/AMD**, Xubuntu generally uses `xf86-video-intel` or `modesetting`.

## Optional: Install GUI tools

You can also try:

```bash
sudo apt install arandr
```

`arandr` is a GUI for `xrandr` that makes it easier to configure.
