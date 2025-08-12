### IMPORTS ###
import sys
import os
import subprocess
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
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile import qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import RectDecoration

sys.path.append(os.path.expanduser('~/.config/qtile'))

# Appscd ~
mod = "mod4"
terminal = "alacritty"
browser = "brave" 
file_manager = "none"

# Rofi
launcher = "rofi -show drun -show-icons -icon-theme Papirus"
show_windows = "rofi -show window -show-icons -icon-theme Papirus"

# Paths
screenshots_path = "/home/milan/screenshots" # creates if doesn't exists
autostart_file = "/home/milan/autostart.sh"

### LAYOUTS ###

colors = [
    ["#2e3440", "#2e3440"],  # 0 background
    ["#d8dee9", "#d8dee9"],  # 1 foreground
    ["#3b4252", "#3b4252"],  # 2 background lighter
    ["#bf616a", "#bf616a"],  # 3 red
    ["#a3be8c", "#a3be8c"],  # 4 green
    ["#ebcb8b", "#ebcb8b"],  # 5 yellow
    ["#81a1c1", "#81a1c1"],  # 6 blue
    ["#b48ead", "#b48ead"],  # 7 magenta
    ["#88c0d0", "#88c0d0"],  # 8 cyan
    ["#e5e9f0", "#e5e9f0"],  # 9 white
    ["#4c566a", "#4c566a"],  # 10 grey
    ["#d08770", "#d08770"],  # 11 orange
    ["#8fbcbb", "#8fbcbb"],  # 12 super cyan
    ["#5e81ac", "#5e81ac"],  # 13 super blue
    ["#242831", "#242831"],  # 14 super dark background
]

layout_theme = {
    "border_width": 3,
    "margin": 9,
    "border_focus": "5d6474",
    "border_normal": "3b4252",
    "font": "Mononoki Nerd Font",
    "grow_amount": 2,
}

layouts_tweaks = {
    "MonadTall": {
        "ratio": 0.57,
        "min_ratio": 0.5,
        "max_ratio": 0.7,
        "change_size": 20,
        "change_ratio": 0.01,
    },
}

layouts = ["MonadTall", "Max"]
layouts = [getattr(layout, i)(**(layout_theme|layouts_tweaks.get(i, {}))) for i in layouts]

### CUSTOM FUNCTIONS ###

@lazy.function
def volume_up(_qtile):
    os.system('pamixer -i 5')
    os.system('sh ~/.config/qtile/scripts/show_volume.sh')

@lazy.function
def volume_down(_qtile):
    os.system('pamixer -d 5')
    os.system('sh ~/.config/qtile/scripts/show_volume.sh')

@lazy.function
def volume_mute(_qtile):
    os.system('pamixer -t')
    os.system('sh ~/.config/qtile/scripts/show_volume.sh')

@lazy.function
def screenshot(_qtile, mode):
    os.system(f'flameshot {mode} -c -p {screenshots_path}')
    os.system(f'dunstify "  Screenshot taken!" "Saved under \'{screenshots_path}\' (When not aborded)"')

def open_pavu():
    qtile.cmd_spawn("pavucontol")

def open_powermenu():
    qtile.cmd_spawn("power")


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
    Group(name="1", label="󰣇", screen_affinity=0),
    Group(name="2", label="󰣇", screen_affinity=0),
    Group(name="3", label="", screen_affinity=1, matches=[Match(wm_class="brave")]),
    Group(name="4", label="", screen_affinity=1, matches=[Match(wm_class="spotify")]),
    Group(name="5", label="", screen_affinity=1, matches=[Match(wm_class="discord")]),
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

    Key([mod], "period", lazy.next_screen(), desc='Move focus to next monitor'),

    Key([mod], "plus", lazy.layout.grow(), desc="Grow window"),
    Key([mod], "minus", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod], "r", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "x", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    
    Key([mod], "f", lazy.next_layout(), desc="Toggle fullscreen on the focused window",),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc="Toggle full-fullscreen on the focused window",),

    Key([mod], "a", lazy.function(go_to_group("3")), desc="Move to Browser group",),
    Key([mod], "d", lazy.function(go_to_group("5")), desc="Move to Discord group",),
    Key([mod], "s", lazy.function(go_to_group("4")), desc="Move to Spotify group",),

    # Media

    Key([], "XF86AudioRaiseVolume", volume_up()),
    Key([], "XF86AudioLowerVolume", volume_down()),
    Key([], "XF86AudioMute", volume_mute()),
    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause')),
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous')),
    Key([], "XF86AudioNext", lazy.spawn('playerctl next')),

    # Launch

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Space", lazy.spawn(launcher), desc="Launch launcher"),
    Key([mod], "w", lazy.spawn(show_windows), desc="Shows open windows"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "e", lazy.spawn(file_manager), desc="Launch file manager"),
    Key([mod], "F4", lazy.spawn(open_powermenu), desc="Launch powermenu"),
    
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
    font = "Mononoki Nerd Font",
    fontsize = 18,
    padding = 3,
    background = colors[0],
    decorations=[
        BorderDecoration(
            colour=colors[0],
            border_width=[11, 0, 10, 0],
        )
    ],
)
extension_defaults = widget_defaults.copy()

