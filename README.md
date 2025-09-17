# Overview

```python
Distro: Arch
WM: Qtile
Compositor: picom-git
Shell: Bash
Terminal: Allacrity
App-runner: Rofi
notification-manager: dunst
```

# Desktop preview

![alt text](https://github.com/miki2017milan/dotfiles/blob/laptop/images/desktop.png?raw=true)

# Alacritty

![alt text](https://github.com/miki2017milan/dotfiles/blob/laptop/images/terminal.png?raw=true)

# Rofi

![alt text](https://github.com/miki2017milan/dotfiles/blob/laptop/images/rofi.png?raw=true)

# Battery alerts

I have a cronjob running every 5 min to check if the battery has reached the warning threshold or is at 100% and display a notification.

```bash
*/5 * * * * /home/username/bin/battery-alert
```

To get a notification when the laptop is plugged or unplugged add a file here /etc/udev/rules.d/power.rules with the content

```bash
# Rule for when switching to battery
ACTION=="change", SUBSYSTEM=="power_supply", ATTR{type}=="Mains", ATTR{online}=="1", ENV{DISPLAY}=":0", ENV{XAUTHORITY}="/home/username/.Xauthority" RUN+="/usr/bin/su username -c '/home/username/bin/battery-charging 1'"
# Rule for when switching to AC
ACTION=="change", SUBSYSTEM=="power_supply", ATTR{type}=="Mains", ATTR{online}=="0", ENV{DISPLAY}=":0", ENV{XAUTHORITY}="/home/username/.Xauthority" RUN+="/usr/bin/su username -c '/home/username/bin/battery-charging 0'"
```

(Credits: https://www.youtube.com/watch?v=3wTt6fStYCI&t=10s)
