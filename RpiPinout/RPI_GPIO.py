import atexit

import RPi.GPIO as GPIO
from RpiPinout.config import *


_input_mapping = {}
_output_mapping = {}
_pwm_mapping = {}


def _try_get(map_name, pin_name):
    if map_name[pin_name] is None:
        raise NameError('Pin name not defined in this mapping')
    else:
        return map_name[pin_name]


def init():
    atexit.register(GPIO.cleanup)
    GPIO.setmode(GPIO.BOARD)
    #GPIO.setwarnings(False)
    for channel, setting in pinout.items():
        if setting['mode'] == 'output':
            _output_mapping[setting['name']] = channel
            GPIO.setup(channel, GPIO.OUT, initial=False)
        elif setting['mode'] == 'input':
            _input_mapping[setting['name']] = channel
            GPIO.setup(channel, GPIO.IN)
        elif setting['mode'] == 'button':
            _input_mapping[setting['name']] = channel
            GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        elif setting['mode'] == 'pwm':
            GPIO.setup(channel, GPIO.OUT)
            _pwm_mapping[setting['name']] = GPIO.PWM(channel, pwm_freq)


def write(pin_name, value):
    GPIO.output(_try_get(_output_mapping, pin_name), value)


def read(pin_name):
    return GPIO.input(_try_get(_output_mapping, pin_name))


def get_pin_name(channel):
    for key, value in _input_mapping.iteritems():
        if value == channel:
            return key
    for key, value in _output_mapping.iteritems():
        if value == channel:
            return key
    for key, value in _pwm_mapping.iteritems():
        if value == channel:
            return key
    return None


def is_button_pressed(pin_name):
    return not GPIO.input(_try_get(_input_mapping, pin_name))


def pwm_set(pin_name, active=None, duty_cycle=None, pwm_freq=None):
    if active is not None:
        if active:
            _try_get(_pwm_mapping, pin_name).start(duty_cycle)
        else:
            _try_get(_pwm_mapping, pin_name).stop()
    elif duty_cycle is not None:
        _try_get(_pwm_mapping, pin_name).ChangeDutyCycle(duty_cycle)
    if pwm_freq is not None:
        _try_get(_pwm_mapping, pin_name).ChangeFrequency(pwm_freq)


def wait_for_input_change(pin_name, rising=True, falling=True):
    channel = _try_get(_input_mapping, pin_name)
    if rising and falling:
        GPIO.wait_for_edge(channel, GPIO.BOTH)
    elif rising:
        GPIO.wait_for_edge(channel, GPIO.RISING)
    elif falling:
        GPIO.wait_for_edge(channel, GPIO.FALLING)


def set_input_callback(pin_name, my_callback, rising=True, falling=True):
    channel = _try_get(_input_mapping, pin_name)
    GPIO.remove_event_detect(channel)
    if rising and falling:
        GPIO.add_event_detect(channel, GPIO.BOTH, callback=my_callback)
    elif rising:
        GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback)
    elif falling:
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=my_callback)


def set_button_callback(pin_name, my_callback):
    channel = _try_get(_input_mapping, pin_name)
    GPIO.remove_event_detect(channel)
    GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=button_bounce)