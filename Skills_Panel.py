# INDEX OF CLASSES AND METHODS
'''
class Skills_Panel
	def __init__(self, panel)
	def Create_Build_Header(self, panel):
	def Create_Build_Frame(self, panel):
	def Create_Schedule_Header(self, panel):
	def Create_Schedule_Footer(self, panel):
	def Create_Dialog_Box(self, panel, title, buttons):
	def Dialog_Box_Onclick(self, result):
	def Add_Edit_Button_Onclick(self, location):
	def ClearAll_Button_Onclick(self):		
	def Plan_Training_Schedule(self):	
	def Update_Schedule_Frames(self):	
	def Skills_Menu_Onchange(self, name):	
	def Scroll_Build_Frame(self, event):	
	def Scroll_Schedule_Frame(self, event):
	def Create_Build_List_Skill(self, parent, name, hidden, order, info, start, target, goal):	
	
class Build_List_Skill:
	def __init__(self, parent, name, hidden, order, info, start, target, goal):	
	def Set_Training_Rate(self):	
	def Update_Adjusted_Training(self, new_start, ranks_taken):	
'''

#!/usr/bin/python

import tkinter
import re
import math
import Pmw
import Globals as globals

  
# Skills panel is responsible for handling character skill training from level 0 to 100.
# This panel is made of 5 sub frames. 
#  Build buttons (Upper Left) - Contains buttons that add new skills to the build list, calculate out a build, or reset the build list
#  Build skill list (Middle/Lower Left) - Contains a list of skills that user wants to train in
#  Schedule buttons (Upper Right) - These button can alter how the Schedule skill list looks
#  Scheduled skills list (Middle Right) - This list every skill available to the character along with rank information.
#  Scheduled footer (Lower Right) - The totals and training point costs are calculated here
class Skills_Panel:  
	def __init__(self, panel):	
		self.schedule_skills = []
		self.SkP_radio_var = tkinter.IntVar()				
		
		# Popup Dialog Box variables
		self.add_order_menu = ""
		self.dialog_menu_skill_names = ""
		self.edit_order_menu = ""
		self.edit_skills_menu = ""
		self.menu_size = 1
		self.dialog_max_ranks = 0
		self.vars_dialog_skill = tkinter.StringVar()
		self.vars_dialog_order = tkinter.StringVar()
		self.vars_dialog_info = tkinter.StringVar()
		self.vars_dialog_hide = tkinter.StringVar()
		self.vars_dialog_goal = tkinter.StringVar()
		self.vars_dialog_slevel = tkinter.StringVar()
		self.vars_dialog_tlevel = tkinter.StringVar()
		self.vars_dialog_errormsg = tkinter.StringVar()
		self.vars_dialog_edit_location = tkinter.IntVar()		
		
		# Schedule Level Calculation variable lists
		self.total_regained_ptp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_regained_mtp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_available_ptp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_available_mtp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_cost_ptp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_cost_mtp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_converted_ptp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_converted_mtp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_leftover_ptp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_leftover_mtp_by_level = [tkinter.IntVar() for i in range(101)]
		
		# Schedule Footer variables
		self.vars_sfooter_ptp_earned = tkinter.IntVar()
		self.vars_sfooter_mtp_earned = tkinter.IntVar()
		self.vars_sfooter_ptp_regained = tkinter.IntVar()
		self.vars_sfooter_mtp_regained = tkinter.IntVar()
		self.vars_sfooter_total_ptp_available = tkinter.IntVar()
		self.vars_sfooter_total_mtp_available = tkinter.IntVar()
		self.vars_sfooter_ptp_total_cost = tkinter.IntVar()
		self.vars_sfooter_mtp_total_cost = tkinter.IntVar()
		self.vars_sfooter_ptp_converted = tkinter.IntVar()
		self.vars_sfooter_mtp_converted = tkinter.IntVar()
		self.vars_sfooter_ptp_leftover = tkinter.IntVar()
		self.vars_sfooter_mtp_leftover = tkinter.IntVar()	
			
		# This creates the popup box that is used to Add or Edit skills on the build skills list	
		self.dialog_box = self.Create_Dialog_Box(panel, "Add Skill", ("Add Skill,Cancel"))
		
		# This counter is used to track what level is being shown in the schedule list frame
		self.level_counter = ""     #Becomes a Pmw.counter later on
					
		#Create all the sub-frames of the panel
		self.UL_Frame = self.Create_Build_Header(panel)
		self.ML_Frame = self.Create_Build_Frame(panel)
		self.UR_Frame = self.Create_Schedule_Header(panel)
		self.MR_Frame = self.Create_Schedule_Frame(panel)
		self.LR_Frame = self.Create_Schedule_Footer(panel)	
		
		#Make the frames visible
		self.UL_Frame.grid(row=0, column=0, sticky="nw")
		self.ML_Frame.grid(row=1, column=0, sticky="nw", rowspan=2)
		self.UR_Frame.grid(row=0, column=1, sticky="nw")
		self.MR_Frame.grid(row=1, column=1, sticky="nw")
		self.LR_Frame.grid(row=2, column=1, sticky="nw")	
		
		# Intitialize the skill list
		globals.db_cur.execute("SELECT name, type, subskill_group, redux_value FROM Skills")
		globals.db_con.commit()		
		data = globals.db_cur.fetchall()		
		for skill in data:
			globals.skill_names.append(skill[0])		
			globals.character.skills_list[skill[0]] = globals.Skill(skill)
			globals.character.skills_list[skill[0]].Create_SkP_schedule_row(self.MR_Frame.interior())
		'''
		globals.db_cur.execute("SELECT DISTINCT subskill_group FROM Skills")
		globals.db_con.commit()		
		data = globals.db_cur.fetchall()			
		for group in data:
			globals.character.subskill_groups.append(group)
		'''
		#initialize defaults
		self.ML_Frame.bind_class("SkP_build", "<MouseWheel>", self.Scroll_Build_Frame)
		self.MR_Frame.bind_class("SkP_schedule", "<MouseWheel>", self.Scroll_Schedule_Frame)
		self.dialog_box.withdraw()
		self.SkP_radio_var.set(1)
		self.level_counter.setvalue(0)
							
	
	# This frame creates 3 buttons used for adding new build skills to the build frame's list, calculating out an existing build list, or clearing the entire panel to start new
	def Create_Build_Header(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 547, hull_height = 50)
		myframe.component("borderframe").config(borderwidth=0)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")	
		myframe_inner = myframe.interior()

		# topframe holds the 3 buttons
		topframe = tkinter.Frame(myframe_inner)		
		topframe.grid(row=0, column=0, sticky="w")			
		tkinter.Button(topframe, height="1", text="Add Skill", command=lambda v="": self.Add_Edit_Button_Onclick(v)).grid(row=0, column=0)		
		tkinter.Button(topframe, height="1", text="Calculate Build", command=self.Plan_Training_Schedule).grid(row=0, column=1)	
		tkinter.Button(topframe, text="Clear", command=self.ClearAll_Button_Onclick).grid(row=0, column=2, sticky="w", pady="1")	
		
		# this is frame will hold the title of the build schedule frame. This is done to allow the other frame to scroll but not lose the title header
		title_scrollframe = Pmw.ScrolledFrame(myframe_inner, usehullsize = 1, hull_width = 530, hull_height = 26 )		
		title_scrollframe.configure(hscrollmode = "none")		
		title_scrollframe.grid(row=3, column=0, sticky="w")		
		title_scrollframe_inner = title_scrollframe.interior()						
		
		# add all labels to the tittle header
		tkinter.Frame(title_scrollframe_inner).grid(row=3, column=0, columnspan=3)	
		tkinter.Label(title_scrollframe_inner, width="3", bg="lightgray", text="Hide").grid(row=0, column=0, padx="1")
		tkinter.Label(title_scrollframe_inner, width="6", bg="lightgray", text="Order").grid(row=0, column=1, padx="1")
		tkinter.Label(title_scrollframe_inner, width="26", bg="lightgray", text="Skill Name").grid(row=0, column=2, padx="1")
		tkinter.Label(title_scrollframe_inner, width="12", bg="lightgray", text="Cost & Ranks").grid(row=0, column=3, padx="1")
		tkinter.Label(title_scrollframe_inner, width="5", bg="lightgray", text="Goal").grid(row=0, column=4, padx="1")
		tkinter.Label(title_scrollframe_inner, width="5", bg="lightgray", text="S.lvl").grid(row=0, column=5, padx="1")
		tkinter.Label(title_scrollframe_inner, width="5", bg="lightgray", text="T.lvl").grid(row=0, column=6, padx="1")
		tkinter.Label(title_scrollframe_inner, width="4", bg="lightgray", text="Edit").grid(row=0, column=7, padx="1")
		
		return myframe
		
		
	# The build frame does nothing but store multiple rows of Build List Skill objects. See that class below for more information	
	def Create_Build_Frame(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 547, hull_height = 474)			
		myframe.configure(hscrollmode = "none", vscrollmode = "static")					
		myframe.bindtags("SkP_build")
		
		return myframe			
		
	# This frame contains:
	# PMW counter object that is used to change what level the schedule frame is displaying
	# 3 radio buttons that change what skills will appear in the schedule frame
	# A title header for the schedule frame which allows that frame scroll independently of the header
	def Create_Schedule_Header(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 535, hull_height = 50)
		myframe.component("borderframe").config(borderwidth=0)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")			
		myframe_inner = myframe.interior()		
						
		topframe = tkinter.Frame(myframe_inner)	
		topframe.grid(row=0, column=0, sticky="w")	
		
		# The level counter will show a number between 0 and 100. This number indicates what level to show the training for in the schedule frame
		tlvl_frame = tkinter.Frame(topframe)
		tlvl_frame.grid(row=0, column=0, sticky="w", padx=3, pady="1")			
		self.level_counter = Pmw.Counter(tlvl_frame, entryfield_entry_width = 3, entryfield_validate = { 'validator':'numeric', 'min':0, 'max':100 }, labelpos = 'w', label_text = 'Skills at Level', entryfield_value = 0, datatype = "numeric", entryfield_modifiedcommand=self.Update_Schedule_Frames )
		self.level_counter.grid(row=0, column=0, sticky="w", pady="1")
		
		# These radio buttons are linked together and determine what rows will be shown in the schedule frame
		# Show All Skills - Every skill the profession can train in is shown.
		# Show All Trained - Only show skills that the character has trained it, regardless of level. If the character has 1 or more ranks in a skill at level 100, the skill will be shown on every level.
		# Shown Trained this Level - Only show skills that were trained in at this specific level.
		tkinter.Radiobutton(topframe, anchor="w", text="All", command=self.Update_Schedule_Frames, var=self.SkP_radio_var, value=1).grid(row=0, column=1)	
		tkinter.Radiobutton(topframe, anchor="w", text="All Trained", command=self.Update_Schedule_Frames, var=self.SkP_radio_var, value=2).grid(row=0, column=2)		
		tkinter.Radiobutton(topframe, anchor="w", text="Trained this Level", command=self.Update_Schedule_Frames, var=self.SkP_radio_var, value=3).grid(row=0, column=3)

		title_scrollframe = Pmw.ScrolledFrame(myframe_inner, usehullsize = 1, hull_width = 515, hull_height = 28 )		
		title_scrollframe.configure(hscrollmode = "none")		
		title_scrollframe.grid(row=3, column=0, sticky="w")	
		title_scrollframe_inner = title_scrollframe.interior()							
		
		tkinter.Frame(title_scrollframe_inner).grid(row=1, column=2, sticky="w", pady="1")	
		tkinter.Label(title_scrollframe_inner, width="26", bg="lightgray", text="Skill Name").grid(row=0, column=0, padx="1")
		tkinter.Label(title_scrollframe_inner, width="6", bg="lightgray", text="Ranks").grid(row=0, column=1, padx="1")
		tkinter.Label(title_scrollframe_inner, width="8", bg="lightgray", text="Cost").grid(row=0, column=2, padx="1")
		tkinter.Label(title_scrollframe_inner, width="10", bg="lightgray", text="Total Ranks").grid(row=0, column=3, padx="1")
		tkinter.Label(title_scrollframe_inner, width="6", bg="lightgray", text="Bonus").grid(row=0, column=4, padx="1")
		tkinter.Label(title_scrollframe_inner, width="10", bg="lightgray", text="Sum Cost").grid(row=0, column=5, padx="1")
	
		return myframe		
		

	# This frame will hold SkP_schedule_row objects for skills the character can train in. For more information, please see the Skill class in Globals.py
	def Create_Schedule_Frame(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 535, hull_height = 395)		
		myframe_inner = myframe.interior()
		myframe.configure(hscrollmode = "none")						
		myframe.bindtags("SkP_schedule")					
		myframe_inner.bindtags("SkP_schedule")
	
		return myframe	
	

	# This frame contains information about PTP and MTP for the current level. 
	# Earned - How many PTP/MTP where gained from increasing in level.
	# Regained - This is the sum of the left over PTP/MTP from the previous level plus the difference between the total cost of all skill ranks from the previous level minus the total cost of all skill ranks from the current level
	# Available - Earned PTP/MTP + Regained PTP/MTP
	# Total Cost - Sum of all PTP/MTP costs from skills trained this level
	# Conversions - How many of one TP were converted to the other TP type
	# Leftover - Available PTP/MTP - Total Cost - Conversions 
	def Create_Schedule_Footer(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 535, hull_height = 80)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")			
		myframe_inner = myframe.interior()									
		
		tkinter.Label(myframe_inner, width="10", bg="lightgray", text="Earned").grid(row=0, column=1, padx="1")
		tkinter.Label(myframe_inner, width="10", bg="lightgray", text="Regained").grid(row=0, column=2, padx="1")
		tkinter.Label(myframe_inner, width="10", bg="lightgray", text="Available").grid(row=0, column=3, padx="1")
		tkinter.Label(myframe_inner, width="10", bg="lightgray", text="Total Cost").grid(row=0, column=4, padx="1")
		tkinter.Label(myframe_inner, width="10", bg="lightgray", text="Conversions").grid(row=0, column=5, padx="1")
		tkinter.Label(myframe_inner, width="10", bg="lightgray", text="Leftover").grid(row=0, column=6, padx="1")

		tkinter.Label(myframe_inner, width=5, text="").grid(row=0, column=0, sticky="w", padx="1", pady="1")		
		tkinter.Label(myframe_inner, width="5", bg="lightgray", text="PTP").grid(row=1, column=0, padx="2", pady="1")
		tkinter.Label(myframe_inner, width="5", bg="lightgray", text="MTP").grid(row=2, column=0, padx="2", pady="1")	
		
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_ptp_earned).grid(row=1, column=1, padx="1")
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_mtp_earned).grid(row=2, column=1, padx="1")	
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_ptp_regained).grid(row=1, column=2, padx="1")
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_mtp_regained).grid(row=2, column=2, padx="1")	
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_total_ptp_available).grid(row=1, column=3, padx="1")	
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_total_mtp_available).grid(row=2, column=3, padx="1")
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_ptp_total_cost).grid(row=1, column=4, padx="1")
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_mtp_total_cost).grid(row=2, column=4, padx="1")		
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_ptp_converted).grid(row=1, column=5, padx="1")	
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_mtp_converted).grid(row=2, column=5, padx="1")
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_ptp_leftover).grid(row=1, column=6, padx="1")
		tkinter.Label(myframe_inner, width="10", bg="lightgray", textvar=self.vars_sfooter_mtp_leftover).grid(row=2, column=6, padx="1")		
					
		return myframe	

		
	# The popup dialog box is used to allow add a new skill or edit an existing skill in the build frame. The frame consists of the following parts
	# Skill Name - Drop down menu to select which skill to train in.
	# Cost and Ranks - How many PTP and MTP it costs to train a single rank in the skill and the maximum ranks you can train in the skill for a single level.
	# Training Order - Determines what order the planner will try to train the skill. If the skill cannot be fully trained at a level, ALL training below it is pushed back to the next level.
	# Hide - Any skill with a checked Hide box will be ignored when build schedule is calculated.
	# Goal - This is either a number greater that 0 for how many ranks to train in the skill or a rate (1x, 1.125x, 2.75x, etc) for how many ranks to train each level.
	# Level Range - Indicates a range for 0 to 100. This is how much time you will give the planner to train to your Goal or how many level you want to train your Goal rate
	def Create_Dialog_Box(self, panel, title, buttons):
		dialog = Pmw.Dialog(panel,
            buttons = (buttons.split(",")),
            title = title,
            command = self.Dialog_Box_Onclick)
			
		dialog.transient(panel)	
		dialog.resizable(width=0, height=0)		
		dialog.geometry('300x280+600+300')
				
		myframe = Pmw.ScrolledFrame(dialog.interior(), usehullsize = 1, hull_width = 300, hull_height = 280)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")		
		myframe.grid(row=0, column=0, sticky="nw")	
		myframe_inner = myframe.interior()	
		
		error_font = tkinter.font.Font(family="Helvetica", size=10)
				
		tkinter.Label(myframe_inner, width="12", anchor="w", bg="lightgray", text="Skill Name").grid(row=0, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="12", anchor="w", bg="lightgray", text="Cost & Ranks").grid(row=1, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="12", anchor="w", textvar=self.vars_dialog_info).grid(row=1, column=1, sticky="w")
		tkinter.Label(myframe_inner, width="12", anchor="w", text="").grid(row=2, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="12", anchor="w", bg="lightgray", text="Training Order").grid(row=3, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="12", anchor="w", bg="lightgray", text="Hide").grid(row=4, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="12", anchor="w", text="").grid(row=5, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="12", anchor="w", bg="lightgray", text="Goal").grid(row=6, column=0, sticky="w", pady=1)
		tkinter.Label(myframe_inner, width="12", anchor="w", bg="lightgray", text="Level Range").grid(row=7, column=0, sticky="w")			
								
		tkinter.Checkbutton(myframe_inner, command="", variable=self.vars_dialog_hide).grid(row=4, column=1, sticky="w")		
	
		
		self.dialog_menu_skill_names = tkinter.OptionMenu(myframe_inner, self.vars_dialog_skill, "", command="")
		self.dialog_menu_skill_names.config(width=27, heigh=1)	
		
		self.add_order_menu = tkinter.ttk.OptionMenu(myframe_inner, self.vars_dialog_order, "1", command="")
		self.add_order_menu.config(width=2)	
		
		self.edit_order_menu = tkinter.ttk.OptionMenu(myframe_inner, self.vars_dialog_order, "1", command="")
		self.edit_order_menu.config(width=2)			
		
		self.add_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.edit_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))	
			
		self.add_order_menu.grid(row=3, column=1, sticky="w")			
		self.dialog_menu_skill_names.grid(row=0, column=1, sticky="w", columnspan=4)		
		
		
		lvlframe = tkinter.Frame(myframe_inner)
		lvlframe.grid(row=7, column=1, sticky="w", columnspan=4)	
		Pmw.Counter(lvlframe, entryfield_entry_width = 3, entryfield_validate = { 'validator':'numeric', 'min':0, 'max':100 }, labelpos = 'w', label_text = 'Start', entryfield_value = 0, datatype = "numeric", entryfield_entry_textvariable=self.vars_dialog_slevel).grid(row=0, column=0, sticky="w")
		Pmw.Counter(lvlframe, entryfield_entry_width = 3, entryfield_validate = { 'validator':'numeric', 'min':0, 'max':100 }, labelpos = 'w', label_text = 'Target', entryfield_value = 0, datatype = "numeric", entryfield_entry_textvariable=self.vars_dialog_tlevel).grid(row=0, column=1, sticky="w", columnspan=2)
		goal_box = tkinter.Entry(myframe_inner, width="6", justify="center", validate="key", validatecommand="", textvariable=self.vars_dialog_goal).grid(row=6, column=1, sticky="w", padx=2)
