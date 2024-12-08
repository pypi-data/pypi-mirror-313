import os
import glob
from myfirstpkg2412.findAdel import findFile


dirs =sorted(glob.glob(os.path.join('/media/ls2410/608C02658C023656/IONcomp/gps/2023rtklibsolu/data', 'test', '*', '*', 'supplemental')))
fileFound=findFile(dirs, ['*_ALL_c0714_CE2.pos'])

