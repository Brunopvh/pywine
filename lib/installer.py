#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import subprocess
import os
import sys
from time import sleep

from lib.os_info import OsInfo 
from lib.downloader import pywget as dow
from lib.managers import PkgManager  
from lib.yesno import YesNo
from lib.colors import PrintColor 

red = PrintColor.red
green = PrintColor.green
yellow = PrintColor.yellow
blue = PrintColor.blue
white = PrintColor.white
msg = PrintColor.msg

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
		PkgManager(programs_archlinux).pacman('-S')

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

		yellow('Adicioando suporte a arch i386')
		os.system('sudo dpkg --add-architecture i386')
		os.system('sudo apt update')
		PkgManager(programs_debian).apt('install')
		
		yn = YesNo('Deseja instalar gnome-exe-thumbnailer').input_yesno()
		if yn == 'True':
			PkgManager(gnome_wine).apt('--no-install-recommends')

#--------------------------| WineTricks |-------------------------#
	def winetricks_archlinux(self):
		if is_executable('wine') == 'False':
			self.wine()

		PkgManager(requeriments_winetricks).pacman('-S')
		PkgManager(requeriments_winetricks_suse).pacman('-S')
		PkgManager(['winetricks']).pacman('-S')

	def winetricks_debian(self):
		if is_executable('wine') == 'False':
			self.wine()

		PkgManager(requeriments_winetricks).apt('install')
		PkgManager(requeriments_winetricks_debian).apt('install')
		PkgManager(['winetricks']).apt('install')

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

	def q4wine(self):
		if self.os_id == 'arch':
			PkgManager(['q4wine']).pacman('-S')
		elif self.os_id == 'debian':
			PkgManager(['q4wine']).apt('install')