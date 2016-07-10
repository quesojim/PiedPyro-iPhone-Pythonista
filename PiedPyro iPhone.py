# coding: utf-8

import ui
import socket
import clipboard
from time import time, sleep, strftime, localtime, gmtime
import datetime
import sound
import console
import threading
from objc_util import *
import csv
global system_armed
system_armed = False
global sequence_running
sequence_running = False
global effectID
global firing_times
firing_times = []
effectID = 1

def sendmessage(message):
	HOST, PORT = "192.168.1.1", 50000
	ctrl_cycle = message
	data = ""
	data += str(ctrl_cycle)
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	try:
		sock.connect((HOST, PORT))
		sock.sendall(bytearray(data, 'utf8'))
		data = sock.recv(1024)
		print (data)
	finally:
		sock.close()

def import_script():
	global firing_times
	firing_times = ["0:00:05.6", "0:00:08.2", "0:00:15.6", "0:00:18.4", "0:00:20.3", "0:00:21.7", "0:00:22.9", "0:00:25.6", "0:00:27.8", "0:00:29.6", "0:00:31.2"]
	
	datasource = [
	{'title': "1	 1	  0:00:05.6		Orange Julius"},
	{'title': "1	 2	  0:00:08.2		Apples Bro"},
	{'title': "1	 3	  0:00:15.6		Blue on Blue"},
	{'title': "1	 4	  0:00:18.4		Apples"},
	{'title': "1	 5	  0:00:20.3		Boom Stick"},
	{'title': "1	 6	  0:00:21.7		ExamplebProd"},
	{'title': "1	 7	  0:00:22.9		Pre-Finale"},
	{'title': "1	 8	  0:00:25.6		Product"},
	{'title': "1	 9	  0:00:27.8		Banger"},
	{'title': "1	 10	  0:00:29.6		Actual Finale 🎉"},
	{'title': "1	 11	  0:00:31.2		Finale 2.0"}
	
]
	lds = ui.ListDataSource(datasource)
	v['firing_times'].data_source = lds
	v['firing_times'].reload_data()
	v['firing_times'].allows_selection = True
	v['firing_times'].selected_row = (0)
	lds.delete_enabled = False
	
def start_show_clock(sender):
	global system_armed
	global sequence_running
	global effectID
	sequence_running = True
	if system_armed == True:
		global t
		t = time()
		timeclock()
		effectID = sound.play_effect('test.mp3')
		v['status_label'].text = ("System Status: Firing Sequence...")
		v['start_sequence_button'].enabled = False
		v['stop_sequence_button'].enabled = True
		v['disarm_system_button'].enabled = False
		v['manual_fire_button'].enabled = False
		
	else:
		console.alert("System Is Not Armed!", "You must arm the system before you can start a firing sequence.", button1="Okay", hide_cancel_button=True)
		
def stop_sequence(sender):
	global effectID
	global sequence_running
	val = console.alert("Stop Running Sequence", "Are you sure you want to stop this sequence?", button1="YES")
	if val == 1:
		sequence_running = False
		sound.stop_effect(effectID)
		v['status_label'].text = ("System Status: ARMED Ready to Fire")
		v['start_sequence_button'].enabled = True
		v['stop_sequence_button'].enabled = False
		v['manual_fire_button'].enabled = True
		v['disarm_system_button'].enabled = True
	
@ui.in_background
def timeclock():
	global firing_times
	currentq = 0
	ms, seconds, minutes, hours, = 0,0,0,0
	global t
	global sequence_running
	while sequence_running == True:
		sleep(0.05)
		v['firing_times'].selected_row = (currentq)
		currenttime = time() - t
		ConvertDuration =str(datetime.timedelta(seconds=currenttime))
		TotalDuration= ConvertDuration[0:9]
		if(currentq != len(firing_times)):
			if (TotalDuration==firing_times[currentq]):
				currentq += 1
				v['showclock'].text_color=("red")
				v['showclock'].text = "   FIRING"
				sendmessage("Fire Q:"+ str(currentq))
				print("Fired Q "+ str(currentq)+ " at " + TotalDuration)
		v['showclock'].text = TotalDuration
		v['showclock'].text_color=('black')
	v['showclock'].text = "0:00:00.0"
	
def disarm_system(sender):
	global system_armed
	system_armed = False
	sound.play_effect('digital:TwoTone2')
	v['status_label'].text_color=('#00e800')
	v['status_label'].text = ("System Status: SAFE")
	v['disarm_system_button'].enabled = False
	v['arm_system_button'].enabled = True

@ui.in_background
def update_time():
		global t
		sleep(0.01)
		v['showclock'].text = strftime("%H:%M:%S", gmtime(time()-t))
	
def arm_system(sender):
	global system_armed
	password = "null"
	if system_armed == False:
		password = console.password_alert("Enter Password to Arm System")
		if (password == "pied"):
			console.alert("WARNING! System Armed", "System Is Now Ready To Fire.  Please Use Caution.", button1="Okay", hide_cancel_button=True)
			system_armed = True
			v['status_label'].text = ("System Status: ARMED Ready to Fire")
			sound.play_effect('digital:TwoTone2')
			v['status_label'].text_color = ("red")
			v['arm_system_button'].enabled = False
			v['continuity_test_button'].enabled=False
			v['disarm_system_button'].enabled=True
		if (password != "pied"):
			console.alert("Password Incorrect", "Please try again", button1= "OK", hide_cancel_button = True)
			arm_system(sender)
			
def hide_show_manual_fire(hide):
	v['manualfireview'].hidden = hide
	v['fire1'].hidden = hide
	v['fire2'].hidden = hide
	v['fire3'].hidden = hide
	v['fire4'].hidden = hide
	v['fire5'].hidden = hide
	v['fire6'].hidden = hide
	v['fire7'].hidden = hide
	v['fire8'].hidden = hide
	v['fire9'].hidden = hide
	v['fire10'].hidden = hide
	v['fire11'].hidden = hide
	v['fire12'].hidden = hide
	v['fire13'].hidden = hide
	v['fire14'].hidden = hide
	v['fire15'].hidden = hide
	v['fire16'].hidden = hide
	v['exit_manual_fire_button'].hidden = hide
	v['manual_fire_label'].hidden = hide
	v['module_segment_control'].hidden = hide

def manual_fire(sender):
	global system_armed
	if system_armed == True:
		choice = console.alert("WARNING! MANUAL FIRE MODE", "You are about to enter manual firing mode.  Do you wish to proceed?", button1="YES")
		if choice == 1:
			v['manual_fire_button'].enabled = False
			hide_show_manual_fire(False)
	else:
		console.alert("System Is Not Armed!", "You must arm the system before you can enter manual firing mode.", button1="Okay", hide_cancel_button=True)

def exit_manual_fire(sender):
	hide_show_manual_fire(True)
	v['manual_fire_button'].enabled = True
	
v = ui.load_view()
import_script()
v['stop_sequence_button'].enabled=False
v['disarm_system_button'].enabled=False
hide_show_manual_fire(True)
v.present()
#ui.View.