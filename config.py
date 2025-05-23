from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [
    # Movement
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Window shuffling
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Resize for MonadTall
    #Key([mod, "control", "shift"], "j", lazy.layout.shrink(), desc="Shrink window down"),
    #Key([mod, "control", "shift"], "k", lazy.layout.grow(), desc="Grow window up"),
    #Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Resize for Columns
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow down (Columns only)"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow up (Columns only)"),

    # Window management
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle split layout"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "b", lazy.spawn("firefox"), desc="Launch browser"),
    Key([mod, "shift"], "m", lazy.window.toggle_minimize(), desc="Minimize window"),
    
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
                "border_width": 4,
                "margin": 8,
                "border_focus": "#d65d0e",
                "border_normal": "#3d3d3d"
            }

gruvbox_colors = {
    "dark_bg": "#282828",      # Dark background for bar
    "light_bg": "#ebdbb2",     # Light background (for text and widgets)
    "red": "#fb4934",          # Red
    "green": "#b8bb26",        # Green
    "yellow": "#fabd2f",       # Yellow
    "blue": "#83a598",         # Blue
    "purple": "#d3869b",       # Purple
    "aqua": "#8ec07c",         # Aqua
    "orange": "#fe8019",       # Orange
    "text": "#ebdbb2",         # Light text color
    "inactive_group": "#7c6f64", # Inactive group color
    "active_group": "#83a598", # Active group color
    "border": "#504945",       # Border color for the bar
}


layouts = [
    layout.Columns(
            border_focus="#d65d0e",
            border_normal="#3d3d3d",
            border_focus_stack=gruvbox_colors["blue"],
            border_width=4,
            margin=8,
            border_on_single=True
            )
    #layout.MonadTall(**layout_theme),
    #layout.MonadWide(**layout_theme),
    #layout.Floating(**layout_theme),
    #layout.Max(**layout_theme)

]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()



screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(
                    foreground="#ffffff",  # White text for layout
                    background="#282828",  # Dark background for layout widget
                    padding=10,
                ),
                widget.GroupBox(
                    font="Ubuntu",
                    fontsize=12,
                    padding=5,
                    active=gruvbox_colors["active_group"],
                    inactive=gruvbox_colors["inactive_group"],
                    highlight_method="block",
                    blockhighight_text_color=gruvbox_colors["text"],  # Active group text color
                    this_current_screen_border=gruvbox_colors["border"],  # Border color for active group
                    this_screen_border=gruvbox_colors["border"],  # Border color for current screen
                    order=["1", "2", "3", "4", "5"],
                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p', foreground=gruvbox_colors["aqua"]),
                widget.Systray(),
                widget.Battery(
                  format='{char} {percent:2.0%}',
                  charge_char='󰂄',
                  discharge_char='󰁹',
                  empty_char='󰂎',
                  full_char='󱊣',
                  update_interval=30,
                  show_short_text=False,
              ),
            ],
            24,  # Height of the bar
            background=gruvbox_colors["dark_bg"],  # Background color of the bar
            foreground=gruvbox_colors["text"],  # Text and widget foreground color
            border_width=2,  # Width of the bar's border
            border_color=gruvbox_colors["border"],  # Border color of the bar

        ),
               # set wallpaper 
               wallpaper= '~/Pictures/wp.png',
               wallpaper_mode='stretch'


    ),

]



# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

import os
import subprocess
from libqtile import hook

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])


# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "QTile"
