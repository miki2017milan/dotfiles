### EXPORT
export LC_ALL=C
export PATH="$HOME/bin:$PATH"

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

### PROMPT
# This is commented out if using starship prompt
# PS1='[\u@\h \W]\$ '

bind "set completion-ignore-case on"

### ALIASES ###
# navigation
alias ..='cd ..'

# Alias
alias ls='ls --color=auto'
alias la='ls -a'
alias ll='ls -l'

# For dotfiles
alias config='/usr/bin/git --git-dir=$HOME/dotfiles/ --work-tree=$HOME'

# adding flags
alias df='df -h'               # human-readable sizes
alias grep='grep --color=auto' # colorize output (good for log files)

# change your default USER shell
alias tobash="sudo chsh $USER -s /bin/bash && echo 'Log out and log back in for change to take effect.'"
alias tozsh="sudo chsh $USER -s /bin/zsh && echo 'Log out and log back in for change to take effect.'"
alias tofish="sudo chsh $USER -s /bin/fish && echo 'Log out and log back in for change to take effect.'"

# the terminal rickroll
alias rr='curl -s -L https://raw.githubusercontent.com/keroserene/rickrollrc/master/roll.sh | bash'

### SETTING THE STARSHIP PROMPT ###
eval "$(starship init bash)"

neofetch
