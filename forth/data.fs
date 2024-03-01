
\ memory pointers

$80 constant RAND16
$f808 constant NATIVE-RNG
$f81c constant NATIVE-STRLEN
$f843 constant NATIVE-DECODE
$f89e constant NATIVE-STRWRAP


$5200 constant ADVDAT  \ ADVDAT + 26983 bytes must be less than $bc00

ADVDAT $0000 + constant DIGRAMS \ 256 bytes
ADVDAT $0100 + constant VOCAB   \ 2482 bytes
ADVDAT $0ab2 + constant CAVES&  \ 280 bytes
ADVDAT $0bca + constant CAVES   \ 11798 bytes
ADVDAT $39e0 + constant MSGS&   \ 402 bytes
ADVDAT $3b72 + constant MSGS    \ 9045 bytes
ADVDAT $5ec7 + constant ITEMS&  \ 128 bytes
ADVDAT $5f47 + constant ITEMS   \ 2592 bytes

ADVDAT $600 - constant MSGBUF
: decode ( strz DIGRAMS outz -- addr n )
    NATIVE-DECODE execute
;

42 RAND16 !     \ initialize random

: random ( -- n )
    NATIVE-RNG execute RAND16 @
;

: asciiz> ( c-addr -- c-addr u )
    NATIVE-STRLEN execute
;
