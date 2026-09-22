import subprocess
import sys

def my_function():
    print("Function is running!")
    # do whatever you want here

subprocess.run([
    sys.executable,
    "-m", "mpremote",
    "connect", "/dev/cu.usbmodem14101"
])

my_function()

print("Done!")
subprocess.run([
    sys.executable, "-m", "mpremote",
    "run", "/dev/cu.usbmodem14101",
    "run", "test.py"
])
