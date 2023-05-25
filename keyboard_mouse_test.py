from pykeyboard import *
from pymouse import *
import keyboard
import time

m = PyMouse()  # 建立鼠标对象
k = PyKeyboard()  # 建立键盘对象

posx = []
posy = []
# posx = [690, 939, 369, 782, 1197, 681, 789]
# posy = [573, 567, 625, 847, 22, 138, 162]
if (len(posx) == 0):
    print("Start recording...")
    print("z: save positioin\nq: quit recording")
    while (not keyboard.is_pressed('q')):
        if (keyboard.is_pressed('z')):
            time.sleep(0.5)
            location = m.position()
            print(location)
            posx.append(location[0])
            posy.append(location[1])

print(posx, posy)

for i in range(len(posx)):
    
    m.click(posx[i], posy[i])
    time.sleep(1)
