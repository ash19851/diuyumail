# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('static', 'static'), ('templates.py', '.'), ('dataconfig.py', '.'), ('config_manager.py', '.'), ('email_sender.py', '.'), ('getmiallist.py', '.'), ('template_config.py', '.')],
    hiddenimports=['jaraco.text', 'jaraco.functools', 'jaraco.context', 'importlib_resources', 'zipp'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['scipy', 'matplotlib', 'IPython', 'pygame', 'numpy', 'pandas', 'pkg_resources'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PhishingTrainer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PhishingTrainer',
)
