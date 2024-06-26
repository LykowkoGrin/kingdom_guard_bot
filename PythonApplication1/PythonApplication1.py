import win32gui
import re
import cv2
import numpy as np
import pyautogui
import time
import json
from datetime import datetime

COOL_WIGHT = 450
COOL_HEIGHT = 768
HALAV_STRELKA_X = 390
HALAV_STRELKA_Y = 110

shahta_delay = 15
halava_delay = 15

window_names = ["BlueStacks App Player 8","BlueStacks App Player 7"]
window_mgrs = []
delay_time = 2

###all images
bashnya = cv2.cvtColor(cv2.imread("Bashnya.png",1),cv2.COLOR_BGR2GRAY)
shahta = cv2.cvtColor(cv2.imread("Shahta.png",1),cv2.COLOR_BGR2GRAY)
polychit = cv2.cvtColor(cv2.imread("Polychit.png",1),cv2.COLOR_BGR2GRAY)
krestik = cv2.cvtColor(cv2.imread("Krestik.png",1),cv2.COLOR_BGR2GRAY)
podtverdit2 = cv2.cvtColor(cv2.imread("Podtverdit2.png",1),cv2.COLOR_BGR2GRAY)

free = cv2.cvtColor(cv2.imread("Free.png",1),cv2.COLOR_BGR2GRAY)
halav = cv2.cvtColor(cv2.imread("Halav.png",1),cv2.COLOR_BGR2GRAY)

globus = cv2.cvtColor(cv2.imread("Globus.png",1),cv2.COLOR_BGR2GRAY)
poisk = cv2.cvtColor(cv2.imread("Poisk.png",1),cv2.COLOR_BGR2GRAY)
grup_attack = cv2.cvtColor(cv2.imread("GrupAttack.png",1),cv2.COLOR_BGR2GRAY)###
plusik = cv2.cvtColor(cv2.imread("Plusik.png",1),cv2.COLOR_BGR2GRAY) ###
poisk_grup = cv2.cvtColor(cv2.imread("PoiskGrup.png",1),cv2.COLOR_BGR2GRAY)
strelka = cv2.cvtColor(cv2.imread("Strelka.png",1),cv2.COLOR_BGR2GRAY)
start_grup_attack = cv2.cvtColor(cv2.imread("StartGrupAttack.png",1),cv2.COLOR_BGR2GRAY)
podtverdit = cv2.cvtColor(cv2.imread("Podtverdit.png",1),cv2.COLOR_BGR2GRAY)
vpered = cv2.cvtColor(cv2.imread("Vpered.png",1),cv2.COLOR_BGR2GRAY)
mechi = cv2.cvtColor(cv2.imread("Mechi.png",1),cv2.COLOR_BGR2GRAY)
no_ochkov = cv2.cvtColor(cv2.imread("NoOchkov.png",1),cv2.COLOR_BGR2GRAY)
###

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
		return None,None
 
	top_left = max_loc
	bottom_right = (top_left[0] + w, top_left[1] + h)
 
	cv2.rectangle(gray_img,top_left, bottom_right, 255, 2)
	return top_left

def new_frame(mgr):
	x,y,w,h = mgr.window_size()
	img = pyautogui.screenshot(region=(x,y,w,h))
	return cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
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

def return_the_menu(mgr):
	for i in range(4):
		pyautogui.press('esc')
		time.sleep(0.5)
	frame = new_frame_gray(mgr)
	x,y = get_template_pos(frame,podtverdit2,0.7)
	if(x != None):
		pyautogui.press('esc')
		time.sleep(0.5)
	frame = new_frame_gray(mgr)
	click_on_template(mgr,frame,mechi,0.7)
	time.sleep(delay_time)
	
def add_time_to_json(json_file, time_name, time_obj):
	time_str = time_obj.strftime('%Y-%m-%d %H:%M:%S')
	
	try:
		with open(json_file, 'r') as f:
			data = json.load(f)
	except FileNotFoundError:
		data = {}
	
	data[time_name] = time_str
	
	with open(json_file, 'w') as f:
		json.dump(data, f, indent=4)
	
def get_time_from_json(json_file,time_name):
	with open(json_file, 'r') as f:
		data = json.load(f)

	time_str = data.get(time_name)
	if time_str is None:
		add_time_to_json(json_file, time_name, datetime(1970,1,1,0,0))
		return datetime(1970,1,1,0,0)

	return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
	
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
	window_mgrs.append(wnd) 
	
