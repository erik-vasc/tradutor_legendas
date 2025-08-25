# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_submodules

# Coletar todas as dependências da biblioteca ttkbootstrap, pysrt e deep_translator
hidden_imports = collect_submodules('ttkbootstrap') + collect_submodules('pysrt') + collect_submodules('deep_translator')

block_cipher = None

a = Analysis(
    ['tradutor_legendas_gui.py'],    # Seu script principal
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Tradutor de Legendas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,           # False → não mostra console
    icon=r'C:\Users\erik_\OneDrive\Área de Trabalho\Projetos Python\tradutor_legendas\icone.ico',         # Caminho do ícone do seu executável
	version='versao.txt'     # Caminho para arquivo de metadados
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Tradutor de Legendas'
)
