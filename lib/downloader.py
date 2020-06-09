#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from os import remove, path

class pywget:

	def __init__(self, url, file=''):
		self.url = url
		self.file = file

	def bar_custom(self, current, total, width=80):
		# https://pt.stackoverflow.com/questions/207887/como-imprimir-texto-na-mesma-linha-em-python
		# print('\033[K[>] Progresso: %d%% [%d / %d]MB ' % (progress, current, total), end='\r')
		#
		current = current / 1048576        # Converter bytes para MB
		total = total / 1048576            # Converter bytes para MB
		progress = (current / total) * 100 # Percentual

		if progress == '100':
			print('[>] Progresso: %d%% [%d / %d]MB ' % (progress, current, total))

		print('\033[K[>] Progresso: %d%% [%d / %d]MB ' % (progress, current, total), end='\r')

	def run_download(self):
		'''
		wget.download(url, out=None, bar=<function bar_adaptive at 0x7f7fdfed9d30>)
		wget.download(url, out=None, bar=bar_adaptive(current, total, width=80))
		'''
		import wget

		if path.isfile(self.file):
			print(f'[>] Arquivo encontrado: {self.file}')
			return

		print(f'[>] Baixando: {self.url}')
		print(f'[>] Destino: {self.file}')
		try:
			wget.download(self.url, self.file, bar=self.bar_custom)
			print('OK ')
		except(KeyboardInterrupt):
			print(' ')
			print('\033[0;31m[!] Interrompido com Ctrl c\033[m') 
			sleep(0.25)
			if path.isfile(self.file): 
				remove(self.file)
				exit()
		except:
			print('\n')
			print('\033[0;31m[!] Falha no download\033[m')
			if path.isfile(self.file):
				remove(self.file)


