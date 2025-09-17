### IMPORTS ###
import psutil

from libqtile.config import (
    Key,
    Screen,
    Group,
    Drag,
    Click,
    ScratchPad,
    DropDown,
    Match,
)
from libqtile import qtile, layout, bar, hook
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import RectDecoration

### CONFIG
#Baisc
mod = "mod4" # Windows key as mod key
font = "Mononoki Nerd Font"

# Apps
terminal = "alacritty"
browser = "firefox" 
file_manager = ""

# Rofi
launcher = "rofi -show drun -show-icons -icon-theme Papirus"
show_windows = "rofi -show window -show-icons -icon-theme Papirus"
power_menu = "rofi -show menu -modi 'menu:~/.config/rofi/scripts/rofi-power-menu --choices=shutdown/reboot --confirm=shutdown/reboot' -config ~/.config/rofi/power.rasi"

# Paths
user_home = "/home/milan/"
screenshots_path = user_home + "screenshots" # creates if doesn't exists
autostart_file = "sh /home/milan/.config/qtile/autostart.sh"

### COLORS

colors = {
    "border_focus": "#b7bdf8",
    "border_normal": "#3b4252",
    "bar_background": "#181926",
    "widget_background": "#1e2030",
    "volume_color": "#8aadf4",
    "calender_color": "#eed49f",
    "battary_color": "#cad3f5",
    "clock_color": "#a6da95",
    "groupbox_active": "#7a51ad",
    "groupbox_inactive": "#494d64",
    "groupbox_used_tab": "#cad3f5"
}

### LAYOUTS ###

layouts = [
    layout.MonadTall(
        border_width=2,
        margin=9,
        border_focus=colors["border_focus"],
        border_normal=colors["border_normal"],
        font=font,
        grow_amount=2,
        ratio=0.57,
        min_ratio=0.5,
        max_ratio=0.7,
        change_size=20,
        change_ratio=0.01
        ),
    layout.Max(
        border_width=2, 
        margin=9,
        border_focus=colors["border_focus"],
        boarder_normal=colors["border_normal"],
        font=font,
        grow_amount=2,
    )
]

### CUSTOM FUNCTIONS ###

@lazy.function
def volume_up(_qtile):
    qtile.spawn('pamixer -i 5')
    qtile.spawn(user_home + '.config/qtile/scripts/show_volume.sh')

@lazy.function
def volume_down(_qtile):
    qtile.spawn('pamixer -d 5')
    qtile.spawn(user_home + '.config/qtile/scripts/show_volume.sh')

@lazy.function
def volume_mute(_qtile):
    qtile.spawn('pamixer -t')
    qtile.spawn(user_home + '.config/qtile/scripts/show_volume.sh')

@lazy.function
def brigthness_up(_qtile):
    qtile.spawn(user_home + '.config/qtile/scripts/brightness_up.sh')

@lazy.function
def brigthness_down(_qtile):
    qtile.spawn(user_home + '.config/qtile/scripts/brightness_down.sh')

@lazy.function
def screenshot(_qtile, mode):
    qtile.spawn(f'flameshot {mode} -c -p {screenshots_path}')
    qtile.spawn(f'dunstify "  Screenshot taken!" "Saved under \'{screenshots_path}\' (When not aborded)"')

def show_keys():
    key_help = ""
    for k in keys:
        mods = ""

        for m in k.modifiers:
            if m == "mod4":
                mods += "Super + "
            else:
                mods += m.capitalize() + " + "

        if len(k.key) > 1:
            mods += k.key.capitalize()
        else:
            mods += k.key

        key_help += "{:<30} {}".format(mods, k.desc + "\n")

    return key_help

### GROUPS ###

groups = [
    Group(name="1", label="", screen_affinity=0),
    Group(name="2", label="", screen_affinity=0),
    Group(name="3", label="", screen_affinity=1),
    Group(name="4", label=" ", screen_affinity=1),
]

def go_to_group(name: str):
    def _inner(qtile):
        if name in '12':
            qtile.focus_screen(0)
            qtile.groups_map[name].toscreen()
        else:
            qtile.focus_screen(1)
            qtile.groups_map[name].toscreen()

    return _inner

def go_to_group_and_move_window(name: str):
    def _inner(qtile):
        if name in "12":
            qtile.current_window.togroup(name, switch_group=False)
            qtile.focus_screen(0)
            qtile.groups_map[name].toscreen()
        else:
            qtile.current_window.togroup(name, switch_group=False)
            qtile.focus_screen(1)
            qtile.groups_map[name].toscreen()

    return _inner

keys = [
    # Window Management
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "left", lazy.screen.prev_group(True)),
    Key([mod, "control"], "right", lazy.screen.next_group(True)),

    Key([mod], "period", lazy.next_screen(), desc='Move focus to next monitor'),

    Key([mod], "plus", lazy.layout.grow(), desc="Grow window"),
    Key([mod], "minus", lazy.layout.shrink(), desc="Shrink window"),

    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "x", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    
    Key([mod], "f", lazy.next_layout(), desc="Toggle fullscreen on the focused window",),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc="Toggle full-fullscreen on the focused window",),

    # Media
    Key([], "XF86AudioRaiseVolume", volume_up()),
    Key([], "XF86AudioLowerVolume", volume_down()),
    Key([], "XF86AudioMute", volume_mute()),
    Key([], "XF86MonBrightnessUp", brigthness_up()),
    Key([], "XF86MonBrightnessDown", brigthness_down()),
    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause')),
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous')),
    Key([], "XF86AudioNext", lazy.spawn('playerctl next')),
    
    # Launch
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Space", lazy.spawn(launcher), desc="Launch launcher"),
    Key([mod], "w", lazy.spawn(show_windows), desc="Shows open windows"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "e", lazy.spawn(file_manager), desc="Launch file manager"),
    Key([mod], "F4", lazy.spawn(power_menu), desc="Launch powermenu"),
    
    # Qtile
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Screenshot
    Key([], "Print", screenshot(mode="gui"), desc="Take a screenshot"),
    Key([mod], "Print", screenshot(mode="screen"), desc="Take a screenshot of a zone or a window"),
    
]

