# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.utils.hooks import is_module_satisfies
from PyInstaller.archive.pyz_crypto import PyiBlockCipher

EXEC_NAME = 'FBapp_backend'

# Set this secret cipher to some secret value. It will be used
# to encrypt archive package containing your app's bytecode
# compiled Python modules, to make it harder to extract these
# files and decompile them. If using secret cipher then you
# must install pycrypto package by typing: "pip install pycrypto".
# Note that this will only encrypt archive package containing
# imported modules, it won't encrypt the main script file
# (main.py). The names of all imported Python modules can be
# still accessed, only their contents are encrypted.
SECRET_CIPHER = None  # "a-secret-AN$YS"  # Only first 16 chars are used  # fixme Bug if encrypted

if SECRET_CIPHER:
    # If using secret cipher then pycrypto package must be installed
    cipher_obj = PyiBlockCipher(key=SECRET_CIPHER)
else:
    cipher_obj = None

a = Analysis(['main_standalone_entrance.py'],
             pathex=[
                'backendapp/external', 
                'backendapp/protodef', 
                './'
             ],
             binaries=[
                 ('backendapp/external/twin_runtime/*.dll', '.'),
                 ('backendapp/external/twin_runtime/*.so', '.'),
                 ('backendapp/external/twin_runtime/lib/', './lib'),
             ],
             datas=[
             #    ('TwinRuntimeGUI/Frontend/View', 'TwinRuntimeGUI/Frontend/View'),
             ],
             hiddenimports=[
                 # 'numpy.random.common',
                 'twin_runtime'
             ],
             # hookspath=["build-essential"],  # To find "hook-*.py"
             runtime_hooks=[],
             excludes=[],
             win_private_assemblies=True,
             win_no_prefer_redirects=True,
             cipher=cipher_obj,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=cipher_obj)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=EXEC_NAME,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,  # upx is known to have issues when compressing .dlls
          console=True,
          # icon="../resources/wxpython.ico"
          )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name=EXEC_NAME)
