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
alias img='sxiv'

# fzf
alias cdf='cd $(fzf --walker dir,hidden)'
alias vimf='vim $(fzf)'
alias catf='cat $(fzf)'
alias imgf='sxiv $(fzf)'

# Better ls with eza
alias ls='eza -l'
alias la='eza -la'

# Adding flags
alias df='df -h'               # human-readable sizes
alias grep='grep --color=auto' # colorize output (good for log files)

# Change your default USER shell
alias tobash="sudo chsh $USER -s /bin/bash && echo 'Log out and log back in for change to take effect.'"
alias tozsh="sudo chsh $USER -s /bin/zsh && echo 'Log out and log back in for change to take effect.'"
alias tofish="sudo chsh $USER -s /bin/fish && echo 'Log out and log back in for change to take effect.'"

# Asthetic terminal things
alias rr='curl -s -L https://raw.githubusercontent.com/keroserene/rickrollrc/master/roll.sh | bash'
alias pipes='pipes.sh -t 4 -f 100'

### SETTING THE STARSHIP PROMPT ###
eval "$(starship init bash)"

neofetch
