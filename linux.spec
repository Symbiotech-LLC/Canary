# -*- mode: python -*-

block_cipher = None


a = Analysis(['canary.py'],
             pathex=['/home/wolf/Scripts/GitHub/Symbiotech-LLC/Canary'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             additional-hooks-dir=['/home/wolf/Scripts/GitHub/Symbiotech-LLC/Canary/src/resources/hooks']
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('canary.png','src/resources/canary.png','DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='linux_canary',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
          icon='src/resources/canary.ico' )