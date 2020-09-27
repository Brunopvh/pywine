#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import tempfile
import tarfile
import platform
import shutil
import urllib.request
from pathlib import Path

from lib.print_text import PrintText
from lib.apt_get import AptGet 
from lib.pacman import Pacman
from lib.os_release import ReleaseInfo

TempDir = tempfile.mkdtemp()

# Winetricks requeriments
requeriments_winetricks = 'zenity cabextract unrar unzip wget'
requeriments_winetricks_debian = 'binutils fuseiso p7zip-full policykit-1 xz-utils'
requeriments_winetricks_suse = 'binutils fuseiso p7zip polkit xdg-utils xz'

# Wine debian requeriments.
requeriments_wine_debian = 'wine-stable-i386 wine-stable-amd64 wine-stable winehq-stable'

def is_executable(exec):
	if int(subprocess.getstatusoutput(f'command -v {exec} 2> /dev/null')[0]) == int('0'):
		return 'True'
	else:
		return 'False'

def mkdir(path):
        try:
            if not os.path.exists(path):
                os.makedirs(path, 0o700)
                return True
        except Exception as erro:
            print("[!] Não foi possível criar o diretório: {0}".format(path))
            print(erro)
            return False

        if not os.access(path, os.W_OK):
            print("[!] Você não tem permissão de escrita em: {0}".format(path))
            return False

        return True

