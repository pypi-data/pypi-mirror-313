import time

print('#{"version": 0, "led_count": 500, "fps": 60}', flush=True)

for i in range(10):
    print("#" + "ff0000" * 500, flush=True)
    time.sleep(1)
    print("#" + "0000ff" * 500, flush=True)
    time.sleep(1)