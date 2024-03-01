\ drop dup swap ! @ over >r r> r@ nip rot
\ -rot tuck , c@ c! +! execute emit type . u. u.r .r d. d.r ud. ud.r ? false
\ true space 0 1 2 2dup ?dup + - 1- 1+ 2* 2/ abs dabs and or xor rshift lshift
\ pick char [char] char+ chars cells cell+ here = <> < u< u> > 0= 0<> 0> 0< min
\ max 2drop 2swap 2over 2! 2@ 2variable 2constant 2literal 2r@ 2r> 2>r invert
\ negate dnegate c, bounds spaces bl -trailing -leading /string refill accept
\ input>r r>input unused depth key allot create does> variable constant value
\ to s>d d>s d- d+ erase blank fill find-name ' ['] name>int int>name
\ name>string >body defer latestxt latestnt parse-name parse execute-parsing
\ source source-id : ; :noname compile, [ ] literal sliteral ." s" s\" postpone
\ immediate compile-only never-native always-native allow-native nc-limit
\ strip-underflow abort abort" do ?do i j loop +loop exit unloop leave recurse
\ quit begin again state evaluate base digit? number >number hex decimal count
\ m* um* * um/mod sm/rem fm/mod / /mod mod */mod */ \ move cmove> cmove pad
\ cleave hexstore within >in <# # #s #> hold sign output input cr page at-xy
\ marker words wordsize aligned align bell dump .s compare search find word (
\ .( if then else repeat until while case of endof endcase defer@ defer! is
\ action-of useraddr buffer: buffstatus buffblocknum blkbuffer scr blk
\ block-write block-write-vector block-read block-read-vector save-buffers
\ block update buffer empty-buffers flush load thru list see cold bye  ok

\ python forth/fpp.py forth/advent.fs

\ py65mon -m 65c02 -i c004 -o c001 -b forth/advent.mon

8 nc-limit !        \ don't inline too much

include data.fs

include defs.fs

include message.fs

include item.fs

include location.fs

include english.fs

include turn.fs
