# PURPOSE

This is the directory containing all the man pages for RECORD provenance and
metadata framework.

To read a local man page then use the following command in this directory:

`man -M .` *the_man_page_in_question*

The available man pages are listed in the man1 directory:

To create the man pages after having edited one of the sources in this
directory then run:

`make_man_pages.sh`

This will format the man pages and deliver them to the man1 directory.

# MANIFEST

+ `README.md` - this file.
+ `make-man-pages.sh` - makes the man pages and delivers them to the directory `man1`.
+ `man1` - the directory containing the final man pages.
+  *some-command*.md - the man page itself, written in markdown.
