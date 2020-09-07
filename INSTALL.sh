#!/bin/sh
#
__version__='2020-09-06'
#
# sh -c "$(curl -fsSL https://raw.github.com/Brunopvh/pywine/master/INSTALL.sh)"
#
#----------------------------------------------#
# Instaldor do script pywine
#----------------------------------------------#
#
#

url_pywine='https://github.com/Brunopvh/pywine/archive/master.tar.gz'
url_pywine_installer='https://raw.github.com/Brunopvh/pywine/master/INSTALL.sh'

_msg()
{
	printf '%s\n' "=> $@"
}

_red()
{
	printf "\033[0;31m $@\033[m\n"
}

is_executable()
{
	pkg=$(command -v "$1" 2> /dev/null)
	if [ -x "$pkg" ]; then
		return 0
	else
		return 1
	fi
}

if ! [ `id -u` -eq 0 ]; then
	_red "Você precisa ser o 'root'"
	exit 1
fi

[ ! -d /usr/local/bin ] && mkdir -p /usr/local/bin
[ ! -d /opt ] && mkdir -p /opt

temp_dir=$(mktemp --directory)
if [ ! -d "$temp_dir" ]; then
	temp_dir="/tmp/temp_$USER"
	mkdir -p "$temp_dir"
fi

cd "$temp_dir"

download_pywine()
{
	_msg "Baixando ... $url_pywine"
	_msg "Destino ... $(pwd)/pywine.tar.gz"
	if is_executable curl; then
		curl -S -L "$url_pywine" -o 'pywine.tar.gz' || return 1
	elif is_executable wget; then
		wget "$url_pywine" -O 'pywine.tar.gz' || return 1
	fi
	return 0
}

clean()
{
	if [ -d "$temp_dir" ]; then
		_msg "Limpando ... $temp_dir"
		rm -rf "$temp_dir"
	fi
}

remove_pywine()
{
	if [ -d /opt/pywine-amd64 ]; then
		printf '%s\n' "Removendo ... /opt/pywine-amd64"
		rm -rf /opt/pywine-amd64
	fi

	if [ -e /usr/local/bin/wine-install ]; then
		printf '%s\n' "Removendo ... /usr/local/bin/wine-install"
		rm -rf /usr/local/bin/wine-install
	fi
}

install_pywine()
{
	remove_pywine
	printf '%s' "Descompactando pywine.tar.gz "
	if tar -zxvf pywine.tar.gz 1> /dev/null; then
		printf '%s\n' "[OK]"
	else
		_red "Falha na descompressão."
		return 1
	fi
	
	mv pywine-master pywine-amd64
	cp -R pywine-amd64 /opt/
	chmod a+x /opt/pywine-amd64/wine-install.py 
	ln -sf /opt/pywine-amd64/wine-install.py /usr/local/bin/wine-install
	_msg "Criando link ... /usr/local/bin/wine-install"
}

main()
{
	if ! download_pywine; then
		_red "Falha no download"
		return 1
	fi


	if ! install_pywine; then
		_red "Falha na instalação"
		return 1
	fi

	if is_executable wine-install; then
		printf '%s\n' "wine-install instalado com sucesso."
	else
		_red "Falha na insalação de wine-install."
	fi
}


if main; then
	clean
	exit 0
else
	clean
	exit 1
fi

