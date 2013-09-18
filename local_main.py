from RpiPinout.securipi import SecuriPi
from SockThread.sc_server import Host
import UsbToken.validation as token

s = SecuriPi()
s.setup()
s.token_callback = token.is_valid_token

try:
    while True:
        s.update(alarm=False,mov_lvl=0,noise_lvl=0)
except KeyboardInterrupt:
    pass
