from RpiPinout.securipi import SecuriPi
from SockThread.sc_server import Host
import UsbToken.validation as token

s = SecuriPi()
s.setup()
s.token_callback = token.is_valid_token
h = Host(5555)
h.set_update_callback(s.update)
try:
    h.start()
except KeyboardInterrupt:
    pass


    #TODO:
    #   check token
    #   value callback
    #   remote client
    #   server version