group_box_settings = {
    "padding": 5,
    "borderwidth": 4,
    "active": colors[9],
    "inactive": colors[10],
    "disable_drag": True,
    "rounded": True,
    "block_highlight_text_color": colors[3],
    "highlight_method": "block",
    "this_current_screen_border": colors[14],
    "this_screen_border": colors[14],
    "other_current_screen_border": colors[14],
    "other_screen_border": colors[14],
    "foreground": colors[1],
    "background": colors[14],
    "urgent_border": colors[3],
}

screen1 = [
    widget.TextBox(
        text=" ",
        foreground=colors[13],
        background=colors[0],
        font="Mononoki Nerd Font",
        fontsize=10,
        padding=10
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.GroupBox(
        font="Mononoki Nerd Font",
        visible_groups=["1", "2"],
        **group_box_settings,
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.Sep(
        linewidth=0,
        foreground=colors[2],
        background=colors[0],
        padding=10,
        size_percent=40,
    ),
    widget.Sep(
        linewidth=0,
        foreground=colors[2],
        padding=10,
        size_percent=50,
    ),
    widget.Spacer(),
    widget.Systray(
        icon_size=26,
        background=colors[0],
        padding=7,
    ),
    widget.Sep(
        linewidth=0,
        foreground=colors[2],
        padding=10,
        size_percent=50,
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.TextBox(
        text=" ",
        foreground=colors[8],
        background=colors[14],
        font="Font Awesome 6 Free Solid",
    ),
    widget.PulseVolume(
        foreground=colors[8],
        background=colors[14],
        limit_max_volume="True",
        mouse_callbacks={"Button3": lambda: qtile.cmd_spawn("pavucontrol")},
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.Sep(
        linewidth=0,
        foreground=colors[2],
        padding=10,
        size_percent=50,
    ),
    widget.Sep(
        linewidth=0,
        foreground=colors[2],
        padding=10,
        size_percent=50,
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.TextBox(
        text=" ",
        font="Mononoki Nerd Font",
        foreground=colors[5],
        background=colors[14],
    ),
    widget.Clock(
        format="%a, %b %d",
        background=colors[14],
        foreground=colors[5],
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.Sep(
        linewidth=0,
        foreground=colors[2],
        padding=10,
        size_percent=50,
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.TextBox(
        text=" ",
        font="Mononoki Nerd Font",
        foreground=colors[4],
        background=colors[14],
    ),
    widget.Clock(
        format="%I:%M %p",
        foreground=colors[4],
        background=colors[14],
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.TextBox(
        text="⏻",
        foreground=colors[13],
        font="Mononoki Nerd Font",
        fontsize=25,
        padding=20,
        mouse_callbacks={"Button1": open_powermenu},
    ),
]

screen2 = [
    widget.TextBox(
        text=" ",
        foreground=colors[13],
        background=colors[0],
        font="Mononoki Nerd Font",
        fontsize=28,
        padding=10
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.GroupBox(
        font="Mononoki Nerd Font",
        visible_groups=["3", "4", "5"],
        **group_box_settings,
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.Sep(
        linewidth=0,
        foreground=colors[2],
        background=colors[0],
        padding=10,
        size_percent=40,
    ),
    widget.Sep(
        linewidth=0,
        foreground=colors[2],
        padding=10,
        size_percent=50,
    ),
    widget.Spacer(),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.TextBox(
        text=" ",
        foreground=colors[8],
        background=colors[14],
        font="Font Awesome 6 Free Solid",
    ),
    widget.PulseVolume(
        foreground=colors[8],
        background=colors[14],
        limit_max_volume="True",
        mouse_callbacks={"Button3": open_pavu},
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.Sep(
        linewidth=0,
        foreground=colors[2],
        padding=10,
        size_percent=50,
    ),
    widget.Sep(
        linewidth=0,
        foreground=colors[2],
        padding=10,
        size_percent=50,
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.TextBox(
        text=" ",
        font="Mononoki Nerd Font",
        foreground=colors[5],
        background=colors[14],
    ),
    widget.Clock(
        format="%a, %b %d",
        background=colors[14],
        foreground=colors[5],
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.Sep(
        linewidth=0,
        foreground=colors[2],
        padding=10,
        size_percent=50,
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.TextBox(
        text="󰥔",
        font="Mononoki Nerd Font",
        foreground=colors[4],
        background=colors[14],
    ),
    widget.Clock(
        format="%I:%M %p",
        foreground=colors[4],
        background=colors[14],
    ),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
    ),
    widget.TextBox(
        text="⏻",
        foreground=colors[13],
        font="Mononoki Nerd Font",
        fontsize=25,
        padding=20,
        mouse_callbacks={"Button1": open_powermenu},
    ),
]

### SCREENS ###

screens = [
    Screen(
        top=bar.Bar(
            widgets= screen1,
            size=56,
            border_width=[0, 0, 3, 0],
            border_color="#3b4252",
            margin = [0, 0, 0, 0],
        ),
    ),

    Screen(
        top=bar.Bar(
            widgets= screen2,
            size=56,
            border_width=[0, 0, 3, 0],
            border_color="#3b4252",
            margin = [0, 0, 0, 0],
        ),
    ),
]

### MOUSE ###

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
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

floating_names = [
    "Preferences ",
    "Eclipse IDE Launcher ",
    "New Java Project ",
    "Delete ",
    "New Java Package ",
    "New Java Class "
]

floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry,
        *[Match(title=app) for app in floating_names],
        *[Match(wm_class=app) for app in floating_apps]
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
    run(autostart_file)

wmname = "qtile"
