#!/bin/bash
volume="$(pamixer --get-volume)"

if $(pamixer --get-mute)
then
    dunstify -a "changeVolume" -u low -i audio-volume-high -h string:x-dunst-stack-tag:Volume \
-h int:value:"$volume" "󰝟 Volume: ${volume}% (muted)"
else
    dunstify -a "changeVolume" -u low -i audio-volume-high -h string:x-dunst-stack-tag:Volume \
-h int:value:"$volume" "󰕾 Volume: ${volume}%"
fi

