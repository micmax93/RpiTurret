import RPI_GPIO as rpin
import time

is_armed = False
move_lvl = 0
noise_lvl = 0
is_alarm = False


def triger_alarm(channel):
    is_alarm = True
    rpin.write('D_ALARM',True)

def stop_alarm():
    is_alarm = False
    rpin.write('D_ALARM',False)

def arm_security(channel):
    is_armed = True
    rpin.write('D_ARMED',True)
    rpin.write('D_DISARMED',False)

def disarm_security(channel):
    is_armed = False
    stop_alarm()
    rpin.write('D_ARMED',False)
    rpin.write('D_DISARMED',True)

def setup():
    rpin.init();
    rpin.set_button_callback('B_ARM',arm_security)
    rpin.set_button_callback('B_DISARM',disarm_security)
    rpin.set_button_callback('B_ALARM',triger_alarm)

def demo():
    rpin.write('D_TOKEN',False)
    rpin.pwm_set('PWM_MOVEMENT',active=True, duty_cycle=50, pwm_freq=1)
    rpin.pwm_set('PWM_NOISE',active=True, duty_cycle=0)
    for dc in range(0, 101, 5):
        rpin.pwm_set('PWM_NOISE', duty_cycle=dc)
        rpin.write('D_TOKEN',dc%4==0)
        time.sleep(0.1)
    for dc in range(100, -1, -5):
        rpin.pwm_set('PWM_NOISE', duty_cycle=dc)
        rpin.write('D_TOKEN',dc%2==0)
        time.sleep(0.1)
    rpin.pwm_set('PWM_MOVEMENT',active=False)
    rpin.pwm_set('PWM_NOISE',active=False)
    rpin.write('D_TOKEN',False)