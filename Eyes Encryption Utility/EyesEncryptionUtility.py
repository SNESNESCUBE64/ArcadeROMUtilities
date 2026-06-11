# This is used for Decrypting and encrypting Eyes ROMs as found in MAME.
# This is based off of the driver as found in MAME. The difference here is that
# it can both decrypt and re-encrypt the ROMs in the same way.

import os
from datetime import datetime
import shutil
import sys

# Bit Orders
CPU_BIT_ORDER_DATA = [7,6,3,4,5,2,1,0]
VID_BIT_ORDER_DATA = [7,4,5,6,3,2,1,0]
VID_BIT_ORDER_ADDR = [15,14,13,12,11,10,9,8,7,6,5,4,3,0,1,2]

# ROM Info
EYES_CPU_ROM_LIST = ["d7", "e7", "f7", "h7"]
EYES_VID_ROM_LIST = ["d5", "e5"]
CPU_BUFFER_SIZE = 0x1000
VID_BUFFER_SIZE = 0x1000

#Sub Functions
#############################################

# Re-arranges an 8bit value in a given bit order 
# [bit7,6,5,4,3,2,1]
def bitSwap8(data, bitOrder):
    output = 0xFF

    dataBuffer = [0]*8
    compValue = 0x01
    output = 0
    
    # convert the uint8 to an 8bit array
    for i in range(0,8):
        dataBuffer[i] = (data & compValue) >> i
        compValue = compValue << 1

    # Generate the new ordered byte
    compValue = 0x80
    for i in range(0,8):
        outputBit = dataBuffer[bitOrder[i]]
        output = output + (outputBit*compValue)
        compValue = compValue >> 1

    return output
# Re-arranges an 16bit value in a given bit order 
# [bit15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
def bitSwap16(data, bitOrder):
    output = 0xFFFF

    dataBuffer = [0]*16
    compValue = 0x0001
    output = 0
    
    # convert the uint16 to an 16bit array
    for i in range(0,16):
        dataBuffer[i] = (data & compValue) >> i
        compValue = compValue << 1

    # Generate the new ordered byte
    compValue = 0x8000
    for i in range(0,16):
        outputBit = dataBuffer[bitOrder[i]]
        output = output + (outputBit*compValue)
        compValue = compValue >> 1

    return output

#Gets the obfuscated buffer for the CPU ROMs
def getCpuBuffer(filename, buffer_size):
    buffer = [0xFF] * buffer_size

    with open(filename,"rb") as openedFile:
        for addressCounter in range(buffer_size):
            buffer[addressCounter] = bitSwap8(int.from_bytes(openedFile.read(1)), CPU_BIT_ORDER_DATA)

    return buffer

#Gets the obfuscated buffer for the video ROMs
def getVideoBuffer(filename, buffer_size):
    buffer = [0xFF] * buffer_size
    addr = 0

    with open(filename,"rb") as openedFile:
        for addressCounter in range(buffer_size):
            addr = bitSwap16(addressCounter, VID_BIT_ORDER_ADDR)
            buffer[addr] = bitSwap8(int.from_bytes(openedFile.read(1)), VID_BIT_ORDER_DATA)
    
    return buffer
            

#Writes a given buffer to a filepath.
def writeROMData(path, buffer):
    with open(path,"wb") as openedFile:
        for byte in buffer:
            openedFile.write(byte .to_bytes(1, 'little', signed=False))

#Makes a backup of both the encrypted and decrypted ROMs.
def makeBackup(base_dir, rom_list):
    folderName = "Backup_" + str(int(round(datetime.now().timestamp())))
    path = os.path.join(base_dir, folderName)
    
    if not os.path.exists(path):
        os.makedirs(path) 
    
    for filename in rom_list:
        encFile = os.path.join(base_dir, filename)
        decFile = os.path.join(base_dir, filename + "_Decrypted")
        if os.path.exists(encFile):
            shutil.copy(encFile,path)
        if os.path.exists(decFile):
            shutil.copy(decFile,path)

#Function that only prints the arguments and how to use this script
def printArguments():
    print("Expected Arguement format: python EyesEncryptionUtility.py *function*")
    print("Function arguement options:")
    print("   -e          Encrypt ROMs")
    print("   -d          Decrypt ROMs")


#Main program
#############################################
base_dir = os.path.dirname(os.path.abspath(__file__))
addressCounter = 0xFFFF

if len(sys.argv) > 1:
    if sys.argv[1] == "-help":
        printArguments()
    elif sys.argv[1] == "-e":
        makeBackup(base_dir, EYES_CPU_ROM_LIST + EYES_VID_ROM_LIST) 
        for filename in EYES_CPU_ROM_LIST:
            obfuscatedBuffer = getCpuBuffer(os.path.join(base_dir, filename + "_Decrypted"),CPU_BUFFER_SIZE)
            writeROMData(os.path.join(base_dir, filename), obfuscatedBuffer)
        for filename in EYES_VID_ROM_LIST:
            obfuscatedBuffer = getVideoBuffer(os.path.join(base_dir, filename + "_Decrypted"),CPU_BUFFER_SIZE)
            writeROMData(os.path.join(base_dir, filename), obfuscatedBuffer)
    elif sys.argv[1] == "-d":
        makeBackup(base_dir, EYES_CPU_ROM_LIST + EYES_VID_ROM_LIST)
        for filename in EYES_CPU_ROM_LIST:
            obfuscatedBuffer = getCpuBuffer(os.path.join(base_dir, filename),CPU_BUFFER_SIZE)
            writeROMData(os.path.join(base_dir, filename + "_Decrypted"), obfuscatedBuffer)
        for filename in EYES_VID_ROM_LIST:
            obfuscatedBuffer = getVideoBuffer(os.path.join(base_dir, filename),CPU_BUFFER_SIZE)
            writeROMData(os.path.join(base_dir, filename + "_Decrypted"), obfuscatedBuffer)
    else:
        print("Error: Invalid Arguements")
        printArguments()

else:
    print("Error: Invalid Arguements")
    printArguments()
