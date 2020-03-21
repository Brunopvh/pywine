#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#--------------------------------------------------------#
# REQUERIMENTS
# python 3.6 ou superior
# wget (módulo do python3 - pip3 install wget)
#
#
VERSION = '2020-03-14'
#

import os, sys
import getpass
import platform 
import re
import subprocess
import socket
#import argparse
from time import sleep
from pathlib import Path

#----------------------------------------------------------#
# Endereço deste script no disco.
dir_root = os.path.dirname(os.path.realpath(__file__)) 

# Diretório onde o terminal está aberto.
dir_run = os.getcwd()        

# Inserir o diretório do script no PATH do python - print(sys.path)                          
sys.path.insert(0, dir_root) 

from modules.sys_info import *
from modules.colors import *

info = SysInfo()
os_id = info.get_id()
os_version = info.get_version()
os_codename = info.get_codename()
os_version_id = info.get_version_id()

# Importar o módulo wget para fazer download dos arquivos.
try:
	import wget
except:
	msg.white('Aguarde - instalado wget')
	# Checar se pip ou pip3 está instalado para poder instalar o módulo wget.
	if subprocess.getstatusoutput('which pip3')[0] == int('0'):
		os.system('pip3 install wget --user')
	elif subprocess.getstatusoutput('which pip') == int('0'):
		os.system('pip install wget --user')
	else:		
		msg.red('[!] Falha instale o gerenciador de pacotes do python3, [pip3] ou pip')
		msg.red('Você pode executar a instalação do módulo wget usando pip3 install wget.')
		sys.exit('1')

	# Tentar importar wget novamente.
	try:
		import wget
	except:
		print(' ')
		msg.red('[!] Falha não foi possível importar o módulo wget')
		sys.exit('1')


#----------------------------------------------------------#

# Necessário python 3.7 ou superior.
if platform.python_version()[0:3] < '3.6':
	print(f'\033[93m[!] Necessário ter python 3.6 ou superior instalado, saindo...\033[m\n')
	sys.exit('1')

space_line = '====================================================='

#----------------------------------------------------------#

# Verificar se o sistema e Linux.
if platform.system() != 'Linux':
	msg.red('[-] Seu sistema não é Linux.')
	sys.exit('1')

# Limpar a tela do console.
#os.system('clear')

# Usuário não pode ser "root"
if getpass.getuser() == 'root': 
	msg.red('Usuário não pode ser o [root]')
	sys.exit('1')

#----------------------------------------------------------#
# Ajuda
def usage():
	print(f"""
   Use: {os.path.basename(sys.argv[0])} --help|--version|--list|install

     --help                   Mostar ajuda.
     --version                Mostra versão.
     --list                   Mostra pacotes disponiveis para instalação.
     install <pacote>         Instala um pacote.
""")

	exit()

#----------------------------------------------------------#

if len(sys.argv) < 2:
	usage()

if len(sys.argv) >= int('2'):
	if sys.argv[1] == '--help':
		usage()
	elif sys.argv[1] == '--version':
		print(f'V{VERSION}')
		exit()

msg.white(f'Sistema: {os_id} {os_version_id}')

# Verificar conexão com a internet.
print('=> Aguardando conexão: ', end='')
a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
a.settimeout(4)
try:
	b = a.connect_ex(('www.google.com', 80))
	if b == 0:
		print(f'{Yellow}[+] Conectado{Reset}')
	else:
		print(f'{Red}[!] AVISO: você está off-line{Reset}')
		# Mostrar esta mensagem e prosseguir quando o usuário teclar enter.
		enter = input('Pressione enter ') 
except:
	print(f'{Red}[!] AVISO: você está off-line{Reset}')
	enter = input('Pressione enter ')

a.close()

#----------------------------------------------------------#

tup_requeriments_winetricks = (
	'zenity',
	'cabextract', 
	'unrar', 
	'unzip', 
	'wget', 
	'aria2', 
	'curl',
	'tor'
)