#		tkinter.Label(myframe_inner, anchor="w", font="-weight bold", wraplength=300, justify="left", textvariable=self.vars_dialog_errormsg).grid(row=8, column=0, sticky="w", columnspan=4)
		tkinter.Label(myframe_inner, anchor="w", font=error_font, wraplength=300, justify="left", textvariable=self.vars_dialog_errormsg).grid(row=8, column=0, sticky="w", columnspan=4)				
			
		return dialog

		
	# This handles button all the button events that occur in the Add/Edit dialog box.	
	def Dialog_Box_Onclick(self, result):
		i = 0

		# Occurs if the user clicks the Cancel button or the "x" in the upper right corner. Just close the box and don't do anything.
		if result is None or result == "Cancel":
			self.dialog_box.withdraw()
			self.dialog_box.grab_release()
			return
			
		# Error checking for Add/Edit Skill choices. Makes sure that your Goal and Level Range is formatted correctly.
		elif result == "Add Skill" or result == "Update Skill":
			if int(self.vars_dialog_slevel.get()) > int(self.vars_dialog_tlevel.get()):
				self.vars_dialog_errormsg.set("ERROR: Start level cannot be greater than target level." )
				return
			elif len(self.vars_dialog_goal.get()) == 0 or self.vars_dialog_goal.get() == "0" or not re.search(r"(^[1-9]\d{0,2}$)|(^[1-3]x$)|(^[0-2]\.[0-9]{1,3}x$)", self.vars_dialog_goal.get()):
				self.vars_dialog_errormsg.set("ERROR: Goal must be a rate (2x, 0.5x, 0.25x, etc) or number greater than 0 and less than 304.")
				return				
			elif self.vars_dialog_goal.get()[-1] == "x" and float(self.vars_dialog_goal.get()[:-1]) > self.dialog_max_ranks:
				self.vars_dialog_errormsg.set("ERROR: Goal rate cannot be greater than the skill's max ranks per level.")
				return				
			elif self.vars_dialog_goal.get()[-1] != "x" and	int(self.vars_dialog_goal.get()) > self.dialog_max_ranks * (2 + int(self.vars_dialog_tlevel.get()) ):
				self.vars_dialog_errormsg.set("ERROR: Goal ranks cannot be achieved within level range.")
				return					

		# Add a new skill the build skill list and update the build frame to show it.
		# This creates a new Build_List_Skill object and appends it to the global build skill list to be referenced later
		# The values the new skill is set to is determined by what was enter into the Add dialog box prior to clicking Add Skill
		if result == "Add Skill":				
			skill = globals.character.skills_list[self.vars_dialog_skill.get()]
			hide = "" 
			if self.vars_dialog_hide.get() == "1":
				hide = "x"
			self.menu_size = self.menu_size + 1
				
			globals.character.build_skills_list.insert(int(self.vars_dialog_order.get())-1, Build_List_Skill(self.ML_Frame.interior(), self.vars_dialog_skill.get(), hide, self.vars_dialog_order.get(), 
			"%s / %s (%s)" % (skill.ptp_cost,skill.mtp_cost, skill.max_ranks), self.vars_dialog_slevel.get(), self.vars_dialog_tlevel.get(), self.vars_dialog_goal.get()))						
			globals.character.build_skills_list[int(self.vars_dialog_order.get())-1].SkP_Edit_Button.config(command=lambda v=int(self.vars_dialog_order.get())-1: self.Add_Edit_Button_Onclick(v))
			globals.character.build_skills_list[int(self.vars_dialog_order.get())-1].Set_Training_Rate(skill.max_ranks)
			
			if self.menu_size-1 > 1:
				self.edit_order_menu["menu"].insert_command("end", label=self.menu_size-1, command=lambda v=self.menu_size-1: self.vars_dialog_order.set(v))				
			self.add_order_menu["menu"].insert_command("end", label=self.menu_size, command=lambda v=self.menu_size: self.vars_dialog_order.set(v))	
			
			for skill in globals.character.build_skills_list:
				skill.order.set(i+1)
				skill.SkP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				skill.SkP_Build_Row.grid(row=i, column=0)			
				i += 1			
			self.dialog_box.withdraw()	
			self.dialog_box.grab_release()	
		
		# Updates an existing build skill entry. 
		# The new information for the entry is take from the Edit verison of the Dialog box and can change every attribute for the entry
		# Once alterted, the build frame is updated with build_skill_list
		elif result == "Update Skill":
			skill = globals.character.build_skills_list.pop(self.vars_dialog_edit_location.get())
			skill.name.set(self.vars_dialog_skill.get())
			skill.info.set(self.vars_dialog_info.get())
			skill.order.set(self.vars_dialog_order.get())
			skill.slvl.set(self.vars_dialog_slevel.get())
			skill.tlvl.set(self.vars_dialog_tlevel.get())
			skill.goal.set(self.vars_dialog_goal.get())			
			
			if self.vars_dialog_hide.get() == "1":
				skill.hide.set("x")
			else:
				skill.hide.set("")			
			
			globals.character.build_skills_list.insert(int(self.vars_dialog_order.get())-1, skill)
			globals.character.build_skills_list[int(self.vars_dialog_order.get())-1].Set_Training_Rate(globals.character.skills_list[skill.name.get()].max_ranks)
			for skill in globals.character.build_skills_list:	
				skill.order.set(i+1)
				skill.SkP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				skill.SkP_Build_Row.grid(row=i, column=0)			
				i += 1						
			self.dialog_box.withdraw()	
			self.dialog_box.grab_release()			
		
		# Current selected entry in the build list is removed, the build list is updated with the correct entry order, and the build frame is updated to reflect the removal.
		elif result == "Remove Skill":
			skill = globals.character.build_skills_list.pop(self.vars_dialog_edit_location.get())
			skill.SkP_Build_Row.grid_remove()
			globals.character.skills_list[skill.name.get()].Set_To_Default()
			self.add_order_menu['menu'].delete("end", "end")
			self.edit_order_menu['menu'].delete("end", "end")
			self.menu_size -= 1
			for skill in globals.character.build_skills_list:
				skill.order.set(i+1)
				skill.SkP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				skill.SkP_Build_Row.grid(row=i, column=0)			
				i += 1	
			self.dialog_box.withdraw()	
			self.dialog_box.grab_release()

			
	# This function is called to display the popup dialog box that allows a user to add a new skill or edit an existing skill.
	# Clicking the Add Skill button in the Build Header frame will show the Add version of this box
	# Clicking an existing Skill's Edit button will show the Edit version of this box
	def Add_Edit_Button_Onclick(self, location):
		# Because the dialog box is used for both adding and editing skills, we need to remove all the menu widgets before adding add menu again
		self.add_order_menu.grid_remove()
		self.edit_order_menu.grid_remove()		
		
		if location == "":
			skill = globals.character.skills_list["Armor Use"]
			self.vars_dialog_skill.set("Armor Use")
			self.vars_dialog_order.set(self.menu_size)
			self.vars_dialog_hide.set("0")
			self.vars_dialog_goal.set("")
			self.vars_dialog_slevel.set("0")
			self.vars_dialog_tlevel.set("100")		
			
			self.add_order_menu.grid(row=3, column=1, sticky="w")	
			
			# If the last time we used the dialog box was as an edit box, change the buttons to the add version
			if self.dialog_box.component("buttonbox").button(0)["text"] == "Update Skill":
				self.dialog_box.component("buttonbox").delete("Update Skill")
				self.dialog_box.component("buttonbox").delete("Remove Skill")		
				self.dialog_box.component("buttonbox").insert("Add Skill", command=lambda v="Add Skill": self.Dialog_Box_Onclick(v))	
		else:
			build_skill = globals.character.build_skills_list[int(location)]
			skill = globals.character.skills_list[build_skill.name.get()]
			self.vars_dialog_skill.set(build_skill.name.get())
			self.vars_dialog_order.set(build_skill.order.get())
			self.vars_dialog_slevel.set(build_skill.slvl.get())
			self.vars_dialog_tlevel.set(build_skill.tlvl.get())
			self.vars_dialog_goal.set(build_skill.goal.get())		
				
			self.vars_dialog_edit_location.set(int(location))
			
			if build_skill.hide.get() == "x":
				self.vars_dialog_hide.set("1")	
			else:
				self.vars_dialog_hide.set("0")					
			
			self.edit_order_menu.grid(row=3, column=1, sticky="w")	
			
			# If the last time we used the dialog box was as an add box, change the buttons to the edit version
			if self.dialog_box.component("buttonbox").button(0)["text"] == "Add Skill":
				self.dialog_box.component("buttonbox").delete("Add Skill")
				self.dialog_box.component("buttonbox").insert("Remove Skill", command=lambda v="Remove Skill": self.Dialog_Box_Onclick(v))	
				self.dialog_box.component("buttonbox").insert("Update Skill", command=lambda v="Update Skill": self.Dialog_Box_Onclick(v))			
			
			
		self.vars_dialog_info.set("%s / %s (%s)" % (skill.ptp_cost, skill.mtp_cost, skill.max_ranks))
		self.vars_dialog_errormsg.set("")
		self.dialog_max_ranks = skill.max_ranks									
				
		self.dialog_box.show()
		self.dialog_box.grab_set()


	# When the Clear All button is clicked, the build_skills_list is emptied, all PTP/MTP totals lists are reset, the menu sizes are set to 1 and level counter set back to 0
	def ClearAll_Button_Onclick(self):			
		for key, row in globals.character.skills_list.items():
			row.Set_To_Default()
			row.SkP_schedule_row.grid_remove()
			
		for skill in globals.character.build_skills_list:	
			skill.SkP_Build_Row.grid_remove()
			
		# Fun fact, if you try to do delete(1, end)	on an option menue that only has 1 object in it, it throws a python error. So this check is needed.
		if self.menu_size > 1:
			self.add_order_menu['menu'].delete(1, "end")
			menu = [1]
			self.edit_order_menu.set_menu(1, *menu)
			self.menu_size = 1
		
		globals.character.build_skills_list = []		
		self.total_regained_ptp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_regained_mtp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_cost_ptp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_cost_mtp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_converted_ptp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_converted_mtp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_leftover_ptp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_leftover_mtp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_available_ptp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_available_mtp_by_level = [tkinter.IntVar() for i in range(101)]
		
		self.SkP_radio_var.set(1)
		self.level_counter.setvalue(0)
		self.ML_Frame.yview("moveto", 0, "units")
		self.MR_Frame.yview("moveto", 0, "units")
		self.Update_Schedule_Frames()

		
	# When the Calculate Build button is pushed the planner will map out level by level, skill by skill (in the build list) what ranks are trained at what level.
	# This method is by far the most process intense and time consuming to execute. Clicking the button does have a noticeable delay, but considering everything it does it's pretty low.
	# This method will also call on a number of different Skill object methods as well. Please review the Skill class in Globals.py for more information.
	def Plan_Training_Schedule(self):		
		abort_loops = 0; error_text = ""
		
		# Clear schedule before using it.
		for key, row in globals.character.skills_list.items():	
			row.Set_To_Default()
			row.SkP_schedule_row.grid_remove()			
					
		# We will use the adjusted rate to determine skill ranks since we need the base training rate to reset all the adjustments
		for bskill in globals.character.build_skills_list:		
			i = 0
			for r in bskill.base_training_rate:
				bskill.adjusted_training_rate[i] = r	
				i += 1		
		
		# Loop through each level. All levels need to be covered regardless of what the level range of the skills in the build list 
		for lvl in range(0, 101):	
