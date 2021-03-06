# from Tkinter import tkk
from PIL import Image, ImageTk 
from Graph import * # this line imports the following:
     # import matplotlib
     # matplotlib.use("TkAgg")
     # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
     # from matplotlib.figure import Figure
     # import matplotlib.animation as animation
     # from matplotlib import style
     # import Tkinter as tk
     # import sqlite3
     # from Settings import * # imports default trip points and color definitions
     # style.use("ggplot")
     # import matplotlib.dates as mdates
     # import numpy as np
     # import datetime
     # import time

HEIGHT = 600
WIDTH = 750

class Monitor():
	def __init__ (self, application):
		self.root = tk.Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.close_window)
		self.root.winfo_toplevel().title("Solar Panel Monitor")
		self.root.geometry('{}x{}'.format(WIDTH, HEIGHT))
		self.root.configure(bg=MAIN_BACKGROUND_COLOR)
		self.root.resizable(0,0)

		self.application = application
		self.graph = None 
		self.selected = 0
		self.vars = []

	# ------------- #

	def setupFrames(self):
		# Spacing
		print("Monitor.spacingFrame created") # * debugger line
		spacingFrame = tk.Frame(self.root, bg=MAIN_BACKGROUND_COLOR, width=25)
		spacingFrame.pack(side="left")

		# Connection frame
		print("Monitor.connFrame created") # * debugger line
		self.connFrame = tk.Frame(self.root, bg=WIDGET_BACKGROUND_COLOR, highlightbackground=TEXT_COLOR, highlightcolor=TEXT_COLOR, highlightthickness=1)
		self.connFrame.pack(side="left", fill="y", pady="25")

		# Data frame
		print("Monitor.dataFrame created") # * debugger line
		self.dataFrame = tk.Frame(self.root, bg=WIDGET_BACKGROUND_COLOR, highlightbackground=TEXT_COLOR, highlightcolor=TEXT_COLOR, highlightthickness=1)
		self.dataFrame.pack(side="right", fill="both", padx="25", pady="25")

	def setupTripPoints(self):
		print("Monitor.TripPointFrame created") # * debugger line
		TripPointFrame = tk.Frame(self.topFrame, bg=WIDGET_BACKGROUND_COLOR)
		TripPointFrame.pack(side="left")

		# TripPoint Title
		TripPointFrame_1 = tk.Frame(TripPointFrame, bg=WIDGET_BACKGROUND_COLOR)
		TripPointFrame_1.pack(side="top", padx=40, pady=2.5, fill="x")
		TripPointTitle = tk.Label(TripPointFrame_1, text="Trip points:", bg=WIDGET_BACKGROUND_COLOR, fg=TEXT_COLOR, font='Helvetica_Neue 15 bold')
		TripPointTitle.pack(side="left")

		# Voltage Trip Point Label and Entry
		print("Monitor.TripPointFrame_2 created") # * debugger line
		TripPointFrame_2 = tk.Frame(TripPointFrame, bg=WIDGET_BACKGROUND_COLOR)
		TripPointFrame_2.pack(side="top", pady=2.5, fill="x")
		voltageEntryTripPoint = tk.Label(TripPointFrame_2, text="Max voltage: ", padx=43, fg=TEXT_COLOR, bg=WIDGET_BACKGROUND_COLOR)
		voltageEntryTripPoint.pack(side="left")
		self.voltageEntry = tk.Entry(TripPointFrame_2, font=40, width=5)
		self.voltageEntry.insert(0, DEFAULT_VOLTAGE_TRIP_POINT)
		self.voltageEntry.bind('<FocusIn>', lambda event, i=0: self.on_entry_click(event, i))
		self.voltageEntry.bind('<FocusOut>', lambda event, i=0: self.on_focusout(event, i))
		self.voltageEntry.config(fg=TEXT_COLOR)
		self.voltageEntry.pack(side="left")
		voltageUnit = tk.Label(TripPointFrame_2, text="V", bg=WIDGET_BACKGROUND_COLOR, fg=TEXT_COLOR, font='Helvetica_Neue 12 bold italic')
		voltageUnit.pack(side="left", padx=15)

		# Current Trip Point Label and Entry
		self.TripPointFrame_3 = tk.Frame(TripPointFrame, bg=WIDGET_BACKGROUND_COLOR)
		self.TripPointFrame_3.pack(side="top", pady=2.5, fill="x")
		currentEntryTripPoint = tk.Label(self.TripPointFrame_3, text="Max current: ", padx=43, fg=TEXT_COLOR, bg=WIDGET_BACKGROUND_COLOR)
		currentEntryTripPoint.pack(side="left")
		self.currentEntry = tk.Entry(self.TripPointFrame_3, font=40, width=5)
		self.currentEntry.insert(0, DEFAULT_CURRENT_TRIP_POINT)
		self.currentEntry.bind('<FocusIn>', lambda event, i=1: self.on_entry_click(event, i))
		self.currentEntry.bind('<FocusOut>', lambda event, i=1: self.on_focusout(event, i))
		self.currentEntry.config(fg=TEXT_COLOR)
		self.currentEntry.pack(side="left", padx=1)
		currentUnit = tk.Label(self.TripPointFrame_3, text="A", fg=TEXT_COLOR, bg=WIDGET_BACKGROUND_COLOR, font='Helvetica_Neue 12 bold italic')
		currentUnit.pack(side="left", padx=15)

		# Temperature Trip Point Label and Entry
		TripPointFrame_4 = tk.Frame(TripPointFrame, bg=WIDGET_BACKGROUND_COLOR)
		TripPointFrame_4.pack(side="top", padx=43, pady=2.5, fill="both")
		temperatureEntryTripPoint = tk.Label(TripPointFrame_4, text="Max temperature: ", fg=TEXT_COLOR, bg=WIDGET_BACKGROUND_COLOR)
		temperatureEntryTripPoint.pack(side="left")
		self.temperatureEntry = tk.Entry(TripPointFrame_4, font=40, width=5)
		self.temperatureEntry.insert(0, DEFAULT_TEMPERATURE_TRIP_POINT)
		self.temperatureEntry.bind('<FocusIn>', lambda event, i=2: self.on_entry_click(event, i))
		self.temperatureEntry.bind('<FocusOut>', lambda event, i=2: self.on_focusout(event, i))
		self.temperatureEntry.config(fg=TEXT_COLOR)
		self.temperatureEntry.pack(side="left", padx=15)
		temperatureUnit = tk.Label(TripPointFrame_4, text="C", fg=TEXT_COLOR, bg=WIDGET_BACKGROUND_COLOR, font='Helvetica_Neue 12 bold italic')
		temperatureUnit.pack(side="left")

	def setupCheckboxes(self):
		self.configFrame = tk.Frame(self.topFrame, bg=WIDGET_BACKGROUND_COLOR)
		self.configFrame.pack(side="right", padx=10)

		configFrame = tk.Frame(self.configFrame, bg=WIDGET_BACKGROUND_COLOR)
		configFrame.pack(side="bottom", pady=2.5)

		configFrame1 = tk.Frame(configFrame, bg=WIDGET_BACKGROUND_COLOR)
		configFrame1.pack(side="left", pady=2.5)
		configFrame2 = tk.Frame(configFrame, bg=WIDGET_BACKGROUND_COLOR)
		configFrame2.pack(side="left", pady=2.5)

		# Output Configuration
		A = TEXT_COLOR
		B = WIDGET_BACKGROUND_COLOR
		C = ACTIVE_BUTTON_COLOR

		var4 = tk.IntVar()
		checkboxD = tk.Checkbutton(configFrame2, text="AD", fg=A, bg=B, activeforeground=A, activebackground=C, variable=var4, command=lambda: self.updateCheckbox(3))
		checkboxD.pack(side="bottom", pady=2.5)
		var3 = tk.IntVar()
		checkboxC = tk.Checkbutton(configFrame2, text="BC", fg=A, bg=B, activeforeground=A, activebackground=C, variable=var3, command=lambda: self.updateCheckbox(2))
		checkboxC.pack(side="bottom", pady=2.5)
		var2 = tk.IntVar()
		checkboxB = tk.Checkbutton(configFrame2, text="CD", fg=A, bg=B, activeforeground=A, activebackground=C, variable=var2, command=lambda: self.updateCheckbox(1))
		checkboxB.pack(side="bottom", pady=2.5)
		var1 = tk.IntVar()
		checkboxA = tk.Checkbutton(configFrame2, text="XX", fg=A, bg=B, activeforeground=A, activebackground=C, variable=var1, command=lambda: self.updateCheckbox(0))
		checkboxA.pack(side="bottom", pady=2.5)
		configLabel = tk.Label(configFrame1, text="Config Switch: ", fg=A, bg=B)
		configLabel.pack(side="bottom")
		self.vars = [var1, var2, var3, var4]

	def setupSyncButton(self):
		# SYNC Label
		self.syncFrame = tk.Frame(self.connFrame, bg=WIDGET_BACKGROUND_COLOR)
		self.syncFrame.pack(side="bottom", fill="x")		

	def setupButtons(self):

		A = TEXT_COLOR
		B = WIDGET_BACKGROUND_COLOR
		C = ACTIVE_BUTTON_COLOR
		D = INACTIVE_BUTTON_COLOR

		TripPointEntryButton = tk.Button(self.TripPointFrame_3, text="OK", fg=A, bg=D, activeforeground=A, activebackground=C, font=40, command=lambda: self.application.TripPointInputting(self.voltageEntry.get(), self.currentEntry.get(), self.temperatureEntry.get(), self.selected))
		TripPointEntryButton.pack(side="left", padx=30)

		manualConfigFrame = tk.Frame(self.configFrame, bg=B)
		manualConfigFrame.pack(side="top", pady=2.5)
		self.toggleManualSwitchButton = tk.Button(manualConfigFrame, text="ON", fg=A, bg=D, activeforeground=A, activebackground=C, font=40, command=lambda: self.application.manualSwitchInputting(self.selected))
		self.toggleManualSwitchButton.pack(side="right", pady=5, padx=5)
		manualConfigLabel = tk.Label(manualConfigFrame, text="Manual Switch: ", fg=A, bg=WIDGET_BACKGROUND_COLOR)
		manualConfigLabel.pack(side="right")

	def setupQueryButtons(self):
		print("Monitor.queryButtonFrame created") # * debugger line

		A = TEXT_COLOR
		B = WIDGET_BACKGROUND_COLOR
		C = ACTIVE_BUTTON_COLOR
		D = INACTIVE_BUTTON_COLOR

		queryButtonFrame = tk.Frame(self.dataFrame, bg=WIDGET_BACKGROUND_COLOR)
		queryButtonFrame.pack(side="bottom")
		v1Button = tk.Button(queryButtonFrame, text="V1", fg=A, background=D, activeforeground=A, activebackground=C, font=30, command=lambda: self.graph.setField('voltage_1'))
		v1Button.pack(side="left", pady=15)
		v2Button = tk.Button(queryButtonFrame, text="V2", fg=A, background=D, activeforeground=A, activebackground=C, font=30, command=lambda: self.graph.setField('voltage_2'))
		v2Button.pack(side="left")
		v3Button = tk.Button(queryButtonFrame, text="V3", fg=A, background=D, activeforeground=A, activebackground=C, font=30, command=lambda: self.graph.setField('voltage_3'))
		v3Button.pack(side="left")
		c1Button = tk.Button(queryButtonFrame, text="C1", fg=A, background=D, activeforeground=A, activebackground=C, font=30, command=lambda: self.graph.setField('current_1'))
		c1Button.pack(side="left")
		t1Button = tk.Button(queryButtonFrame, text="T1", fg=A, background=D, activeforeground=A, activebackground=C, font=30, command=lambda: self.graph.setField('temperature_1'))
		t1Button.pack(side="left")
		t2Button = tk.Button(queryButtonFrame, text="T2", fg=A, background=D, activeforeground=A, activebackground=C, font=30, command=lambda: self.graph.setField('temperature_2'))
		t2Button.pack(side="left")
		t3Button = tk.Button(queryButtonFrame, text="T3", fg=A, background=D, activeforeground=A, activebackground=C, font=30, command=lambda: self.graph.setField('temperature_3'))
		t3Button.pack(side="left")
		t4Button = tk.Button(queryButtonFrame, text="T4", fg=A, background=D, activeforeground=A, activebackground=C, font=30, command=lambda: self.graph.setField('temperature_4'))
		t4Button.pack(side="left")
		t5Button = tk.Button(queryButtonFrame, text="T5", fg=A, background=D, activeforeground=A, activebackground=C, font=30, command=lambda: self.graph.setField('temperature_5'))
		t5Button.pack(side="left")
		t6Button = tk.Button(queryButtonFrame, text="T6", fg=A, background=D, activeforeground=A, activebackground=C, font=30, command=lambda: self.graph.setField('temperature_6'))
		t6Button.pack(side="left")

	def setup(self):			
		self.setupFrames()
		self.topFrame = tk.Frame(self.dataFrame, bg=WIDGET_BACKGROUND_COLOR)
		self.topFrame.pack(side="top", fill="x", pady=10)
		# self.topFrame = tk.Frame(self.connFrame, bg=CONNECTOR_WIDGET_COLOR)
		# self.topFrame.pack(side="bottom", fill="x", pady=10)
		self.setupTripPoints()
		self.setupCheckboxes()
		self.setupSyncButton()
		self.setupQueryButtons()

	def updateStatus(self):
		# connLength = len(self.application.c.connections)

		BACKGROUND = WIDGET_BACKGROUND_COLOR

		if self.application.c.isConnected == False:

			# Frame for Widget
			self.statusWidget = tk.Frame(self.connFrame, bg=BACKGROUND)
			self.statusWidget.pack(side="top", fill="x")
			print("a new status widget was created") # * debugger line

			# IP Status
			ipStatus = tk.Label(self.statusWidget, text="Status: Not Connected", fg=RED, bg=BACKGROUND, font='TkDefaultFont 8 bold')
			ipStatus.pack(side="bottom", fill="x", padx=5, pady=5)

		else:

			# Frame for Widget
			self.statusWidget = tk.Frame(self.connFrame, bg=BACKGROUND)
			self.statusWidget.pack(side="top", fill="x")
			print("a new status widget was created") # * debugger line

			# IP Label
			ipLabel = tk.Label(self.statusWidget, text='IP: ' + self.application.c.connection.ip, fg=GREEN, bg=BACKGROUND, font='TkDefaultFont 8')
			ipLabel.pack(side="top", fill="x", padx=10, pady=5)
		
			# IP Status
			ipStatus = tk.Label(self.statusWidget, text="Status: Connected", fg=GREEN, bg=BACKGROUND, font='TkDefaultFont 8 bold')
			ipStatus.pack(side="bottom", fill="x", padx=10, pady=5)

			# self.widgetFrames.append([self.statusWidget, ipLabel, ipStatus]) # * delete this line if widgetFrames[] --> statusWidget rewrite works
			# index = len(self.widgetFrames) - 1 # * and this one
			# self.statusWidget.bind('<Button-1>', lambda event, statusWidget.frameInteraction(event, BACKGROUND))
			# ipLabel.bind('<Button-1>', lambda event, self.labelInteraction(event))
			# ipStatus.bind('<Button-1>', lambda event, self.labelInteraction(event))
			# self.statusWidget.bind("<Enter>", lambda event, self.frameInteraction(event, BACKGROUND))
			# self.statusWidget.bind("<Leave>", lambda event, self.frameInteraction(event, BACKGROUND))

			# '<Button-1>' references a right click of the mouse
			# '<Enter>' means the mouse pointer entered the widget
			# '<Leave>' means the mouse pointer left the widget
			# Why does self.statusWidget have the same action bound to it when the mouse enters and when the mouse leaves?
			# What the fuck does that whole block of code above me even do? It only seems to interact with the connection status displays... 
			# and I only want one of those to show at a time anyway.
			# Why are we making an array of connection status displays lmao like wtf

			# Nevermind, I think I figured out what this does - it looks like it displays each connection (maybe an individual one for each solar panel?) and 
			# allows you to show individual data for any one of them simply by clicking on it. I won't know for sure until I've had a chance to hook this up 
			# to the actual solar panels though.

	# ------------- #

	def switchConnections(self):
		# Change checkbox
		self.updateCheckbox(self.application.c.connection.configSwitch)

		# Change Trip Point values
		self.voltageEntry.delete(0, "end")
		self.voltageEntry.insert(0, self.application.c.connection.voltageValue)
		self.voltageEntry.config(fg=TEXT_COLOR)
		self.currentEntry.delete(0, "end")
		self.currentEntry.insert(0, self.application.c.connection.currentValue)
		self.currentEntry.config(fg=TEXT_COLOR)
		self.temperatureEntry.delete(0, "end")
		self.temperatureEntry.insert(0, self.application.c.connection.temperatureValue)
		self.temperatureEntry.config(fg=TEXT_COLOR)

	def updateCheckbox(self, i):
		for var in self.vars:
			var.set(0)
		for j in range(0, len(self.vars)):
			if j == i:
				self.vars[j].set(1)
		self.application.configSwitchInputting(self.selected, i)
		try:
			self.statusWidget.destroy()
		except:
			pass
		self.updateStatus()

	# def labelInteraction(self, event):
	# 	color = CONNECTOR_WIDGET_COLOR
	# 
	# 	if event.type == 4 :	# if a button is clicked
	# 		self.clearWidgetColors()
	# 		self.switchConnections(self.selected)
	# 		self.graph.a.clear()
	# 
	# 	self.statusWidget.configure(bg=color)

	# def frameInteraction(self, event, bg):
	# 	color = CONNECTOR_WIDGET_COLOR
	# 
	# 	if event.type == 4 :	# if a button is clicked
	# 		self.clearWidgetColors()
	# 		self.switchConnections(self.selected)
	#  		self.graph.a.clear()
	# 
	#  	if event.type == 7 :	# if the mouse enters the widget
	#  		color = CONNECTOR_WIDGET_COLOR if self.selected == index else GRAPH_BACKGROUND_COLOR
	# 
	# 	if event.type == 8 :	# if the mouse exits the widget
	#  		color = CONNECTOR_WIDGET_COLOR if self.selected == index else GRAPH_BACKGROUND_COLOR
	# 
	# 	self.statusWidget.configure(bg=color)

	# def clearWidgetColors(self):
	#  	self.statusWidget.configure(bg=MAIN_BACKGROUND_COLOR)

	# ------------- #

	def on_entry_click(self, event, i):
		if i == 0:
			self.voltageEntry.delete(0, "end")
			self.voltageEntry.insert(0, '')
			self.voltageEntry.config(bg=INACTIVE_BUTTON_COLOR, fg=TEXT_COLOR)
		if i == 1:
			self.currentEntry.delete(0, "end")
			self.currentEntry.insert(0, '')
			self.currentEntry.config(bg=INACTIVE_BUTTON_COLOR, fg=TEXT_COLOR)
		if i == 2:
			self.temperatureEntry.delete(0, "end")
			self.temperatureEntry.insert(0, '')
			self.temperatureEntry.config(bg=INACTIVE_BUTTON_COLOR, fg=TEXT_COLOR)

	def on_focusout(self, event, i):
		if self.application.c.isconnected == False:
			if i == 0:
				if self.voltageEntry.get() == '':
					self.voltageEntry.insert(0, DEFAULT_VOLTAGE_TRIP_POINT)
					self.voltageEntry.config(bg=INACTIVE_BUTTON_COLOR, fg=TEXT_COLOR)
			if i == 1:
				if self.currentEntry.get() == '':
					self.currentEntry.insert(0, DEFAULT_CURRENT_TRIP_POINT)
					self.currentEntry.config(bg=INACTIVE_BUTTON_COLOR, fg=TEXT_COLOR)
			if i == 2:
				if self.temperatureEntry.get() == '':
					self.temperatureEntry.insert(0, DEFAULT_TEMPERATURE_TRIP_POINT)
					self.temperatureEntry.config(bg=INACTIVE_BUTTON_COLOR, fg=TEXT_COLOR)
		else:
			if i == 0:
				if self.voltageEntry.get() == '':
					self.voltageEntry.insert(0, self.application.c.connection.voltageValue)
					self.voltageEntry.config(fg=TEXT_COLOR)
			if i == 1:
				if self.currentEntry.get() == '':
					self.currentEntry.insert(0, self.application.c.connection.currentValue)
					self.currentEntry.config(fg=TEXT_COLOR)
			if i == 2:
				if self.temperatureEntry.get() == '':
					self.temperatureEntry.insert(0, self.application.c.connection.temperatureValue)
					self.temperatureEntry.config(fg=TEXT_COLOR)

	def updateEntries(self):
		self.voltageEntry.delete(0, "end")
		self.voltageEntry.insert(0, self.application.c.connection.voltageValue)
		self.voltageEntry.config(fg=TEXT_COLOR)

		self.currentEntry.delete(0, "end")
		self.currentEntry.insert(0, self.application.c.connection.currentValue)
		self.currentEntry.config(fg=TEXT_COLOR)

		self.temperatureEntry.delete(0, "end")
		self.temperatureEntry.insert(0, self.application.c.connections[self.selected].temperatureValue)
		self.temperatureEntry.config(fg=TEXT_COLOR)

	# def updateStatus(self):
	# 	if len(self.application.c.connections) == 0:
	# 		return
	# 
	# 	self.statusWidget[2]['fg'] = GREEN
	# 	self.statusWidget[2]['text'] = 'Status: Connected'
	# 	self.application.c.connections[self.selected].currentAck = 0

	# ------------- #

	# def clearStatus(self):
	#  	self.statusWidget.destroy()

	def runSetup(self):
		self.setup()
		self.updateCheckbox(0)

	def close_window(self):
		self.application.command = 'quit'

	# ------------- #

	def run(self):
		print("Monitor.run() about to run")
		self.setupButtons()

		# Button Images
		sync_button = Image.open('sync.png')
		sync_image_for_button = ImageTk.PhotoImage(sync_button)
		self.syncButton = tk.Button(self.syncFrame, image=sync_image_for_button, bg=INACTIVE_BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR, 
									command=lambda: self.application.inputting('sync'))
		self.syncButton.config(width="150", height="20")
		self.syncButton.pack(side="bottom")
		self.syncButton.config(image=sync_image_for_button) 
		
		print("Monitor.graph = Graph(self) about to run")
		self.graph = Graph(self)
		print("Monitor.graph = Graph(self) ran")
		self.graph.run()
		print("Monitor.graph.run() ran")
		ani = animation.FuncAnimation(self.graph.f, self.graph.animate, interval=1000)
		print("Monitor.root.mainloop() about to run")
		self.root.mainloop()
		print("Monitor.root.mainloop() ran")

