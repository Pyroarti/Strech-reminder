from PyInstaller.utils.hooks import copy_metadata, collect_submodules

datas = copy_metadata('win10toast')
hiddenimports = collect_submodules('win10toast')
