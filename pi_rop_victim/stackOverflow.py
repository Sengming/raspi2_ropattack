import struct
string = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
jump = struct.pack("i", 0x00000000)
print(string)
