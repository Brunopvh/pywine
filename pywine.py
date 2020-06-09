#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pip3 install wget
#
# https://stackoverflow.com/questions/24180527/argparse-required-arguments-listed-under-optional-arguments
# https://stackoverflow.com/questions/15405636/pythons-argparse-to-show-programs-version-with-prog-and-version-string-formatt
#
#
#

import os, sys
import re
import subprocess
import tarfile
import tempfile
import shutil
import wget
import argparse
from platform import system as sys_kernel 
from getpass import getuser
from time import sleep
from pathlib import Path

__version__ = '2020-06-06'

#----------------------------------------------------------#

# Endereço deste script no disco.
dir_root = os.path.dirname(os.path.realpath(__file__)) 

# Diretório onde o terminal está aberto.
dir_run = os.getcwd()        

# Inserir o diretório do script no PATH do python - print(sys.path)                          
sys.path.insert(0, dir_root) 

from lib.os_info import OsInfo      # Detectar a distro e outras informações do sistema
from lib.colors import PrintColor   # Exibir mensagens personalizadas com cores
from lib.downloader import pywget as dow
from lib.managers import PkgManager  
from lib.yesno import YesNo

red = PrintColor.red
green = PrintColor.green
yellow = PrintColor.yellow
blue = PrintColor.blue
white = PrintColor.white
msg = PrintColor.msg

#----------------------------------------------------------#
# Verificações
#----------------------------------------------------------#
# root
if os.geteuid() == int('0'):
	red('Usuário não pode ser o root saindo')
	sys.exit('1')

# Linux
if (sys_kernel() != 'Linux') and (sys_kernel != 'FreeBSD'):
	red('Execute este program em sistemas Linux ou FreeBSD')
	exit()


#----------------------------------------------------------#
# URLs
#----------------------------------------------------------#
UrlWinetricks = 'https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks'
UrlPywinery = 'https://github.com/ergoithz/pywinery/releases/download/0.3.3/pywinery_0.3-3.tar.gz'

#----------------------------------------------------------#
# Listas e Tuplas
#----------------------------------------------------------#
requeriments_winetricks = [
	'zenity',
	'cabextract', 
	'unrar', 
	'unzip', 
	'wget', 
	'aria2', 
	'curl',
	'tor'
]

requeriments_winetricks_debian = [
	'binutils', 
	'fuseiso', 
	'p7zip-full', 
	'policykit-1', 
	'xz-utils'
]

requeriments_winetricks_suse = [
	'binutils', 
	'fuseiso', 
	'p7zip', 
	'polkit',  
	'xdg-utils',
	'xz'
]

def is_executable(exec):
	if int(subprocess.getstatusoutput(f'command -v {exec} 2> /dev/null')[0]) == int('0'):
		return 'True'
	else:
		return 'False'

class InstallerPrograms:
	
	def __init__(self, os_id=OsInfo.get_os_id()):
		self.os_id = os_id

#--------------------------| Wine |-------------------------#

	def wine_archlinux(self):
		'''
		Instalar wine no archlinux
		FONTES:
		   https://sempreupdate.com.br/veja-como-instalar-o-wine-4-5-no-arch-ubuntu-e-derivados/
		   https://www.archlinux.org/packages/multilib/x86_64/wine/
		   https://wiki.archlinux.org/index.php/Wine
		   https://github.com/ergoithz/pywinery
		
		pacman -Syu
		pacman -S wine wine_gecko wine-mono lib32-libpulse lib32-alsa-plugins lib32-mpg123 lib32-sdl
		sudo pacman -S --needed wine 
		'''
		programs_archlinux = [
			'wine', 
			'wine_gecko', 
			'wine-mono', 
			'lib32-libpulse', 
			'lib32-alsa-plugins', 
			'lib32-mpg123', 
			'lib32-sdl',
			]
		# Habilitar [multilib] no archlinux
		os.system(f'sudo {dir_root}/scripts/addrepo.py --repo archlinux')
		PkgManager(programs_archlinux).pacman()

	def wine_debian(self):
		'''
		Instalar o wine no sistema incluindo dependências
		https://forum.winehq.org/viewtopic.php?f=8&t=32192
		https://forum.winehq.org/viewtopic.php?t=32061
		https://forum.winehq.org/viewtopic.php?f=8&t=32192
		'''
		programs_debian = [
			'dirmngr', 
			'apt-transport-https', 
			'gnupg', 
			'gpgv2' ,
			'gpgv',
			'wine',
			'wine32',
		]

		gnome_wine = [
			'gnome-colors-common', 
			'gnome-wine-icon-theme', 
			'gtk2-engines-murrine',
			'gnome-exe-thumbnailer',
		]

		msg('Adicioando suporte a arch i386')
		os.system('sudo dpkg --add-architecture i386')
		os.system('sudo apt update')
		PkgManager(programs_debian).apt()
		
		yn = YesNo('Deseja instalar gnome-exe-thumbnailer').input_yesno()
		if yn == 'True':
			PkgManager(gnome_wine).apt('--no-install-recommends')

#--------------------------| WineTricks |-------------------------#
	def winetricks_archlinux(self):
		if is_executable('wine') == 'False':
			self.wine()

		PkgManager(requeriments_winetricks).pacman()
		PkgManager(requeriments_winetricks_suse).pacman()
		PkgManager(['winetricks']).pacman()

	def winetricks_debian(self):
		if is_executable('wine') == 'False':
			self.wine()

		PkgManager(requeriments_winetricks).apt()
		PkgManager(requeriments_winetricks_debian).apt()
		PkgManager(['winetricks']).apt()

#--------------------------| Executar Instalação |-------------------------#

	def wine(self):
		if self.os_id == 'arch':
			self.wine_archlinux()
		elif self.os_id == 'debian':
			self.wine_debian()

	def winetricks(self):
		if self.os_id == 'arch':
			self.winetricks_archlinux()
		elif self.os_id == 'debian':
			self.winetricks_debian()



parser = argparse.ArgumentParser(
			description='Instala o wine e programas relacionados em sistemas Linux.'
			)

parser.add_argument(
	'-v', '--version', 
	action='version', 
	version=(f"%(prog)s {__version__}")
	)

parser.add_argument(
	'-l', '--list',
	action='store_true', 
	dest='list_all_apps', # Argumento que não será passado para opção -l/--list.
	help='Mostra programas disponíveis para instalação'
	)
	
parser.add_argument(
	'-i', '--install', 
	action='store', 
	dest='pkg_for_install',
	type=str,
	help='Instalar um pacote'
	)

args = parser.parse_args()

#----------------------------------------------------------#
# Execução
#----------------------------------------------------------#
if args.list_all_apps:
	print('wine')
	print('winetricks')
elif args.pkg_for_install:
	msg(f'{os.path.basename(sys.argv[0])} {__version__}')

	if args.pkg_for_install == 'wine':
		InstallerPrograms().wine()
	elif args.pkg_for_install == 'winetricks':
		InstallerPrograms().winetricks()
