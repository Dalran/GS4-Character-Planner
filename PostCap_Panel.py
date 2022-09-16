# INDEX OF CLASSES AND METHODS
'''
class PostCap_Panel: 
	def __init__(self, panel)
	def Create_Build_Header(self, panel):
	def Create_Build_Frame(self, panel):
	def Create_Schedule_Header(self, panel):
	def Create_Schedule_Footer(self, panel):
	def Create_Dialog_Box(self, panel, title, buttons):
	def Dialog_Box_Onclick(self, result):
	def Dialog_Menu_Onchange(self, name):
	def Add_Edit_Button_Onclick(self, location):
	def Clear_Button_Onclick(self, style):		
	def PostCap_Style_Onchange(self, result):	
	def Plan_Training_Schedule(self):	
	def Update_Schedule_Frames(self):	
	def Scroll_Build_Frame(self, event):	
	def Scroll_Schedule_Frame(self, event):
	def Create_Build_List_Maneuver(self, parent, name, type, hidden, order, start, target, goal, ranks_arr ):
	
class PostCap_Build_List_Skill:
	def __init__(self, parent, name, hidden, order, info, goal):
	def Calculate_Total_Cost(self):	
	def Update_Adjusted_Training(self, new_start, ranks_taken):
	def PcP_Row_Label_Onclick(self, event, val):	
	
class PostCap_Build_List_Maneuver:
	def __init__(self, parent, name, type, hidden, order, goal, ranks_arr ):	
	def Calculate_Total_Cost(self):	
	def PcP_Row_Label_Onclick(self, event, val):	
'''

#!/usr/bin/python

