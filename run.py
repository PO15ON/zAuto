import time

import requests
from datetime import datetime
from threading import Timer
import os
import pyautogui as auto
import cv2
import numpy as np
import clx.xms



def getSec(hours, mins):
	x = datetime.today()
	y = x.replace(day=x.day, hour=hours, minute=mins, second=0, microsecond=0)
	delta_t = y - x
	print(delta_t)
	return delta_t.total_seconds()

def open_zoom():
	os.system("xdg-open \"zoommtg://hp.zoom.us/join?action=join&confno=[MEETING_ID]\"")

def sendSms(message='Meeting started successfully! at %s' % datetime.now()):
	client = clx.xms.Client(service_plan_id='*********',
	                        token='***********')

	create = clx.xms.api.MtBatchTextSmsCreate()
	create.sender = '447537404817'
	# Add your phone number in format {country_code}*****
	create.recipients = {'*******'}
	create.body = message

	try:
		batch = client.create_batch(create)
	except (requests.exceptions.RequestException,
	        clx.xms.exceptions.ApiException) as ex:
		print('Failed to communicate with XMS: %s' % str(ex))


def open(image1, delay=1, execuse=False, fun=None):
	loop = True
	now = time.time()
	sent = False

	while (loop):
		try:
			# 0: w, 1: h, 2: p[0], 3: p[1]
			r = getLoc(image1)

			auto.moveTo(r[2], r[3])
			print("%s %s" % (r[2], r[3]))
			if image1 != "chat.png":
				auto.click(r[2] + r[0] / 2, r[3] + r[1] / 2, duration=1.0)

			loop = False

		except:
			# print("No link found, sleeping")
			if execuse and int(time.time() - now) > 60*60 and datetime.now().hour >= 10 and not sent:
				# execuseMessage('I was having a problem with zoom, sorry.')
				sendSms("Meeting haven't started yet..")
				sent = True
			time.sleep(delay)


def getLoc(image1):
	image = auto.screenshot()
	template = cv2.imread(image1)
	img_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
	img_gray = cv2.Canny(img_gray, 50, 200)

	template = cv2.Canny(template, 50, 200)
	r = []
	x, y = template.shape[::-1]
	r.insert(0, x)
	r.insert(1, y)
	# Perform match operations.
	res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
	threshold = 0.8

	# Store the coordinates of matched area in a numpy array
	loc = np.where(res >= threshold)

	for pt in zip(*loc[::-1]):
		r.insert(2, pt[0])
		r.insert(3, pt[1])
	return r

def waitForMeeting():
	open('chat.png', execuse=True)

def shutdown():
	os.system("shutdown -h 13:30")

sec = getSec(9, 10)
t = Timer(sec, open_zoom)
t.start()
t.join()
print("done")
print('Script started successfully! at %s' % datetime.now())
shutdown()
print('Shutdown scheduled at 13:30')
waitForMeeting()
print('Meeting started successfully! at %s' % datetime.now())
sendSms('Meeting started successfully!')
