#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from os import system
from lib.colors import PrintColor

class PkgManager:

	def __init__(self, pkgs='False'):
		self.pkgs = pkgs
			
	def pkg_is_list(self):
		if isinstance(self.pkgs, list): 
			return 'True'
		else:
			print('[!] Falha o(s) pacotes para instalação precisam ser passados em forma de uma lista.') 
			print(__class__)
			return 'False'

	def pacman(self, arguments):
		if self.pkg_is_list() != 'True':
			return

		if arguments == '-S':
			for i in self.pkgs:
				print(f'Instalando: {i}')
				system(f'sudo pacman -S --needed --noconfirm {i}')

	def apt(self, arguments):
		if self.pkg_is_list() != 'True':
			return

		if arguments == 'install':
			for i in self.pkgs:
				PrintColor.yellow(f'Instalando: {i}')
				system(f'sudo apt install -y {i}')
		elif arguments == '--no-install-recommends':
			for i in self.pkgs:
				PrintColor.yellow(f'Instalando: {i}')
				system(f'sudo apt install -y --no-install-recommends {i}')
		elif arguments == 'remove':
			for i in self.pkgs:
				system(f'sudo apt remove {i}')