import tkinter
import re
import math
import Pmw
import Globals as globals
  
  
# Postcap panel is responsible for handling character skills, combat maneuver, shield maneuver, and armor maneuver training beyond level 100.
# This panel is made of 5 sub frames. 
#  Build buttons (Upper Left) - Contains buttons that add new skills or maneuvers to the build list, calculate out a build, or reset the build list. A drop down menu is used to switch between skills, combat, shield, and armor styles.
#  Build skill list (Middle/Lower Left) - Contains a list of maneuvers that user wants to train in. Changing the maneuver style (UL frame), will change what kind of maneuvers are shown here.
#  Schedule buttons (Upper Right) - These button can alter how the Schedule maneuver list looks
#  Scheduled skills list (Middle Right) - This list every maneuver available to the character along with rank cost information.
#  Scheduled footer (Lower Right) - The totals and training point costs are calculated here
class PostCap_Panel:  
	def __init__(self, panel):	
		self.PcP_radio_var = tkinter.IntVar()	
		self.goal_mode = tkinter.StringVar()
		self.current_goal_mode = "Skills"
		self.man_select_menu = ""
		self.dialog_max_ranks = 0
		
		# Dialog Box vars
		self.dialog_skill_names_menu = ""
		self.dialog_armor_names_menu = ""
		self.dialog_combat_names_menu = ""
		self.dialog_shield_names_menu = ""
		self.add_skill_order_menu = ""
		self.add_armor_order_menu = ""
		self.add_combat_order_menu = ""
		self.add_shield_order_menu = ""
		self.edit_skill_order_menu = ""
		self.edit_armor_order_menu = ""
		self.edit_combat_order_menu = ""
		self.edit_shield_order_menu = ""
		self.skills_menu_size = 1			
		self.armor_menu_size = 1			
		self.combat_menu_size = 1			
		self.shield_menu_size = 1	
		self.vars_dialog_label_skill_name = tkinter.StringVar()
		self.vars_dialog_label_skill_costs = tkinter.StringVar()
		self.vars_dialog_label_maneuver_name = tkinter.StringVar()
		self.vars_dialog_label_maneuver_costs = tkinter.StringVar()
		self.vars_dialog_label_maneuver_prerequisites = tkinter.StringVar()
		self.vars_dialog_skill = tkinter.StringVar()
		self.vars_dialog_combat_maneuver = tkinter.StringVar()
		self.vars_dialog_shield_maneuver = tkinter.StringVar()
		self.vars_dialog_armor_maneuver = tkinter.StringVar()
		self.vars_dialog_maneuver_prerequisites = tkinter.StringVar()
		self.vars_dialog_order = tkinter.StringVar()
		self.vars_dialog_info = tkinter.StringVar()
		self.vars_dialog_precap_ranks = tkinter.StringVar()
		self.vars_dialog_prerequisites = tkinter.StringVar()
		self.vars_dialog_hide = tkinter.StringVar()
		self.vars_dialog_goal = tkinter.StringVar()
		self.vars_dialog_errormsg = tkinter.StringVar()
		self.vars_dialog_edit_location = tkinter.IntVar()		
		
		# Schedule Calculations
		self.total_available_combat_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_available_shield_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_available_armor_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_cost_combat_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_cost_shield_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_cost_armor_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_leftover_combat_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_leftover_shield_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_leftover_armor_points_by_level = [tkinter.IntVar() for i in range(101)]
		
		# Schedule Footer vars
		self.sfooter_skill_title_row = ""
		self.sfooter_maneuver_title_row = ""
		self.sfooter_ptp_row = ""
		self.sfooter_mtp_row = ""
		self.sfooter_combat_row = ""
		self.sfooter_shield_row = ""
		self.sfooter_armor_row = ""
		
		self.vars_sfooter_ptp_earned = tkinter.IntVar()
		self.vars_sfooter_mtp_earned = tkinter.IntVar()
		self.vars_sfooter_ptp_available = tkinter.IntVar()
		self.vars_sfooter_mtp_available = tkinter.IntVar()
		self.vars_sfooter_ptp_total_cost = tkinter.IntVar()
		self.vars_sfooter_mtp_total_cost = tkinter.IntVar()
		self.vars_sfooter_ptp_converted = tkinter.IntVar()
		self.vars_sfooter_mtp_converted = tkinter.IntVar()
		self.vars_sfooter_ptp_leftover = tkinter.IntVar()
		self.vars_sfooter_mtp_leftover = tkinter.IntVar()	
		
		self.vars_sfooter_combat_earned = tkinter.IntVar()
		self.vars_sfooter_shield_earned = tkinter.IntVar()
		self.vars_sfooter_armor_earned = tkinter.IntVar()
		self.vars_sfooter_combat_available = tkinter.IntVar()
		self.vars_sfooter_shield_available = tkinter.IntVar()
		self.vars_sfooter_armor_available = tkinter.IntVar()
		self.vars_sfooter_combat_total_cost = tkinter.IntVar()
		self.vars_sfooter_shield_total_cost = tkinter.IntVar()
		self.vars_sfooter_armor_total_cost = tkinter.IntVar()
		self.vars_sfooter_combat_leftover = tkinter.IntVar()
		self.vars_sfooter_shield_leftover = tkinter.IntVar()	
		self.vars_sfooter_armor_leftover = tkinter.IntVar()	
			
		self.dialog_box = self.Create_Dialog_Box(panel, "Add Skill", ("Add Skill,Cancel"))	
		
		self.experience_counter = ""    									 #Becomes a Pmw.counter later on
		self.schedule_skill_header = ""
		self.schedule_maneuver_header = ""
					
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
		
		# Create the rows seen in the schedule frame for each type of style
		for skill in globals.character.skills_list:
			globals.character.skills_list[skill].Create_PcP_schedule_row(self.MR_Frame.interior())
		
		for man in globals.character.combat_maneuvers_list:
			globals.character.combat_maneuvers_list[man].Create_PcP_schedule_row(self.MR_Frame.interior())
			
		for man in globals.character.shield_maneuvers_list:
			globals.character.shield_maneuvers_list[man].Create_PcP_schedule_row(self.MR_Frame.interior())
			
		for man in globals.character.armor_maneuvers_list:
			globals.character.armor_maneuvers_list[man].Create_PcP_schedule_row(self.MR_Frame.interior())
			
		#initialize defaults
		self.ML_Frame.bind_class("PcP_build", "<MouseWheel>", self.Scroll_Build_Frame)
		self.MR_Frame.bind_class("PcP_schedule", "<MouseWheel>", self.Scroll_Schedule_Frame)
		self.dialog_box.withdraw()
		self.PcP_radio_var.set(1)
		self.goal_mode.set("Skills")
		self.experience_counter.setvalue(7572500)
				
				
	# The build header contains the the buttons to calculate or reset a build.
	# It also contains a drop down menu to change the between Skills, Combat, Shield, and Armor styles
	def Create_Build_Header(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 600, hull_height = 50)
		myframe.component("borderframe").config(borderwidth=0)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")	
		myframe_inner = myframe.interior()

		topframe = tkinter.Frame(myframe_inner)		
		topframe.grid(row=0, column=0, sticky="w")	
		choices = ["Skills", "Combat", "Shield", "Armor"]
		self.man_select_menu = tkinter.OptionMenu(topframe, self.goal_mode, *choices, command=self.PostCap_Style_Onchange)
		self.man_select_menu.config(width=6, heigh=1)	
		self.man_select_menu.grid(row=0, column=0, sticky="w")		
		tkinter.Button(topframe, height="1", text="Add", command=lambda v="": self.Add_Edit_Button_Onclick(v)).grid(row=0, column=1)		
		tkinter.Button(topframe, height="1", text="Calculate Build", command=lambda : self.Plan_Training_Schedule(self.goal_mode.get())).grid(row=0, column=2)		
		tkinter.Button(topframe, height="1", text="Calculate All", command=lambda v="All": self.Plan_Training_Schedule(v)).grid(row=0, column=3)	
		tkinter.Button(topframe, text="Clear", command=lambda v="": self.Clear_Button_Onclick(v)).grid(row=0, column=4, sticky="w", pady="1")	
		tkinter.Button(topframe, text="Clear All", command=lambda v="All": self.Clear_Button_Onclick(v)).grid(row=0, column=5, sticky="w", pady="1")	
		
		title_scrollframe = Pmw.ScrolledFrame(myframe_inner, usehullsize = 1, hull_width = 583, hull_height = 26 )	
		title_scrollframe.configure(hscrollmode = "none")		
		title_scrollframe.grid(row=3, column=0, sticky="w")		
		title_scrollframe_inner = title_scrollframe.interior()						
		
		tkinter.Frame(title_scrollframe_inner).grid(row=3, column=0, columnspan=3)	
		tkinter.Label(title_scrollframe_inner, width="3", bg="lightgray", text="Hide").grid(row=0, column=0, padx="1")
		tkinter.Label(title_scrollframe_inner, width="6", bg="lightgray", text="Order").grid(row=0, column=1, padx="1")
		tkinter.Label(title_scrollframe_inner, width="26", bg="lightgray", text="Name").grid(row=0, column=2, padx="1")
		tkinter.Label(title_scrollframe_inner, width="5", bg="lightgray", text="Goal").grid(row=0, column=3, padx="1")
		tkinter.Label(title_scrollframe_inner, width="10", bg="lightgray", text="Total Cost").grid(row=0, column=4, padx="1")
		tkinter.Label(title_scrollframe_inner, width="10", bg="lightgray", text="Needed EXP").grid(row=0, column=5, padx="1")
		tkinter.Label(title_scrollframe_inner, width="10", bg="lightgray", text="Ending EXP").grid(row=0, column=6, padx="1")
		tkinter.Label(title_scrollframe_inner, width="4", bg="lightgray", text="Edit").grid(row=0, column=7, padx="1")
		
		return myframe
		
		
	# All Build Skills/Maneuver objects are displayed in this panel. This panel is populated using the Dialog box Add and Update functions.
	# Only one style of objects (skills, combat, shield, armor) is shown in this panel at a time. The style can be changed with the drop down menu in the Build Header panel.
	def Create_Build_Frame(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 600, hull_height = 474)			
		myframe.configure(hscrollmode = "none", vscrollmode = "static")					
		
		return myframe			
	
	
	# This frame contains:
	#  PMW counter object that is used to change what experience interval the schedule frame is displaying
	#  The counter increases and decreases by 2500 but can never go below 7572500
	#  3 radio buttons that change what skills/maneuvers will appear in the schedule frame
	#  A title header for the schedule frame which allows that frame scroll independently of the header
	def Create_Schedule_Header(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 470, hull_height = 50)
		myframe.component("borderframe").config(borderwidth=0)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")			
		myframe_inner = myframe.interior()		
						
		topframe = tkinter.Frame(myframe_inner)	
		topframe.grid(row=0, column=0, sticky="w")	
		tlvl_frame = tkinter.Frame(topframe)
		tlvl_frame.grid(row=0, column=0, sticky="w", padx=3, pady="1")	
		self.experience_counter = Pmw.Counter(tlvl_frame, entryfield_entry_width = 9, entryfield_validate = { 'validator':'numeric', 'min':'7572500', 'minstrict': 0 }, labelpos = 'w', label_text = 'Experience', entryfield_value = 7572500, increment = 2500, datatype = "numeric", entryfield_modifiedcommand=self.Update_Schedule_Frames ) 
		self.experience_counter.grid(row=0, column=0, sticky="w", pady="1")
		
		tkinter.Radiobutton(topframe, anchor="w", text="All", command=self.Update_Schedule_Frames, var=self.PcP_radio_var, value=1).grid(row=0, column=1)	
		tkinter.Radiobutton(topframe, anchor="w", text="All Trained", command=self.Update_Schedule_Frames, var=self.PcP_radio_var, value=2).grid(row=0, column=2)		
		tkinter.Radiobutton(topframe, anchor="w", text="Trained this Interval", command=self.Update_Schedule_Frames, var=self.PcP_radio_var, value=3).grid(row=0, column=3)
		
		self.schedule_skill_header = Pmw.ScrolledFrame(myframe_inner, usehullsize = 1, hull_width = 450, hull_height = 28 )		
		self.schedule_skill_header.configure(hscrollmode = "none")		
		self.schedule_skill_header.grid(row=3, column=0, sticky="w")	
		self.schedule_skill_header_inner = self.schedule_skill_header.interior()							
		
		tkinter.Frame(self.schedule_skill_header_inner).grid(row=1, column=2, sticky="w", pady="1")	
		tkinter.Label(self.schedule_skill_header_inner, width="25", bg="lightgray", text="Skill Name").grid(row=0, column=0, padx="1")
		tkinter.Label(self.schedule_skill_header_inner, width="4", bg="lightgray", text="Ranks").grid(row=0, column=1, padx="1")
		tkinter.Label(self.schedule_skill_header_inner, width="7", bg="lightgray", text="Cost").grid(row=0, column=2, padx="1")
		tkinter.Label(self.schedule_skill_header_inner, width="8", bg="lightgray", text="Total Ranks").grid(row=0, column=3, padx="1")
		tkinter.Label(self.schedule_skill_header_inner, width="4", bg="lightgray", text="Bonus").grid(row=0, column=4, padx="1")
		tkinter.Label(self.schedule_skill_header_inner, width="9", bg="lightgray", text="Sum Cost").grid(row=0, column=5, padx="1")		
		
		self.schedule_maneuver_header = Pmw.ScrolledFrame(myframe_inner, usehullsize = 1, hull_width = 450, hull_height = 28 )		
		self.schedule_maneuver_header.configure(hscrollmode = "none")	
		self.schedule_maneuver_header_inner = self.schedule_maneuver_header.interior()							
		
		tkinter.Frame(self.schedule_maneuver_header_inner).grid(row=1, column=2, sticky="w", pady="1")	
		tkinter.Label(self.schedule_maneuver_header_inner, width="26", bg="lightgray", text="Maneuver Name").grid(row=0, column=0, padx="1")
		tkinter.Label(self.schedule_maneuver_header_inner, width="8", bg="lightgray", text="Ranks").grid(row=0, column=1, padx="1")
		tkinter.Label(self.schedule_maneuver_header_inner, width="6", bg="lightgray", text="Cost").grid(row=0, column=2, padx="1")
		tkinter.Label(self.schedule_maneuver_header_inner, width="10", bg="lightgray", text="Total Ranks").grid(row=0, column=3, padx="1")
		tkinter.Label(self.schedule_maneuver_header_inner, width="8", bg="lightgray", text="Sum Cost").grid(row=0, column=4, padx="1")
		
		return myframe		
		
		
	# This frame will hold PcP_schedule_row objects for skills/maneuvers the character can train in. For more information, please see the Skills class and Maneuver class in Globals.py
	# Only one style of objects (skills, combat, shield, armor) is shown in this panel at a time. The style can be changed with the drop down menu in the Build Header panel.
	def Create_Schedule_Frame(self, panel):
		self.training_middle_scrollframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 470, hull_height = 372)		
		self.training_middle_scrollframe_inner = self.training_middle_scrollframe.interior()
		self.training_middle_scrollframe.configure(hscrollmode = "none")		
	
		return self.training_middle_scrollframe		
	

	# This frame contains information about skill, combat, shield, and armor training points for each level for the current level. 
	# What is seen is this frame depends on the current style of the panel. 
	# In Skills style this panel, the frame contains information about PTP and MTP for the current experience interval. This information is divided into columns and they are:
	#  Earned - At 7572500, this how many TP were leftover from level 100, beyond that this value is 1.
	#  Available - Earned PTP/MTP + the leftover PTP/MTP from the previous experience interval
	#  Total Cost - Sum of all PTP/MTP costs from skills trained this experience interval
	#  Conversions - How many of one TP were converted to the other TP type
	#  Leftover - Available PTP/MTP - Total Cost - Converted 	
	# Every profession will see the Combat maneuvers row but only Rogues, Warriors, and Paladins will see the Shield and Armor rows.
	# Every maneuver row contains:
	#  Earned - How many training points where gained this interval for training in the appropriate skill. "Armor Use", "Combat Maneuvers", "Shield Use"
	#  Available - Earned training points + Leftover training points.
	#  Total Cost - Sum of all training costs from maneuvers trained this level.
	#  Leftover - Available training points - Total Cost.
	def Create_Schedule_Footer(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 470, hull_height = 100)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")			
		myframe_inner = myframe.interior()									
		
		self.sfooter_skill_title_row = tkinter.Frame(myframe_inner)
		self.sfooter_ptp_row = tkinter.Frame(myframe_inner)
		self.sfooter_mtp_row = tkinter.Frame(myframe_inner)
		
		self.sfooter_maneuver_title_row = tkinter.Frame(myframe_inner)
		self.sfooter_combat_row = tkinter.Frame(myframe_inner)	
		self.sfooter_shield_row = tkinter.Frame(myframe_inner)	
		self.sfooter_armor_row = tkinter.Frame(myframe_inner)	
		
		self.sfooter_skill_title_row.grid(row=0, column=0, padx="1")	
		self.sfooter_ptp_row.grid(row=1, column=0, padx="1")		
		self.sfooter_mtp_row.grid(row=2, column=0, padx="1")				

		tkinter.Label(self.sfooter_skill_title_row, width=5, text="").grid(row=0, column=0, sticky="w", padx="1", pady="1")	
		tkinter.Label(self.sfooter_skill_title_row, width="10", bg="lightgray", text="Earned").grid(row=0, column=1, padx="1")
		tkinter.Label(self.sfooter_skill_title_row, width="10", bg="lightgray", text="Available").grid(row=0, column=2, padx="1")
		tkinter.Label(self.sfooter_skill_title_row, width="10", bg="lightgray", text="Total Cost").grid(row=0, column=4, padx="1")
		tkinter.Label(self.sfooter_skill_title_row, width="10", bg="lightgray", text="Conversions").grid(row=0, column=5, padx="1")
		tkinter.Label(self.sfooter_skill_title_row, width="10", bg="lightgray", text="Leftover").grid(row=0, column=6, padx="1")

		tkinter.Label(self.sfooter_ptp_row, width="5", bg="lightgray", text="PTP").grid(row=1, column=0, padx="2", pady="1")
		tkinter.Label(self.sfooter_ptp_row, width="10", bg="lightgray", textvar=self.vars_sfooter_ptp_earned).grid(row=1, column=1, padx="1")
		tkinter.Label(self.sfooter_ptp_row, width="10", bg="lightgray", textvar=self.vars_sfooter_ptp_available).grid(row=1, column=2, padx="1")
		tkinter.Label(self.sfooter_ptp_row, width="10", bg="lightgray", textvar=self.vars_sfooter_ptp_total_cost).grid(row=1, column=4, padx="1")	
		tkinter.Label(self.sfooter_ptp_row, width="10", bg="lightgray", textvar=self.vars_sfooter_ptp_converted).grid(row=1, column=5, padx="1")	
		tkinter.Label(self.sfooter_ptp_row, width="10", bg="lightgray", textvar=self.vars_sfooter_ptp_leftover).grid(row=1, column=6, padx="1")		
		
		tkinter.Label(self.sfooter_mtp_row, width="5", bg="lightgray", text="MTP").grid(row=2, column=0, padx="2", pady="1")			
		tkinter.Label(self.sfooter_mtp_row, width="10", bg="lightgray", textvar=self.vars_sfooter_mtp_earned).grid(row=2, column=1, padx="1")	
		tkinter.Label(self.sfooter_mtp_row, width="10", bg="lightgray", textvar=self.vars_sfooter_mtp_available).grid(row=2, column=2, padx="1")	
		tkinter.Label(self.sfooter_mtp_row, width="10", bg="lightgray", textvar=self.vars_sfooter_mtp_total_cost).grid(row=2, column=4, padx="1")	
		tkinter.Label(self.sfooter_mtp_row, width="10", bg="lightgray", textvar=self.vars_sfooter_mtp_converted).grid(row=2, column=5, padx="1")
		tkinter.Label(self.sfooter_mtp_row, width="10", bg="lightgray", textvar=self.vars_sfooter_mtp_leftover).grid(row=2, column=6, padx="1")	
		
		
		tkinter.Label(self.sfooter_maneuver_title_row, width=8, text="").grid(row=0, column=0, sticky="w", padx="1", pady="1")	
		tkinter.Label(self.sfooter_maneuver_title_row, width="10", bg="lightgray", text="Earned").grid(row=0, column=1, padx="1")
		tkinter.Label(self.sfooter_maneuver_title_row, width="10", bg="lightgray", text="Available").grid(row=0, column=2, padx="1")
		tkinter.Label(self.sfooter_maneuver_title_row, width="10", bg="lightgray", text="Total Cost").grid(row=0, column=4, padx="1")
		tkinter.Label(self.sfooter_maneuver_title_row, width="10", bg="lightgray", text="Leftover").grid(row=0, column=5, padx="1")
	
		tkinter.Label(self.sfooter_combat_row, width="8", bg="lightgray", text="Combat").grid(row=1, column=0, padx="2", pady="1")
		tkinter.Label(self.sfooter_combat_row, width="10", bg="lightgray", textvar=self.vars_sfooter_combat_earned).grid(row=1, column=1, padx="1")
		tkinter.Label(self.sfooter_combat_row, width="10", bg="lightgray", textvar=self.vars_sfooter_combat_available).grid(row=1, column=2, padx="1")
		tkinter.Label(self.sfooter_combat_row, width="10", bg="lightgray", textvar=self.vars_sfooter_combat_total_cost).grid(row=1, column=4, padx="1")
		tkinter.Label(self.sfooter_combat_row, width="10", bg="lightgray", textvar=self.vars_sfooter_combat_leftover).grid(row=1, column=5, padx="1")
		
		tkinter.Label(self.sfooter_shield_row, width="8", bg="lightgray", text="Shield").grid(row=2, column=0, padx="2", pady="1")	
		tkinter.Label(self.sfooter_shield_row, width="10", bg="lightgray", textvar=self.vars_sfooter_shield_earned).grid(row=2, column=1, padx="1")	
		tkinter.Label(self.sfooter_shield_row, width="10", bg="lightgray", textvar=self.vars_sfooter_shield_available).grid(row=2, column=2, padx="1")	
		tkinter.Label(self.sfooter_shield_row, width="10", bg="lightgray", textvar=self.vars_sfooter_shield_total_cost).grid(row=2, column=4, padx="1")		
		tkinter.Label(self.sfooter_shield_row, width="10", bg="lightgray", textvar=self.vars_sfooter_shield_leftover).grid(row=2, column=5, padx="1")	
		
		tkinter.Label(self.sfooter_armor_row, width="8", bg="lightgray", text="Armor").grid(row=3, column=0, padx="2", pady="1")		
		tkinter.Label(self.sfooter_armor_row, width="10", bg="lightgray", textvar=self.vars_sfooter_armor_earned).grid(row=3, column=1, padx="1")		
		tkinter.Label(self.sfooter_armor_row, width="10", bg="lightgray", textvar=self.vars_sfooter_armor_available).grid(row=3, column=2, padx="1")	
		tkinter.Label(self.sfooter_armor_row, width="10", bg="lightgray", textvar=self.vars_sfooter_armor_total_cost).grid(row=3, column=4, padx="1")
		tkinter.Label(self.sfooter_armor_row, width="10", bg="lightgray", textvar=self.vars_sfooter_armor_leftover).grid(row=3, column=5, padx="1")	
					
		return myframe	
	
	
	# The popup dialog box is used to allow add a skill/maneuver or edit an existing skill/maneuver in the build frame. The type of skill/maneuver that will be added is determined by the drop down menu in the Build Header frame.
	# This frame consists of the following parts when the Skills style is set:
	# Skill Name - Drop down menu to select which skill to train in.
	# Cost and Ranks - How many PTP and MTP it costs to train a single rank in the skill and the maximum ranks you can train in the skill for a single level.
	# Training Order - Determines what order the planner will try to train the skill. If the skill cannot be fully trained at a level, ALL training below it is pushed back to the next level.
	# Hide - Any skill with a checked Hide box will be ignored when build schedule is calculated.
	# Goal - This is either a number greater that 0 for how many ranks to train in the skill or a rate (1x, 1.125x, 2.75x, etc) for how many ranks to train each level.
	# Level Range - Indicates a range for 0 to 100. This is how much time you will give the planner to train to your Goal or how many level you want to train your Goal rate
	#
	# This frame consists of the following parts when a maneuver style is set:
	# Maneuver Name - Drop down menu to select which skill to train in.
	# Cost per Rank - How many training points it costs for each rank of the maneuver and the maximum ranks you can train in the skill for a single level.
	# Prerequisites - What maneuvers/skills ranks/Guild skills, this maneuver requires beyond any ranks can be taken.
	# Training Order - Determines what order the planner will try to train the maneuver. If the maneuver cannot be fully trained at a level, ALL training below it is pushed back to the next level.
	# Hide - Any maneuver with a checked Hide box will be ignored when build schedule is calculated.
	# Goal - This is a number greater that 0 for how many ranks to train in the maneuver.
	# Level Range - Indicates a range for 0 to 100. This is how much time you will give the planner to train to your Goal or how many level you want to train your Goal rate
	def Create_Dialog_Box(self, panel, title, buttons):
		dialog = Pmw.Dialog(panel,
            buttons = (buttons.split(",")),
            title = title,
            command = self.Dialog_Box_Onclick)
			
		dialog.transient(panel)	
		dialog.resizable(width=0, height=0)		
		dialog.geometry('315x330+600+300')
				
		myframe = Pmw.ScrolledFrame(dialog.interior(), usehullsize = 1, hull_width = 315, hull_height = 330)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")		
		myframe.grid(row=0, column=0, sticky="nw")	
		myframe_inner = myframe.interior()	
				
		self.vars_dialog_label_skill_name = tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Skill Name")
		self.vars_dialog_label_skill_costs = tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Cost & Ranks")
		self.vars_dialog_label_maneuver_name = tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Maneuver Name")
		self.vars_dialog_label_maneuver_costs = tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Cost per Rank")
		self.vars_dialog_maneuver_prerequisites = tkinter.Label(myframe_inner, width="30", anchor="w", justify="left", textvar=self.vars_dialog_prerequisites)
		self.vars_dialog_label_maneuver_prerequisites = tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Prerequisites")
		
		self.vars_dialog_label_skill_name.grid(row=0, column=0, sticky="w")
		self.vars_dialog_label_skill_costs.grid(row=1, column=0, sticky="w")				
		self.vars_dialog_label_maneuver_name.grid(row=0, column=0, sticky="w")
		self.vars_dialog_label_maneuver_costs.grid(row=1, column=0, sticky="w")
		self.vars_dialog_label_maneuver_prerequisites.grid(row=2, column=0, sticky="w")
		self.vars_dialog_maneuver_prerequisites.grid(row=2, column=1, sticky="w")

		tkinter.Label(myframe_inner, width="30", anchor="w", textvar=self.vars_dialog_info).grid(row=1, column=1, sticky="w")
		
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Precap Ranks").grid(row=3, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="30", anchor="w", textvar=self.vars_dialog_precap_ranks).grid(row=3, column=1, sticky="w")

		tkinter.Label(myframe_inner, width="13", anchor="w", text="").grid(row=4, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Training Order").grid(row=5, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Hide").grid(row=6, column=0, sticky="w")
		tkinter.Checkbutton(myframe_inner, command="", variable=self.vars_dialog_hide).grid(row=6, column=1, sticky="w")	
		tkinter.Label(myframe_inner, width="13", anchor="w", text="").grid(row=7, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Goal").grid(row=8, column=0, sticky="w", pady=1)		
									
	
		self.dialog_skill_names_menu = tkinter.OptionMenu(myframe_inner, self.vars_dialog_skill, "1", command="")
		self.dialog_skill_names_menu.config(width=27)	
		self.add_skill_order_menu = tkinter.ttk.OptionMenu(myframe_inner, self.vars_dialog_order, "1", command="")
		self.add_skill_order_menu.config(width=2)	
		self.edit_skill_order_menu = tkinter.ttk.OptionMenu(myframe_inner, self.vars_dialog_order, "1", command="")
		self.edit_skill_order_menu.config(width=2)	
		
		self.dialog_combat_names_menu = tkinter.OptionMenu(myframe_inner, self.vars_dialog_combat_maneuver, "", command="")
		self.dialog_combat_names_menu.config(width=27)	
		self.add_combat_order_menu = tkinter.ttk.OptionMenu(myframe_inner, self.vars_dialog_order, "1", command="")
		self.add_combat_order_menu.config(width=2)	
		self.edit_combat_order_menu = tkinter.ttk.OptionMenu(myframe_inner, self.vars_dialog_order, "1", command="")
		self.edit_combat_order_menu.config(width=2)	
		
		self.dialog_shield_names_menu = tkinter.OptionMenu(myframe_inner, self.vars_dialog_shield_maneuver, "", command="")
		self.dialog_shield_names_menu.config(width=27)	
		self.add_shield_order_menu = tkinter.ttk.OptionMenu(myframe_inner, self.vars_dialog_order, "1", command="")
		self.add_shield_order_menu.config(width=2)	
		self.edit_shield_order_menu = tkinter.ttk.OptionMenu(myframe_inner, self.vars_dialog_order, "1", command="")
		self.edit_shield_order_menu.config(width=2)	
		
		self.dialog_armor_names_menu = tkinter.OptionMenu(myframe_inner, self.vars_dialog_armor_maneuver, "", command="")
		self.dialog_armor_names_menu.config(width=27)	
		self.add_armor_order_menu = tkinter.ttk.OptionMenu(myframe_inner, self.vars_dialog_order, "1", command="")
		self.add_armor_order_menu.config(width=2)	
		self.edit_armor_order_menu = tkinter.ttk.OptionMenu(myframe_inner, self.vars_dialog_order, "1", command="")
		self.edit_armor_order_menu.config(width=2)
		
		
		self.add_skill_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.edit_skill_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.add_combat_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.edit_combat_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.add_shield_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.edit_shield_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.add_armor_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.edit_armor_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))	
			

		self.add_skill_order_menu.grid(row=5, column=1, sticky="w")
		self.dialog_skill_names_menu.grid(row=0, column=1, sticky="w", columnspan=4)			

		goal_box = tkinter.Entry(myframe_inner, width="6", justify="center", validate="key", validatecommand="", textvariable=self.vars_dialog_goal).grid(row=8, column=1, sticky="w", padx=2)				
		tkinter.Label(myframe_inner, anchor="w", font="-weight bold", wraplength=300, justify="left", textvariable=self.vars_dialog_errormsg).grid(row=9, column=0, sticky="w", columnspan=4)
			
		return dialog

		
	# This handles button all the button events that occur in the Add/Edit dialog box.	
	def Dialog_Box_Onclick(self, result):
		i = 0
		slevel = 0
		tlevel = 100		

		goal = self.vars_dialog_goal.get()

		if result is None or result == "Cancel":
			self.dialog_box.withdraw()
			self.dialog_box.grab_release()
			return

		# The maneuver used is determined by current maneuver mode (style)
		if self.goal_mode.get() == "Combat":
			man = globals.character.combat_maneuvers_list[self.vars_dialog_combat_maneuver.get()]
		elif self.goal_mode.get() == "Shield":
			man = globals.character.shield_maneuvers_list[self.vars_dialog_shield_maneuver.get()]
		elif self.goal_mode.get() == "Armor":
			man = globals.character.armor_maneuvers_list[self.vars_dialog_armor_maneuver.get()]

	
		if result == "Add Skill" or result == "Update Skill":
			skill = globals.character.skills_list[self.vars_dialog_skill.get()]		
			subskill_ranks = globals.character.Get_Total_Ranks_Of_Subskill(skill.name, 100, skill.subskill_group)
			
			if len(self.vars_dialog_goal.get()) == 0 or self.vars_dialog_goal.get() == "0" or not re.search(r"^[1-3]?\d{1,2}$", self.vars_dialog_goal.get()):
				self.vars_dialog_errormsg.set("ERROR: Goal must be a number greater than 0 and less than 304.")
				return				
			elif int(self.vars_dialog_goal.get()) + int(self.vars_dialog_precap_ranks.get().split(" ")[0]) + subskill_ranks > self.dialog_max_ranks * 101:
				self.vars_dialog_errormsg.set("ERROR: Goal + precap ranks cannot be greater than the skill's max ranks * 101.")
				return		
	
	
		# Error checking for Add/Update Maneuver choices
		if result == "Add Maneuver" or result == "Update Maneuver":	
			if len(goal) == 0 or goal == "0" or not re.search(r"(^[1-5]$)", goal):
				self.vars_dialog_errormsg.set("ERROR: Goal must be greater than 0 and less than 5.")
				return				
			elif int(goal) + int(self.vars_dialog_precap_ranks.get().split(" ")[0]) > man.max_ranks:
				self.vars_dialog_errormsg.set("ERROR: Goal + precap ranks cannot be greater than max maneuver ranks.")
				return				
			elif man.Get_Total_Cost_At_Rank(0, int(goal)) > 101 and man.type == "combat":
				self.vars_dialog_errormsg.set("ERROR: Combat Manevuer total cost cannot be greater than 101.")
				return					

				
		if result == "Add Skill":				
			skill = globals.character.skills_list[self.vars_dialog_skill.get()]
			hide = "" 
			if self.vars_dialog_hide.get() == "1":
				hide = "x"
			self.skills_menu_size = self.skills_menu_size + 1
				
			globals.character.postcap_build_skills_list.insert(int(self.vars_dialog_order.get())-1, PostCap_Build_List_Skill(self.ML_Frame.interior(), self.vars_dialog_skill.get(), hide, self.vars_dialog_order.get(), 
			"%s / %s (%s)" % (skill.ptp_cost,skill.mtp_cost, skill.max_ranks), self.vars_dialog_goal.get()))						
			globals.character.postcap_build_skills_list[int(self.vars_dialog_order.get())-1].PcP_Edit_Button.config(command=lambda v=int(self.vars_dialog_order.get())-1: self.Add_Edit_Button_Onclick(v))
			globals.character.postcap_build_skills_list[int(self.vars_dialog_order.get())-1].Calculate_Total_Cost()
			
			if self.skills_menu_size-1 > 1:
				self.edit_skill_order_menu["menu"].insert_command("end", label=self.skills_menu_size-1, command=lambda v=self.skills_menu_size-1: self.vars_dialog_order.set(v))
			self.add_skill_order_menu["menu"].insert_command("end", label=self.skills_menu_size, command=lambda v=self.skills_menu_size: self.vars_dialog_order.set(v))	
			
			for skill in globals.character.postcap_build_skills_list:
				skill.order.set(i+1)
				skill.PcP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				skill.PcP_Build_Row.grid(row=i, column=0)		
