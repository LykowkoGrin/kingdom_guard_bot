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
delay_time = 2

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
		
def send_alarm_telegram():
	pass

def click(global_x,global_y):
	pyautogui.moveTo(global_x, global_y, duration=0.25)
	pyautogui.click()

def get_template_pos(gray_img,template,threshold):
	h, w = template.shape
	res = cv2.matchTemplate(gray_img,template,cv2.TM_CCOEFF_NORMED)

	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	if(max_val < threshold):
		return None,None
 
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

def click_on_template(mgr,gray_img,template,threshold):
	for i in range(0,3):
		win_x,win_y,_,_ = mgr.window_size()
	
		x,y = get_template_pos(gray_img,template,threshold)
		if(x == None):
			continue
		h, w = template.shape
		click(win_x + x + w/2,win_y + y + h/2)

		return True
	return False

for i in window_names:
	wnd = WindowMgr()
	wnd.find_window_wildcard(i)
	wnd.resize_to_cool()
	time.sleep(0.5)
	window_mgrs.append(wnd)
	
def main_script(mgr):
	
	window_x,window_y,_,_ = mgr.window_size()
	globus = cv2.cvtColor(cv2.imread("Globus.png",1),cv2.COLOR_BGR2GRAY)
	poisk = cv2.cvtColor(cv2.imread("Poisk.png",1),cv2.COLOR_BGR2GRAY)
	grup_attack = cv2.cvtColor(cv2.imread("GrupAttack.png",1),cv2.COLOR_BGR2GRAY)
	plusik = cv2.cvtColor(cv2.imread("Plusik.png",1),cv2.COLOR_BGR2GRAY)
	poisk_grup = cv2.cvtColor(cv2.imread("PoiskGrup.png",1),cv2.COLOR_BGR2GRAY)
	strelka = cv2.cvtColor(cv2.imread("Strelka.png",1),cv2.COLOR_BGR2GRAY)
	start_grup_attack = cv2.cvtColor(cv2.imread("StartGrupAttack.png",1),cv2.COLOR_BGR2GRAY)
	podtverdit = cv2.cvtColor(cv2.imread("Podtverdit.png",1),cv2.COLOR_BGR2GRAY)
	vpered = cv2.cvtColor(cv2.imread("Vpered.png",1),cv2.COLOR_BGR2GRAY)
	mechi = cv2.cvtColor(cv2.imread("Mechi.png",1),cv2.COLOR_BGR2GRAY)
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,globus,0.5)):
		return 0
	time.sleep(delay_time)
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,poisk,0.5)):
		return 0
	time.sleep(delay_time)
	
	#frame = new_frame_gray(mgr)
	#if(not click_on_template(mgr,frame,grup_attack,0.7)):
	#	return False
	#time.sleep(2)
	for i in range(0,10):
		frame = new_frame_gray(mgr)
		if(not click_on_template(mgr,frame,plusik,0.5)):
			return 0
		time.sleep(0.5)
	time.sleep(delay_time)
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,poisk_grup,0.5)):
		return 0
	time.sleep(delay_time)

	frame = new_frame_gray(mgr)
	strelka_x,strelka_y = get_template_pos(frame,strelka,0.5)
	if(strelka_x == None):

		frame = new_frame_gray(mgr)
		if(not click_on_template(mgr,frame,mechi,0.5)):
			return 0
		time.sleep(delay_time)

		return 1
	
	#ãðóáàÿ ñèëà
	strelka_w,strelka_h = strelka.shape
	pyautogui.click(window_x + strelka_x + strelka_w/2,window_y + strelka_y + strelka_h + 20,1,0.01)#ÇÄÅÑÜ ÍÀ ÑÊÎËÜÊÎ ÒÛÊÀÒÜ ÏÎÄ ÑÒÐÅËÊÓ!!!
	time.sleep(delay_time)
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,start_grup_attack,0.5)):
		return 0
	time.sleep(delay_time)
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,podtverdit,0.5)):
		return 0
	time.sleep(delay_time)
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,vpered,0.5)):
		
		time.sleep(delay_time / 2)
		pyautogui.click()
		time.sleep(delay_time / 2)
		
		frame = new_frame_gray(mgr)
		if(not click_on_template(mgr,frame,mechi,0.5)):
			return 0
		time.sleep(delay_time)
		
		return 2
	
	time.sleep(delay_time)
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,mechi,0.5)):
		return 0
	time.sleep(delay_time)

	
	return 1

	#mask = color_mask(frame,np.array([30,150,50]),np.array([255,255,180]))
	#x,y = find_bigger_counter(mask)
	#cv2.circle(frame, (globus_x, globus_y), 10, (0,0,255), -1)
	
	#cv2.imshow('Screen Capture', frame)
	#if cv2.waitKey(1) & 0xFF == ord('q'):
	#	return False
	
	

#testim = cv2.imread("testim.png",1)
#testim = cv2.cvtColor(testim,cv2.COLOR_BGR2GRAY)
loop_flag = True
while loop_flag:
	for mgr in window_mgrs:
		mgr.set_foreground()
		mgr.resize_to_cool()
		
		script_flag = 1
		while(script_flag == 1):
			script_flag = main_script(mgr) #0 âñå ïëîõî 1 ïðîäîëæàåì öèêë 2 ñëåäóþùèé
		if(script_flag == 0):
			send_alarm_telegram()
			break
		



	#get_template_pos(frame,testim,0.6)



cv2.destroyAllWindows()

