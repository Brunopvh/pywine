#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from subprocess import getstatusoutput
from time import sleep

class SysProcs:

	def __init__(self, proc):
		self.proc = str(proc)
	
	def search_name_process(self):
		return str(getstatusoutput(f'ps aux | grep -m 1 {self.proc}')[1].split()[10])

	def search_pid_process(self):
		return int(getstatusoutput(f'ps aux | grep -m 1 {self.proc}')[1].split()[1])
		
	def loop_process_run(self):
		'''
		Verificar se o processo está em execução no sistema, caso não estiver
		em execução a função encerra aqui.
		'''
		if not (self.proc in self.search_name_process()):
			return

		chars = ('\\', '|', '/', '-')
		num = int('0')
		while True:
			if not (self.proc in self.search_name_process()):
				print(f'Aguardando processo ({Name}) com pid ({Pid}) finalizado [{Char}]', end=' ')
				print('\033[0;33mFinalizado\033[m')
				break

			Name = self.search_name_process()
			Pid = self.search_pid_process()
			Char = chars[num]
			print(f'\033[KAguardando processo ({Name}) com pid ({Pid}) finalizar [{Char}]', end='\r')
			
			if num == int('3'):
				num = int('0')
			num += 1
			sleep(0.25)

