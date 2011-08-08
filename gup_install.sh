#!/bin/sh
#Copies necessary gup files into system directories
#Run as root!

if [ $1 == "uninstall" ]
then
	rm -f /usr/bin/gupc
	rm -f /usr/include/gupstd.h
	rm -f /usr/include/gupkernel.h
	rm -f /usr/include/gupdevice.h
	rm -f /usr/include/gupmem.h
else
	cp -f gupc.py /usr/bin/gupc
	cp -f gup_lib/gupstd.h /usr/include/
	cp -f gup_lib/gupdevice.h /usr/include/
	cp -f gup_lib/gupmem.h /usr/include/
	cp -f gup_lib/gupkernel.h /usr/include/
fi

