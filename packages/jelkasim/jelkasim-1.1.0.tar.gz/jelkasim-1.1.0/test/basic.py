import sys

import time
from jelka_validator.datawriter import DataWriter

print("Version:", sys.version, file=sys.stderr)

lc = 300
n = 5400
ds = DataWriter(led_count=lc, fps=60)
t = time.time()
for i in range(n):
    ds.write_frame([(i % 256, i % 256, i % 256)] * lc)
    if i % 100 == 0:
        print(f"Printed {i}-th frame at time {time.time() - t}")
