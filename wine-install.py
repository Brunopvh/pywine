#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import argparse
from platform import system as sys_kernel 
from getpass import getuser

__version__ = '2020-08-09'

# Endereço deste script no disco.
dir_root = os.path.dirname(os.path.realpath(__file__)) 

# Nome do script/app
app_name = os.path.basename(__file__)

# Diretório onde o terminal está aberto.
dir_run = os.getcwd()        

# Inserir o diretório do script no PATH do python - print(sys.path)                          
sys.path.insert(0, dir_root)

#from lib.processloop import ProcessLoop
from lib.print_text import PrintText
from lib.installer import InstallerPrograms


# Default
CRed = '\033[0;31m'
CGreen = '\033[0;32m'
CYellow = '\033[0;33m'
CBlue = '\033[0;34m'
CWhite = '\033[0;37m'


# Strong
CSRed = '\033[1;31m'
CSGreen = '\033[1;32m'
CSYellow = '\033[1;33m'
CSBlue = '\033[1;34m'
CSWhite = '\033[1;37m'


# Dark
CDRed = '\033[2;31m'
CDGreen = '\033[2;32m'
CDYellow = '\033[2;33m'
CDBlue = '\033[2;34m'
CDWhite = '\033[2;37m'



# Blinking text
CBRed = '\033[5;31m'
CBGreen = '\033[5;32m'
CBYellow = '\033[5;33m'
CBBlue = '\033[5;34m'
CBWhite = '\033[5;37m'

# Reset
CReset = '\033[0m'

# root
if os.geteuid() == int('0'):
	red('Usuário não pode ser o root saindo')
	sys.exit('1')

# Linux
if (sys_kernel() != 'Linux') and (sys_kernel != 'FreeBSD'):
	red('Execute este program em sistemas Linux ou FreeBSD')
	exit()


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
	PrintText().line()
	print(f'[{os.path.abspath(os.path.join(dir_root, app_name))}]', end=' ')
	print(f'[Versão {__version__}]')
	PrintText().line()

	if args.pkg_for_install == 'q4wine':
		InstallerPrograms().q4wine()
	elif args.pkg_for_install == 'wine':
		InstallerPrograms().wine()
	elif args.pkg_for_install == 'winetricks':
		InstallerPrograms().winetricks()
	elif args.pkg_for_install == 'pywinery':
		InstallerPrograms().pywinery()