from rover_common import aiolcm
from rover_msgs import Countdown
import time

# needed by build system
def main():
    # LCM object handles LCM publishing and subscribing
    lcm = aiolcm.AsyncLCM()

    for i in range(15, 0, -1):
        # Create LCM message object
        countdown = Countdown()
        countdown.num = i

        lcm.publish("/countdown", countdown.encode())
        time.sleep(1)

# if-main block - prevents accidental code execution
if __name__ == "__main__":
    main()