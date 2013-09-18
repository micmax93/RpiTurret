import time
import pygame.mixer as playback
import RPI_GPIO as rpin


def _dummy_token(self):
    return True


class SecuriPi:
    is_armed = False
    move_lvl = 0
    noise_lvl = 0
    is_alarm = False
    _button_lock = False
    token_callback = _dummy_token

    def button_pressed(self, channel):
        if not self._button_lock:
            self._button_lock = True
            # ------------------------
            func = self.token_callback
            if not func():
                self.bad_token()
            else:
            # ------------------------
                name = rpin.get_pin_name(channel)
                if name == 'B_ARM':
                    self.arm_security()
                elif name == 'B_DISARM':
                    self.disarm_security()
                elif name == 'B_ALARM':
                    self.trigger_alarm()
                # ------------------------
            self._button_lock = False

    def bad_token(self):
        for dc in range(0, 10, 1):
            rpin.write('D_TOKEN', dc % 2 == 0)
            time.sleep(0.1)
        rpin.write('D_TOKEN', False)

    def lock_timeout(self):
        for t in range(10, 0, -1):
            rpin.write('D_DISARMED', True)
            time.sleep(t / 100)
            rpin.write('D_DISARMED', False)
            time.sleep(t / 100)
        rpin.write('D_DISARMED', False)

    def trigger_alarm(self):
        rpin.write('D_ALARM', True)
        if not self.is_alarm:
            self.is_alarm = True
            playback.music.play(-1)

    def stop_alarm(self):
        self.is_alarm = False
        rpin.write('D_ALARM', False)
        playback.music.stop()

    def arm_security(self):
        self.lock_timeout()
        self.is_armed = True
        rpin.write('D_ARMED', True)
        rpin.write('D_DISARMED', False)

    def disarm_security(self):
        self.is_armed = False
        self.stop_alarm()
        rpin.write('D_ARMED', False)
        rpin.write('D_DISARMED', True)

    def setup(self):
        rpin.init()
        rpin.set_button_callback('B_ARM', self.button_pressed)
        rpin.set_button_callback('B_DISARM', self.button_pressed)
        rpin.set_button_callback('B_ALARM', self.button_pressed)
        playback.init()
        playback.music.load("Resources/siren.mp3")
        rpin.pwm_set('PWM_MOVEMENT', active=True, duty_cycle=0)
        rpin.pwm_set('PWM_NOISE', active=True, duty_cycle=0)
        rpin.write('D_DISARMED', True)

    def demo(self):
        rpin.write('D_TOKEN', False)
        rpin.pwm_set('PWM_MOVEMENT', active=True, duty_cycle=50, pwm_freq=1)
        rpin.pwm_set('PWM_NOISE', active=True, duty_cycle=0)
        for dc in range(0, 101, 5):
            rpin.pwm_set('PWM_NOISE', duty_cycle=dc)
            rpin.write('D_TOKEN', dc % 4 == 0)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            rpin.pwm_set('PWM_NOISE', duty_cycle=dc)
            rpin.write('D_TOKEN', dc % 2 == 0)
            time.sleep(0.1)
        rpin.pwm_set('PWM_MOVEMENT', active=False)
        rpin.pwm_set('PWM_NOISE', active=False)
        rpin.write('D_TOKEN', False)

    def refresh(self):
        rpin.pwm_set('PWM_MOVEMENT', duty_cycle=self.move_lvl)
        rpin.pwm_set('PWM_NOISE', duty_cycle=self.noise_lvl)

    def update(self, alarm, mov_lvl, noise_lvl):
        if alarm and self.is_armed:
            self.trigger_alarm()
        self.move_lvl = mov_lvl
        self.noise_lvl = noise_lvl
        self.refresh()