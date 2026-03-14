# This is used for Decrypting and encrypting PacPlus ROMs as found in MAME.
# This is based off of the driver as found in MAME. The difference here is that
# it can both decrypt and re-encrypt the ROMs in the same way.

import os
from datetime import datetime
import shutil
import sys

#This is the decryption/encryption table for decoding the data bits
XOR_SWAP_TABLE =    [[ 7,6,5,4,3,2,1,0, 0x00 ], #decryption half
                    [ 7,6,5,4,3,2,1,0, 0x28 ],
                    [ 6,1,3,2,5,7,0,4, 0x96 ],
                    [ 6,1,5,2,3,7,0,4, 0xbe ],
                    [ 0,3,7,6,4,2,1,5, 0xd5 ],
                    [ 0,3,4,6,7,2,1,5, 0xdd ],
                    [ 7,6,5,4,3,2,1,0, 0x00 ],  #encryption half
                    [ 7,6,5,4,3,2,1,0, 0x28 ],
                    [ 2,7,3,0,5,4,6,1, 0x96 ],
                    [ 2,7,5,0,3,4,6,1, 0xbe ],
                    [ 5,4,0,3,6,2,1,7, 0xd5 ],
                    [ 3,4,0,5,6,2,1,7, 0xdd ]]

#This chooses which bit order is used based on the address
PICK_TABLE = [0,2,4,2,4,0,4,2,2,0,2,2,4,0,4,2,
            2,2,4,0,4,2,4,0,0,4,0,4,4,2,4,2]

PMP_ROM_LIST = ["pacplus.6e", "pacplus.6f", "pacplus.6h", "pacplus.6j"]
PMP_BUFFER_SIZE = 0x1000

#Sub Functions
#############################################
def PacPlusDecrypt(address, encryptedData):
    decryptedData = 0xFF

    #Figure out which order we are using
    method = getMethod(address)
    decryptedData = bitSwap8(encryptedData, XOR_SWAP_TABLE[method]) ^ XOR_SWAP_TABLE[method][8]

    return decryptedData

def PacPlusEncrypt(address, unencryptedData):
    encryptedData = 0xFF
    #Figure out which order we are using
    method = getMethod(address) + 6

    #Encrypt the byte
    encryptedData = bitSwap8((unencryptedData ^ XOR_SWAP_TABLE[method][8]), XOR_SWAP_TABLE[method])

    return encryptedData

# Picks which bit order based on the address
def getMethod(address):
    method = 0
    method = PICK_TABLE[
            (address & 0x001) |
            ((address & 0x004) >> 1) |
            ((address & 0x020) >> 3) |
            ((address & 0x080) >> 4) |
            ((address & 0x200) >> 5)]

    if ((address & 0x800) == 0x800):
        method = method ^ 0x01
    
    return method

# Moves bits into the correct order [bit7,6,5,4,3,2,1]
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

# Gets the entire buffer of a ROM. Runs the encryption or decryption functions
def getBuffer(filename, buffer_size, startAddress, function):
    buffer = [0xFF] * buffer_size

    with open(filename,"rb") as openedFile:
        for addressCounter in range(buffer_size):
            if (function == "-e"):
                buffer[addressCounter] = PacPlusEncrypt(startAddress + addressCounter, int.from_bytes(openedFile.read(1)))
            else:
                buffer[addressCounter] = PacPlusDecrypt(startAddress + addressCounter, int.from_bytes(openedFile.read(1)))

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
    print("Expected Arguement format: python PacPlusEncryptionUtility.py *function*")
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
        makeBackup(base_dir, PMP_ROM_LIST)
        addressCounter = 0
        for filename in PMP_ROM_LIST:
            obfuscatedBuffer = getBuffer(os.path.join(base_dir, filename + "_Decrypted"),PMP_BUFFER_SIZE, addressCounter, "-e")
            writeROMData(os.path.join(base_dir, filename), obfuscatedBuffer)
            addressCounter = addressCounter + 0x1000
    elif sys.argv[1] == "-d":
        makeBackup(base_dir, PMP_ROM_LIST)
        addressCounter = 0
        for filename in PMP_ROM_LIST:
            obfuscatedBuffer = getBuffer(os.path.join(base_dir, filename),PMP_BUFFER_SIZE, addressCounter, "-d")
            writeROMData(os.path.join(base_dir, filename+ "_Decrypted"), obfuscatedBuffer)
            addressCounter = addressCounter + 0x1000
    else:
        print("Error: Invalid Arguements")
        printArguments()

else:
    print("Error: Invalid Arguements")
    printArguments()
