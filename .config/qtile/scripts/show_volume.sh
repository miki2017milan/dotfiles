#!/bin/bash
volume="$(pamixer --get-volume)"

if $(pamixer --get-mute)
then
    dunstify -a "changeVolume/Brightness" -u low -h string:x-dunst-stack-tag:Volume/Brightness \
-h int:value:"$volume" "󰝟 Volume: ${volume}% (muted)"
else
    dunstify -a "changeVolume/Brightness" -u low -h string:x-dunst-stack-tag:Volume/Brightness \
-h int:value:"$volume" "󰕾 Volume: ${volume}%"
fi
