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
Just copy the sddm-themes dir into '/usr/share/sddm/themes' and rename it to whatever you want. Then edit '/usr/lib/sddm/sddm.conf.d/default.conf'
``` python
[Theme]
# Current theme name
Current="Your theme name"
```

# yay
1. git clone https://aur.archlinux.org/yay.git
2. cd yay
3. makepkg -si
4. Done!