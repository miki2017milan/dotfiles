#!/bin/bash
sudo xbacklight -dec 5
brigthness="$(xbacklight -get)"

dunstify -a "changeVolume/Brightness" -u low -h string:x-dunst-stack-tag:Volume/Brightness \
-h int:value:"$brigthness" " Brightness: ${brigthness}%"
