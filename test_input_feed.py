#feeds automated input for testing
#simulates 1000 rounds trying to split every hand

import sys

sys.stdout.write("frowa\n10000\n")
for _ in range(1000):
    sys.stdout.write("y\n25\nn\ny\nsplit\nstand\nstand\n")