# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['StartGame.py'],
             pathex=['C:\\Users\\Gergo\\IdeaProjects\\2021-ca400-omancrn2-gellerg2\\src'],
             binaries=[],
             datas=[('data', 'data/'), ('PuyoPuyo', 'PuyoPuyo/'), ('Tetris', 'Tetris/'), ('options.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Puyo Puyo Tetris',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='data\\puyologo32x32.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Puyo Puyo Tetris')
