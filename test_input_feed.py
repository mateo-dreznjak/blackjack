#feeds automated input for testing
#simulates 90 rounds until one reshuffle should have happened

import sys

sys.stdout.write("frowa\n10000\n")
for _ in range(90):
    sys.stdout.write("y\n25\nn\nsurrender\n")