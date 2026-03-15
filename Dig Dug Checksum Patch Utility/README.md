# Dig Dug Checksum Patch Utility

This is a tool for patching the checksums in Dig Dug ROMs. The checksums at the end of memory are used for the ROM check when the game boots. The problem is that if any byte gets changed in a ROM, the test fails. So if a mod is written for it, the checksums have to be calculated. This tool will do it automatically, eliminating the need for it.

## Using the tool
*to do*

## Theory of Operation
In Dig Dug, the checksum lives at the end of program ROM for the main CPU. It reserves the last 5 bytes.