from rover_common import aiolcm
from rover_common.aiohelper import run_coroutines
from rover_msgs import Countdown

# Callback function called when a message is received
def callback(channel, msg):
    countdown = Countdown.decode(msg)
    print(countdown.num)

# needed by build system
def main():
    # LCM object handles LCM publishing and subscribing
    lcm = aiolcm.AsyncLCM()
    lcm.subscribe("/countdown", callback)
    run_coroutines(lcm.loop())

# if-main block - prevents accidental code execution
if __name__ == "__main__":
    main()