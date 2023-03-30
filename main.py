from cncpresets import *
from files import Files
import os

dxf_path = os.getcwd() + "\\dxf\\"
nc_path = os.getcwd() + "\\nc\\"

cnc_operations = CNCPresets.get_operations(CNCPresets.select_preset())

files = Files.list_files(dxf_path)
for file in files:
    Files.convert_file(dxf_path, nc_path, file, cnc_operations)
