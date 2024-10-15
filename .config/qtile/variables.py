### THEME ###
from themes import arch as theme

group_highlight_color = '#cd49b9'

### GENERAL ###

mod = "mod4"
terminal = "alacritty"
browser = "firefox"
file_manager = None 
launcher = "rofi -show drun -show-icons"
show_windows = "rofi -show window -show-icons"
powermenu = "rofi -show menu -modi 'menu:~/.config/rofi/scripts/rofi-power-menu --choices=shutdown/reboot' -config ~/.config/rofi/power.rasi"
screenshots_path = "~/screenshots/" # creates if doesn't exists
autostart_file = "~/.config/qtile/autostart.sh"

floating_apps = [
    'sxiv',
]

floating_names = [
    "Preferences ",
    "Eclipse IDE Launcher ",
    "New Java Project ",
    "Delete ",
    "New Java Package ",
    "New Java Class "
]

### LAYOUTS ###

layouts = [
    "MonadTall",
    "Max",
]

layouts_margin = 7
layouts_border_width = 2
layouts_border_color = theme['disabled']
layouts_border_focus_color = theme['accent']
layouts_border_on_single = True

### BAR ###

bar_top_margin = 7
bar_bottom_margin = 7
bar_left_margin = 7
bar_right_margin = 7
bar_size = 40

bar_background_color = theme['background']
bar_foreground_color = theme['foreground']

bar_font = "Mononoki Nerd Font"
bar_fontsize = 16