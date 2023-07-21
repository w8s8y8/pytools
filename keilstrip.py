# -*- coding: utf-8 -*-

import os
import shutil
import glob

dirs = ['license_terms',
        'ARM/SiLabs', 'ARM/SiLabs', 'ARM/NULink', 'ARM/ULINK', 'ARM/Hlp', 'ARM/Utilities', 'ARM/PEMicro', 'ARM/TI_XDS', 'ARM/Startup', 'ARM/PACK', 'ARM/VHT', 'ARM/Flash',
        'ARM/ARMCLANG/lib/libcxx', 'ARM/ARMCLANG/sw/hlp',
        'ARM/ARMCLANG']
for d in dirs:
    if os.path.exists(d):
        shutil.rmtree(d)

files = ['ARM/BIN/UL2CM3.DLL', 'ARM/BIN/ULP2CM3.DLL', 'ARM/BIN/ULPL2CM3.dll', 'ARM/BIN/BIN\DbgFM.DLL', 'ARM/BIN/ABLSTCM.dll', 'ARM/BIN/ULP2V8M.DLL', 'ARM/BIN/UL2V8M.DLL', 'ARM/BIN/CMSIS_AGDI_V8M.DLL', 'ARM/BIN/DbgFMv8M.DLL', 'ARM/BIN/UL2ARM.DLL', 'ARM/BIN/ULP2ARM.DLL',
         'License.rtf',
         'Uninstall.exe',
         'DeleteFiles.txt',
         'UV4/uv4.chm', 'UV4/uv4jp.chm']
for f in files:
    if os.path.exists(f):
        os.remove(f)

for SVCS in glob.glob(r'UV4/*.SVCS'):
    if SVCS != 'UV4/GIT.SVCS':
        os.remove(SVCS)