#			if abort_loops or lvl > 20:
			if abort_loops:			
				break
			
			
			subskill_ranks_this_level = {}
			
			ptp_earned = globals.character.ptp_by_level[lvl].get()
			mtp_earned = globals.character.mtp_by_level[lvl].get()
			ptp_regained = 0
			mtp_regained = 0	
			total_ptp_available = 0
			total_mtp_available = 0
			ptp_converted_to_mtp = 0
			mtp_converted_to_ptp = 0
			ptp_converted_at_level = 0
			mtp_converted_at_level = 0	
			
			ptp_cost = 0
			mtp_cost = 0
			prev_pleftover = 0
			prev_mleftover = 0
			prev_pconverted = 0
			prev_mconverted = 0
			
			subskills_calculated = []
			ss_ptp_regain = 0
			ss_mtp_regain = 0
			
			push_back = 0	
			
			# Get the converted TP and leftover TP from the previous level
			if lvl > 0:
				prev_pleftover += self.total_leftover_ptp_by_level[lvl-1].get()	
				prev_mleftover += self.total_leftover_mtp_by_level[lvl-1].get()			
				prev_pconverted += self.total_converted_ptp_by_level[lvl-1].get()	
				prev_mconverted += self.total_converted_mtp_by_level[lvl-1].get()					
	
			#lets keep track skills we already calculated the regained value
			calculated_skills = []

			# Calculating the regained TP needs to be done for each skill at each level to get an accurate count of the TP. We need ALL the TP before we can determine if the skills cost can be meet
			for row in globals.character.build_skills_list:
				if lvl == 0:
					break
				
				#check if we already calculated this skills regain, if so move on
				if row.name.get() in calculated_skills:
					continue
				else:
					calculated_skills.append(row.name.get())

				sskill = globals.character.skills_list[row.name.get()]
					
				if sskill.subskill_group != "NONE":
					if not sskill.subskill_group in subskills_calculated:		
						(ss_ptp_regain, ss_mtp_regain) = globals.character.Calculate_Subskill_Regained_TP(lvl, sskill.subskill_group)
						ptp_regained += ss_ptp_regain
						mtp_regained += ss_mtp_regain	
						subskills_calculated.append(sskill.subskill_group)
				else:
					sskill.Calculate_TP_Regain(lvl, lvl)
