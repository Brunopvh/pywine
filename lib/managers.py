#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from os import system
from lib.process import SysProcs

class PkgManager:

	def __init__(self, pkgs):
		self.pkgs = pkgs

		if not isinstance(self.pkgs, list): 
		  print('[!] Falha o(s) pacotes para instalação precisam ser passados em forma de uma lista.') 
		  print(__class__)
		  exit()

	def pacman(self):
		SysProcs('pacman').loop_process_run()
		
		for i in self.pkgs:
			print(f'Instalando: {i}')
			system(f'sudo pacman -S --needed --noconfirm {i}')

	def apt(self, arguments=False):

		# Gerar um loop enquanto outro processo 'apt install' estiver em execução.
		SysProcs('apt install').loop_process_run()
		SysProcs('apt.systemd').loop_process_run()
		SysProcs('dpkg install').loop_process_run()

		for i in self.pkgs:
			print(f'Instalando: {i}')
			if arguments == False:
				system(f'sudo apt install -y {i}')
			else:
				system(f'sudo apt install -y {arguments} {i}')