import audioop
import pyaudio
import math


def empty_callback(val):
    pass


class NoiseDetect:
    def __init__(self):
        self.chunk = 2048
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(#PA_manager = self.p,
                                  format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True
        )

    def get_rms(self):
        data = self.stream.read(self.chunk)
        rms = audioop.rms(data, 2)  #width=2 for format=paInt16
        return rms

    def get_db(self):
        return 10 * math.log10((self.get_rms() / 0.1) + 0.0001)

    threshold = 40

    def getNoiseFactor(self):
        vol = self.get_db()
        if vol >= self.threshold:
            return 100
        else:
            return round((vol / self.threshold) * 100)

    noise_callback = empty_callback
    def run(self):
        while True:
            self.noise_callback(self.getNoiseFactor())

#
# threshold = 35
# #a = Accumulator(10,'avg')
# n = NoiseDetect()
# n.get_rms()
# while True:
#     val = n.get_db()
#     # print val
#     if val > threshold:
#         print val
# #     #     a.add_item(val-threshold)
# #     # else:
# #     #     a.add_item(0)
# #     # print a.get_value()
