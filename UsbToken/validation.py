from subprocess import Popen
import os


def is_valid_token():
    proc = Popen([os.getcwd() + '/UsbToken/checkKeys.sh'])
    return_code = proc.wait()
    if return_code == 0:
        return True
        #print "Success"
    else:
        return False
        #print "Failure"