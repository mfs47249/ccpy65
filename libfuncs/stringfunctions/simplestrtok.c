
ADDRESSPTR strtok_nextstring;

ADDRESSPTR strtok(ADDRESSPTR string_adr) {
    _LDY #strtok_string_adr;    // load ar ptr into zeropage scratchregister for using as a pointer
    _LDA (_framepointer),Y;
    _STA _zpscratch_0;
    _INY;
    _LDA (_framepointer),Y;
    _STA _zpscratch_1;
    // in zpscratch 0,1 is address argument to string
    _LDA _zpscratch_0;
    _STA _zpscratch_2;
    _LDA _zpscratch_1;
    _STA _zpscratch_3;
    // in zpscratch 2,3 is copy of zpscratch 0,1 (startptr)
    _LDA _zpscratch_0;
    _STA _zpscratch_4;
    _LDA _zpscratch_1;
    _STA _zpscratch_5;
    // in zpscratch 4,5 is copy of zpscratch 0,1 (stringptr)
    _LDA _zpscratch_1;               // if (stringptr == 0) {
    _BNE strtok_ptrnotnull;
    _LDA _zpscratch_0;
    _BNE strtok_ptrnotnull;
    // ptr is null
    _LDA global_strtok_nextstring_0; // stringptr = strtok_nextstring;
    _STA _zpscratch_2;
    _STA _zpscratch_4;
    _LDA global_strtok_nextstring_1; // startptr = strtok_nextstring;
    _STA _zpscratch_3;
    _STA _zpscratch_5;
// check if char *ptr is null, if null, then no token will follow and we are done
    _LDA (_zpscratch_2);
    _BNE strtok_ptrnotnull;
// char on ptr is null, must be the end of the string
    _STZ _unireg0_0;
    _STZ _unireg0_1;
    _BRA strtok_exit_subroutine;
// there is another token that must be processed, save the start of this
// token in global var nextstring, for further processing
_LABEL strtok_ptrnotnull;
// Load char at ptr we are now searching for the next
_LABEL strtok_search_delim;
    _LDA (_zpscratch_2);
    _BEQ strtok_eos_found;
    _CMP #$20;   // space char
    _BEQ strtok_delim_found;
    _CLC;
    _LDA _zpscratch_2;
    _ADC #1;
    _STA _zpscratch_2;
    _LDA _zpscratch_3;
    _ADC #0;
    _STA _zpscratch_3;
    _BRA strtok_search_delim;
_LABEL strtok_delim_found;
// put end of string into *ptr
    _LDA #0;
    _STA (_zpscratch_2);
// move ptr after new end of string marker and save it
// in strtok_nextstring for the next iteration.
    _CLC;
    _LDA _zpscratch_2;
    _ADC #1;
    _STA _zpscratch_2;
    _STA global_strtok_nextstring_0;
    _LDA _zpscratch_3;
    _ADC #0;
    _STA _zpscratch_3;
    _STA global_strtok_nextstring_1;
    _BRA strtok_exit_withstartptr;
// we found the end of string marker
_LABEL strtok_eos_found;
    _LDA _zpscratch_2;
    _STA global_strtok_nextstring_0;
    _LDA _zpscratch_3;
    _STA global_strtok_nextstring_1;
_LABEL strtok_exit_withstartptr;
    _LDA _zpscratch_4;
    _STA _unireg0_0;
    _LDA _zpscratch_5;
    _STA _unireg0_1;
_LABEL strtok_exit_subroutine;
}