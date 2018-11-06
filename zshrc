# Created by newuser for 5.0.5
source ~/.shell_prompt.sh
source /etc/profile.d/autojump.zsh
alias ls='ls --color=auto'
alias ll='ls -l --color=auto'
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
autoload -U compinit
compinit

# bindkey '"\e\e":"\C-asudo \C-e"'

#关于历史纪录的配置 {{{
#历史纪录条目数量
export HISTSIZE=20000
#注销后保存的历史纪录条目数量
export SAVEHIST=20000
#历史纪录文件
export HISTFILE=~/.zhistory
#以附加的方式写入历史纪录
setopt INC_APPEND_HISTORY
#如果连续输入的命令相同，历史纪录中只保留一个
setopt HIST_IGNORE_DUPS
#为历史纪录中的命令添加时间戳
setopt EXTENDED_HISTORY      
 
#启用 cd 命令的历史纪录，cd -[TAB]进入历史路径
setopt AUTO_PUSHD
#相同的历史路径只保留一个
setopt PUSHD_IGNORE_DUPS
#自动cd到目录
setopt AUTO_CD
 
#在命令前添加空格，不将此命令添加到纪录文件中
#setopt HIST_IGNORE_SPACE
#}}}

export GOPATH=/home/chenfu/go
export PATH=$PATH:$GOPATH/bin

bindkey -s '\e\e' '\C-asudo \C-e'

# allow approximate
zstyle ':completion:*' completer _complete _match
zstyle ':completion:*:match:*' original only
# zstyle ':completion:*:approximate:*' max-errors 1 numeric

# tab completion for PID :D
zstyle ':completion:*:*:kill:*' menu yes select
zstyle ':completion:*:kill:*' force-list always
