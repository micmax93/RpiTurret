from SockThread.sc_server import Host


def update(a, m, n):
    print a, m, n


h = Host(5555)
h.set_update_callback(update)
try:
    h.start()
except KeyboardInterrupt:
    pass


    #TODO:
    #   check token
    #   value callback
    #   remote client
    #   server version