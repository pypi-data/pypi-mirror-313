import json
import os
import subprocess
from pathlib import Path
from pyloid.utils import get_platform
from PyInstaller.__main__ import run as pyinstaller_run
import shutil


def create_spec_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Create spec file for each OS
    os_type = get_platform()
    
    # Select template for each OS
    if os_type == 'macos':
        spec_content = _create_macos_spec(config)
    elif os_type == 'linux':
        spec_content = _create_linux_spec(config)
    else:  # windows
        spec_content = _create_windows_spec(config)
    
    # Save spec file
    spec_path = Path(f"build-{os_type}.spec")
    spec_path.write_text(spec_content, encoding='utf-8')
    
    return str(spec_path)

def _create_windows_spec(config):
    return f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{config['main_script']}'],
    pathex={config.get('pathex', [])},
    binaries={config.get('binaries', [])},
    datas={config.get('datas', [])},
    hiddenimports={config.get('hiddenimports', [])},
    hookspath={config.get('hookspath', [])},
    hooksconfig={config.get('hooksconfig', {})},
    runtime_hooks={config.get('runtime_hooks', [])},
    excludes={config.get('excludes', [])},
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{config.get("name", "pyloid-app")}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{config.get('icon', 'src-pyloid/icons/icon.ico')}'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{config.get("name", "pyloid-app")}'
)
"""

def _create_macos_spec(config):
    return f"""# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['{config['main_script']}'],
    pathex={config.get('pathex', [])},
    binaries={config.get('binaries', [])},
    datas={config.get('datas', [])},
    hiddenimports={config.get('hiddenimports', [])},
    hookspath={config.get('hookspath', [])},
    hooksconfig={config.get('hooksconfig', {})},
    runtime_hooks={config.get('runtime_hooks', [])},
    excludes={config.get('excludes', [])},
    noarchive=False,
    optimize=0
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{config.get("name", "pyloid-app")}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{config.get('icon', 'src-pyloid/icons/icon.ico')}'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{config.get("name", "pyloid-app")}'
)

app = BUNDLE(
    coll,
    name='{config.get("name", "pyloid-app")}.app',
    icon='{config.get('icon', 'src-pyloid/icons/icon.icns')}',
    bundle_identifier=None
)
"""

def _create_linux_spec(config):
    return f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{config['main_script']}'],
    pathex={config.get('pathex', [])},
    binaries={config.get('binaries', [])},
    datas={config.get('datas', [])},
    hiddenimports={config.get('hiddenimports', [])},
    hookspath={config.get('hookspath', [])},
    hooksconfig={config.get('hooksconfig', {})},
    runtime_hooks={config.get('runtime_hooks', [])},
    excludes={config.get('excludes', [])},
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{config.get("name", "pyloid-app")}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon={config.get('icon', 'src-pyloid/icons/icon.png')}
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{config.get("name", "pyloid-app")}'
)
"""

def cleanup_after_build(json_path):
    """Function to clean up unnecessary files after build"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        cleanup_patterns = config.get('cleanup_patterns', [])
        if not cleanup_patterns:
            return True
            
        dist_dir = Path(f'dist/{config.get("name", "pyloid-app")}')
        if not dist_dir.exists():
            print(f"Cannot find directory to clean: {dist_dir}")
            return False

        print("Cleaning up unnecessary files...")
        for pattern in cleanup_patterns:
            for file_path in dist_dir.glob(pattern):
                if file_path.is_dir():
                    shutil.rmtree(file_path)
                else:
                    file_path.unlink()
                print(f"Removed: {file_path}")
                
        print("File cleanup completed.")
        return True
        
    except Exception as e:
        print(f"Error occurred during file cleanup: {e}")
        return False

def build_from_spec(spec_path):
    try:
        pyinstaller_run([
            '--clean',  # Clean temporary files
            spec_path   # Spec file path
        ])
        print("Build completed.")
    
        return True
    except Exception as e:
        print(f"Error occurred during build: {e}")
        return False

def main():
    spec_path = create_spec_from_json('build_config.json')
    
    build_from_spec(spec_path)
    
    cleanup_after_build('build_config.json')
    
if __name__ == "__main__":
    main()