#					if sskill.ptp_regained_at_level[lvl].get() > 0 or sskill.mtp_regained_at_level[lvl].get() > 0:
#						print("%s %s: %s %s" % (lvl, row.name.get(), sskill.ptp_regained_at_level[lvl].get(), sskill.mtp_regained_at_level[lvl].get()) )
					ptp_regained += sskill.ptp_regained_at_level[lvl].get()
					mtp_regained += sskill.mtp_regained_at_level[lvl].get()			

			ptp_regained -= prev_pconverted 
			mtp_regained -= prev_mconverted 
						
	
			# Calculate how many TP we have to work with.
			total_ptp_available = ptp_earned + prev_pleftover + ptp_regained
			total_mtp_available = mtp_earned + prev_mleftover + mtp_regained 				
						
			# In some cases, there isn't enough TP earned from leveling up to unconvert all the points. 
			# So only convert back enough TP to set the converted from TP to 0.			
			if total_ptp_available < 0:
				ptp_converted_at_level = total_ptp_available * -1
				mtp_converted_at_level = total_ptp_available * 2					
			elif total_mtp_available < 0:
				mtp_converted_at_level = total_mtp_available * -1
				ptp_converted_at_level = total_mtp_available * 2		
			
			
			# Go through each skill in the build list. The order of skills denotes what will be trained first. 			
			for bskill in globals.character.build_skills_list:	
				if abort_loops == 1:					
					break
				ranks_needed = 0; ranks_taken = 0
				ptp_cost_at_level = 0; mtp_cost_at_level = 0		
				
				# Skip this skill if it is hidden, falls outside the level range, has no ranks needed to be trained this level
				if bskill.hide.get() == "x" or int(bskill.slvl.get()) > lvl or int(bskill.tlvl.get()) < lvl or int(bskill.adjusted_training_rate[lvl]) == 0:
					continue									
							
				# If a skill cannot be fully trained, the remaining ranks for that and all ranks of every skill after it will be added to the ranks that need to be trained next level.
				if push_back == 1:
					bskill.adjusted_training_rate[lvl+1] = bskill.adjusted_training_rate[lvl+1] + bskill.adjusted_training_rate[lvl]
					continue	
							
				row = globals.character.skills_list[bskill.name.get()]
				ranks_taken = bskill.adjusted_training_rate[lvl]	
				
				if row.subskill_group == 'NONE':
					subskill_ranks = 0
				else:
					subskill_ranks = subskill_ranks_this_level.get(row.subskill_group,0) + globals.character.Get_Total_Ranks_Of_Subskill(bskill.name.get(), lvl-1, row.subskill_group)
					subskill_ranks_this_level[row.subskill_group] = subskill_ranks_this_level.get(row.subskill_group,0) + ranks_taken

				
								
				# Current skill would add too many ranks to the skill. This happens if a person tries to train the same skill (or subskill) more than once in a set range				
				if row.max_ranks * (2+min(lvl, 99)) < row.total_ranks_by_level[lvl].get() + bskill.adjusted_training_rate[lvl] + subskill_ranks:
					if lvl == int(bskill.tlvl.get()):
						error_text = "Level %s: Error training in %s\nRanks desired exceeds maximum profession ranks\n%s desired ranks vs. %s maximum ranks.  Aborting calculation." % (lvl, row.name, row.total_ranks_by_level[lvl].get() + bskill.adjusted_training_rate[lvl], row.max_ranks * (1+lvl))								
						abort_loops = 1
						break
						
					# If we are not at the last level, we might be able to train some of the ranks even if we can't train them all. Try to figure out how many we can afford and set that to ranks_taken
					elif row.max_ranks * (1+lvl) >= row.total_ranks_by_level[lvl].get() + 1 + subskill_ranks:
						j = ranks_taken
						for k in range(j, 0, -1):				
							if row.max_ranks * (1+lvl) >= row.total_ranks_by_level[lvl].get() + k:				
								ranks_taken = k				
								break
								#moves on to next part of the loop
					else:
						ranks_taken = 0
					
				# Determine if we can afford these new ranks. Try to use TP conversion if we need to
				j = ranks_taken
				ptp_needed = 0
				mtp_needed = 0
				for k in range(j, -1, -1):
					if k <= 0:
						ranks_taken = 0
						break
						
					cur_ptp_available = total_ptp_available - ptp_cost + ptp_converted_at_level
					cur_mtp_available = total_mtp_available - mtp_cost + mtp_converted_at_level					
						
					# Calculate the cost of the next rank.
					(ptp_cost_at_level, mtp_cost_at_level) = row.Get_Next_Ranks_Cost(lvl, subskill_ranks, k)
					
					# If we have enough PTP and MTP to train those ranks, do it and break out of the loop
					if cur_ptp_available >= ptp_cost_at_level and cur_mtp_available >= mtp_cost_at_level:
						ranks_taken = k
						break		

					
					# Otherwise, if the PTP or MTP cost is too high and the other has points left, see if we have enough to train using convertion
					# Only one type of conversion can occur per skills. 
					if cur_ptp_available < ptp_cost_at_level:
						ptp_needed = ptp_cost_at_level - cur_ptp_available
						
						# If we don't haven enough MTP, go back to the top and reduce the trains/go to the next skill
						if ptp_needed > (cur_mtp_available - mtp_cost_at_level)/2:
							continue				

						# Convert MTP to PTP
						while ptp_cost + ptp_cost_at_level > total_ptp_available + ptp_converted_at_level:
							mtp_converted_at_level -= 2		
							ptp_converted_at_level += 1		
						ranks_taken = k
						break	
						
					elif cur_mtp_available < mtp_cost_at_level:
						mtp_needed = mtp_cost_at_level - cur_mtp_available
						
						# If we don't haven enough PTP, go back to the top and reduce the trains/go to the next skill
						if mtp_needed > (cur_ptp_available - ptp_cost_at_level)/2:
							continue	
							
						# Convert PTP to MTP	
						while mtp_cost + mtp_cost_at_level > total_mtp_available + mtp_converted_at_level:
							ptp_converted_at_level -= 2		
							mtp_converted_at_level += 1	
						ranks_taken = k
						break	
				
				# Error checking
				if ranks_taken < bskill.adjusted_training_rate[lvl] and lvl >= int(bskill.tlvl.get()):
					error_text = "Failed to meet training goal %s ranks by target level %s for %s. Aborting calculation.\n\n" % (bskill.goal.get(), lvl, row.name) + error_text
					abort_loops = 1
					break
					
				
				# If we actually took some ranks, train them now
				if ranks_taken > 0:
					(ptp_cost_at_level, mtp_cost_at_level) = row.Get_Next_Ranks_Cost(lvl, subskill_ranks, ranks_taken)		
					ptp_cost += ptp_cost_at_level
					mtp_cost += mtp_cost_at_level	
					row.Train_New_Ranks(lvl, subskill_ranks, ranks_taken)
					
					
				if ranks_taken < bskill.adjusted_training_rate[lvl]:
					error_text += "Level %s: Error training in %s\nUnable to train %s ranks (trained %s ranks this level)\nRemaining training pushed back to next level.\n\n" % (lvl, row.name, bskill.adjusted_training_rate[lvl], ranks_taken)											
					bskill.adjusted_training_rate[lvl+1] = bskill.adjusted_training_rate[lvl+1] + bskill.adjusted_training_rate[lvl] - ranks_taken
					push_back = 1
				

			
			# Set the totals for this level once we completed the skill training						
			self.total_regained_ptp_by_level[lvl].set(ptp_regained)
			self.total_regained_mtp_by_level[lvl].set(mtp_regained)	
			self.total_available_ptp_by_level[lvl].set(total_ptp_available)
			self.total_available_mtp_by_level[lvl].set(total_mtp_available)		
			self.total_cost_ptp_by_level[lvl].set(ptp_cost)
			self.total_cost_mtp_by_level[lvl].set(mtp_cost)
			self.total_converted_ptp_by_level[lvl].set(ptp_converted_at_level)	
			self.total_converted_mtp_by_level[lvl].set(mtp_converted_at_level)
			self.total_leftover_ptp_by_level[lvl].set(total_ptp_available - ptp_cost + ptp_converted_at_level)
			self.total_leftover_mtp_by_level[lvl].set(total_mtp_available - mtp_cost + mtp_converted_at_level)	

		# Display an error if something didn't go right	
		if error_text != "":		
			globals.info_dialog.Show_Message(error_text)
	
