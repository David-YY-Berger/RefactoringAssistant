# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\RefactoringAssistant\\RefactoringAssistantCode\\src\\main_refactoring_assistant\\main-RefactoringAssistant.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['openpyxl', 'pandas'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main-RefactoringAssistant',
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
    icon='C:\\RefactoringAssistant\\RefactoringAssistantCode\\src\\refactoringImage.ico',  # Specify the path to your icon file
    onefile=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main-RefactoringAssistant',
)