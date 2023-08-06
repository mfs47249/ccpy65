
ASM	= vasm6502_oldstyle
ASMOPT	= -Fbin -c02 -dotdir -L test.lst

CC	= gcc

a.out:	test.s
	$(ASM) $(ASMOPT) test.s

test.s:	../ccpy65/test.s
	cp ../test.s .

show:	a.out
	hexdump -C a.out

clean:
	rm -f a.out *.s *~

emu:
	emu -f a.out -s 512