class InstallerPrograms(PrintText):
	def __init__(self):
		if platform.system() == 'FreeBSD':
			self.user_home = os.path.abspath(os.path.join('/usr', Path.home()))
		else:
			self.user_home = Path.home()

		self.user_bin = os.path.abspath(os.path.join(self.user_home, '.local', 'bin'))
		self.winetricks_script = os.path.abspath(os.path.join('/usr/local/bin', 'winetricks'))
		if os.path.isdir(self.user_bin) == False:
			mkdir(self.user_bin)	

	def broke(self):
		os.system('sudo apt --fix-broken install')
		os.system('sudo dpkg --configure -a')
		os.system('sudo apt update')

	def wine_debian(self):
		'''
		https://forum.winehq.org/viewtopic.php?f=8&t=32192
		'''
		codename = ReleaseInfo().info('VERSION_CODENAME')
		
		repo_wine_debian_buster = 'deb https://dl.winehq.org/wine-builds/debian/ buster main'
		repo_wine_ubuntu_bionic = 'deb https://dl.winehq.org/wine-builds/ubuntu/ bionic main'
		repo_libfaudio_debian_buster = 'deb https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10 ./'
		repo_libfaudio_ubuntu_bionic = 'deb https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_18.04/ ./'
		url_key_wine_stable = 'https://dl.winehq.org/wine-builds/winehq.key'
		url_key_libfaudio_debian_buster = 'https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10/Release.key'
		url_key_libfaudio_ubuntu_bionic = 'https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_18.04/Release.key'

		# Adicionar key wine-stable.
		self.msg('Adicionando winehq.key para wine-stable aguarde...')
		os.chdir(TempDir)
		urllib.request.urlretrieve(url_key_wine_stable, 'winehq.key')
		os.system('sudo apt-key add winehq.key')

		# Adicionar key para libf-audio.
		self.msg('Adicionando key para libfaudio aguarde...')
		if codename == 'buster':
			urllib.request.urlretrieve(url_key_libfaudio_debian_buster, 'Release-buster.key')
			os.system('sudo apt-key add Release-buster.key')
		elif (codename == 'bionic') or (codename == 'tricia'):
			urllib.request.urlretrieve(url_key_libfaudio_ubuntu_bionic, 'Release-bionic.key')
			os.system('sudo apt-key add Release-bionic.key')

		self.msg('Adicionando repositórios para wine-stable e libfaudio')
		if codename == 'buster':
			os.system(f'echo "{repo_wine_debian_buster}" | sudo tee /etc/apt/sources.list.d/wine.list')
			os.system(f'echo "{repo_libfaudio_debian_buster}" | sudo tee /etc/apt/sources.list.d/libfaudio.list')
		elif (codename == 'bionic') or (codename == 'tricia'):
			os.system(f'echo "{repo_wine_ubuntu_bionic}" | sudo tee /etc/apt/sources.list.d/wine.list')
			os.system(f'echo "{repo_libfaudio_ubuntu_bionic}" | sudo tee /etc/apt/sources.list.d/libfaudio.list')
		
		# Adicionar suporte a arquitetura 32 bits.
		self.msg('Adicionando suporte a ARCH i386 aguarde...')
		os.system('sudo dpkg --add-architecture i386')

		AptGet().update()
		AptGet().install('libfaudio0:i386')
		AptGet().install(requeriments_wine_debian)

	def add_archlinux_multilib(self):
		if os.path.isfile('/etc/pacman.conf.original') == True:
			print('Backup de configuração encontrado em: /etc/pacman.conf.original')
		else:
			print('Criando backup do arquivo /etc/pacman.conf em: /etc/pacman.conf.original')
			os.system('sudo cp -n /etc/pacman.conf /etc/pacman.conf.original')

		open_file = open('/etc/pacman.conf', 'rt')
		content = open_file.readlines()
		for num in range(0, len(content)):
			line = str(content[num]).replace('\n', '')
			
			if (line == str('#[multilib]')) or (line == str('[multilib]')):
				numLineMirrorList = int(num + 1) # Linha que está em baixo do [multilib]
				content[numLineMirrorList] = 'Include = /etc/pacman.d/mirrorlist\n'
				content[num] = '[multilib]\n'

		# Gravar o novo conteúdo em um arquivo temporário.
		tmpFile = tempfile.NamedTemporaryFile().name
		open_tmp_file = open(tmpFile, 'w')
		for LINE in content:
			LINE = str(LINE)
			open_tmp_file.write(LINE)

		open_tmp_file.seek(0)
		open_tmp_file.close()
		print(f'Atualizando o arquivo: /etc/pacman.conf')
		os.system(f'sudo cp -u {tmpFile} /etc/pacman.conf')
		

	def wine_archlinux(self):
		self.add_archlinux_multilib()
		Pacman().update()
		Pacman().install('wine wine-mono wine-gecko')

	def wine_fedora(self):
		os.system('sudo dnf install wine')

	def wine(self):
		os_id = ReleaseInfo().info('ID')

		if os.path.isfile('/etc/debian_version') == True: # Sistemas baseados em Debian
			self.wine_debian()
		elif os_id == 'arch':
			self.wine_archlinux()
		elif os_id == 'fedora':
			self.wine_fedora()
		else:
			self.red('A instalação do wine-stable não está disponível para o seu sistema apartir deste programa.')
			return int('1')

	def winetricks(self):
		winetricks_url = 'https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks'
		os_id = ReleaseInfo().info('ID')
		tmpFile = tempfile.NamedTemporaryFile().name

		self.yellow('Instalado winetricks')
		if os.path.isfile('/etc/debian_version') == True: # Debian/Ubuntu/Mint
			AptGet().update()
			AptGet().install(requeriments_winetricks)
			AptGet().install(requeriments_winetricks_debian)
			AptGet().install('winetricks') # Versão disponível nos repositórios do sistema.
		elif os_id == 'arch':
			Pacman().update()
			Pacman().install(requeriments_winetricks)
			Pacman().install('winetricks')
		elif os_id == 'arch':
			os.system(f'sudo dnf install {requeriments_winetricks}')
			os.system('sudo dnf install winetricks')
		else:
			self.red('A instalação do winetricks não está disponível para o seu sistema apartir deste programa.')
			return int('1')

		# Instalar winetricks para o usuário atual.
		print(f'Baixando winetricks em .... {tmpFile}')
		urllib.request.urlretrieve(winetricks_url, tmpFile)
		self.line('*')
		print(f'Instalando winetricks em: {self.winetricks_script}')
		self.line('*')
		os.system(f'sudo cp -u {tmpFile} {self.winetricks_script}')
		os.system(f'sudo chmod a+x {self.winetricks_script}')
		os.system(f'{self.winetricks_script} --version')

	def pywinery(self):
		url_pywinery_tarfile = 'https://github.com/ergoithz/pywinery/releases/download/0.3.3/pywinery_0.3-3.tar.gz'
		os.chdir(TempDir)
		self.line('=')
		print(f'Baixando: {url_pywinery_tarfile}')
		print(f'Destino: {TempDir}')
		self.line('=')
		urllib.request.urlretrieve(url_pywinery_tarfile, 'pywinery_0.3-3.tar.gz')
		self.unpack_files('pywinery_0.3-3.tar.gz', 'pywinery')
		os.chdir('pywinery/0.3')
		self.yellow('Instalando...')
		os.system('sudo python3 setup.py install')

		lines_script_pywinery = (
				'#!/usr/bin/env bash\n\n',
				'if [[ -x $(which python3 2> /dev/null) ]]; then\n',
				'   python3 -m pywinery\n',
				'else\n',
				'   python -m pywinery\n',
				'fi\n',
			)

		script_pywinery = open('pywinery.tmp', 'w')
		for L in lines_script_pywinery:
			script_pywinery.write(L)
		
		script_pywinery.seek(0)
		script_pywinery.close()
		os.system('sudo mv pywinery.tmp /usr/local/bin/pywinery')
		os.system('sudo chmod a+x /usr/local/bin/pywinery')

	def q4wine(self):
		if os.path.isfile('/etc/debian_version') == True:
			AptGet().install('q4wine')
		else:
			self.red('A instalação do q4wine não está disponível para o seu sistema apartir deste programa.')
			return int('1')

	def unpack_files(self, file, dir=''):
		# https://docs.python.org/3.3/library/tarfile.html
		self.yellow(f'Descomprimindo: {file}')
		self.yellow(f'Destino: {TempDir}')

		os.chdir(TempDir)
		tar = tarfile.open(file)
		tar.extractall(path=dir)
		tar.close()
