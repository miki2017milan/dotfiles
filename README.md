# Grub Menu
My grub settings
``` python
GRUB_TIMEOUT=3
GRUB_TIMEOUT_STYLE=hidden
```

# SDDM login screen
Install the 'sddm-sugar-dark' package from the AUR for all the dependencies. Then replace the sugar-dark folder in '/usr/share/sddm/themes' with the sugar-dark folder in this reposetory. 
Then edit '/usr/lib/sddm/sddm.conf.d/default.conf'
``` python
[Theme]
# Current theme name
Current=sugar-dark
```

# yay
1. git clone https://aur.archlinux.org/yay.git
2. cd yay
3. makepkg -si
4. Done!