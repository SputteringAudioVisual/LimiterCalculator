# -*- mode: python ; coding: utf-8 -*-
#
# Uso:  pyinstaller "Build files/main.spec"
# (ejecutar desde la raiz del proyecto)
#
# Resultado:
#   dist/LimiterCalculator.exe   <- ejecutable unico, sin consola
#   dist/dataBase/               <- copia editable de la DB junto al exe
#
# El usuario puede anadir sus propios JSON a dist/dataBase/ sin recompilar.

import os
import shutil
from pathlib import Path

block_cipher = None

# SPECPATH = directorio de este fichero .spec  ("Build files/")
ROOT = str(Path(SPECPATH).parent)

a = Analysis(
    [os.path.join(ROOT, 'src', 'main.py')],
    pathex=[ROOT],
    binaries=[],
    datas=[
        # Recursos estaticos: empaquetados dentro del exe (_MEIPASS)
        (os.path.join(ROOT, 'GUI', 'MainGui', 'MainGUI.ui'),     'GUI/MainGui'),
        (os.path.join(ROOT, 'GUI', 'resources', 'imageFF.png'),  'GUI/resources'),
        # DB incluida en el exe como fallback si no existe junto al exe
        (os.path.join(ROOT, 'dataBase', 'amplifierDataBase'),    'dataBase/amplifierDataBase'),
        (os.path.join(ROOT, 'dataBase', 'driverDataBase'),       'dataBase/driverDataBase'),
    ],
    hiddenimports=[
        'PyQt5.uic',
        'PyQt5.uic.properties',
        'PyQt5.uic.uiparser',
        'qdarktheme',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Excluir librerias de los scripts de AudioAnalisys (ya eliminados)
    excludes=['pyaudio', 'scipy', 'matplotlib', 'numpy', 'tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LimiterCalculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(ROOT, 'Build files', 'icon.ico'),
)


# Post-build: copia dataBase/ junto al .exe para que el usuario
# pueda anadir/editar JSONs sin tocar el ejecutable
import PyInstaller.config as _pyi_cfg

_dist = Path(_pyi_cfg.CONF['distpath'])
_db_src = Path(ROOT) / 'dataBase'
_db_dst = _dist / 'dataBase'

if _db_src.exists() and not _db_dst.exists():
    shutil.copytree(str(_db_src), str(_db_dst))
    print(f'[post-build] dataBase/ -> {_db_dst}')
