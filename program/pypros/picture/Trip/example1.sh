#!/bin/sh
for file in `ls *.png`; do
    cnv="convert ${file} ./cnv/${file%.png}.eps"
    eval ${cnv}
done