#!/bin/sh
	newDevices=$(lsusb | awk '{print $6}')
	for device in $newDevices
	do
		if grep -q $device usb-authorized-list
			then
				echo 1
				exit 0
			fi
	done
	echo 0
	exit 1



