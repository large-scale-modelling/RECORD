#!/usr/bin/env bash

# To read a local man page then use the following command:

# make -M . command_name

for file in *.md
do
    ORIGINAL=$(echo "$file" | sed 's/\.md$//')
    if [ "$file" == "README.md" ] || [ "$file" == "template.md" ]
    then
        continue
    elif [ ! -f ../bin/"$ORIGINAL" ] && [ ! -f ../lib/"$ORIGINAL" ]
    then
        echo make-man-pages:sh: You no longer need $file
    fi
done
first=
for file in man1/*.1
do
    ORIGINAL=$(echo "$file" | sed 's/\.1$//' | sed 's/man1\///')
    if [ "$file" == "README.md" ] 
    then
        continue
    elif [ ! -f ../bin/"$ORIGINAL" ] && [ ! -f ../lib/"$ORIGINAL" ]
    then
        if [ -z "$first" ]
        then
            echo "make-man-pages:sh: run the following to remove unneeded man pages..."
            first=1
        fi
        echo rm "$file"
    fi
done
for file in ../bin/*.jl ../lib/*.py ../lib/*.sh ../bin/*.py ../bin/*.sh
do
    MARKDOWN=$(basename $file).md
    if [ ! -f "$MARKDOWN" ]
    then
        echo make-man-pages.sh: You need to write $MARKDOWN
    else
        ronn --roff "$MARKDOWN" 2>/dev/null
        mv $(basename $file) man1/$(basename $file).1
    fi
done


