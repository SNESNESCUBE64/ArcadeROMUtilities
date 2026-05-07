# Eyes Encryption Utility

This is a tool that is used for decrpyting and encrypting the ROM data for Eyes. It is based of the methods used in MAME and is translated to python for ease of use outside of MAME. 

[MAME source for decryption](https://github.com/mamedev/mame/blob/master/src/mame/pacman/pacman.cpp)

## Using the tool
To use this script, place the python script in the same folder as the ROMs (d7, e7, f7, h7, d5, and e5) and execute one of below commands

### Decryption Execution
```
python EyesEncryptionUtility.py -d
```

### Encryption Execution
```
python EyesEncryptionUtility.py -e
```

### Arguements
- Function
    - -d     Decrypt
    - -e     Encrypt

For Windows users, batch scripts are provided for ease of use. 

## Theory of Operation
Eyes has a very simple obfuscation that simply swaps around the data bits for the CPU ROMs. With the GFX ROMs it is a little bit different. Instead of just swapping CPU bits, it also swaps bytes to be at slightly different addresses.

- For the CPU ROMs, data bits 3 and 5 are swapped.
- For the GFX/Vid ROMs, data bits 4 and 6 are swapped and address lines 0 and 2 are swapped.
