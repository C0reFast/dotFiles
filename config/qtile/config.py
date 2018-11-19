#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Drag, Group, Key, Match, Screen
import locale
import subprocess
import re

locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")


# Theme defaults
bar_defaults = dict(
    size=28,
    background=['#222222', '#111111'],
)

layout_defaults = dict(
    border_width=1,
    margin=0,
    border_focus='#336699',
    border_normal='#333333',
)

widget_defaults = dict(
    font='Sans',
    fontsize=14,
    padding=5,
    background=bar_defaults['background'],
    foreground=['#ffffff', '#ffffff', '#999999'],
    fontshadow='#000000',
)


class Widget(object):
    ''' Container for individual widget style options '''

    graph = dict(
        background='#000000',
        border_width=0,
        border_color='#000000',
        line_width=1,
        margin_x=0,
        margin_y=0,
        width=50,
    )

    groupbox = dict(
        active=widget_defaults['foreground'],
        inactive=['#444444', '#333333'],

        this_screen_border=layout_defaults['border_focus'],
        this_current_screen_border=layout_defaults['border_focus'],
        other_screen_border='#444444',

        urgent_text=widget_defaults['foreground'],
        urgent_border='#ff0000',

        highlight_method='block',
        rounded=True,

        # margin=-1,
        padding=3,
        borderwidth=2,
        disable_drag=True,
        invert_mouse_wheel=True,
    )

    sep = dict(
        foreground=layout_defaults['border_normal'],
        height_percent=100,
        padding=5,
    )

    systray = dict(
        icon_size=22,
        padding=5,
    )

    battery = dict(
        energy_now_file='charge_now',
        energy_full_file='charge_full',
        power_now_file='current_now',
    )

    battery_text = battery.copy()
    battery_text.update(
        charge_char='',  # fa-arrow-up
        discharge_char='',  # fa-arrow-down
        format='{char} {hour:d}:{min:02d}',
    )


# Commands to spawn
class Commands(object):
    browser = 'google-chrome'
    mail = 'thunderbird'
    dmenu = 'dmenu_run -i -b -p ">>>" -fn "-*-fixed-*-*-*-12-*-*-*-*" -nb "#15181a" -nf "#fff" -sb "#333" -sf "#fff"'
    file_manager = 'caja --no-desktop'
    lock_screen = 'mate-screensaver-command -l'
    screenshot = 'deepin-screenshot'
    terminal = 'mate-terminal'
    trackpad_toggle = "synclient TouchpadOff=$(synclient -l | grep -c 'TouchpadOff.*=.*0')"
    volume_up = 'amixer -q -c 0 sset Master 5dB+'
    volume_down = 'amixer -q -c 0 sset Master 5dB-'
    volume_toggle = 'amixer -q -D pulse sset Master 1+ toggle'


# Keybindings
mod = 'mod4'
keys = [
    # Window Manager Controls
    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'q', lazy.shutdown()),
    Key([mod, 'control'], 'l', lazy.spawn(Commands.lock_screen)),

    # Window Controls
    Key([mod], 'w', lazy.window.kill()),
    Key([mod], 'f', lazy.window.toggle_floating()),

    # Layout, group, and screen modifiers
    # Key([mod], 'j', lazy.layout.up()),
    # Key([mod], 'k', lazy.layout.down()),
    # Key([mod, 'shift'], 'j', lazy.layout.shuffle_up()),
    # Key([mod, 'shift'], 'k', lazy.layout.shuffle_down()),
    # Key([mod, 'shift'], 'g', lazy.layout.grow()),
    # Key([mod, 'shift'], 's', lazy.layout.shrink()),
    # Key([mod, 'shift'], 'n', lazy.layout.normalize()),
    # Key([mod, 'shift'], 'm', lazy.layout.maximize()),
    # Key([mod, 'shift'], 'space', lazy.layout.flip()),

    # Switch groups
    Key([mod], 'Left', lazy.screen.prev_group()),
    Key([mod], 'Right', lazy.screen.next_group()),
    # Key([mod], '`', lazy.screen.next_group()),

    # Cycle layouts
    Key([mod], 'Up', lazy.next_layout()),
    Key([mod], 'Down', lazy.prev_layout()),

    # Change window focus
    Key([mod], 'Tab', lazy.layout.next()),
    Key([mod, 'shift'], 'Tab', lazy.layout.previous()),

    # Switch focus to other screens
    Key([mod], 'h', lazy.to_screen(0)),  # left
    Key([mod], 'l', lazy.to_screen(1)),  # right

    # Commands: Application Launchers
    Key([mod], 'space', lazy.spawn(Commands.dmenu)),
    Key([mod], 'n', lazy.spawn(Commands.browser)),
    Key([mod], 'm', lazy.spawn(Commands.mail)),
    Key([mod], 'e', lazy.spawn(Commands.file_manager)),
    Key([mod], 'Return', lazy.spawn(Commands.terminal)),

    # Commands: Volume Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(Commands.volume_up)),
    Key([], 'XF86AudioLowerVolume', lazy.spawn(Commands.volume_down)),
    Key([], 'XF86AudioMute', lazy.spawn(Commands.volume_toggle)),

    Key([], 'XF86TouchpadToggle', lazy.spawn(Commands.trackpad_toggle)),

    # TODO: What does the PrtSc button map to?
    Key(['mod1', 'control'], 'a', lazy.spawn(Commands.screenshot)),     # Alt+Ctrl+A
]


