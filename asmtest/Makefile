
ASM	= vasm6502_oldstyle
ASMOPT	= -Fbin -wdc02 -dotdir -L test.lst

CC	= gcc

a.out:	test.s
	$(ASM) $(ASMOPT) test.s

test.s:	../test.s
	cp ../test.s .

show:	a.out
	hexdump -C a.out

clean:
	rm -f a.out *.s *~

emu:
	emu -f a.out -s 512

transfer:
	python3 ../communication.py
