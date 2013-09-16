#!/bin/bash
echo "Wybierz kod:"
OLD_IFS= $IFS
IFS=$'\r\n'
select kod in $(lsusb)
do
	IFS= $OLD_IFS
	echo $kod | awk '{print $6}' >> usb-authorized-list
	exit 0
done


