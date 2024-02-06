
for f in advent	database itverb verb english turn; do cc

-I .. --cpu 65C02 --add-source

$(CL65) -g --verbose --target none --config breadboard.cfg -l rom.lst -m rom.map -Ln rom.sym -o rom.bin rom.asm

__CC65__
