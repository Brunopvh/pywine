#!/bin/sh
#
# Instalador do script pywine
#

_c()
{
	if [ -z $2]; then
		printf "\033[1;$1m\n"
	elif [[ $2 ]]; then
		printf "\033[$2;$1m"
	fi
}

msg()
{
	echo "$@"
}

red()
{
	echo "$(_c 31)$@$(_c)"
}

green(){
	echo "$(_c 32)$@$(_c)"
}

space_line='=========================================='
github='https://github.com'
repo="$github/Brunopvh/pywine"
Curl=$(command -v curl 2> /dev/null)

if [ ! -x "$Curl" ]; then
	red "Instale a ferramenta ...................... curl"
	exit 1
fi

exit "$?"



