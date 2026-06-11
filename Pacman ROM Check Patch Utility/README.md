# Pacman ROM Check Patch Utility
This is a tool used for patching the padding bytes at the end of pacman ROMs for the purpose of passing the ROM check.

## Using the tool
Just execute the pythons script, file select is done via file browser. When executing the tool, it will automatically back up the files that are being patched.

## Theory of Operation
The ROM check is quite simple. Each ROM chip is checked twice, once on the even bytes and once on the odd bytes. For the ROM check to pass, the separate sums of the odd and even bytes have to add up to 0 in the lower eight bits. The last two bytes are padding for this checksum, so these can be patched if the file is updated. The second to last byte is the even checksum padding. The last byte is the odd checksum padding.

Let's say the even bytes add up to 0xFE, the padding byte would have to be 0x02 as the 8 bit sum of 0xFE + 0x02 is 0x00. 