tup_requeriments_winetricks_debian = (
	'binutils', 
	'fuseiso', 
	'p7zip-full', 
	'policykit-1', 
	'xz-utils'
)

tup_requeriments_winetricks_suse = (
	'binutils', 
	'fuseiso', 
	'p7zip', 
	'polkit',  
	'xdg-utils',
	'xz'
)

# Lista de programas disponiveis para instalção.
tup_programs = (
	'formatfactory',
	'peazip',
	'wine',
	'winetricks',
	'winrar',
	'vlc',
	)

#----------------------------------------------------------#
# URLs
#----------------------------------------------------------#
url_key_libfaudio_buster = 'https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10/Release.key'
url_key_libfaudio_bionic = 'https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_18.04/Release.key'
url_key_winehq = 'https://dl.winehq.org/wine-builds/winehq.key'

url_winrar = 'http://www.rarlab.com/rar/winrar-x64-571br.exe'
url_burnaware = 'http://download.betanews.com/download/1212419334-2/burnaware_free_12.4.exe'
url_vlc = 'https://get.videolan.org/vlc/3.0.8/win32/vlc-3.0.8-win32.exe'
url_peazip = 'https://osdn.net/frs/redir.php?m=c3sl&f=peazip%2F71536%2Fpeazip-6.9.2.WIN64.exe'
url_ffactory = 'http://www.pcfreetime.com/public/FFSetup4.8.0.0.exe'
url_epsxe = 'http://www.epsxe.com/files/ePSXe205.zip' 

#----------------------------------------------------------#
# Repositórios
#----------------------------------------------------------#
repos_emulators_buster = 'deb https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10 ./'
repos_emulators_bionic = 'deb https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_18.04/ ./'
repos_wine_buster = 'deb https://dl.winehq.org/wine-builds/debian/ buster main'
repos_wine_bionic = 'deb https://dl.winehq.org/wine-builds/ubuntu/ bionic main'
repos_winetricks = 'https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks'

#----------------------------------------------------------#
# Diretórios.
#----------------------------------------------------------#
dir_home = Path.home()                       # Home do usuario
dir_bin = (f'{dir_home}/.local/bin')         # Local de binarios na home
dir_downloads = (f'{dir_home}/.cache/downloads')  # Cache temporário para downloads
dir_wine = (f'{dir_home}/.wine')             # Pasta dos aplicativos wine na home.
dir_drive_c = (f'{dir_wine}/drive_c')        #

tup_dirs = (dir_bin, dir_downloads)          # Tupla com diretórios.
for d in tup_dirs:
	if os.path.isdir(d) == False:
		os.makedirs(d)                       # Criar diretórios.

#----------------------------------------------------------#
# Arquivos
#----------------------------------------------------------#
Winetricks_Script = (f'{dir_bin}/winetricks')
wine_file_repos = '/etc/apt/sources.list.d/wine.list'
path_file_epsxe = (f'{dir_downloads}/{os.path.basename(url_epsxe)}')
path_file_ffactory = (f'{dir_downloads}/{os.path.basename(url_ffactory)}')
path_file_peazip = (f'{dir_downloads}/peazip-6.9.2.WIN64.exe')
path_file_winrar = (f'{dir_downloads}/{os.path.basename(url_winrar)}')
path_file_vlc = (f'{dir_downloads}/{os.path.basename(url_vlc)}')

#----------------------------------------------------------#
def config_cli_utils():
	"""
	Instalar utlitários necessarios
	"""
	if (os_id == 'debian') or (os_id == 'linuxmint') or (os_id == 'ubuntu'):
		# Instalar utilitários de linha de comando antes de prosseguir.
		msg.white('Necessário instalar os pacotes: dirmngr apt-transport-https gnupg gpgv2 gpgv')
		os.system("sudo sh -c 'apt update; apt install -y dirmngr apt-transport-https gnupg gpgv2 gpgv'")

