#!/usr/bin/env bash
#
# Instalador do script pywine
# https://github.com/Brunopvh/pywine.git
#
#--------------------| INSTALAÇÃO |-----------------------------#
# curl -sSL https://raw.github.com/Brunopvh/pywine/master/conf_pywine.sh -o- | bash
# wget -q https://raw.github.com/Brunopvh/pywine/master/conf_pywine.sh -O- | bash 
# 
#

#-------------------------------------------------------#
# URLs
#-------------------------------------------------------#
url_master_storecli='https://raw.github.com/Brunopvh/storecli/master'
url_master_pywine='https://github.com/Brunopvh/pywine/archive/master.zip'
url_conf_path="$url_master_storecli/scripts/conf_path.sh"
url_unpack="$url_master_storecli/scripts/UnPack.sh"
url_colors="$url_master_storecli/lib/Colors.sh"

#-------------------------------------------------------#
# Diretórios
#-------------------------------------------------------#
DirTemp="/tmp/ConfPywine_$USER"
DirUnpack="$DirTemp/unpack_files"
DirPywine="$HOME/.local/bin/pywine-amd64"
mkdir -p "$DirPywine" "$DirTemp" "$DirUnpack"

# Criar o diretório ~/.local/bin se não existir
if ! [[ -d "$HOME/.local/bin" ]]; then
	mkdir "$HOME/.local/bin"
fi

# Inserir o diretório ~/.local/bin em PATH se não existir.
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
	echo -e "Inserindo [$HOME/.local/bin] na variável PATH de [$USER]"
	PATH="$HOME/.local/bin:$PATH"
fi

#-------------------------------------------------------#
# Arquivos
#-------------------------------------------------------#
File_conf_path="$DirTemp/conf_path.sh"
File_pywine_zip="$DirTemp/pywine.zip"

function WHICH()
{
	if [[ -x $(which "$1" 2> /dev/null) ]]; then
		printf "[+] .............................. $1\n"
		return 0
	else
		printf "\033[1;31m[!]\033[1;m .............................. $1\n"
		return 1
	fi
}

if ! WHICH 'curl'; then
	printf "Instale a ferramenta: curl\n"
	exit 1
fi

if ! WHICH 'unzip'; then
	printf "Instale a ferramenta: unzip\n"
	exit 1
fi

#-------------------------------------------------------#
function dow()
{
	# $1 = url
	# $2 = file

	if [[ -f "$1" ]]; then
		rm -rf  "$1"
	fi

	printf "Baixando [$1]\n"
	printf "Destino [$2]\n"
	if ! curl -SL "$1" -o "$2"; then
		printf "\033[1;31m[!] Falha no download\033[1;m\n"
	fi
}

#-------------------------------------------------------#
function Config_bash()
{
	# Criar o arquivo ~/.bashrc se não existir
	if [[ ! -f "$HOME/.bashrc" ]]; then
		echo ' ' >> "$HOME/.bashrc"
	fi

	# Configurar o arquivo ~/.bashrc
	if ! grep -q "^export.*$HOME/.local/bin.*" "$HOME/.bashrc"; then
		echo "Adicionando [$HOME/.local/bin] em PATH [$HOME/.bashrc]"
		echo -e "export PATH=$HOME/.local/bin:$PATH" >> "$HOME/.bashrc"
	fi

	bash -c ". $HOME/.bashrc"
}

#-------------------------------------------------------#
function Config_zsh()
{
	# zshell não instalado.
	Zshell=$(command -v zsh 2> /dev/null)
	if [[ ! -x "$Zshell" ]]; then
		return 0
	fi

	# Criar o arquivo ~/.zshrc se não existir
	if [[ ! -f "$HOME/.zshrc" ]]; then
		echo ' ' >> "$HOME/.zshrc"
	fi

	# Configurar o arquivo ~/.zshrc
	if ! grep -q "^export.*$HOME/.local/bin.*" "$HOME/.zshrc"; then
		echo "Adicionando [$HOME/.local/bin] em PATH [$HOME/.zshrc]"
		echo -e "export PATH=$HOME/.local/bin:$PATH" >> "$HOME/.zshrc"
	fi

	zsh -c ". ~/.zshrc"
}

#-------------------------------------------------------#
function conf_path()
{
	Config_bash || return 1
	Config_zsh || return 1
}

#-------------------------------------------------------#
function unpck()
{
	cd "$DirUnpack" && rm -rf *

	printf "Descomprimindo [$1]\n"
	printf "Destino [$DirUnpack]\n"
	unzip "$1" -d "$DirUnpack" 1> /dev/null
}

#-------------------------------------------------------#
function install_pywine(){
	printf "Instalando\n"
	cd "$DirPywine" && rm -rf *
	cd "$DirUnpack/pywine-master"
	mv -v * "$DirPywine/"
	ln -sf "$DirPywine/pywine.py" "$HOME/.local/bin/pywine"
	chmod -R a+x "$DirPywine"
	chmod -R a+x "$HOME/.local/bin/pywine"
}
#-------------------------------------------------------#

function main()
{
	dow "$url_master_pywine" "$File_pywine_zip" || return 1
	unpck "$File_pywine_zip" || return 1
	install_pywine
	conf_path || return 1
}

#-------------------------------------------------------#
main || exit 1

