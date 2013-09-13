pinout = {
	#1 : {'name': '3V3 Power'},
	#1 : {'name': '5V Power'},
	3 : {'name': 'D_ARMED' , 'mode' : 'output'}, #1K8 pull up resistor
	#4 : {'name': '5V Power'},
	5 : {'name': 'D_DISARMED' , 'mode' : 'output'}, #1K8 pull up resistor
	#6 : {'name': 'GND' , 'mode' : ''},
	7 : {'name': 'D_TOKEN' , 'mode' : 'output'},
	#8 : {'name': 'GPIO 14' , 'mode' : 'output'}, #UART
	#9 : {'name': 'GND' , 'mode' : ''},
	#10 : {'name': 'GPIO 15' , 'mode' : ''}, #UART
	11 : {'name': 'D_ALARM' , 'mode' : 'output'},
	#12 : {'name': 'GPIO 18' , 'mode' : ''}, #hardware pwm support
	13 : {'name': 'PWM_NOISE' , 'mode' : 'pwm'},
	#14 : {'name': 'GND' , 'mode' : ''},
	15 : {'name': 'PWM_MOVEMENT' , 'mode' : 'pwm'},
	#16 : {'name': 'GPIO 23' , 'mode' : ''},
	#17 : {'name': '3V3 Power' , 'mode' : ''},
	#18 : {'name': 'GPIO 24' , 'mode' : ''},
	#19 : {'name': 'GPIO 10' , 'mode' : ''},
	26 : {'name': 'B_ALARM' , 'mode' : 'button'},

	#20 : {'name': 'GND' , 'mode' : ''},
	#21 : {'name': 'GPIO 9' , 'mode' : ''},
	22 : {'name': 'B_ARM' , 'mode' : 'button'},
	#23 : {'name': 'GPIO 11' , 'mode' : ''},
	24 : {'name': 'B_DISARM' , 'mode' : 'button'}
	#25 : {'name': 'GND' , 'mode' : ''},
}
pwm_freq = 50
button_bounce = 200
