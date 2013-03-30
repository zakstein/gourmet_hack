# System-wide .bashrc file for interactive bash(1) shells.

# To enable the settings / commands in this file for login shells as well,
# this file has to be sourced in /etc/profile.

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, overwrite the one in /etc/profile)
# PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '

# Commented out, don't overwrite xterm -T "title" -n "icontitle" by default.
# If this is an xterm set the title to user@host:dir
#case "$TERM" in
#xterm*|rxvt*)
#    PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME}: ${PWD}\007"'
#    ;;
#*)
#    ;;
#esac

# enable bash completion in interactive shells
#if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
#    . /etc/bash_completion
#fi

# sudo hint
if [ ! -e "$HOME/.sudo_as_admin_successful" ]; then
    case " $(groups) " in *\ admin\ *)
    if [ -x /usr/bin/sudo ]; then
	cat <<-EOF
	To run a command as administrator (user "root"), use "sudo <command>".
	See "man sudo_root" for details.
	
	EOF
    fi
    esac
fi

# if the command-not-found package is installed, use it
if [ -x /usr/lib/command-not-found -o -x /usr/share/command-not-found ]; then
	function command_not_found_handle {
	        # check because c-n-f could've been removed in the meantime
                if [ -x /usr/lib/command-not-found ]; then
		   /usr/bin/python /usr/lib/command-not-found -- $1
                   return $?
                elif [ -x /usr/share/command-not-found ]; then
		   /usr/bin/python /usr/share/command-not-found -- $1
                   return $?
		else
		   return 127
		fi
	}
fi

# Load /etc/bash_prompt, /etc/exports, /etc/aliases, /etc/functions and /etc/extra
# /etc/extra can be used for settings you don’t want to commit
for file in exports functions extra; do
	file="/etc/$file"
	[ -e "$file" ] && source "$file"
done

# Other aliases

# Easier navigation: .., ..., ~ and -
 alias ..="cd .."
 alias ...="cd ../.."
 alias ~="cd ~" # `cd` is probably faster to type though
 alias -- -="cd -"

# List all files colorized in long format, including dot files
alias la="ls -Gla"

# List only directories
alias lsd='ls -l | grep "^d"'

# Undo a `git push`
alias undopush="git push -f origin HEAD^:master"

# IP addresses
alias ip="dig +short myip.opendns.com @resolver1.opendns.com"
alias localip="ipconfig getifaddr en1"
alias ips="ifconfig -a | perl -nle'/(\d+\.\d+\.\d+\.\d+)/ && print $1'"

# Flush Directory Service cache
alias flush="dscacheutil -flushcache"

# View HTTP traffic
alias sniff="sudo ngrep -d 'en1' -t '^(GET|POST) ' 'tcp and port 80'"
alias httpdump="sudo tcpdump -i en1 -n -s 0 -w - | grep -a -o -E \"Host\: .*|GET \/.*\""

# Start an HTTP server from a directory
alias server="open http://localhost:8080/ && python -m SimpleHTTPServer 8080"

# Trim new lines and copy to clipboard
alias c="tr -d '\n' | pbcopy"

# Shortcuts
alias v="cd /vagrant"
alias p="cd /vagrant/puppet"
alias g="git"
alias ssa="sudo service apache2 restart"
alias vsnip="vim ~/.vim/vim-addons/snipmate-snippets/snippets/$1.vim"


# File size
alias fs="stat -f \"%z bytes\""

# ROT13-encode text. Works for decoding, too! ;)
alias rot13='tr a-zA-Z n-za-mN-ZA-M'


# One of @janmoesen’s ProTip™s
for method in GET HEAD POST PUT DELETE TRACE OPTIONS; do alias "$method"="lwp-request -m '$method'"; done

# @gf3’s Sexy Bash Prompt, inspired by "Extravagant Zsh Prompt"
# Shamelessly copied from https://github.com/gf3/dotfiles

if tput setaf 1 &> /dev/null; then
tput sgr0
	if [[ $(tput colors) -ge 256 ]] 2>/dev/null; then
	MAGENTA=$(tput setaf 9)
	ORANGE=$(tput setaf 172)
	GREEN=$(tput setaf 190)
	PURPLE=$(tput setaf 141)
WHITE=$(tput setaf 256)
	else
	MAGENTA=$(tput setaf 5)
	ORANGE=$(tput setaf 4)
	GREEN=$(tput setaf 2)
	PURPLE=$(tput setaf 1)
WHITE=$(tput setaf 7)
	fi
	BOLD=$(tput bold)
RESET=$(tput sgr0)
	else
	MAGENTA="\033[1;31m"
	ORANGE="\033[1;33m"
	GREEN="\033[1;32m"
	PURPLE="\033[1;35m"
	WHITE="\033[1;37m"
	BOLD=""
	RESET="\033[m"
	fi

	parse_git_dirty () {
		[[ $(git status 2> /dev/null | tail -n1) != "nothing to commit (working directory clean)" ]] && echo "*"
	}
parse_git_branch () {
	git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e "s/* \(.*\)/\1$(parse_git_dirty)/"
}

PS1="\[${BOLD}${MAGENTA}\]\u\[$WHITE\]@\[$ORANGE\]\h\[$WHITE\]:\[$GREEN\]\w\[$WHITE\]\$([[ -n \$(git branch 2> /dev/null) ]] && echo \" on \")\[$PURPLE\]\$(parse_git_branch)\[$WHITE\]\$ \[$RESET\]"
