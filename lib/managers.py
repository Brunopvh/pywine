#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from os import system
from lib.process import SysProcs

class ManagerPkgs:

	def __init__(self, pkgs):
		self.pkgs = pkgs

		if not isinstance(self.pkgs, list): 
		  print('[!] Falha o(s) pacotes para instalação precisam ser passados em forma de uma lista.') 
		  print(__class__)
		  exit()

	def pacman(self):

		SysProcs('vlc').loop_process_run()
		exit()
		
		for i in self.pkgs:
			print(f'Instalando: {i}')
			system(f'sudo pacman -S --needed --noconfirm {i}')


	def apt(self):
		for i in self.pkgs:
			print(f'Instalando: {i}')
			#system(f'sudo apt install -y {i}')