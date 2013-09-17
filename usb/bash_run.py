from subprocess import Popen
import os


def is_token():
    proc = Popen([os.getcwd() + '/checkKeys.sh'])
    return_code = proc.wait()
    if return_code == 0:
        return True
        #print "Success"
    else:
        return False
        #print "Failure"

print is_token()