#		globals.character.Update_Statistics()
		for i in range(101):
			globals.character.Update_Resources(i)
		self.Update_Schedule_Frames()
		

	# This is called when user changes the level counter or when the user's build has been recalculated.
	# It uses what ever the current level is and updates the schedule frame and schedule footer
	def Update_Schedule_Frames(self):
		if self.level_counter.getvalue() == "":
			return
			
		level = int(self.level_counter.getvalue())
		subskill_ranks_this_level = {}
		previous_subskill_ranks_this_level = {}
		i = 0	
		
		# Go through each skill in the profession knows 
		# Show skill if: Show All Skills is checked, Show All Trained is checked and the character has at least 1 rank in it, Show Trained this Level is checked and they have ranks for this level
		for key in globals.skill_names:		
			row = globals.character.skills_list[key]
					
			if row.active_skill == 1 and (self.SkP_radio_var.get() == 1 or (self.SkP_radio_var.get() == 2 and row.total_ranks_by_level[100].get() > 0) or (self.SkP_radio_var.get() == 3 and row.ranks_by_level[level].get() > 0)):
				if row.ranks_by_level[level].get() > 0:
					row.cost.set("%s / %s" % (row.ptp_cost_at_level[level].get(), row.mtp_cost_at_level[level].get()))
				else:
					row.cost.set("")			
					
				if row.total_ranks_by_level[100].get() > 0:	
					if row.subskill_group == 'NONE':
						row.sum_cost.set("%s / %s" % (row.Get_Total_Skill_Cost(0, row.total_ranks_by_level[level].get(), level)))
					else:	
						try:
							subskill_ranks = subskill_ranks_this_level[row.subskill_group]	
							base_skill_ranks = row.total_ranks_by_level[level].get() + previous_subskill_ranks_this_level[row.subskill_group]
							
							(base1, base2) = row.Get_Total_Skill_Cost(0, base_skill_ranks, level)
							(subranks1, subranks2) = row.Get_Total_Skill_Cost(subskill_ranks, row.total_ranks_by_level[level].get(), level)			
							
							previous_subskill_ranks_this_level[row.subskill_group] = subskill_ranks_this_level[row.subskill_group]
							subskill_ranks_this_level[row.subskill_group] += row.total_ranks_by_level[level].get()			
							
							row.sum_cost.set("%s / %s" % (subranks1-base1, subranks2-base2))		
						except:
							subskill_ranks = globals.character.Get_Total_Ranks_Of_Subskill(row.name, level-1, row.subskill_group)
							subskill_ranks_this_level[row.subskill_group] = row.total_ranks_by_level[level].get()
							previous_subskill_ranks_this_level[row.subskill_group] = 0
							
							row.sum_cost.set("%s / %s" % (row.Get_Total_Skill_Cost(0, row.total_ranks_by_level[level].get(), level)))				
					
				else:
					row.sum_cost.set("")		
				
				row.ranks.set(row.ranks_by_level[level].get())
				row.total_ranks.set(row.total_ranks_by_level[level].get())
				row.bonus.set(row.bonus_by_level[level].get())
				row.SkP_schedule_row.grid(row=i, column=0)
			else:
				row.SkP_schedule_row.grid_remove()
			i += 1
			
		# Set the footer values for this given level
		self.vars_sfooter_ptp_earned.set(globals.character.ptp_by_level[level].get())
		self.vars_sfooter_mtp_earned.set(globals.character.mtp_by_level[level].get())
		self.vars_sfooter_ptp_regained.set(self.total_regained_ptp_by_level[level].get())
		self.vars_sfooter_mtp_regained.set(self.total_regained_mtp_by_level[level].get())			
		self.vars_sfooter_total_ptp_available.set(self.total_available_ptp_by_level[level].get())
		self.vars_sfooter_total_mtp_available.set(self.total_available_mtp_by_level[level].get())	
		self.vars_sfooter_ptp_total_cost.set(self.total_cost_ptp_by_level[level].get())
		self.vars_sfooter_mtp_total_cost.set(self.total_cost_mtp_by_level[level].get())
		self.vars_sfooter_ptp_converted.set(self.total_converted_ptp_by_level[level].get())
		self.vars_sfooter_mtp_converted.set(self.total_converted_mtp_by_level[level].get()) 
		self.vars_sfooter_ptp_leftover.set(self.total_leftover_ptp_by_level[level].get())
		self.vars_sfooter_mtp_leftover.set(self.total_leftover_mtp_by_level[level].get())
		
		
	# When skills drop down menu in the dialog box is changed, update the skill name, skill cost, and max ranks
	def Skills_Menu_Onchange(self, name):
		skill = globals.character.skills_list[name]
		self.vars_dialog_skill.set(name)
		self.vars_dialog_info.set("%s/%s (%s)" % (skill.ptp_cost, skill.mtp_cost, skill.max_ranks))
		self.dialog_max_ranks = skill.max_ranks

	
	# This allows mouse scrolling in the build frame. Anything with the bind tag SkP_Build will allow the scrolling
	def Scroll_Build_Frame(self, event):
		self.ML_Frame.yview("scroll", -1*(event.delta/120), "units")
		
		
	# This allows mouse scrolling in the schedule frame. Anything with the bind tag SkP_Schedule will allow the scrolling	
	def Scroll_Schedule_Frame(self, event):
		self.MR_Frame.yview("scroll", -1*(event.delta/120), "units")	


	# Wrapper function used by Globals.py to create a new Skill from Character file.		
	def Create_Build_List_Skill(self, parent, name, hidden, order, info, start, target, goal):
		return Build_List_Skill(parent, name, hidden, order, info, start, target, goal)
		
		