#----------------------------------------------------------#
class Setup_Wine:
	"""
	Instalar o wine no sistema incluindo dependências
	https://forum.winehq.org/viewtopic.php?f=8&t=32192
	https://forum.winehq.org/viewtopic.php?t=32061
	https://forum.winehq.org/viewtopic.php?f=8&t=32192
	"""
	
	def wine_debian():
		"""
		Instalar wine apartir do repositório da distro.
		"""
		print(space_line)
		msg.white('Adicionando suporte a arch-i386')
		os.system('dpkg --add-architecture i386')

		msg.white('Instalando os pacotes: dirmngr apt-transport-https gnupg gpgv2 gpgv')
		os.system("sudo sh -c 'apt update; apt install -y dirmngr apt-transport-https gnupg gpgv2 gpgv'")

		print(space_line)
		msg.white('Instalando: wine')
		os.system('sudo apt install -y wine')

		print(space_line)
		msg.white('Instalando: wine32')
		os.system('sudo apt install -y install wine32')

		# Suporte a icones .exe do windows.
		print(space_line)
		msg.white('Instalando: gnome-colors-common gnome-wine-icon-theme gtk2-engines-murrine gnome-exe-thumbnailer')
		os.system(f'sudo apt install -y --no-install-recommends gnome-colors-common gnome-wine-icon-theme gtk2-engines-murrine')
		os.system(f'sudo apt install -y --no-install-recommends gnome-exe-thumbnailer')

	def wine_archlinux():
		# pacman -Ss wine
		print(space_line)
		msg.red('[!] Instale o wine manualmente visite o link abaixo para mais informações: ')
		msg.white('https://wiki.archlinux.org/index.php/Wine')
		sys.exit('1')

	def winetricks():
		"""
		Instalar o script winetricks na HOME.
		"""

		# Instalar requerimentos para sistemas baseado em debian
		if os.path.isfile('/etc/debian_version'):
			for c in tup_requeriments_winetricks:
				print(space_line)
				msg.yellow(f'Instalando: {c}')
				os.system(f'sudo apt install {c}')

		# Instalar requerimentos para sistemas RedHat.
		if which_pkg('dnf') == int('0'):
			for c in tup_requeriments_winetricks:
				print(space_line)
				msg.yellow(f'Instalando: {c}')
				os.system(f'sudo dnf install {c}')

			for c in tup_requeriments_winetricks_suse:
				print(space_line)
				msg.yellow(f'Instalando: {c}')
				os.system(f'sudo dnf install {c}')


		# Instalar requerimentos para sistemas RedHat.
		if which_pkg('zypper') == int('0'):
			for c in tup_requeriments_winetricks:
				print(space_line)
				msg.yellow(f'Instalando: {c}')
				os.system(f'sudo dnf install {tup_requeriments_winetricks}')

			for c in tup_requeriments_winetricks_suse:
				print(space_line)
				msg.yellow(f'Instalando: {c}')
				os.system(f'sudo dnf install {c}')


		# Instalar winetricks
		print(space_line)
		msg.yellow(f'Instalando winetricks')
		os.system(f'curl -SL {repos_winetricks} -o {Winetricks_Script}')

		if os.path.isfile(Winetricks_Script) == True:
			msg.yellow('[+] Sucesso')
			os.system(f'chmod a+x {Winetricks_Script}')
		else:
			msg.red('[!] Falha')
		
#----------------------------------------------------------#

def which_pkg(app):
	"""
	Usar o utilitário de linha de comando which para verificar 
	a existência de um executável qualquer.
	"""
	if (subprocess.getstatusoutput(f'which {app} 2> /dev/null')[0]) == int('0'):
		return int('0') # Sucesso, o pacote executável existe.
	else:
		return int('1') # Falha, não existe.

#----------------------------------------------------------#

