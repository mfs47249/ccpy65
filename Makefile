
ASM	= vasm6502_oldstyle
ASMOPT	= -Fbin -wdc02 -dotdir 


CC	= gcc

asmtest/a.out:	test.s
	$(ASM) $(ASMOPT) -L test.lst test.s

test_old.s:	../test_old.s
	cp ../test_old.s .

serialtest.s: ../serialtest.s .
	cp ../serialtest.s .

serialtest.out:	serialtest.s 
	$(ASM) $(ASMOPT) -o serialtest.out serialtest.s

show:	a.out
	hexdump -C a.out

clean:
	rm -f a.out *.s *~

emu:
	emu -f a.out -s 512

transfer:
	python3 ../communication.py --fastmode

t4.s:	testfiles/t4.c
	echo "0x0200" > /tmp/newstart.address
	python3 main.py --debug2 -o t4.s -I testfiles -I testfiles/expressions -I testfiles/usefulfunctions -I testfiles/numbertests -I testfiles/stringfunctions -I testfiles/numberconvert -I testfiles/memory -I testfiles/misc -I testfiles/programs --stackstart 0x7000 --varstart 0x6000 --progstart $(cat /tmp/newstart.address) t4.c

t4.bin:	t4.s testfiles/t4.c
	$(ASM) $(ASMOPT) -o t4.bin -L t4.lst t4.s
	sed -nr "s/^([0-F][0-F][0-F][0-F]) LASTBYTEINPROG/0x\1/gp" t4.lst >/tmp/newstart.address
	echo -n "Lastaddress in Program is:" ; cat /tmp/newstart.address
	rm t4.s
	make t4.s
	$(ASM) $(ASMOPT) -o t4.bin -L t4.lst t4.s
	
