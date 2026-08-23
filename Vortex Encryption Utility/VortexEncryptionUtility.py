# This is used for Decrypting Vortex ROMs, which run on taito hardware. This is a quick and dirty script

import os

ROMSIZE = 0x800

#Sub Functions
#############################################
def getDecryptedBuffer(rom, startAddress):
    decryptedBuffer = [0xFF]*0x800
    
    with open(rom, "rb") as file:
        for byteCounter in range(ROMSIZE):
            if startAddress < 0x4000:
                decryptedBuffer[byteCounter ^ 0x0209] = int.from_bytes(file.read(1))
            elif startAddress < 0x6000:
                decryptedBuffer[byteCounter ^ 0x0209] = int.from_bytes(file.read(1))
            else:
                decryptedBuffer[byteCounter ^ 0x0208] = int.from_bytes(file.read(1))

    return decryptedBuffer

#Writes a given buffer to a filepath.
def writeROMData(path, buffer):
    with open(path,"wb") as openedFile:
        for byte in buffer:
            openedFile.write(byte .to_bytes(1, 'little', signed=False))

# #Function that only prints the arguments and how to use this script
# def printArguments():
#     print("Expected Arguement format: python EyesEncryptionUtility.py *function*")
#     print("Function arguement options:")
#     print("   -e          Encrypt ROMs")
#     print("   -d          Decrypt ROMs")


#Main program
#############################################
base_dir = os.path.dirname(os.path.abspath(__file__))
addressCounter = 0

writeROMData(os.path.join(base_dir, "1.t36_Decrypted"),getDecryptedBuffer(os.path.join(base_dir, "1.t36"),0x0000))
writeROMData(os.path.join(base_dir, "2.t35_Decrypted"),getDecryptedBuffer(os.path.join(base_dir, "2.t35"),0x0800))
writeROMData(os.path.join(base_dir, "3.t34_Decrypted"),getDecryptedBuffer(os.path.join(base_dir, "3.t34"),0x1000))
writeROMData(os.path.join(base_dir, "4.t33_Decrypted"),getDecryptedBuffer(os.path.join(base_dir, "4.t33"),0x1800))
writeROMData(os.path.join(base_dir, "5.t32_Decrypted"),getDecryptedBuffer(os.path.join(base_dir, "5.t32"),0x4000))
writeROMData(os.path.join(base_dir, "6.t31_Decrypted"),getDecryptedBuffer(os.path.join(base_dir, "6.t31"),0x4800))


