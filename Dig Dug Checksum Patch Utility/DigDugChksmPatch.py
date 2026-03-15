#Dig Dug Checksum Patch Utility - SNESNESCUBE64

import os
rom101FileName = '136007.101'
rom102FileName = '136007.102'
rom103FileName = '136007.103'
rom104FileName = '136007.104'
patchFileName = '136007_patched.104'

#this will make the original file ".old" and make the patch file the current file
overwriteOriginalFile = True

#Function to calculate the 8 bit checksum used by ROM 104
def CalculateChecksum8(file):
    checksum = 0
    with open(file,"rb") as openedFile:
        while (byte := openedFile.read(1)):
            checksum += int.from_bytes(byte)
            #We only care about the last byte
            if checksum > 255:
                checksum = checksum - 256
        openedFile.close()

    return checksum

#Function to patch ROM 104. This has the checksums of ROMS 101 thru 104, so they have
#To be appended to the end of the file
def PatchRom104(file, fileout, checksums):
    checksum104 = 0
    fileLength = os.path.getsize(file)
    byteCount = 0
    patchedFile = open(fileout,"wb")

    #Copy everything but the last 5 bytes, calculating the checksum up to that point
    with open(file,"rb") as openedFile:
        for byteCount in range (fileLength-5):
            byte = openedFile.read(1)
            readValue =  int.from_bytes(byte)
            patchedFile.write(readValue.to_bytes(1, 'little', signed=False))
            checksum104 += readValue
            if checksum104 > 255:
                checksum104 = checksum104 - 256

    #Add the new calculated checksums to the current checksum
    for counter in range(3):
        checksum104 += checksums[counter]
        if checksum104 > 255:
            checksum104 = checksum104 - 256
    
    #Calculate the padding for ROM 104
    paddedValue = 255-checksum104+1
    checksum104 += paddedValue
    if checksum104 > 255:
            checksum104 = checksum104 - 256

    #Write the last 5 bytes
    patchedFile.write(paddedValue.to_bytes(1, 'little', signed=False))
    patchedFile.write(checksums[0].to_bytes(1, 'little', signed=False))
    patchedFile.write(checksums[1].to_bytes(1, 'little', signed=False))
    patchedFile.write(checksums[2].to_bytes(1, 'little', signed=False))
    patchedFile.write(int(0).to_bytes(1, 'little', signed=False))#Last checksum should always be 0
    patchedFile.close()

    #Validate the patch
    validationChecksum = CalculateChecksum8(fileout)
    if checksum104 == validationChecksum:
        print("Patched ROM 104 successfully created")
        if overwriteOriginalFile:
            #Overwrite the original file with the patched file
            if os.path.exists((file + '_old')):
                os.remove((file + '_old'))
                os.rename(file, (file + '_old'))
            else:
                os.rename(file, (file + '_old'))          
            
            if os.path.exists(os.path.join(base_dir, rom104FileName)):
                os.remove(os.path.join(base_dir, rom104FileName))
                os.rename(fileout, os.path.join(base_dir, rom104FileName))
            else:
                os.rename(fileout, os.path.join(base_dir, rom104FileName))
            
    else:
        print("Patched file checksum error")
        print("Expected: " + str(hex(checksum104)))
        print("Read: " + str(hex(validationChecksum)))

print("Dig Dug Checksum Patch Utility")
print("2025 - SNESNESCUBE64")
print()

#Get the directory
base_dir = os.path.dirname(os.path.abspath(__file__))

#Init the checksum array
checksums = [None] * 3

#Calculate the first 3 file's checksum
checksums[0] = CalculateChecksum8(os.path.join(base_dir, rom101FileName))
checksums[1] = CalculateChecksum8(os.path.join(base_dir, rom102FileName))
checksums[2] = CalculateChecksum8(os.path.join(base_dir, rom103FileName))

print("ROM 101 Checksum: " + str(hex(checksums[0])))   
print("ROM 102 Checksum: " + str(hex(checksums[1])))  
print("ROM 103 Checksum: " + str(hex(checksums[2])))

PatchRom104(os.path.join(base_dir, rom104FileName),os.path.join(base_dir, patchFileName), checksums)