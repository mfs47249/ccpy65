/*

int convert_to_bin_err;
int convert_to_bin(ADDRESSPTR ptr) {
    ADDRESSPTR p;
    byte index, flag, ch;
    int result;

    convert_to_bin_err = 0;
    p = ptr;
    index = 0;
    result = 0;
    ch = peek(p);
    while (ch != 0) {
        ch = upchar(ch);
        if (ch > 64) {
            if (ch < 71) {
                ch = ch - 55;
            }
        }
        if (ch > 47) {
            if (ch < 58) {
                ch = ch - 48;
            }
        }
        if (ch > 15) {
            convert_to_bin_err = 1;
            return 0;
        }
        result = result + ch;
        p = p + 1;
        index = index + 1;
        ch = peek(p);
        if (ch != 0) {
            shiftleft(result,4);
        }
    }
    return result;
}
*/

byte hex_to_bin_check(ADDRESSPTR ptr) {
    char ch;

    ch = peek(ptr);
    if (ch > 64) {
        if (ch < 71) {
            ch = ch - 55;
        }
    }
    if (ch > 47) {
        if (ch < 58) {
            ch = ch - 48;
        }
    }
    if (ch > 15) {
        return 1;
    }
    return 0;
}


long hex_to_bin(ADDRESSPTR ptr) {
    ADDRESSPTR test;
    byte c;

    // test = ptr;
    _STZ _unireg0_0;
    _STZ _unireg0_1;
    _STZ _unireg0_2;
    _STZ _unireg0_3;
    _LDY #hex_to_bin_ptr;    // load var ptr into zeropage scratchregister for using as a pointer
    _LDA (_framepointer),Y;
    _STA _zpscratch_0;
    _INY;
    _LDA (_framepointer),Y;
    _STA _zpscratch_1;
_LABEL hex_to_int_read_loop;
    _LDA (_zpscratch_0);       // load character indexed by pointer into accu
    _BEQ hex_to_int_exit_string_scan; // end of string detected
    _CMP #'A';                 // test if inbetween A and F (works only with upper case)
    _BMI hex_to_int_shouldbedigit;
    _SEC;
    _SBC #'A'+6;              // after subtraction accu is 0A -- 0F
    _BRA hex_to_int_shiftin;  // now we can shift in 4 bits
_LABEL hex_to_int_shouldbedigit;
    _SEC;
    _SBC #'9'+7;              // after subtraction accu is 00 -- 09
_LABEL hex_to_int_shiftin;    // shift in the bits
    _ASL;
    _ASL;
    _ASL;
    _ASL;
    _LDX #4;
_LABEL hex_to_int_shiftloop;
    _ASL;
    _ROL _unireg0_0;
    _ROL _unireg0_1;
    _ROL _unireg0_2;
    _ROL _unireg0_3;
    _DEX;
    _BNE hex_to_int_shiftloop;
    _CLC;
    _LDA _zpscratch_0;
    _ADC #1;
    _STA _zpscratch_0;
    _LDA _zpscratch_1;
    _ADC #0;
    _STA _zpscratch_1;
    _BRA hex_to_int_read_loop;
_LABEL hex_to_int_exit_string_scan;
}
