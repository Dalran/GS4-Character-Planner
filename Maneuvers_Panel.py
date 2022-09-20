# TODO LIST
# convert most optionmenu objects from tkinter to tkinter.ttk

# INDEX OF CLASSES AND METHODS
'''
class Maneuvers_Panel
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
	def Maneuver_Style_Onchange(self, result):	
	def Plan_Training_Schedule(self):	
	def Update_Schedule_Frames(self):	
	def Scroll_Build_Frame(self, event):	
	def Scroll_Schedule_Frame(self, event):
	def Create_Build_List_Maneuver(self, parent, name, type, hidden, order, start, target, goal, ranks_arr ):
	
class Build_List_Maneuver:
	def __init__(self, parent, name, type, hidden, order, start, target, goal, ranks_arr ):
'''

#!/usr/bin/python

import tkinter
import tkinter.ttk
import re
import math
import Pmw
import Globals as globals
  
  
# Maneuvers panel is responsible for handling character combat, shield, and armor maneuver training from level 0 to 100.
# This panel is made of 5 sub frames. 
#  Build buttons (Upper Left) - Contains buttons that add new maneuvers to the build list, calculate out a build, or reset the build list. A drop down menu is used to switch between combat, shield, and armor styles.
#  Build skill list (Middle/Lower Left) - Contains a list of maneuvers that user wants to train in. Changing the maneuver style (UL frame), will change what kind of maneuvers are shown here.
#  Schedule buttons (Upper Right) - These button can alter how the Schedule maneuver list looks
#  Scheduled skills list (Middle Right) - This list every maneuver available to the character along with rank cost information.
#  Scheduled footer (Lower Right) - The totals and training point costs are calculated here
class Maneuvers_Panel:  
	def __init__(self, panel):	
		self.ManP_radio_var = tkinter.IntVar()	
		self.maneuver_mode = tkinter.StringVar()
		self.man_select_menu = ""
		
		# Dialog Box vars
		self.dialog_armor_names_menu = ""
		self.dialog_combat_names_menu = ""
		self.dialog_shield_names_menu = ""
		self.add_armor_order_menu = ""
		self.add_combat_order_menu = ""
		self.add_shield_order_menu = ""
		self.edit_armor_order_menu = ""
		self.edit_combat_order_menu = ""
		self.edit_shield_order_menu = ""
		self.armor_menu_size = 1			
		self.combat_menu_size = 1			
		self.shield_menu_size = 1		
		self.vars_dialog_combat_maneuver = tkinter.StringVar()
		self.vars_dialog_shield_maneuver = tkinter.StringVar()
		self.vars_dialog_armor_maneuver = tkinter.StringVar()
		self.vars_dialog_order = tkinter.StringVar()
		self.vars_dialog_info = tkinter.StringVar()
		self.vars_dialog_prerequisites = tkinter.StringVar()
		self.vars_dialog_hide = tkinter.StringVar()
		self.vars_dialog_goal = tkinter.StringVar()
		self.vars_dialog_slevel = tkinter.StringVar()
		self.vars_dialog_tlevel = tkinter.StringVar()
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
		self.sfooter_shield_row = ""
		self.sfooter_armor_row = ""
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
			
		self.dialog_box = self.Create_Dialog_Box(panel, "Add Maneuver", ("Add Maneuver,Cancel"))	
		
		self.level_counter = ""    									 #Becomes a Pmw.counter later on
					
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
		
		# Create the maneuver lists using all the maneuvers from the database. 	
		globals.db_cur.execute("SELECT * FROM Maneuvers")
		globals.db_con.commit()		
		data = globals.db_cur.fetchall()		
		for man in data:
			if man[2] == "combat":
				globals.combat_maneuver_names.append(man[0])		
				globals.character.combat_maneuvers_list[man[0]] = globals.Maneuver(self.MR_Frame.interior(), man)
			elif man[2] == "shield":
				globals.shield_maneuver_names.append(man[0])		
				globals.character.shield_maneuvers_list[man[0]] = globals.Maneuver(self.MR_Frame.interior(), man)
			elif man[2] == "armor":
				globals.armor_maneuver_names.append(man[0])		
				globals.character.armor_maneuvers_list[man[0]] = globals.Maneuver(self.MR_Frame.interior(), man)
		
		#initialize defaults
		self.ML_Frame.bind_class("ManP_build", "<MouseWheel>", self.Scroll_Build_Frame)
		self.MR_Frame.bind_class("ManP_schedule", "<MouseWheel>", self.Scroll_Schedule_Frame)
		self.dialog_box.withdraw()
		self.ManP_radio_var.set(1)
		self.level_counter.setvalue(0)
							

	# The build header contains the the buttons to calculate or reset a build.
	# It also contains a drop down menu to change the maneuver style between Combat, Shield, and Armor
	def Create_Build_Header(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 600, hull_height = 50)
		myframe.component("borderframe").config(borderwidth=0)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")	
		myframe_inner = myframe.interior()

		topframe = tkinter.Frame(myframe_inner)		
		topframe.grid(row=0, column=0, sticky="w")	
		choices = ["Combat", "Shield", "Armor"]
		self.man_select_menu = tkinter.OptionMenu(topframe, self.maneuver_mode, *choices, command=self.Maneuver_Style_Onchange)
		self.man_select_menu.config(width=6, height=1)	
		self.man_select_menu.grid(row=0, column=0, sticky="w")		
		tkinter.Button(topframe, height="1", text="Add Maneuver", command=lambda v="": self.Add_Edit_Button_Onclick(v)).grid(row=0, column=1)		
		tkinter.Button(topframe, height="1", text="Calculate Build", command=lambda : self.Plan_Training_Schedule(self.maneuver_mode.get())).grid(row=0, column=2)		
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
		tkinter.Label(title_scrollframe_inner, width="26", bg="lightgray", text="Maneuver Name").grid(row=0, column=2, padx="1")
		tkinter.Label(title_scrollframe_inner, width="19", bg="lightgray", text="Cost by Rank").grid(row=0, column=3, padx="3")
		tkinter.Label(title_scrollframe_inner, width="5", bg="lightgray", text="Goal").grid(row=0, column=4, padx="1")
		tkinter.Label(title_scrollframe_inner, width="5", bg="lightgray", text="S.lvl").grid(row=0, column=5, padx="1")
		tkinter.Label(title_scrollframe_inner, width="5", bg="lightgray", text="T.lvl").grid(row=0, column=6, padx="1")
		tkinter.Label(title_scrollframe_inner, width="4", bg="lightgray", text="Edit").grid(row=0, column=7, padx="1")
		
		return myframe
		
		
	# All Build Maneuver objects are displayed in this panel. This panel is populated using the Dialog box Add and Update functions.
	# Only one type of maneuver is shown in this panel at a time. The style can be changed with the drop down menu in the Build Header panel.
	def Create_Build_Frame(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 600, hull_height = 474)			
		myframe.configure(hscrollmode = "none", vscrollmode = "static")					
		
		return myframe			
	
	
	# This frame contains:
	#  PMW counter object that is used to change what level the schedule frame is displaying
	#  3 radio buttons that change what maneuvers will appear in the schedule frame
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
		self.level_counter = Pmw.Counter(tlvl_frame, entryfield_entry_width = 3, entryfield_validate = { 'validator':'numeric', 'min':0, 'max':100 }, labelpos = 'w', label_text = 'Manevuers at Level', entryfield_value = 0, datatype = "numeric", entryfield_modifiedcommand=self.Update_Schedule_Frames )
		self.level_counter.grid(row=0, column=0, sticky="w", pady="1")
		
		tkinter.Radiobutton(topframe, anchor="w", text="All", command=self.Update_Schedule_Frames, var=self.ManP_radio_var, value=1).grid(row=0, column=1)	
		tkinter.Radiobutton(topframe, anchor="w", text="All Trained", command=self.Update_Schedule_Frames, var=self.ManP_radio_var, value=2).grid(row=0, column=2)		
		tkinter.Radiobutton(topframe, anchor="w", text="Trained this Level", command=self.Update_Schedule_Frames, var=self.ManP_radio_var, value=3).grid(row=0, column=3)

		title_scrollframe = Pmw.ScrolledFrame(myframe_inner, usehullsize = 1, hull_width = 450, hull_height = 28 )		
		title_scrollframe.configure(hscrollmode = "none")		
		title_scrollframe.grid(row=3, column=0, sticky="w")	
		title_scrollframe_inner = title_scrollframe.interior()							
		
		tkinter.Frame(title_scrollframe_inner).grid(row=1, column=2, sticky="w", pady="1")	
		tkinter.Label(title_scrollframe_inner, width="26", bg="lightgray", text="Maneuver Name").grid(row=0, column=0, padx="1")
		tkinter.Label(title_scrollframe_inner, width="8", bg="lightgray", text="Ranks").grid(row=0, column=1, padx="1")
		tkinter.Label(title_scrollframe_inner, width="6", bg="lightgray", text="Cost").grid(row=0, column=2, padx="1")
		tkinter.Label(title_scrollframe_inner, width="10", bg="lightgray", text="Total Ranks").grid(row=0, column=3, padx="1")
		tkinter.Label(title_scrollframe_inner, width="8", bg="lightgray", text="Sum Cost").grid(row=0, column=4, padx="1")
	
		return myframe		
		
		
	# This frame will hold ManP_schedule_row objects for maneuvers the character can train in. For more information, please see the Maneuver class in Globals.py
	# Only one type of maneuver is shown in this panel at a time. The style can be changed with the drop down menu in the Build Header panel.
	def Create_Schedule_Frame(self, panel):
		self.training_middle_scrollframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 470, hull_height = 372)		
		self.training_middle_scrollframe_inner = self.training_middle_scrollframe.interior()
		self.training_middle_scrollframe.configure(hscrollmode = "none")		
	
		return self.training_middle_scrollframe		
	

	# This frame contains information about combat, shield, and armor training points for each level for the current level. 
	# Every profession will see the Combat maneuver row but only Rogues, Warriors, and Paladins will see the Shield and Armor rows.
	# Every maneuver row contains:
	# Earned - How many training points where gained this level for training in the appropriate skill. "Armor Use", "Combat Maneuvers", "Shield Use"
	# Available - Earned training points + Leftover training points.
	# Total Cost - Sum of all training costs from maneuvers trained this level.
	# Leftover - Available training points - Total Cost .
	def Create_Schedule_Footer(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 470, hull_height = 100)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")			
		myframe_inner = myframe.interior()									
		
		title_frame = tkinter.Frame(myframe_inner)
		self.sfooter_combat_row = tkinter.Frame(myframe_inner)	
		self.sfooter_shield_row = tkinter.Frame(myframe_inner)	
		self.sfooter_armor_row = tkinter.Frame(myframe_inner)	
		
		title_frame.grid(row=0, column=0, padx="1")	
		self.sfooter_combat_row.grid(row=1, column=0, padx="1")		
		self.sfooter_shield_row.grid(row=2, column=0, padx="1")		
		self.sfooter_armor_row.grid(row=3, column=0, padx="1")			
		
		tkinter.Label(title_frame, width=8, text="").grid(row=0, column=0, sticky="w", padx="1", pady="1")	
		tkinter.Label(title_frame, width="10", bg="lightgray", text="Earned").grid(row=0, column=1, padx="1")
		tkinter.Label(title_frame, width="10", bg="lightgray", text="Available").grid(row=0, column=2, padx="1")
		tkinter.Label(title_frame, width="10", bg="lightgray", text="Total Cost").grid(row=0, column=3, padx="1")
		tkinter.Label(title_frame, width="10", bg="lightgray", text="Leftover").grid(row=0, column=4, padx="1")
	
		tkinter.Label(self.sfooter_combat_row, width="8", bg="lightgray", text="Combat").grid(row=1, column=0, padx="2", pady="1")
		tkinter.Label(self.sfooter_combat_row, width="10", bg="lightgray", textvar=self.vars_sfooter_combat_earned).grid(row=1, column=1, padx="1")
		tkinter.Label(self.sfooter_combat_row, width="10", bg="lightgray", textvar=self.vars_sfooter_combat_available).grid(row=1, column=2, padx="1")	
		tkinter.Label(self.sfooter_combat_row, width="10", bg="lightgray", textvar=self.vars_sfooter_combat_total_cost).grid(row=1, column=3, padx="1")
		tkinter.Label(self.sfooter_combat_row, width="10", bg="lightgray", textvar=self.vars_sfooter_combat_leftover).grid(row=1, column=4, padx="1")
		
		tkinter.Label(self.sfooter_shield_row, width="8", bg="lightgray", text="Shield").grid(row=2, column=0, padx="2", pady="1")	
		tkinter.Label(self.sfooter_shield_row, width="10", bg="lightgray", textvar=self.vars_sfooter_shield_earned).grid(row=2, column=1, padx="1")	
		tkinter.Label(self.sfooter_shield_row, width="10", bg="lightgray", textvar=self.vars_sfooter_shield_available).grid(row=2, column=2, padx="1")
		tkinter.Label(self.sfooter_shield_row, width="10", bg="lightgray", textvar=self.vars_sfooter_shield_total_cost).grid(row=2, column=3, padx="1")		
		tkinter.Label(self.sfooter_shield_row, width="10", bg="lightgray", textvar=self.vars_sfooter_shield_leftover).grid(row=2, column=4, padx="1")	
		
		tkinter.Label(self.sfooter_armor_row, width="8", bg="lightgray", text="Armor").grid(row=3, column=0, padx="2", pady="1")			
		tkinter.Label(self.sfooter_armor_row, width="10", bg="lightgray", textvar=self.vars_sfooter_armor_earned).grid(row=3, column=1, padx="1")	
		tkinter.Label(self.sfooter_armor_row, width="10", bg="lightgray", textvar=self.vars_sfooter_armor_available).grid(row=3, column=2, padx="1")
		tkinter.Label(self.sfooter_armor_row, width="10", bg="lightgray", textvar=self.vars_sfooter_armor_total_cost).grid(row=3, column=3, padx="1")
		tkinter.Label(self.sfooter_armor_row, width="10", bg="lightgray", textvar=self.vars_sfooter_armor_leftover).grid(row=3, column=4, padx="1")	
					
		return myframe	
	
	
	# The popup dialog box is used to allow add a maneuver or edit an existing maneuver in the build frame. The type of maneuver that will be added is determined by the drop down menu in the Build Header frame.
	# This frame consists of the following parts:
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
				
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Maneuver Name").grid(row=0, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Cost per Rank").grid(row=1, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="30", anchor="w", textvar=self.vars_dialog_info).grid(row=1, column=1, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Prerequisites").grid(row=2, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="30", anchor="w", justify="left", textvar=self.vars_dialog_prerequisites).grid(row=2, column=1, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", text="").grid(row=3, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Training Order").grid(row=4, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Hide").grid(row=5, column=0, sticky="w")
		tkinter.Checkbutton(myframe_inner, command="", variable=self.vars_dialog_hide).grid(row=5, column=1, sticky="w")	
		tkinter.Label(myframe_inner, width="13", anchor="w", text="").grid(row=6, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Goal").grid(row=7, column=0, sticky="w", pady=1)
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Level Range").grid(row=8, column=0, sticky="w")			
									
	

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
		
		self.add_combat_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.edit_combat_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.add_shield_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.edit_shield_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.add_armor_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))
		self.edit_armor_order_menu["menu"].insert_command("end", label=1, command=lambda v=1: self.vars_dialog_order.set(v))			
			
		self.add_combat_order_menu.grid(row=4, column=1, sticky="w")
		self.dialog_combat_names_menu.grid(row=0, column=1, sticky="w", columnspan=4)	

		goal_box = tkinter.Entry(myframe_inner, width="6", justify="center", validate="key", validatecommand="", textvariable=self.vars_dialog_goal).grid(row=7, column=1, sticky="w", padx=2)				
		
		lvlframe = tkinter.Frame(myframe_inner)
		lvlframe.grid(row=8, column=1, sticky="w", columnspan=4)	
		Pmw.Counter(lvlframe, entryfield_entry_width = 3, entryfield_validate = { 'validator':'numeric', 'min':0, 'max':100 }, labelpos = 'w', label_text = 'Start', entryfield_value = 0, datatype = "numeric", entryfield_entry_textvariable=self.vars_dialog_slevel).grid(row=0, column=0, sticky="w")
		Pmw.Counter(lvlframe, entryfield_entry_width = 3, entryfield_validate = { 'validator':'numeric', 'min':0, 'max':100 }, labelpos = 'w', label_text = 'Target', entryfield_value = 0, datatype = "numeric", entryfield_entry_textvariable=self.vars_dialog_tlevel).grid(row=0, column=1, sticky="w", columnspan=2)

		tkinter.Label(myframe_inner, anchor="w", font="-weight bold", wraplength=300, justify="left", textvariable=self.vars_dialog_errormsg).grid(row=9, column=0, sticky="w", columnspan=4)
							
		return dialog

		
	# This handles button all the button events that occur in the Add/Edit dialog box.	
	def Dialog_Box_Onclick(self, result):
		i = 0
		slevel = int(self.vars_dialog_slevel.get())
		tlevel = int(self.vars_dialog_tlevel.get())
		goal = self.vars_dialog_goal.get()

		if result is None or result == "Cancel":
			self.dialog_box.withdraw()
			self.dialog_box.grab_release()
			return

		# The maneuver used is determined by current maneuver mode (style)
		if self.maneuver_mode.get() == "Combat":
			man = globals.character.combat_maneuvers_list[self.vars_dialog_combat_maneuver.get()]
		elif self.maneuver_mode.get() == "Shield":
			man = globals.character.shield_maneuvers_list[self.vars_dialog_shield_maneuver.get()]
		elif self.maneuver_mode.get() == "Armor":
			man = globals.character.armor_maneuvers_list[self.vars_dialog_armor_maneuver.get()]
	
		# Error checking for Add/Update choices
		if re.search(r"(^Add)|(^Update)", result):
			if slevel > tlevel:
				self.vars_dialog_errormsg.set("ERROR: Start level cannot be greater than target level." )
				return
			elif len(goal) == 0 or goal == "0" or not re.search(r"(^\d{1,3}$)", goal):
				self.vars_dialog_errormsg.set("ERROR: Goal must be number greater than 0 and less than 6.")
				return				
			elif int(goal) > man.max_ranks:
				self.vars_dialog_errormsg.set("ERROR: Goal is greater than maximum maneuver ranks.")
				return				
			elif man.Get_Total_Cost_At_Rank(0, int(goal)) > tlevel+1 and man.type == "combat":
				self.vars_dialog_errormsg.set("ERROR: Combat Manevuer total cost cannot be greater than target level + 1.")
				return					

		# Add a new maneuver to the appropriate build list		
		if result == "Add Maneuver":	
			hide = "" 
			if self.vars_dialog_hide.get() == "1":
				hide = "x"				
				
			if self.maneuver_mode.get() == "Combat":
				man = globals.character.combat_maneuvers_list[self.vars_dialog_combat_maneuver.get()]
				self.combat_menu_size += 1			
				
				globals.character.build_combat_maneuvers_list.insert(int(self.vars_dialog_order.get())-1, Build_List_Maneuver(self.ML_Frame.interior(), self.vars_dialog_combat_maneuver.get(), 
				"Combat", hide, self.vars_dialog_order.get(), self.vars_dialog_slevel.get(), self.vars_dialog_tlevel.get(), self.vars_dialog_goal.get(),
				(man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ))	
				
				globals.character.build_combat_maneuvers_list[int(self.vars_dialog_order.get())-1].ManP_Edit_Button.config(command=lambda v=int(self.vars_dialog_order.get())-1: self.Add_Edit_Button_Onclick(v))
			
				self.add_combat_order_menu["menu"].insert_command("end", label=self.combat_menu_size, command=lambda v=self.combat_menu_size: self.vars_dialog_order.set(v))	
				if self.combat_menu_size-1 > 1:
					self.edit_combat_order_menu["menu"].insert_command("end", label=self.combat_menu_size-1, command=lambda v=self.combat_menu_size-1: self.vars_dialog_order.set(v))		
			
				for man in globals.character.build_combat_maneuvers_list:
					man.order.set(i+1)
					man.ManP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
					man.ManP_Build_Row.grid(row=i, column=0)			
					i += 1	
				
			elif self.maneuver_mode.get() == "Shield":
				man = globals.character.shield_maneuvers_list[self.vars_dialog_shield_maneuver.get()]
				self.shield_menu_size = self.shield_menu_size + 1				
				
				globals.character.build_shield_maneuvers_list.insert(int(self.vars_dialog_order.get())-1, Build_List_Maneuver(self.ML_Frame.interior(), self.vars_dialog_shield_maneuver.get(), 
				"Shield", hide, self.vars_dialog_order.get(), self.vars_dialog_slevel.get(), self.vars_dialog_tlevel.get(), self.vars_dialog_goal.get(),
				(man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ))
				
				globals.character.build_shield_maneuvers_list[int(self.vars_dialog_order.get())-1].ManP_Edit_Button.config(command=lambda v=int(self.vars_dialog_order.get())-1: self.Add_Edit_Button_Onclick(v))
			
				self.add_shield_order_menu["menu"].insert_command("end", label=self.shield_menu_size, command=lambda v=self.shield_menu_size: self.vars_dialog_order.set(v))	
				if self.shield_menu_size-1 > 1:
					self.edit_shield_order_menu["menu"].insert_command("end", label=self.shield_menu_size-1, command=lambda v=self.shield_menu_size-1: self.vars_dialog_order.set(v))		
			
				for man in globals.character.build_shield_maneuvers_list:
					man.order.set(i+1)
					man.ManP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
					man.ManP_Build_Row.grid(row=i, column=0)			
					i += 1	
					
			elif self.maneuver_mode.get() == "Armor":
				man = globals.character.armor_maneuvers_list[self.vars_dialog_armor_maneuver.get()]
				self.armor_menu_size = self.armor_menu_size + 1			
				
				globals.character.build_armor_maneuvers_list.insert(int(self.vars_dialog_order.get())-1, Build_List_Maneuver(self.ML_Frame.interior(), self.vars_dialog_armor_maneuver.get(), 
				"Armor", hide, self.vars_dialog_order.get(), self.vars_dialog_slevel.get(), self.vars_dialog_tlevel.get(), self.vars_dialog_goal.get(), 
				(man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ))	
				
				globals.character.build_armor_maneuvers_list[int(self.vars_dialog_order.get())-1].ManP_Edit_Button.config(command=lambda v=int(self.vars_dialog_order.get())-1: self.Add_Edit_Button_Onclick(v))
			
				self.add_armor_order_menu["menu"].insert_command("end", label=self.armor_menu_size, command=lambda v=self.armor_menu_size: self.vars_dialog_order.set(v))	
				if self.armor_menu_size-1 > 1:
					self.edit_armor_order_menu["menu"].insert_command("end", label=self.armor_menu_size-1, command=lambda v=self.armor_menu_size-1: self.vars_dialog_order.set(v))			
			
				for man in globals.character.build_armor_maneuvers_list:
					man.order.set(i+1)
					man.ManP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
					man.ManP_Build_Row.grid(row=i, column=0)			
					i += 1		

			self.dialog_box.withdraw()	
			self.dialog_box.grab_release()	
		
		# Change the information for an existing maneuver
		elif result == "Update Maneuver":
			if self.maneuver_mode.get() == "Combat":
				man = globals.character.build_combat_maneuvers_list.pop(self.vars_dialog_edit_location.get())
				list = globals.character.build_combat_maneuvers_list
				man.name.set(self.vars_dialog_combat_maneuver.get())
				m_ranks = globals.character.combat_maneuvers_list[self.vars_dialog_combat_maneuver.get()]
			elif self.maneuver_mode.get() == "Shield":
				man = globals.character.build_shield_maneuvers_list.pop(self.vars_dialog_edit_location.get())
				list = globals.character.build_shield_maneuvers_list
				man.name.set(self.vars_dialog_shield_maneuver.get())
				m_ranks = globals.character.shield_maneuvers_list[self.vars_dialog_shield_maneuver.get()]
			elif self.maneuver_mode.get() == "Armor":
				man = globals.character.build_armor_maneuvers_list.pop(self.vars_dialog_edit_location.get())
				list = globals.character.build_armor_maneuvers_list
				man.name.set(self.vars_dialog_armor_maneuver.get())		
				m_ranks = globals.character.armor_maneuvers_list[self.vars_dialog_armor_maneuver.get()]

			man.ranks[0].set(m_ranks.cost_by_rank[0])	
			man.ranks[1].set(m_ranks.cost_by_rank[1])	
			man.ranks[2].set(m_ranks.cost_by_rank[2])	
			man.ranks[3].set(m_ranks.cost_by_rank[3])	
			man.ranks[4].set(m_ranks.cost_by_rank[4])	
			man.order.set(self.vars_dialog_order.get())
			man.slvl.set(self.vars_dialog_slevel.get())
			man.tlvl.set(self.vars_dialog_tlevel.get())
			man.goal.set(self.vars_dialog_goal.get())			
			
			if self.vars_dialog_hide.get() == "1":
				man.hide.set("x")
			else:
				man.hide.set("")			
			
			list.insert(int(self.vars_dialog_order.get())-1, man)
			for man in list:	
				man.order.set(i+1)
				man.ManP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				man.ManP_Build_Row.grid(row=i, column=0)			
				i += 1						
			self.dialog_box.withdraw()	
			self.dialog_box.grab_release()			
		
		elif result == "Remove Maneuver":
			if self.maneuver_mode.get() == "Combat":
				list = globals.character.build_combat_maneuvers_list
				self.add_combat_order_menu['menu'].delete("end", "end")
				self.edit_combat_order_menu['menu'].delete("end", "end")
				self.combat_menu_size -= 1
			elif self.maneuver_mode.get() == "Shield":
				list = globals.character.build_shield_maneuvers_list
				self.add_shield_order_menu['menu'].delete("end", "end")
				self.edit_shield_order_menu['menu'].delete("end", "end")
				self.shield_menu_size -= 1
			elif self.maneuver_mode.get() == "Armor":
				list = globals.character.build_armor_maneuvers_list
				self.add_armor_order_menu['menu'].delete("end", "end")
				self.edit_armor_order_menu['menu'].delete("end", "end")
				self.armor_menu_size -= 1				
				
			list.pop(self.vars_dialog_edit_location.get()).ManP_Build_Row.grid_remove()
			for man in list:
				man.order.set(i+1)
				man.ManP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				man.ManP_Build_Row.grid(row=i, column=0)			
				i += 1	
			self.dialog_box.withdraw()		
			self.dialog_box.grab_release()
				
	
	# When a new maneuver is clicked from the maneuver drop down menu in the popup dialog box, this method will update the dialog box with the newly chosen maneuver
	def Dialog_Menu_Onchange(self, name):

	
		if self.maneuver_mode.get() == "Combat":
			man = globals.character.combat_maneuvers_list[name]
			self.vars_dialog_combat_maneuver.set(name)				
		elif self.maneuver_mode.get() == "Shield":
			man = globals.character.shield_maneuvers_list[name]
			self.vars_dialog_shield_maneuver.set(name)				
		elif self.maneuver_mode.get() == "Armor":
			man = globals.character.armor_maneuvers_list[name]
			self.vars_dialog_armor_maneuver.set(name)		
			
		self.vars_dialog_prerequisites.set(man.prerequisites_displayed)	
		self.vars_dialog_info.set("%s,    %s,    %s,    %s,    %s" % (man.Get_Cost_At_Rank(1), man.Get_Cost_At_Rank(2), man.Get_Cost_At_Rank(3), man.Get_Cost_At_Rank(4), man.Get_Cost_At_Rank(5)))		
		
	
	# This function is called to display the popup dialog box that allows a user to add a new meneuver or edit an existing meneuver.
	# Clicking the Add Maneuver button in the Build Header frame will show the Add version of this box
	# Clicking an existing Maneuver's Edit button will show the Edit version of this box	
	def Add_Edit_Button_Onclick(self, location):

		self.dialog_combat_names_menu.grid_remove()
		self.dialog_shield_names_menu.grid_remove()
		self.dialog_armor_names_menu.grid_remove()
		self.add_combat_order_menu.grid_remove()
		self.add_shield_order_menu.grid_remove()
		self.add_armor_order_menu.grid_remove()
		self.edit_combat_order_menu.grid_remove()
		self.edit_shield_order_menu.grid_remove()
		self.edit_armor_order_menu.grid_remove()
				
		if self.maneuver_mode.get() == "Combat":
			char_man = globals.character.combat_maneuvers_list[self.dialog_combat_names_menu['menu'].entrycget(0, "label")]
			self.dialog_combat_names_menu.grid(row=0, column=1, sticky="w", columnspan=4)	
			self.vars_dialog_order.set(self.combat_menu_size)	
			if location == "":			
				self.vars_dialog_combat_maneuver.set(char_man.name)
				self.add_combat_order_menu.grid(row=4, column=1, sticky="w")	
			else:
				man = globals.character.build_combat_maneuvers_list[int(location)]
				char_man = globals.character.combat_maneuvers_list[man.name.get()]
				self.vars_dialog_combat_maneuver.set(man.name.get())
				self.edit_combat_order_menu.grid(row=4, column=1, sticky="w")			
		elif self.maneuver_mode.get() == "Shield":
			char_man = globals.character.shield_maneuvers_list[self.dialog_shield_names_menu['menu'].entrycget(0, "label")]	
			self.dialog_shield_names_menu.grid(row=0, column=1, sticky="w", columnspan=4)	
			self.vars_dialog_order.set(self.shield_menu_size)
			if location == "":			
				self.vars_dialog_shield_maneuver.set(char_man.name)
				self.add_shield_order_menu.grid(row=4, column=1, sticky="w")		
			else:
				man = globals.character.build_shield_maneuvers_list[int(location)]
				char_man = globals.character.shield_maneuvers_list[man.name.get()]
				self.vars_dialog_shield_maneuver.set(man.name.get())		
				self.edit_shield_order_menu.grid(row=4, column=1, sticky="w")					
		elif self.maneuver_mode.get() == "Armor":
			char_man = globals.character.armor_maneuvers_list[self.dialog_armor_names_menu['menu'].entrycget(0, "label")]
			self.dialog_armor_names_menu.grid(row=0, column=1, sticky="w", columnspan=4)	
			self.vars_dialog_order.set(self.armor_menu_size)
			if location == "":			
				self.vars_dialog_armor_maneuver.set(char_man.name)
				self.add_armor_order_menu.grid(row=4, column=1, sticky="w")		
			else:
				man = globals.character.build_armor_maneuvers_list[int(location)]
				char_man = globals.character.armor_maneuvers_list[man.name.get()]
				self.vars_dialog_armor_maneuver.set(man.name.get())		
				self.edit_armor_order_menu.grid(row=4, column=1, sticky="w")		

		# Location determines if this is the Add or Edit version of this box. A lack of Location means it is the Add version.
		# Location is used as a reference for what number frame called this function. IE: Location 4 is the 4th maneuver in the build list.
		if location == "":
			self.vars_dialog_hide.set("0")
			self.vars_dialog_goal.set("")
			self.vars_dialog_slevel.set("0")
			self.vars_dialog_tlevel.set("100")	
			self.vars_dialog_errormsg.set("")
			if self.dialog_box.component("buttonbox").button(0)["text"] == "Update Maneuver":
				self.dialog_box.component("buttonbox").delete("Update Maneuver")
				self.dialog_box.component("buttonbox").delete("Remove Maneuver")		
				self.dialog_box.component("buttonbox").insert("Add Maneuver", command=lambda v="Add Maneuver": self.Dialog_Box_Onclick(v))	
		else:
			self.vars_dialog_order.set(man.order.get())
			self.vars_dialog_slevel.set(man.slvl.get())
			self.vars_dialog_tlevel.set(man.tlvl.get())
			self.vars_dialog_goal.set(man.goal.get())		
			self.vars_dialog_errormsg.set("")
			self.vars_dialog_edit_location.set(int(location))
			
			if man.hide.get() == "x":
				self.vars_dialog_hide.set("1")	
			else:
				self.vars_dialog_hide.set("0")		
				
			if self.dialog_box.component("buttonbox").button(0)["text"] == "Add Maneuver":
				self.dialog_box.component("buttonbox").delete("Add Maneuver")
				self.dialog_box.component("buttonbox").insert("Remove Maneuver", command=lambda v="Remove Maneuver": self.Dialog_Box_Onclick(v))	
				self.dialog_box.component("buttonbox").insert("Update Maneuver", command=lambda v="Update Maneuver": self.Dialog_Box_Onclick(v))	
			
		self.vars_dialog_prerequisites.set(char_man.prerequisites_displayed)	
		self.vars_dialog_info.set("%s,    %s,    %s,    %s,    %s" % (char_man.Get_Cost_At_Rank(1), char_man.Get_Cost_At_Rank(2), char_man.Get_Cost_At_Rank(3), char_man.Get_Cost_At_Rank(4), char_man.Get_Cost_At_Rank(5) ))		
		self.dialog_box.show()
		self.dialog_box.grab_set()
		
		
	# When the Clear All button is clicked, the build_maneuver_lists are emptied, all training point totals lists are reset, the menu sizes are set to 1 and level counter set back to 0
	def Clear_Button_Onclick(self, style):		
		if self.maneuver_mode.get() == "Combat" or style == "All":
			for key, row in globals.character.combat_maneuvers_list.items():
				row.Set_To_Default()
			for man in globals.character.build_combat_maneuvers_list:	
				man.ManP_Build_Row.grid_remove()
			if self.combat_menu_size > 1:			
				self.add_combat_order_menu['menu'].delete(1, "end")
				menu = [1]
				self.edit_combat_order_menu.set_menu(1, *menu)
				self.combat_menu_size = 1		
			globals.character.build_combat_maneuvers_list = []	
			self.total_available_combat_points_by_level = [tkinter.IntVar() for i in range(101)]
			self.total_cost_combat_points_by_level = [tkinter.IntVar() for i in range(101)]
			self.total_leftover_combat_points_by_level = [tkinter.IntVar() for i in range(101)]
			
		if self.maneuver_mode.get() == "Shield" or style == "All":		
			for key, row in globals.character.shield_maneuvers_list.items():
				row.Set_To_Default()		
			for man in globals.character.build_shield_maneuvers_list:	
				man.ManP_Build_Row.grid_remove()
			if self.shield_menu_size > 1:	
				self.add_shield_order_menu['menu'].delete(1, "end")
				menu = [1]
				self.edit_shield_order_menu.set_menu(1, *menu)
				self.shield_menu_size = 1		
			globals.character.build_shield_maneuvers_list = []	
			self.total_available_shield_points_by_level = [tkinter.IntVar() for i in range(101)]
			self.total_cost_shield_points_by_level = [tkinter.IntVar() for i in range(101)]
			self.total_leftover_shield_points_by_level = [tkinter.IntVar() for i in range(101)]
			
		if self.maneuver_mode.get() == "Armor" or style == "All":		
			for key, row in  globals.character.armor_maneuvers_list.items():
				row.Set_To_Default()				
			for man in globals.character.build_armor_maneuvers_list:	
				man.ManP_Build_Row.grid_remove()		
			if self.armor_menu_size > 1:				
				self.add_armor_order_menu['menu'].delete(1, "end")
				menu = [1]
				self.edit_armor_order_menu.set_menu(1, *menu)

				self.armor_menu_size = 1	
			globals.character.build_armor_maneuvers_list = []
			self.total_available_armor_points_by_level = [tkinter.IntVar() for i in range(101)]
			self.total_cost_armor_points_by_level = [tkinter.IntVar() for i in range(101)]
			self.total_leftover_armor_points_by_level = [tkinter.IntVar() for i in range(101)]

		self.ManP_radio_var.set(1)
		self.level_counter.setvalue(0)
		if style == "All" and self.maneuver_mode.get() != "Combat":
			self.Maneuver_Style_Onchange("Combat")
		else:
			self.Update_Schedule_Frames()

		
	# This method is called when the drop down menu in the build header is changed to a new value. Changing the value will swap out the current build list and schedule list values for either Combat, Shield, or Armor maneuver values.
	def Maneuver_Style_Onchange(self, result):
		i=0
		current_schedule = ""
		current_keys = ""
		
		if self.maneuver_mode.get() == result:
			return			
								
		if self.maneuver_mode.get() == "Combat":
			self.maneuver_mode.set("Combat")
			for man in globals.character.build_combat_maneuvers_list:
				man.ManP_Build_Row.grid_remove()
			for key, man in globals.character.combat_maneuvers_list.items():
				man.ManP_schedule_row.grid_remove()
		elif self.maneuver_mode.get() == "Shield":
			self.maneuver_mode.set("Shield")
			for man in globals.character.build_shield_maneuvers_list:	
				man.ManP_Build_Row.grid_remove()
			for key, man in globals.character.shield_maneuvers_list.items():
				man.ManP_schedule_row.grid_remove()
		elif self.maneuver_mode.get() == "Armor":
			self.maneuver_mode.set("Armor") 
			for man in globals.character.build_armor_maneuvers_list:	
				man.ManP_Build_Row.grid_remove()
			for key, man in globals.character.armor_maneuvers_list.items():
				man.ManP_schedule_row.grid_remove()
		
		if result == "Combat":
			self.maneuver_mode.set("Combat")	
			current_schedule = globals.character.combat_maneuvers_list
			current_keys = globals.combat_maneuver_names
			
			for man in globals.character.build_combat_maneuvers_list:	
				man.order.set(i+1)
				man.ManP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				man.ManP_Build_Row.grid(row=i, column=0)			
				i += 1	
		elif result == "Shield":
			self.maneuver_mode.set("Shield")
			current_schedule = globals.character.shield_maneuvers_list
			current_keys = globals.shield_maneuver_names
			
			for man in globals.character.build_shield_maneuvers_list:	
				man.order.set(i+1)
				man.ManP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				man.ManP_Build_Row.grid(row=i, column=0)		
				i += 1	
		elif result == "Armor":
			self.maneuver_mode.set("Armor") 
			current_schedule = globals.character.armor_maneuvers_list
			current_keys = globals.armor_maneuver_names
			
			for man in globals.character.build_armor_maneuvers_list:	
				man.order.set(i+1)
				man.ManP_Edit_Button.config(command=lambda v=i: self.Add_Edit_Button_Onclick(v))
				man.ManP_Build_Row.grid(row=i, column=0)	
				i += 1	
				
		self.ML_Frame.yview("moveto", 0, "units")
		self.MR_Frame.yview("moveto", 0, "units")		
		self.Update_Schedule_Frames()	
		

	# When the Calculate button is pushed the planner will map out level by level, maneuver by maneuver (in the build list) what ranks are trained at what level for the current maneuver style.
	# Calculate All will do this for Combat, Shield, Armor in that order.
	# This method will also call on a number of different Maneuver object methods as well. Please review the Maneuver class in Globals.py for more information.
	def Plan_Training_Schedule(self, style):
		error_text = ""
		schedule_names = []
		
		total_available_array = [tkinter.IntVar() for i in range(101)]
		total_cost_array = [tkinter.IntVar() for i in range(101)]
		total_leftover_array = [tkinter.IntVar() for i in range(101)]
		
		if style == "All":
			schedule_names = ["Combat", "Shield", "Armor"]
		else:
			schedule_names = [style]			
					
		for type in schedule_names:		
			abort_loops = 0
			slevel = 0; tlevel = 0; ranks_taken = 0; ranks_needed = 0
			next_rank_cost = 0; available = 0; cost_at_level = 0; prev_leftover = 0
			tranks = 0; tcost = 0; new_min = 0; 
			
			for i in range(0, 101):
				total_available_array[i].set(0)
				total_cost_array[i].set(0)
				total_leftover_array[i].set(0) 
							
			if type == "Combat":
				skill_name = "Combat Maneuvers"
				blist = globals.character.build_combat_maneuvers_list
				slist = globals.character.combat_maneuvers_list					
			elif type == "Shield":
				skill_name = "Shield Use"
				blist = globals.character.build_shield_maneuvers_list
				slist = globals.character.shield_maneuvers_list
			elif type == "Armor":
				skill_name = "Armor Use"
				blist = globals.character.build_armor_maneuvers_list
				slist = globals.character.armor_maneuvers_list				
						
			for key, row in slist.items():
				row.Set_To_Default()
				
			for i in range(0, 101):
				if i > 0:
					prev_leftover = total_leftover_array[i-1].get()
				
				tranks = globals.character.skills_list[skill_name].ranks_by_level[i].get()									
				total_available_array[i].set( prev_leftover + tranks )
				total_leftover_array[i].set( prev_leftover + tranks )					
						
			for man in blist:		
				if abort_loops:
					break
				if man.hide.get() == "x":
					continue						
				
				slevel = int(man.slvl.get())
				tlevel = int(man.tlvl.get())
				ranks_needed = int(man.goal.get())
				ranks_taken = 0				
				prev_leftover = 0				
				if slevel < new_min:
					slevel = new_min	

				row = slist[man.name.get()]	
				available = 0	

				for lvl in range(slevel, tlevel+1):			
					if not globals.character.Meets_Maneuver_Prerequisites(lvl, row.name, row.type):
						if lvl >= tlevel:
							error_text += "ERROR: Unable to meet the prerequisites to train in %s by level %s.\n" % (man.name.get(), tlevel)							
							abort_loops = 1
							break
						else:
							continue
							
					# Does character have prerequisites for maneuver at this level??? logic will go here	
					available = total_leftover_array[lvl].get()							
							
					cost_at_level = 0	
					prev_leftover = 0
					next_rank_cost = row.Get_Cost_At_Rank(row.total_ranks_by_level[lvl].get() + 1)  
					tcost = row.Get_Total_Cost_At_Rank(0, row.total_ranks_by_level[lvl].get() + 1)
									
					while available >= next_rank_cost and (type == "Armor" or lvl+1 >= tcost):
						cost_at_level += next_rank_cost
						available -= next_rank_cost
						ranks_taken += 1
						row.Train_New_Ranks(lvl, 1)	
						if ranks_needed <= ranks_taken:
							break
						next_rank_cost = row.Get_Cost_At_Rank(row.total_ranks_by_level[lvl].get() + 1)    
						tcost = row.Get_Total_Cost_At_Rank(0, row.total_ranks_by_level[lvl].get() + 1)

					if cost_at_level > 0:
						total_cost_array[lvl].set( cost_at_level + total_cost_array[lvl].get() )
						new_min = lvl
						
						for i in range(lvl, 101):
							prev_leftover = total_leftover_array[i-1].get()
					
							ranks = globals.character.skills_list[skill_name].ranks_by_level[i].get()	
										
							total_available_array[i].set( prev_leftover + ranks )
							total_leftover_array[i].set( prev_leftover + ranks - total_cost_array[i].get() )	
								
					if ranks_needed > ranks_taken and lvl >= tlevel:	
						error_text += "ERROR: Insufficient points to train %s ranks in %s by level %s.\n" % (ranks_needed, man.name.get(), tlevel)
						abort_loops = 1
						break				
					elif ranks_needed <= ranks_taken:
						break

			if type == "Combat":
				for i in range(101):
					self.total_available_combat_points_by_level[i].set(total_available_array[i].get())
					self.total_cost_combat_points_by_level[i].set(total_cost_array[i].get())
					self.total_leftover_combat_points_by_level[i].set(total_leftover_array[i].get())
			elif type == "Shield":
				for i in range(101):
					self.total_available_shield_points_by_level[i].set(total_available_array[i].get())
					self.total_cost_shield_points_by_level[i].set(total_cost_array[i].get())
					self.total_leftover_shield_points_by_level[i].set(total_leftover_array[i].get())
			elif type == "Armor":
				for i in range(101):
					self.total_available_armor_points_by_level[i].set(total_available_array[i].get())
					self.total_cost_armor_points_by_level[i].set(total_cost_array[i].get())
					self.total_leftover_armor_points_by_level[i].set(total_leftover_array[i].get())			
			
		if error_text != "":
			globals.info_dialog.Show_Message(error_text)

#		globals.character.Update_Statistics()
#		for i in range(101):
#			globals.character.Update_Resources(i)	
		self.Update_Schedule_Frames()	

		
	# This is called when user changes the level counter or when the user's build has been recalculated.
	# It uses what ever the current level is and updates the schedule frame and schedule footer			
	def Update_Schedule_Frames(self):
		if self.level_counter.getvalue() == "":
			return
			
		i = 0; combat_ranks = 0; shield_ranks = 0; armor_ranks = 0
		level = int(self.level_counter.getvalue())
		style = self.maneuver_mode.get()
		prof = globals.character.profession.name
		combat_ranks = globals.character.skills_list["Combat Maneuvers"].ranks_by_level[level].get()	
		shield_ranks = globals.character.skills_list["Shield Use"].ranks_by_level[level].get()
		armor_ranks = globals.character.skills_list["Armor Use"].ranks_by_level[level].get()
			
		if style == "Combat":
			current_keys = globals.combat_maneuver_names
			current_schedule = globals.character.combat_maneuvers_list
		elif style == "Shield":
			current_keys = globals.shield_maneuver_names
			current_schedule = globals.character.shield_maneuvers_list
		elif style == "Armor":		
			current_keys = globals.armor_maneuver_names
			current_schedule = globals.character.armor_maneuvers_list			

		for key in current_keys:	
			row = current_schedule[key]			
			if row.availability[prof] == 1 and (self.ManP_radio_var.get() == 1 or (self.ManP_radio_var.get() == 2 and row.total_ranks_by_level[100].get() > 0) or (self.ManP_radio_var.get() == 3 and row.ranks_by_level[level].get() > 0)):
				if row.ranks_by_level[level].get() > 0:
					row.cost.set(row.cost_at_level[level].get())
				else:
					row.cost.set("")				
				row.ranks.set(row.ranks_by_level[level].get())
				row.total_ranks.set(row.total_ranks_by_level[level].get())
				row.combined_cost.set(row.combined_cost_by_level[level].get())
				row.ManP_schedule_row.grid(row=i, column=0)
			else:
				row.ManP_schedule_row.grid_remove()
			i += 1
			
		self.vars_sfooter_combat_earned.set(combat_ranks)
		self.vars_sfooter_shield_earned.set(shield_ranks)		
		self.vars_sfooter_armor_earned.set(armor_ranks)		
		self.vars_sfooter_combat_available.set(self.total_available_combat_points_by_level[level].get())
		self.vars_sfooter_shield_available.set(self.total_available_shield_points_by_level[level].get())	
		self.vars_sfooter_armor_available.set(self.total_available_armor_points_by_level[level].get())	
		self.vars_sfooter_combat_total_cost.set(self.total_cost_combat_points_by_level[level].get())
		self.vars_sfooter_shield_total_cost.set(self.total_cost_shield_points_by_level[level].get())
		self.vars_sfooter_armor_total_cost.set(self.total_cost_armor_points_by_level[level].get())
		self.vars_sfooter_combat_leftover.set(self.total_leftover_combat_points_by_level[level].get())
		self.vars_sfooter_shield_leftover.set(self.total_leftover_shield_points_by_level[level].get())
		self.vars_sfooter_armor_leftover.set(self.total_leftover_armor_points_by_level[level].get())

	
	# This allows mouse scrolling in the build frame. Anything with the bind tag SkP_Build will allow the scrolling
	def Scroll_Build_Frame(self, event):
		self.ML_Frame.yview("scroll", -1*(event.delta/120), "units")
		
		
	# This allows mouse scrolling in the schedule frame. Anything with the bind tag SkP_Schedule will allow the scrolling	
	def Scroll_Schedule_Frame(self, event):
		self.MR_Frame.yview("scroll", -1*(event.delta/120), "units")	

			
	# Wrapper function used by Globals.py to create a new Maneuver from Character file.		
	def Create_Build_List_Maneuver(self, parent, name, type, hidden, order, start, target, goal, ranks_arr ):
		return Build_List_Maneuver(parent, name, type, hidden, order, start, target, goal, ranks_arr )
		
		
# This class holds all the information for a specific maneuver the character wants to train in. These maneuvers are shown the build frame using the object's ManP_Build_Row frame		
class Build_List_Maneuver:
	def __init__(self, parent, name, type, hidden, order, start, target, goal, ranks_arr ):
		self.name = tkinter.StringVar()
		self.ranks = [tkinter.StringVar() for i in range(5)]
		self.order = tkinter.StringVar()
		self.hide = tkinter.StringVar()
		self.slvl = tkinter.StringVar()
		self.tlvl = tkinter.StringVar()
		self.goal = tkinter.StringVar()
		self.ManP_Build_Row = tkinter.Frame(parent)
		self.ManP_Edit_Button = ""
		self.type = type				
		
		i=0
		for rank in ranks_arr:
			if rank != "-":
				self.ranks[i].set( math.floor(int(rank) ) )
			else:
				self.ranks[i].set("-")			
			i += 1
						
		self.name.set(name)
		self.hide.set(hidden)
		self.order.set(order)
		self.slvl.set(start)
		self.tlvl.set(target)
		self.goal.set(goal)
				
		L1 = tkinter.Label(self.ManP_Build_Row, width=3, bg="lightgray", textvariable=self.hide)
		L1.grid(row=0, column=0, sticky="w", padx="1", pady="1")
		L1.bindtags("ManP_build")
		L2 = tkinter.Label(self.ManP_Build_Row, width=6, bg="lightgray", textvariable=self.order)
		L2.grid(row=0, column=2, padx="1", pady="1")
		L2.bindtags("ManP_build")
		L3 = tkinter.Label(self.ManP_Build_Row, width="26", anchor="w", bg="lightgray", textvariable=self.name)
		L3.grid(row=0, column=3, padx="1", pady="1")
		L3.bindtags("ManP_build")
		L4 = tkinter.Label(self.ManP_Build_Row, width="3", bg="lightgray", textvar=self.ranks[0])
		L4.grid(row=0, column=4, padx="1", pady="1")
		L4.bindtags("ManP_build")
		L5 = tkinter.Label(self.ManP_Build_Row, width="3", bg="lightgray", textvar=self.ranks[1])
		L5.grid(row=0, column=5, padx="1", pady="1")
		L5.bindtags("ManP_build")
		L6 = tkinter.Label(self.ManP_Build_Row, width="3", bg="lightgray", textvar=self.ranks[2])
		L6.grid(row=0, column=6, padx="1", pady="1")
		L6.bindtags("ManP_build")
		L7 = tkinter.Label(self.ManP_Build_Row, width="3", bg="lightgray", textvar=self.ranks[3])
		L7.grid(row=0, column=7, padx="1", pady="1")
		L7.bindtags("ManP_build")
		L8 = tkinter.Label(self.ManP_Build_Row, width="3", bg="lightgray", textvar=self.ranks[4])
		L8.grid(row=0, column=8, padx="1", pady="1")
		L8.bindtags("ManP_build")
		L9 = tkinter.Label(self.ManP_Build_Row, width=5, bg="lightgray", textvariable=self.goal)
		L9.grid(row=0, column=9, padx="1")
		L9.bindtags("ManP_build")
		L10 = tkinter.Label(self.ManP_Build_Row, width=5, bg="lightgray", textvariable=self.slvl)
		L10.grid(row=0, column=10, padx="1")
		L10.bindtags("ManP_build")
		L11 = tkinter.Label(self.ManP_Build_Row, width=5, bg="lightgray", textvariable=self.tlvl)
		L11.grid(row=0, column=11, padx="1")
		L11.bindtags("ManP_build")
		self.ManP_Edit_Button = tkinter.Button(self.ManP_Build_Row, text="Edit", command="")
		self.ManP_Edit_Button.grid(row=0, column=12, padx="3")		
