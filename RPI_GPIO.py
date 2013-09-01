import RPi.GPIO as GPIO
from config import *
import atexit

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
        if setting['mode'] == 'out':
            _output_mapping[setting['name']] = channel
            GPIO.setup(channel, GPIO.OUT, initial=False)
        elif setting['mode'] == 'in':
            _input_mapping[setting['name']] = channel
            GPIO.setup(channel, GPIO.IN)
        elif setting['mode'] == 'pwm':
            GPIO.setup(channel, GPIO.OUT)
            _pwm_mapping[setting['name']] = GPIO.PWM(channel, pwm_freq)


def write(pin_name, value):
    GPIO.output(_try_get(_output_mapping, pin_name), value)


def read(pin_name):
    return GPIO.input(_try_get(_output_mapping, pin_name))


def pwm_set(pin_name, active=None, duty_cycle=None):
    if active is not None:
        if active:
            _try_get(_pwm_mapping, pin_name).start(duty_cycle)
        else:
            _try_get(_pwm_mapping, pin_name).stop()
    elif duty_cycle is not None:
        _try_get(_pwm_mapping, pin_name).ChangeDutyCycle(duty_cycle)


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
        GPIO.add_event_detect(channel, GPIO.BOTH, callback=my_callback, bouncetime=input_bounce)
    elif rising:
        GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=input_bounce)
    elif falling:
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=my_callback, bouncetime=input_bounce)