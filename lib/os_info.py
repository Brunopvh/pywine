#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# from os_info import *
# os_id = OsInfo.get_os_id
#
#

import os
import platform

# Versão python 3.6 ou superior
if platform.python_version() < '3.6':
	print('\033[0;31m[!] Necessário ter python 3.6 ou superior instalado em seu sistema\033[m')
	exit()

# Linux ou FreeBSD
if (platform.system() != 'Linux') and (platform.system() != 'FreeBSD'):
	print('Use esse módulo em Linux ou FreeBSD')
	exit()


if os.path.isfile('/usr/lib/os-release'):
	file_release = open('/usr/lib/os-release', 'rt').readlines()
elif os.path.isfile('/usr/local/etc/os-release'):
	file_release = open('/usr/local/etc/os-release', 'rt').readlines()
else:
	print('\033[0;31m[!] Arquivo os-release não encontrado, saindo\033[m')
	exit()


# Dicionario com os dados do arquivo os-release.
dict_release = {}

for x in file_release:
	x = x.replace('\n', '')
	x = str(x)
	x = x.replace('"', '').replace(' ', '')

	# Inserir cada informação relevante no dicionario.
	#
	if x[0:3] == 'ID=':                        # ID
		x = x.replace('ID=', '')
		dict_release['os_id'] = x
	elif x[0:11] == 'VERSION_ID=':             # VERSION_ID
		x = x.replace('VERSION_ID=', '')
		dict_release['os_version_id'] = x
	elif x[0:8] == 'ID_LIKE=':                 # ID_LIKE
		x = x.replace('ID_LIKE=', '')
		dict_release['os_id_like'] = x
	elif x[0:8] == 'VERSION=':                 # VERSION
		x = x.replace('VERSION=', '')  
		dict_release['os_version'] = x
	elif x[0:17] == 'VERSION_CODENAME=':       # VERSION_CODENAME
		x = x.replace('VERSION_CODENAME=', '')
		dict_release['os_codename'] = x
	elif x[0:5] == 'NAME=':                    # NAME
		x = x.replace('NAME=', '')
		dict_release['os_name'] = x

class OsInfo:
	
	def __init__(self, dict_release):
		self.dict_release = dict_release

	def get_os_id():
		if 'os_id' in dict_release:
			os_id = dict_release['os_id']
		else:
			os_id = 'NoNe'

		return os_id

	def get_os_codename():
		if 'os_codename' in dict_release:
			os_codename = dict_release['os_codename']
		else:
			os_codename = 'NoNe'

		return os_codename

	def get_os_version_id():
		if 'os_version_id' in dict_release:
			os_version_id = dict_release['os_version_id']
		else:
			os_version_id = 'NoNe'

		return os_version_id

	def get_os_id_like():
		if 'os_id_like' in dict_release:
			os_id_like = dict_release['os_id_like']
		else:
			os_id_like = 'NoNe'

		return os_id_like

	def get_os_version():
		if 'os_version' in dict_release:
			os_version = dict_release['os_version']
		else:
			os_version = 'NoNe'

		return os_version

	def get_os_name():
		if 'os_name' in dict_release:
			os_name = dict_release['os_name']
		else:
			os_name = 'NoNe'

		return os_name