for i in groups:
    keys.append(Key([mod], i.name, lazy.function(go_to_group(i.name))))

for i in groups:
    keys.append(Key([mod, "shift"], i.name, lazy.function(go_to_group_and_move_window(i.name))))

### WIDGETS ###

widget_defaults = dict(
    font = font,
    fontsize = 18,
    padding = 3,
    background = colors["bar_background"],
    foreground=colors["widget_background"],
    decorations=[
        BorderDecoration(
            colour=colors["bar_background"],
            border_width=[11, 0, 10, 0],
        )
    ],
)
# extension_defaults = widget_defaults.copy()

group_box_settings = {
    "padding": 5,
    "borderwidth": 4,
    "active": colors["groupbox_used_tab"],
    "inactive": colors["groupbox_inactive"],
    "disable_drag": True,
    "rounded": True,
    "block_highlight_text_color": colors["groupbox_active"],
    "highlight_method": "block",
    "this_current_screen_border": colors["widget_background"],
    "this_screen_border": colors["widget_background"],
    "other_current_screen_border": colors["widget_background"],
    "other_screen_border": colors["widget_background"],
    "background": colors["widget_background"],
    "fontsize": 25
}

screen1 = [
    widget.Sep(
        linewidth=0,
        padding=30,
    ),

    ### GROUP BOX
    widget.TextBox(
        text="",
        fontsize=30,
        padding=0,
    ),
    widget.GroupBox(
        visible_groups=["1", "2", "3", "4"],
        **group_box_settings,
    ),
    widget.TextBox(
        text="",
        fontsize=30,
        padding=0,
    ),
    ### END GROUP BOX

    widget.Spacer(),# Space in the middle

    ### SYSTRAY
    widget.Systray(
        icon_size=26,
        padding=7,
    ),
    ### END SYSTRAY

    ### VOLUME
    widget.TextBox(
        text="",
        fontsize=30,
        padding=0,
    ),
    widget.TextBox( # Volume icon
        text=" ",
        foreground=colors["volume_color"],
        background=colors["widget_background"],
    ),
    widget.PulseVolume(
        foreground=colors["volume_color"],
        background=colors["widget_background"],
        limit_max_volume="True",
    ),
    widget.TextBox(
        text="",
        fontsize=30,
        padding=0,
    ),
    ### END VOLUME

    widget.Sep(
        linewidth=0,
        padding=10,
    ),

    ### CALENDER
    widget.TextBox(
        text="",
        fontsize=30,
        padding=0,
    ),
    widget.TextBox(
        text=" ",
        foreground=colors["calender_color"],
        background=colors["widget_background"],
    ),
    widget.Clock(
        format="%a, %b %d",
        foreground=colors["calender_color"],
        background=colors["widget_background"],
    ),
    widget.TextBox(
        text="",
        fontsize=30,
        padding=0,
    ),
    ### END CALENDER

    widget.Sep(
        linewidth=0,
        padding=10,
    ),

    ### BATTARY
    widget.TextBox(
        text="",
        fontsize=30,
        padding=0,
    ),
    widget.BatteryIcon(
        theme_path = '~/.local/share/icons/qtile-battery',
        scale = 2,
        background=colors["widget_background"],
        foreground=colors["battary_color"],
        update_interval = 5,
        padding = 0
    ),
    widget.Battery(
        discharge_char="",
        charge_char="",
        format="{percent:2.0%}",
        background=colors["widget_background"],
        foreground=colors["battary_color"],
        padding = 0,
        update_interval = 5,
    ),
    widget.TextBox(
        text="",
        fontsize=30,
        padding=0,
    ),
    ### BATTARY END

    widget.Sep(
        linewidth=0,
        padding=10,
    ),

    ### CLOCK
    widget.TextBox(
        text="",
        fontsize=30,
        padding=0,
    ),
    widget.TextBox(
        text=" ",
        background=colors["widget_background"],
        foreground=colors["clock_color"],
    ),
    widget.Clock(
        format="%I:%M %p",
        background=colors["widget_background"],
        foreground=colors["clock_color"],
    ),
    widget.TextBox(
        text="",
        fontsize=30,
        padding=0,
    ),
    ### END CLOCK

    widget.Sep(
        linewidth=0,
        padding=10,
    ),
]

### SCREENS ###

screens = [
    Screen(
        top=bar.Bar(
            widgets=screen1,
            size=56,
            background=colors["bar_background"],
            border_width=[0, 0, 5, 0],
            border_color=colors["widget_background"]
        ),
    ),
]

### MOUSE ###
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
]

### OTHER SETTINGS ###

dgroups_key_binder = None
dgroups_app_rules: list = []
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False

floating_apps = [
    'sxiv',
]

floating_title = [
    "Preferences ",
    "Eclipse IDE Launcher ",
    "New Java Project ",
    "Delete ",
    "New Java Package ",
    "New Java Class ",
    "IdleProduction"
]

floating_layout = layout.Floating(
    border_width=2, 
    margin=9,
    border_focus=colors["border_focus"],
    border_normal=colors["border_normal"],
    font=font,
    grow_amount=2,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry,
        *[Match(title=app) for app in floating_title],
        *[Match(wm_class=app) for app in floating_apps],
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

### HOOKS ###

ready = False

@hook.subscribe.startup_once
def _():
    qtile.spawn(autostart_file)

wmname = "qtile"