def install_wine():
	"""
	Esta função verifica qual é o sistema atual (ubunt/fedora/mint) e em seguida instala o wine
	de acordo com o sistema.
	"""

	if (os_id == 'debian') or (os_id == 'ubuntu') or (os_id == 'linuxmint'):
		Setup_Wine.wine_debian()
		Setup_Wine.winetricks()

	elif os_id == 'fedora':
		os.system('sudo dnf install wine')

	elif os_id == 'arch':
		Setup_Wine.wine_archlinux()

	else:
		msg.red('Programa indisponível para seu sistema - tente instalar o wine manualmente.')
		sys.exit('1')

#----------------------------------------------------------#


#----------------------------------------------------------#
# Função para download dos arquivos
#----------------------------------------------------------#
def down(url, path_file):

	if os.path.isfile(path_file) == True:
		msg.white(f'Arquivo em cache [{path_file}]')
		return int('0')


	print(space_line)
	msg.white(f'Baixando [{url}]')
	msg.white(f'Destino [{path_file}]')

	try:
		wget.download(url, path_file)
		print(' OK')

	except(KeyboardInterrupt):
		msg.red('Interrompido com Ctrl c'); sleep(0.5)
		if os.path.isfile(path_file): 
			os.remove(path_file)
		exit()

	except:
		msg.red('Falha no download'); sleep(0.5)
		if os.path.isfile(path_file): 
			os.remove(path_file)
		exit()

#----------------------------------------------------------#
# Programas windows
#----------------------------------------------------------#
class WindPrograms:

	def epsxe():
		down(url_epsxe, path_file_epsxe)
		msg.yellow(f'epsxe baixado em: {path_file_epsxe}')

	def formatfactory():
		down(url_ffactory, path_file_ffactory)

	def office2007():
		msg.white('Necessário ter o CD ou arquivo de imagem para instalação [volume OFFICE12]')
		enter = input('Pressione enter: ')
		os.system('winetricks office2007pro')

	def peazip():
		down(url_peazip, path_file_peazip)
		os.system(f'wine {path_file_peazip}')
	
	def winrar():
		# Baixar é instalar o programa.
		down(url_winrar, path_file_winrar)
		os.system(f'wine {path_file_winrar}')

	def vlc():
		down(url_vlc, path_file_vlc)
		os.system(f'wine {path_file_vlc}')

#----------------------------------------------------------#

def install_programs(Arguments):

	# Verificar se o wine já está instalado, caso não esteja o usuario 
	# será indagado a respeito de instalação.
	if which_pkg('wine') != int('0'):
		print(space_line)
		sn = str(input('Necessário instalar o winehq-stable deseja proseguir [s/n]?: ').lower())
		if sn != 's':
			exit()

		install_wine()

	# Verificar se o winetricks já está instalado, caso não esteja o usuario 
	# será indagado a respeito de instalação.
	if which_pkg('winetricks') != int('0'):
		print(space_line)
		sn = str(input('Necessário instalar o script winetricks deseja proseguir [s/n]?: ').lower())
		if sn != 's':
			exit()

		Setup_Wine.winetricks()

	for c in Arguments:

		if c == 'office2007':        # Office 2007
			WindPrograms.office2007()
		elif c == 'peazip':            # Peazip
			WindPrograms.peazip()
		elif c == 'wine':              # Winehq-stable
			install_wine()
		elif c == 'winetricks':      # Winetricks
			Setup_Wine.winetricks()
		elif c == 'winrar':          # Winrar
			WindPrograms.winrar()    
		elif c == 'vlc':             # Vlc
			WindPrograms.vlc()
		else:
			msg.red(f'Programa indisponível: [{c}]')

#----------------------------------------------------------#
for c in sys.argv:
	if sys.argv[1] == 'install':
		install_programs(sys.argv[2:])

	elif sys.argv[1] == '--list':
		for c in tup_programs:
			print(f'    {c}')

	elif sys.argv[1] == '--upgrade':
		os.system(f'sh -c "{dir_root}/conf_pywine.sh"')

	else:
		msg.red(f'Comando não encontrado: {sys.argv[1]}')








