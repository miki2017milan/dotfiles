current=$(pamixer --get-default-sink)

if [[ ${current:14:1} == "1" ]]
then
    pacmd set-default-sink 2
    dunstify -h string:x-dunst-stack-tag:Volume "󰓃 Switched to Speakers!"
else
    pacmd set-default-sink 1
    dunstify -h string:x-dunst-stack-tag:Volume " Switched to Headphones!"
    
fi