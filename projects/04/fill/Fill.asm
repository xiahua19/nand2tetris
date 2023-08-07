// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(keyboard)
@KBD
D = M
@keyboard
D; JEQ

(blackinit)
@SCREEN
D = A
@R0
M = D
@8192
D = A
@R1
M = D
@SCREEN
D = A
@R1
M = M + D

(black)
@R0
A = M
M = -1
@R0
D = M + 1
M = D
@R1
M = M - D
@keyboard
M; JEQ
@KBD
D = M
@whiteinit
D; JEQ
@black
0; JEQ


(whiteinit)
@SCREEN
D = A
@R0
M = D
@8192
D = A
@R1
M = D
@SCREEN
D = A
@R1
M = M + D

(white)
@R0
A = M
M = 0
@R0
D = M + 1
M = D
@R1
M = M - D
@keyboard
M; JEQ
@KBD
D = M
@blackinit
D; JNE
@white
0; JEQ