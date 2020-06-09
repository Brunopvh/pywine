#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class YesNo:
	Red = '\033[0;31m'
	Yel = '\033[0;33m'
	Res = '\033[m'

	def __init__(self, text):
		self.text = text

	def input_yesno(self):
		yes_no = str(input(f'[?] {self.text} [{self.Yel}s{self.Res}/{self.Red}n{self.Res}]: '))
		yes_no = yes_no.lower().strip()

		if (yes_no == 's') or (yes_no == 'sim') or (yes_no == 'yes') or (yes_no == 'y'):
			return 'True'
		elif (yes_no == 'n') or (yes_no == 'nao') or (yes_no == 'no'):
			return 'False'
		else:
			print(f'{self.Red}[!]{self.Res} Opção inválida')
			return 'False'