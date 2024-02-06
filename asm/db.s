    .setcpu "65C02"
    .feature c_comments

; unzip a zero-terminated dizzy-compressed string at dizzyp using digrams lookup
; outputs a sequence of uncompressed characters (excluding the terminator) to the putc routine

dizzyp  = $10       ; pointer to compressed data
digrams = $12       ; digram lookup table (128 2-byte pairs)


    .code
putc:   sta $f001   ; pymon character output, or could write buffer etc
        rts


undizzy:
        ldx #0      ; track stack depth
@nextz: lda (dizzyp)   ; get encoded char
        tay
        inc dizzyp  ; inc pointer
        bne @ready
        inc dizzyp+1
@ready: tya
@chk7:  bmi @subst  ; is it a digraph (bit 7 set)?
        beq @done   ; if 0 we're done
        jsr putc
@stk:   cpx #0      ; any stacked items?
        beq @nextz
        dex
        pla         ; pop latest
        bra @chk7
@subst: sec
        rol         ; index*2+1 for second char in digram
        tay
        lda (digrams),y
        inx         ; track stack depth
        pha         ; stack the second char
        dey
        lda (digrams),y   ; fetch the first char of the digram
        bra @chk7   ; keep going
@done:  rts


test_undizzy:
        lda #<dizzyData
        sta dizzyp
        lda #>dizzyData
        sta dizzyp+1
        lda #<digramTable
        sta digrams
        lda #>digramTable
        sta digrams+1
        jsr undizzy
        brk

digramTable:
        .byte $65,$20, $74,$68, $20,$61, $69,$6e, $6f,$75, $74,$20, $65,$72, $73,$20
        .byte $20,$20, $20,$81, $64,$20, $61,$72, $83,$67, $89,$80, $82,$20, $72,$80
        .byte $6f,$72, $6f,$66, $65,$6e, $6c,$6c, $6f,$6e, $73,$74, $59,$84, $61,$6e
        .byte $79,$20, $74,$6f, $72,$65, $2e,$88, $54,$68, $61,$73, $72,$6f, $69,$74
        .byte $79,$84, $8c,$20, $6f,$77, $65,$73, $69,$73, $20,$77, $86,$80, $2c,$20
        .byte $82,$6e, $69,$87, $91,$20, $63,$68, $8f,$83, $61,$74, $6f,$6d, $65,$61
        .byte $61,$93, $61,$67, $96,$82, $99,$20, $88,$88, $65,$87, $20,$63, $9d,$73
        .byte $6c,$6f, $9c,$80, $63,$6b, $62,$65, $74,$6c, $20,$73, $70,$b7, $96,$27
        .byte $81,$80, $69,$64, $20,$68, $6c,$69, $67,$68, $9c,$a6, $65,$8a, $be,$b1
        .byte $65,$2e, $b2,$ac, $69,$81, $76,$80, $61,$85, $20,$66, $20,$64, $76,$86
        .byte $a8,$8a, $65,$65, $c9,$8e, $61,$6d, $20,$62, $6d,$61, $65,$64, $69,$95
        .byte $20,$6c, $67,$80, $a4,$8e, $bc,$80, $9f,$db, $69,$85, $75,$70, $6e,$6f
        .byte $9e,$ae, $69,$94, $20,$a0, $a5,$68, $65,$6c, $65,$78, $61,$6c, $69,$72
        .byte $91,$8d, $92,$74, $65,$95, $62,$6c, $70,$6c, $62,$75, $72,$84, $9b,$41
        .byte $65,$0a, $75,$6e, $20,$a9, $6c,$dc, $6f,$6c, $61,$79, $84,$85, $72,$69
        .byte $b6,$97, $74,$77, $6d,$20, $a8,$64, $72,$61, $92,$64, $77,$ca, $62,$6f

dizzyData:
        .byte $b2, $8f, $95, $97, $64, $8c, $82, $85, $c0, $92, $8a, $91, $8e, $9e, $61, $8a
        .byte $bb, $66, $6f, $8f, $61, $bd, $6d, $b0, $d4, $f7, $ba, $0a, $ed, $69, $6c, $64
        .byte $8c, $ef, $ee, $6e, $8a, $a0, $20, $da, $66, $90, $ea, $ef, $bd, $6d, $b0, $20
        .byte $95, $9a, $d3, $cd, $6c, $a2, $87, $84, $74, $0a, $e8, $ed, $69, $6c, $64, $8c
        .byte $d0, $64, $a2, $6e, $8e, $67, $75, $93, $79, $2e, $00