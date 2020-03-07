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


red "Testando vermelho"
green "Testando verde"


exit "$?"



