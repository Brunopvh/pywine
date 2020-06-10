#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pip3 install wget
#
# https://stackoverflow.com/questions/24180527/argparse-required-arguments-listed-under-optional-arguments
# https://stackoverflow.com/questions/15405636/pythons-argparse-to-show-programs-version-with-prog-and-version-string-formatt
#
#
#

import os
import sys
import re
import argparse
from platform import system as sys_kernel 
from getpass import getuser
from pathlib import Path

__version__ = '2020-06-10'

#----------------------------------------------------------#

# Endereço deste script no disco.
dir_root = os.path.dirname(os.path.realpath(__file__)) 

# Diretório onde o terminal está aberto.
dir_run = os.getcwd()        

# Inserir o diretório do script no PATH do python - print(sys.path)                          
sys.path.insert(0, dir_root) 

from lib.os_info import OsInfo      # Detectar a distro e outras informações do sistema
from lib.colors import PrintColor   # Exibir mensagens personalizadas com cores
from lib.installer import InstallerPrograms 

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
	print('q4wine')
	print('wine')
	print('winetricks')
elif args.pkg_for_install:
	msg(f'{os.path.basename(sys.argv[0])} {__version__}')

	if args.pkg_for_install == 'q4wine':
		InstallerPrograms().q4wine()
	elif args.pkg_for_install == 'wine':
		InstallerPrograms().wine()
	elif args.pkg_for_install == 'winetricks':
		InstallerPrograms().winetricks()
