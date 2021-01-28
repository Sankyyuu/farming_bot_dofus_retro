import time
import threading
from pynput import mouse
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import win32gui

delay = 10.3
button = Button.left
start_stop_key = KeyCode(char='s')
exit_key = KeyCode(char='e')
get_ressources_key = KeyCode(char='r')

def get_pixel_colour(i_x, i_y):
	import win32gui
	i_desktop_window_id = win32gui.GetDesktopWindow()
	i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
	long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
	i_colour = int(long_colour)
	win32gui.ReleaseDC(i_desktop_window_id,i_desktop_window_dc)
	return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)

class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True
        self.isGettingRessources = False
        self.ressource_pos = []
        self.ressource_pos2 = []
        self.next_level_check_pos = (2923, 475)

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False
    
    def start_gettingR(self):
        self.ressource_pos.append(mouseControl.position)
        x, y = mouseControl.position
        self.ressource_pos2.append((x + 12, y + 54))
        color = get_pixel_colour(mouseControl.position[0], mouseControl.position[1])
        print(color)
        print(self.ressource_pos)
        print(self.ressource_pos2)
    
    def stop_gettingR(self):
        self.isGettingRessource = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def get_available_ressource(self):
        color = (0, 0, 0)
        i = 0
        isCollecting = False
        while isCollecting == False:
            mouseControl.position = self.ressource_pos[i]
            mouseControl.click(self.button)
            mouseControl.position = self.ressource_pos2[i]
            time.sleep(0.5)
            color = get_pixel_colour(mouseControl.position[0], mouseControl.position[1])
            print(color)
            if color == (255, 102, 0):
                mouseControl.position = self.ressource_pos2[i]
                mouseControl.click(self.button)
                time.sleep(self.delay)
            else:
                time.sleep(1.2)
            i = i + 1
            if (i == len(self.ressource_pos)):
                return
    
    def run(self):
        while self.program_running:
            while self.running:
                self.get_available_ressource()
            time.sleep(0.1)

    def gettingR(self):
        while self.program_running:
            while self.isGettingRessources:
                time.sleep(0.1)



mouseControl = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == get_ressources_key:
        if click_thread.isGettingRessources:
            click_thread.stop_gettingR()
        else:
            click_thread.start_gettingR()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False

def get_ressources():
    time.sleep(0.1)

# with mouse.Listener(on_click=on_click) as listener:
#     listener.join()
listener = mouse.Listener(on_click=on_click)
listener.start()

with Listener(on_press=on_press) as listener2:
    listener2.join()
