import audioop
import pyaudio
import math
#http://stackoverflow.com/questions/2668442/detect-and-record-a-sound-with-python
#http://stackoverflow.com/questions/4160175/detect-tap-with-pyaudio-from-live-mic

class Accumulator:
    value_list = [0]
    max_count = 1
    type = 'sum'

    def __init__(self, size, type='avg'):
        self.max_count = size
        self.type = type

    def add_item(self, val):
        self.value_list.insert(0, val)
        if len(self.value_list) <= self.max_count:
            pass
        elif len(self.value_list) == self.max_count + 1:
            self.value_list.pop()
        else:
            raise Exception("too much items in array")

    def get_value(self):
        sum = 0
        for val in self.value_list:
            sum += val
        if self.type == 'sum':
            return sum
        elif self.type == 'avg':
            return sum / self.max_count


class NoiseDetect:
    def __init__(self):
        self.chunk = 2048
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=self.chunk)

    def get_rms(self):
        data = self.stream.read(self.chunk)
        rms = audioop.rms(data, 2)  #width=2 for format=paInt16
        return rms

    def get_db(self):
        return 10 * math.log10(self.get_rms() / 0.1)


threshold = 43
a = Accumulator(10,'avg')
n = NoiseDetect()
while True:
    val = n.get_db()
    #print val
    if val > threshold:
        print val
    #     a.add_item(val-threshold)
    # else:
    #     a.add_item(0)
    # print a.get_value()