#				skill.Calculate_Total_Cost()
				i += 1			
			self.dialog_box.withdraw()	
			self.dialog_box.grab_release()	
			
		# Updates an existing build skill entry. 
		# The new information for the entry is take from the Edit verison of the Dialog box and can change every attribute for the entry
		# Once alterted, the build frame is updated with build_skill_list
		elif result == "Update Skill":
			skill = globals.character.postcap_build_skills_list.pop(self.vars_dialog_edit_location.get())
			skill.name.set(self.vars_dialog_skill.get())
			skill.info.set(self.vars_dialog_info.get())
			skill.goal.set(self.vars_dialog_goal.get())			
			
			if self.vars_dialog_hide.get() == "1":
				skill.hide.set("x")
			else:
				skill.hide.set("")			
			
			globals.character.postcap_build_skills_list.insert(int(self.vars_dialog_order.get())-1, skill)
			for skill in globals.character.postcap_build_skills_list:	
				skill.order.set(i+1)
				skill.PcP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				skill.PcP_Build_Row.grid(row=i, column=0)		
				skill.Calculate_Total_Cost()		
				i += 1						
			self.dialog_box.withdraw()	
			self.dialog_box.grab_release()			
		
		# Current selected entry in the build list is removed, the build list is updated with the correct entry order, and the build frame is updated to reflect the removal.
		elif result == "Remove Skill":
			skill = globals.character.postcap_build_skills_list.pop(self.vars_dialog_edit_location.get())
			skill.PcP_Build_Row.grid_remove()
			globals.character.skills_list[skill.name.get()].Set_To_Default()
			self.add_skill_order_menu['menu'].delete("end", "end")
			self.edit_skill_order_menu['menu'].delete("end", "end")
			self.skills_menu_size -= 1
			for skill in globals.character.postcap_build_skills_list:
				skill.order.set(i+1)
				skill.PcP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				skill.PcP_Build_Row.grid(row=i, column=0)	
				skill.Calculate_Total_Cost()				
				i += 1	
			self.dialog_box.withdraw()	
			self.dialog_box.grab_release()
						
		# Add a new maneuver to the appropriate build list		
		elif result == "Add Maneuver":	
			hide = "" 
			if self.vars_dialog_hide.get() == "1":
				hide = "x"				
				
			if self.goal_mode.get() == "Combat":
				man = globals.character.combat_maneuvers_list[self.vars_dialog_combat_maneuver.get()]
				self.combat_menu_size += 1			
				
				globals.character.postcap_build_combat_maneuvers_list.insert(int(self.vars_dialog_order.get())-1, PostCap_Build_List_Maneuver(self.ML_Frame.interior(), self.vars_dialog_combat_maneuver.get(), 
				"Combat", hide, self.vars_dialog_order.get(), self.vars_dialog_goal.get(), (man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ))	
				
				globals.character.postcap_build_combat_maneuvers_list[int(self.vars_dialog_order.get())-1].PcP_Edit_Button.config(command=lambda v=int(self.vars_dialog_order.get())-1: self.Add_Edit_Button_Onclick(v))
			
				self.add_combat_order_menu["menu"].insert_command("end", label=self.combat_menu_size, command=lambda v=self.combat_menu_size: self.vars_dialog_order.set(v))	
				if self.combat_menu_size-1 > 1:
					self.edit_combat_order_menu["menu"].insert_command("end", label=self.combat_menu_size-1, command=lambda v=self.combat_menu_size-1: self.vars_dialog_order.set(v))				
			
				for man in globals.character.postcap_build_combat_maneuvers_list:
					man.order.set(i+1)
					man.PcP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
					man.PcP_Build_Row.grid(row=i, column=0)			
					i += 1	
				
			elif self.goal_mode.get() == "Shield":
				man = globals.character.shield_maneuvers_list[self.vars_dialog_shield_maneuver.get()]
				self.shield_menu_size = self.shield_menu_size + 1				
				
				globals.character.postcap_build_shield_maneuvers_list.insert(int(self.vars_dialog_order.get())-1, PostCap_Build_List_Maneuver(self.ML_Frame.interior(), self.vars_dialog_shield_maneuver.get(), 
				"Shield", hide, self.vars_dialog_order.get(), self.vars_dialog_goal.get(), (man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ))
				
				globals.character.postcap_build_shield_maneuvers_list[int(self.vars_dialog_order.get())-1].PcP_Edit_Button.config(command=lambda v=int(self.vars_dialog_order.get())-1: self.Add_Edit_Button_Onclick(v))
			
				self.add_shield_order_menu["menu"].insert_command("end", label=self.shield_menu_size, command=lambda v=self.shield_menu_size: self.vars_dialog_order.set(v))	
				if self.shield_menu_size-1 > 1:
					self.edit_shield_order_menu["menu"].insert_command("end", label=self.shield_menu_size-1, command=lambda v=self.shield_menu_size-1: self.vars_dialog_order.set(v))				
			
				for man in globals.character.postcap_build_shield_maneuvers_list:
					man.order.set(i+1)
					man.PcP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
					man.PcP_Build_Row.grid(row=i, column=0)			
					i += 1	
					
			elif self.goal_mode.get() == "Armor":
				man = globals.character.armor_maneuvers_list[self.vars_dialog_armor_maneuver.get()]
				self.armor_menu_size = self.armor_menu_size + 1			
				
				globals.character.postcap_build_armor_maneuvers_list.insert(int(self.vars_dialog_order.get())-1, PostCap_Build_List_Maneuver(self.ML_Frame.interior(), self.vars_dialog_armor_maneuver.get(), 
				"Armor", hide, self.vars_dialog_order.get(), self.vars_dialog_goal.get(), (man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ))	
				
				globals.character.postcap_build_armor_maneuvers_list[int(self.vars_dialog_order.get())-1].PcP_Edit_Button.config(command=lambda v=int(self.vars_dialog_order.get())-1: self.Add_Edit_Button_Onclick(v))
			
				self.add_armor_order_menu["menu"].insert_command("end", label=self.armor_menu_size, command=lambda v=self.armor_menu_size: self.vars_dialog_order.set(v))	
				if self.armor_menu_size-1 > 1:
					self.edit_armor_order_menu["menu"].insert_command("end", label=self.armor_menu_size-1, command=lambda v=self.armor_menu_size-1: self.vars_dialog_order.set(v))				
			
				for man in globals.character.postcap_build_armor_maneuvers_list:
					man.order.set(i+1)
					man.PcP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
					man.PcP_Build_Row.grid(row=i, column=0)			
					i += 1		

			self.dialog_box.withdraw()	
			self.dialog_box.grab_release()	
		
		# Change the information for an existing maneuver
		elif result == "Update Maneuver":
			if self.goal_mode.get() == "Combat":
				man = globals.character.postcap_build_combat_maneuvers_list.pop(self.vars_dialog_edit_location.get())
				list = globals.character.postcap_build_combat_maneuvers_list
				man.name.set(self.vars_dialog_combat_maneuver.get())
				m_ranks = globals.character.combat_maneuvers_list[self.vars_dialog_combat_maneuver.get()]
			elif self.goal_mode.get() == "Shield":
				man = globals.character.postcap_build_shield_maneuvers_list.pop(self.vars_dialog_edit_location.get())
				list = globals.character.postcap_build_shield_maneuvers_list
				man.name.set(self.vars_dialog_shield_maneuver.get())
				m_ranks = globals.character.shield_maneuvers_list[self.vars_dialog_shield_maneuver.get()]
			elif self.goal_mode.get() == "Armor":
				man = globals.character.postcap_build_armor_maneuvers_list.pop(self.vars_dialog_edit_location.get())
				list = globals.character.postcap_build_armor_maneuvers_list
				man.name.set(self.vars_dialog_armor_maneuver.get())		
				m_ranks = globals.character.armor_maneuvers_list[self.vars_dialog_armor_maneuver.get()]


			man.ranks[0].set(m_ranks.cost_by_rank[0])	
			man.ranks[1].set(m_ranks.cost_by_rank[1])	
			man.ranks[2].set(m_ranks.cost_by_rank[2])	
			man.ranks[3].set(m_ranks.cost_by_rank[3])	
			man.ranks[4].set(m_ranks.cost_by_rank[4])	
			man.order.set(self.vars_dialog_order.get())
			man.goal.set(self.vars_dialog_goal.get())			
			
			if self.vars_dialog_hide.get() == "1":
				man.hide.set("x")
			else:
				man.hide.set("")			
			
			list.insert(int(self.vars_dialog_order.get())-1, man)
			for man in list:	
				man.order.set(i+1)
				man.PcP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				man.PcP_Build_Row.grid(row=i, column=0)		
				man.Calculate_Total_Cost()				
				i += 1						
			self.dialog_box.withdraw()	
			self.dialog_box.grab_release()			
		
		elif result == "Remove Maneuver":
			if self.goal_mode.get() == "Combat":
				list = globals.character.postcap_build_combat_maneuvers_list
				self.add_combat_order_menu['menu'].delete("end", "end")
				self.edit_combat_order_menu['menu'].delete("end", "end")
				self.combat_menu_size -= 1
			elif self.goal_mode.get() == "Shield":
				list = globals.character.postcap_build_shield_maneuvers_list
				self.add_shield_order_menu['menu'].delete("end", "end")
				self.edit_shield_order_menu['menu'].delete("end", "end")
				self.shield_menu_size -= 1
			elif self.goal_mode.get() == "Armor":
				list = globals.character.postcap_build_armor_maneuvers_list
				self.add_armor_order_menu['menu'].delete("end", "end")
				self.edit_armor_order_menu['menu'].delete("end", "end")
				self.armor_menu_size -= 1				
				
			list.pop(self.vars_dialog_edit_location.get()).PcP_Build_Row.grid_remove()
			for man in list:
				man.order.set(i+1)
				man.PcP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				man.PcP_Build_Row.grid(row=i, column=0)			
				i += 1	
			self.dialog_box.withdraw()		
			self.dialog_box.grab_release()
				
	
	# When a new maneuver is clicked from the maneuver drop down menu in the popup dialog box, this method will update the dialog box with the newly chosen skill/maneuver
	def Dialog_Menu_Onchange(self, name):
		if self.goal_mode.get() == "Skills":
			skill = globals.character.skills_list[name]
			self.vars_dialog_skill.set(name)
			self.vars_dialog_info.set("%s/%s (%s)" % (skill.ptp_cost, skill.mtp_cost, skill.max_ranks))
			self.dialog_max_ranks = skill.max_ranks
			
			subskill_ranks = globals.character.Get_Total_Ranks_Of_Subskill(skill.name, 100, skill.subskill_group)
			if subskill_ranks == 0:
				self.vars_dialog_precap_ranks.set(skill.total_ranks_by_level[100].get())
			else:
				self.vars_dialog_precap_ranks.set("%s + %s other subskill ranks" % (skill.total_ranks_by_level[100].get(), subskill_ranks))
		elif self.goal_mode.get() == "Combat":
			man = globals.character.combat_maneuvers_list[name]
			self.vars_dialog_combat_maneuver.set(name)				
		elif self.goal_mode.get() == "Shield":
			man = globals.character.shield_maneuvers_list[name]
			self.vars_dialog_shield_maneuver.set(name)				
		elif self.goal_mode.get() == "Armor":
			man = globals.character.armor_maneuvers_list[name]
			self.vars_dialog_armor_maneuver.set(name)		
			
		if self.goal_mode.get() != "Skills":
			self.vars_dialog_info.set("%s,    %s,    %s,    %s,    %s" % (man.Get_Cost_At_Rank(1), man.Get_Cost_At_Rank(2), man.Get_Cost_At_Rank(3), man.Get_Cost_At_Rank(4), man.Get_Cost_At_Rank(5)))		
			self.vars_dialog_prerequisites.set(man.prerequisites_displayed)	
			self.vars_dialog_precap_ranks.set(man.total_ranks_by_level[100].get())
			
	
	# This function is called to display the popup dialog box that allows a user to add a new skill/meneuver or edit an existing skill/maneuver.
	# Clicking the Add button in the Build Header frame will show the Add version of this box
	# Clicking an existing skills/maneuver's Edit button will show the Edit version of this box	and will populate it with the correct fields depending on the panel's style
	def Add_Edit_Button_Onclick(self, location):
		man = ""
		skill = ""
		bskill = ""
		subskill_ranks = 0
		
		self.dialog_skill_names_menu.grid_remove()
		self.dialog_combat_names_menu.grid_remove()
		self.dialog_shield_names_menu.grid_remove()
		self.dialog_armor_names_menu.grid_remove()
		self.add_skill_order_menu.grid_remove()
		self.add_combat_order_menu.grid_remove()
		self.add_shield_order_menu.grid_remove()
		self.add_armor_order_menu.grid_remove()
		self.edit_skill_order_menu.grid_remove()
		self.edit_combat_order_menu.grid_remove()
		self.edit_shield_order_menu.grid_remove()
		self.edit_armor_order_menu.grid_remove()
		
		self.vars_dialog_label_skill_name.grid_remove()
		self.vars_dialog_label_skill_costs.grid_remove()				
		self.vars_dialog_label_maneuver_name.grid_remove()
		self.vars_dialog_label_maneuver_costs.grid_remove()
		self.vars_dialog_label_maneuver_prerequisites.grid_remove()
		self.vars_dialog_maneuver_prerequisites.grid_remove()
		
		if self.dialog_box.component("buttonbox").button(0)["text"] == "Update Maneuver":
			self.dialog_box.component("buttonbox").delete("Update Maneuver")
			self.dialog_box.component("buttonbox").delete("Remove Maneuver")		
		elif self.dialog_box.component("buttonbox").button(0)["text"] == "Update Skill":
			self.dialog_box.component("buttonbox").delete("Update Skill")
			self.dialog_box.component("buttonbox").delete("Remove Skill")		
		elif self.dialog_box.component("buttonbox").button(0)["text"] == "Add Skill":
			self.dialog_box.component("buttonbox").delete("Add Skill")
		elif self.dialog_box.component("buttonbox").button(0)["text"] == "Add Maneuver":
			self.dialog_box.component("buttonbox").delete("Add Maneuver")
		
		self.vars_dialog_errormsg.set("")
		self.vars_dialog_hide.set("0")	
		
		if self.goal_mode.get() == "Skills":					
			if location == "":			
				self.vars_dialog_skill.set("Armor Use")
				skill = globals.character.skills_list["Armor Use"]
				self.vars_dialog_order.set(self.skills_menu_size)
				self.dialog_skill_names_menu.grid(row=0, column=1, sticky="w", columnspan=4)	
				self.add_skill_order_menu.grid(row=5, column=1, sticky="w")
			else:			
				bskill = globals.character.postcap_build_skills_list[int(location)]
				self.vars_dialog_skill.set(bskill.name.get())
				self.vars_dialog_goal.set(bskill.goal.get())	
				skill = globals.character.skills_list[bskill.name.get()]
				self.dialog_skill_names_menu.grid(row=0, column=1, sticky="w", columnspan=4)
				self.edit_skill_order_menu.grid(row=5, column=1, sticky="w")	
				
			self.dialog_box["title"] = "Add Skill"
			self.dialog_max_ranks = skill.max_ranks	
			
		elif self.goal_mode.get() == "Combat":
			char_man = globals.character.combat_maneuvers_list[self.dialog_combat_names_menu['menu'].entrycget(0, "label")]
			self.dialog_combat_names_menu.grid(row=0, column=1, sticky="w", columnspan=4)		
			self.dialog_box["title"] = "Add Combat Maneuver"
			
			if location == "":			
				self.vars_dialog_order.set(self.combat_menu_size)	
				self.vars_dialog_combat_maneuver.set(char_man.name)
				self.add_combat_order_menu.grid(row=5, column=1, sticky="w")	
			else:
				man = globals.character.postcap_build_combat_maneuvers_list[int(location)]
				char_man = globals.character.combat_maneuvers_list[man.name.get()]
				self.vars_dialog_goal.set(man.goal.get())	
				self.vars_dialog_combat_maneuver.set(man.name.get())
				self.edit_combat_order_menu.grid(row=5, column=1, sticky="w")	
			
		elif self.goal_mode.get() == "Shield":
			char_man = globals.character.shield_maneuvers_list[self.dialog_shield_names_menu['menu'].entrycget(0, "label")]	
			self.dialog_shield_names_menu.grid(row=0, column=1, sticky="w", columnspan=4)		
			self.dialog_box["title"] = "Add Shield Maneuver"
			
			if location == "":			
				self.vars_dialog_order.set(self.shield_menu_size)
				self.vars_dialog_shield_maneuver.set(char_man.name)
				self.add_shield_order_menu.grid(row=5, column=1, sticky="w")		
			else:
				man = globals.character.postcap_build_shield_maneuvers_list[int(location)]
				char_man = globals.character.shield_maneuvers_list[man.name.get()]
				self.vars_dialog_goal.set(man.goal.get())	
				self.vars_dialog_shield_maneuver.set(man.name.get())		
				self.edit_shield_order_menu.grid(row=5, column=1, sticky="w")	
			
		elif self.goal_mode.get() == "Armor":
			char_man = globals.character.armor_maneuvers_list[self.dialog_armor_names_menu['menu'].entrycget(0, "label")]
			self.dialog_armor_names_menu.grid(row=0, column=1, sticky="w", columnspan=4)			
			self.dialog_box["title"] = "Add Armor Maneuver"
			
			if location == "":			
				self.vars_dialog_order.set(self.armor_menu_size)
				self.vars_dialog_armor_maneuver.set(char_man.name)
				self.add_armor_order_menu.grid(row=5, column=1, sticky="w")		
			else:
				man = globals.character.postcap_build_armor_maneuvers_list[int(location)]
				char_man = globals.character.armor_maneuvers_list[man.name.get()]
				self.vars_dialog_goal.set(man.goal.get())	
				self.vars_dialog_armor_maneuver.set(man.name.get())		
				self.edit_armor_order_menu.grid(row=5, column=1, sticky="w")		
				
				
		# Location determines if this is the Add or Edit version of this box. A lack of Location means it is the Add version.
		# Location is used as a reference for what number frame called this function. IE: Location 4 is the 4th maneuver in the build list.		
		if location == "":
			self.vars_dialog_hide.set("0")
			self.vars_dialog_goal.set("")
			self.vars_dialog_errormsg.set("")
			
				
			if self.goal_mode.get() != "Skills":		
				self.dialog_box.component("buttonbox").insert("Add Maneuver", command=lambda v="Add Maneuver": self.Dialog_Box_Onclick(v))	
			elif self.goal_mode.get() == "Skills":			
				self.dialog_box.component("buttonbox").insert("Add Skill", command=lambda v="Add Skill": self.Dialog_Box_Onclick(v))	
		else:
			self.vars_dialog_edit_location.set(int(location))
			self.vars_dialog_order.set(int(location)+1)
			
			if man and man.hide.get() == "x":
				self.vars_dialog_hide.set("1")	
			elif bskill and bskill.hide.get() == "x":
				self.vars_dialog_hide.set("1")	
				

			if self.goal_mode.get() != "Skills":
				self.dialog_box.component("buttonbox").insert("Remove Maneuver", command=lambda v="Remove Maneuver": self.Dialog_Box_Onclick(v))	
				self.dialog_box.component("buttonbox").insert("Update Maneuver", command=lambda v="Update Maneuver": self.Dialog_Box_Onclick(v))	
			else:
				self.dialog_box.component("buttonbox").insert("Remove Skill", command=lambda v="Remove Skill": self.Dialog_Box_Onclick(v))	
				self.dialog_box.component("buttonbox").insert("Update Skill", command=lambda v="Update Skill": self.Dialog_Box_Onclick(v))
					
		
		if self.goal_mode.get() != "Skills":	
			self.vars_dialog_label_maneuver_name.grid(row=0, column=0, sticky="w")
			self.vars_dialog_label_maneuver_costs.grid(row=1, column=0, sticky="w")
			self.vars_dialog_label_maneuver_prerequisites.grid(row=2, column=0, sticky="w")
			self.vars_dialog_maneuver_prerequisites.grid(row=2, column=1, sticky="w")
			self.vars_dialog_prerequisites.set(char_man.prerequisites_displayed)	
			self.vars_dialog_info.set("%s,    %s,    %s,    %s,    %s" % (char_man.Get_Cost_At_Rank(1), char_man.Get_Cost_At_Rank(2), char_man.Get_Cost_At_Rank(3), char_man.Get_Cost_At_Rank(4), char_man.Get_Cost_At_Rank(5) ))	
			self.vars_dialog_precap_ranks.set(char_man.total_ranks_by_level[100].get())
		else:
			self.vars_dialog_label_skill_name.grid(row=0, column=0, sticky="w")
			self.vars_dialog_label_skill_costs.grid(row=1, column=0, sticky="w")	
			self.vars_dialog_info.set("%s / %s (%s)" % (skill.ptp_cost, skill.mtp_cost, skill.max_ranks))
			
			subskill_ranks = globals.character.Get_Total_Ranks_Of_Subskill(skill.name, 100, skill.subskill_group)
			if subskill_ranks == 0:
				self.vars_dialog_precap_ranks.set(skill.total_ranks_by_level[100].get())
			else:
				self.vars_dialog_precap_ranks.set("%s + %s other subskill ranks" % (skill.total_ranks_by_level[100].get(), subskill_ranks))			
		
		self.dialog_box.show()
		self.dialog_box.grab_set()
		
		
	# When the Clear All button is clicked, the postcap_build_skills_list and all postcap_build_maneuver_lists are emptied, 
	# all training point totals lists are reset, the menu sizes are set to 1 and experience counter is set back to 7572500
	def Clear_Button_Onclick(self, style):			
		if self.goal_mode.get() == "Skills" or style == "All":
			for key, row in globals.character.skills_list.items():
				row.Set_To_Default_Postcap()
			for man in globals.character.postcap_build_skills_list:	
				man.PcP_Build_Row.grid_remove()
			if self.skills_menu_size > 1:			
				self.skills_menu_size = 1		
				self.add_skill_order_menu['menu'].delete(1, "end")
				menu = [1]
				self.edit_skill_order_menu.set_menu(1, *menu)
			globals.character.postcap_build_skills_list = []	
			globals.character.postcap_skill_training_by_interval.clear()
			globals.character.postcap_total_skill_cost_by_interval.clear()
			globals.character.postcap_TP_conversions_by_interval.clear()
			
	
		if self.goal_mode.get() == "Combat" or style == "All":
			for key, row in globals.character.combat_maneuvers_list.items():
				row.Set_To_Default_Postcap()
			for man in globals.character.postcap_build_combat_maneuvers_list:	
				man.PcP_Build_Row.grid_remove()
			if self.combat_menu_size > 1:			
				self.combat_menu_size = 1		
				self.add_combat_order_menu['menu'].delete(1, "end")
				menu = [1]
				self.edit_combat_order_menu.set_menu(1, *menu)
			globals.character.postcap_build_combat_maneuvers_list = []	
			globals.character.postcap_combat_training_by_interval.clear()	
			globals.character.postcap_total_combat_cost_by_interval.clear()

			
		if self.goal_mode.get() == "Shield" or style == "All":		
			for key, row in globals.character.shield_maneuvers_list.items():
				row.Set_To_Default_Postcap()		
			for man in globals.character.postcap_build_shield_maneuvers_list:	
				man.PcP_Build_Row.grid_remove()
			if self.shield_menu_size > 1:	
				self.shield_menu_size = 1		
				self.add_shield_order_menu['menu'].delete(1, "end")
				menu = [1]
				self.edit_shield_order_menu.set_menu(1, *menu)
			globals.character.postcap_build_shield_maneuvers_list = []	
			globals.character.postcap_build_shield_maneuvers_list = []	
			globals.character.postcap_shield_training_by_interval.clear()	
			globals.character.postcap_total_shield_cost_by_interval.clear()
			
		if self.goal_mode.get() == "Armor" or style == "All":		
			for key, row in  globals.character.armor_maneuvers_list.items():
				row.Set_To_Default_Postcap()				
			for man in globals.character.postcap_build_armor_maneuvers_list:	
				man.PcP_Build_Row.grid_remove()		
			if self.armor_menu_size > 1:				
				self.armor_menu_size = 1	
				self.add_armor_order_menu['menu'].delete(1, "end")
				menu = [1]
				self.edit_armor_order_menu.set_menu(1, *menu)
			globals.character.postcap_build_armor_maneuvers_list = []
			globals.character.postcap_build_armor_maneuvers_list = []	
			globals.character.postcap_armor_training_by_interval.clear()	
			globals.character.postcap_total_armor_cost_by_interval.clear()

		self.PcP_radio_var.set(1)
		self.experience_counter.setvalue(7572500)
		if style == "All" and self.goal_mode.get() != "Skills":
			self.PostCap_Style_Onchange("Skills")
		else:
			self.Update_Schedule_Frames()

		
	# This method is called when the drop down menu in the build header is changed to a new value. 
	# Changing the value will swap out the current build list and schedule list values for either Skills, Combat, Shield, or Armor values.
	def PostCap_Style_Onchange(self, result):
		i=0				
		
		if self.current_goal_mode == result:
			return			
		
		# Remove the header and all footer rows
		self.schedule_skill_header.grid_remove()
		self.schedule_maneuver_header.grid_remove()
		self.sfooter_skill_title_row.grid_remove()	
		self.sfooter_ptp_row.grid_remove()
		self.sfooter_mtp_row.grid_remove()
		self.sfooter_maneuver_title_row.grid_remove()	
		self.sfooter_combat_row.grid_remove()
		self.sfooter_shield_row.grid_remove()
		self.sfooter_armor_row.grid_remove()
		
		# Depending on the previous style, remove those rows from the schedule frame
		if self.current_goal_mode == "Skills":	
			for man in globals.character.postcap_build_skills_list:
				man.PcP_Build_Row.grid_remove()
			for key, man in globals.character.skills_list.items():
				man.PcP_schedule_row.grid_remove()			
			
		elif self.current_goal_mode == "Combat":	
			for man in globals.character.postcap_build_combat_maneuvers_list:
				man.PcP_Build_Row.grid_remove()
			for key, man in globals.character.combat_maneuvers_list.items():
				man.PcP_schedule_row.grid_remove()
				
		elif self.current_goal_mode == "Shield":
			for man in globals.character.postcap_build_shield_maneuvers_list:	
				man.PcP_Build_Row.grid_remove()
			for key, man in globals.character.shield_maneuvers_list.items():
				man.PcP_schedule_row.grid_remove()
				
		elif self.current_goal_mode == "Armor":	
			for man in globals.character.postcap_build_armor_maneuvers_list:	
				man.PcP_Build_Row.grid_remove()
			for key, man in globals.character.armor_maneuvers_list.items():
				man.PcP_schedule_row.grid_remove()
		
		# Add the correct header and footer fields for the newly chosen style
		if result == "Skills":
			self.schedule_skill_header.grid(row=3, column=0, sticky="w")
			self.sfooter_skill_title_row.grid(row=0, column=0, padx="1")	
			self.sfooter_ptp_row.grid(row=1, column=0, padx="1")		
			self.sfooter_mtp_row.grid(row=2, column=0, padx="1")	
			
		else: 
			self.schedule_maneuver_header.grid(row=3, column=0, sticky="w")
			self.sfooter_maneuver_title_row.grid(row=0, column=0, padx="1")	
			self.sfooter_combat_row.grid(row=1, column=0, padx="1")	

			if globals.character.profession.name == "Paladin" or globals.character.profession.name == "Rogue" or globals.character.profession.name == "Warrior":
				self.sfooter_shield_row.grid(row=2, column=0, padx="1")	
				self.sfooter_armor_row.grid(row=3, column=0, padx="1")	
			
		if result == "Skills":
			self.current_goal_mode = "Skills"
			self.goal_mode.set("Skills")				
			list = globals.character.postcap_build_skills_list
		elif result == "Combat":
			self.current_goal_mode = "Combat"
			self.goal_mode.set("Combat")				
			list = globals.character.postcap_build_combat_maneuvers_list
		elif result == "Shield":
			self.current_goal_mode = "Shield"
			self.goal_mode.set("Shield")				
			list = globals.character.postcap_build_shield_maneuvers_list
		elif result == "Armor":
			self.current_goal_mode = "Armor"
			self.goal_mode.set("Armor")
			list = globals.character.postcap_build_armor_maneuvers_list
				
		for item in list:
			item.order.set(i+1)
			item.PcP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
			item.PcP_Build_Row.grid(row=i, column=0)	
			i += 1	
			
		self.ML_Frame.yview("moveto", 0, "units")
		self.MR_Frame.yview("moveto", 0, "units")		
		self.Update_Schedule_Frames()	
		

	# When the Calculate button is pushed the planner will map out what skills to train in or maneuvers to take at each expereience interval.
	# Unlike the precap training, postcap skill training will simply increase the experience interval by 2500 to generate more TP if the character doesn't have enough to train in something.
	# On a similar note, unless the character has enough training in the corresponding maneuver skill, the planner will throw an error when trying to train maneuvers if the character would never have enough.
	# Calculate All will do this for Skills, Combat, Shield, Armor in that order.
	# This method will also call on a number of different Skills and Maneuver object methods as well. Please review the Skills class and Maneuver class in Globals.py for more information.
	def Plan_Training_Schedule(self, style):
		abort_loops = 0; error_text = ""
		schedule_names = []			
		ending_exp = 7572500
		pcost = 0
		mcost = 0
		current_ptp = globals.panels["Skills"].total_leftover_ptp_by_level[100].get()
		current_mtp = globals.panels["Skills"].total_leftover_mtp_by_level[100].get()	
		style_list = []
		
		if style == "All":
			style_list = ["Combat", "Shield", "Armor"]
		elif style != "Skills":
			style_list.append(style)
		
		globals.character.postcap_total_skill_cost_by_interval.clear()
		globals.character.postcap_skill_training_by_interval.clear()	
		globals.character.postcap_TP_conversions_by_interval.clear()		
		globals.character.postcap_combat_training_by_interval.clear()	
		globals.character.postcap_total_combat_cost_by_interval.clear()		
		globals.character.postcap_shield_training_by_interval.clear()	
		globals.character.postcap_total_shield_cost_by_interval.clear()		
		globals.character.postcap_armor_training_by_interval.clear()	
		globals.character.postcap_total_armor_cost_by_interval.clear()	
		
		# Calculate skill training
		if style == "Skills" or style == "All":
			# Clear schedule before using it.
			for key, row in globals.character.skills_list.items():	
				row.Set_To_Default_Postcap()
			
			# Go through each skill in the build list and attempt to train ranks in each one
			for skill in globals.character.postcap_build_skills_list:	
				if skill.hide.get() == 'x':
					continue
				char_skill = globals.character.skills_list[skill.name.get()]				
				total_pcost = 0
				total_mcost = 0
				goal = int(skill.goal.get())
				subskill_ranks = 0
				ranks_taken = 0
				needed_exp = 0			
				sum = 0			
							
				# Train each rank in the skill
				while ranks_taken < goal:
					converted_PTP2MTP = 0
					converted_MTP2PTP = 0
					subskill_ranks = globals.character.Get_Total_Postcap_Ranks_Of_Subskill(skill.name.get(), ending_exp + needed_exp, char_skill.subskill_group)
					(pcost, mcost) = globals.character.skills_list[skill.name.get()].Get_Next_Ranks_Cost(101, subskill_ranks, 1)
					
					# This error will happen if the character tries to train beyond the skill cap. This only happens if the character has multiple build_skills for the same skills
					if pcost == 9999 and mcost == 9999:
						error_text = "ERROR: Cannot to train beyond %s ranks in skill: %s.\nPlease adjust postcap training." % (char_skill.max_ranks*101, skill.name.get())
						abort_loops = 1
						break
					
					current_ptp -= pcost
					current_mtp -= mcost
					total_pcost += pcost
					total_mcost += mcost
					
					# Do TP conversions if the costs put the character into negatives.
					# Unlike precap, postcap has endless TP (technically). So just increase the exp to get more TP if you run out.
					while current_ptp < 0 or current_mtp < 0:					
						if current_ptp < 0 and current_mtp > 1:
							while current_ptp < 0 and current_mtp > 1:
								current_ptp += 1
								current_mtp -= 2
								converted_MTP2PTP -= 2
								converted_PTP2MTP += 1
							continue	
						elif current_mtp < 0 and current_ptp > 1:
							while current_mtp < 0 and current_ptp > 1:
								current_mtp += 1
								current_ptp -= 2
								converted_PTP2MTP -= 2
								converted_MTP2PTP += 1
							continue							
								
						needed_exp += 2500
						if converted_MTP2PTP < 0:
							current_mtp += 2
							converted_PTP2MTP += 2
						else:
							current_ptp += 1
							
						if converted_PTP2MTP < 0:
							current_ptp += 2
							converted_PTP2MTP += 2
						else:
							current_mtp += 1
					
					# Break the loop if an error was encountered	
					if abort_loops == 1:
						break						
					
					# Make a note of TP conversions
					if (ending_exp + needed_exp) in globals.character.postcap_TP_conversions_by_interval:
						(prev_ptp, prev_mtp) = globals.character.postcap_TP_conversions_by_interval[ending_exp + needed_exp].split("|")[0].split("/")
						(prev_total_ptp, prev_total_mtp) = globals.character.postcap_TP_conversions_by_interval[ending_exp + needed_exp].split("|")[0].split("/")
						globals.character.postcap_TP_conversions_by_interval[ending_exp + needed_exp] = "%s/%s|%s/%s" % (converted_PTP2MTP + int(prev_ptp), converted_MTP2PTP + int(prev_mtp), converted_PTP2MTP + int(prev_total_ptp), converted_MTP2PTP + int(prev_total_mtp))
					else:
						prev_total_ptp = 0
						prev_total_mtp = 0
						for key, val in globals.character.postcap_TP_conversions_by_interval.items():
							(prev_total_ptp, prev_total_mtp) = val.split("|")[1].split("/")	
						globals.character.postcap_TP_conversions_by_interval[ending_exp + needed_exp] = "%s/%s|%s/%s" % (converted_PTP2MTP, converted_MTP2PTP, converted_PTP2MTP + int(prev_total_ptp), converted_MTP2PTP + int(prev_total_mtp))
							
					# Do the actual skill training here
					globals.character.skills_list[skill.name.get()].Train_Postcap_Ranks(1, subskill_ranks, ending_exp + needed_exp)				
					ranks_taken += 1
					
				if abort_loops == 1:
					break
					
				# Set the values of the build skill row with how much exp is needed and what exp we end up at after all the training.
				ending_exp += needed_exp
				skill.info.set("%s / %s" % (total_pcost, total_mcost))	
				skill.needed_exp.set("{:,}".format(needed_exp))			
				skill.ending_exp.set("{:,}".format(ending_exp))
				skill.needed_exp_label.bind("<Button-1>", lambda event, arg=ending_exp-needed_exp: skill.PcP_Row_Label_Onclick(event, arg))
				skill.ending_exp_label.bind("<Button-1>", lambda event, arg=ending_exp: skill.PcP_Row_Label_Onclick(event, arg))
				
				if len(globals.character.skills_list[skill.name.get()].postcap_exp_intervals) > 0:	
					globals.character.skills_list[skill.name.get()].postcap_total_ranks_at_interval.clear()
					for key, val in globals.character.skills_list[skill.name.get()].postcap_ranks_at_interval.items():
						sum += int(val)
						gskill = globals.character.skills_list[skill.name.get()]
						gskill.postcap_total_ranks_at_interval[key] = sum
						gskill.postcap_bonus_at_interval[key] = gskill.Get_Skill_Bonus(sum)						
						

			# If no problems occured, loop through the skill training and calculate the total cost for each interval
			if abort_loops != 1:										
				total_pcost = 0
				total_mcost = 0
				for key, val in globals.character.postcap_skill_training_by_interval.items():	
					pcost = 0
					mcost = 0
					parts = val.split("|")
				
					for part in parts:
						(name, ranks) = part.split(":")
						name = part.split(":")[0]
						costs = globals.character.skills_list[name].postcap_cost_at_interval[key].split("|")
						for cost in costs:
							(ptp, mtp) = cost.split("/")
							pcost += int(ptp)
							mcost += int(mtp)			
					
					total_pcost += pcost
					total_mcost += mcost		
					
					globals.character.postcap_total_skill_cost_by_interval[key] = "%s/%s|%s/%s" % (pcost, mcost, total_pcost, total_mcost)	
					
		if len(style_list) > 0:
			# Training in maneuvers is more or less the same, just with different lists. Go through each style (if "All" was used) and train in each maneuver of that type
			for s in style_list:
				if abort_loops == 1:
					break
					
				# Get the appropriate lists for the current style
				if s == "Combat":
					build_list = globals.character.postcap_build_combat_maneuvers_list
					if len(build_list) == 0:
						continue
					char_skill = globals.character.skills_list["Combat Maneuvers"]
					char_man_list = globals.character.combat_maneuvers_list
					man_training_intervals = globals.character.postcap_combat_training_by_interval
					man_total_cost_list = globals.character.postcap_total_combat_cost_by_interval
					precap_points = globals.panels["Maneuvers"].total_leftover_combat_points_by_level[100].get()
				elif s == "Shield":
					build_list = globals.character.postcap_build_shield_maneuvers_list
					if len(build_list) == 0:
						continue
					char_skill = globals.character.skills_list["Shield Use"]
					char_man_list = globals.character.shield_maneuvers_list
					man_training_intervals = globals.character.postcap_shield_training_by_interval
					man_total_cost_list = globals.character.postcap_total_shield_cost_by_interval
					precap_points = globals.panels["Maneuvers"].total_leftover_shield_points_by_level[100].get()
				elif s == "Armor":
					build_list = globals.character.postcap_build_armor_maneuvers_list
					if len(build_list) == 0:
						continue
					char_skill = globals.character.skills_list["Armor Use"]
					char_man_list = globals.character.armor_maneuvers_list
					man_training_intervals = globals.character.postcap_armor_training_by_interval
					man_total_cost_list = globals.character.postcap_total_armor_cost_by_interval
					precap_points = globals.panels["Maneuvers"].total_leftover_armor_points_by_level[100].get()
					
				
				ending_exp = 7572500	
				
				# Clear schedule before using it.
				for key, row in char_man_list.items():	
					row.Set_To_Default_Postcap()								
					
				# Train in each maneuver in the list
				i = 0 				
				for man in build_list:		
					if man.hide.get() == 'x':
						continue
					char_man = char_man_list[man.name.get()]
					precap_ranks = char_man.total_ranks_by_level[100].get()
					postcap_ranks = 0
					total_cost = 0
					cost = 0
					goal = int(man.goal.get())
					ranks_taken = 0
					current_exp = 7572500	
					sum = 0			
						
					if len(char_man.postcap_exp_intervals) > 0:
						postcap_ranks = char_man.postcap_total_ranks_at_interval[char_man.postcap_exp_intervals[-1]]
						
					# Cancel the whole thing if the character doesn't have the right prerequisites for the maneuver	
					if not globals.character.Meets_Maneuver_Prerequisites(101, char_man.name, char_man.type):
						error_text += "ERROR: Prerequisites for %s not meet.\n" % (man.name.get())							
						abort_loops = 1
						break
					
					# Start training each rank
					while ranks_taken < goal:
						if abort_loops == 1:
							break
						cost = char_man.Get_Cost_At_Rank(precap_ranks + postcap_ranks + ranks_taken + 1)  
						
						# This error will happen if the character tries to train beyond the max ranks of the maneuver. This only happens if the character has multiple build_maneuverss for the same maneuver
						if cost == 9999 or cost == "-":
							error_text = "ERROR: Cannot train beyond %s ranks in maneuver: %s.\nPlease adjust postcap training." % (char_man.max_ranks, char_man.name)
							abort_loops = 1
							break
							
						# Get more points to train this skill						
						while precap_points < cost:		
							if i >= len(char_skill.postcap_exp_intervals):
								error_text = "ERROR: Not enough training points to train %s ranks in maneuver: %s.\nPlease adjust postcap training." % (char_man.max_ranks, char_man.name)
								abort_loops = 1
								break						
							precap_points += char_skill.postcap_ranks_at_interval[char_skill.postcap_exp_intervals[i]]
							current_exp = char_skill.postcap_exp_intervals[i]
							i += 1
							
						precap_points -= cost 
						total_cost += cost
						ranks_taken += 1
						char_man.Train_Postcap_Ranks(current_exp, 1)					

					if abort_loops == 1:
						break
						
					if len(char_skill.postcap_exp_intervals) > 1:
						needed_exp = char_skill.postcap_exp_intervals[i-1] - ending_exp
						ending_exp = char_skill.postcap_exp_intervals[i-1]
					else:
						needed_exp = 0
						
					# Set the values of the build skill row with how much exp is needed and what exp we end up at after all the training.
					man.cost.set("%s" % total_cost)	
					man.needed_exp.set("{:,}".format(needed_exp))			
					man.ending_exp.set("{:,}".format(ending_exp))
					man.needed_exp_label.bind("<Button-1>", lambda event, arg=ending_exp-needed_exp: man.PcP_Row_Label_Onclick(event, arg))	
					man.ending_exp_label.bind("<Button-1>", lambda event, arg=ending_exp: man.PcP_Row_Label_Onclick(event, arg))					
					
					if len(char_man_list[man.name.get()].postcap_exp_intervals) > 0:	
						char_man_list[man.name.get()].postcap_total_ranks_at_interval.clear()
						for key, val in char_man_list[man.name.get()].postcap_ranks_at_interval.items():
							sum += int(val)
							gman = char_man_list[man.name.get()]
							gman.postcap_total_ranks_at_interval[key] = sum
#							gman.postcap_bonus_at_interval[key] = gman.Get_Skill_Bonus(sum)		

				# If no problems occured, loop through the maneuver training costs and calculate the total cost for each interval
				if abort_loops != 1:										
					total_cost = 0
					
					for key, val in man_training_intervals.items():	
						combat_cost = 0
						parts = val.split("|")				
						
						for part in parts:
							(name, ranks) = part.split(":")
							name = part.split(":")[0]
							costs = char_man_list[name].postcap_cost_at_interval[key].split("|")
							for cost in costs:
								combat_cost += int(cost)		
						
						total_cost += combat_cost		
						man_total_cost_list[key] = "%s|%s" % (combat_cost, total_cost)		

		if error_text != "":	
			globals.info_dialog.Show_Message(error_text)
		else:
			self.experience_counter.setvalue(7572500)	
			self.Update_Schedule_Frames()	

		
	# This is called when user changes the experience counter or when the user's build has been recalculated.
	# It uses what ever the current experience interval is and updates the schedule frame and schedule footer			
	def Update_Schedule_Frames(self):
		if self.experience_counter.getvalue() == "":
			return
		elif int(self.experience_counter.getvalue()) < 7572500:
			exp = 7572500
		else:
			exp = int(self.experience_counter.getvalue())
			
		i = 0		
		style = self.goal_mode.get()
		prof = globals.character.profession.name
		precap_ptp = globals.panels["Skills"].total_leftover_ptp_by_level[100].get()
		precap_mtp = globals.panels["Skills"].total_leftover_mtp_by_level[100].get()
		
		
		if style == "Skills":			
			prev_ptp_cost = 0
			prev_mtp_cost = 0
			ptp_cost = 0
			mtp_cost = 0
			ptp_converstion = 0
			mtp_converstion = 0
			prev_ptp_converstion = 0
			prev_mtp_converstion = 0
			current_keys = globals.skill_names
			current_schedule = globals.character.skills_list						
			prev_exp = globals.character.Get_Last_Training_Interval(exp-1, "skills", "")
			
			if len(globals.character.postcap_total_skill_cost_by_interval) > 0:			
				if exp in globals.character.postcap_total_skill_cost_by_interval:
					(ptp_cost, mtp_cost) = globals.character.postcap_total_skill_cost_by_interval[exp].split("|")[0].split("/")		
				
				if prev_exp < exp:
					(prev_ptp_cost, prev_mtp_cost) = globals.character.postcap_total_skill_cost_by_interval[prev_exp].split("|")[1].split("/")
					
			if len(globals.character.postcap_TP_conversions_by_interval) > 0:			
				if exp in globals.character.postcap_TP_conversions_by_interval:	
					(ptp_converstion, mtp_converstion) = globals.character.postcap_TP_conversions_by_interval[exp].split("|")[0].split("/")
				
				if prev_exp < exp and prev_exp > 0:
					(prev_ptp_converstion, prev_mtp_converstion) = globals.character.postcap_TP_conversions_by_interval[prev_exp].split("|")[1].split("/")	
					
			
			if exp == 7572500:
				self.vars_sfooter_ptp_earned.set(precap_ptp)
				self.vars_sfooter_mtp_earned.set(precap_mtp)
			else:
				self.vars_sfooter_ptp_earned.set(1)
				self.vars_sfooter_mtp_earned.set(1)
				
				
			self.vars_sfooter_ptp_available.set(precap_ptp + int((exp - 7572500) / 2500) - int(prev_ptp_cost) + int(prev_ptp_converstion))
			self.vars_sfooter_mtp_available.set(precap_mtp + int((exp - 7572500) / 2500) - int(prev_mtp_cost) + int(prev_mtp_converstion))
			self.vars_sfooter_ptp_total_cost.set(ptp_cost)
			self.vars_sfooter_mtp_total_cost.set(mtp_cost)
			self.vars_sfooter_ptp_converted.set(ptp_converstion)
			self.vars_sfooter_mtp_converted.set(mtp_converstion)
			self.vars_sfooter_ptp_leftover.set(precap_ptp + int((exp - 7572500) / 2500) - int(prev_ptp_cost) + int(ptp_converstion) + int(prev_ptp_converstion) - int(ptp_cost))
			self.vars_sfooter_mtp_leftover.set(precap_mtp + int((exp - 7572500) / 2500) - int(prev_mtp_cost) + int(mtp_converstion) + int(prev_mtp_converstion) - int(mtp_cost))			
						
		else:
			style_list = ["Combat", "Shield", "Armor"]
			for s in style_list:
				prev_cost = 0
				cost = 0
				earned = 0
				prev_earned = 0				
				
				if s == "Combat":
					precap_points = globals.panels["Maneuvers"].total_leftover_combat_points_by_level[100].get()
					skill = globals.character.skills_list["Combat Maneuvers"]
					skills_prev_exp = globals.character.Get_Last_Training_Interval(exp-1, "skills", "Combat Maneuvers")
					prev_exp = globals.character.Get_Last_Training_Interval(exp-1, "combat", "")
					interval_list = globals.character.postcap_total_combat_cost_by_interval
					vars_earned = self.vars_sfooter_combat_earned			
					vars_available = self.vars_sfooter_combat_available
					vars_total_cost = self.vars_sfooter_combat_total_cost
					vars_leftover = self.vars_sfooter_combat_leftover	
				elif s == "Shield":
					precap_points = globals.panels["Maneuvers"].total_leftover_shield_points_by_level[100].get()
					skill = globals.character.skills_list["Shield Use"]
					skills_prev_exp = globals.character.Get_Last_Training_Interval(exp-1, "skills", "Shield Use")
					prev_exp = globals.character.Get_Last_Training_Interval(exp-1, "shield", "")
					interval_list = globals.character.postcap_total_shield_cost_by_interval
					vars_earned = self.vars_sfooter_shield_earned			
					vars_available = self.vars_sfooter_shield_available
					vars_total_cost = self.vars_sfooter_shield_total_cost
					vars_leftover = self.vars_sfooter_shield_leftover	
				elif s == "Armor":
					precap_points = globals.panels["Maneuvers"].total_leftover_armor_points_by_level[100].get()
					skill = globals.character.skills_list["Armor Use"]
					skills_prev_exp = globals.character.Get_Last_Training_Interval(exp-1, "skills", "Armor Use")
					prev_exp = globals.character.Get_Last_Training_Interval(exp-1, "armor", "")
					interval_list = globals.character.postcap_total_armor_cost_by_interval
					vars_earned = self.vars_sfooter_armor_earned			
					vars_available = self.vars_sfooter_armor_available
					vars_total_cost = self.vars_sfooter_armor_total_cost
					vars_leftover = self.vars_sfooter_armor_leftover	
					
				if len(interval_list) > 0:			
					if exp in interval_list:
						cost = interval_list[exp].split("|")[0]		
					
					if prev_exp != 0 and prev_exp < exp and prev_exp in interval_list:
						prev_cost = interval_list[prev_exp].split("|")[1]						
									
				if exp in skill.postcap_exp_intervals:
					earned = skill.postcap_ranks_at_interval[exp]
					prev_earned = skill.postcap_total_ranks_at_interval[exp]
				elif skills_prev_exp != 0 and skills_prev_exp < exp:
					prev_earned = skill.postcap_total_ranks_at_interval[skills_prev_exp]					
				
				if exp == 7572500:
					vars_earned.set(precap_points + earned)
				else:
					vars_earned.set(earned)			
					
				vars_available.set(precap_points + prev_earned - int(prev_cost))
				vars_total_cost.set(cost)
				vars_leftover.set(precap_points + prev_earned - int(prev_cost) - int(cost))			
			
		# Pick the right lists to display schedule rows from
		if style == "Combat":
			current_keys = globals.combat_maneuver_names
			current_schedule = globals.character.combat_maneuvers_list	
		elif style == "Shield":
			current_keys = globals.shield_maneuver_names
			current_schedule = globals.character.shield_maneuvers_list
		elif style == "Armor":		
			current_keys = globals.armor_maneuver_names
			current_schedule = globals.character.armor_maneuvers_list				
			
		# Display and update the schedule rows for the experience interval	
		for key in current_keys:	
			row = current_schedule[key]		
			total_postcap_ranks = 0
			pcost = 0
			mcost = 0
			total_pcost = 0
			total_mcost = 0
				
			if style == "Skills" and row.active_skill == 1:		
				# Remove a row if it shouldn't be shown right now. Otherwise, move on and reset everything to default
				if self.PcP_radio_var.get() == 2 and row.total_ranks_by_level[100].get() == 0 and len(row.postcap_exp_intervals) == 0:
					row.PcP_schedule_row.grid_remove()	
					continue
				elif self.PcP_radio_var.get() == 3 and exp not in row.postcap_exp_intervals:
					row.PcP_schedule_row.grid_remove()	
					continue
				
				row.postcap_ranks.set(0)
				row.postcap_sum_cost.set("")	
				row.postcap_cost.set("")
				
				# Get the last time this skill was trained in before this experience interval
				last_exp = globals.character.Get_Last_Training_Interval(exp-1, "skills", row.name)
				total_postcap_ranks = int(row.total_ranks_by_level[100].get())
				
				# Assuming the last time isn't 0 (never trained) or greater than this experience interval (first train is in the future) then ...
				if last_exp != 0 and exp >= last_exp:	
						if exp != last_exp:
							total_postcap_ranks += row.postcap_total_ranks_at_interval[last_exp]
							
						# Calculate the total cost of this skill and set that as the sum cost
						for key, val in globals.character.skills_list[row.name].postcap_cost_at_interval.items():
							if int(key) > exp:
								break
							costs = val.split("|")
							for cost in costs:
								(ptp, mtp) = cost.split("/")
								total_pcost += int(ptp)
								total_mcost += int(mtp)				
						row.postcap_sum_cost.set("%s/%s" % (total_pcost, total_mcost))							
				
				# If this skill was trained in this exp interval then calculate it's cost
				if exp in row.postcap_exp_intervals:		
					row.postcap_ranks.set(row.postcap_ranks_at_interval[exp])
					total_postcap_ranks += int(row.postcap_ranks_at_interval[exp])		
					
					costs = globals.character.skills_list[row.name].postcap_cost_at_interval[exp].split("|")
					for cost in costs:
						(ptp, mtp) = cost.split("/")
						pcost += int(ptp)
						mcost += int(mtp)				
					row.postcap_cost.set("%s/%s" % (pcost, mcost))									
					
				# Set the total ranks and bonus for the schedule row then display it
				row.postcap_total_ranks.set( total_postcap_ranks )
				row.postcap_bonus.set(row.Get_Skill_Bonus(total_postcap_ranks))		
#				row.postcap_bonus.set(row.postcap_bonus_at_interval[exp])								
				row.PcP_schedule_row.grid(row=i, column=0)
				
			# Display manuevers	
			elif (style == "Combat" or style == "Shield" or style == "Armor") and row.availability[prof] == 1:		
				# Remove a row if it shouldn't be shown right now. Otherwise, move on and reset everything to default					
				if self.PcP_radio_var.get() == 2 and row.total_ranks_by_level[100].get() == 0 and len(row.postcap_exp_intervals) == 0:
					row.PcP_schedule_row.grid_remove()	
					continue
				elif self.PcP_radio_var.get() == 3 and exp not in row.postcap_exp_intervals:
					row.PcP_schedule_row.grid_remove()	
					continue
					
				row.postcap_ranks.set(0)	
				row.postcap_cost.set("")	
				row.postcap_sum_cost.set("")					
				
				# Get the last time this maneuver's corresponding skill was trained in before this experience interval
				last_exp = globals.character.Get_Last_Training_Interval(exp-1, style.lower(), row.name)
				total_postcap_ranks = int(row.total_ranks_by_level[100].get())
				
				# Assumeing the last time isn't 0 (never trained) or greater than this experience interval (first train is in the future) then ...
				if last_exp != 0 and exp >= last_exp:	
						if exp != last_exp:
							total_postcap_ranks += row.postcap_total_ranks_at_interval[last_exp]
							
						# Calculate the total cost of this skill and set that as the sum cost
						for key, val in current_schedule[row.name].postcap_cost_at_interval.items():
							if int(key) > exp:
								break
							costs = val.split("|")
							for cost in costs:
								total_pcost += int(cost)		
						row.postcap_sum_cost.set(total_pcost)	
						
				# If this maneuver was trained in this exp interval then calculate it's cost						
				if exp in row.postcap_exp_intervals:		
					row.postcap_ranks.set(row.postcap_ranks_at_interval[exp])
					total_postcap_ranks += int(row.postcap_ranks_at_interval[exp])		
				
					costs = current_schedule[row.name].postcap_cost_at_interval[exp].split("|")
					for cost in costs:
						pcost += int(cost)			
					row.postcap_cost.set(pcost)		
				
				# Set the total ranks for the schedule row then display it
				row.postcap_total_ranks.set( total_postcap_ranks )
				row.PcP_schedule_row.grid(row=i, column=0)
				
			else:
				row.PcP_schedule_row.grid_remove()
			i += 1
			

	# This allows mouse scrolling in the build frame. Anything with the bind tag SkP_Build will allow the scrolling
	def Scroll_Build_Frame(self, event):
		self.ML_Frame.yview("scroll", -1*(event.delta/120), "units")
		
		
	# This allows mouse scrolling in the schedule frame. Anything with the bind tag SkP_Schedule will allow the scrolling	
	def Scroll_Schedule_Frame(self, event):
		self.MR_Frame.yview("scroll", -1*(event.delta/120), "units")	


	# Wrapper function used by Globals.py to create a new Postcap_Skill from a Character file.		
	def Create_Postcap_Build_List_Skill(self, parent, name, hidden, order, info, goal):
		return PostCap_Build_List_Skill(parent, name, hidden, order, info, goal)
	
	
	# Wrapper function used by Globals.py to create a new Postcap_Maneuver from a Character file.		
	def Create_Postcap_Build_List_Maneuver(self, parent, name, type, hidden, order, goal, ranks_arr ):
		return PostCap_Build_List_Maneuver(parent, name, type, hidden, order, goal, ranks_arr )
		
		
# This class holds all the information for a specific skill the character wants to train in. These skills are shown the build frame using the object's SkP_Build_Row frame
class PostCap_Build_List_Skill:
	def __init__(self, parent, name, hidden, order, info, goal):
		self.name = tkinter.StringVar()
		self.info = tkinter.StringVar()
		self.order = tkinter.StringVar()
		self.hide = tkinter.StringVar()
		self.needed_exp = tkinter.StringVar()
		self.ending_exp = tkinter.StringVar()
		self.goal = tkinter.StringVar()
		self.PcP_Build_Row = tkinter.Frame(parent)
		self.PcP_Edit_Button = ""
		self.needed_exp_label = ""
		self.ending_exp_label = ""
		
		self.exp_intervals = {}
		
		self.base_training_rate = [0 for i in range(101)]
		self.adjusted_training_rate = [0 for i in range(101)]
								
		self.name.set(name)
		self.hide.set(hidden)
		self.order.set(order)
		self.info.set(info)
		self.goal.set(goal)
		self.PcP_Build_Row.bindtags("PcP_build")
		
		L1 = tkinter.Label(self.PcP_Build_Row, width=3, bg="lightgray", textvariable=self.hide)
		L1.grid(row=0, column=0, padx="1", pady="1")
		L1.bindtags("PcP_build")
		L2 = tkinter.Label(self.PcP_Build_Row, width=6, bg="lightgray", textvariable=self.order)
		L2.grid(row=0, column=1, padx="1", pady="1")
		L2.bindtags("PcP_build")
		L3 = tkinter.Label(self.PcP_Build_Row, width="26", anchor="w", bg="lightgray", textvariable=self.name)
		L3.grid(row=0, column=2, padx="1", pady="1")
		L3.bindtags("PcP_build")
		L4 = tkinter.Label(self.PcP_Build_Row, width=5, bg="lightgray", textvariable=self.goal)
		L4.grid(row=0, column=3, padx="1")
		L4.bindtags("PcP_build")
		L5 = tkinter.Label(self.PcP_Build_Row, width="10", bg="lightgray", textvar=self.info)
		L5.grid(row=0, column=4, padx="1", pady="1")
		L5.bindtags("PcP_build")
		self.needed_exp_label = tkinter.Label(self.PcP_Build_Row, width=10, bg="lightgray", textvariable=self.needed_exp)
		self.needed_exp_label.grid(row=0, column=5, padx="1")
		self.needed_exp_label.bind("<MouseWheel>", globals.panels["Post Cap"].Scroll_Build_Frame)
		self.ending_exp_label = tkinter.Label(self.PcP_Build_Row, width=10, bg="lightgray", textvariable=self.ending_exp)
		self.ending_exp_label.grid(row=0, column=6, padx="1")
		self.ending_exp_label.bind("<MouseWheel>", globals.panels["Post Cap"].Scroll_Build_Frame)
		self.PcP_Edit_Button = tkinter.Button(self.PcP_Build_Row, text="Edit", command="")
		self.PcP_Edit_Button.grid(row=0, column=7, padx="3")	

		
	# Calculates out how much exp will be needed to train "goal" amount of ranks.
	def Calculate_Total_Cost(self):
		goal = int(self.goal.get())
		exp_at_100 = 7572500
		needed = 0
		target = 0
		
		skill = globals.character.skills_list[self.name.get()]
		
		(pcost, mcost) = skill.Get_Next_Ranks_Cost(100, 0, goal)
		self.info.set("%s / %s" % (pcost, mcost))
		self.needed_exp.set("")
		self.ending_exp.set("")
		
	
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


	# Clicking either the need_exp or ending_exp label of this object will "jump" the exp_counter to that experience number					
	def PcP_Row_Label_Onclick(self, event, val):
		globals.panels["Post Cap"].experience_counter.setvalue(val)		
		

# This class holds all the information for a specific maneuver the character wants to train in. These maneuvers are shown the build frame using the object's PcP_Build_Row frame		
class PostCap_Build_List_Maneuver:
	def __init__(self, parent, name, type, hidden, order, goal, ranks_arr ):
		self.name = tkinter.StringVar()
		self.ranks = [tkinter.StringVar() for i in range(5)]
		self.order = tkinter.StringVar()
		self.hide = tkinter.StringVar()
		self.goal = tkinter.StringVar()
		self.cost = tkinter.StringVar()
		self.needed_exp = tkinter.StringVar()
		self.ending_exp = tkinter.StringVar()
		self.PcP_Build_Row = tkinter.Frame(parent)
		self.PcP_Edit_Button = ""
		self.needed_exp_label = ""
		self.ending_exp_label = ""
		self.type = type				
		
		if globals.character.profession.type == "square" or self.type != "Combat":
			modifier = 1
		elif globals.character.profession.type == "semi":
			modifier = 1.5
		elif globals.character.profession.type == "pure":
			modifier = 2
			
		i=0
		for rank in ranks_arr:
			if rank != "-":
				self.ranks[i].set( math.floor(int(rank) * modifier) )
			else:
				self.ranks[i].set("-")			
			i += 1
						
		self.name.set(name)
		self.hide.set(hidden)
		self.order.set(order)
		self.goal.set(goal)
				
		L1 = tkinter.Label(self.PcP_Build_Row, width=3, bg="lightgray", textvariable=self.hide)
		L1.grid(row=0, column=0, sticky="w", padx="1", pady="1")
		L1.bindtags("PcP_build")
		L2 = tkinter.Label(self.PcP_Build_Row, width=6, bg="lightgray", textvariable=self.order)
		L2.grid(row=0, column=1, padx="1", pady="1")
		L2.bindtags("PcP_build")
		L3 = tkinter.Label(self.PcP_Build_Row, width="26", anchor="w", bg="lightgray", textvariable=self.name)
		L3.grid(row=0, column=2, padx="1", pady="1")
		L3.bindtags("PcP_build")
		L4 = tkinter.Label(self.PcP_Build_Row, width=5, bg="lightgray", textvariable=self.goal)
		L4.grid(row=0, column=3, padx="1")
		L4.bindtags("PcP_build")
		L5 = tkinter.Label(self.PcP_Build_Row, width="10", bg="lightgray", textvar=self.cost)
		L5.grid(row=0, column=4, padx="1", pady="1")
		L5.bindtags("PcP_build")
		self.needed_exp_label = tkinter.Label(self.PcP_Build_Row, width=10, bg="lightgray", textvariable=self.needed_exp)
		self.needed_exp_label.grid(row=0, column=5, padx="1")
		self.needed_exp_label.bind("<MouseWheel>", globals.panels["Post Cap"].Scroll_Build_Frame)
		self.ending_exp_label = tkinter.Label(self.PcP_Build_Row, width=10, bg="lightgray", textvariable=self.ending_exp)
		self.ending_exp_label.grid(row=0, column=6, padx="1")
		self.ending_exp_label.bind("<MouseWheel>", globals.panels["Post Cap"].Scroll_Build_Frame)
		self.PcP_Edit_Button = tkinter.Button(self.PcP_Build_Row, text="Edit", command="")
		self.PcP_Edit_Button.grid(row=0, column=7, padx="3")		

		self.Calculate_Total_Cost()

	# Calculates out how much exp will be needed to train "goal" amount of ranks.		
	def Calculate_Total_Cost(self):
		total = 0
		num = int(self.goal.get())
		
		for i in range(num):
			total += int(self.ranks[i].get())
			
		self.cost.set(total)
		self.needed_exp.set("")
		self.ending_exp.set("")

	# Clicking either the need_exp or ending_exp label of this object will "jump" the exp_counter to that experience number
	def PcP_Row_Label_Onclick(self, event, val):
		globals.panels["Post Cap"].experience_counter.setvalue(val)		
