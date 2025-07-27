#!/usr/bin/env bash

xrandr -s 1920x1080 

setxkbmap -layout "us,ru,ge" -option "grp:alt_shift_toggle"

nm-applet &

volumeicon & 

blueman-applet &

dunst
