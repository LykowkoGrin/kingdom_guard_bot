import win32gui
import re
import cv2
import numpy as np
import pyautogui
import time

COOL_WIGHT = 450
COOL_HEIGHT = 768
window_names = ["BlueStacks App Player 3"]
window_mgrs = []

class WindowMgr:
	"""Encapsulates some calls to the winapi for window management"""

	def __init__ (self):
		"""Constructor"""
		self._handle = None

	def find_window(self, class_name, window_name=None):
		"""find a window by its class_name"""
		self._handle = win32gui.FindWindow(class_name, window_name)

	def _window_enum_callback(self, hwnd, wildcard):
		"""Pass to win32gui.EnumWindows() to check all the opened windows"""
		if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
			self._handle = hwnd

	def find_window_wildcard(self, wildcard):
		"""find a window whose title matches the wildcard regex"""
		self._handle = None
		win32gui.EnumWindows(self._window_enum_callback, wildcard)

	def set_foreground(self):
		"""put the window in the foreground"""
		win32gui.SetForegroundWindow(self._handle)
		
	def window_size(self):
		rect = win32gui.GetWindowRect(self._handle)
		x = rect[0]
		y = rect[1]
		w = rect[2] - x
		h = rect[3] - y
		return x,y,w,h;
	
	def resize_to_cool(self):
		x,y,w,h = self.window_size()
		win32gui.MoveWindow(self._handle, x, y, COOL_WIGHT, COOL_HEIGHT, True)

def click(global_x,global_y):
	pyautogui.moveTo(global_x, global_y, duration=0.25)
	pyautogui.click()

def get_template_pos(gray_img,template,threshold):
	h, w = template.shape
	res = cv2.matchTemplate(gray_img,template,cv2.TM_CCOEFF_NORMED)

	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	if(max_val < threshold):
		return None
 
	top_left = max_loc
	bottom_right = (top_left[0] + w, top_left[1] + h)
 
	cv2.rectangle(gray_img,top_left, bottom_right, 255, 2)
	return top_left

def new_frame(mgr):
	x,y,w,h = mgr.window_size()
	img = pyautogui.screenshot(region=(x,y,w,h))
	return np.array(img)
def new_frame_gray(mgr):
	return cv2.cvtColor(new_frame(mgr),cv2.COLOR_BGR2GRAY)

def color_mask(image,hsv_lower,hsv_upper):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	thresh = cv2.inRange(hsv, hsv_lower, hsv_upper)
	return thresh

def find_bigger_counter(thresh):
	moments = cv2.moments(thresh, 1)
	dM01 = moments['m01']
	dM10 = moments['m10']
	dArea = moments['m00']
	return int(dM10 / dArea),int(dM01 / dArea)

for i in window_names:
	wnd = WindowMgr()
	wnd.find_window_wildcard(i)
	wnd.resize_to_cool()
	time.sleep(0.5)
	window_mgrs.append(wnd)
	
def main_script(mgr):
	mgr.set_foreground()
	frame = new_frame(mgr)
	mask = color_mask(frame,np.array([30,150,50]),np.array([255,255,180]))
	x,y = find_bigger_counter(mask)
	cv2.circle(frame, (x, y), 10, (0,0,255), -1)
	
	cv2.imshow('Screen Capture', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		return False


	return True
	
	

#testim = cv2.imread("testim.png",1)
#testim = cv2.cvtColor(testim,cv2.COLOR_BGR2GRAY)
loop_flag = True
while loop_flag:
	for mgr in window_mgrs:
		mgr.set_foreground()
		main_script(mgr)
	
	#get_template_pos(frame,testim,0.6)



cv2.destroyAllWindows()

