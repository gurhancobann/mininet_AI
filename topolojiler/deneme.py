
import os
import time

code1="python3 code1.py"
code2="python3 code2.py"

# print("deneme")
os.system("gnome-terminal -e 'bash -c \""+code1+";bash\"'")
time.sleep(5)
print("ikinci")
os.system("gnome-terminal -e 'bash -c \""+code2+";bash\"'")