def start_group_attack(mgr):
	window_x,window_y,_,_ = mgr.window_size()
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,globus,0.5)):
		return 0
	time.sleep(delay_time)
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,poisk,0.5)):
		return 0
	time.sleep(delay_time)
	
	frame = new_frame_gray(mgr)
	click_on_template(mgr,frame,grup_attack,0.83)
	time.sleep(delay_time)
	
	for i in range(0,10):
		frame = new_frame_gray(mgr)
		click_on_template(mgr,frame,plusik,0.7)
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
	
	strelka_w,strelka_h = strelka.shape
	rect_monstr_x0 = int(strelka_x - 2 * strelka_w)
	rect_monstr_y0 = int(strelka_y + strelka_h)
	rect_monstr_w = int(5 * strelka_w)
	rect_monstr_h = int(5 * strelka_h)
	rect_monstr = new_frame(mgr)[rect_monstr_y0:rect_monstr_y0 + rect_monstr_h,rect_monstr_x0:rect_monstr_x0 + rect_monstr_w]
	monstr_mask = color_mask(rect_monstr,np.array([0, 100, 100]),np.array([10, 255, 255]))
	monstr_x,monstr_y = find_bigger_counter(monstr_mask)
	
	pyautogui.click(rect_monstr_x0 + window_x+ monstr_x,rect_monstr_y0 + window_y + monstr_y,1,0.001)

	time.sleep(delay_time)
	###
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,start_grup_attack,0.5)):
		frame = new_frame_gray(mgr)
		if(not click_on_template(mgr,frame,mechi,0.5)):
			return 0
		time.sleep(0.5)
		pyautogui.click()
		time.sleep(delay_time)
		return 1
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
	if(click_on_template(mgr,frame,no_ochkov,0.5)):
		pyautogui.press('esc')
		time.sleep(0.5)
		frame = new_frame_gray(mgr)
		click_on_template(mgr,frame,mechi,0.5)
		time.sleep(0.3)
		pyautogui.click()
		return 2
	
	time.sleep(delay_time)
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,mechi,0.5)):
		return 0
	time.sleep(delay_time)

	
	return 1

def farm_shahta(mgr):
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,bashnya,0.5)):
		return 0
	time.sleep(delay_time)
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,shahta,0.5)):
		return 0
	time.sleep(delay_time)
	
	frame = new_frame_gray(mgr)
	click_on_template(mgr,frame,polychit,0.5)
	time.sleep(delay_time)
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,podtverdit2,0.8)):
		if(not click_on_template(mgr,frame,krestik,0.5)):
			return 0
	time.sleep(delay_time)
	
	
	frame = new_frame_gray(mgr)
	if(not click_on_template(mgr,frame,mechi,0.5)):
		return 0
	time.sleep(delay_time)
	
	return 2

def claim_prise(mgr):
	frame = new_frame_gray(mgr)
	#390 110
	if(not click_on_template(mgr,frame,halav,0.6)):
		return 0
	time.sleep(delay_time)
	
	x_win,y_win,w_win,h_win = mgr.window_size()
	for i in range(12):
		click(x_win + HALAV_STRELKA_X,y_win + HALAV_STRELKA_Y)
		time.sleep(0.3)
	
	frame = new_frame_gray(mgr)
	while(click_on_template(mgr,frame,free,0.7)):
		time.sleep(0.5)
		pyautogui.press('esc')
		time.sleep(0.5)
		frame = new_frame_gray(mgr)
	
	
	pyautogui.scroll(-1)
	time.sleep(0.3)
	pyautogui.scroll(-1)
	time.sleep(1)
	
	frame = new_frame_gray(mgr)
	while(click_on_template(mgr,frame,free,0.7)):
		time.sleep(0.3)
		pyautogui.press('esc')
		time.sleep(0.3)
		frame = new_frame_gray(mgr)
	
	time.sleep(0.3)
	pyautogui.press('esc')
	return 2

loop_flag = True
while loop_flag:
	i = 0
	for mgr in window_mgrs:
		try:
			
			mgr.set_foreground()
			time.sleep(delay_time)
			mgr.resize_to_cool()
			window_name = window_names[i]
			
			add_time_to_json("timings.json",window_name + " group attack",datetime.now())
			script_flag = 1
			while(script_flag != 2):
				script_flag = start_group_attack(mgr) 
				if(script_flag == 0):
					return_the_menu(mgr)
				
			if((datetime.now() - get_time_from_json("timings.json",window_name + " farm shahta")).total_seconds() / 60 > shahta_delay):
				add_time_to_json("timings.json",window_name + " farm shahta",datetime.now())
				script_flag = 1
				while(script_flag != 2):
					script_flag = farm_shahta(mgr) 
					if(script_flag == 0):
						return_the_menu(mgr)

			if((datetime.now() - get_time_from_json("timings.json",window_name + " claim prise")).total_seconds() / 60 > halava_delay):
				add_time_to_json("timings.json",window_name + " claim prise",datetime.now())
				script_flag = 1
				while(script_flag != 2):
					script_flag = claim_prise(mgr)
					if(script_flag == 0):
						return_the_menu(mgr)
					
		except:
			return_the_menu(mgr)
		i+=1



cv2.destroyAllWindows()

