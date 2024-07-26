# Backlights
For the backlight control you'll need to add xbacklight to the sudoers file
``` python
%wheel ALL=(ALL:ALL) NOPASS: /usr/bin/xbacklight
```

# Grub Menu
If you want to have the same grub config then change this:
``` python
GRUB_TIMEOUT=3
GRUB_TIMEOUT_STYLE=hidden
```

# SDDM login screen
Just copy the sddm-themes dir into the sddm themes dir and rename it