# Groups
group_setup = (
    ('\uf120', {  # fa-terminal
        'layout': 'max',
        }),
    ('\uf121', {  # fa-code
        'layout': 'max',
        'matches': [Match(wm_class=('LiteIDE',))],
    }),
    ('\uf0ac', {  # fa-globe
        'layout': 'max',
        'matches': [Match(wm_class=('Firefox', 'Chromium', 'chrome'))],
    }),
    ('\uf10c', {  # fa-circle-o
        'layout': 'max',
    }),
    ('\uf192', {  # fa-dot-circle-o
        'layout': 'max',
        }),
    ('\uf111', {  # fa-circle
        'layout': 'max',
    }),
    ('\uf0e0', {  # fa-envelope
        'layout': 'max',
        'matches': [Match(wm_class=('Thunderbird',))],
    }),
)

groups = []
for idx, (label, config) in enumerate(group_setup):
    hotkey = str(idx + 1)
    config.setdefault('layout', 'tile')
    groups.append(Group(label, **config))

    # mod + hotkey = switch to group
    keys.append(Key([mod], hotkey, lazy.group[label].toscreen()))

    # mod + shift + hotkey = move focused window to group
    keys.append(Key([mod, 'shift'], hotkey, lazy.window.togroup(label)))


# Mouse
# mouse = (
#     Drag([mod], 'Button1', lazy.window.set_position_floating(),
#          start=lazy.window.get_position()),
#     Drag([mod], 'Button3', lazy.window.set_size_floating(),
#          start=lazy.window.get_size()),
# )
mouse = ()

# Screens
screens = [
    Screen(
        top=bar.Bar(widgets=[
            widget.GroupBox(**Widget.groupbox),
            widget.WindowName(),
            widget.CurrentLayout(),
        ], **bar_defaults),
    ),
    Screen(
        # bottom=bar.Bar(widgets=[Powerline()], **bar_defaults),
        top=bar.Bar(widgets=[
            widget.GroupBox(**Widget.groupbox),
            widget.WindowName(),

            widget.ThermalSensor(tag_sensor='Package id 0', update_interval=1),

            widget.CPUGraph(graph_color='#18BAEB', fill_color='#1667EB.3', **Widget.graph),
            widget.MemoryGraph(graph_color='#00FE81', fill_color='#00B25B.3', **Widget.graph),
            widget.SwapGraph(graph_color='#5E0101', fill_color='#FF5656', **Widget.graph),
            widget.HDDBusyGraph(device='sda', **Widget.graph),

            # widget.ThermalSensor(metric=False, threshold=158),
            widget.Sep(**Widget.sep),

            widget.CurrentLayout(),
            widget.Systray(**Widget.systray),
            widget.BatteryIcon(**Widget.battery),
            # widget.Battery(**Widget.battery_text),
            widget.Volume(theme_path='/usr/share/icons/Humanity/status/22/', cardid=1),
            # widget.YahooWeather(location='Fresno, CA', **Widget.weather),
            widget.Clock(format='%m-%d %A %I:%M'),
            ], **bar_defaults),
    ),
]


# Layouts
layouts = (
    layout.Tile(ratio=0.5, **layout_defaults),
    layout.Max(**layout_defaults),
    layout.RatioTile(**layout_defaults),
    layout.Matrix(**layout_defaults),
    layout.MonadTall(**layout_defaults),
    layout.Stack(**layout_defaults),
    layout.Zoomy(**layout_defaults),
)

floating_layout = layout.floating.Floating(
    auto_float_types=(
        'notification',
        'toolbar',
        'splash',
        'dialog',
    ),
    float_rules=[{'wmclass': x} for x in (
        'audacious',
        'Download',
        'dropbox',
        'file_progress',
        'file-roller',
        'gimp',
        'Komodo_confirm_repl',
        'Komodo_find2',
        'pidgin',
        'skype',
        'Transmission',
        'Update',  # Komodo update window
        'Xephyr',
        'QQ',
        'TXMenuWindow',
    )],
    **layout_defaults
)


def main(qtile):
    pass


@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True


def is_running(process):
    s = subprocess.Popen(["ps", "axuw"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process.encode(), x):
            return True
    return False


def execute_once(process):
    if not is_running(process):
        return subprocess.Popen(process.split())


# start the applications at Qtile startup
@hook.subscribe.startup
def startup():
    execute_once("fcitx")
    execute_once('nm-applet')
    execute_once('mate-screensaver')
    execute_once('feh -z --bg-fill --randomize --recursive /home/chenfu/Documents/Wallpapers')
    execute_once('cow')
