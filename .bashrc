# some more ls aliases
alias edt='emacs -nw ~/.bashrc'
alias edm='em ~/.tmux.conf'
alias em='emacs -nw'
alias sem='sudo emacs -nw'
alias l='ls -vxCF --color=auto'
alias lsd='ls -vxCFd */'
alias ll='ls -lhvF --color=auto'
alias lt='ls -alhvFtr --color=auto'
alias df='df -h'
alias du='du -h'

alias td='tree -d'

alias less='less -S'
alias lest='less $(\ls -v1td *.* | head -1)'
alias vdl='vd $(\ls -v1td *.* | head -1)'

alias wt="watch \"ls -alth\""

function cv() { column -ts $'\t' $1 |less;}
function cvc() { column -ts $',' $1 |less;}
function l5() { h5dump $1 |less;}

function scpi() { scp -r ycho@220.125.199.66:$1 . ;}
function scpo() { scp -r $1 ycho@220.125.199.66:~/getdata ;}

function ngh() { ngrok http $1;}

# directory
alias cdp='cd ~/program'
alias cda='cd $(\ls -v1td */ | head -1)'

# For tmux
alias tl='tmux ls'
alias t0='tmux attach -t 0'
alias t1='tmux attach -t 1'
alias t2='tmux attach -t 2'
alias t3='tmux attach -t 3'
alias t4='tmux attach -t 4'
alias t5='tmux attach -t 5'
alias t6='tmux attach -t 6'
alias t7='tmux attach -t 7'
alias t8='tmux attach -t 8'
alias t9='tmux attach -t 9'

alias inet='google-chrome-stable'

export DISPLAY="`grep nameserver /etc/resolv.conf | sed 's/nameserver //'`:0"
export LIBGL_ALWAYS_INDIRECT=1

HISTFILESIZE=1000000
HISTSIZE=10000