# This class holds all the information for a specific skill the character wants to train in. These skills are shown the build frame using the object's SkP_Build_Row	frame
class Build_List_Skill:
	def __init__(self, parent, name, hidden, order, info, start, target, goal):
		self.name = tkinter.StringVar()
		self.info = tkinter.StringVar()
		self.order = tkinter.StringVar()
		self.hide = tkinter.StringVar()
		self.slvl = tkinter.StringVar()
		self.tlvl = tkinter.StringVar()
		self.goal = tkinter.StringVar()
		self.SkP_Build_Row = tkinter.Frame(parent)
		self.SkP_Edit_Button = ""
		self.base_training_rate = [0 for i in range(101)]
		self.adjusted_training_rate = [0 for i in range(101)]
								
		self.name.set(name)
		self.hide.set(hidden)
		self.order.set(order)
		self.info.set(info)
		self.slvl.set(start)
		self.tlvl.set(target)
		self.goal.set(goal)
		self.SkP_Build_Row.bindtags("SkP_build")
		
		L1 = tkinter.Label(self.SkP_Build_Row, width=3, bg="lightgray", textvariable=self.hide)
		L1.grid(row=0, column=0, padx="1", pady="1")
		L1.bindtags("SkP_build")
		L2 = tkinter.Label(self.SkP_Build_Row, width=6, bg="lightgray", textvariable=self.order)
		L2.grid(row=0, column=1, padx="1", pady="1")
		L2.bindtags("SkP_build")
		L3 = tkinter.Label(self.SkP_Build_Row, width="26", anchor="w", bg="lightgray", textvariable=self.name)
		L3.grid(row=0, column=2, padx="1", pady="1")
		L3.bindtags("SkP_build")
		L4 = tkinter.Label(self.SkP_Build_Row, width="12", bg="lightgray", textvar=self.info)
		L4.grid(row=0, column=3, padx="1", pady="1")
		L4.bindtags("SkP_build")
		L5 = tkinter.Label(self.SkP_Build_Row, width=5, bg="lightgray", textvariable=self.goal)
		L5.grid(row=0, column=4, padx="1")
		L5.bindtags("SkP_build")
		L6 = tkinter.Label(self.SkP_Build_Row, width=5, bg="lightgray", textvariable=self.slvl)
		L6.grid(row=0, column=5, padx="1")
		L6.bindtags("SkP_build")
		L7 = tkinter.Label(self.SkP_Build_Row, width=5, bg="lightgray", textvariable=self.tlvl)
		L7.grid(row=0, column=6, padx="1")
		L7.bindtags("SkP_build")
		self.SkP_Edit_Button = tkinter.Button(self.SkP_Build_Row, text="Edit", command="")
		self.SkP_Edit_Button.grid(row=0, column=7, padx="3")	

		
	# This takes either a number or rates (1x, 2x) and maps it out across the level range.
	# Numbers will be front loaded with extra ranks if the ranks cannot be spread across the level ranks.
	# Rates will set the skill ranks evenly over the level range
	def Set_Training_Rate(self, max_ranks_per_level):
		self.base_training_rate = [0 for i in range(101)]
		self.adjusted_training_rate = [0 for i in range(101)]
		start = int(self.slvl.get())
		end = int(self.tlvl.get())
		
		# Map out a Rate
		if self.goal.get()[-1] == "x":
			goal = float(self.goal.get()[:-1])
			prev_ranks = 0
			for i in range(0, 101):
				if i < start or i > end:
					continue					
				estimated_ranks = goal * (i+1-start)   # We need to factor in the start number too. If we don't it will front load a bunch of ranks on the start level
				
				mod_ranks = round(estimated_ranks % 1, 3)
				mod_goal = goal % 1
				
				# We need to round up for anything at .9 or with the rate of 1/3. .999999... ~= 1 in this case
				if ( mod_ranks == .9 or mod_ranks == .99 or mod_ranks == .999 ) and ( mod_goal == .3 or mod_goal == .33 or mod_goal == .333 ):		
					self.base_training_rate[i] = int(math.ceil(estimated_ranks) - prev_ranks)
					prev_ranks = math.ceil(estimated_ranks)		   
				else:		
					self.base_training_rate[i] = int(math.floor(estimated_ranks) - prev_ranks)
					prev_ranks = math.floor(estimated_ranks)
				
		# Map out a Number. Unlike using a rate, a set number of ranks will train as many ranks as possible and
		# as soon as possible, until the goal is met. Using a number instead of a rate effectly frontloads the 
		# skill ranks.
		else:
			goal = int(self.goal.get())
			target = end + 1
			spanning = end - start + 1
			ranks_taken = 0			
			
			if goal <= (max_ranks_per_level * (start + 2)):
				self.base_training_rate[start] = goal	
			else:								
				while goal > 0:
					for i in range(start, target):
						if i == start:
							self.base_training_rate[i] = (max_ranks_per_level * (start + 2))
							goal -= (max_ranks_per_level * (start + 2))
						elif goal < max_ranks_per_level:
							self.base_training_rate[i] += goal
							goal = 0							
						else:
							self.base_training_rate[i] += max_ranks_per_level
							goal -= max_ranks_per_level
							
						if goal <= 0:
							break

	
	# This is used to figure out a new training rate when we had to do a push back from calculating the schedule
	def Update_Adjusted_Training(self, new_start, ranks_taken):
		self.adjusted_training_rate = [0 for i in range(101)]
		goal = int(self.goal.get()) - ranks_taken
		target = int(self.tlvl.get()) + 1
		spanning = int(self.tlvl.get()) - new_start + 1
		ranks_taken = 0
		if spanning >= goal:				
			for i in range(new_start, target):	
				self.adjusted_training_rate[i] = 1
				ranks_taken += 1
				if ranks_taken >= goal:
					break
		else:
			base_ranks = math.floor(goal / spanning)
			remainder = goal % spanning 
			for i in range(new_start, target):
				if remainder > 0 and remainder > ranks_taken:
					self.adjusted_training_rate[i] = base_ranks + 1					
					ranks_taken += 1
				else:
					self.adjusted_training_rate[i] = base_ranks		
		
