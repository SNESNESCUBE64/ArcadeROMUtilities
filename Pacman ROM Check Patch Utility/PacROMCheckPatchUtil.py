# This is a utility used for patching the two bytes at the end of each ROM file
# for various pacman ROM sets.

import os
from datetime import datetime
import shutil
import stat
from tkinter import Tk
from tkinter.filedialog import askopenfilenames


#Sub Functions
#############################################

# Function that calculates that padding bytes and patches them
def patchROMs(rom_list):
    makeBackup(rom_list)

    checksumEven = 0
    checksumOdd = 0

    if checkPaths(rom_list):
        clearReadOnly(rom_list)
        for rom in rom_list:
            checksumEven = 0
            checksumOdd = 0
            romSize = os.path.getsize(rom)
            buffer = [0]*romSize

            with open(rom, "rb") as file:
                for byteCounter in range(romSize):
                    if byteCounter < (romSize - 2):
                        buffer[byteCounter] = int.from_bytes(file.read(1))
                        if (byteCounter % 2) == 0:
                            checksumEven = (checksumEven + buffer[byteCounter]) & 255
                        else:
                            checksumOdd = (checksumOdd + buffer[byteCounter]) & 255
                    elif byteCounter == (romSize - 2):
                        buffer[byteCounter] = (256 - checksumEven) & 255
                    elif byteCounter == (romSize - 1):
                        buffer[byteCounter] = (256 - checksumOdd) & 255

            writeROMData(rom, buffer)        
            
    else:
        print("Error: Invalid path given")

#Makes a backup of the selected ROMs
def makeBackup(rom_list):
    base_dir = os.path.dirname(rom_list[0])
    folderName = "Backup_" + str(int(round(datetime.now().timestamp())))
    path = os.path.join(base_dir, folderName)
    
    if not os.path.exists(path):
        os.makedirs(path) 
    
    for filename in rom_list:
        fullPath = os.path.join(base_dir, filename)
        if os.path.exists(fullPath):
            shutil.copy(fullPath,path)

#Validates that the paths are all valid
def checkPaths(rom_list):
    allValid = True
    for file in rom_list:
        if not os.path.isfile(file):
            allValid = False
    
    return allValid

#Clears the read only flag 
def clearReadOnly(rom_list):
    for rom in rom_list:
        os.chmod( rom, (stat.S_IWRITE | stat.S_IREAD ))

#Writes a given buffer to a filepath.
def writeROMData(path, buffer):
    with open(path,"wb") as openedFile:
        for byte in buffer:
            openedFile.write(byte .to_bytes(1, 'little', signed=False))   

#Main program
#############################################
base_dir = os.path.dirname(os.path.abspath(__file__))

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filenames = askopenfilenames(initialdir=base_dir, title='Choose files to patch')
print(filenames)

if filenames:
    patchROMs(filenames)

