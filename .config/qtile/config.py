### IMPORTS ###
import sys

from os import system, makedirs
from os.path import expanduser, exists

from subprocess import run

from libqtile import layout, hook, bar
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget

sys.path.append(expanduser('~/.config/qtile'))

from variables import *

screenshots_path = expanduser(screenshots_path)
autostart_file = expanduser(autostart_file)

if not exists(screenshots_path):
    makedirs(screenshots_path)

### LAYOUTS ###

layout_theme = {
    "border_width": layouts_border_width,
    "margin": layouts_margin,
    "border_focus": layouts_border_focus_color,
    "border_normal": layouts_border_color,
    "border_on_single": layouts_border_on_single
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

layouts = [getattr(layout, i)(**(layout_theme|layouts_tweaks.get(i, {}))) for i in layouts]

### CUSTOM FUNCTIONS ###

@lazy.function
def volume_up(_qtile):
    system('pamixer -i 5')
    system('sh ~/.config/qtile/scripts/show_volume.sh')

@lazy.function
def volume_down(_qtile):
    system('pamixer -d 5')
    system('sh ~/.config/qtile/scripts/show_volume.sh')

@lazy.function
def volume_mute(_qtile):
    system('pamixer -t')
    system('sh ~/.config/qtile/scripts/show_volume.sh')

@lazy.function
def screenshot(_qtile, mode):
    system(f'flameshot {mode} -c -p {screenshots_path}')
    system(f'dunstify "  Screenshot taken!" "Saved under \'{screenshots_path}\' (When not aborded)"')

@lazy.function
def switch_audio(_qtile):
    system("sh ~/.config/qtile/scripts/switch_audio.sh")

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

    # Media

    Key([], "XF86AudioRaiseVolume", volume_up()),
    Key([], "XF86AudioLowerVolume", volume_down()),
    Key([], "XF86AudioMute", volume_mute()),
    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause')),
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous')),
    Key([], "XF86AudioNext", lazy.spawn('playerctl next')),

    Key([mod], "s", switch_audio()),

    # Launch

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Space", lazy.spawn(launcher), desc="Launch launcher"),
    Key([mod], "w", lazy.spawn(show_windows), desc="Shows open windows"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "e", lazy.spawn(file_manager), desc="Launch file manager"),
    Key([mod], "F4", lazy.spawn(powermenu), desc="Launch powermenu"),
    
    # Qtile
    
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Screenshot

    Key([], "Print", screenshot(mode="gui"), desc="Take a screenshot"),
    Key([mod], "Print", screenshot(mode="screen"), desc="Take a screenshot of a zone or a window"),
    
]

### GROUPS ###

groups = [
    Group(name="1", label="●", screen_affinity=0),
    Group(name="2", label="●", screen_affinity=0),
    Group(name="3", label="●", screen_affinity=1),
    Group(name="4", label="●", screen_affinity=1),
]


def go_to_group(name: str):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.groups_map[name].toscreen()
            return

        if name in '12':
            qtile.focus_screen(0)
            qtile.groups_map[name].toscreen()
        else:
            qtile.focus_screen(1)
            qtile.groups_map[name].toscreen()

    return _inner

for i in groups:
    keys.append(Key([mod], i.name, lazy.function(go_to_group(i.name))))

def go_to_group_and_move_window(name: str):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.current_window.togroup(name, switch_group=False)
            return

        if name in "12":
            qtile.current_window.togroup(name, switch_group=False)
            qtile.focus_screen(0)
            qtile.groups_map[name].toscreen()
        else:
            qtile.current_window.togroup(name, switch_group=False)
            qtile.focus_screen(1)
            qtile.groups_map[name].toscreen()

    return _inner

for i in groups:
    keys.append(Key([mod, "shift"], i.name, lazy.function(go_to_group_and_move_window(i.name))))

### WIDGETS ###

widget_defaults = dict(
    font=bar_font,
    foreground=bar_foreground_color,
    fontsize=bar_fontsize,
)

extension_defaults = widget_defaults.copy()

# Decorations
powerlineR = {
    "decorations": [
        widget.decorations.PowerLineDecoration(path="back_slash")
    ]
}

powerlineL = {
    "decorations": [
        widget.decorations.PowerLineDecoration(path="forward_slash")
    ]
}

screen1 = [
    widget.TextBox(
        padding = 5,
        background=theme['alt_background']
    ),

    widget.GroupBox(
        fontsize=20,
        border_width=3,

        inactive=theme['disabled'],
        active=theme['accent'],

        highlight_color=bar_background_color,
        highlight_method="line",
        this_current_screen_border = theme['alt_background'],
        this_screen_border = theme['alt_background'],

        padding=10,
        **powerlineR,
        background=theme['alt_background'],
        visible_groups=['1', '2']
    ),

    widget.TextBox(
        text=" ",
        padding = 0,
        **powerlineR,
        background=theme['alt_background'],
    ),

    widget.CurrentLayoutIcon(
        padding = 10
    ),

    widget.WindowName(
        foreground=bar_foreground_color, 
        padding=20
    ),

    widget.TextBox(
        text=" ",
        padding = 0,
        **powerlineL,
        background=theme['background'],
    ),

    widget.CheckUpdates(
        colour_no_updates=bar_foreground_color,
        colour_have_updates=bar_foreground_color,
        no_update_string='No updates',
        **powerlineL,
        background=theme['alt_background'],
        padding=10
    ),

    widget.CPU(
        format="{load_percent}%",
        fmt=" 󰍛   {} ",
        **powerlineL,
        background=theme['background']
    ),

    widget.Memory(
        measure_mem="G",
        format="   {MemUsed: .2f}{mm} /{MemTotal: .2f}{mm} ",
        **powerlineL,
        background=theme['alt_background']
    ),

    widget.Clock(
        format=" %A %d %B %Y %H:%M ",
    ),

    widget.Systray(),

    widget.TextBox(
        **powerlineL,
        background=theme['background']
    ),

    widget.TextBox(
        ' ⏻',
        mouse_callbacks={
            'Button1': lazy.spawn(powermenu)
        },
        **powerlineL,
        background=theme['alt_background']
    ),

    widget.TextBox(
        padding = 0,
        background=theme['alt_background']
    ),
]

screen2 = [
    widget.TextBox(
        padding = 5,
        background=theme['alt_background']
    ),

    widget.GroupBox(
        fontsize=20,
        border_width=3,

        inactive=theme['disabled'],
        active=theme['accent'],

        highlight_color=bar_background_color,
        highlight_method="line",
        this_current_screen_border = theme['alt_background'],
        this_screen_border = theme['alt_background'],

        padding=10,
        **powerlineR,
        background=theme['alt_background'],
        visible_groups=['3', '4']
    ),

    widget.TextBox(
        text=" ",
        padding = 0,
        **powerlineR,
        background=theme['alt_background'],
    ),

    widget.CurrentLayoutIcon(
        padding = 10
    ),

    widget.WindowName(
        foreground=bar_foreground_color, 
        padding=20
    ),

    widget.Clock(
        format=" %A %d %B %Y %H:%M ",
    )
]

### SCREENS ###

screens = [
    Screen(
        top=bar.Bar(
            widgets= screen1,
            size=bar_size,
            background = bar_background_color,
            margin = [bar_top_margin, bar_right_margin, bar_bottom_margin-layouts_margin, bar_left_margin],
        ),
    ),

    Screen(
        top=bar.Bar(
            widgets= screen2,
            size=bar_size,
            background = bar_background_color,
            margin = [bar_top_margin, bar_right_margin, bar_bottom_margin-layouts_margin, bar_left_margin],
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
