# INDEX OF CLASSES AND METHODS

'''
class Progression_Panel
	def __init__(self, panel)
	def Create_Gear_List_Frame(self, panel):
	def Create_Effect_Header_Frame(self, panel):	
	def Create_Effect_List_Frame(self, panel):
	def Create_Graph_Plot_Frame(self, panel):
	def Plot_Graph_Clear(self):	
	def Plot_Graph_Data(self):
	def Graph_Marker_Onclick(self, event):
	def Graph_Option_Category_OnChange(self, choice):
	def Graph_Option_Subcategory_OnChange(self, choice):
	def Gear_List_Populate_Lists(self):
	def Gear_List_Onchange(self, type, gear_name):	
	def Get_Gear_By_Order(self, gear_name):		
	def Effects_List_Populate_List(self):		
	def Effects_Toggle_Button_Onclick(self):
	def Scroll_Effects_Frame(self, event):
	def Scroll_Tooltip_Frame(self, event):
	def Find_Overrides_By_Tags(self, effect_tags):
	def Find_Effects_By_Tags(self, effect_tags):	
	def Set_Graph_Labels(self, skill_names, xlabel, ylabel):
	def Combine_Effects(self, level, effect_name, base_value, effects_lists_arr, tag_arr, action_type):
	def Formula_Attack_Strength(self, twc_mode, gear_name, gear_skills_names, main_enchantment, other_enchantment, self.calc_style):	
	def Formula_Unarmed_Attack_Factor(self, gloves, boots, main, other, self.calc_style):	
	def Formula_Defense_Strength(self, vs_type, main_gear, other_hand_gear, armor_gear, gloves_gear, self.calc_style):
	def Formula_Roundtime_Qstrike(self, alt_mode):	
	def Formula_Casting_Strength(self, display_spell_circles, statistic_names, self.calc_style):
	def Formula_Target_Defense(self, self.calc_style):
	def Formula_Armor_Use(self):	
	def Formula_Spell_Hindrance(self, spell_circles):	
	def Formula_Multi_Opponent_Combat(self, self.calc_style):	
	def Formula_AS_MIU(self, choice):	
	def Formula_Redux(self):	
	def Formula_Mana_Control(self, self.calc_style):	
	def Formula_Summation_Bonuses(lore):
	def Formula_First_Aid(self, self.calc_style):	
	def Formula_Trading(self, self.calc_style):
	def Formula_Encumbrance(self):	
	def Formula_Imprint(self):	
	def Formula_Resources(self, self.calc_style):
	def Formula_Spellburst(self, self.calc_style):
	def Formula_Spellsong(self):
	
	
class Graph_Data_Line_Container:	
	def __init__(self):			
	def Reset_Graph_Data(self):		
'''


#!/usr/bin/python

import tkinter
import math
import Pmw
import Globals as globals
import Calculations as calculations

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTk, NavigationToolbar2Tk
from matplotlib.figure import Figure


# The Progression Panel combines the data entered into the Statistics, Misc, Skills, Maneuvers,
# Postcap, and Loadout Panels to display how a character grows in regards to
# various game mechanics such as Attack Strength and Target Defense. The results are presented 
# as a line graph that the user can interact with to display more detailed information.
class Progression_Panel:  
	def __init__(self, panel):		
		self.gear_main_weapon = tkinter.StringVar()
		self.gear_other_hand = tkinter.StringVar()
		self.gear_armor = tkinter.StringVar()
		self.gear_uac_gloves = tkinter.StringVar()
		self.gear_uac_boots = tkinter.StringVar()		
		self.graph_figure = ""
		self.graph_tooltip_frame = ""
		self.graph_tooltip_text = tkinter.StringVar()
		self.graph_option_category = tkinter.StringVar()
		self.graph_option_subcategory = tkinter.StringVar()		
		self.graph_radio_var = tkinter.IntVar()
		self.effects_list_toggle = 0
		self.calc_style = 1
		
		# These are the default gear options that are always included in the Gear List Frame
		self.base_main_weapon = globals.Gear(0, "Closed Fist", 0, 0, "Brawling", "")
		self.base_main_weapon.gear_traits = {"base_speed": 1, "minimum_speed": 3}		
		self.base_other_hand = globals.Gear(0, "Empty", 0, 0, "None", "")
		self.base_armor = globals.Gear(0, "No Armor", 0, 0, "None", "")
		self.base_armor.dialog_type = "Armor"
		self.base_armor.Set_Gear_Traits("Clothing")
		self.base_uac_gloves = globals.Gear(0, "No Gloves", 0, 0, "None", "")
		self.base_uac_boots = globals.Gear(0, "No Boots", 0, 0, "None", "")	
		
		# Set the default gear to be the default option selected
		self.gear_main_weapon.set(self.base_main_weapon.name.get())
		self.gear_other_hand.set(self.base_other_hand.name.get())
		self.gear_armor.set(self.base_armor.name.get())
		self.gear_uac_gloves.set(self.base_uac_gloves.name.get())
		self.gear_uac_boots.set(self.base_uac_boots.name.get())		
		
		self.subcategory_list_physical = [
				"Attack Strength (Main Weapon)", 
				"Attack Strength (Other Hand Weapon)", 
				"Unarmed Attack Factor (UAF)", 
				"Defense Strength (vs Melee)", 
				"Defense Strength (vs Ranged)", 
				"Defense Strength (vs Bolt Spell)", 
				"Roundtime & Qstrike Stamina Cost", 
				"Roundtime & Qstrike Stamina Cost (TWC)", 
				"Roundtime & Qstrike Stamina Cost (UAC)"
				]	
		self.subcategory_list_magical = [
				"Attack Strength (Spell Aiming)", 
				"Casting Strength (Bard - MnE, Bard)", 
				"Casting Strength (Cleric - MnS, MjS, Cleric)", 
				"Casting Strength (Empath - MnS, MjS, Empath)", 
				"Casting Strength (Monk - MnS, MnM)", 
				"Casting Strength (Paladin - MnS, Paladin)", 
				"Casting Strength (Ranger - MnS, Ranger)", 
				"Casting Strength (Rogue/Warrior - MnS, MnE)", 
#				"Casting Strength (Savant - MnM, MjM, Savant)", 
				"Casting Strength (Sorcerer - MnS, MnE, Sorc)", 
				"Casting Strength (Wizard - MnE, MjE, Wizard)", 
				"Casting Strength (Arcane Circle)", 
				"Target Defense",
				]		
		self.subcategory_list_skills_physical = [		
				"Armor Use - Action & Roundtime Penalties", 
				"Armor Use - Spell Hindrance (MnE, Bard)",						
				"Armor Use - Spell Hindrance (MnS, MjS, Cleric)",
				"Armor Use - Spell Hindrance (MnS, MjS, Empath)",
				"Armor Use - Spell Hindrance (MnS, MnM)",
				"Armor Use - Spell Hindrance (MnS, Paladin)",
				"Armor Use - Spell Hindrance (MnS, Ranger)",
				"Armor Use - Spell Hindrance (MnS, MnE)",
#				"Armor Use - Spell Hindrance (MnM, MjM, Savant)",
				"Armor Use - Spell Hindrance (MnS, MnE, Sorc)",
				"Armor Use - Spell Hindrance (MnE, MjE, Wizard)",	
				"Multi Opponent Combat - FoF, Mstrike",
				]	

		self.subcategory_list_skills_magical = [
				"Arcane Symbols - CS, Max Spell, Duration", 
				"Magic Item Use - CS, Max Spell, Duration", 
				"Mana Control - Mana Pulse & Spellup",
				"Elemental Lore, Air - Summations", 
				"Elemental Lore, Earth - Summations", 
				"Elemental Lore, Fire - Summations", 
				"Elemental Lore, Water - Summations", 
				"Elemental Lore, Multiple - Summations", 
				"Spiritual Lore, Blessings - Summations", 
				"Spiritual Lore, Religion - Summations", 
				"Spiritual Lore, Summoning - Summations", 
				"Spiritual Lore, Multiple - Summations", 
				"Sorcerous Lore, Demonology - Summations", 
				"Sorcerous Lore, Necromancy - Summations", 
				"Mental Lore, Divination - Summations", 
				"Mental Lore, Manipulation - Summations", 
				"Mental Lore, Telepathy - Summations", 
				"Mental Lore, Transference - Summations", 
				"Mental Lore, Transformation - Summations", 
				]

		self.subcategory_list_skills_general = [
				"First Aid - Bandage Duration & Herb RT", 
				"Trading - Skill Boost",
				]
				
		self.subcategory_list_other = [
				"Bard Spellsong Duration", 
				"Empath Imprint Chance & Maximum",
				"Encumbrance", 
				"Redux", 
				"Resources Maximums & Recovery", 
				"Spellburst",
				]
			
		
		# Create each section of the Progression Panel
		self.Gear_List_Frame = self.Create_Gear_List_Frame(panel)
		self.Effect_Header_Frame = self.Create_Effect_Header_Frame(panel)
		self.Effect_List_Frame = self.Create_Effect_List_Frame(panel)		
		self.Graph_Plot_Frame = self.Create_Graph_Plot_Frame(panel)

		
		# Make the frames visible
		self.Gear_List_Frame.grid(row=1, column=0, sticky="nw")
		self.Effect_Header_Frame.grid(row=2, column=0, sticky="nw")
		self.Effect_List_Frame.grid(row=3, column=0, sticky="nw")		
		self.Graph_Plot_Frame.grid(row=0, column=1, rowspan=4, sticky="nw")		
		
		
		# Initialize defaults
		self.graph_information = Graph_Data_Line_Container()
		self.graph_radio_var.set(1)		
		self.graph_option_category.set("Physical Combat")
		self.Graph_Option_Category_OnChange("Physical Combat")
		self.Effect_List_Frame.bind_class("ProgP_effects", "<MouseWheel>", self.Scroll_Effects_Frame)
		self.graph_tooltip_frame.bind_class("ProgP_tooltip", "<MouseWheel>", self.Scroll_Tooltip_Frame)
		self.Plot_Graph_Clear()
		
		
	# Creates the frame that holds the equipped gear used by the character. These lists are populated by the Gear_List_Populate_Lists method	
	def Create_Gear_List_Frame(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 369, hull_height = 200)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")	
		myframe_inner = myframe.interior()
		
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Main Weapon").grid(row=0, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Other Hand").grid(row=1, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="Armor").grid(row=2, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="UAC Gloves").grid(row=3, column=0, sticky="w")
		tkinter.Label(myframe_inner, width="13", anchor="w", bg="lightgray", text="UAC Boots").grid(row=4, column=0, sticky="w")
		
		self.gear_main_weapon_menu = tkinter.OptionMenu(myframe_inner, self.gear_main_weapon, self.gear_main_weapon.get() )
		self.gear_main_weapon_menu.config(width=33, heigh=1)	
		self.gear_other_hand_menu = tkinter.OptionMenu(myframe_inner, self.gear_other_hand, self.gear_other_hand.get() )
		self.gear_other_hand_menu.config(width=33, heigh=1)	
		self.gear_armor_menu = tkinter.OptionMenu(myframe_inner, self.gear_armor, self.gear_armor.get() )
		self.gear_armor_menu.config(width=33, heigh=1)	
		self.gear_uac_gloves_menu = tkinter.OptionMenu(myframe_inner, self.gear_uac_gloves, self.gear_uac_gloves.get() )
		self.gear_uac_gloves_menu.config(width=33, heigh=1)	
		self.gear_uac_boots_menu = tkinter.OptionMenu(myframe_inner, self.gear_uac_boots, self.gear_uac_boots.get() )
		self.gear_uac_boots_menu.config(width=33, heigh=1)	
		
		# Make the frames visible
		self.gear_main_weapon_menu.grid(row=0, column=1, sticky="w")	
		self.gear_other_hand_menu.grid(row=1, column=1, sticky="w")	
		self.gear_armor_menu.grid(row=2, column=1, sticky="w")	
		self.gear_uac_gloves_menu.grid(row=3, column=1, sticky="w")	
		self.gear_uac_boots_menu.grid(row=4, column=1, sticky="w")	
				
		return myframe

	
	# Creates a frame to hold the column titles for the Effects List Frame. This is done to allow scrolling, without losing the titles.
	def Create_Effect_Header_Frame(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 369, hull_height = 53)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")	
		myframe_inner = myframe.interior()
		
		
		# top frame holds the 3 buttons
		topframe = tkinter.Frame(myframe_inner)		
		topframe.grid(row=1, column=0, sticky="w")			
		tkinter.Button(topframe, text="Toggle All Effects", command=self.Effects_Toggle_Button_Onclick).grid(row=0, column=0, sticky="w", pady="1")	
		
		# this is frame will hold the title of the build schedule frame. This is done to allow the other frame to scroll but not lose the title header
		title_scrollframe = Pmw.ScrolledFrame(myframe_inner, usehullsize = 1, hull_width = 348, hull_height = 26 )		
		title_scrollframe.configure(hscrollmode = "none")		
		title_scrollframe.grid(row=3, column=0, sticky="w")		
		title_scrollframe_inner = title_scrollframe.interior()						
		
		# add all labels to the tittle header
		tkinter.Frame(title_scrollframe_inner).grid(row=3, column=0, columnspan=3)	
		tkinter.Label(title_scrollframe_inner, width="3", bg="lightgray", text="Hide").grid(row=0, column=0, padx="1")
		tkinter.Label(title_scrollframe_inner, width="15", bg="lightgray", text="Effect Name").grid(row=0, column=2, padx="1")
		tkinter.Label(title_scrollframe_inner, width="8", bg="lightgray", text="Type").grid(row=0, column=3, padx="1")
		tkinter.Label(title_scrollframe_inner, width="20", bg="lightgray", text="Effect Scaling").grid(row=0, column=4, padx="1")		
		
		return myframe

		
	# Frame dedicated to holding the effects the character is using. The effects are supplied by the Loadout Panel.
	# Displays: Hide, Effect Name, Scaling
	def Create_Effect_List_Frame(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 369, hull_height = 290)
		myframe.configure(hscrollmode = "none", vscrollmode = "static")	
		myframe_inner = myframe.interior()
		
		return myframe
		

	# This method creates 3 important frames:
	# - tkinter drawing area. Composed of Figure and a single plot that displays data in a table in line format.
	# - option frame below the drawing area. The options determine what data will be display on the data plot.
	# - tooltip frame to the right of the options frame. Clicking the graph after ploting data will display
	#    a message in the tooltip frame that breaks down how the data for a specific level/postcap experience 
	#    interval was calculated.
	def Create_Graph_Plot_Frame(self, panel):
		myframe = Pmw.ScrolledFrame(panel, usehullsize = 1, hull_width = 731, hull_height = 543)
		myframe.configure(hscrollmode = "none", vscrollmode = "none")	
		myframe_inner = myframe.interior()
		
#		plt.ion()
		# Creates the figure and plot contained in the canvas that data can be plotted on
		self.graph_figure = Figure(figsize=(7.25, 3.80), dpi=100, tight_layout={'pad':3})
		a = self.graph_figure.add_subplot(111)
			
		# a tk.DrawingArea
		canvas = FigureCanvasTk(self.graph_figure, master=myframe_inner)
		canvas.draw()
		canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nw")
		
		# Creates the toolbar for the figure. At this time, the toolbar is the default one used Matplotlib. In the future, I might customize this
		toolbar_frame = tkinter.Frame(myframe_inner)
		toolbar_frame.grid(row=1, column=0, sticky="nw")
		toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
		toolbar.update()
		

		# The lower frame where the type of plot data can be specified
		options_frame = tkinter.Frame(myframe_inner, width=10)

		tkinter.Label(options_frame, width="10", anchor="w", bg="lightgray", text="Category").grid(row=0, column=0, sticky="w")
		tkinter.Label(options_frame, width="10", anchor="w", bg="lightgray", text="Subcategory").grid(row=1, column=0, sticky="w")
		
		choices = ["Physical Combat", "Magical Combat", "Physical Skills", "Magical Skills", "General Skills", "Other"]
		self.graph_option_category_menu = tkinter.OptionMenu(options_frame, self.graph_option_category, *choices, command=self.Graph_Option_Category_OnChange)
		self.graph_option_category_menu.config(width=43, heigh=1)				
		self.graph_option_subcategory_menu = tkinter.OptionMenu(options_frame, self.graph_option_subcategory, "", command=self.Graph_Option_Subcategory_OnChange)
		self.graph_option_subcategory_menu.config(width=43, heigh=1)			
		tkinter.Radiobutton(options_frame, anchor="w", text="Pre-Cap", command="", var=self.graph_radio_var, value=1).grid(row=2, column=0, sticky="w", pady="1")
		tkinter.Radiobutton(options_frame, anchor="w", text="Post-Cap", command="", var=self.graph_radio_var, value=2).grid(row=2, column=1, sticky="w", pady="1")			
		tkinter.Button(options_frame, text="Plot Data", command=self.Plot_Graph_Data).grid(row=3, column=0, sticky="w", pady="1")	
		
		self.graph_option_category_menu.grid(row=0, column=1, sticky="w")	
		self.graph_option_subcategory_menu.grid(row=1, column=1, sticky="w")		
		options_frame.grid(row=2, column=0, sticky="nw")

		# Tooltip frame				
		self.graph_tooltip_frame = Pmw.ScrolledFrame(myframe_inner, usehullsize = 1, hull_width = 345, hull_height = 158)
		self.graph_tooltip_frame.configure(hscrollmode = "none", vscrollmode = "static")		
		self.graph_tooltip_frame.bindtags("ProgP_tooltip")
		tooltip_label = tkinter.Label(self.graph_tooltip_frame.interior(), justify="left", anchor="nw", width=100, wraplength=310, textvariable=self.graph_tooltip_text)	
		tooltip_label.bindtags("ProgP_tooltip")
		
		tooltip_label.grid(row=0, column=0, sticky="nw", padx="1") 
		self.graph_tooltip_frame.grid(row=1, column=1, sticky="nw", rowspan=2)					
		
		return myframe		
		
	
	# Clears the graph figure of whatever data was shown. Used to "reset" the figure after 
	def Plot_Graph_Clear(self):		
		self.graph_information.Reset_Graph_Data()
	
		a = self.graph_figure.axes[0]
		a.cla()		
		a.grid()   						 # This isn't a tkinter grid, this makes it SHOW a grid format on the graph figure
		a.set_picker(True)
		
		# major ticks every 10, minor ticks every 1                                      
		major_ticks = np.arange(0, 101, 10)                                              
		minor_ticks = np.arange(0, 101, 1)       
		
		a.set_xlabel("Level Axis")
		a.set_ylabel("Value Axis")
		
		self.graph_figure.canvas.draw()
		self.graph_tooltip_text.set("")
	
	
	# This method is used to plot data depending on the options selected by the user.
	# The choice option determines which formula is called. This formula will populated
	# the graph_information object which is used as the data for the figure's plot
	def Plot_Graph_Data(self):	
		# Reset the graphing data 
		self.graph_information.Reset_Graph_Data()
		self.graph_tooltip_text.set("Click the data points on the graph for more information.")
		self.calc_style = self.graph_radio_var.get()
		
		a = self.graph_figure.axes[0]
		a.cla()		
		a.grid()   						 # This isn't a tkinter grid, this makes it SHOW a grid format
		a.set_picker(True)
		
		# Yes, this DOES need to be done everytime data is plotted. Changing the graphed information, removes the button press event
		self.graph_figure.canvas.mpl_connect('button_press_event', self.Graph_Marker_Onclick)			
					
		category = self.graph_option_category.get()
		choice = self.graph_option_subcategory.get()
		calculations.override_dict = {}
		
		summation_mode = 0
		
				
		if category == "Physical Combat":
			if choice == "Attack Strength (Main Weapon)":	
				main_gear = self.Get_Gear_By_Order(self.gear_main_weapon.get())
				other_gear = self.Get_Gear_By_Order(self.gear_other_hand.get())
				ammo_enchantment = 0
				if main_gear.skills == "Ranged Weapons" and other_gear.name.get() == "Arrows/Bolts":
					ammo_enchantment = int(other_gear.enchantment)
				
				self.Formula_Attack_Strength(0, main_gear, ammo_enchantment)
					
			elif choice == "Attack Strength (Other Hand Weapon)":		
				other_gear = self.Get_Gear_By_Order(self.gear_other_hand.get())
				name = other_gear.name.get() 
				
				# Invalid off-hand gear, abort ploting
				if name == "Empty" or name == "Small Shield" or name == "Medium Shield" or name == "Large Shield" or name == "Tower Shield":
					self.Plot_Graph_Clear()
					tkinter.messagebox.showerror("Error", "Other Hand Weapon AS cannot be calculated without a weapon equipped in Other Hand")
					return
				
				self.Formula_Attack_Strength(1, other_gear, 0)		
					
			elif choice == "Unarmed Attack Factor (UAF)":
				gloves = self.Get_Gear_By_Order(self.gear_uac_gloves.get())
				boots = self.Get_Gear_By_Order(self.gear_uac_boots.get())
				main = self.Get_Gear_By_Order(self.gear_main_weapon.get())
				other = self.Get_Gear_By_Order(self.gear_other_hand.get())
				
				self.Formula_Unarmed_Attack_Factor(gloves, boots, main, other)							
					
			elif choice == "Defense Strength (vs Melee)":	
				gear = self.Get_Gear_By_Order(self.gear_main_weapon.get())
				other = self.Get_Gear_By_Order(self.gear_other_hand.get())
				armor = self.Get_Gear_By_Order(self.gear_armor.get())
				gloves = self.Get_Gear_By_Order(self.gear_uac_gloves.get())
				
				self.Formula_Defense_Strength("Melee", gear, other, armor, gloves)
					
			elif choice == "Defense Strength (vs Ranged)":	
				gear = self.Get_Gear_By_Order(self.gear_main_weapon.get())
				other = self.Get_Gear_By_Order(self.gear_other_hand.get())
				armor = self.Get_Gear_By_Order(self.gear_armor.get())
				gloves = self.Get_Gear_By_Order(self.gear_uac_gloves.get())
				
				self.Formula_Defense_Strength("Ranged", gear, other, armor, gloves)
					
			elif choice == "Defense Strength (vs Bolt Spell)":	
				gear = self.Get_Gear_By_Order(self.gear_main_weapon.get())
				other = self.Get_Gear_By_Order(self.gear_other_hand.get())
				armor = self.Get_Gear_By_Order(self.gear_armor.get())
				gloves = self.Get_Gear_By_Order(self.gear_uac_gloves.get())
				
				self.Formula_Defense_Strength("Bolt", gear, other, armor, gloves)
				
			elif choice == "Roundtime & Qstrike Stamina Cost":	
				self.Formula_Roundtime_Qstrike("")
				
			elif choice == "Roundtime & Qstrike Stamina Cost (TWC)":	
				other_hand_name = self.Get_Gear_By_Order(self.gear_other_hand.get()).name.get()
				
				# Invalid off-hand gear, abort ploting
				if other_hand_name == "Empty" or other_hand_name == "Small Shield" or other_hand_name == "Medium Shield" or other_hand_name == "Large Shield" or other_hand_name == "Tower Shield":
					self.Plot_Graph_Clear()
					tkinter.messagebox.showerror("Error", "Roundtime & Qstrike Stamina Cost (TWC) cannot be calculated without a weapon equipped in Other Hand")
					return
					
				self.Formula_Roundtime_Qstrike("TWC")
				
			elif choice == "Roundtime & Qstrike Stamina Cost (UAC)":	
				self.Formula_Roundtime_Qstrike("UAC")
				
			else:
				print("ERROR!!! Progression choice is not implemented!")
				self.Plot_Graph_Clear()
				return

		elif category == "Magical Combat":
			if choice == "Attack Strength (Spell Aiming)":	
				dummy_gear = globals.Gear(0, "Bolt Spell", 0, 0, "Spell Aiming", "")
				self.Formula_Attack_Strength(0, dummy_gear, 0)
					
			elif choice == "Target Defense":
				self.Formula_Target_Defense()	
				
			elif "Casting Strength" in choice:
				if choice == "Casting Strength (Bard - MnE, Bard)":
					spell_circles = ["Minor Elemental", "Bard"]
					statistic_names = ["Aura"]		
						
				elif choice == "Casting Strength (Cleric - MnS, MjS, Cleric)":
					spell_circles = ["Minor Spiritual", "Major Spiritual", "Cleric"]
					statistic_names = ["Wisdom"]	
							
				elif choice == "Casting Strength (Empath - MnS, MjS, Empath)":
					spell_circles = ["Minor Spiritual", "Major Spiritual", "Empath"]
					statistic_names = ["Wisdom"]	
							
				elif choice == "Casting Strength (Monk - MnS, MnM)":
					spell_circles = ["Minor Spiritual", "Minor Mental"]
					statistic_names = ["Logic", "Wisdom"]	
							
				elif choice == "Casting Strength (Paladin - MnS, Paladin)":
					spell_circles = ["Minor Spiritual", "Paladin"]
					statistic_names = ["Wisdom"]	
							
				elif choice == "Casting Strength (Ranger - MnS, Ranger)":
					spell_circles = ["Minor Spiritual", "Ranger"]
					statistic_names = ["Wisdom"]	
							
				elif choice == "Casting Strength (Rogue/Warrior - MnS, MnE)":
					spell_circles = ["Minor Spiritual", "Minor Elemental"]
					statistic_names = ["Aura", "Wisdom"]	
							
				elif choice == "Casting Strength (Savant - MnM, MjM, Savant)":
					spell_circles = ["Minor Mental", "Major Mental", "Savant"]
					statistic_names = ["Discipline", "Influence", "Logic"]			
					
				elif choice == "Casting Strength (Sorcerer - MnS, MnE, Sorc)":
					spell_circles = ["Minor Spiritual", "Minor Elemental", "Sorcerer"]
					statistic_names = ["Aura", "Wisdom"]			
					
				elif choice == "Casting Strength (Wizard - MnE, MjE, Wizard)":
					spell_circles = ["Minor Elemental", "Major Elemental", "Wizard"]
					statistic_names = ["Aura"]			
					
				elif choice == "Casting Strength (Arcane Circle)":
					spell_circles = ["Arcane"]
					statistic_names = ["Aura", "Logic", "Wisdom"]	
					
				
				self.Formula_Casting_Strength(spell_circles, statistic_names)											
					
			else:
				print("ERROR!!! Progression choice is not implemented!")
				self.Plot_Graph_Clear()
				return
	
		elif category == "Physical Skills":			
			if choice == "Armor Use - Action & Roundtime Penalties":				
				self.Formula_Armor_Use()	

			elif "Spell Hindrance" in choice:
				if choice == "Armor Use - Spell Hindrance (MnE, Bard)":
					spell_circles = ["Minor Elemental", "Bard"]
						
				elif choice == "Armor Use - Spell Hindrance (MnS, MjS, Cleric)":
					spell_circles = ["Minor Spiritual", "Major Spiritual", "Cleric"]
							
				elif choice == "Armor Use - Spell Hindrance (MnS, MjS, Empath)":
					spell_circles = ["Minor Spiritual", "Major Spiritual", "Empath"]
							
				elif choice == "Armor Use - Spell Hindrance (MnS, MnM)":
					spell_circles = ["Minor Spiritual", "Minor Mental"]
							
				elif choice == "Armor Use - Spell Hindrance (MnS, Paladin)":
					spell_circles = ["Minor Spiritual", "Paladin"]
							
				elif choice == "Armor Use - Spell Hindrance (MnS, Ranger)":
					spell_circles = ["Minor Spiritual", "Ranger"]
							
				elif choice == "Armor Use - Spell Hindrance (MnS, MnE)":
					spell_circles = ["Minor Spiritual", "Minor Elemental"]
							
				elif choice == "Armor Use - Spell Hindrance (MnM, MjM, Savant)":
					spell_circles = ["Minor Mental", "Major Mental", "Savant"]	
					
				elif choice == "Armor Use - Spell Hindrance (MnS, MnE, Sorc)":
					spell_circles = ["Minor Spiritual", "Minor Elemental", "Sorcerer"]
					
				elif choice == "Armor Use - Spell Hindrance (MnE, MjE, Wizard)":
					spell_circles = ["Minor Elemental", "Major Elemental", "Wizard"]
									
				self.Formula_Spell_Hindrance(spell_circles)		
				
			elif choice == "Multi Opponent Combat - FoF, Mstrike":				
				self.Formula_Multi_Opponent_Combat()	
				
			else:
				print("ERROR!!! Progression choice is not implemented!")
				self.Plot_Graph_Clear()
				return			

		elif category == "Magical Skills":			
			if choice == "Arcane Symbols - CS, Max Spell, Duration":
				self.Formula_AS_MIU("Arcane Symbols")
			elif choice == "Magic Item Use - CS, Max Spell, Duration":
				self.Formula_AS_MIU("Magic Item Use")
			elif choice == "Mana Control - Mana Pulse & Spellup":				
				self.Formula_Mana_Control()			

			elif "Summations" in choice:			
				if choice == "Elemental Lore, Air - Summations":
					lore = ["Elemental Lore, Air"]		
					
				elif choice == "Elemental Lore, Earth - Summations":
					lore = ["Elemental Lore, Earth"]	
					
				elif choice == "Elemental Lore, Fire - Summations":
					lore = ["Elemental Lore, Fire"]
					
				elif choice == "Elemental Lore, Water - Summations":
					lore = ["Elemental Lore, Water"]						
					
				elif choice == "Elemental Lore, Multiple - Summations":
					lore = ["Elemental Lore, Air", "Elemental Lore, Earth", "Elemental Lore, Fire", "Elemental Lore, Water"]
					summation_mode = 1
			
				elif choice == "Spiritual Lore, Blessings - Summations":
					lore = ["Spiritual Lore, Blessings"]			
					
				elif choice == "Spiritual Lore, Summoning - Summations":
					lore = ["Spiritual Lore, Summoning"]
					
				elif choice == "Spiritual Lore, Religion - Summations":
					lore = ["Spiritual Lore, Religion"]					
					
				elif choice == "Spiritual Lore, Multiple - Summations":
					lore = ["Spiritual Lore, Blessings", "Spiritual Lore, Religion", "Spiritual Lore, Summoning"]
					summation_mode = 1
			
				elif choice == "Sorcerous Lore, Demonology - Summations":
					lore = ["Sorcerous Lore, Demonology"]				
					
				elif choice == "Sorcerous Lore, Necromancy - Summations":
					lore = ["Sorcerous Lore, Necromancy"]
					
				elif choice == "Mental Lore, Divination - Summations":
					lore = ["Mental Lore, Divination"]			
					
				elif choice == "Mental Lore, Manipulation - Summations":
					lore = ["Mental Lore, Manipulation"]	
					
				elif choice == "Mental Lore, Telepathy - Summations":
					lore = ["Mental Lore, Telepathy"]
					
				elif choice == "Mental Lore, Transference - Summations":
					lore = ["Mental Lore, Transference"]			
					
				elif choice == "Mental Lore, Transformation - Summations":
					lore = ["Mental Lore, Transformation"]			
					
				self.Formula_Summation_Bonuses(lore, summation_mode)						
			
			else:
				print("ERROR!!! Progression choice is not implemented!")
				self.Plot_Graph_Clear()
				return		
				
		elif category == "General Skills":			
			if choice == "First Aid - Bandage Duration & Herb RT":				
				self.Formula_First_Aid()	
			elif choice == "Trading - Skill Boost":				
				self.Formula_Trading()	
				
			else:
				print("ERROR!!! Progression choice is not implemented!")
				self.Plot_Graph_Clear()
				return		
				
		elif category == "Other":			
			if choice == "Bard Spellsong Duration":				
				self.Formula_Spellsong()	
			elif choice == "Empath Imprint Chance & Maximum":
				self.Formula_Imprint()
			elif choice == "Encumbrance":
				self.Formula_Encumbrance()
			elif choice == "Redux":
				self.Formula_Redux()
			elif choice == "Resources Maximums & Recovery":				
				self.Formula_Resources()	
			elif choice == "Spellburst":				
				self.Formula_Spellburst()					
				
			else:
				print("ERROR!!! Progression choice is not implemented!")
				self.Plot_Graph_Clear()
				return		
		
		else:
			print("ERROR!!! Unknown Category selected")
			return
		
		
		# Plot the data stored in the graph_information object
		for i in range(self.graph_information.graph_num_lines):
			a.plot(self.graph_information.graph_xaxis_tick_range, self.graph_information.graph_data_lists[i], self.graph_information.graph_legend_styles[i], label=self.graph_information.graph_legend_labels[i])			
		
		# Set up the graph figure's look before showing it
#		a.tick_params(labelsize=8)   													# both x and y
		a.xaxis.set_tick_params(labelsize=self.graph_information.graph_xlabel_size) 	# just x		

		# major ticks every 10, minor ticks every 1                                       
		mtick = math.floor(len(self.graph_information.graph_xaxis_tick_range)/10)
		if mtick == 0:
			mtick = 1
		major_ticks = np.arange(0, len(self.graph_information.graph_xaxis_tick_range), mtick)     				
		minor_ticks = np.arange(0, len(self.graph_information.graph_xaxis_tick_range), 1)                                               

		a.set_xticklabels(self.graph_information.graph_xaxis_tick_labels, rotation=self.graph_information.graph_xaxis_rotation)
		a.set_xticks(major_ticks)                                                       
		a.set_xticks(minor_ticks, minor=True)     			
			
		# Create the graph legend
		handles, labels = a.get_legend_handles_labels()		
		a.legend(handles, labels, ncol=self.graph_information.graph_legend_columns, loc='upper left', prop={'size':9}, bbox_to_anchor=(0, 1.25))
		
		a.set_ylim(self.graph_information.graph_yaxis_min, self.graph_information.graph_yaxis_max)
		a.set_xlabel(self.graph_information.graph_xlabel, fontsize=self.graph_information.graph_xaxis_size)
		a.set_ylabel(self.graph_information.graph_ylabel)
		

		# Finally, show the the graph figure
		self.graph_figure.canvas.draw()


	# Clicking any part of the graph will set the tooltip variable and display information in the tooltip frame
	def Graph_Marker_Onclick(self, event):
		if event.xdata == None or len(self.graph_information.tooltip_array) == 0:
			return
			
#		print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata))
		xloc = int(round(event.xdata))

		if len(self.graph_information.tooltip_array) > xloc:
			self.graph_tooltip_text.set(self.graph_information.tooltip_array[xloc])
		else: 
			self.graph_tooltip_text.set(self.graph_information.tooltip_array[-1])		
		
		self.graph_tooltip_frame.yview("moveto", 0, "units")	
		
	
	# When the user picks a new category, change the subcategory list to reflect the new choice
	def Graph_Option_Category_OnChange(self, choice):
		self.graph_option_subcategory_menu["menu"].insert_command("end", label="buffer")
		self.graph_option_subcategory_menu['menu'].delete(0, "end")
		list = ["Unknown Category"]
		
		if choice == "Physical Combat":
			list = self.subcategory_list_physical	
		elif choice == "Magical Combat":
			list = self.subcategory_list_magical	
		elif choice == "Physical Skills":
			list = self.subcategory_list_skills_physical
		elif choice == "Magical Skills":
			list = self.subcategory_list_skills_magical	
		elif choice == "General Skills":
			list = self.subcategory_list_skills_general	
		elif choice == "Other":
			list = self.subcategory_list_other	
					
		self.graph_option_subcategory.set(list[0])
		for i in list:	
			self.graph_option_subcategory_menu["menu"].insert_command("end", label=i, command=lambda v=i: self.Graph_Option_Subcategory_OnChange(v))		

	
	# Sets the drop menu to display the user's choice
	def Graph_Option_Subcategory_OnChange(self, choice):
		self.graph_option_subcategory.set(choice)
		
		
	def Gear_List_Populate_Lists(self):		
		globals.character.loadout_gear_build_list 
		globals.character.loadout_effects_build_list
		
		# Delete all the existing items from each list. The inserting of the "temp" command prevents delete(0, end) from throwing an error if the list is empty
		self.gear_main_weapon_menu['menu'].insert_command("end", label="temp")
		self.gear_other_hand_menu['menu'].insert_command("end", label="temp")
		self.gear_armor_menu['menu'].insert_command("end", label="temp")
		self.gear_uac_gloves_menu['menu'].insert_command("end", label="temp")
		self.gear_uac_boots_menu['menu'].insert_command("end", label="temp")		
		self.gear_main_weapon_menu['menu'].delete(0, "end")
		self.gear_other_hand_menu['menu'].delete(0, "end")
		self.gear_armor_menu['menu'].delete(0, "end")
		self.gear_uac_gloves_menu['menu'].delete(0, "end")
		self.gear_uac_boots_menu['menu'].delete(0, "end")	
			
		# Insert the default gear items and set them to be the currently equipped gear
		self.gear_main_weapon_menu['menu'].insert_command("end", label=self.base_main_weapon.name.get(), command=lambda v=self.base_main_weapon.name.get(): self.gear_main_weapon.set(v))
		self.gear_other_hand_menu['menu'].insert_command("end", label=self.base_other_hand.name.get(), command=lambda v=self.base_other_hand.name.get(): self.gear_other_hand.set(v))
		self.gear_armor_menu['menu'].insert_command("end", label=self.base_armor.name.get(), command=lambda v=self.base_armor.name.get(): self.gear_armor.set(v))
		self.gear_uac_gloves_menu['menu'].insert_command("end", label=self.base_uac_gloves.name.get(), command=lambda v=self.base_uac_gloves.name.get(): self.gear_uac_gloves.set(v))
		self.gear_uac_boots_menu['menu'].insert_command("end", label=self.base_uac_boots.name.get(), command=lambda v=self.base_uac_boots.name.get(): self.gear_uac_boots.set(v))	
		self.gear_main_weapon.set(self.base_main_weapon.name.get())
		self.gear_other_hand.set(self.base_other_hand.name.get())
		self.gear_armor.set(self.base_armor.name.get())
		self.gear_uac_gloves.set(self.base_uac_gloves.name.get())
		self.gear_uac_boots.set(self.base_uac_boots.name.get())	

		# Go through the loadout gear list and add all the items the appropriate lists
		for gear in globals.character.loadout_gear_build_list:
			type = gear.display_type.get()
			name = gear.ProgP_display_name		
			
			if type == "Armor":
				self.gear_armor_menu['menu'].insert_command("end", label=name, command=lambda v=name: self.Gear_List_Onchange("Armor", v))
			elif type == "Shield":
				self.gear_other_hand_menu['menu'].insert_command("end", label=name, command=lambda v=name: self.Gear_List_Onchange("Other Hand", v))
			elif type == "UAC" and "UAC Gloves" in name:
				self.gear_uac_gloves_menu['menu'].insert_command("end", label=name, command=lambda v=name: self.Gear_List_Onchange("UAC Gloves", v))
			elif type == "UAC" and "UAC Boots" in name: 
				self.gear_uac_boots_menu['menu'].insert_command("end", label=name, command=lambda v=name: self.Gear_List_Onchange("UAC Boots", v))
			elif type == "THW" or type == "Ranged" or type == "OHE/THW" or name == "Whip-blade" or (name != "Trident, One-Handed" and type == "Polearm"):
				self.gear_main_weapon_menu['menu'].insert_command("end", label=name, command=lambda v=name: self.Gear_List_Onchange("Main Weapon", v))
			elif type == "Brawling" or type == "OHE" or type == "OHB" or type == "Thrown" or type == "OHE/BRW" or name == "Trident, One-Handed":
				self.gear_main_weapon_menu['menu'].insert_command("end", label=name, command=lambda v=name: self.Gear_List_Onchange("Main Weapon", v))
				self.gear_other_hand_menu['menu'].insert_command("end", label=name, command=lambda v=name: self.Gear_List_Onchange("Other Hand", v))
				
	
	# When a choice in a gear drop down menu is selected, set it as equipped gear for that menu
	def Gear_List_Onchange(self, type, gear_name):
		if type == "Armor":
			self.gear_armor.set(gear_name)			
		elif type == "UAC Gloves":
			self.gear_uac_gloves.set(gear_name)			
		elif type == "UAC Boots":
			self.gear_uac_boots.set(gear_name)
		elif type == "Main Weapon":
			self.gear_main_weapon.set(gear_name)
			if gear_name != "Closed Fist":
				main_weapon = self.Get_Gear_By_Order(self.gear_main_weapon.get())
				
				if self.gear_other_hand.get() != "Empty":
					other_hand = self.Get_Gear_By_Order(self.gear_other_hand.get())
					display = main_weapon.display_type.get()
					if main_weapon.order.get() == other_hand.order.get() or display == "THW" or (display == "Ranged" and other_hand.name.get() != "Arrows/Bolts") or (main_weapon.ProgP_display_name != "Trident, One-Handed" and display == "Polearm"):
						self.gear_other_hand.set("Empty")						
		elif type == "Other Hand":
			self.gear_other_hand.set(gear_name)		
			if gear_name != "Empty":
				other_hand = self.Get_Gear_By_Order(self.gear_other_hand.get())				
				
				if self.gear_main_weapon.get() != "Closed Fist":
					main_weapon = self.Get_Gear_By_Order(self.gear_main_weapon.get())
					display = main_weapon.display_type.get()
					if main_weapon.order.get() == other_hand.order.get() or display == "THW" or (display == "Ranged" and other_hand.name.get() != "Arrows/Bolts") or (other_hand.ProgP_display_name != "Trident, One-Handed" and display == "Polearm"):
						self.gear_main_weapon.set("Closed Fist")
	
	
	# Gets gear by it's the order number which is it's location in the Loadout Panel's gear list. Default gear items just return themselves
	def Get_Gear_By_Order(self, gear_name):	
		if gear_name == "Closed Fist":
			return self.base_main_weapon
		elif gear_name == "Empty":
			return self.base_other_hand
		elif gear_name == "No Armor":
			return self.base_armor
		elif gear_name == "No Gloves":
			return self.base_uac_gloves
		elif gear_name == "No Boots":
			return self.base_uac_boots
			
		order = int(gear_name.split(".")[0]) - 1		
		return globals.character.loadout_gear_build_list[order]
		
	
	# Goes through the Effects List created by the Loadout Panel and creates (or adds back) the ProP_row of each effect object.
	# Effects must be unique. Only the first effect with a given is used. Duplicates are skipped.
	def Effects_List_Populate_List(self):	
		effects_list = globals.character.loadout_effects_build_list
		added_effect_names = []
		
		i = 0
		for effect in effects_list:
			if effect.name.get() in added_effect_names:
				if effect.ProgP_Build_Row != "":
					effect.ProgP_Build_Row.grid_remove()				
				continue
			
			added_effect_names.append(effect.name.get())
			
			if effect.ProgP_Build_Row == "":
				effect.Create_ProgP_row(self.Effect_List_Frame.interior())
				effect.ProgP_Build_Row.grid(row=i, column=0)
			else:
				effect.ProgP_Build_Row.grid_remove()
				effect.ProgP_Build_Row.grid(row=i, column=0)
				
			i += 1
				
		self.Gear_List_Frame.yview("moveto", 0, "units")
		

	# Toggles the hide buttons of all effects in the Effects List frame
	def Effects_Toggle_Button_Onclick(self):
		self.effects_list_toggle = (self.effects_list_toggle + 1) % 2
		effects_list = globals.character.loadout_effects_build_list
		
		for effect in effects_list:
			effect.hide.set(self.effects_list_toggle)
		

	# This allows mouse scrolling in the build frame. Anything with the bind tag ProgP_Effect will allow the scrolling
	def Scroll_Effects_Frame(self, event):
		self.Effect_List_Frame.yview("scroll", -1*(event.delta/120), "units")				

		
	# This allows mouse scrolling in the build frame. Anything with the bind tag ProgP_Effect will allow the scrolling
	def Scroll_Tooltip_Frame(self, event):
		self.graph_tooltip_frame.yview("scroll", -1*(event.delta/120), "units")				
						

	# Get a list of override options from any effect that is relavant to the formula being calculated. 
	# What will be done with the override options is handled individually in each formula method.
	def Find_Overrides_By_Tags(self, effect_tags):
		effects_list = globals.character.loadout_effects_build_list		
		override_list = []
		parts = []
				
		# Ignore effects that are not visible or in the Progression Panel's effects list frame
		for effect in effects_list:
			if effect.hide.get() == "1" or effect.ProgP_Build_Row == "" or (effect.ProgP_Build_Row != "" and len(effect.ProgP_Build_Row.grid_info()) == 0):
				continue
			
			tag_list = effect.effect_tags.split("|")	
			
			for etag in tag_list:
				for tag in effect_tags:
					if etag == tag:						
						if effect.options != "NONE":
							parts = effect.options.split("|")
							
							for option in parts:
								if option not in override_list:
									override_list.append(option)
							

		return override_list
		
						
	# Part of sorting the effects, this method will figure out which effects in the loadout effects list are relavant to what formuala is being
	# calculated on the Progression Panel and add each effect to one or more keys in the dict, matching_arr. 
	# The effect_tags list determines what effects we are looking for
	def Find_Effects_By_Tags(self, effect_tags):
		effects_list = globals.character.loadout_effects_build_list		
		matching_arr = {}
		parts = []
		
		for tag in effect_tags:
			matching_arr[tag] = []		
		
		# Ignore effects that are not visible or in the Progression Panel's effects list frame
		for effect in effects_list:
			if effect.hide.get() == "1" or effect.ProgP_Build_Row == "" or (effect.ProgP_Build_Row != "" and len(effect.ProgP_Build_Row.grid_info()) == 0):
				continue
			
			tag_list = effect.effect_tags.split("|")	
			
			for etag in tag_list:
				for tag in effect_tags:
					if etag == tag:
						matching_arr[tag].append(effect)										

						
		return matching_arr
					
						
	# Given a specific tag to look for, an effects_arr to search through, and an action_type to format the return data:
	# Combine_Effects will get the total bonus for an effect from all the effects in effects_arr. Calculate_Tag_Bonus
	# is called on each effect to execute a specfic internal method to calculate the data. This always returns an list
	# of 2 elements: 1st being the bonus and the 2nd being the type of the bonus
	def Combine_Effects(self, level, effect_name, base_value, effects_lists_arr, tag_arr, action_type):
		temp_arr = []
		temp_value = 0
		sum = 0
		tooltip = ""
		temp_tooltip = ""
		indenting = "            "		
		
		if action_type == "stat_inc_to_bonus":
			effects_arr = effects_lists_arr[0]
			tag = tag_arr[0]			
			for effect in effects_arr:
				temp_arr = effect.Calculate_Tag_Bonus(tag, level)
				if temp_arr[0] == 0:           						
					continue		
				tooltip += "%s%s  bonus  (%s)\n" % ( indenting,  ("%+d" % temp_arr[0]).rjust(4), temp_arr[1])
				sum += temp_arr[0]		
		
			effects_arr = effects_lists_arr[1]
			tag = tag_arr[1]		
			for effect in effects_arr:
				temp_arr = effect.Calculate_Tag_Bonus(tag, level)
				if temp_arr[0] == 0:           						
					continue
				tooltip += "%s%s bonus  (%+d %s)\n" % ( indenting,  ("%+d" % (temp_arr[0]/2)).rjust(4),   temp_arr[0],   temp_arr[1])
				sum += temp_arr[0]/2					

			if sum > 0:
				tooltip = "       %s  enhancive %s bonus (%s vs max +20)\n" % (("%+d" % min(20, sum)).rjust(4), effect_name, "%+d" % (sum)) + tooltip

		
		elif action_type == "stat_bonus_to_inc":
			effects_arr = effects_lists_arr[0]
			tag = tag_arr[0]			
			for effect in effects_arr:
				temp_arr = effect.Calculate_Tag_Bonus(tag, level)
				if temp_arr[0] == 0:           						
					continue		
				tooltip += "%s%s statistic increase  (%s)\n" % ( indenting,  ("%+d" % (temp_arr[0]*2)).rjust(4), temp_arr[1])
				sum += temp_arr[0] * 2		
		
			effects_arr = effects_lists_arr[1]
			tag = tag_arr[1]		
			for effect in effects_arr:
				temp_arr = effect.Calculate_Tag_Bonus(tag, level)
				if temp_arr[0] == 0:           						
					continue
				tooltip += "%s%s statistic increase  (%+d %s)\n" % ( indenting,  ("%+d" % temp_arr[0]).rjust(4),   temp_arr[0],   temp_arr[1])
				sum += temp_arr[0]					

			if sum > 0:
				tooltip = "       %s  enhancive %s statistic increase (%s vs max +40)\n" % (("%+d" % min(40, sum)).rjust(4), effect_name, "%+d" % (sum)) + tooltip				
				
				
		elif action_type == "skill_bonus_to_ranks":
			effects_arr = effects_lists_arr[0]
			tag = tag_arr[0]		
			for effect in effects_arr:
				temp_arr = effect.Calculate_Tag_Bonus(tag, level)
				if temp_arr[0] == 0:           						
					continue					
				temp_value = calculations.Convert_Bonus_To_New_Ranks(base_value, temp_arr[0])
				tooltip += "%s%s ranks  (%+d %s)\n" % (indenting,  ("%+d" % temp_value).rjust(4), temp_arr[0], temp_arr[1])
				sum += temp_value	

			effects_arr = effects_lists_arr[1]
			tag = tag_arr[1]		
			for effect in effects_arr:
				temp_arr = effect.Calculate_Tag_Bonus(tag, level)
				if temp_arr[0] == 0:           						
					continue
				tooltip += "%s%s ranks  (%s)\n" % ( indenting,  ("%+d" % temp_arr[0]).rjust(4), temp_arr[1])
				sum += temp_arr[0]							

			if sum > 0:
				tooltip = "       %s  enhancive %s ranks (%s vs max +50)\n" % (("%+d" % min(50, sum)).rjust(4), effect_name, "%+d" % (sum)) + tooltip
				
			if len(effects_lists_arr) > 2:
				effects_arr = effects_lists_arr[2]
				tag = tag_arr[2]		
				temp_value = 0
				temp_tooltip = ""
				for effect in effects_arr:
					temp_arr = effect.Calculate_Tag_Bonus(tag, level)
					if temp_arr[0] == 0:           						
						continue
					temp_tooltip += "%s%s %s  (%s)\n" % (indenting,  ("%+d" % temp_arr[0]).rjust(4),  temp_arr[1],  effect.name.get())
					temp_value += temp_arr[0]		
				sum += temp_value				
				
				if temp_value > 0:
					tooltip += "       %s  %s phantom ranks\n" % (("%+d" % temp_value).rjust(4), effect_name) + temp_tooltip					
					

		elif action_type == "skill_ranks_to_bonus":
			effects_arr = effects_lists_arr[0]
			tag = tag_arr[0]		
			for effect in effects_arr:
				temp_arr = effect.Calculate_Tag_Bonus(tag, level)
				if temp_arr[0] == 0:           						
					continue					
				tooltip += "%s%s bonus  (%s)\n" % ( indenting,  ("%+d" % temp_arr[0]).rjust(4), temp_arr[1])
				sum += temp_arr[0]	

			effects_arr = effects_lists_arr[1]
			tag = tag_arr[1]		
			for effect in effects_arr:
				temp_arr = effect.Calculate_Tag_Bonus(tag, level)
				if temp_arr[0] == 0:           						
					continue
				temp_value = calculations.Convert_Ranks_To_New_Bonus(base_value, temp_arr[0])
				tooltip += "%s%s bonus  (%d %s)\n" % (indenting,  ("%+d" % temp_value).rjust(4), temp_arr[0], temp_arr[1])
				sum += temp_value	

			if sum > 0:
				tooltip = "       %s  enhancive %s bonus (%s vs max +50)\n" % (("%+d" % min(50, sum)).rjust(4), effect_name, "%+d" % sum) + tooltip

				
			if len(effects_lists_arr) > 2:
				effects_arr = effects_lists_arr[2]
				tag = tag_arr[2]		
				temp_value = 0
				temp_value2 = 0
				temp_tooltip = ""
				for effect in effects_arr:
					temp_arr = effect.Calculate_Tag_Bonus(tag, level)
					if temp_arr[0] == 0:           						
						continue
					temp_tooltip += "%s%s %s  (%s)\n" % (indenting,  ("%+d" % temp_arr[0]).rjust(4),  temp_arr[1],  effect.name.get())
					temp_value += calculations.Convert_Ranks_To_New_Bonus(base_value, temp_arr[0])
					temp_value2 += temp_arr[0]		
				sum += temp_value				
				
				if temp_value > 0:
					tooltip += "       %s  bonus from %s %s phantom ranks\n" % (("%+d" % temp_value).rjust(4), temp_value2, effect_name) + temp_tooltip	
				
			
		elif action_type == "effect_display":
			arr_length = len(effects_lists_arr)
			
			for i in range(arr_length):
				effects_arr = effects_lists_arr[i]
				tag = tag_arr[i]
				for effect in effects_arr:					
					temp_arr = effect.Calculate_Tag_Bonus(tag, level)
					if temp_arr[0] == 0:           						
						continue
					tooltip += "%s%s %s  (%s)\n" % (indenting,  ("%+d" % temp_arr[0]).rjust(4),  temp_arr[1],  effect.name.get())
					sum += temp_arr[0]	
					

		elif action_type == "effect_display_2":
			arr_length = len(effects_lists_arr)
			
			for i in range(arr_length):
				effects_arr = effects_lists_arr[i]
				tag = tag_arr[i]
				for effect in effects_arr:					
					temp_arr = effect.Calculate_Tag_Bonus(tag, level)
					if temp_arr[0] == 0:           						
						continue
					tooltip += "%s%s  %s  (%s)\n" % ("      ",  ("%+d" % temp_arr[0]).rjust(4),  temp_arr[1],  effect.name.get())
					sum += temp_arr[0]	
					
					
		elif action_type == "float_format":
			effects_arr = effects_lists_arr[0]
			tag = tag_arr[0]		
			for effect in effects_arr:
				temp_arr = effect.Calculate_Tag_Bonus(tag, level)
				if temp_arr[0] == 0:           						
					continue					
				tooltip += "%s%s bonus  (%s)\n" % ("    ",  ("%+.2f" % temp_arr[0]).rjust(4), effect.name.get())
				sum += temp_arr[0]	
					

		elif action_type == "AAP_display":
			arr_length = len(effects_lists_arr)
			
			for i in range(arr_length):
				effects_arr = effects_lists_arr[i]
				tag = tag_arr[i]
				for effect in effects_arr:					
					temp_arr = effect.Calculate_Tag_Bonus(tag, level)
					if temp_arr[0] == 0:           						
						continue
					tooltip += "%s%s %s  (%s)\n" % ("  ",  ("%+d" % temp_arr[0]).rjust(4),  temp_arr[1],  effect.name.get())
					sum += temp_arr[0]	
					
					
		elif action_type == "spellburst_float_format":
			effects_arr = effects_lists_arr[0]
			tag = tag_arr[0]		
			for effect in effects_arr:
				temp_arr = effect.Calculate_Tag_Bonus(tag, level)
				if temp_arr[0] == 0:           						
					continue					
				tooltip += "%s%s %s  (%s)\n" % ("    ",  ("%.1f" % temp_arr[0]).rjust(4), temp_arr[1], effect.name.get())
				sum += temp_arr[0]	

					
		return (sum, tooltip)


	# Set the x and y axis labels of the graph plot along with the sizes tick ranges too.
	# The x axis tick labels and values will vary depending on if the the radio button is
	# set to pre-cap mode or post-cap mode. In addtion, the post-cap mode section will determine
	# what the post-cap loop range is based on the post-cap intervals in which the character
	# trained in a relavant skill.
	def Set_Graph_Labels(self, skill_names, xlabel, ylabel):
		postcap_intervals = []		
		self.graph_information.graph_ylabel = ylabel	
		
		if self.graph_radio_var.get() == 1:
			loop_range = [i for i in range(101)]
			self.graph_information.graph_xlabel = "%s per Level" % (xlabel)
			self.graph_information.graph_xaxis_rotation = 0
			self.graph_information.graph_xlabel_size = 12
			self.graph_information.graph_xaxis_size = 12
			self.graph_information.graph_xaxis_tick_range = loop_range
			self.graph_information.graph_xaxis_tick_labels = [0,10,20,30,40,50,60,70,80,90,100]		
			
		# In Postcap mode, loop_range is not 0-100, instead its the first and last time the character trained in something	
		else:
			interval = 7575000
			for interval, training in globals.character.postcap_skill_training_by_interval.items():
				for skill in skill_names:
					if skill in training:
						postcap_intervals.append(interval)
						break										
							
			if len(postcap_intervals) == 0:
				postcap_intervals.append(7572500)
				postcap_intervals.append(interval)
			elif postcap_intervals[0] != 7572500:
				postcap_intervals.insert(0, 7572500)			
			
			if postcap_intervals[-1] != interval:
				postcap_intervals.append(interval)		
							
			loop_range = postcap_intervals
			self.graph_information.graph_xlabel = "%s per Postcap Experience Interval" % (xlabel)
			self.graph_information.graph_xaxis_rotation = 30
			self.graph_information.graph_xlabel_size = 10
			self.graph_information.graph_xaxis_size = 9		
			tick_range_length = len(postcap_intervals)
			self.graph_information.graph_xaxis_tick_range = [i for i in range(tick_range_length)]
			
			if len(postcap_intervals) <= 10:
				self.graph_information.graph_xaxis_tick_labels = [i for i in postcap_intervals]	
			else:
				temp = math.floor(len(postcap_intervals)/10)
				i = 0
								
				for interval in postcap_intervals:
					if i % temp == 0:
						self.graph_information.graph_xaxis_tick_labels.append(interval)
					i += 1					

			
		return loop_range
		

	# This massive method is used to calculate the Attack Strength (AS) of a character from level 0-100 or across
	# postcap training. It can calculate the AS for any weapon type including weapons that use multiple skills
	# like the Katar. It can also calculate Bolt AS and TWC AS as well. All statistics, skills, and effects that
	# increase skills, statistics, or AS itself are included in this calculation.	
	def Formula_Attack_Strength(self, twc_mode, main_gear, ammo_enchantment):	
		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}
		base_bonus_arr = {}
		
		off_hand_text = ""			
		main_enchantment = int(main_gear.enchantment)
		weapon_types = main_gear.skills.split("/")	
			
		off_stance_totals = []
		adv_stance_totals = []
		for_stance_totals = []
		neu_stance_totals = []
		gua_stance_totals = []
		def_stance_totals = []		
		
		# Setup the lists for what skills and stats are relavent for calculate AS
		if weapon_types[0] == "Spell Aiming":
			effects_list = ["Statistic_Dexterity", "Statistic_Bonus_Dexterity", "AS_All", "AS_Bolt"]	
			statistic_names = ["Dexterity"]
			skill_names = []
			effect_type = "AS_Bolt"
		elif weapon_types[0] == "Ranged Weapons":
			effects_list = ["Statistic_Dexterity", "Statistic_Bonus_Dexterity", "Skill_Bonus_Ambush", "Skill_Ranks_Ambush", "Skill_Bonus_Perception", "Skill_Ranks_Perception", "AS_All", "AS_Ranged"]	
			statistic_names = ["Dexterity"]
			skill_names = ["Ambush", "Perception"]
			effect_type = "AS_Ranged"
		elif weapon_types[0] == "Thrown Weapons":
			effects_list = ["Statistic_Strength", "Statistic_Bonus_Strength", "Statistic_Dexterity", "Statistic_Bonus_Dexterity", "Skill_Bonus_Perception", "Skill_Ranks_Perception", "Skill_Phantom_Ranks_Combat_Maneuvers", "Skill_Bonus_Combat_Maneuvers", "Skill_Ranks_Combat_Maneuvers", "AS_All", "AS_Ranged"]	
			statistic_names = ["Dexterity", "Strength"]
			skill_names = ["Combat Maneuvers", "Perception"]
			effect_type = "AS_Ranged"
		else:				
			effects_list = ["Statistic_Strength", "Statistic_Bonus_Strength", "Skill_Phantom_Ranks_Combat_Maneuvers", "Skill_Bonus_Combat_Maneuvers", "Skill_Ranks_Combat_Maneuvers", "AS_All", "AS_Melee"]	
			statistic_names = ["Strength"]
			skill_names = ["Combat Maneuvers"]
			effect_type = "AS_Melee"
		
		# TWC is considered an extra step in the calculation process and needs to add extra skills and effects to calculate it 
		if twc_mode == 1:
			off_hand_text = "Off-hand "
			skill_names.append("Two Weapon Combat")
			effects_list.extend(("Skill_Bonus_Two_Weapon_Combat", "Skill_Ranks_Two_Weapon_Combat"))
			if "Dexterity" not in statistic_names:
				statistic_names.append("Dexterity")
				effects_list.extend(("Statistic_Dexterity", "Statistic_Bonus_Dexterity"))
		
					
		# This is a quicker way to add weapon skill effects to the effects list
		for skill in weapon_types:
			skill_names.append(skill)
			effects_list.append("Skill_Ranks_%s" % skill.replace(" ", "_").replace("-", "_").replace(",", ""))
			effects_list.append("Skill_Bonus_%s" % skill.replace(" ", "_").replace("-", "_").replace(",", ""))
			
			
		override_options = self.Find_Overrides_By_Tags(effects_list)		
		
		# Set the overrides if needed
		for option in override_options:
			if option == "Main Weapon":
				calculations.override_dict["Main Weapon"] = main_gear.name.get()					
			elif option == "Influence Bonus":
				effects_list.extend(("Statistic_Influence", "Statistic_Bonus_Influence"))
				statistic_names.append("Influence")
			elif option == "Wisdom Bonus":
				effects_list.extend(("Statistic_Wisdom", "Statistic_Bonus_Wisdom"))
				statistic_names.append("Wisdom")	
			elif option == "Armor Group":
				calculations.override_dict["Armor Group"] = int(self.Get_Gear_By_Order(self.gear_armor.get()).gear_traits["AG"])						

		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		loop_range = self.Set_Graph_Labels(skill_names, "%s %sAttack Strength" % (main_gear.skills, off_hand_text), "%sAS" % (off_hand_text))		
		
					
		# Begin the big loop to calculate all the data		
		for i in loop_range:
			skill_inc_bonus = 0		
			skill_rank_count = 0
			effects_total = 0
			combined_weapons_bonus = 0
			combined_statistic_bonus = 0
			
			weapon_enhancive_totals = []
			stat_enhancive_totals = []
			
			stat_tooltip_text = ""
			skill_tooltip = ""
			weapon_tooltip_text = ""
			effects_tooltip_text = ""
			weapon_tooltip_arr = []
			
			# Get the base ranks and bonus for each relevant statistic and skill for this level/interval
			if self.calc_style == 1:
				tooltip = "Level %s: %sAttack Strength with %s\n" % (i, off_hand_text, main_gear.skills)
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()	
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: %sAttack Strength with %s\n" % ("{:,}".format(i), off_hand_text, main_gear.skills)
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[100].get()	
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
		

			# Calculate Statistic bonus	
			# TWC has a different way of calculating than the rest of the weapons
			if twc_mode == 1:		
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, "Strength", 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_Strength"], lists_of_effects_by_tag["Statistic_Strength"]], 
												["Statistic_Bonus_Strength", "Statistic_Strength"], 
												"stat_inc_to_bonus")													
				
				combined_strength_bonus = base_stat_arr["Strength"] + min(50, stat_enh_bonus)	
				stat_tooltip_text += "       %s  Strength base bonus\n" % (("%+d" % base_stat_arr["Strength"]).rjust(4)) + temp_tooltip	
				
			
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, "Dexterity", 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_Dexterity"], lists_of_effects_by_tag["Statistic_Dexterity"]], 
												["Statistic_Bonus_Dexterity", "Statistic_Dexterity"], 
												"stat_inc_to_bonus")
				
				combined_dexterity_bonus = base_stat_arr["Dexterity"] + min(50, stat_enh_bonus)		
				stat_tooltip_text += "       %s  Dexterity base bonus\n" % (("%+d" % base_stat_arr["Dexterity"]).rjust(4)) + temp_tooltip	
				
				stat_tooltip_text = "  %s  Statistic bonus: min(Strength %+d vs Dexterity %+d)\n" % (("%+d" % min(combined_strength_bonus, combined_dexterity_bonus)).rjust(4), combined_strength_bonus, combined_dexterity_bonus) + stat_tooltip_text	
				
			# Statistic calculations for every other weapon style	
			else:
				k = 0
				for stat in statistic_names:
					if stat == "Wisdom" or stat == "Influence":
						continue
						
					stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, stat, 0, 
													[lists_of_effects_by_tag["Statistic_Bonus_%s" % stat], lists_of_effects_by_tag["Statistic_%s" % stat]], 
													["Statistic_Bonus_%s" % stat, "Statistic_%s" % stat], 
													"stat_inc_to_bonus")													

					stat_enhancive_totals.append(base_stat_arr[stat] + min(50, stat_enh_bonus))	
					combined_statistic_bonus += base_stat_arr[stat] + min(50, stat_enh_bonus)
					stat_tooltip_text += "       %s  %s base bonus\n" % (("%+d" % base_stat_arr[stat]).rjust(4), stat) + temp_tooltip	
					k += 1									
				combined_statistic_bonus /= k							

								
				if k > 1:	
					mutli_tooltip = ""
					for j in range(k):
						mutli_tooltip = " %s (%s)," % (statistic_names[j], "%+d" % stat_enhancive_totals[j]) + mutli_tooltip
					stat_tooltip_text = "  %s  Statistic bonus avg: %s\n" % (("%+d" % combined_statistic_bonus).rjust(4), mutli_tooltip[:-1]) + stat_tooltip_text
				else:						
					stat_tooltip_text = "  %s  %s bonus\n" % (("%+d" % combined_statistic_bonus).rjust(4), statistic_names[0]) + stat_tooltip_text
			
			
			if weapon_types[0] == "Spell Aiming":	
				if "Influence Bonus" in override_options:
					stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, "Influence", 0, 
													[lists_of_effects_by_tag["Statistic_Bonus_Influence"], lists_of_effects_by_tag["Statistic_Influence"]], 
													["Statistic_Bonus_Influence", "Statistic_Influence"], 
													"stat_inc_to_bonus")		

					calculations.override_dict["Influence Bonus"] = base_stat_arr["Influence"] + stat_enh_bonus
												
				if "Wisdom Bonus" in override_options:
					stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, "Wisdom", 0, 
													[lists_of_effects_by_tag["Statistic_Bonus_Wisdom"], lists_of_effects_by_tag["Statistic_Wisdom"]], 
													["Statistic_Bonus_Wisdom", "Statistic_Wisdom"], 
													"stat_inc_to_bonus")			
													
					calculations.override_dict["Wisdom Bonus"] = base_stat_arr["Wisdom"] + stat_enh_bonus
				
			elif weapon_types[0] == "Ranged Weapons":
				# Calculate Ambush ranks
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Ambush", base_ranks_arr["Ambush"], 
												[lists_of_effects_by_tag["Skill_Bonus_Ambush"], lists_of_effects_by_tag["Skill_Ranks_Ambush"]], 
												["Skill_Bonus_Ambush", "Skill_Ranks_Ambush"], 
												"skill_bonus_to_ranks")

				ambush_total = base_ranks_arr["Ambush"] + min(50, skill_rank_count)		
				skill_tooltip += "  %s  Ambush ranks  ((%s - 40) / 4) vs min +0)\n" % (("%+d" % ( max(0, math.floor(0/4) + math.floor((ambush_total - 40) / 4) )) ).rjust(4), ambush_total) 		
				skill_tooltip += "       %s  Ambush base ranks\n" % (("%+d" % base_ranks_arr["Ambush"]).rjust(4)) 
				skill_tooltip += temp_tooltip							
				
				
				# Calculate Perception ranks
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Perception", base_ranks_arr["Perception"], 
												[lists_of_effects_by_tag["Skill_Bonus_Perception"], lists_of_effects_by_tag["Skill_Ranks_Perception"]], 
												["Skill_Bonus_Perception", "Skill_Ranks_Perception"], 
												"skill_bonus_to_ranks")

				perception_total = base_ranks_arr["Perception"] + min(50, skill_rank_count)		
				skill_tooltip += "  %s  Perception ranks  ((%s - 40) / 4) vs min +0)\n" % (("%+d" % ( max(0, math.floor(0/4) + math.floor((perception_total - 40) / 4) )) ).rjust(4), perception_total)			
				skill_tooltip += "       %s  Perception base ranks\n" % (("%+d" % base_ranks_arr["Perception"]).rjust(4)) 
				skill_tooltip += temp_tooltip											

				
			elif weapon_types[0] == "Thrown Weapons":
				# Calculate Combat Maneuver ranks
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Combat Maneuvers", base_ranks_arr["Combat Maneuvers"], 
												[lists_of_effects_by_tag["Skill_Bonus_Combat_Maneuvers"], lists_of_effects_by_tag["Skill_Ranks_Combat_Maneuvers"], lists_of_effects_by_tag["Skill_Phantom_Ranks_Combat_Maneuvers"]], 
												["Skill_Bonus_Combat_Maneuvers", "Skill_Ranks_Combat_Maneuvers", "Skill_Phantom_Ranks_Combat_Maneuvers"], 
												"skill_bonus_to_ranks")

				cman_total = base_ranks_arr["Combat Maneuvers"] + skill_rank_count
				skill_tooltip += "       %s  Combat Maneuvers base ranks\n" % (("%+d" % base_ranks_arr["Combat Maneuvers"]).rjust(4)) 				
				skill_tooltip += temp_tooltip		

				
				# Calculate Perception ranks
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Perception", base_ranks_arr["Perception"], 
												[lists_of_effects_by_tag["Skill_Bonus_Perception"], lists_of_effects_by_tag["Skill_Ranks_Perception"]], 
												["Skill_Bonus_Perception", "Skill_Ranks_Perception"], 
												"skill_bonus_to_ranks")

				perception_total = base_ranks_arr["Perception"] + min(50, skill_rank_count)			
				skill_tooltip += "       %s  Perception base ranks\n" % (("%+d" % base_ranks_arr["Perception"]).rjust(4)) 			
				skill_tooltip += temp_tooltip		


				skill_tooltip = "  %s  CM ranks + Perception ranks  ((%s + %s) / 4)\n" % (("%+d" % ( math.floor((cman_total + perception_total) / 4) )).rjust(4), cman_total, perception_total) + skill_tooltip	
				
			else:
				# Calculate Combat Maneuver ranks
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Combat Maneuvers", base_ranks_arr["Combat Maneuvers"], 
												[lists_of_effects_by_tag["Skill_Bonus_Combat_Maneuvers"], lists_of_effects_by_tag["Skill_Ranks_Combat_Maneuvers"], lists_of_effects_by_tag["Skill_Phantom_Ranks_Combat_Maneuvers"]], 
												["Skill_Bonus_Combat_Maneuvers", "Skill_Ranks_Combat_Maneuvers", "Skill_Phantom_Ranks_Combat_Maneuvers"], 
												"skill_bonus_to_ranks")

				cman_total = base_ranks_arr["Combat Maneuvers"] + skill_rank_count		
				skill_tooltip = "  %s  Combat Maneuver ranks  (%s / 2)\n" % (("%+d" % (cman_total/2)).rjust(4), cman_total) 		
				skill_tooltip += "       %s  %s base ranks\n" % (("%+d" % base_ranks_arr["Combat Maneuvers"]).rjust(4), "Combat Maneuvers") 				
				skill_tooltip += temp_tooltip				
				
					
			# Calculate Weapon Skill bonus. Takes several weapons skills into account in the case of Katana, Katar, or similar
			for skill in weapon_types:		
				tag_name_sub = skill.replace(" ", "_").replace("-", "_").replace(",", "")		

				weapon_inc_bonus, temp_tooltip = self.Combine_Effects(i, skill, base_bonus_arr[skill], 
												[lists_of_effects_by_tag["Skill_Bonus_%s" % tag_name_sub], lists_of_effects_by_tag["Skill_Ranks_%s" % tag_name_sub]], 
												["Skill_Bonus_%s" % tag_name_sub, "Skill_Ranks_%s" % tag_name_sub], 
												"skill_ranks_to_bonus")

				weapon_enhancive_totals.append(base_bonus_arr[skill] + min(50, weapon_inc_bonus) )				
				combined_weapons_bonus += base_bonus_arr[skill] + min(50, weapon_inc_bonus) 	
				weapon_tooltip_text += "       %s bonus from %s %s base ranks\n" % (("%+d" % base_bonus_arr[skill]).rjust(4), base_ranks_arr[skill], skill) 
				weapon_tooltip_text += temp_tooltip
				
			combined_weapons_bonus /= len(weapon_types)							

			# In TWC mode, we need to calculate the TWC bonus
			if twc_mode == 1:	
				twc_inc_bonus, temp_tooltip = self.Combine_Effects(i, "Two Weapon Combat", base_ranks_arr["Two Weapon Combat"], 
												[lists_of_effects_by_tag["Skill_Bonus_Two_Weapon_Combat"], lists_of_effects_by_tag["Skill_Ranks_Two_Weapon_Combat"]], 
												["Skill_Bonus_Two_Weapon_Combat", "Skill_Ranks_Two_Weapon_Combat"], 
												"skill_ranks_to_bonus")

				combined_twc_bonus = base_bonus_arr["Two Weapon Combat"] + min(50, twc_inc_bonus) 	
				weapon_tooltip_text = "       %s bonus from %s Two Weapon Combat base ranks\n" % (("%+d" % base_bonus_arr["Two Weapon Combat"]).rjust(4), base_ranks_arr["Two Weapon Combat"]) + temp_tooltip + weapon_tooltip_text	
				
			
			# Create the tooltip for the weapons part
			if len(weapon_types) > 1:	
				mutli_tooltip = ""
				for j in range(len(weapon_types)):
					mutli_tooltip = " %s (%s)," % (weapon_types[j], "%+d" % weapon_enhancive_totals[j]) + mutli_tooltip
					
				if twc_mode == 1:
					weapon_tooltip_text = "       %s  Skill bonus avg: %s\n" % (("%+d" % combined_weapons_bonus).rjust(4), mutli_tooltip[:-1]) + weapon_tooltip_text
					weapon_tooltip_text = "  %s  Off-hand %s skill bonus (3/5 * %+d) + (2/5 * %+d) \n" % (("%+d" % ((3/5 * combined_weapons_bonus) + (2/5 * combined_twc_bonus)) ).rjust(4), main_gear.skills,  combined_weapons_bonus, combined_twc_bonus) + weapon_tooltip_text
				else:
					weapon_tooltip_text = "  %s  Skill bonus avg: %s\n" % (("%+d" % combined_weapons_bonus).rjust(4), mutli_tooltip[:-1]) + weapon_tooltip_text
					
			elif twc_mode == 1:
				weapon_tooltip_text = "  %s  Off-hand %s skill bonus (3/5 * %+d) + (2/5 * %+d) \n" % (("%+d" % ((3/5 * combined_weapons_bonus) + (2/5 * combined_twc_bonus)) ).rjust(4), weapon_types[0],  combined_weapons_bonus, combined_twc_bonus) + weapon_tooltip_text
			else:
				weapon_tooltip_text = "  %s  %s skill bonus\n" % (("%+d" % combined_weapons_bonus).rjust(4), weapon_types[0]) + weapon_tooltip_text
			
			
			weapon_tooltip_arr.append(weapon_tooltip_text)	

			
			# Calculate total of AS_All	and either AS_Melee, AS_Ranged, or AS_Bolt	
			effects_total, effects_tooltip_text = self.Combine_Effects(i, "", 0, 
											[lists_of_effects_by_tag["AS_All"], lists_of_effects_by_tag[effect_type]], 
											["AS_All", effect_type], 
											"effect_display")			

			if effects_tooltip_text != "":
					effects_tooltip_text = "  %s  bonus from Attack Strength effects\n" % (("%+d" % effects_total).rjust(4)) + effects_tooltip_text								
						
									
			
			if twc_mode == 1:
				value = min(combined_strength_bonus, combined_dexterity_bonus) + math.floor( ((3/5 * combined_weapons_bonus) + (2/5 * combined_twc_bonus)) ) + math.floor(cman_total / 2) + main_enchantment + effects_total	
			elif weapon_types[0] == "Spell Aiming":		
				value = combined_statistic_bonus + math.floor(combined_weapons_bonus) + effects_total				
			elif weapon_types[0] == "Thrown Weapons":
				value = combined_statistic_bonus + math.floor(combined_weapons_bonus) + math.floor((cman_total + perception_total) / 4) + effects_total	
			elif weapon_types[0] == "Ranged Weapons":	
				value = combined_statistic_bonus + math.floor(combined_weapons_bonus) + max(0, math.floor(0/4) + math.floor((ambush_total - 40) / 4) ) + max(0, math.floor((perception_total - 40) / 4)) + min(50, main_enchantment+ammo_enchantment) + effects_total				
			else:										
				value = combined_statistic_bonus + math.floor(combined_weapons_bonus) + math.floor(cman_total / 2) + main_enchantment + effects_total		
				
			# Calculate the AS in each stance
			off_stance_totals.append(value * 1.0)
			neu_stance_totals.append(value * 0.7)
			adv_stance_totals.append(value * 0.9)
			gua_stance_totals.append(value * 0.6)
			for_stance_totals.append(value * 0.8)
			def_stance_totals.append(value * 0.5)
			
			# Create Tooltip
			weapon_tooltip_text = ""	
			for text in weapon_tooltip_arr:
				weapon_tooltip_text += text
				
			tooltip = "".join( [ tooltip,
						"%+s = %+d * 1.0  (Offensive Stance)\n" % (("%+d" % off_stance_totals[index]).rjust(4), value),
						"%+s = %+d * 0.9  (Advanced Stance)\n" % (("%+d" % adv_stance_totals[index]).rjust(4), value),
						"%+s = %+d * 0.8  (Forward Stance)\n" % (("%+d" % for_stance_totals[index]).rjust(4), value),
						"%+s = %+d * 0.7  (Neutral Stance)\n" % (("%+d" % neu_stance_totals[index]).rjust(4), value),
						"%+s = %+d * 0.6  (Guarded Stance)\n" % (("%+d" % gua_stance_totals[index]).rjust(4), value),
						"%+s = %+d * 0.5  (Defensive Stance)\n" % (("%+d" % def_stance_totals[index]).rjust(4), value),
						"%+d calculated with:\n" % value
						])			
			
			if weapon_types[0] == "Ranged Weapons":						
				tooltip = "".join( [ tooltip,
							"  %s  Combined enchantment bonus (%+d vs max +50)\n" % (("%+d" % min(50, main_enchantment+ammo_enchantment)).rjust(4), main_enchantment+ammo_enchantment),
							"      %s  Enchantment bonus of %s\n" % (("%+d" % main_enchantment).rjust(4), main_gear.name.get()),
							"      %s  Enchantment bonus of Arrows/Bolts\n" % (("%+d" % ammo_enchantment).rjust(4))
							])
							
			elif weapon_types[0] != "Spell Aiming":					
				tooltip = "".join( [ tooltip,
							"  %s  Enchantment bonus of %s\n" % (("%+d" % main_enchantment).rjust(4), main_gear.name.get())
							])

			tooltip = "".join( [ tooltip,
						stat_tooltip_text,
						weapon_tooltip_text,
						skill_tooltip,
						effects_tooltip_text
						])

			
			self.graph_information.tooltip_array.append(tooltip[:-1])					

			index += 1
					

					
		# Loop is done, set up the graph_infomation object						
		
		self.graph_information.graph_yaxis_min = min(def_stance_totals[0], off_stance_totals[0]) - 5
		self.graph_information.graph_yaxis_max = max(def_stance_totals[-1], off_stance_totals[-1]) + 5
		self.graph_information.graph_data_lists.append(off_stance_totals)
		self.graph_information.graph_data_lists.append(adv_stance_totals)
		self.graph_information.graph_data_lists.append(for_stance_totals)
		self.graph_information.graph_data_lists.append(neu_stance_totals)
		self.graph_information.graph_data_lists.append(gua_stance_totals)
		self.graph_information.graph_data_lists.append(def_stance_totals)

		# Legend Information
		self.graph_information.graph_num_lines = 6
		self.graph_information.graph_legend_columns = 3
		self.graph_information.graph_legend_labels.append("Offensive Stance")
		self.graph_information.graph_legend_styles.append("r^-")
		self.graph_information.graph_legend_labels.append("Neutral Stance")
		self.graph_information.graph_legend_styles.append("g*-")
		self.graph_information.graph_legend_labels.append("Advanced Stance")
		self.graph_information.graph_legend_styles.append("mD-")
		self.graph_information.graph_legend_labels.append("Guarded Stance")
		self.graph_information.graph_legend_styles.append("cH-")
		self.graph_information.graph_legend_labels.append("Forward Stance")
		self.graph_information.graph_legend_styles.append("yd-")
		self.graph_information.graph_legend_labels.append("Defensive Stance")
		self.graph_information.graph_legend_styles.append("bs-")			
	
	
	# Calculate the Unarmed Attack Factor (UAF) of the character from level 0-100 or across postcap training.
	# Certain brawling weapons add their enhancement to UAF but this formula is pretty straight forwards otherwise.
	def Formula_Unarmed_Attack_Factor(self, gloves, boots, main, other):
		effects_list = ["Statistic_Strength", "Statistic_Bonus_Strength", "Statistic_Agility", "Statistic_Bonus_Agility", 
						"Skill_Bonus_Brawling", "Skill_Ranks_Brawling", "Skill_Bonus_Combat_Maneuvers", "Skill_Ranks_Combat_Maneuvers", "Skill_Phantom_Ranks_Combat_Maneuvers",
						"UAF"]
		statistic_names = ["Strength", "Agility"]
		skill_names = ["Brawling", "Combat Maneuvers"]
		gloves_enchantment = int(gloves.enchantment)
		boots_enchantment = int(boots.enchantment)		
		main_enchantment = 0
		other_enchantment = 0
		main_name = main.name.get()
		other_name = other.name.get()
		held_enchantment = 0
		held_weapons = 0
		
		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}
		base_bonus_arr = {}
		gloves_totals = []
		boots_totals = []
			
		# Setup the effects lists and td lists	
		for stat in statistic_names:
			effects_list.append("Statistic_Bonus_%s" % stat)
			effects_list.append("Statistic_%s" % stat)			

		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		loop_range = self.Set_Graph_Labels(skill_names, "Unarmed Attack Factor", "UAF")		


		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			held_weapons = 0
			stat_enh_bonus = 0
			effects_total = 0
			stat_enhancive_totals = {}
			held_weapons_tooltip = ""
			stat_tooltip_arr = {}
			skill_tooltip_arr = {}
			effects_tooltip_text = ""
			stat_tooltip = ""
			skill_tooltip = ""
		
			# Only a minor change depending on self.calc_style
			# Get the base ranks and bonus for each relevant statistic and skill for this level/interval
			if self.calc_style == 1:
				tooltip = "Level %s: Unarmed Attack Factor\n" % (i)
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()	
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Unarmed Attack Factor\n" % ("{:,}".format(i))
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[100].get()	
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)					
		

			# Calculate Statistic bonus	
			for stat in statistic_names:
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, stat, 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_%s" % stat], lists_of_effects_by_tag["Statistic_%s" % stat]], 
												["Statistic_Bonus_%s" % stat, "Statistic_%s" % stat], 
												"stat_inc_to_bonus")													

				stat_enhancive_totals[stat] = int(base_stat_arr[stat] + min(50, stat_enh_bonus))
				stat_tooltip_arr[stat] = "".join( [ "  %s  %s bonus (%+d / 2)\n" % (("%+d" % (stat_enhancive_totals[stat]/2)).rjust(4), stat, stat_enhancive_totals[stat]),
											"       %s  %s base bonus\n" % (("%+d" % base_stat_arr[stat]).rjust(4), stat),
											temp_tooltip
											])			
			
				
			# Calculate Weapon Skill bonus. 
			weapon_inc_bonus, temp_tooltip = self.Combine_Effects(i, "Brawling", base_bonus_arr["Brawling"], 
											[lists_of_effects_by_tag["Skill_Bonus_Brawling"], lists_of_effects_by_tag["Skill_Ranks_Brawling"]], 
											["Skill_Bonus_Brawling", "Skill_Ranks_Brawling"], 
											"skill_bonus_to_ranks")

			brawling_total = base_ranks_arr["Brawling"] + min(50, weapon_inc_bonus)	
			skill_tooltip_arr["Brawling"] = "".join( [ "  %s  Brawling ranks  (%s * 2)\n" % (("%+d" % (brawling_total*2)).rjust(4), brawling_total), 	
											"       %s  Brawling base ranks\n" % (("%+d" % base_ranks_arr["Brawling"]).rjust(4)),
											temp_tooltip
											] )
											
			
			# Calculate Combat Maneuver ranks
			skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Combat Maneuvers", base_ranks_arr["Combat Maneuvers"], 
											[lists_of_effects_by_tag["Skill_Bonus_Combat_Maneuvers"], lists_of_effects_by_tag["Skill_Ranks_Combat_Maneuvers"], lists_of_effects_by_tag["Skill_Phantom_Ranks_Combat_Maneuvers"]], 
											["Skill_Bonus_Combat_Maneuvers", "Skill_Ranks_Combat_Maneuvers", "Skill_Phantom_Ranks_Combat_Maneuvers"], 
											"skill_bonus_to_ranks")

			cman_total = base_ranks_arr["Combat Maneuvers"] + skill_rank_count	
			skill_tooltip_arr["Combat Maneuvers"] = "".join( [ "  %s  Combat Maneuver ranks  (%s / 2)\n" % (("%+d" % (cman_total/2)).rjust(4), cman_total),
											"       %s  Combat Maneuvers base ranks\n" % (("%+d" % base_ranks_arr["Combat Maneuvers"]).rjust(4)),
											temp_tooltip
											] )
				
	
			# Calculate total of UAF effects
			effects_total, effects_tooltip_text = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["UAF"]], ["UAF"], "effect_display")			

			if effects_tooltip_text != "":
					effects_tooltip_text = "  %s  bonus from UAF effects\n" % (("%+d" % effects_total).rjust(4)) + effects_tooltip_text				
			
			# Only certain weapons can be used with UAC. If held, allow their enchantments to be added into the formula.
			if main_name == "Cestus" or main_name == "Knuckle-blade" or main_name == "Knuckle-duster" or main_name == "Paingrip" or main_name == "Razorpaw" or main_name == "Tiger-claw" or main_name == "Yierka-spur":
				main_enchantment = int(main.enchantment)
				held_weapons_tooltip += "       %+d  Enchantment bonus from %s\n" % (main_enchantment, main_name)
				held_weapons += 1
			if other_name == "Cestus" or other_name == "Knuckle-blade" or other_name == "Knuckle-duster" or other_name == "Paingrip" or other_name == "Razorpaw" or other_name == "Tiger-claw" or other_name == "Yierka-spur":
				other_enchantment = int(other.enchantment)
				held_weapons_tooltip += "       %+d  Enchantment bonus from %s\n" % (other_enchantment, other_name) 
				held_weapons += 1			
			
			# If one or more of UAC weapon is being used, allow their enchantments to be included in the calculations.
			if held_weapons != 0:
				held_enchantment = math.floor(((main_enchantment + other_enchantment) / held_weapons) / 2)
				held_weapons_tooltip = "  %s  Avg held UAC weapons bonus ((%d + %d) / %s) / 2)\n" % (("%+d" % held_enchantment).rjust(4), main_enchantment, other_enchantment, held_weapons) + held_weapons_tooltip
			
			
			# Calculate the base value for UAC
			base_value = int((stat_enhancive_totals["Strength"] / 2) + (stat_enhancive_totals["Agility"] / 2) + (brawling_total * 2) + math.floor(cman_total / 2) + held_enchantment + effects_total)
			
			# The glove and boot enchantments are calculated seperately. Boots work with Kick and gloves work with Jab/Punch/Grapple.
			gloves_value = base_value + gloves_enchantment
			boots_value = base_value + boots_enchantment
			
			gloves_totals.append(gloves_value)
			boots_totals.append(boots_value)
			
		
			# Create Tooltip info			
			for stat in statistic_names:
				stat_tooltip += stat_tooltip_arr[stat]
			for skill in skill_names:
				skill_tooltip += skill_tooltip_arr[skill]		
				
			tooltip = "".join( [ tooltip,
						"%s = %s + %s (Jab/Punch/Grapple)\n" % (("%+d" % gloves_value).rjust(4), base_value, gloves_enchantment),
						"%s = %s + %s (Kick)\n" % (("%+d" % boots_value).rjust(4), base_value, boots_enchantment),
						"%+d from enchantment bonus of %s\n" % (gloves_enchantment, gloves.name.get()),
						"%+d from enchantment bonus of %s\n" % (boots_enchantment, boots.name.get()),
						"%+d calculated with:\n" % base_value,
						stat_tooltip,
						skill_tooltip,
						held_weapons_tooltip,
						effects_tooltip_text
						])
			
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(gloves_totals)
		self.graph_information.graph_data_lists.append(boots_totals)
		
		# Set the minimum height for the graph
		ymin = min(gloves_totals[0], boots_totals[0])
		ymax = max(gloves_totals[-1], boots_totals[-1])
		self.graph_information.graph_yaxis_min = ymin - 5
		self.graph_information.graph_yaxis_max = ymax + 5		

		# Setup the Legend
		self.graph_information.graph_num_lines = 2
		self.graph_information.graph_legend_columns = 2
		self.graph_information.graph_legend_labels.append("Jab/Punch/Grapple")
		self.graph_information.graph_legend_styles.append("r^-")		
		self.graph_information.graph_legend_labels.append("Kick")
		self.graph_information.graph_legend_styles.append("bs-")
	
	
	# This huge method is used to Defense Strength (DS) of a character from level 0-100 or across postcap training. 
	# The user picks between melee and ranged defense and the DS is calculated depending on their gear's combat style.
	# All three parts of the DS formula, Parry, Block, and Evade are calculated seperately and added up to show the
	# total DS gained. Off-Hand Parry DS is also done if a weapon is in the off-hand. All statistics, skills, and 
	# effects that increase skills, statistics, or AS itself are included in this calculation.	
	def Formula_Defense_Strength(self, vs_type, main_gear, other_hand_gear, armor_gear, gloves_gear):
		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}
		base_bonus_arr = {}
		postcap_intervals = []
		lists_of_effects_by_tag = {}	
		override_options = []
		
		main_enchantment = int(main_gear.enchantment)
		other_name = other_hand_gear.name.get()
		other_enchantment = int(other_hand_gear.enchantment)
		armor_enchantment = int(armor_gear.enchantment)
		gloves_enchantment = int(gloves_gear.enchantment)
		weapon_types = main_gear.skills.split("/")
		shield_factor = 1
		shield_size_penalty = 0
		shield_size = "none"	
		runestaff_rank_conversions = [0, 0.15, 0.30, 0.45, 0.60, 0.70, 0.80, 0.90, 1, 1.1, 1.2, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55]
		
		off_stance = []
		adv_stance = []
		for_stance = []
		neu_stance = []
		gua_stance = []
		def_stance = []			
		
		stance_arr = ["Offensive", "Advanced", "Forward", "Neutral", "Guarded", "Defensive"]
		block_stance_mod = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]	
		evade_stance_mod = [0.75, 0.80, 0.85, 0.9, 0.95, 1.0]		
		
		# Setup the lists for what skills and stats are relavent for calculate DS by fighting style
		if main_gear.name.get() == "Runestaff":
			effects_list = ["Skill_Ranks_Arcane_Symbols", "Skill_Ranks_Magic_Item_Use", "Skill_Ranks_Harness_Power", "Skill_Ranks_Spell_Aiming",
							"Skill_Ranks_Elemental_Mana_Control", "Skill_Ranks_Mental_Mana_Control", "Skill_Ranks_Spiritual_Mana_Control",
							"Skill_Ranks_Elemental_Lore_Air", "Skill_Ranks_Elemental_Lore_Earth", "Skill_Ranks_Elemental_Lore_Fire", "Skill_Ranks_Elemental_Lore_Water",
							"Skill_Ranks_Spiritual_Lore_Blessings", "Skill_Ranks_Spiritual_Lore_Summoning", "Skill_Ranks_Spiritual_Lore_Religion",
							"Skill_Ranks_Mental_Lore_Divination", "Skill_Ranks_Mental_Lore_Manipulation", "Skill_Ranks_Mental_Lore_Telepathy", "Skill_Ranks_Mental_Lore_Transference", "Skill_Ranks_Mental_Lore_Transformation",
							"Skill_Ranks_Sorcerous_Lore_Demonology", "Skill_Ranks_Sorcerous_Lore_Necromancy", "Skill_Ranks_Spell_Research_Minor_Spiritual", "Skill_Ranks_Spell_Research_Major_Spiritual", "Skill_Ranks_Spell_Research_Cleric", "Skill_Ranks_Spell_Research_Minor_Elemental", "Skill_Ranks_Spell_Research_Major_Elemental", "Skill_Ranks_Spell_Research_Ranger", "Skill_Ranks_Spell_Research_Sorcerer", "Skill_Ranks_Spell_Research_Wizard","Skill_Ranks_Spell_Research_Savant", "Skill_Ranks_Spell_Research_Minor_Mental", "Skill_Ranks_Spell_Research_Major_Mental", "Skill_Ranks_Spell_Research_Paladin",
							"Skill_Bonus_Arcane_Symbols", "Skill_Bonus_Magic_Item_Use", "Skill_Bonus_Harness_Power", "Skill_Bonus_Spell_Aiming",
							"Skill_Bonus_Elemental_Mana_Control", "Skill_Bonus_Mental_Mana_Control", "Skill_Bonus_Spiritual_Mana_Control",
							"Skill_Bonus_Elemental_Lore_Air", "Skill_Bonus_Elemental_Lore_Earth", "Skill_Bonus_Elemental_Lore_Fire", "Skill_Bonus_Elemental_Lore_Water",
							"Skill_Bonus_Spiritual_Lore_Blessings", "Skill_Bonus_Spiritual_Lore_Summoning", "Skill_Bonus_Spiritual_Lore_Religion",
							"Skill_Bonus_Mental_Lore_Divination", "Skill_Bonus_Mental_Lore_Manipulation", "Skill_Bonus_Mental_Lore_Telepathy", "Skill_Bonus_Mental_Lore_Transference", "Skill_Bonus_Mental_Lore_Transformation",
							"Skill_Bonus_Sorcerous_Lore_Demonology", "Skill_Bonus_Sorcerous_Lore_Necromancy", "Skill_Bonus_Spell_Research_Minor_Spiritual", "Skill_Bonus_Spell_Research_Major_Spiritual", "Skill_Bonus_Spell_Research_Cleric", "Skill_Bonus_Spell_Research_Minor_Elemental", "Skill_Bonus_Spell_Research_Major_Elemental", "Skill_Bonus_Spell_Research_Ranger", "Skill_Bonus_Spell_Research_Sorcerer", "Skill_Bonus_Spell_Research_Wizard","Skill_Bonus_Spell_Research_Savant", "Skill_Bonus_Spell_Research_Minor_Mental", "Skill_Bonus_Spell_Research_Major_Mental", "Skill_Bonus_Spell_Research_Paladin",
							"Statistic_Strength", "Statistic_Bonus_Strength", "Statistic_Dexterity", "Statistic_Bonus_Dexterity", "Statistic_Intuition", "Statistic_Bonus_Intuition", "Statistic_Agility", "Statistic_Bonus_Agility", "DS_All"]	
			statistic_names = ["Intuition", "Agility", "Dexterity", "Strength"]
			skill_names = ["Arcane Symbols", "Magic Item Use", "Harness Power", "Spell Aiming",
							"Elemental Mana Control", "Mental Mana Control", "Spiritual Mana Control", 
							"Elemental Lore, Air", "Elemental Lore, Earth", "Elemental Lore, Fire", "Elemental Lore, Water",
							"Spiritual Lore, Blessings", "Spiritual Lore, Summoning", "Spiritual Lore, Religion",
							"Mental Lore, Divination", "Mental Lore, Manipulation", "Mental Lore, Telepathy", "Mental Lore, Transference", "Mental Lore, Transformation", 
							"Sorcerous Lore, Demonology", "Sorcerous Lore, Necromancy",
							"Spell Research, Minor Spiritual", "Spell Research, Major Spiritual", "Spell Research, Cleric", "Spell Research, Minor Elemental", "Spell Research, Major Elemental", "Spell Research, Ranger", "Spell Research, Sorcerer", "Spell Research, Wizard", "Spell Research, Savant", "Spell Research, Minor Mental", "Spell Research, Major Mental", "Spell Research, Paladin"
						]
						
		elif weapon_types[0] == "Ranged Weapons":
			effects_list = ["Statistic_Intuition", "Statistic_Bonus_Intuition", "Statistic_Agility", "Statistic_Bonus_Agility", "Skill_Bonus_Ambush", "Skill_Ranks_Ambush", "Skill_Bonus_Perception", "Skill_Ranks_Perception", "DS_All"]	
			statistic_names = ["Intuition", "Agility"]
			skill_names = ["Ambush", "Perception"]

		else:				
			effects_list = ["Statistic_Strength", "Statistic_Bonus_Strength", "Statistic_Dexterity", "Statistic_Bonus_Dexterity", "Statistic_Intuition", "Statistic_Bonus_Intuition", "Statistic_Agility", "Statistic_Bonus_Agility", "DS_All"]	
			statistic_names = ["Intuition", "Agility", "Dexterity", "Strength"]
			skill_names = []
			
		
		if other_name == "Small Shield" or other_name == "Medium Shield" or other_name == "Large Shield" or other_name == "Tower Shield":
			effects_list.extend( ("Skill_Bonus_Shield_Use", "Skill_Ranks_Shield_Use", "Shield_Factor") )
			shield_size = other_hand_gear.gear_traits["size"]
			shield_melee_size_modifer = other_hand_gear.gear_traits["melee_size_modifer"]
			shield_ranged_size_modifer = other_hand_gear.gear_traits["ranged_size_modifer"]
			shield_ranged_size_bonus = other_hand_gear.gear_traits["ranged_size_bonus"]
			shield_size_penalty = other_hand_gear.gear_traits["dodging_size_penalty"]	
			shield_factor = other_hand_gear.gear_traits["dodging_shield_factor"]				
			skill_names.append("Shield Use")
			
		elif ( weapon_types[0] != "Ranged Weapons" and other_name != "Empty" ) or ( weapon_types[0] == "Brawling" and other_name == "Empty" ):
			effects_list.extend( ("Skill_Bonus_Two_Weapon_Combat", "Skill_Ranks_Two_Weapon_Combat") )
			skill_names.append("Two Weapon Combat")

			
		# Evade DS setup
		dodge_armor_action_penalty = armor_gear.gear_traits["action_penalty"]	
		armor_overtrain_ranks = int(armor_gear.gear_traits["roundtime_train_off_ranks"])
		armor_AG = int(armor_gear.gear_traits["AG"])
		
		effects_list.extend( ("Skill_Bonus_Dodging", "Skill_Ranks_Dodging", "Skill_Phantom_Ranks_Dodging", "Skill_Bonus_Armor_Use", "Skill_Ranks_Armor_Use", "Action_Penalty") )
		skill_names.extend( ("Dodging", "Armor Use") )
		
		
		if vs_type == "Melee":
			effects_list.append("DS_Melee")
		elif vs_type == "Ranged":
			effects_list.append("DS_Ranged")
		elif vs_type == "Bolt":		
			effects_list.append("DS_Bolt")
		
						
		# Don't need THW skill when using a Runestaff
		if main_gear.name.get() != "Runestaff":
			for skill in weapon_types:
				skill_names.append(skill)
				effects_list.append("Skill_Ranks_%s" % skill.replace(" ", "_").replace("-", "_").replace(",", ""))
				effects_list.append("Skill_Bonus_%s" % skill.replace(" ", "_").replace("-", "_").replace(",", ""))
			
			
		
		override_options = self.Find_Overrides_By_Tags(effects_list)	
			
		if "Armor Group" in override_options:
			calculations.override_dict["Armor Group"] = armor_AG
			
		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		loop_range = self.Set_Graph_Labels(skill_names, "Defense Strength vs %s"% (vs_type), "DS")		
		

		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			skill_inc_bonus = 0		
			skill_rank_count = 0
			effects_total = 0
			combined_weapons_bonus = 0
			combined_statistic_bonus = 0			
			weapon_enhancive_totals = []
			stat_enhancive_totals = {}
			stat_tooltip_arr = {}
			skill_tooltip_arr = {}			
			skill_tooltip = ""
			weapon_tooltip_text = ""
			effects_tooltip_text = ""
			parry_tooltip_text = ""
			off_hand_tooltip_text = ""
			shield_tooltip_text = ""
			evade_tooltip_text = ""
			weapon_tooltip_arr = []		
			
			parry_totals_arr = []
			shield_totals_arr = []
			evade_totals_arr = []
			
			if self.calc_style == 1:
				tooltip = "Level %s: Defense Strength vs %s\n" % (i, vs_type)
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()	
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Defense Strength vs %s\n" % ("{:,}".format(i), vs_type)
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[100].get()	
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
		

			# Calculate Statistic bonus	
			for stat in statistic_names:
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, stat, 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_%s" % stat], lists_of_effects_by_tag["Statistic_%s" % stat]], 
												["Statistic_Bonus_%s" % stat, "Statistic_%s" % stat], 
												"stat_inc_to_bonus")													

				stat_enhancive_totals[stat] = base_stat_arr[stat] + min(50, stat_enh_bonus)		
				stat_tooltip_arr[stat] = "       %s  %s base bonus\n" % (("%+d" % base_stat_arr[stat]).rjust(4), stat) + temp_tooltip	
				
						

			# Calculate Parry DS	
			if main_gear.name.get() == "Runestaff":		
				combined_weapons_ranks = 0
				for skill in skill_names:		
					if skill == "Dodging" or skill == "Two Weapon Combat":
						continue

					tag_name_sub = skill.replace(" ", "_").replace("-", "_").replace(",", "")		
					weapon_inc_bonus, temp_tooltip = self.Combine_Effects(i, skill, base_ranks_arr[skill], 
													[lists_of_effects_by_tag["Skill_Bonus_%s" % tag_name_sub], lists_of_effects_by_tag["Skill_Ranks_%s" % tag_name_sub]], 
													["Skill_Bonus_%s" % tag_name_sub, "Skill_Ranks_%s" % tag_name_sub], 
													"skill_bonus_to_ranks")

					weapon_enhancive_totals.append(base_ranks_arr[skill] + min(50, weapon_inc_bonus))		
					combined_weapons_ranks += base_ranks_arr[skill] + min(50, weapon_inc_bonus) 
					weapon_tooltip_text = "       %s bonus from %s %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(4), base_ranks_arr[skill], skill) 
					weapon_tooltip_text += temp_tooltip				
					skill_tooltip_arr[skill] = weapon_tooltip_text	

				
				if (i > 0 and i*8 > combined_weapons_ranks) or (i == 0 and combined_weapons_ranks < 8):
					if i == 0:
						parry_tooltip_text = "--Parry DS by Stance--\n+0 Parry DS.  Character has insuficent Runestaff magical ranks (%s vs %s).\n" % (combined_weapons_ranks, 8)
					else:
						parry_tooltip_text = "--Parry DS by Stance--\n+0 Parry DS.  Character has insuficent Runestaff magical ranks (%s vs %s).\n" % (combined_weapons_ranks, 8*i)
					parry_totals_arr = [0 for i in range(6)]	
				else:
					if i > 0:	 # Stupid divide by zero errors...
						conversion_rate = min(16, int(math.floor(combined_weapons_ranks/i)))
						parry_ranks = int(math.floor( runestaff_rank_conversions[conversion_rate] * i ))
					else:
						conversion_rate = min(16, combined_weapons_ranks)
						parry_ranks = int(math.floor( runestaff_rank_conversions[conversion_rate] ))						


					parry_tooltip_text = "--Parry DS by Stance--\n"			
					parry_base_value = int(parry_ranks + math.floor(stat_enhancive_totals["Strength"]/4) + math.floor(stat_enhancive_totals["Dexterity"]/4))

					stance_mod = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]			 	
					stance_bonus = [0, 10, 20, 30, 40, 50]
					for j in range(6):
						value = math.floor(parry_base_value * stance_mod[j])
						value = math.floor(value * 1.5)
						
						if vs_type == "Melee":
							value += main_enchantment
							value += stance_bonus[j]
						else:
							value = math.floor(value/2)
							value += math.floor(main_enchantment/2)
							value += math.floor(stance_bonus[j]/2)
						
						parry_totals_arr.append(value)	
												
						if vs_type == "Melee":
							parry_tooltip_text += "%+d = (%s  x  %.2f)  x  1.5  +  %s  +  %s  (%s)\n" % (value, parry_base_value, stance_mod[j], main_enchantment, stance_bonus[j], stance_arr[j]) 
						else:
							parry_tooltip_text += "%+d = ((%s  x  %.2f)  x  1.5)/2  +  %s  +  %s  (%s)\n" % (value, parry_base_value, stance_mod[j], int(math.floor(main_enchantment/2)), int(stance_bonus[j]/2),  stance_arr[j]) 
													

					parry_tooltip_text += "%+d (Parry Base Value) calculated with:\n" % parry_base_value	
					if i == 0:
						parry_tooltip_text += "  %s  Parry Ranks (%s vs %s -> %s(%s) = %s * %s)\n" % (("%+d" % parry_ranks).rjust(4), combined_weapons_ranks, 8, conversion_rate,  runestaff_rank_conversions[conversion_rate], runestaff_rank_conversions[conversion_rate], 1)					
					else:					
						parry_tooltip_text += "  %s  Parry Ranks (%s vs %s -> %s(%s) = %s * %s)\n" % (("%+d" % parry_ranks).rjust(4), combined_weapons_ranks, i*8, conversion_rate,runestaff_rank_conversions[conversion_rate], runestaff_rank_conversions[conversion_rate], i)					
					for skill in skill_names:	
						if skill == "Dodging" or skill == "Two Weapon Combat":
							continue
						parry_tooltip_text += skill_tooltip_arr[skill]
					parry_tooltip_text += "  %s  Strength bonus  (%+d / 4)\n" % (("%+d" % math.floor(stat_enhancive_totals["Strength"]/4)).rjust(4), stat_enhancive_totals["Strength"])		
					parry_tooltip_text += stat_tooltip_arr["Strength"]		
					parry_tooltip_text += "  %s  Dexterity bonus  (%+d / 4)\n" % (("%+d" % math.floor(stat_enhancive_totals["Dexterity"]/4)).rjust(4), stat_enhancive_totals["Dexterity"])		
					parry_tooltip_text += stat_tooltip_arr["Dexterity"]		
					if vs_type == "Melee":
						parry_tooltip_text += "  %s  Enchantment bonus of %s\n" % (("%+d" % main_enchantment).rjust(3), main_gear.name.get())	
					else:
						parry_tooltip_text += "  %s  Enchantment bonus of %s  (%d / 2)\n" % (("%+d" % int(math.floor(main_enchantment/2))).rjust(3), main_gear.name.get(), main_enchantment)		
						
						
			# Ranged Parry DS	
			elif weapon_types[0] == "Ranged Weapons":	
				skill_inc_bonus, weapon_tooltip_text = self.Combine_Effects(i, "Ranged Weapons", base_ranks_arr["Ranged Weapons"], 
												[lists_of_effects_by_tag["Skill_Bonus_Ranged_Weapons"], lists_of_effects_by_tag["Skill_Ranks_Ranged_Weapons"]], 
												["Skill_Bonus_Ranged_Weapons", "Skill_Ranks_Ranged_Weapons"], 
												"skill_ranks_to_bonus")

				weapons_bonus = base_bonus_arr["Ranged Weapons"] + min(50, skill_inc_bonus) 
				weapon_enhancive_totals.append(base_bonus_arr["Ranged Weapons"] + min(50, skill_inc_bonus) )				

				weapon_tooltip_text = "".join([ "  %s  %s skill bonus\n" % (("%+d" % weapons_bonus).rjust(4), weapon_types[0]),
									"       %s bonus from %s Ranged Weapons base ranks\n" % (("%+d" % base_bonus_arr["Ranged Weapons"]).rjust(4), base_ranks_arr["Ranged Weapons"]),
									"       %s  Ranged Weapons base ranks\n" % (("%+d" % base_ranks_arr["Ranged Weapons"]).rjust(4)),
									temp_tooltip
									])	
									
				
				# Calculate Ambush ranks
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Ambush", base_ranks_arr["Ambush"], 
												[lists_of_effects_by_tag["Skill_Bonus_Ambush"], lists_of_effects_by_tag["Skill_Ranks_Ambush"]], 
												["Skill_Bonus_Ambush", "Skill_Ranks_Ambush"], 
												"skill_bonus_to_ranks")

				ambush_total = base_ranks_arr["Ambush"] + min(50, skill_rank_count)		
				
				skill_tooltip_arr["Ambush"] = "".join([ "  %s  Ambush ranks  ((%s - 40) / 4) vs min +0)\n" % (("%+d" % ( max(0, math.floor(0/4) + math.floor((ambush_total - 40) / 4) )) ).rjust(4), ambush_total),
										"       %s  Ambush base ranks\n" % (("%+d" % base_ranks_arr["Ambush"]).rjust(4)),
										temp_tooltip
										])
				
				
				# Calculate Perception ranks
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Perception", base_ranks_arr["Perception"], 
												[lists_of_effects_by_tag["Skill_Bonus_Perception"], lists_of_effects_by_tag["Skill_Ranks_Perception"]], 
												["Skill_Bonus_Perception", "Skill_Ranks_Perception"], 
												"skill_bonus_to_ranks")

				perception_total = base_ranks_arr["Perception"] + min(50, skill_rank_count)		

				skill_tooltip_arr["Perception"] = "".join([ "  %s  Perception ranks  ((%s - 40) / 4) vs min +0)\n" % (("%+d" % ( max(0, math.floor(0/4) + math.floor((perception_total - 40) / 4) )) ).rjust(4), perception_total),
										"       %s  Perception base ranks\n" % (("%+d" % base_ranks_arr["Perception"]).rjust(4)),
										temp_tooltip
										])


				# Calculate Parry DS
				if weapons_bonus == 0:
					parry_tooltip_text = "--Parry DS by Stance--\n+0 Parry DS.  Character has no ranks in %s.\n" % main_gear.skills
					parry_totals_arr = [0 for i in range(6)]	
				else:
					# Ranged Parry DS calculations				
					parry_tooltip_text = "--Parry DS by Stance--\n"			
					parry_base_value = int(weapons_bonus + math.floor(perception_total/2) + math.floor(ambush_total/2))	
					
					
					if main_gear.name.get() == "Heavy Crossbow" or main_gear.name.get() == "Light Crossbow":
						stance_mod = [0.12, 0.17, 0.22, 0.27, 0.32, 0.37]		
					else:
						stance_mod = [0.15, 0.21, 0.27, 0.33, 0.39, 0.45]	
					stance_bonus = [0, 10, 20, 30, 40, 50]
					for j in range(6):
						if vs_type == "Melee":
							value = math.floor(parry_base_value * stance_mod[j]) + stance_bonus[j]
						else:
							value = math.floor(parry_base_value * stance_mod[j])	

						value += main_enchantment
						
						parry_totals_arr.append(value)	
						
						if vs_type == "Melee":		
							parry_tooltip_text += "%+d = (%s  x  %.2f)  +  %s  + %s  (%s)\n" % (value, parry_base_value, stance_mod[j], main_enchantment, stance_bonus[j], stance_arr[j]) 
						else:
							parry_tooltip_text += "%+d = (%s  x  %.2f)  +  %s  (%s)\n" % (value, parry_base_value, stance_mod[j], main_enchantment, stance_arr[j]) 	

					parry_tooltip_text = "".join([ parry_tooltip_text,
								"%+d (Parry Base Value) calculated with:\n" % parry_base_value,
								weapon_tooltip_text,
								skill_tooltip_arr["Perception"],
								skill_tooltip_arr["Ambush"],
								"%s  Enchantment bonus of %s\n" % (("%+d" % main_enchantment).rjust(3), main_gear.name.get())
								])
			
			# THW Parry DS
			elif weapon_types[0] == "Two-Handed Weapons" or (weapon_types[0] == "Polearm Weapons" and (main_gear.name.get() != "Pilum" and main_gear.name.get() != "Spear, One-Handed")):
				tag_name_sub = weapon_types[0].replace(" ", "_").replace("-", "_").replace(",", "")		
				
				weapon_inc_bonus, temp_tooltip = self.Combine_Effects(i, weapon_types[0], base_bonus_arr[weapon_types[0]], 
												[lists_of_effects_by_tag["Skill_Bonus_%s" % tag_name_sub], lists_of_effects_by_tag["Skill_Ranks_%s" % tag_name_sub]], 
												["Skill_Bonus_%s" % tag_name_sub, "Skill_Ranks_%s" % tag_name_sub], 
												"skill_ranks_to_bonus")

				weapon_enhancive_totals.append(base_bonus_arr[weapon_types[0]] + min(50, weapon_inc_bonus))		
				combined_weapons_ranks += base_bonus_arr[weapon_types[0]] + min(50, skill_inc_bonus) 
				weapon_tooltip_text = "       %s bonus from %s %s base ranks\n" % (("%+d" % base_bonus_arr[weapon_types[0]]).rjust(4), base_ranks_arr[weapon_types[0]], weapon_types[0]) 
				weapon_tooltip_text += temp_tooltip			
				weapons_bonus = base_bonus_arr[weapon_types[0]] + min(50, skill_inc_bonus) 				
				weapon_tooltip_text = "  %s  %s skill bonus\n" % (("%+d" % weapons_bonus).rjust(4), weapon_types[0]) + weapon_tooltip_text				
					
			
				# No skill, no parry DS
				if weapons_bonus == 0:
					parry_tooltip_text = "--Parry DS by Stance--\n+0 Parry DS.  Character has no ranks in %s.\n" % main_gear.skills
					parry_totals_arr = [0 for i in range(6)]	
				else:			
					# Two-Handed Weapons and Two-Handed Polearms Parry DS calculations				
					parry_tooltip_text = "--Parry DS by Stance--\n"			
					parry_base_value = int(weapons_bonus + math.floor(stat_enhancive_totals["Strength"]/4) + math.floor(stat_enhancive_totals["Dexterity"]/4)) + main_enchantment
					
					
					if weapon_types[0] == "Two-Handed Weapons":
						stance_mod = [0.30, 0.45, 0.60, 0.75, 0.90, 1.05]				
						stance_bonus = [0, 10, 20, 30, 40, 50]
					else:
						stance_mod = [0.27, 0.41, 0.54, 0.68, 0.81, 0.94]			 	
						stance_bonus = [15, 28, 41, 54, 67, 80]
					for j in range(6):
						if vs_type == "Melee":
							value = math.floor(parry_base_value * stance_mod[j]) + stance_bonus[j]
						else:
							value = math.floor(parry_base_value * stance_mod[j])	
						
						parry_totals_arr.append(value)	
						
						if vs_type == "Melee":		
							parry_tooltip_text += "%+d = (%s  x  %.2f)  + %s  (%s)\n" % (value, parry_base_value, stance_mod[j], stance_bonus[j], stance_arr[j]) 
						else:
							parry_tooltip_text += "%+d = (%s  x  %.2f)  (%s)\n" % (value, parry_base_value, stance_mod[j], stance_arr[j]) 
							
					parry_tooltip_text = "".join([ parry_tooltip_text,
									"%+d (Parry Base Value) calculated with:\n" % parry_base_value,
									weapon_tooltip_text,
									"  %s  Strength bonus  (%+d / 4)\n" % (("%+d" % math.floor(stat_enhancive_totals["Strength"]/4)).rjust(4), stat_enhancive_totals["Strength"]),
									stat_tooltip_arr["Strength"],
									"  %s  Dexterity bonus  (%+d / 4)\n" % (("%+d" % math.floor(stat_enhancive_totals["Dexterity"]/4)).rjust(4), stat_enhancive_totals["Dexterity"]),
									stat_tooltip_arr["Dexterity"],
									"  %s  Enchantment bonus of %s\n" % (("%+d" % main_enchantment).rjust(3), main_gear.name.get())
									])
			
			# Every other weapon for Parry DS (one handed and possible off-hand)
			else:			
				for skill in weapon_types:	
					tag_name_sub = skill.replace(" ", "_").replace("-", "_").replace(",", "")		

					weapon_inc_bonus, temp_tooltip = self.Combine_Effects(i, skill, base_bonus_arr[skill], 
													[lists_of_effects_by_tag["Skill_Bonus_%s" % tag_name_sub], lists_of_effects_by_tag["Skill_Ranks_%s" % tag_name_sub]], 
													["Skill_Bonus_%s" % tag_name_sub, "Skill_Ranks_%s" % tag_name_sub], 
													"skill_bonus_to_ranks")

					weapon_enhancive_totals.append(base_ranks_arr[skill] + min(50, weapon_inc_bonus) )				
					combined_weapons_bonus += base_ranks_arr[skill] + min(50, weapon_inc_bonus) 	
					weapon_tooltip_text = "       %s %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(4), skill) + weapon_tooltip_text
					weapon_tooltip_text += temp_tooltip
					
				combined_weapons_bonus /= len(weapon_types)		

				if len(weapon_types) > 1:	
					mutli_tooltip = ""
					for j in range(len(weapon_types)):
						mutli_tooltip = " %s (%s)," % (weapon_types[j], "%+d" % weapon_enhancive_totals[j]) + mutli_tooltip
					weapon_tooltip_text = "  %s  Skill ranks avg: %s\n" % (("%+d" % combined_weapons_bonus).rjust(4), mutli_tooltip[:-1]) + weapon_tooltip_text
				else:	
					weapon_tooltip_text = "  %s  %s Skill ranks\n" % (("%+d" % combined_weapons_bonus).rjust(4), weapon_types[0]) + weapon_tooltip_text


				# No skill bonus, no parry DS
				if combined_weapons_bonus == 0:
					parry_tooltip_text = "--Parry DS by Stance--\n+0 Parry DS.  Character has no ranks in %s.\n" % main_gear.skills
					parry_totals_arr = [0 for i in range(6)]	
				else:									
					if main_gear.name.get() == "Closed Fist" and gloves_gear.name.get() != "No Gloves":
						parry_weapon = gloves_gear
						enchantment = gloves_enchantment
					else:
						parry_weapon = main_gear
						enchantment = main_enchantment
						
					# Main Hand Parry DS calculations				
					parry_tooltip_text = "--Parry DS by Stance--\n"			
					parry_base_value = int(combined_weapons_bonus + math.floor(stat_enhancive_totals["Strength"]/4) + math.floor(stat_enhancive_totals["Dexterity"]/4))+ int(math.floor(enchantment/2))					
					
					stance_mod = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]			 	
					stance_bonus = [0, 10, 20, 30, 40, 50]
					for j in range(6):
						value = math.floor(parry_base_value * stance_mod[j]) + stance_bonus[j]
						
						parry_totals_arr.append(value)							

						parry_tooltip_text += "%+d = (%s  x  %.2f)  + %s  (%s)\n" % (value, parry_base_value, stance_mod[j], stance_bonus[j], stance_arr[j]) 
						
						'''
						if vs_type == "Melee":		
							parry_tooltip_text += "%+d = (%s  x  %.2f)  + %s  (%s)\n" % (value, parry_base_value, stance_mod[j], stance_bonus[j], stance_arr[j]) 
						else:
							parry_tooltip_text += "%+d = (%s  x  %.2f)  (%s)\n" % (value, parry_base_value, stance_mod[j], stance_arr[j])						
						'''							

					parry_tooltip_text = "".join([ parry_tooltip_text,
										"%+d (Parry Base Value) calculated with:\n" % parry_base_value,
										weapon_tooltip_text,
										"  %s  Strength bonus  (%+d / 4)\n" % (("%+d" % math.floor(stat_enhancive_totals["Strength"]/4)).rjust(4), stat_enhancive_totals["Strength"]),
										stat_tooltip_arr["Strength"],
										"  %s  Dexterity bonus  (%+d / 4)\n" % (("%+d" % math.floor(stat_enhancive_totals["Dexterity"]/4)).rjust(4), stat_enhancive_totals["Dexterity"]),
										stat_tooltip_arr["Dexterity"],
										"  %s  Enchantment bonus of %s  (%+d / 2)\n" % (("%+d" % int(math.floor(enchantment/2))).rjust(3), parry_weapon.name.get(), enchantment)
										])
			
			
				# Checked for off-hand Parry. If not using a shield		
				if shield_factor == 1:	
					weapon_inc_bonus, off_hand_tooltip_text = self.Combine_Effects(i, "Two Weapon Combat", base_ranks_arr["Two Weapon Combat"], 
													[lists_of_effects_by_tag["Skill_Bonus_Two_Weapon_Combat"], lists_of_effects_by_tag["Skill_Ranks_Two_Weapon_Combat"]], 
													["Skill_Bonus_Two_Weapon_Combat", "Skill_Ranks_Two_Weapon_Combat"], 
													"skill_bonus_to_ranks")
													
					weapons_bonus = base_ranks_arr["Two Weapon Combat"] + min(50, weapon_inc_bonus) 
					weapon_enhancive_totals.append(weapons_bonus)	
					
					off_hand_tooltip_text = "       %s Two Weapon Combat base ranks\n" % (("%+d" % base_ranks_arr["Two Weapon Combat"]).rjust(4)) + off_hand_tooltip_text
					off_hand_tooltip_text = "  %s  Two Weapon Combat ranks\n" % (("%+d" % weapons_bonus).rjust(4)) + off_hand_tooltip_text
					skill_tooltip_arr["Two Weapon Combat"] = off_hand_tooltip_text	
					

					# No skill bonus, no off-hand parry DS
					if weapons_bonus == 0:
						off_hand_tooltip_text = "--Off-Hand Parry DS by Stance--\n+0 Off-Hand Parry DS.  Character has no ranks in Two Weapon Combat.\n"
					else:			
						# Off-Hand Parry DS DS calculations				
						off_hand_tooltip_text = "--Off-Hand Parry DS by Stance--\n"			
						parry_base_value = int(weapons_bonus + math.floor(stat_enhancive_totals["Strength"]/4) + math.floor(stat_enhancive_totals["Dexterity"]/4))+ int(math.floor(other_enchantment/2))
						
						
						stance_mod = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35]	
						if other_hand_gear.name.get() == "Sai" or other_hand_gear.name.get() == "Main Gauche" or (other_hand_gear.name.get() == "Empty" and weapons_bonus > i/2):
							bonus = 15
						else:
							bonus = 5
						for j in range(6):
							value = math.floor(parry_base_value * stance_mod[j]) + bonus
							
							parry_totals_arr[j] += value
							
							off_hand_tooltip_text += "%+d = (%s  x  %.2f)  + %s  (%s)\n" % (value, parry_base_value, stance_mod[j], bonus, stance_arr[j]) 
							
							'''
							if vs_type == "Melee":		
								off_hand_tooltip_text += "%+d = (%s  x  %.2f)  + %s  (%s)\n" % (value, parry_base_value, stance_mod[j], stance_bonus[j], stance_arr[j]) 
							else:
								off_hand_tooltip_text += "%+d = (%s  x  %.2f)  (%s)\n" % (value, parry_base_value, stance_mod[j], stance_arr[j])						
							'''
						
						off_hand_tooltip_text = "".join([ off_hand_tooltip_text,
											"%+d (Off-Hand Parry Base Value) calculated with:\n" % parry_base_value,
											skill_tooltip_arr["Two Weapon Combat"],
											"  %s  Strength bonus  (%+d / 4)\n" % (("%+d" % math.floor(stat_enhancive_totals["Strength"]/4)).rjust(4), stat_enhancive_totals["Strength"]),
											stat_tooltip_arr["Strength"],
											"  %s  Dexterity bonus  (%+d / 4)\n" % (("%+d" % math.floor(stat_enhancive_totals["Dexterity"]/4)).rjust(4), stat_enhancive_totals["Dexterity"]),
											stat_tooltip_arr["Dexterity"],
											"  %s  Enchantment bonus of %s  (%+d / 2)\n" % (("%+d" % int(math.floor(other_enchantment/2))).rjust(3), other_hand_gear.name.get(), other_enchantment)
											])					

			
			# Calculate Block DS
			if shield_factor == 1:
				shield_tooltip_text = "--Block DS by Stance--\n+0 Block DS.  Character is not using a shield.\n"
				shield_totals_arr = [0 for i in range(6)]	
			else:
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Shield Use", base_ranks_arr["Shield Use"], 
												[lists_of_effects_by_tag["Skill_Bonus_Shield_Use"], lists_of_effects_by_tag["Skill_Ranks_Shield_Use"]], 
												["Skill_Bonus_Shield_Use", "Skill_Ranks_Shield_Use"], 
												"skill_bonus_to_ranks")
												
				shield_total = base_ranks_arr["Shield Use"] + min(50, skill_rank_count)	

				skill_tooltip_arr["Shield Use"] = "".join([ "  %s  Shield Use ranks  \n" % (("%+d" % shield_total).rjust(4)),
										"       %s  base ranks\n" % (("%+d" % base_ranks_arr["Shield Use"]).rjust(4)),
										temp_tooltip
										])
			
				
				
				# Block DS calculations				
				shield_tooltip_text = "--Block DS by Stance--\n"			
				shield_base_value = int(shield_total + math.floor(stat_enhancive_totals["Strength"]/4) + math.floor(stat_enhancive_totals["Dexterity"]/4))	
								
				for j in range(6):
					if vs_type == "Melee":
						value = math.floor(shield_base_value * shield_melee_size_modifer * block_stance_mod[j])
					else:
						value = math.floor((math.floor(shield_base_value * shield_ranged_size_modifer) + shield_ranged_size_bonus) * block_stance_mod[j])

					value = int(math.floor(value / 1.5))
					value += 20 + other_enchantment
					
					shield_totals_arr.append(value)		
					
					if vs_type == "Melee":		
						shield_tooltip_text += "%+d = %s  x  %.2f  x  %s  /  1.5  +  20  + %s  (%s)\n" % (value, shield_base_value, shield_melee_size_modifer, block_stance_mod[j], other_enchantment, stance_arr[j]) 
					else:
						shield_tooltip_text += "%+d = (%s  x  %.2f  +  %s)  x  %s  /  1.5  +  20  + %s  (%s)\n" % (value, shield_base_value, shield_ranged_size_modifer, shield_ranged_size_bonus, block_stance_mod[j], other_enchantment, stance_arr[j]) 

				shield_tooltip_text = "".join([ shield_tooltip_text,
									"%+d (Shield Base Value) calculated with:\n" % shield_base_value,
									skill_tooltip_arr["Shield Use"],
									"  %s  Strength bonus  (%+d / 4)\n" % (("%+d" % math.floor(stat_enhancive_totals["Strength"]/4)).rjust(4), stat_enhancive_totals["Strength"]),
									stat_tooltip_arr["Strength"],
									"  %s  Dexterity bonus  (%+d / 4)\n" % (("%+d" % math.floor(stat_enhancive_totals["Dexterity"]/4)).rjust(4), stat_enhancive_totals["Dexterity"]),
									stat_tooltip_arr["Dexterity"]
									])
				
				if vs_type == "Melee":						
					shield_tooltip_text = "".join([ shield_tooltip_text,
									"%+.2f (Melee Shield Size Modifier) calculated with:\n" % shield_melee_size_modifer,
									"    %+.2f base modifier of %s :\n" % (shield_melee_size_modifer, other_hand_gear.name.get())
									])
				else:
					shield_tooltip_text = "".join([ shield_tooltip_text,
									"%+.2f (Ranged Shield Size Modifier) calculated with:\n" % shield_ranged_size_modifer,
									"    %+.2f base modifier of %s\n" % (shield_ranged_size_modifer, other_hand_gear.name.get()),
									"%+d (Ranged Shield Size Bonus) calculated with:\n" % shield_ranged_size_bonus,
									"    %+d base modifier of %s\n" % (shield_ranged_size_bonus, other_hand_gear.name.get())
									])

				shield_tooltip_text = "".join([ shield_tooltip_text,
									"+20  Base shield DS\n",
									"%s  Enchantment bonus of %s\n" % (("%+d" % other_enchantment).rjust(3), other_hand_gear.name.get())
									])
				
			# Calculate Evade DS
			
			# Calculate Dodging ranks
			skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Dodging", base_ranks_arr["Dodging"], 
											[lists_of_effects_by_tag["Skill_Bonus_Dodging"], lists_of_effects_by_tag["Skill_Ranks_Dodging"], lists_of_effects_by_tag["Skill_Phantom_Ranks_Dodging"]], 
											["Skill_Bonus_Dodging", "Skill_Ranks_Dodging", "Skill_Phantom_Ranks_Dodging"], 
											"skill_bonus_to_ranks")

			dodge_total = base_ranks_arr["Dodging"] + skill_rank_count

			skill_tooltip_arr["Dodging"] = "".join([ "  %s  Dodging ranks\n" % (("%+d" % dodge_total).rjust(4)),
										"       %s  base ranks\n" % (("%+d" % base_ranks_arr["Dodging"]).rjust(4)),
										temp_tooltip
										])
			
			# Calculate Armor Use ranks 
			skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Armor Use", base_ranks_arr["Armor Use"], 
											[lists_of_effects_by_tag["Skill_Bonus_Armor_Use"], lists_of_effects_by_tag["Skill_Ranks_Armor_Use"]], 
											["Skill_Bonus_Armor_Use", "Skill_Ranks_Armor_Use"], 
											"skill_bonus_to_ranks")
			armor_total = base_ranks_arr["Armor Use"] + skill_rank_count

			skill_tooltip_arr["Armor Use"] = "".join([ "  %s  Armor Use ranks\n" % (("%+d" % armor_total).rjust(4)),
										"       %s  base ranks\n" % (("%+d" % base_ranks_arr["Armor Use"]).rjust(4)),
										temp_tooltip
										])
			

			# Calculate Evade DS				
			evade_tooltip_text = "--Evade DS by Stance--\n"			
			dodge_base_value = int(dodge_total + stat_enhancive_totals["Agility"] + math.floor(stat_enhancive_totals["Intuition"]/4))					
			s_factor = 0
			s_factor_tooltip = ""
			armor_hindrance = 0
			armor_hindrance_tooltip = ""
			overtrain_hindrance_tooltip = ""
			
			# Calculate Shield Factor
			if shield_size == "small" or shield_size == "medium":
				s_factor, s_factor_tooltip = self.Combine_Effects(i, "Shield_Factor", 0, [lists_of_effects_by_tag["Shield_Factor"]], ["Shield_Factor",], "float_format")				
			s_factor += shield_factor 
			
			# Calculate Armor Action Penalty
			armor_hindrance, armor_hindrance_tooltip = self.Combine_Effects(i, "Action_Penalty", 0, [lists_of_effects_by_tag["Action_Penalty"]], ["Action_Penalty",], "AAP_display")	
			base_armor_hindrance = int(dodge_armor_action_penalty)
			min_armor_hindrance = -1 * math.ceil(base_armor_hindrance / 2)
			reduction = (armor_AG - 1)  * math.floor((armor_total - armor_overtrain_ranks) / 50) 
						
			if reduction < 0:
				reduction = 0
			elif reduction > min_armor_hindrance:			
				reduction = min_armor_hindrance
			
			if reduction != 0:
				overtrain_hindrance_tooltip = "    %+d (%+.2f) bonus from %s Armor Use ranks\n" % (reduction, (reduction/200), armor_total)
			
			raw_dodge_armor_hindrance = 1.00 + (math.floor((dodge_armor_action_penalty + reduction + armor_hindrance) / 2) / 100)	
			dodge_armor_hindrance = min(1.00, raw_dodge_armor_hindrance)			
			for j in range(6):
				if vs_type == "Melee":
					value = math.floor(dodge_base_value * dodge_armor_hindrance) 
					value = math.floor(value * s_factor) - shield_size_penalty 
					value = int(math.floor(value * evade_stance_mod[j]))
					
				else:
					value = math.floor(dodge_base_value * dodge_armor_hindrance) 
					value = math.floor(value * s_factor)
					value = math.floor(value * evade_stance_mod[j])
					value = int(math.floor(value * 1.5))					
					
				evade_totals_arr.append(value)		
				
				if vs_type == "Melee":		
					evade_tooltip_text += "%+d = ((%s  x  %.2f  x  %.2f)  -  %s)  x  %.2f  (%s)\n" % (value, dodge_base_value, dodge_armor_hindrance, s_factor, shield_size_penalty, evade_stance_mod[j], stance_arr[j]) 
				else:
					evade_tooltip_text += "%+d = %s  x  %.2f  x  %.2f   x  %.2f  x  1.5  (%s)\n" % (value, dodge_base_value, dodge_armor_hindrance, s_factor, evade_stance_mod[j], stance_arr[j]) 

			evade_tooltip_text = "".join([ evade_tooltip_text,
									"%+d (Dodge Base Value) calculated with:\n" % dodge_base_value,
									skill_tooltip_arr["Dodging"],
									"    %s  Agility bonus\n" % (("%+d" % stat_enhancive_totals["Agility"]).rjust(4)),
									stat_tooltip_arr["Agility"],
									"    %s  Intuition bonus  (%+d / 4)\n" % (("%+d" % math.floor(stat_enhancive_totals["Intuition"]/4)).rjust(4), stat_enhancive_totals["Intuition"]),
									stat_tooltip_arr["Intuition"],
									"%.2f (Armor Hindrance) (%.2f vs max 1.00) calculated with:\n" % (dodge_armor_hindrance, raw_dodge_armor_hindrance),
									"    %+d (%.2f) base AP of %s\n" % (base_armor_hindrance, 1.00 + base_armor_hindrance/200, armor_gear.name.get()),
									overtrain_hindrance_tooltip,
									armor_hindrance_tooltip,
									"%.2f (Shield Factor) calculated with:\n" % s_factor,
									"    %.2f base modifier of %s\n" % (shield_factor, other_hand_gear.name.get()),
									s_factor_tooltip
									])
			
			
			if vs_type == "Melee":			
				evade_tooltip_text = "".join([ evade_tooltip_text,
									"%d (Shield Size Penalty) calculated with:\n" % shield_size_penalty,
									"  -%d base modifier of %s\n" % (shield_size_penalty, other_hand_gear.name.get())	
									])
			
			# Calculate Effects values from total of DS_All effects and either DS_Melee, DS_Ranged, or DS_Bolt effects
			effects_total, effects_tooltip_text = self.Combine_Effects(i, "", 0, 
											[lists_of_effects_by_tag["DS_All"], lists_of_effects_by_tag["DS_%s" % vs_type]], 
											["DS_All", "DS_%s" % vs_type], 
											"effect_display")		

			if effects_tooltip_text != "":
					effects_tooltip_text = "  %s  bonus from Defense Strength effects\n" % (("%+d" % effects_total).rjust(4)) + effects_tooltip_text		
					
			effects_total += armor_enchantment		
			
			effects_tooltip_text = "".join([ "--Effects DS--\n",
								"  %s  Enchantment bonus of %s\n" % (("%+d" % armor_enchantment).rjust(3), armor_gear.name.get()),
								effects_tooltip_text								
								])
						
			# Calculate DS totals 						
			off_stance.append(parry_totals_arr[0] + shield_totals_arr[0] + evade_totals_arr[0] + effects_total)
			neu_stance.append(parry_totals_arr[1] + shield_totals_arr[1] + evade_totals_arr[1] + effects_total)
			adv_stance.append(parry_totals_arr[2] + shield_totals_arr[2] + evade_totals_arr[2] + effects_total)
			gua_stance.append(parry_totals_arr[3] + shield_totals_arr[3] + evade_totals_arr[3] + effects_total)
			for_stance.append(parry_totals_arr[4] + shield_totals_arr[4] + evade_totals_arr[4] + effects_total)
			def_stance.append(parry_totals_arr[5] + shield_totals_arr[5] + evade_totals_arr[5] + effects_total)
			
			# Create Tooltip info
			tooltip = "".join( [ tooltip,
						"%s = %d  +  %d  +  %d  +  %d  (Offensive Stance)\n" % (("%+d" % off_stance[index]).rjust(4), parry_totals_arr[0], shield_totals_arr[0], evade_totals_arr[0], effects_total),
						"%s = %d  +  %d  +  %d  +  %d  (Forward Stance)\n" % (("%+d" % for_stance[index]).rjust(4), parry_totals_arr[2], shield_totals_arr[2], evade_totals_arr[2], effects_total),
						"%s = %d  +  %d  +  %d  +  %d  (Neutral Stance)\n" % (("%+d" % neu_stance[index]).rjust(4), parry_totals_arr[3], shield_totals_arr[3], evade_totals_arr[3], effects_total),
						"%s = %d  +  %d  +  %d  +  %d  (Guarded Stance)\n" % (("%+d" % gua_stance[index]).rjust(4), parry_totals_arr[4], shield_totals_arr[4], evade_totals_arr[4], effects_total),
						"%s = %d  +  %d  +  %d  +  %d  (Defensive Stance)\n" % (("%+d" % def_stance[index]).rjust(4), parry_totals_arr[5], shield_totals_arr[5], evade_totals_arr[5], effects_total),
						parry_tooltip_text,
						off_hand_tooltip_text,
						shield_tooltip_text,
						evade_tooltip_text,
						effects_tooltip_text
						])
			
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	
			index += 1
					
		# Setup graph_information object with new data					

		self.graph_information.graph_yaxis_min = min(off_stance[0], def_stance[0]) - 5
		self.graph_information.graph_yaxis_max = def_stance[-1] + 5	
		self.graph_information.graph_data_lists.append(off_stance)
		self.graph_information.graph_data_lists.append(adv_stance)
		self.graph_information.graph_data_lists.append(for_stance)
		self.graph_information.graph_data_lists.append(neu_stance)
		self.graph_information.graph_data_lists.append(gua_stance)
		self.graph_information.graph_data_lists.append(def_stance)
				
		self.graph_information.graph_num_lines = 6
		self.graph_information.graph_legend_columns = 3
		self.graph_information.graph_legend_labels.append("Offensive Stance")
		self.graph_information.graph_legend_styles.append("r^-")
		self.graph_information.graph_legend_labels.append("Neutral Stance")
		self.graph_information.graph_legend_styles.append("g*-")
		self.graph_information.graph_legend_labels.append("Advanced Stance")
		self.graph_information.graph_legend_styles.append("mD-")
		self.graph_information.graph_legend_labels.append("Guarded Stance")
		self.graph_information.graph_legend_styles.append("cH-")
		self.graph_information.graph_legend_labels.append("Forward Stance")
		self.graph_information.graph_legend_styles.append("yd-")
		self.graph_information.graph_legend_labels.append("Defensive Stance")
		self.graph_information.graph_legend_styles.append("bs-")


	# Calculate the Roundtime for attack and the stamina cost for using Qstrike for the character from level 0-100
	# or across postcap training. 
	# Roundtime is calculated differently for Melee, Ranged (bows), Ranged (crossbows), Thrown, Two Weapon Combat
	# and UAC. Qstrike's stamina cost is based on the attack style and weapons used. Because of this, the cost will
	# be calculated and displayed in the tooltip but not ploted on the graph.
	def Formula_Roundtime_Qstrike(self, alt_mode):
		effects_list = ["Statistic_Strength", "Statistic_Bonus_Strength", "Statistic_Dexterity", "Statistic_Bonus_Dexterity", "Statistic_Agility", "Statistic_Bonus_Agility", "Skill_Bonus_Armor_Use", "Skill_Ranks_Armor_Use", "Roundtime_Strength", "Roundtime_Reduction"]	
		statistic_names = ["Strength", "Dexterity", "Agility"]
		skill_names = ["Armor Use"]
				
		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}
		base_bonus_arr = {}		

		override_options = self.Find_Overrides_By_Tags(effects_list)
		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		
		
		main_hand = self.Get_Gear_By_Order(self.gear_main_weapon.get())
		main_hand_name = main_hand.name.get()
		other_hand = self.Get_Gear_By_Order(self.gear_other_hand.get())
		other_hand_name = other_hand.name.get()
		armor = self.Get_Gear_By_Order(self.gear_armor.get())	
		armor_name = armor.name.get()		
		armor_base_roundtime = int(armor.gear_traits["roundtime"])
		main_hand_base_speed = int(main_hand.gear_traits["base_speed"])
		main_hand_min_speed = int(main_hand.gear_traits["minimum_speed"])
		
		weapon_types = main_hand.skills.split("/")	
				
		if alt_mode == "TWC":
			weapon_type = ""
			other_hand_base_speed = int(other_hand.gear_traits["base_speed"])
			other_hand_weight = int(other_hand.weight)
			qstrike_stamina_cost = 10 + main_hand_base_speed + math.floor(other_hand_base_speed / 2)
			RT_type = "Two Weapon Combat"
		elif alt_mode == "UAC":
			weapon_type = ""
			j_base_speed = 2
			pg_base_speed = 3
			k_base_speed = 4
			j_qstrike_stamina_cost = 12
			pg_qstrike_stamina_cost = 13
			k_qstrike_stamina_cost = 14
			RT_type = "Unarmed Combat"
		elif ("Two-Handed Weapons" in main_hand.skills or "Polearm Weapons" in main_hand.skills) and "One-Handed" not in main_hand_name:
			# Needed for GRIPable weapons like Bastard Swords and Katanas
			weapon_type = "Two Handed Weapon"
			qstrike_stamina_cost = 10 + math.floor(main_hand_base_speed * 1.5)
			RT_type = "Melee"
		elif "Ranged Weapons" in main_hand.skills:
			weapon_type = "Ranged Weapons"
			qstrike_stamina_cost = 10 + math.floor(main_hand_base_speed * 2.5)	
			RT_type = "Ranged"	
		else:	
			weapon_type = weapon_types[0]
			qstrike_stamina_cost = 10 + main_hand_base_speed
			RT_type = "Melee"

			
		if "Stamina Cost" in override_options:
			calculations.override_dict["Stamina Cost"] = qstrike_stamina_cost
						
						
		if alt_mode == "UAC":
			j_normal_totals = []
			pg_normal_totals = []
			k_normal_totals = []
			aimed_j_normal_totals = []
			aimed_pg_normal_totals = []
			aimed_k_normal_totals = []
		else:
			normal_totals = []
			aimed_or_hidden_totals = []	
			aimed_and_hidden_totals = []
		
		
		loop_range = self.Set_Graph_Labels(skill_names, "%s Roundtime and Qstrike Cost" % (RT_type), "Seconds")	
		
		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			stat_enh_bonus = 0
			effects_total = 0
			stat_enhancive_totals = {}
			stat_tooltip_arr = {}
			skill_tooltip_arr = {}
			effects_tooltip_text = ""
			tooltip_array = []
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: %s Roundtime and Qstrike Cost\n" % (i, RT_type)
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()	
					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: %s Roundtime & Qstrike Cost\n" % ("{:,}".format(i), RT_type)
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[100].get()					
		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
					

			# Calculate Statistic bonus	
			for stat in statistic_names:
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, stat, 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_%s" % stat], lists_of_effects_by_tag["Statistic_%s" % stat]], 
												["Statistic_Bonus_%s" % stat, "Statistic_%s" % stat], 
												"stat_inc_to_bonus")													

				stat_enhancive_totals[stat] = int(base_stat_arr[stat] + min(50, stat_enh_bonus))
				stat_tooltip_arr[stat] = "%s  %s base bonus\n" % (("%+d" % base_stat_arr[stat]).rjust(11), stat) + temp_tooltip		
	
			
						
			# Calculate Armor Use ranks
			armor_use_bonus, temp_tooltip = self.Combine_Effects(i, "Armor Use", base_ranks_arr["Armor Use"], 
											[lists_of_effects_by_tag["Skill_Bonus_Armor_Use"], lists_of_effects_by_tag["Skill_Ranks_Armor_Use"]], 
											["Skill_Bonus_Armor_Use", "Skill_Ranks_Armor_Use"], 
											"skill_ranks_to_bonus")

			armor_use_total = base_bonus_arr["Armor Use"] + min(50, armor_use_bonus)		
			armor_tootip = "".join( [ "%s  Armor Use skill bonus\n" % (("%+d" % armor_use_total).rjust(7)),
									"%s  bonus from %s Armor Use base ranks\n" % (("%+d" % base_bonus_arr["Armor Use"]).rjust(11), base_ranks_arr["Armor Use"]),
									temp_tooltip
									])				
			
			
			# Calculate Roundtime Reduction effects
			roundtime_reduction_effects, roundtime_reduction_tooltip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["Roundtime_Reduction"]], ["Roundtime_Reduction"], "effect_display")
			
			if roundtime_reduction_tooltip != "":
				roundtime_reduction_tooltip = "%s  Bonus from Roundtime Reduction effects\n" % (("%+d" % roundtime_reduction_effects).rjust(4)) + roundtime_reduction_tooltip
				
			# Calculate Roundtime Strength effects
			roundtime_strength_effects, roundtime_strength_tooltip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["Roundtime_Strength"]], ["Roundtime_Strength"], "effect_display")
			
			if roundtime_strength_tooltip != "":
				roundtime_strength_tooltip = "%s  Bonus from Roundtime Reduction effects\n" % (("%+d" % roundtime_strength_effects).rjust(12)) + roundtime_strength_tooltip

				
							
			# Main Calculation section
			armor_roundtime =  min(armor_base_roundtime - math.floor(armor_use_total/20), 0) 	
		
			if alt_mode == "TWC":
				strength_offset = math.floor((stat_enhancive_totals["Strength"] + roundtime_strength_effects + 10) / 15) 				
				raw_weight_penalty = max(0, other_hand_weight - 2 - strength_offset)
				weight_penalty = min(raw_weight_penalty, 3)
				left_hand_speed = max(other_hand_base_speed - 2, 0)
				final_base_speed = main_hand_base_speed + left_hand_speed + weight_penalty
				speed_offset = math.floor((stat_enhancive_totals["Agility"] + stat_enhancive_totals["Dexterity"]) / 15)
				
				raw_normal_roundtime = final_base_speed + armor_roundtime + 0 - speed_offset - roundtime_reduction_effects
				normal_roundtime = max(max(1, final_base_speed - roundtime_reduction_effects), raw_normal_roundtime)
				raw_aimed_roundtime = raw_normal_roundtime + 3
				aimed_or_hidden_roundtime = max(max(1, final_base_speed +1 - roundtime_reduction_effects), raw_aimed_roundtime)

				
				normal_formula_tooltip = "%s = %s + %s - %s - %s.  %s vs min %s\n" % (normal_roundtime, final_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_normal_roundtime, max(1, final_base_speed - roundtime_reduction_effects))
				aimed_formula_tooltip = "%s = %s + %s - %s - %s + 3.  %s vs min %s\n" % (aimed_or_hidden_roundtime, final_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_aimed_roundtime, max(1, final_base_speed + 1 - roundtime_reduction_effects))
				
				twc_base_speed_tooltip = "%s  Two Weapon Combat base speed  (%s + %s + %s)\n" % (("%+d" % final_base_speed).rjust(4), main_hand_base_speed, left_hand_speed, weight_penalty)
				main_base_speed_tooltip = "%s  %s base speed\n" % (("%+d" % main_hand_base_speed).rjust(6), main_hand_name)
				left_hand_speed_tooltip = "%s  Other hand weapon speed  (%s - 2).  min 0 \n" % (("%+d" % left_hand_speed).rjust(6), other_hand_base_speed)
				other_base_speed_tooltip = "%s  %s base speed\n" % (("%+d" % other_hand_base_speed).rjust(8), other_hand_name)
				weight_tooltip = "%s  Off-Hand weight penalty (%s - 2 - %s).  min 0, max 3\n" % (("%+d" % weight_penalty).rjust(6), other_hand_weight, strength_offset)
				other_base_weight_tooltip = "%s  %s weight\n" % (("%+d" % other_hand_weight).rjust(8), other_hand_name)
				strength_offset_tooltip = "%s  Strength offset (%s + %s + 10) / 15\n" % (("%+d" % strength_offset).rjust(8), stat_enhancive_totals["Strength"], roundtime_strength_effects)
				other_base_speed_tooltip2 = "%s  %s base speed\n" % (("%+d" % other_hand_base_speed).rjust(6), other_hand_name)
				
				
				armor_formula_tooltip = "%s  Armor roundtime penalty  %s - (%s /20).  min 0  \n" % (("%+d" % armor_roundtime).rjust(4), armor_base_roundtime, armor_use_total)
				armor_penalty_tooltip = "%s  %s base penalty\n" % (("%+d" % armor_base_roundtime).rjust(7), armor_name)
				speed_offset_tooltip = "%s  Speed offset  (%s + %s) / 15.  min 0\n" % (("%+d" % speed_offset).rjust(4), stat_enhancive_totals["Agility"], stat_enhancive_totals["Dexterity"])
				qstrike_formula_tooltip = "%s = 10 + %s + (%s / 2)\n" % (qstrike_stamina_cost, main_hand_base_speed, other_hand_base_speed)

				# Create Tooltip info		
				tooltip = "".join([		
							tooltip,
							"%s  Normal Roundtime\n" % ("%d" % normal_roundtime).rjust(4),
							"%s  Aimed roundtime\n" % ("%d" % aimed_or_hidden_roundtime).rjust(4),
							"%s  Qstrike stamina cost per second\n" % ("%d" % qstrike_stamina_cost).rjust(4),
							"--Roundtime--\n",
							normal_formula_tooltip,
							"--Aimed Roundtime--\n",
							aimed_formula_tooltip,			
							"--Roundtime Details--\n",		
							twc_base_speed_tooltip,
							main_base_speed_tooltip,
							left_hand_speed_tooltip,
							other_base_speed_tooltip,
							weight_tooltip,
							other_base_weight_tooltip,
							strength_offset_tooltip,
							armor_formula_tooltip,
							armor_penalty_tooltip,
							armor_tootip,
							speed_offset_tooltip,
							stat_tooltip_arr["Agility"],
							stat_tooltip_arr["Dexterity"],
							roundtime_reduction_tooltip,	
							"--Qstrike Stamina cost per second--\n",
							qstrike_formula_tooltip,
							main_base_speed_tooltip,	
							other_base_speed_tooltip2,
						])	
				
			elif alt_mode == "UAC":
				speed_offset = max(0, math.floor((stat_enhancive_totals["Agility"] + stat_enhancive_totals["Dexterity"]) / 15))
				
				raw_j_roundtime = j_base_speed + armor_roundtime + 0 - speed_offset - roundtime_reduction_effects
				raw_aimed_j_roundtime = j_base_speed + armor_roundtime + 0 + 3 - speed_offset - roundtime_reduction_effects
				raw_pg_roundtime = pg_base_speed + armor_roundtime + 0 - speed_offset - roundtime_reduction_effects
				raw_aimed_pg_roundtime = pg_base_speed + armor_roundtime + 0 + 3 - speed_offset - roundtime_reduction_effects
				raw_k_roundtime = k_base_speed + armor_roundtime + 0 - speed_offset - roundtime_reduction_effects
				raw_aimed_k_roundtime = k_base_speed + armor_roundtime + 0 + 3 - speed_offset - roundtime_reduction_effects
				
				j_roundtime = max(max(1, j_base_speed - roundtime_reduction_effects), raw_j_roundtime)
				aimed_j_roundtime = max(max(1, j_base_speed + 1 - roundtime_reduction_effects), raw_aimed_j_roundtime)		
				pg_roundtime = max(max(1, pg_base_speed - roundtime_reduction_effects), raw_pg_roundtime)
				aimed_pg_roundtime = max(max(1, pg_base_speed + 1 - roundtime_reduction_effects), raw_aimed_pg_roundtime)			
				k_roundtime = max(max(1, k_base_speed - roundtime_reduction_effects), raw_k_roundtime)
				aimed_k_roundtime = max(max(1, k_base_speed + 1 - roundtime_reduction_effects), raw_aimed_k_roundtime)			

				
				j_formula_tooltip = "%s = %s + %s - %s - %s.  %s vs min %s\n" % (j_roundtime, j_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_j_roundtime, max(1, j_base_speed - roundtime_reduction_effects))
				aimed_j_formula_tooltip = "%s = %s + %s - %s - %s + 3.  %s vs min %s\n" % (aimed_j_roundtime, j_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_aimed_j_roundtime, max(1, j_base_speed + 1 - roundtime_reduction_effects))				
				j_base_speed_tooltip = "%s  Jab base speed\n" % (("%+d" % j_base_speed).rjust(4))	
				
				pg_formula_tooltip = "%s = %s + %s - %s - %s.  %s vs min %s\n" % (pg_roundtime, pg_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_pg_roundtime, max(1, pg_base_speed - roundtime_reduction_effects))
				aimed_pg_formula_tooltip = "%s = %s + %s - %s - %s + 3.  %s vs min %s\n" % (aimed_pg_roundtime, pg_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_aimed_pg_roundtime, max(1, pg_base_speed + 1 - roundtime_reduction_effects))				
				pg_base_speed_tooltip = "%s  Punch/Grapple base speed\n" % (("%+d" % pg_base_speed).rjust(4))				
				
				k_formula_tooltip = "%s = %s + %s - %s - %s.  %s vs min %s\n" % (k_roundtime, k_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_k_roundtime, max(1, k_base_speed - roundtime_reduction_effects))
				aimed_k_formula_tooltip = "%s = %s + %s - %s - %s + 3.  %s vs min %s\n" % (aimed_k_roundtime, k_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_aimed_k_roundtime, max(1, k_base_speed + 1 - roundtime_reduction_effects))				
				k_base_speed_tooltip = "%s  Kick base speed\n" % (("%+d" % k_base_speed).rjust(4))
				
				armor_formula_tooltip = "%s  Armor roundtime penalty  %s - (%s /20).  min 0  \n" % (("%+d" % armor_roundtime).rjust(4), armor_base_roundtime, armor_use_total)
				armor_penalty_tooltip = "%s  %s base penalty\n" % (("%+d" % armor_base_roundtime).rjust(7), armor_name)
				speed_offset_tooltip = "%s  Speed offset  (%s + %s) / 15.  min 0\n" % (("%+d" % speed_offset).rjust(4), stat_enhancive_totals["Agility"], stat_enhancive_totals["Dexterity"])
				
				j_qstrike_formula_tooltip = "%s = 10 + %s\n" % (pg_qstrike_stamina_cost, j_base_speed)
				pg_qstrike_formula_tooltip = "%s = 10 + %s\n" % (pg_qstrike_stamina_cost, pg_base_speed)
				k_qstrike_formula_tooltip = "%s = 10 + %s\n" % (k_qstrike_stamina_cost, k_base_speed)

				
				
				# Create Tooltip info		
				tooltip = "".join([		
							tooltip,
							"%s  Jab roundtime\n" % ("%d" % j_roundtime).rjust(4),
							"%s  Punch/Grapple roundtime\n" % ("%d" % pg_roundtime).rjust(4),
							"%s  Kicked roundtime\n" % ("%d" % k_roundtime).rjust(4),
							"%s  Aimed jab roundtime\n" % ("%d" % aimed_j_roundtime).rjust(4),
							"%s  Aimed punch/grapple roundtime\n" % ("%d" % aimed_pg_roundtime).rjust(4),
							"%s  Aimed kick roundtime\n" % ("%d" % aimed_k_roundtime).rjust(4),
							"%s  Punch qstrike stamina cost per second\n" % ("%d" % pg_qstrike_stamina_cost).rjust(4),
							"%s  Kick qstrike stamina cost per second\n" % ("%d" % k_qstrike_stamina_cost).rjust(4),
							"--Jab Roundtime--\n",
							j_formula_tooltip,							
							"--Punch/Grapple Roundtime--\n",
							pg_formula_tooltip,
							"--Kick Roundtime--\n",
							k_formula_tooltip,
							"--Aimed Jab Roundtime--\n",
							aimed_j_formula_tooltip,			
							"--Aimed Punch/Grapple Roundtime--\n",
							aimed_pg_formula_tooltip,			
							"--Aimed Kick Roundtime--\n",
							aimed_k_formula_tooltip,
							"--Roundtime Details--\n",		
							j_base_speed_tooltip,	
							pg_base_speed_tooltip,	
							k_base_speed_tooltip,
							armor_formula_tooltip,
							armor_penalty_tooltip,
							armor_tootip,
							speed_offset_tooltip,
							stat_tooltip_arr["Agility"],
							stat_tooltip_arr["Dexterity"],
							roundtime_reduction_tooltip,	
							"--Jab Qstrike Stamina cost per second--\n",
							j_qstrike_formula_tooltip,
							j_base_speed_tooltip,
							"--Punch/Grapple Qstrike Stamina cost per second--\n",
							pg_qstrike_formula_tooltip,
							pg_base_speed_tooltip,					
							"--Kick Qstrike Stamina cost per second--\n",
							k_qstrike_formula_tooltip,
							k_base_speed_tooltip,					
						])			
				
			elif weapon_type == "Ranged Weapons" or weapon_type == "Thrown Weapons":	
				if "Crossbow" in main_hand_name:
					speed_offset = 0
				else:
					speed_offset = max(0, math.floor((stat_enhancive_totals["Strength"] + roundtime_strength_effects) / 10))
				
				if weapon_type == "Ranged Weapons":
					final_base_speed = main_hand_base_speed	
				else:
					final_base_speed = 3

				raw_normal_roundtime = final_base_speed + armor_roundtime + 0 - speed_offset - roundtime_reduction_effects
				normal_roundtime = max(max(1, main_hand_min_speed - roundtime_reduction_effects), raw_normal_roundtime)
				raw_aimed_roundtime = raw_normal_roundtime + 1
				aimed_or_hidden_roundtime = max(max(1, main_hand_min_speed - roundtime_reduction_effects), raw_aimed_roundtime)
				raw_aimed_and_hidden_roundtime = raw_normal_roundtime + 2
				aimed_and_hidden_roundtime = max(max(1, main_hand_min_speed - roundtime_reduction_effects), raw_aimed_and_hidden_roundtime)
				
				normal_formula_tooltip = "%s = %s + %s - %s - %s.  %s vs min %s\n" % (normal_roundtime, final_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_normal_roundtime, max(0, main_hand_min_speed - roundtime_reduction_effects))
				aimed_or_hidden_formula_tooltip = "%s = %s + %s - %s - %s + 1.  %s vs min %s\n" % (aimed_or_hidden_roundtime, final_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_aimed_roundtime, max(1, main_hand_min_speed - roundtime_reduction_effects))
				aimed_and_hidden_formula_tooltip = "%s = %s + %s - %s - %s + 2.  %s vs min %s\n" % (aimed_and_hidden_roundtime, final_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_aimed_roundtime, max(1, main_hand_min_speed - roundtime_reduction_effects))
				
				main_base_speed_tooltip = "%s  %s base speed\n" % (("%+d" % final_base_speed).rjust(4), main_hand_name)
				armor_formula_tooltip = "%s  Armor roundtime penalty  %s - (%s /20).  min 0  \n" % (("%+d" % armor_roundtime).rjust(4), armor_base_roundtime, armor_use_total)
				armor_penalty_tooltip = "%s  %s base penalty\n" % (("%+d" % armor_base_roundtime).rjust(6), armor_name)
				speed_offset_tooltip = "%s  Speed offset  (%s + %s) / 10.  min 0\n" % (("%+d" % speed_offset).rjust(4), stat_enhancive_totals["Strength"], roundtime_strength_effects)
				if weapon_type == "Ranged Weapons":
					qstrike_formula_tooltip = "%s = 10 + (%s * 2.5)\n" % (qstrike_stamina_cost, final_base_speed)
				else:
					qstrike_formula_tooltip = "%s = 10 + %s\n" % (qstrike_stamina_cost, final_base_speed)
	
				# Create Tooltip info		
				tooltip = "".join([		
							tooltip,
							"%s  Normal Roundtime\n" % ("%d" % normal_roundtime).rjust(4),
							"%s  Aimed or hidden roundtime\n" % ("%d" % aimed_or_hidden_roundtime).rjust(4),
							"%s  Aimed and hidden roundtime\n" % ("%d" % aimed_and_hidden_roundtime).rjust(4),
							"%s  Qstrike stamina cost per second\n" % ("%d" % qstrike_stamina_cost).rjust(4),
							"--Roundtime--\n",
							normal_formula_tooltip,
							"--Aimed or Hidden Roundtime--\n",
							aimed_or_hidden_formula_tooltip,					
							"--Aimed and Hidden Roundtime--\n",	
							aimed_and_hidden_formula_tooltip,				
							"--Roundtime Details--\n",		
							main_base_speed_tooltip,
							armor_formula_tooltip,
							armor_penalty_tooltip,
							armor_tootip,
							speed_offset_tooltip,
							stat_tooltip_arr["Strength"],
							roundtime_strength_tooltip,
							roundtime_reduction_tooltip,	
							"--Qstrike Stamina cost per second--\n",
							qstrike_formula_tooltip,
							main_base_speed_tooltip,					
						])		
						
			else:			
				final_base_speed = main_hand_base_speed	
				speed_offset = max(0, math.floor((stat_enhancive_totals["Agility"] + stat_enhancive_totals["Dexterity"]) / 15))
			
				raw_normal_roundtime = final_base_speed + armor_roundtime + 0 - speed_offset - roundtime_reduction_effects
				raw_aimed_roundtime = final_base_speed + armor_roundtime + 0 + 3 - speed_offset - roundtime_reduction_effects
				normal_roundtime = max(max(1, main_hand_min_speed - roundtime_reduction_effects), raw_normal_roundtime)
				aimed_or_hidden_roundtime = max(max(1, main_hand_min_speed + 1 - roundtime_reduction_effects), raw_aimed_roundtime)
				
				normal_formula_tooltip = "%s = %s + %s - %s - %s.  %s vs min %s\n" % (normal_roundtime, final_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_normal_roundtime, max(1, main_hand_min_speed - roundtime_reduction_effects))
				aimed_formula_tooltip = "%s = %s + %s - %s - %s + 3.  %s vs min %s\n" % (aimed_or_hidden_roundtime, final_base_speed, armor_roundtime, speed_offset, roundtime_reduction_effects, raw_aimed_roundtime, max(1, main_hand_min_speed + 1 - roundtime_reduction_effects))
				main_base_speed_tooltip = "%s  %s base speed\n" % (("%+d" % final_base_speed).rjust(4), main_hand_name)
				armor_formula_tooltip = "%s  Armor roundtime penalty  %s - (%s /20).  min 0  \n" % (("%+d" % armor_roundtime).rjust(4), armor_base_roundtime, armor_use_total)
				armor_penalty_tooltip = "%s  %s base penalty\n" % (("%+d" % armor_base_roundtime).rjust(7), armor_name)
				speed_offset_tooltip = "%s  Speed offset  (%s + %s) / 15.  min 0\n" % (("%+d" % speed_offset).rjust(4), stat_enhancive_totals["Agility"], stat_enhancive_totals["Dexterity"])
				if weapon_type == "Two Handed Weapon":
					qstrike_formula_tooltip = "%s = 10 + (%s * 1.5)\n" % (qstrike_stamina_cost, final_base_speed)
				else:
					qstrike_formula_tooltip = "%s = 10 + %s\n" % (qstrike_stamina_cost, final_base_speed)

				# Create Tooltip info		
				tooltip = "".join([		
							tooltip,
							"%s  Normal Roundtime\n" % ("%d" % normal_roundtime).rjust(4),
							"%s  Aimed roundtime\n" % ("%d" % aimed_or_hidden_roundtime).rjust(4),
							"%s  Qstrike stamina cost per second\n" % ("%d" % qstrike_stamina_cost).rjust(4),
							"--Roundtime--\n",
							normal_formula_tooltip,
							"--Aimed Roundtime--\n",
							aimed_formula_tooltip,			
							"--Roundtime Details--\n",		
							main_base_speed_tooltip,
							armor_formula_tooltip,
							armor_penalty_tooltip,
							armor_tootip,
							speed_offset_tooltip,
							stat_tooltip_arr["Agility"],
							stat_tooltip_arr["Dexterity"],
							roundtime_reduction_tooltip,	
							"--Qstrike Stamina cost per second--\n",
							qstrike_formula_tooltip,
							main_base_speed_tooltip,					
						])				
		
				
			# Update totals arrays and tooltip array
			if alt_mode == "UAC":
				j_normal_totals.append(j_roundtime)
				pg_normal_totals.append(pg_roundtime)
				k_normal_totals.append(k_roundtime)
				aimed_j_normal_totals.append(aimed_j_roundtime)
				aimed_pg_normal_totals.append(aimed_pg_roundtime)
				aimed_k_normal_totals.append(aimed_k_roundtime)
			else:				
				normal_totals.append(normal_roundtime)			
				aimed_or_hidden_totals.append(aimed_or_hidden_roundtime)	
			
			if weapon_type == "Ranged Weapons" or weapon_type == "Thrown Weapons":
				aimed_and_hidden_totals.append(aimed_and_hidden_roundtime)		

				
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		
		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = 0
		if alt_mode == "UAC":
			self.graph_information.graph_yaxis_max = aimed_k_normal_totals[0] + 1	
		elif weapon_type == "Ranged Weapons" or weapon_type == "Thrown Weapons":		
			self.graph_information.graph_yaxis_max = aimed_and_hidden_totals[0] + 1		
		else:
			self.graph_information.graph_yaxis_max = aimed_or_hidden_totals[0] + 1		
		

		# Append the completed lists to graph_infomation object and create legend
		
		if alt_mode == "UAC":
			self.graph_information.graph_num_lines = 6
			self.graph_information.graph_legend_columns = 3
			self.graph_information.graph_data_lists.append(j_normal_totals)	
			self.graph_information.graph_legend_labels.append("Jab RT")
			self.graph_information.graph_legend_styles.append("y^-")	
			self.graph_information.graph_data_lists.append(aimed_j_normal_totals)		
			self.graph_information.graph_legend_labels.append("Aimed Jab RT")
			self.graph_information.graph_legend_styles.append("r^-")
			self.graph_information.graph_data_lists.append(pg_normal_totals)	
			self.graph_information.graph_legend_labels.append("Punch/Grapple RT")
			self.graph_information.graph_legend_styles.append("yo-")	
			self.graph_information.graph_data_lists.append(aimed_pg_normal_totals)		
			self.graph_information.graph_legend_labels.append("Aimed Punch/Grapple RT")
			self.graph_information.graph_legend_styles.append("ro-")
			self.graph_information.graph_data_lists.append(k_normal_totals)		
			self.graph_information.graph_legend_labels.append("Kick RT")
			self.graph_information.graph_legend_styles.append("ys-")
			self.graph_information.graph_data_lists.append(aimed_k_normal_totals)		
			self.graph_information.graph_legend_labels.append("Aimed Kick RT")
			self.graph_information.graph_legend_styles.append("rs-")
		elif weapon_type == "Ranged Weapons" or weapon_type == "Thrown Weapons":		
			self.graph_information.graph_num_lines = 3
			self.graph_information.graph_legend_columns = 3		
			self.graph_information.graph_data_lists.append(normal_totals)
			self.graph_information.graph_legend_labels.append("Normal RT")
			self.graph_information.graph_legend_styles.append("ro-")
			self.graph_information.graph_data_lists.append(aimed_or_hidden_totals)	
			self.graph_information.graph_legend_labels.append("Aimed or Hidden RT")	
			self.graph_information.graph_legend_styles.append("b*-")			
			self.graph_information.graph_data_lists.append(aimed_and_hidden_totals)	
			self.graph_information.graph_legend_labels.append("Aimed & Hidden RT")	
			self.graph_information.graph_legend_styles.append("gs-")			
		else:	
			self.graph_information.graph_num_lines = 2
			self.graph_information.graph_legend_columns = 2	
			self.graph_information.graph_data_lists.append(normal_totals)
			self.graph_information.graph_legend_labels.append("Normal RT")
			self.graph_information.graph_legend_styles.append("ro-")
			self.graph_information.graph_data_lists.append(aimed_or_hidden_totals)	
			self.graph_information.graph_legend_labels.append("Aimed RT")	
			self.graph_information.graph_legend_styles.append("b*-")				

		
	# This method is used to calculate the character's Casting Strength (CS) from level 0-100 or across postcap training.
	# CS is calculated based on spell circles and due to the large amount of spell circles that exist in game, only 1-3 
	# spell circles are calculated at once and this is determined by the profession (or just Arcane) picked by the user.
	# All statistics skills, and effects that increase statistics or CS itself are included in these calculations.		
	def Formula_Casting_Strength(self, display_spell_circles, statistic_names):
		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}
		skill_names = []
		
		cs_effects_per_display = {}
		cs_tooltips_per_display = {}
		cs_tooltips_primary_secondary = ""
		casting_strength_totals = {}
		casting_strength_per_display_per_character = {}		
		character_spell_circles = globals.character.profession.spell_circles
		effects_list = ["CS_All", "CS_Elemental", "CS_Mental", "CS_Spiritual", "CS_Sorcerer", "CS_Special"]
		mystic_focus_as_override = 0
		mystic_focus_miu_override = 0

		# Populate the dictionaries with spell circle keys	
		for circle in display_spell_circles:
			self.graph_information.graph_legend_labels.append(circle)
			casting_strength_totals[circle] = []
			cs_effects_per_display[circle] = []
			cs_tooltips_per_display[circle] = []
			casting_strength_per_display_per_character[circle] = {}
			
		# Populate relevant skills and statistics	
		for circle in character_spell_circles:
			skill_names.append("Spell Research, %s" % circle)		
			for display in display_spell_circles:
				casting_strength_per_display_per_character[display][circle] = []
			
		for stat in statistic_names:
			effects_list.append("Statistic_Bonus_%s" % stat)
			effects_list.append("Statistic_%s" % stat)				
			
			
		override_options = self.Find_Overrides_By_Tags(effects_list)	
		
		# Set the overrides if needed
		for option in override_options:			
			if option == "Armor Group":
				calculations.override_dict["Armor Group"] = int(self.Get_Gear_By_Order(self.gear_armor.get()).gear_traits["AG"])	
			elif option == "Influence Bonus":
				if "Influence" not in statistic_names:
					effects_list.extend(("Statistic_Influence", "Statistic_Bonus_Influence"))
					statistic_names.append("Influence")				
			elif option == "Wisdom Bonus":
				if "Wisdom" not in statistic_names:
					effects_list.extend(("Statistic_Wisdom", "Statistic_Bonus_Wisdom"))
					statistic_names.append("Wisdom")
			elif option == "CS Boost AS":
				if "Arcane Symbols" not in skill_names:
					effects_list.extend(("Skill_Ranks_Arcane_Symbols", "Skill_Bonus_Arcane_Symbols"))
					skill_names.append("Arcane Symbols")
			elif option == "CS Boost MIU":
				if "Magic Item Use" not in skill_names:
					effects_list.extend(("Skill_Ranks_Magic_Item_Use", "Skill_Bonus_Magic_Item_Use"))
					skill_names.append("Magic Item Use")
			elif option == "425 CS":
				mystic_focus_as_override -= 1
				mystic_focus_miu_override -= 1
			elif option == "1711 AS":
				mystic_focus_as_override += 1
				if "Arcane Symbols" not in skill_names:
					effects_list.extend(("Skill_Ranks_Arcane_Symbols", "Skill_Bonus_Arcane_Symbols"))
					skill_names.append("Arcane Symbols")
			elif option == "1711 MIU":
				mystic_focus_miu_override += 1
				if "Magic Item Use" not in skill_names:
					effects_list.extend(("Skill_Ranks_Magic_Item_Use", "Skill_Bonus_Magic_Item_Use"))
					skill_names.append("Magic Item Use")

		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		loop_range = self.Set_Graph_Labels(skill_names, "CS by Spell Circle", "Casting Strength")			


		# Begin the big loop to calculate all the data	
		for i in loop_range:
			stat_enh_bonus = 0
			effects_total = 0
			stat_enhancive_totals = {}
			stat_tooltip_text = ""
			stat_tooltip_arr = {}
			effects_tooltip_text = ""
			AS_MIU_CS_Boost = 0
			AS_MIU_tooltip_text = ""
						
						
			if self.calc_style == 1:
				tooltip = "Level %s: Casting Strength\n" % (i)
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()	
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Casting Strength\n" % ("{:,}".format(i))
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[100].get()	
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
		

			# Calculate Statistic bonus	
			for stat in statistic_names:
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, stat, 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_%s" % stat], lists_of_effects_by_tag["Statistic_%s" % stat]], 
												["Statistic_Bonus_%s" % stat, "Statistic_%s" % stat], 
												"stat_inc_to_bonus")													

				stat_enhancive_totals[stat] = base_stat_arr[stat] + min(50, stat_enh_bonus)
				stat_tooltip_arr[stat] = "       %s  %s base bonus\n" % (("%+d" % base_stat_arr[stat]).rjust(4), stat) + temp_tooltip		
	
			# Set override options
			if "Influence Bonus" in override_options:
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, "Influence", 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_Influence"], lists_of_effects_by_tag["Statistic_Influence"]], 
												["Statistic_Bonus_Influence", "Statistic_Influence"], 
												"stat_inc_to_bonus")		

				calculations.override_dict["Influence Bonus"] = base_stat_arr["Influence"] + stat_enh_bonus
											
			if "Wisdom Bonus" in override_options:
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, "Wisdom", 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_Wisdom"], lists_of_effects_by_tag["Statistic_Wisdom"]], 
												["Statistic_Bonus_Wisdom", "Statistic_Wisdom"], 
												"stat_inc_to_bonus")			
												
				calculations.override_dict["Wisdom Bonus"] = base_stat_arr["Wisdom"] + stat_enh_bonus		
				
			if "CS Boost AS" in override_options or mystic_focus_as_override > 0:
				result, AS_MIU_tooltip_text = self.Combine_Effects(i, "", base_ranks_arr["Arcane Symbols"], 
												[lists_of_effects_by_tag["Skill_Ranks_Arcane_Symbols"], lists_of_effects_by_tag["Skill_Bonus_Arcane_Symbols"]], 
												["Skill_Ranks_Arcane_Symbols", "Skill_Bonus_Arcane_Symbols"], 
												"skill_bonus_to_ranks")		
												
				calculations.override_dict["Arcane Symbols ranks"] = result + base_ranks_arr["Arcane Symbols"]	
				AS_MIU_CS_Boost, AS_MIU_tooltip_text = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["CS_Special"]], ["CS_Special"], "effect_display")
																
												
			elif "CS Boost MIU" in override_options or mystic_focus_miu_override > 0:
				result, AS_MIU_tooltip_text = self.Combine_Effects(i, "", base_ranks_arr["Magic Item Use"], 
												[lists_of_effects_by_tag["Skill_Ranks_Magic_Item_Use"], lists_of_effects_by_tag["Skill_Bonus_Magic_Item_Use"]], 
												["Skill_Ranks_Magic_Item_Use", "Skill_Bonus_Magic_Item_Use"], 
												"skill_bonus_to_ranks")		
												
				calculations.override_dict["Magic Item Use ranks"]	= result + base_ranks_arr["Magic Item Use"]							
				AS_MIU_CS_Boost, AS_MIU_tooltip_text = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["CS_Special"]], ["CS_Special"], "effect_display")	
				
												
				 	
		
			# Calculate CS. Cycle through the spell circles we are showing and compare to each character user spell circles. 
			# Treat as primary if the match or secondary if not
			base_cs = min(300, i*3)
			current_cs = 0.0	
			total_cs = 0
			cs_stat = 0
			level = min(i, 100)
			level_secondary_var = math.ceil(i * 2/3)
			 
			for display_circle in display_spell_circles:
				total_cs = base_cs
				cs_tooltips_primary_secondary = ""
				for char_circle in character_spell_circles:
					ranks = base_ranks_arr["Spell Research, %s" % char_circle]
					current_cs = 0.0	
					# Do calculations if char_circle is the primary circle 
					if display_circle == char_circle:
						while ranks > 0:							
							if ranks <= level:
								current_cs += 1
							elif ranks <= (level+20):
								current_cs += 0.75
							elif ranks <= (level+60):
								current_cs += 0.5
							elif ranks <= (level+100):
								current_cs += 0.25
							else:
								current_cs += 0.125								
								
							ranks -= 1
						current_cs = int(math.ceil(current_cs))
						cs_tooltips_primary_secondary = "%s  Bonus from Primary Circle\n          %s  %s base ranks\n" % (("%+d" % current_cs).rjust(4), base_ranks_arr["Spell Research, %s" % char_circle], char_circle) + cs_tooltips_primary_secondary
						
					# Otherwise calculate it as a secondary circle
					else: 
						while ranks > 0:							
							if ranks <= level_secondary_var:
								current_cs += 0.333
							elif ranks <= level:
								current_cs += 0.1
							else:
								current_cs += 0.5								
								
							ranks -= 1
						current_cs = int(math.ceil(current_cs))
						cs_tooltips_primary_secondary += "%s  Bonus from Secondary Circle\n" % (("%+d" % current_cs).rjust(4))
						cs_tooltips_primary_secondary += "          %s %s base ranks\n" % (base_ranks_arr["Spell Research, %s" % char_circle], char_circle) 
						
					casting_strength_per_display_per_character[display_circle][char_circle] = current_cs					
					total_cs += current_cs

					
				# Calculate CS Effects values		
				effects_total, effects_tooltip_text = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["CS_All"]], ["CS_All"], "effect_display")				
				
				if display_circle == "Bard" or display_circle == "Minor Elemental" or display_circle == "Major Elemental" or display_circle == "Wizard":
					ce_total, ce_tooltip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["CS_Elemental"]], ["CS_Elemental"], "effect_display")	
				elif display_circle == "Monk" or display_circle == "Minor Mental" or display_circle == "Major Mental" or display_circle == "Savant":
					ce_total, ce_tooltip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["CS_Mental"]], ["CS_Mental"], "effect_display")	
				elif display_circle == "Sorcerer" or display_circle == "Arcane":
					ce_total, ce_tooltip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["CS_Sorcerer"]], ["CS_Sorcerer"], "effect_display")	
				else:
					ce_total, ce_tooltip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["CS_Spiritual"]], ["CS_Spiritual"], "effect_display")
						
				effects_total += ce_total
				effects_tooltip_text += ce_tooltip	
				
				if effects_tooltip_text != "" or (AS_MIU_tooltip_text != "" and display_circle not in character_spell_circles):
					effects_total += AS_MIU_CS_Boost
					effects_tooltip_text = "%s  Bonus from Casting Strength effects\n" % (("%+d" % effects_total).rjust(4)) + AS_MIU_tooltip_text + effects_tooltip_text

					
				cs_effects_per_display[display_circle] = effects_total				
				cs_tooltips_per_display[display_circle] = "%s  Base Casting Strength\n" % ("%+d" % base_cs).rjust(4)				
			
			
				# Find the relevant CS stat for the current spell circle and add it to the total CS
				if display_circle == "Bard" or display_circle == "Minor Elemental" or display_circle == "Major Elemental" or display_circle == "Wizard":
					cs_stat = int(stat_enhancive_totals["Aura"])					
					cs_tooltips_per_display[display_circle] += "%s  Bonus from Aura (%+d)\n" % (("%+d" % cs_stat).rjust(4), stat_enhancive_totals["Aura"])
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Aura"]
				elif display_circle == "Monk" or display_circle == "Minor Mental":
					cs_stat = int(stat_enhancive_totals["Logic"])
					cs_tooltips_per_display[display_circle] += "%s  Bonus from Logic (%+d)\n" % (("%+d" % cs_stat).rjust(4), stat_enhancive_totals["Logic"])
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Logic"]	
				elif display_circle == "Major Mental":
					cs_stat = math.ceil((stat_enhancive_totals["Influence"] + stat_enhancive_totals["Logic"]) / 2) 
					cs_tooltips_per_display[display_circle] += "%s  Avg of Influence (%+d), Logic (%+d)\n" % (("%+d" % cs_stat).rjust(4), stat_enhancive_totals["Influence"], stat_enhancive_totals["Logic"])
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Influence"]	
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Logic"]	
				elif display_circle == "Savant":
					cs_stat = math.ceil((stat_enhancive_totals["Discipline"] + stat_enhancive_totals["Logic"]) / 2) 
					cs_tooltips_per_display[display_circle] += "%s  Avg of Discipline (%+d), Logic (%+d)\n" % (("%+d" % cs_stat).rjust(4), stat_enhancive_totals["Discipline"], stat_enhancive_totals["Logic"])
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Discipline"]	
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Logic"]	
				elif display_circle == "Sorcerer":
					cs_stat = math.ceil((stat_enhancive_totals["Aura"] + stat_enhancive_totals["Wisdom"]) / 2) 
					cs_tooltips_per_display[display_circle] += "%s  Avg of Aura (%+d), Logic (%+d)\n" % (("%+d" % cs_stat).rjust(4), stat_enhancive_totals["Aura"], stat_enhancive_totals["Wisdom"])
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Aura"]	
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Wisdom"]	
				elif display_circle == "Arcane":
					cs_stat = math.ceil((stat_enhancive_totals["Wisdom"] + stat_enhancive_totals["Aura"] + stat_enhancive_totals["Logic"]) / 3) 
					cs_tooltips_per_display[display_circle] += "%s  Avg of Aura (%+d), Logic (%+d), Wisdom( %+d)\n" % (("%+d" % cs_stat).rjust(4), stat_enhancive_totals["Aura"], stat_enhancive_totals["Logic"], stat_enhancive_totals["Wisdom"])
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Aura"]	
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Logic"]	
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Wisdom"]	
				else:
					cs_stat = int(stat_enhancive_totals["Wisdom"])			
					cs_tooltips_per_display[display_circle] += "%s  Bonus from Wisdom (%+d)\n" % (("%+d" % cs_stat).rjust(4), stat_enhancive_totals["Wisdom"])
					cs_tooltips_per_display[display_circle] += stat_tooltip_arr["Wisdom"]			
				
				cs_tooltips_per_display[display_circle] += cs_tooltips_primary_secondary
				cs_tooltips_per_display[display_circle] += "  " + effects_tooltip_text

				total_cs += cs_stat + effects_total
				casting_strength_totals[display_circle].append(total_cs)
				cs_tooltips_per_display[display_circle] = ("%+d calculated with:\n" % total_cs) + cs_tooltips_per_display[display_circle]
				cs_tooltips_per_display[display_circle] = "-- %s CS --\n" % (display_circle) + cs_tooltips_per_display[display_circle]
				
				
			# Create Tooltip info
			for display_circle in display_spell_circles:			
				tooltip += "  %+d = %d + %d + " % (casting_strength_totals[display_circle][index], base_cs, cs_stat)
				
				for char_circle in character_spell_circles:
					tooltip += "%d + " % (casting_strength_per_display_per_character[display_circle][char_circle])
				tooltip += "%d  (%s)\n" % (cs_effects_per_display[display_circle], display_circle)
			
			for display_circle in display_spell_circles:		
				tooltip += cs_tooltips_per_display[display_circle]
					
			self.graph_information.tooltip_array.append(tooltip[:-1])	
			index += 1
					
			
		self.graph_information.graph_num_lines = len(display_spell_circles)
		self.graph_information.graph_legend_columns = len(display_spell_circles)
		
		legend_styles = ["r^-", "g*-", "mD-"]
		for style in legend_styles:
			self.graph_information.graph_legend_styles.append(style)					

		ymin = 5000
		ymax = 0
		for circle in display_spell_circles:
			ymin = min(ymin, casting_strength_totals[circle][0])
			ymax = max(ymax, casting_strength_totals[circle][0])
			ymin = min(ymin, casting_strength_totals[circle][-1])
			ymax = max(ymax, casting_strength_totals[circle][-1])
			self.graph_information.graph_data_lists.append(casting_strength_totals[circle])
		self.graph_information.graph_yaxis_min = ymin - 5	
		self.graph_information.graph_yaxis_max = ymax + 5	
		
		
	# This method is used to calculate the character's Target Defense (TD) from level 0-100 or across postcap training.
	# It calculates all four types of TD (elemental, mental, spiritual, sorcerer) at the same time. All statistics, and
	# effects that increase statistics or TD itself are included in this calculation.
	def Formula_Target_Defense(self):
		char_race = globals.character.race
		racial_td = {"Elemental":int(char_race.elemental_td), "Mental":int(char_race.mental_td), "Spiritual":int(char_race.spiritual_td), "Sorcerer":int(char_race.sorc_td)}
		legend_styles = ["r^-", "g*-", "mD-"]
		effects_list = ["TD_All", "TD_Elemental", "TD_Mental", "TD_Spiritual", "TD_Sorcerer"]
		td_types = ["Elemental", "Mental", "Spiritual", "Sorcerer"]
		statistic_names = ["Aura", "Discipline", "Wisdom", ]
		td_totals_by_type = {}
		td_effects_per_type = {}
		td_tooltips_per_type = {}
		td_stat_per_type = {}
		index = 0
		loop_range = [i for i in range(101)]
		base_stat_arr = {}
		postcap_intervals = []
		lists_of_effects_by_tag = {}			
			
		# Setup the effects lists and td lists	
		for stat in statistic_names:
			effects_list.append("Statistic_Bonus_%s" % stat)
			effects_list.append("Statistic_%s" % stat)
			
		for type in td_types:
			td_totals_by_type[type] = []
			td_effects_per_type[type] = []
			td_stat_per_type[type] = []
			td_tooltips_per_type[type] = []
				
					
		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		loop_range = self.Set_Graph_Labels([], "TD by type", "Target Defense")				


		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			sub_tooltip1 = ""	
			sub_tooltip2 = ""					
			ce_total = 0
			stat_enh_bonus = 0
			effects_total = 0
			stat_enhancive_totals = {}
			stat_tooltip_text = ""
			stat_tooltip_arr = {}
			skill_tooltip_arr = {}
			effects_tooltip_text = ""
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Target Defense\n" % (i)
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()	
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Target Defense\n" % ("{:,}".format(i))
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[100].get()					
		

			# Calculate Statistic bonus	
			for stat in statistic_names:
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, stat, 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_%s" % stat], lists_of_effects_by_tag["Statistic_%s" % stat]], 
												["Statistic_Bonus_%s" % stat, "Statistic_%s" % stat], 
												"stat_inc_to_bonus")													

				stat_enhancive_totals[stat] = base_stat_arr[stat] + min(50, stat_enh_bonus)
				stat_tooltip_arr[stat] = "       %s  %s base bonus\n" % (("%+d" % base_stat_arr[stat]).rjust(4), stat) + temp_tooltip					
			
			
			# Calculate each type of TD
			td_base = min(300, i*3)
			level = min(100, i)
			for type in td_types:
				td_tooltips_per_type[type] = ""
						
				# Add the relevant statistics to the TD
				if type == "Elemental":							
					td_stat_per_type[type] = stat_enhancive_totals["Aura"]
					td_tooltips_per_type[type] += "%s  Bonus from Aura (%+d)\n" % (("%+d" % td_stat_per_type[type]).rjust(4), stat_enhancive_totals["Aura"])
					td_tooltips_per_type[type] += stat_tooltip_arr["Aura"]
				elif type == "Mental":					
					td_stat_per_type[type] = stat_enhancive_totals["Discipline"]
					td_tooltips_per_type[type] += "%s  Bonus from Discipline (%+d)\n" % (("%+d" % td_stat_per_type[type]).rjust(4), stat_enhancive_totals["Discipline"])
					td_tooltips_per_type[type] += stat_tooltip_arr["Discipline"]
				elif type == "Spiritual":					
					td_stat_per_type[type] = stat_enhancive_totals["Wisdom"]
					td_tooltips_per_type[type] += "%s  Bonus from Wisdom (%+d)\n" % (("%+d" % td_stat_per_type[type]).rjust(4), stat_enhancive_totals["Wisdom"])
					td_tooltips_per_type[type] += stat_tooltip_arr["Wisdom"]
				elif type == "Sorcerer":					
					td_stat_per_type[type] = math.ceil((stat_enhancive_totals["Aura"] + stat_enhancive_totals["Wisdom"]) / 2)
					td_tooltips_per_type[type] += "%s  Avg of Aura (%+d), Wisdom (%+d)\n" % (("%+d" % td_stat_per_type[type]).rjust(4), stat_enhancive_totals["Aura"], stat_enhancive_totals["Wisdom"])
					td_tooltips_per_type[type] += stat_tooltip_arr["Aura"]
					td_tooltips_per_type[type] += stat_tooltip_arr["Wisdom"]
			
			
				# Calculate TD Effects values		
				effects_total, effects_tooltip_text = self.Combine_Effects(i, "", 0, 
												[lists_of_effects_by_tag["TD_All"], lists_of_effects_by_tag["TD_%s" % type]], 
												["TD_All", "TD_%s" % type], 
												"effect_display")			

				if effects_tooltip_text != "":
						effects_tooltip_text = "  %s  bonus from Target Defense effects\n" % (("%+d" % effects_total).rjust(4)) + effects_tooltip_text	
						
				td_effects_per_type[type] = effects_total	
				td_totals_by_type[type].append(td_base + td_stat_per_type[type] + effects_total)
				
				td_tooltips_per_type[type] = "".join( [ "-- %s TD --\n" % (type),
											("%+d calculated with:\n" % td_totals_by_type[type][index]),
											"%s  Base Target Defense\n" % ("%+d" % td_base).rjust(4),
											"%s  %s racial bonus\n" % (("%+d" % racial_td[type]).rjust(4), char_race.name),
											td_tooltips_per_type[type],
											effects_tooltip_text
											])
			
			# Create Tooltip info
			for type in td_types:			
				sub_tooltip1 += "  %+d = %d + %d + %d + %d  (%s)\n" % (td_totals_by_type[type][index], td_base, racial_td[type], td_stat_per_type[type], td_effects_per_type[type], type)
			
			for type in td_types:		
				sub_tooltip2 += td_tooltips_per_type[type]		
			
			tooltip = "".join( [tooltip,
						sub_tooltip1,
						sub_tooltip2])
						
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		ymin = 5000
		ymax = 0
		for type in td_types:
			ymin = min(ymin, td_totals_by_type[type][0])
			ymax = max(ymax, td_totals_by_type[type][0])
			ymin = min(ymin, td_totals_by_type[type][-1])
			ymax = max(ymax, td_totals_by_type[type][-1])
			self.graph_information.graph_data_lists.append(td_totals_by_type[type])
		self.graph_information.graph_yaxis_min = ymin - 5	
		self.graph_information.graph_yaxis_max = ymax + 5		

		# Setup the Legend
		self.graph_information.graph_num_lines = 4
		self.graph_information.graph_legend_columns = 4
		self.graph_information.graph_legend_labels.append("Elemental TD")
		self.graph_information.graph_legend_styles.append("r^-")
		self.graph_information.graph_legend_labels.append("Mental TD")
		self.graph_information.graph_legend_styles.append("g*-")
		self.graph_information.graph_legend_labels.append("Spiritual TD")
		self.graph_information.graph_legend_styles.append("mD-")
		self.graph_information.graph_legend_labels.append("Sorcerer TD")
		self.graph_information.graph_legend_styles.append("cH-")			
	

	# This method is used to calculate the character's roundtime and action penalties caused by armor from level 0-100
	# or across postcap training. Armor Use is the only skill required for this calculation, no stats are needed, and
	# the only effects that matter are Action Penalty effects such as Armored Evasion.
	def Formula_Armor_Use(self):
		effects_list = ["Skill_Bonus_Armor_Use", "Skill_Ranks_Armor_Use", "Action_Penalty"]
		skill_names = ["Armor Use"]

		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}
		base_bonus_arr = {}		
		AP_value = 0
		RT_value = 0
		action_penalty_totals = []
		roundtime_penalty_totals = []		
			
		armor_gear = self.Get_Gear_By_Order(self.gear_armor.get())	
		
		roundtime_penalty = 				int(armor_gear.gear_traits["roundtime"])
		roundtime_penalty_negative = 		-1 * roundtime_penalty
		action_penalty = 					int(armor_gear.gear_traits["action_penalty"])
		max_action_penalty =				action_penalty + roundtime_penalty_negative
		
		action_penalty_skill_needed = 		roundtime_penalty * 20
		roundtime_penalty_skill_needed = 	max(0, action_penalty_skill_needed - 10)
		
		armor_overtrain_ranks = 			int(armor_gear.gear_traits["roundtime_train_off_ranks"])
		armor_AG =							int(armor_gear.gear_traits["AG"])
			
			
		AP_base_tooltip = "%s max AP penalty of %s.\n%s ranks (%s bonus) reduces penalty to base %s\n" % (("%+d" % (max_action_penalty)).rjust(4), armor_gear.name.get(), ("%d" % (armor_overtrain_ranks)).rjust(12), roundtime_penalty_skill_needed, action_penalty)
		RT_base_tooltip = "%s base RT penalty of %s.\n%s ranks (%s bonus) reduces penalty to 0\n" % (("%+d" % (roundtime_penalty_negative)).rjust(4), armor_gear.name.get(), ("%d" % (armor_overtrain_ranks)).rjust(12), roundtime_penalty_skill_needed)
			
			
		override_options = self.Find_Overrides_By_Tags(effects_list)

		if "Armor Group" in override_options:
			calculations.override_dict["Armor Group"] = armor_AG


		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)		
		loop_range = self.Set_Graph_Labels(skill_names, "Action and roundtime penalties", "Penalties")	


		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			stat_enh_bonus = 0
			effects_total = 0
			stat_enhancive_totals = {}
			stat_tooltip_arr = {}
			skill_tooltip_arr = {}
			effects_tooltip_text = ""
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Action and roundtime penalties\n" % (i)		
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Action and roundtime penalties\n" % ("{:,}".format(i))
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
					
					
			# Calculate Armor Use ranks
			armor_inc_ranks, temp_tooltip = self.Combine_Effects(i, "Armor Use", base_ranks_arr["Armor Use"], 
											[lists_of_effects_by_tag["Skill_Bonus_Armor_Use"], lists_of_effects_by_tag["Skill_Ranks_Armor_Use"]], 
											["Skill_Bonus_Armor_Use", "Skill_Ranks_Armor_Use"], 
											"skill_bonus_to_ranks")
											
			armor_ranks_total = base_ranks_arr["Armor Use"] + min(50, armor_inc_ranks)	
			armor_ranks_tooltip = "      %s  Armor Use ranks\n" % (("%+d" % armor_ranks_total).rjust(4))
			armor_ranks_tooltip += "           %s  Armor Use base ranks\n" % (("%+d" % base_ranks_arr["Armor Use"]).rjust(4))
			armor_ranks_tooltip += temp_tooltip
			
			
			# Calculate Armor Use bonus
			armor_inc_bonus, temp_tooltip = self.Combine_Effects(i, "Armor Use", base_bonus_arr["Armor Use"], 
											[lists_of_effects_by_tag["Skill_Bonus_Armor_Use"], lists_of_effects_by_tag["Skill_Ranks_Armor_Use"]], 
											["Skill_Bonus_Armor_Use", "Skill_Ranks_Armor_Use"], 
											"skill_ranks_to_bonus")

			armor_bonus_total = base_bonus_arr["Armor Use"] + min(50, armor_inc_bonus)	
			armor_skill_tooltip = "      %s  bonus from %s Armor Use base ranks\n" % (("%+d" % base_bonus_arr["Armor Use"]).rjust(4), base_ranks_arr["Armor Use"])	+ temp_tooltip
		
		
			# Calculate Action Penalty effects
			armor_hindrance, armor_hindrance_tooltip = self.Combine_Effects(i, "Action_Penalty", 0, [lists_of_effects_by_tag["Action_Penalty"]], ["Action_Penalty",], "effect_display_2")	
			if armor_hindrance != 0:
				armor_hindrance_tooltip = "%s bonus from Action Penalty effects\n" % (("%+d" % armor_hindrance).rjust(4)) + armor_hindrance_tooltip
			
			
			# Main Calculation section
			
			# The formula to reduce the action penalty is 1 per 20 Armor Use bonus
			AP_reduction =  math.floor(armor_bonus_total / 20)			
			AP_base = min(action_penalty, max_action_penalty + AP_reduction)		
			
			# If they have more than 50 ranks over the base amount of ranks needed, there is an additional reduction to the action penalty
			armor_overtrain = (armor_AG - 1) * math.floor((armor_ranks_total - armor_overtrain_ranks) / 50) 			
			AP_value = min(0, AP_base + armor_overtrain + armor_hindrance)				
		
			# The formula to reduce the roundtime penalty is 1 per 20 Armor Use bonus
			RT_reduction =  math.floor(armor_bonus_total / 20)
			RT_value = min(0, (roundtime_penalty_negative + RT_reduction))
			
			# If they are at -1, check again using the true formula. Same as above but with a +10 bonus to their armor use bonus
			if RT_value == -1:
				RT_reduction =  math.floor((armor_bonus_total + 10) / 20)
				RT_value = min(0, (roundtime_penalty_negative + RT_reduction))
				
				
			action_penalty_totals.append(AP_value)
			roundtime_penalty_totals.append(RT_value)
			
			# Create Tooltip info
			action_penalty_tooltip = "".join([ 
						"--Action Penalty--\n",
						"%s calculated with:\n" % AP_value,
						AP_base_tooltip,
						"%s from Armor Use (%s - %s) / 20.  %+d vs max %+d\n" % (("%+d" % min(AP_reduction, roundtime_penalty)).rjust(4), action_penalty_skill_needed, armor_bonus_total, AP_reduction, roundtime_penalty),
						armor_skill_tooltip,
						"%s from Armor Use overtraining (%s - %s) / 50\n" % (("%+d" % armor_overtrain).rjust(4), armor_ranks_total, armor_overtrain_ranks),
						armor_ranks_tooltip,
						armor_hindrance_tooltip
						])
						
			roundtime_tooltip = "".join([ 
						"--Roundtime Penalty--\n",
						"%s calculated with:\n" % RT_value,
						RT_base_tooltip,
						"%s from Armor Use (%s - %s) / 20.  %+d vs max %+d\n" % (("%+d" % min(RT_reduction, roundtime_penalty)).rjust(4), roundtime_penalty_skill_needed, armor_bonus_total, RT_reduction, roundtime_penalty),
						armor_skill_tooltip,
						])
			
			
			tooltip = "".join([ tooltip,
						"%s  Action Penalty\n" % AP_value,
						"%s  Roundtime Penalty\n" % RT_value,
						action_penalty_tooltip,
						roundtime_tooltip,
						])
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(action_penalty_totals)
		self.graph_information.graph_data_lists.append(roundtime_penalty_totals)					
					

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = min(action_penalty_totals[0], roundtime_penalty_totals[0]) - 3
		self.graph_information.graph_yaxis_max = max(action_penalty_totals[-1], roundtime_penalty_totals[-1]) + 3		
		

		# Setup the Legend
		self.graph_information.graph_num_lines = 2
		self.graph_information.graph_legend_columns = 2
		self.graph_information.graph_legend_labels.append("Action Penalty")
		self.graph_information.graph_legend_labels.append("Roundtime Penalty")
		self.graph_information.graph_legend_styles.append("bo-")	
		self.graph_information.graph_legend_styles.append("r^-")	

		
	# This method is used to calculate the character's spell hindrance caused by armor from level 0-100 or across postcap 
	# training. Due to the large amount of spell circles, only a small subset of each are shown at a time.
	def Formula_Spell_Hindrance(self, spell_circles):
		effects_list = ["Skill_Bonus_Armor_Use", "Skill_Ranks_Armor_Use", "Spell_Hindrance_All", "Spell_Hindrance_Spiritual"]
		skill_names = ["Armor Use"]

		index = 0
		base_ranks_arr = {}
		base_bonus_arr = {}		
									
		spell_circle_keys = {}
		armor_circle_hindrance = {}
		hindrance_totals = {}	
		armor = self.Get_Gear_By_Order(self.gear_armor.get())
		armor_max_hindrance = int(armor.gear_traits["max_spell_hindrance"])	
		
		for circle in spell_circles:
			hindrance_totals[circle] = []
			spell_circle_keys[circle] = circle.lower().replace(" ", "_")
			armor_circle_hindrance[circle] = int(armor.gear_traits["%s_spell_hindrance" % spell_circle_keys[circle]])		

		override_options = self.Find_Overrides_By_Tags(effects_list)
		
		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)		
		loop_range = self.Set_Graph_Labels(skill_names, "Spell Hindrance by spell circle", "Spell Hindrance %")	


		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			effects_total = 0
			ce_total = 0
			ce_tooltip = ""
			armor_tooltip = ""
			effects_tooltip_text = ""
			header_tooltip = ""
			circle_tooltips = {}
			required_bonus = {}
			circle_hindrance = {}
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Spell Hindrance by spell circle\n" % (i)					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
										
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Spell Hindrance by spell circle\n" % ("{:,}".format(i))		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
					
						
			# Calculate Armor Use bonus
			armor_skill_bonus, temp_tooltip = self.Combine_Effects(i, "Armor Use", base_ranks_arr["Armor Use"], 
											[lists_of_effects_by_tag["Skill_Bonus_Armor_Use"], lists_of_effects_by_tag["Skill_Ranks_Armor_Use"]], 
											["Skill_Bonus_Armor_Use", "Skill_Ranks_Armor_Use"], 
											"skill_ranks_to_bonus")

			armor_skill_total = base_bonus_arr["Armor Use"] + armor_skill_bonus		
			armor_tooltip = "  %s  Armor Use bonus calculated from\n" % (("%d" % (armor_skill_total)).rjust(4)) 		
			armor_tooltip += "       %s  Armor Use base ranks\n" % (("%+d" % base_ranks_arr["Armor Use"]).rjust(4)) 				
			armor_tooltip += temp_tooltip				

										
			# Main Calculation section
			for circle in spell_circles:		
				# Calculate Spell Hindrance effect values	
				if "Armor Base Hindrance" in override_options:		
					calculations.override_dict["Armor Base Hindrance"] = armor_circle_hindrance[circle]				
					
				effects_total, effects_tooltip_text = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["Spell_Hindrance_All"]], ["Spell_Hindrance_All"], "effect_display")
				if circle == "Minor Spiritual" or circle == "Major Spiritual" or circle == "Cleric" or circle == "Empath" or circle == "Paladin" or circle == "Ranger":
					ce_total, ce_tooltip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["Spell_Hindrance_Spiritual"]], ["Spell_Hindrance_Spiritual"], "effect_display")
					effects_total += ce_total
					effects_tooltip_text += ce_tooltip
				
				if effects_tooltip_text != "":
					effects_tooltip_text = "%s  Bonus from Spell Hindrance effects\n" % (("%+d" % effects_total).rjust(4)) + effects_tooltip_text			
			
			
				required_bonus[circle] = max(0, ((20 * armor_circle_hindrance[circle]) - 10))
				circle_hindrance[circle] = max(0, armor_circle_hindrance[circle] * (1 + max(0, math.floor((required_bonus[circle] - armor_skill_total) / 20))) - effects_total)
				hindrance_totals[circle].append(min(circle_hindrance[circle], armor_max_hindrance))		
				
				header_tooltip += "  %s%%  %s\n" % (("%d" % hindrance_totals[circle][-1]).rjust(4), circle)				
				circle_tooltips[circle] = "".join([
											"--%s spell hindrance--\n" % (circle),
											"%s%%  = %s * (1 + (%s - %s) / 20) - %s.  %s vs max %s \n" % (hindrance_totals[circle][-1], armor_circle_hindrance[circle], required_bonus[circle], armor_skill_total, effects_total, circle_hindrance[circle], armor_max_hindrance),
											"  %s  %s min spell hindrance\n" % (("%d" % armor_circle_hindrance[circle]).rjust(4), armor.name.get()),
											"  %s  %s max spell hindrance\n" % (("%d" % armor_max_hindrance).rjust(4), armor.name.get()),
											"  %s  Armor Use bonus for min spell hindrance\n" % (("%d" % required_bonus[circle]).rjust(4)),
											armor_tooltip,
											effects_tooltip_text,
											])
			
	
			# Create Tooltip info
			tooltip = "".join([ 
						tooltip,
						header_tooltip,
						])			
			for circle in spell_circles:
				tooltip += circle_tooltips[circle]
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		for circle in spell_circles:
			self.graph_information.graph_data_lists.append(hindrance_totals[circle])	
			self.graph_information.graph_legend_labels.append(circle)							

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = 0
		self.graph_information.graph_yaxis_max = 100				

		# Setup the Legend
		self.graph_information.graph_num_lines = len(spell_circles)
		self.graph_information.graph_legend_columns = len(spell_circles)
		legend_styles = ["r^-", "g*-", "mD-"]
		for style in legend_styles:
			self.graph_information.graph_legend_styles.append(style)		

		
	# This method is used to calculate the character's Force on Force enemy offset, Open Mstrike targets, and Focused 
	# Mstrike swings from level 0-100 or across postcap training.
	# All Multi Opponent Combat related abilities are calculated at the same time.
	def Formula_Multi_Opponent_Combat(self):
		effects_list = ["Skill_Bonus_Multi_Opponent_Combat", "Skill_Ranks_Multi_Opponent_Combat", "Force_On_Force"]
		skill_names = ["Multi Opponent Combat"]
		fof_totals = []
		open_mstrike_totals = []
		focused_mstrike_totals = []
		fof_tiers = [10, 25, 45, 70]
		open_mstrike_tiers = [5, 15, 35, 60, 100, 155]
		focused_mstrike_tiers = [30, 55, 90, 135, 190]
		
		index = 0
		base_ranks_arr = {}
					
		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		loop_range = self.Set_Graph_Labels(skill_names, "Foes Ignored, Targets, and Swings", "Values")		


		# Begin the big loop to calculate all the data	
		for i in loop_range:
			fof_total = 0
			fof_moc = 0
			open_mstrike_total = 0
			focused_mstrike_total = 0
			fof_tooltip = ""
			fof_effects_tooltip_text = ""
			open_mstrike_tooltip = ""
			focused_mstrike_tooltip = ""
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Multi Opponent Combat\n" % (i)
					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Multi Opponent Combat\n" % ("{:,}".format(i))		
		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					

			# Calculate Combat Maneuver ranks
			skill_rank_count, skill_tooltip = self.Combine_Effects(i, "Multi Opponent Combat", base_ranks_arr["Multi Opponent Combat"], 
											[lists_of_effects_by_tag["Skill_Bonus_Multi_Opponent_Combat"], lists_of_effects_by_tag["Skill_Ranks_Multi_Opponent_Combat"]], 
											["Skill_Bonus_Multi_Opponent_Combat", "Skill_Ranks_Multi_Opponent_Combat"], 
											"skill_bonus_to_ranks")

			moc_total = base_ranks_arr["Multi Opponent Combat"] + min(50, skill_rank_count)	

			
			# Force of Force calculations
			
			# Calculate FoF effects
			fof_count, fof_tooltip = self.Combine_Effects(i, "", 0, 
											[lists_of_effects_by_tag["Force_On_Force"]], 
											["Force_On_Force"], 
											"effect_display")		
			
			if fof_tooltip != "":
				fof_tooltip = "".join( ["  %s  bonus from Force on Force effects\n" % (("%+d" % fof_count).rjust(4)), fof_tooltip] )
											
			# Main FoF calculation								
			if moc_total >= fof_tiers[-1]:
				fof_moc = 4 + math.floor((moc_total - 70) / 25) 
			else:
				for tier in fof_tiers:
					if moc_total >= tier:
						fof_moc += 1		
			
			fof_total = fof_moc + fof_count
			
			fof_tooltip = "".join(	["--Force on Force--\n%s  Foes ignored (beyond the first) calculated with:\n" % fof_total,
							"  %s  from Multi Opponent Combat ranks (%s)\n" % (("%+d" % fof_total).rjust(4), fof_moc),
							"       %s  Multi Opponent Combat base ranks\n" % (("%+d" % base_ranks_arr["Multi Opponent Combat"]).rjust(4)),
							skill_tooltip,
							fof_tooltip]	)				
			
			
			# Open Mstrike calculations
			for tier in open_mstrike_tiers:
				if moc_total >= tier:
					open_mstrike_total += 1
								
			if open_mstrike_total > 0:
				open_mstrike_total += 1
					
			open_mstrike_tooltip = "".join(	["--Open Mstrike--\n  %s  max targets calculated with:\n" % open_mstrike_total,
							"  %s  from Multi Opponent Combat ranks (%s)\n" % (("%+d" % open_mstrike_total).rjust(4), moc_total),
							"       %s  Multi Opponent Combat base ranks\n" % (("%+d" % base_ranks_arr["Multi Opponent Combat"]).rjust(4)),
							skill_tooltip]	)				
			
			
			# Focused Mstrike calculations
			for tier in focused_mstrike_tiers:
				if moc_total >= tier:
					focused_mstrike_total += 1
			
			if focused_mstrike_total > 0:
				focused_mstrike_total += 1
				
			focused_mstrike_tooltip = "".join(	["--Focused Mstrike--\n  %s  max swings calculated with:\n" % focused_mstrike_total,
							"  %s  from Multi Opponent Combat ranks (%s)\n" % (("%+d" % focused_mstrike_total).rjust(4), moc_total),
							"       %s  Multi Opponent Combat base ranks\n" % (("%+d" % base_ranks_arr["Multi Opponent Combat"]).rjust(4)),
							skill_tooltip]	)		
			
			
			
			fof_totals.append(fof_total)
			open_mstrike_totals.append(open_mstrike_total)
			focused_mstrike_totals.append(focused_mstrike_total)
			
			
			# Create Tooltip info
			tooltip = "".join( [tooltip,
							"%s  Foes ignored beyond first  (Force on Force)\n" % ("%s" % fof_total).rjust(4),
							"%s  Max targets  (Open Mstrike)\n" % ("%s" % open_mstrike_total).rjust(4),
							"%s  Max swings  (Focused Mstrike)\n" % ("%s" % focused_mstrike_total).rjust(4),
							fof_tooltip,
							open_mstrike_tooltip,
							focused_mstrike_tooltip] )
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		


		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(fof_totals)
		self.graph_information.graph_data_lists.append(open_mstrike_totals)		
		self.graph_information.graph_data_lists.append(focused_mstrike_totals)					
					

		# Set the minimum height for the graph
		ymax = max(fof_totals[-1], open_mstrike_totals[-1], focused_mstrike_totals[-1])		
		self.graph_information.graph_yaxis_min = -1
		self.graph_information.graph_yaxis_max = ymax + 1			

		# Setup the Legend
		self.graph_information.graph_num_lines = 3
		self.graph_information.graph_legend_columns = 3
		self.graph_information.graph_legend_labels.append("Force on Force")
		self.graph_information.graph_legend_styles.append("bo-")	
		self.graph_information.graph_legend_labels.append("Open Mstrike")
		self.graph_information.graph_legend_styles.append("mD-")	
		self.graph_information.graph_legend_labels.append("Focused Mstrike")
		self.graph_information.graph_legend_styles.append("r^-")	


	# This method is used to calculate the character's CS bonus, maximum readable/useable spell, general spell duration
	# when using Arcane Symbols and Magic Item Use items from level 0-100 or across postcap training
	def Formula_AS_MIU(self, choice):		
		if choice == "Arcane Symbols":
			effects_list = ["Skill_Ranks_Arcane_Symbols", "Skill_Bonus_Arcane_Symbols"]
			skill_names = ["Arcane Symbols"]
			
		else:
			effects_list = ["Skill_Ranks_Magic_Item_Use", "Skill_Bonus_Magic_Item_Use"]
			skill_names = ["Magic Item Use"]

		index = 0
		base_ranks_arr = {}
		base_bonus_arr = {}					
		
		cs_bonus = 0
		max_spell = 0
		duration = 0
		
		cs_bonus_totals = []
		max_spell_totals = []
		duration_totals = []
		
		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)		
		loop_range = self.Set_Graph_Labels(skill_names, "%s - CS, Spell Level, Duration" % (choice), "")


		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			effects_total = 0
			effects_tooltip_text = ""
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: %s CS, Spell Level, Duration\n" % (i, choice)					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: %s - CS, Spell Level, Duration\n" % ("{:,}".format(i), choice)		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
					
				
			# Calculate Arcane Symbols / Magic Item Use ranks 			
			skill_ranks, temp_tooltip = self.Combine_Effects(i, choice, base_ranks_arr[choice], 
											[lists_of_effects_by_tag[effects_list[1]], lists_of_effects_by_tag[effects_list[0]]], 
											[effects_list[1], effects_list[0]], 
											"skill_bonus_to_ranks")

			skill_ranks_total = base_ranks_arr[choice] + min(50, skill_ranks)	
			skill_ranks_tooltip = "".join([ "  %s  %s ranks\n" % (("%d" % skill_ranks_total).rjust(4), choice),
								"       %s  %s base ranks\n" % (("%+d" % base_ranks_arr[choice]).rjust(4), choice),
								temp_tooltip
								])				
											
			# Calculate Arcane Symbols / Magic Item Use skill bonus
			skill_bonus, temp_tooltip = self.Combine_Effects(i, choice, base_ranks_arr[choice], 
											[lists_of_effects_by_tag[effects_list[1]], lists_of_effects_by_tag[effects_list[0]]], 
											[effects_list[1], effects_list[0]], 
											"skill_ranks_to_bonus")
											
			skill_bonus_total = base_bonus_arr[choice] + min(50, skill_bonus)				
			skill_bonus_tooltip = "".join([ "  %s  %s skill bonus\n" % (("%d" % skill_bonus_total).rjust(4), choice),
								"       %s bonus from %s %s base ranks\n" % (("%+d" % base_bonus_arr[choice]).rjust(4), base_ranks_arr[choice], choice),
								temp_tooltip
								])	
																		
			
			# Main Calculation section

			# Find max readable/useable spell level
			if skill_bonus_total >= 170:
				max_spell = 50
				spell_level_tooltip = "50 = (%s >= 170 skill bonus)\n" % skill_bonus_total
			elif skill_bonus_total >= 115:
				max_spell = 20 + (5 * math.floor((skill_bonus_total - 100) / 15))
				spell_level_tooltip = "%s = 20 + (5 * (%s - 100) / 15)\n" % (max_spell, skill_bonus_total)
			else:
				max_spell = math.floor(skill_bonus_total / 5)
				spell_level_tooltip = "%s = %s / 5\n" % ("%s" % max_spell, skill_bonus_total)
			
			# Calculate the duration of beneficial spells
			duration = 10 + (skill_ranks_total * 0.5)

			# Find CS bonus
			if i > 100:
				level = 101
			else:
				level = i+1				

			cs_bonus = 0.0
			cs_level = 0
			cs_level2 = 0
			cs_level3 = 0
			double_level = level * 2
			ranks = skill_ranks_total

			while ranks > 0:							
				if ranks <= level:
					cs_bonus += 0.75
					cs_level += 1
				elif ranks <= double_level:
					cs_bonus += 0.5
					cs_level2 += 1
				else:
					cs_bonus += 0.33		
					cs_level3 += 1						
					
				ranks -= 1						
			cs_bonus = math.ceil(cs_bonus)	
			
			cs_tooltip = "%s = (0.75 * %s) + (0.5 * %s) + (0.33 * %s)\n" % ("%+d" % cs_bonus, cs_level, cs_level2, cs_level3)
			
			
			max_spell_totals.append(max_spell)
			duration_totals.append(duration)
			cs_bonus_totals.append(cs_bonus)
			
			# Create Tooltip info
			max_spell_tooltip = "".join([ 
						"--Max Readable/Useable Level--\n",
						spell_level_tooltip,
						skill_bonus_tooltip,
						])
			durations_tooltip = "".join([ 
						"--Spell Duration (in minutes)--\n",
						"%s = 10 + (0.5 * %s)\n" % (duration, skill_ranks_total),
						skill_ranks_tooltip,
						])
			cs_bonus_tooltip = "".join([ 
						"--Bonus Casting Strength--\n",
						cs_tooltip,
						skill_ranks_tooltip,
						])
			tooltip = "".join([ tooltip,
						"%s     Max readable/useable spell level\n" % ("%s" % max_spell).rjust(4),
						"%s  General spell duration in minutes\n" % ("%s" % duration).rjust(6),
						"%s     Bonus CS from scrolls/magic items\n" % ("%s" % cs_bonus).rjust(4),
						max_spell_tooltip,
						durations_tooltip,
						cs_bonus_tooltip,
						])
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(cs_bonus_totals)
		self.graph_information.graph_data_lists.append(max_spell_totals)	
		self.graph_information.graph_data_lists.append(duration_totals)						
					

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = -1
		self.graph_information.graph_yaxis_max = max(cs_bonus_totals[-1], max_spell_totals[-1], duration_totals[-1]) + 5		
		

		# Setup the Legend
		self.graph_information.graph_num_lines = 3
		self.graph_information.graph_legend_columns = 3
		self.graph_information.graph_legend_labels.append("CS Bonus")
		self.graph_information.graph_legend_styles.append("ro-")		
		self.graph_information.graph_legend_labels.append("Max Spell Level")
		self.graph_information.graph_legend_styles.append("bs-")			
		self.graph_information.graph_legend_labels.append("General Duration")
		self.graph_information.graph_legend_styles.append("g^-")				
				
		
	# This method is used to calculate how many uses of Mana Spellup are useable per day and how many seconds from a 
	# pulse that Mana Pulse can be invoked from level 0-100 or across postcap training. Mana control is the primary
	# skill for this method but the exact type will vary by profession.
	def Formula_Mana_Control(self):
		effects_list = []
		skill_names = []

		index = 0
		base_ranks_arr = {}			
		pulse_totals = []
		spellup_totals = []		
								
		profession = globals.character.profession.name
		
		# Determine	which mana controls to use 
		if profession == "Cleric" or profession == "Paladin" or profession == "Ranger":
			effects_list = ["Skill_Bonus_Spiritual_Mana_Control", "Skill_Ranks_Spiritual_Mana_Control"]
			skill_names = ["Spiritual Mana Control"]
		elif profession == "Rogue" or profession == "Sorcerer" or profession == "Warrior":
			effects_list = ["Skill_Bonus_Elemental_Mana_Control", "Skill_Ranks_Elemental_Mana_Control", "Skill_Bonus_Spiritual_Mana_Control", "Skill_Ranks_Spiritual_Mana_Control"]
			skill_names = ["Elemental Mana Control", "Spiritual Mana Control"]
		elif profession == "Empath" or profession == "Monk":
			effects_list = ["Skill_Bonus_Mental_Mana_Control", "Skill_Ranks_Mental_Mana_Control", "Skill_Bonus_Spiritual_Mana_Control", "Skill_Ranks_Spiritual_Mana_Control"]
			skill_names = ["Mental Mana Control", "Spiritual Mana Control"]
		elif profession == "Bard":
			effects_list = ["Skill_Bonus_Elemental_Mana_Control", "Skill_Ranks_Elemental_Mana_Control", "Skill_Bonus_Mental_Mana_Control", "Skill_Ranks_Mental_Mana_Control"]
			skill_names = ["Elemental Mana Control", "Mental Mana Control"]
		elif profession == "Wizard":
			effects_list = ["Skill_Bonus_Elemental_Mana_Control", "Skill_Ranks_Elemental_Mana_Control"]
			skill_names = ["Elemental Mana Control"]
		elif profession == "Savant":
			effects_list = ["Skill_Bonus_Mental_Mana_Control", "Skill_Ranks_Mental_Mana_Control"]
			skill_names = ["Mental Mana Control"]			


		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		loop_range = self.Set_Graph_Labels(skill_names, "Mana Pulse & Spellup", "Seconds / Uses")			
					
			
		# Begin the big loop to calculate all the data	
		for i in loop_range:
			highest_name = ""
			highest_value = -1
			ce_tooltip = ""	
			stat_enhancive_totals = {}
			skill_ranks_arr = {}
			skill_tooltip_arr = {}
			pulse_tootip = ""
			spellup_tootip = ""
			pulse_value = 0
			spellup_value = 0
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Mana Control - Mana Pulse & Spellup\n" % (i)					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Mana Control - Mana Pulse & Spellup\n" % ("{:,}".format(i))		
		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					
				
			# Calculate all Mana Control ranks
			for skill in skill_names:				
				tagname = skill.replace(" ", "_")
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, skill, base_ranks_arr[skill], 
												[lists_of_effects_by_tag["Skill_Bonus_%s" % tagname], lists_of_effects_by_tag["Skill_Ranks_%s" % tagname]], 
												["Skill_Bonus_%s" % tagname, "Skill_Ranks_%s" % tagname], 
												"skill_bonus_to_ranks")

				skill_ranks_arr[skill] = base_ranks_arr[skill] + min(50, skill_rank_count)			
				skill_tooltip_arr[skill] = temp_tooltip
				
				if skill_ranks_arr[skill] > highest_value:
					highest_name = skill
					highest_value = skill_ranks_arr[skill]

			
			
			# Main Calculation section
			for skill in skill_names:			
				if skill == highest_name:					
					pulse_value += skill_ranks_arr[skill]
					spellup_value += skill_ranks_arr[skill]
					pulse_tootip += "".join([
								"    %s  %s ranks\n" % (("%+d" % skill_ranks_arr[skill] ).rjust(4), skill),
								"       %s  %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(4), skill),
								skill_tooltip_arr[skill]
								])
					spellup_tootip += "".join([
								"    %s  %s ranks\n" % (("%+d" % skill_ranks_arr[skill] ).rjust(4), skill),
								"       %s  %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(4), skill),
								skill_tooltip_arr[skill]
								])					
				else:
					pulse_value += math.floor(skill_ranks_arr[skill] / 2)
					spellup_value += math.floor(skill_ranks_arr[skill] / 2)
					pulse_tootip += "".join([
								"    %s  %s ranks (%s / 2)\n" % (("%+d" % math.floor(skill_ranks_arr[skill] / 2)).rjust(4), skill, skill_ranks_arr[skill]),
								"       %s  %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(4), skill),
								skill_tooltip_arr[skill]		
								])
					spellup_tootip += "".join([
								"    %s  %s ranks (%s / 2)\n" % (("%+d" % math.floor(skill_ranks_arr[skill] / 2)).rjust(4), skill, skill_ranks_arr[skill]),
								"       %s  %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(4), skill),
								skill_tooltip_arr[skill]		
								])								
					
			
			
			# Create Tooltip info
			pulse_tootip = "".join([ 
							"--Mana Pulse--\n",
							"%s  Seconds calculated with:\n" % pulse_value,
							"%s  Mana Control ranks\n" % (("%s" % pulse_value).rjust(4)),
							pulse_tootip
							])		
				
			spellup_tootip = "".join([ 
							"--Mana Spellup--\n",
							"%s  Uses per day calculated with:\n" % math.floor(spellup_value / 25),
							"%s  from Mana Control ranks (%s / 25)\n" % (("%s" % math.floor(spellup_value / 25)).rjust(4), spellup_value),
							spellup_tootip
							])										
							
			tooltip = "".join([ 
							tooltip,
							"%s  Seconds mana pulse may be invoked\n" % ("%s" % pulse_value).rjust(4),
							"%s  Mana spellup\n" % ("%s" % math.floor(spellup_value / 25)).rjust(4),
							pulse_tootip,
							spellup_tootip
							])

			pulse_totals.append(pulse_value)
			spellup_totals.append(math.floor(spellup_value / 25))
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(pulse_totals)
		self.graph_information.graph_data_lists.append(spellup_totals)								

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = min(pulse_totals[0], spellup_totals[0]) - 5
		self.graph_information.graph_yaxis_max = max(pulse_totals[-1], spellup_totals[-1]) + 5				

		# Setup the Legend
		self.graph_information.graph_num_lines = 2
		self.graph_information.graph_legend_columns = 2
		self.graph_information.graph_legend_labels.append("Mana Pulse Seconds")
		self.graph_information.graph_legend_styles.append("bs-")		
		self.graph_information.graph_legend_labels.append("Mana Spellup Uses")
		self.graph_information.graph_legend_styles.append("y^-")			
		

	# This method is used to calculate how effective the character lore ranks are in regards to bonuses to certain effects,
	# which are usually spells, from level 0-100 or across postcap training.
	# The actual plotting is the least important part of this method and instead a very length tooltip is generated and
	# details all the bonues (summation or otherwise) the character's current lore ranks have earned.
	# A call to the SQL database for summations of the relavant lore are stored in Summation objects. These objects 
	# simplify the tooltip creation process.
	def Formula_Summation_Bonuses(self, skill_names, mode):
		effects_list = []
		lore_totals = {}
		
		number_of_skills = len(skill_names)
		
		for skill in skill_names:
			lore_effect = skill.replace(",", "").replace(" ", "_")			
			effects_list.append("Skill_Bonus_%s" % lore_effect)
			effects_list.append("Skill_Ranks_%s" % lore_effect)
			lore_totals[skill] = []		
			
		character_spell_circles = globals.character.profession.spell_circles
		summation_spell_circles = []
		summation_list = []
		
		index = 0
		base_ranks_arr = {}
		base_bonus_arr = {}	
		
		
		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		
		if mode:
			label = "%s, Multiple - Summations" % (skill_names[0].split(",")[0])
			where = ""
			for skill in skill_names:
				where += "lore_skill LIKE '%%%s%%' OR " % skill
			query = "SELECT * FROM Summations WHERE lore_skill LIKE '%%|%%' AND (%s)" % where[:-4]
		else:
			label = "%s - Summations" % (skill_names[0])
			query = "SELECT * FROM Summations WHERE lore_skill='%s'" % skill_names[0]
		
		
		loop_range = self.Set_Graph_Labels(skill_names, label, "Ranks")						


		globals.db_cur.execute(query)
		globals.db_con.commit()		
		data = globals.db_cur.fetchall()	
		for lore_summation in data:
			summation_list.append(Summation(lore_summation, character_spell_circles))

		
		# Begin the big loop to calculate all the data	
		for i in loop_range:		
			useable_ranks = {}
			summation_tooltip_arr = []
			lore_ranks_totals = {}
			lore_tooltips = {}
			
			summation_tooltip = ""		
			current_spell_circle = ""
			current_effect_name = ""
			
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: %s\n" % (i, label)					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: %s\n" % ("{:,}".format(i), label)		
		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
					
	
			for skill in skill_names:
				lore_effect = skill.replace(",", "").replace(" ", "_")	
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, skill, base_ranks_arr[skill], 
												[lists_of_effects_by_tag["Skill_Bonus_%s" % lore_effect], lists_of_effects_by_tag["Skill_Ranks_%s" % lore_effect]], 
												["Skill_Bonus_%s" % lore_effect, "Skill_Ranks_%s" % lore_effect], 
												"skill_bonus_to_ranks")
		
				lore_ranks_totals[skill] = base_ranks_arr[skill] + min(50, skill_rank_count)		
				skill_tootip = "".join( [ 
#									"  %s  %s ranks\n" % (("%d" % lore_ranks_totals[skill] ).rjust(4), skill),
									"       %s  %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(4), skill),
									temp_tooltip
									])						
				lore_tooltips[skill] = skill_tootip
						
				lore_totals[skill].append(lore_ranks_totals[skill])		
					
			for summation in summation_list:			
				for skill in skill_names:
					useable_ranks[skill] = math.floor(lore_ranks_totals[skill] / summation.circle_divisor)		
				info = summation.Get_Summation_Info_String(skill_names, useable_ranks)	
				
				if info == "":
					continue
				
				
				# Add spell circle header	
				if current_spell_circle != summation.category:
					current_spell_circle = summation.category
					if summation.circle_divisor == 3:
						circle_message = "--%s  (non-native profession spell circle)--\n" % current_spell_circle
					elif summation.circle_divisor == 2:
						circle_message = "--%s  (non-native major spell circle)--\n" % current_spell_circle
					elif summation.circle_divisor == 1:
						circle_message = "--%s--\n" % current_spell_circle
					
					useable_ranks_tooltip = ""
					if number_of_skills == 1:
						useable_ranks_tooltip = "%s %s ranks = %s / %s\n" % (useable_ranks[skill_names[0]], skill_names[0], lore_ranks_totals[skill_names[0]], summation.circle_divisor)
					else:
						for skill in skill_names:
							useable_ranks_tooltip += "%s %s ranks = %s / %s\n" % (useable_ranks[skill], skill, lore_ranks_totals[skill], summation.circle_divisor)
				
					summation_tooltip_arr.append("%s%s" % (circle_message, useable_ranks_tooltip))				
				
				# Add effect name header	
				if current_effect_name != summation.effect_name:
					summation_tooltip_arr.append("%s\n" % summation.effect_name)
					current_effect_name = summation.effect_name
				
				summation_tooltip_arr.append(info)					
					
			if len(summation_tooltip_arr) == 0:
				summation_tooltip = "\nInsufficent lore ranks to gain any summation bonuses\n"
			else:
				summation_tooltip = "".join(summation_tooltip_arr)

			# Create Tooltip info		
			header_tooltips = "".join(["%s  %s ranks\n%s" % (("%s" % lore_ranks_totals[lore]).rjust(4), lore, lore_tooltips[lore]) for lore in skill_names])
			tooltip = "".join([ 
					tooltip,
					header_tooltips,
#					"--Lore Rank Totals--\n",
#					"".join(lore_tooltips),
					summation_tooltip,
					])		
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Setup the Legend
		self.graph_information.graph_num_lines = len(skill_names)
		if len(skill_names) > 2:
			self.graph_information.graph_legend_columns = 2			
		else:
			self.graph_information.graph_legend_columns = len(skill_names)
			
		i = 0
		highest_lore = 0
		legend_styles = ["rs-", "bo-", "y^-", "g*-", "mD-"]
		
		for skill in skill_names:			
			if highest_lore < lore_totals[skill][-1]:
				highest_lore = lore_totals[skill][-1]
				
			# Append the completed lists to graph_infomation object
			self.graph_information.graph_data_lists.append(lore_totals[skill])		
			self.graph_information.graph_legend_labels.append(skill)
			self.graph_information.graph_legend_styles.append(legend_styles[i])		
			i += 1			
		
		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = 0
		self.graph_information.graph_yaxis_max = highest_lore + 1	
		
						
	# This method is used to calculate the duration of the character's bandages and roundtime reduction when eating herbs
	# from level 0-100 or across postcap training.
	def Formula_First_Aid(self):
		effects_list = ["Skill_Bonus_First_Aid", "Skill_Ranks_First_Aid", "Skill_Phantom_Ranks_First_Aid"]
		skill_names = ["First Aid"]

		index = 0
		base_ranks_arr = {}
		base_bonus_arr = {}			
		bandage_totals = []
		herb_totals = []					

		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		loop_range = self.Set_Graph_Labels(skill_names, "Bandage Duration & Herb Roundtime", "Duration / Roundtime")						
			
		# Begin the big loop to calculate all the data	
		for i in loop_range:			
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: First Aid - Bandage Duration & Herb Roundtime\n" % (i)					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: First Aid - Bandage Duration & Herb Roundtime\n" % ("{:,}".format(i))		
		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
					
				
			# Calculate First Aid ranks
			skill_rank_count, temp_tooltip = self.Combine_Effects(i, "First Aid", base_ranks_arr["First Aid"], 
											[lists_of_effects_by_tag["Skill_Bonus_First_Aid"], lists_of_effects_by_tag["Skill_Ranks_First_Aid"], lists_of_effects_by_tag["Skill_Phantom_Ranks_First_Aid"]], 
											["Skill_Bonus_First_Aid", "Skill_Ranks_First_Aid", "Skill_Phantom_Ranks_First_Aid"], 
											"skill_bonus_to_ranks")

			fa_ranks_total = base_ranks_arr["First Aid"] + min(50, skill_rank_count)			
			fa_ranks_tootip = temp_tooltip
			
			
			# Calculate First Aid bonus							
			skill_bonus_count, temp_tooltip = self.Combine_Effects(i, "First Aid", base_ranks_arr["First Aid"], 
											[lists_of_effects_by_tag["Skill_Bonus_First_Aid"], lists_of_effects_by_tag["Skill_Ranks_First_Aid"], lists_of_effects_by_tag["Skill_Phantom_Ranks_First_Aid"]], 
											["Skill_Bonus_First_Aid", "Skill_Ranks_First_Aid", "Skill_Phantom_Ranks_First_Aid"], 
											"skill_ranks_to_bonus")

			fa_bonus_total = base_bonus_arr["First Aid"] + min(50, skill_bonus_count)		
			fa_bonus_tootip = temp_tooltip		
			
			
			# Set the bandage duration and herb roundtime values
			bandage_value = math.floor(fa_ranks_total / 10)
			herb_value = -1 * math.floor(fa_bonus_total / 20)	
			
			bandage_totals.append(bandage_value)
			herb_totals.append(herb_value)
			
			
			# Create Tooltip info
			fa_ranks_tootip = "".join([ 
							"--Bandage Duration--\n",
							"%s  Offensive actions calculated with:\n" % bandage_value,
							"  %s  from First Aid ranks (%s / 10)\n" % (("%+d" %bandage_value ).rjust(4), fa_ranks_total),
							"       %s  First Aid base ranks\n" % (("%+d" % base_ranks_arr["First Aid"]).rjust(4)),
							fa_ranks_tootip
							])		
				
			fa_bonus_tootip = "".join([ 
							"--Herb Roundtime Reduction--\n",
							"%s  Roundtime reduction calculated with:\n" % herb_value,
							"  %s  from First Aid bonus (%s / 20)\n" % (("%+d" % herb_value).rjust(4), fa_bonus_total),
							"       %s  bonus from %s First Aid base ranks\n" % (("%+d" % base_bonus_arr["First Aid"]).rjust(4), base_ranks_arr["First Aid"]),
							fa_bonus_tootip
							])										
							
			tooltip = "".join([ 
							tooltip,
							"%s  Offensive actions per bandage application\n" % ("%s" % bandage_value).rjust(5),
							"%s  Roundtime reduction when using herbs\n" % ("%+d" % herb_value).rjust(4),
							fa_ranks_tootip,
							fa_bonus_tootip
							])
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(bandage_totals)
		self.graph_information.graph_data_lists.append(herb_totals)							

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = herb_totals[-1] - 1
		self.graph_information.graph_yaxis_max = bandage_totals[-1] + 1		

		# Setup the Legend
		self.graph_information.graph_num_lines = 2
		self.graph_information.graph_legend_columns = 2
		self.graph_information.graph_legend_labels.append("Bandage Duration")
		self.graph_information.graph_legend_styles.append("rs-")		
		self.graph_information.graph_legend_labels.append("Herb Roundtime Reduction")
		self.graph_information.graph_legend_styles.append("g^-")	


	# This method is used to calculate the character's Trading Skill Boost from level 0-100 or across postcap training.
	# This number is meant to be used as a percent. IE Skill Boost 13 = 13% (base * 1.13) bonus when selling or discount
	# when buying items.
	def Formula_Trading(self):
		effects_list = ["Statistic_Influence", "Statistic_Bonus_Influence", "Skill_Bonus_Trading", "Skill_Ranks_Trading"]
		skill_names = ["Trading"]
		statistic_names = ["Influence"]

		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}
		base_bonus_arr = {}
			
		boost_totals = []		
			
		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		loop_range = self.Set_Graph_Labels(skill_names, "Trading - Skill Boost", "Skill Boost")		
					
			
		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			ce_tooltip = ""					
			ce_total = 0
			stat_enh_bonus = 0
			effects_total = 0
			stat_tooltip_text = ""
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Trading - Skill Boost\n" % i
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()	
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Trading - Skill Boost\n" % ("{:,}".format(i))
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[100].get()	
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
					


			# Calculate Influence bonus
			stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, "Influence", 0, 
											[lists_of_effects_by_tag["Statistic_Bonus_Influence"], lists_of_effects_by_tag["Statistic_Influence"]], 
											["Statistic_Bonus_Influence", "Statistic_Influence"], 
											"stat_inc_to_bonus")	
												
			stat_total = math.floor(base_stat_arr["Influence"] + min(50, stat_enh_bonus))
			stat_tootip = "".join( [ "  %s  Influence bonus\n" % (("%+d" % stat_total).rjust(4)),
									"       %s  %s base bonus\n" % (("%+d" % base_stat_arr["Influence"]).rjust(4), stat),
									temp_tooltip
									])			
			
					
			# Calculate Trading bonus							
			skill_bonus_count, temp_tooltip = self.Combine_Effects(i, "Trading", base_ranks_arr["Trading"], 
											[lists_of_effects_by_tag["Skill_Bonus_Trading"], lists_of_effects_by_tag["Skill_Ranks_Trading"]], 
											["Skill_Bonus_Trading", "Skill_Ranks_Trading"], 
											"skill_ranks_to_bonus")

			skill_total = base_bonus_arr["Trading"] + min(50, skill_bonus_count)		
			skill_tootip = "".join( [ "  %s  Trading skill bonus\n" % (("%+d" % skill_total).rjust(4)),
									"       %s  bonus from %s Trading base ranks\n" % (("%+d" % base_bonus_arr["Trading"]).rjust(4), base_ranks_arr["Trading"]),
									temp_tooltip
									])			

			
			# The skill boost is limited by the number of ranks in Trading the character has. 
			skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Trading", base_ranks_arr["Trading"], 
											[lists_of_effects_by_tag["Skill_Bonus_Trading"], lists_of_effects_by_tag["Skill_Ranks_Trading"]], 
											["Skill_Bonus_Trading", "Skill_Ranks_Trading"], 
											"skill_bonus_to_ranks")
			boost_limit = base_ranks_arr["Trading"] + min(50, skill_rank_count)	
			
			
			# Calculate the skill boost
			boost_value = min(skill_total, math.floor((stat_total + skill_total) / 12))			
			boost_totals.append(boost_value)
			
			
			# Create Tooltip info			
			tooltip = "".join([ 
							tooltip,
							"%s  Skill boost\n" % ("%s" % boost_value).rjust(5),
							"--Skill Boost--\n",
							"%s  calculated with:\n" % boost_value,
							"%s  from truc((%s + %s) / 12) = %s vs max %s\n" % (("%d" % boost_value).rjust(4), skill_total, stat_total, math.floor((stat_total + skill_total) / 12), boost_limit),
							stat_tootip,
							skill_tootip,
							])
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object	

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(boost_totals)						

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = boost_totals[0] - 5
		self.graph_information.graph_yaxis_max = boost_totals[-1] + 5		

		# Setup the Legend
		self.graph_information.graph_num_lines = 1
		self.graph_information.graph_legend_columns = 1
		self.graph_information.graph_legend_labels.append("Skill Boost")
		self.graph_information.graph_legend_styles.append("g^-")	


	# This method is used to calculate the character's maximum unencumbered carrying capacity and over encumbered weight
	# intervals from level 0-100 or across postcap training.
	def Formula_Encumbrance(self):
		effects_list = ["Statistic_Strength", "Statistic_Bonus_Strength", "Encumbrance_Reduction_Percent", "Encumbrance_Reduction_Absolute"]
		statistic_names = ["Strength", "Constitution"]
		skill_names = []
		
		race = globals.character.race.name
		race_enc_factor = float(globals.character.race.encumbrance_factor)
		armor = self.Get_Gear_By_Order(self.gear_armor.get())	
		armor_name = armor.name.get()
		armor_base_weight = int(armor.gear_traits["base_weight"])
		armor_weight = int(armor.weight)
		armor_AG =	int(armor.gear_traits["AG"])
		armor_bonus = int((armor_base_weight - armor_weight) * race_enc_factor)
		weight_factor = float(globals.character.race.weight_factor)
		base_weight = int(100 * weight_factor) 
		

		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}
		base_bonus_arr = {}					
			
		carry_weight = 0	
		carry_totals = []		
		
					
		override_options = self.Find_Overrides_By_Tags(effects_list)

		if "Armor Group" in override_options:
			calculations.override_dict["Armor Group"] = armor_AG

		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)		
		loop_range = self.Set_Graph_Labels(skill_names, "Encumbrance", "Weight (lb)")	


		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			stat_enh_bonus = 0
			effects_total = 0
			stat_enhancive_totals = {}
			stat_tooltip_arr = {}
			effects_tooltip_text = ""
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Unencumbered Carry Capacity\n" % (i)
				for stat in statistic_names:				
					#base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()						
					base_stat_arr[stat] = int(globals.character.statistics_list[stat].values_by_level[i].get())
					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Unencumbered Carry Capacity\n" % ("{:,}".format(i))
				for stat in statistic_names:									
					base_stat_arr[stat] = int(globals.character.statistics_list[stat].values_by_level[100].get())				
		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
					

			# Calculate Statistic bonus	
			str_enhancive, temp_tooltip = self.Combine_Effects(i, "Strength", 0, 
											[lists_of_effects_by_tag["Statistic_Bonus_Strength"], lists_of_effects_by_tag["Statistic_Strength"]], 
											["Statistic_Bonus_Strength", "Statistic_Strength"], 
											"stat_bonus_to_inc")													

			str_enhancive_total = int(base_stat_arr["Strength"] + min(50, str_enhancive))
			strength_tooltip = "       %s  Strength base statistic\n" % (("%+d" % base_stat_arr["Strength"]).rjust(4)) + temp_tooltip	
			strength_tooltip = "  %s  Strength statistic\n" % (("%d" % (str_enhancive_total)).rjust(4)) + strength_tooltip					
			
			
			# Calculate Encumbrance Effects values		
			percent_effects_total, percent_effects_tooltip = self.Combine_Effects(i, "", 0, 
											[lists_of_effects_by_tag["Encumbrance_Reduction_Percent"]], 
											["Encumbrance_Reduction_Percent"], 
											"effect_display")			

			if percent_effects_tooltip != "":
					percent_effects_tooltip = "  %s%%  bonus from Encumbrance Percent Reduction effects\n" % (("%+d" % percent_effects_total).rjust(4)) + percent_effects_tooltip		

			absolute_effects_total, absolute_effects_tooltip = self.Combine_Effects(i, "", 0, 
											[lists_of_effects_by_tag["Encumbrance_Reduction_Absolute"]], 
											["Encumbrance_Reduction_Absolute"], 
											"effect_display")		

			if absolute_effects_tooltip != "":
					absolute_effects_tooltip = "  %s  bonus from Encumbrance Absolute Reduction effects\n" % (("%+d" % absolute_effects_total).rjust(4)) + absolute_effects_tooltip
			
			
			# Main Calculation section
			str_stat = base_stat_arr["Strength"]
			con_stat = base_stat_arr["Constitution"]
			if str_stat % 2 == 1:
				str_tooltip = "(%s - 1)" % str_stat
				str_stat -= 1
			else:
				str_tooltip = "%s" % str_stat
				
			if con_stat % 2 == 1:
				con_tooltip = "(%s - 1)" % con_stat
				con_stat -= 1
			else:
				con_tooltip = "%s" % con_stat
			
			body_weight = base_weight + math.floor((str_stat + con_stat) * weight_factor)
			carry_weight = round(((str_enhancive_total - 20) / 200), 2) 
			carry_weight = (carry_weight + effects_total) * body_weight 
			carry_weight = carry_weight + round((body_weight / 200), 2)
			carry_weight = round((carry_weight + armor_bonus + absolute_effects_total), 2)
			
			encumbrance_inc = round((body_weight / 100), 2)
			
			carry_totals.append(carry_weight)
			
			# Create Tooltip info
			body_weight_tooltip = "".join([
						"  %s  Body weight.  (%s + (%.2f * (%s + %s))) \n" % (("%d" % body_weight).rjust(4), base_weight, weight_factor, base_stat_arr["Strength"], base_stat_arr["Constitution"]),
						"        %s  %s base weight\n" % (("%d" % (base_weight)).rjust(4), race),
						"        %s  %s weight factor\n" % (("%.2f" % (weight_factor)).rjust(4), race),
						"        %s  Strength statistic\n" % ("%d" % (base_stat_arr["Strength"])).rjust(4),
						"        %s  Constitution statistic\n" % ("%d" % (base_stat_arr["Constitution"])).rjust(4),
						])
						
			armor_bonus_tooltip = "".join([
						"  %s  %s weight bonus.  ((%s - %s) * %.2f)\n" % (("%+d" % armor_bonus).rjust(4), armor_name, armor_base_weight, armor_weight, race_enc_factor),
						"        %s  base weight\n" % (("%d" % (armor_base_weight)).rjust(4)),
						"        %s  actual weight\n" % (("%d" % (armor_weight)).rjust(4)),						
						])			
						
			carry_tooltip = "".join([
						"--Carry Capacity--\n",
						"%s lb = (((%s - 20) / 200) + %s) * %s + (%s / 200) + %s + %s\n" % (carry_weight, str_enhancive_total, percent_effects_total, body_weight, body_weight, absolute_effects_total, armor_bonus),
						strength_tooltip,
						body_weight_tooltip,
						percent_effects_tooltip,
						absolute_effects_tooltip,
						armor_bonus_tooltip,
						])
			
			inc_tooltip = "".join([
						"--Over Encumbered Increments--\n",
						"%s lb = %s / 100\n" % (encumbrance_inc, body_weight),
						body_weight_tooltip,
						])
			
			tooltip = "".join([ tooltip,
						"%s lb  Carry Capacity\n" % (("%.2f" % carry_weight).rjust(5)),
						" %s lb  Over Encumbered Increments\n" % (("%.2f" % encumbrance_inc).rjust(4)),
						carry_tooltip,
						inc_tooltip,
						])
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(carry_totals)				
					

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = carry_totals[0] - 5
		self.graph_information.graph_yaxis_max = carry_totals[-1] + 5		
		

		# Setup the Legend
		self.graph_information.graph_num_lines = 1
		self.graph_information.graph_legend_columns = 1
		self.graph_information.graph_legend_labels.append("Carry Weight")
		self.graph_information.graph_legend_styles.append("rs-")		


	# This method is used to calculate the character's imprint success chance and maximum number players
	# that can be imprinted from level 0-100 or across postcap training.
	def Formula_Imprint(self):
		effects_list = [
		"Statistic_Influence", "Statistic_Bonus_Influence", 
		"Skill_Bonus_Spell_Research_Minor_Spiritual", "Skill_Ranks_Spell_Research_Minor_Spiritual", 
		"Skill_Bonus_Spell_Research_Major_Spiritual", "Skill_Ranks_Spell_Research_Major_Spiritual", 
		"Skill_Bonus_Spell_Research_Empath", "Skill_Ranks_Spell_Research_Empath", 
		"Skill_Bonus_Spiritual_Lore_Blessings", "Skill_Ranks_Spiritual_Lore_Blessings", 
		"Skill_Bonus_Mental_Lore_Transference", "Skill_Ranks_Mental_Lore_Transference", 
		"Skill_Bonus_Mental_Lore_Transformation", "Skill_Ranks_Mental_Lore_Transformation",
		"Skill_Bonus_First_Aid", "Skill_Ranks_First_Aid", 
		"Skill_Bonus_Physical_Fitness", "Skill_Ranks_Physical_Fitness"
		]
		statistic_names = ["Influence"]
		skill_names = ["Spiritual Lore, Blessings", "Mental Lore, Transference", "Mental Lore, Transformation", "First Aid", "Physical Fitness",
		"Spell Research, Minor Spiritual", "Spell Research, Major Spiritual", "Spell Research, Empath"]

		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}
		base_bonus_arr = {}					
			
		imprint_totals = []		
		max_totals = []		
		
					
		override_options = self.Find_Overrides_By_Tags(effects_list)

		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)		
		loop_range = self.Set_Graph_Labels(skill_names, "Imprint Chance & Max", "Percent %")	


		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			stat_enh_bonus = 0
			effects_total = 0
			stat_enhancive_totals = {}
			values_dict = {}
			tooltip_dict = {}
			stat_tooltip_arr = {}
			effects_tooltip_text = ""
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Imprint Chance & Max\n" % (i)
				for stat in statistic_names:									
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()	
					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Imprint Chance & Max\n" % ("{:,}".format(i))
				for stat in statistic_names:									
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[100].get()				
		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
					

			# Calculate Statistic bonus	
			inf_enhancive, temp_tooltip = self.Combine_Effects(i, "Influence", 0, 
											[lists_of_effects_by_tag["Statistic_Bonus_Influence"], lists_of_effects_by_tag["Statistic_Influence"]], 
											["Statistic_Bonus_Influence", "Statistic_Influence"], 
											"stat_inc_to_bonus")													
			inf_enhancive_total = int(base_stat_arr["Influence"] + min(50, inf_enhancive))
			influence_tooltip = "".join( [ "  %s  Influence bonus\n" % (("%+d" % inf_enhancive_total).rjust(8)),
									"       %s  Influence base bonus\n" % (("%+d" % base_stat_arr["Influence"]).rjust(8)),
									temp_tooltip
									])						
			

			# Calculate skill ranks and bonus
			for skill in skill_names:
				tagname = skill.replace(" ", "_").replace(",", "")
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, skill, base_ranks_arr[skill], 
												[lists_of_effects_by_tag["Skill_Bonus_%s" % tagname], lists_of_effects_by_tag["Skill_Ranks_%s" % tagname]], 
												["Skill_Bonus_%s" % tagname, "Skill_Ranks_%s" % tagname], 
												"skill_bonus_to_ranks")
				values_dict[skill] = base_ranks_arr[skill] + skill_rank_count	
				tooltip_dict[skill] = "".join( [ "  %s  %s ranks\n" % (("%+d" % values_dict[skill]).rjust(8), skill),
										"       %s  %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(8), skill),
										temp_tooltip
										])		
			
			
			# Main Calculation section
			level = i + 1
			level_0_5 = math.floor(0.5 * level)
			level_1_5 = math.floor(1.5 * level)
			level_2 = 2 * level
			level_3_5 = math.floor(3.5 * level)
			level_4 = 4 * level
			level_6 = 6 * level
			influence_bonus = max(0, 2 * inf_enhancive_total)
			sr_minor = min(level, values_dict["Spell Research, Minor Spiritual"])
			sr_major = min(level, values_dict["Spell Research, Major Spiritual"])
			sr_empath = min(level, values_dict["Spell Research, Empath"])
			lore_bless = min(level_4, values_dict["Spiritual Lore, Blessings"])
			lore_transfer = min(level_4, values_dict["Mental Lore, Transference"])
			lore_transform = min(level_4, values_dict["Mental Lore, Transformation"])
			skill_fa = min(level_6, values_dict["First Aid"])
			skill_pf = min(level_6, values_dict["Physical Fitness"])
			
			spell_research_ranks = max(0, (300 * math.floor(((sr_minor + sr_major + sr_empath) - level_1_5) / level_1_5)))
			lore_ranks = max(0, math.floor((200 * ((lore_bless + lore_transfer + lore_transform) - level_0_5)) / level_3_5))
			skill_ranks = max(0, math.floor((150 * ((skill_fa + skill_pf) - level_2)) / level_4))
			
			imprint_chance = math.floor((100 + influence_bonus + spell_research_ranks + lore_ranks + skill_ranks) / 10)
			max_imprints = 1 + math.floor(values_dict["Mental Lore, Transference"] / 40)
			
			imprint_totals.append(imprint_chance)
			max_totals.append(max_imprints)
			
			# Create Tooltip info			
			max_tooltip = "".join([
						"--Maximum number of Imprints--\n",
						"%s = 1 + (%s / 40)\n" % (max_imprints, values_dict["Mental Lore, Transference"]),
						tooltip_dict["Mental Lore, Transference"],				
						])			
			
			chance_tooltip = "".join([
						"--Imprint Chance--\n",
						"%s%% = (100 + %s + %s + %s + %s) / 10.  min 0\n" % (imprint_chance, influence_bonus, spell_research_ranks, lore_ranks, skill_ranks),	
						"%s  Statistic bonus.  (2 * %s).  min 0\n" % (("%d" % influence_bonus).rjust(4), inf_enhancive_total),
						influence_tooltip,
						"%s  Spell Research bonus.  (300 * (%s + %s + %s - (%s)) / (%s).  min 0\n" % (("%d" % spell_research_ranks).rjust(4), sr_minor, sr_major, sr_empath, level_1_5, level_1_5),	
						tooltip_dict["Spell Research, Minor Spiritual"],
						tooltip_dict["Spell Research, Major Spiritual"],
						tooltip_dict["Spell Research, Empath"],
						"%s  Lore bonus.  (200 * (%s + %s + %s - (%s)) / (%s).  min 0\n" % (("%d" % lore_ranks).rjust(4), lore_bless, lore_transfer, lore_transform, level_0_5, level_3_5),	
						tooltip_dict["Spiritual Lore, Blessings"],
						tooltip_dict["Mental Lore, Transference"],
						tooltip_dict["Mental Lore, Transformation"],
						"%s  Skill bonus.  (150 * (%s + %s - (%s)) / (%s).  min 0\n" % (("%d" % skill_ranks).rjust(4), skill_fa, skill_pf, level_2, level_4),	
						tooltip_dict["First Aid"],
						tooltip_dict["Physical Fitness"],
						])
			
			tooltip = "".join([ 
				tooltip,
				"  %s%%  Chance to imprint non-empath player\n" % imprint_chance,
				"  %s  Maximum number of imprints\n" % max_imprints,
				chance_tooltip,
				max_tooltip,
				])
			
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = 0
		self.graph_information.graph_yaxis_max = 100		
		

		# Setup the Legend
		self.graph_information.graph_num_lines = 2
		self.graph_information.graph_legend_columns = 2
		self.graph_information.graph_data_lists.append(imprint_totals)		
		self.graph_information.graph_legend_labels.append("Imprint Chance")
		self.graph_information.graph_legend_styles.append("ro-")		
		self.graph_information.graph_data_lists.append(max_totals)	
		self.graph_information.graph_legend_labels.append("Max Imprints")
		self.graph_information.graph_legend_styles.append("bo-")		
		
		
	# This method is used to calculate the character's redux percentage, redux points from physical skills, and spell penalty
	# from level 0-100 or across postcap training.
	# Special thanks goes to Brute and his redux.lic script. Without them, I wouldn't have been about to add this calculation.
	def Formula_Redux(self):
		effects_list = []		
		primary_skills_names = ["Physical Fitness"]
		secondary_skills_names = [
						"Ambush", "Armor Use", "Combat Maneuvers", "Dodging",
						"Multi Opponent Combat", "Shield Use", "Two Weapon Combat"						
						]
		tertiary_skills_names = [
						"Edged Weapons", "Blunt Weapons", "Two-Handed Weapons",
						"Ranged Weapons", "Thrown Weapons", "Polearm Weapons", "Brawling"	
						]
		spell_skills_names = [											
						"Spell Research, Minor Spiritual", "Spell Research, Major Spiritual", "Spell Research, Cleric", 
						"Spell Research, Minor Elemental", "Spell Research, Major Elemental", "Spell Research, Ranger", 
						"Spell Research, Sorcerer", "Spell Research, Wizard", "Spell Research, Savant", 
						"Spell Research, Minor Mental", "Spell Research, Major Mental", "Spell Research, Paladin"			
						]
		skill_names = primary_skills_names + secondary_skills_names + tertiary_skills_names + spell_skills_names

		index = 0
		base_ranks_arr = {}
		base_bonus_arr = {}		
			
		redux_points = 0
		redux_totals = []
		

		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)		
		loop_range = self.Set_Graph_Labels(skill_names, "Redux", "Redux %")	


		# Begin the big loop to calculate all the data	
		for i in loop_range:
			primary_ranks = 0
			secondary_ranks = 0
			tertiary_ranks = 0	
			primary_points = 0
			secondary_points = 0
			tertiary_points = 0
			spell_ranks = 0
			primary_tooltip = ""
			secondary_tooltip = ""
			tertiary_tooltip = ""
			spell_tooltip = ""
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Redux\n" % (i)
					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Redux\n" % ("{:,}".format(i))			
		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					
				
			# Calculate redux points
			for skill in primary_skills_names:
				primary_ranks += base_ranks_arr[skill]
				if base_ranks_arr[skill] > 0:
					primary_tooltip += "%s  %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(10), skill)				
				
			for skill in secondary_skills_names:
				secondary_ranks += base_ranks_arr[skill]
				if base_ranks_arr[skill] > 0:
					secondary_tooltip += "%s  %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(10), skill)				
				
			for skill in tertiary_skills_names:
				tertiary_ranks += base_ranks_arr[skill]
				if base_ranks_arr[skill] > 0:
					tertiary_tooltip += "%s  %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(10), skill)
					
			for skill in spell_skills_names:
				spell_ranks += base_ranks_arr[skill]
				if base_ranks_arr[skill] > 0:
					spell_tooltip += "%s  %s ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(10), skill)

			
			
			# Main Calculation section
			#Redux Factor = (Redux Points - T) / ((2*Redux Points)-X+Y) - spell penalty
			
			# Get level
			if i > 100:
				level = 100
			elif i == 0:
				level = 1
			else:
				level = i	
				
			primary_points = primary_ranks * 10
			secondary_points = secondary_ranks * 4
			tertiary_points =  tertiary_ranks * 3
			redux_points = primary_points + secondary_points + tertiary_points
			t = 1060 + (2000 / level)
			x = 4472 / level
			y = (60 * math.sqrt(redux_points)) - 3600
			
			if y <= 0:
				y = 0
				raw_redux_percent = 0
				redux_percent = 0
			elif level <= spell_ranks * 2:
				spell_ranks = 1000000
				raw_redux_percent = 0
				redux_percent = 0
			else:
				raw_redux_percent = max(0, ((redux_points - t) / ((2 * redux_points) - (x + y))) - (spell_ranks * 0.00135))
				redux_percent = round(100 * raw_redux_percent, 2)

				
			redux_totals.append(redux_percent)
			
			# Create Tooltip info
			percent_tooltip = "".join([
						"--Redux Percent--\n",
						"%.2f (%f) = ((%s - %.2f) / (2 * %s)) - (%.2f + %.2f) - (%s * 0.00135)\n" % (redux_percent, raw_redux_percent, redux_points, t, redux_points, x, y, spell_ranks),
						"%s  Redux points\n" % ("%d" % redux_points).rjust(6),
						"%s  (1060 + (2000 / %s))\n" % (("%d" % t).rjust(6), level),
						"%s  (4472 / %s)\n" % (("%d" % x).rjust(6), level),
						"%s  ((60 * sqrt(%s)) - 3600)\n" % (("%d" % y).rjust(6), redux_points),
						"%s  Total spell ranks\n" % ("%d" % spell_ranks).rjust(6),
						spell_tooltip
						])
			points_tooltip = "".join([
						"--Redux Points--\n",
						"%s = %s + %s + %s\n" % (redux_points, primary_points, secondary_points, tertiary_points),
						"%s  Primary points. (%s * 10)\n" % (("%d" % primary_points).rjust(6), primary_ranks),
						primary_tooltip,
						"%s  Secondary points. (%s * 4)\n" % (("%d" % secondary_points).rjust(6), secondary_ranks),
						secondary_tooltip,
						"%s  Tertiary points. (%s * 3)\n" % (("%d" % tertiary_points).rjust(6), tertiary_ranks),
						tertiary_tooltip,			
						])
			
			tooltip = "".join([ tooltip,
						"  %.2f  Redux Percentage\n" % redux_percent,
						"  %s  Redux Points\n" % redux_points,
						percent_tooltip,
						points_tooltip,
						])
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(redux_totals)				
					

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = -1
		self.graph_information.graph_yaxis_max = 100
		

		# Setup the Legend
		self.graph_information.graph_num_lines = 1
		self.graph_information.graph_legend_columns = 1
		self.graph_information.graph_legend_labels.append("Redux")
		self.graph_information.graph_legend_styles.append("r^-")		

		
	# This method is used to calculate the character's maximum value and recovery for Health, Mana, Stamina and Spriit 
	# from level 0-100 or across postcap training.
	def Formula_Resources(self):
		effects_list = ["Statistic_Strength", "Statistic_Bonus_Strength", "Statistic_Constitution", "Statistic_Bonus_Constitution", "Statistic_Agility", "Statistic_Bonus_Agility", "Statistic_Discipline", "Statistic_Bonus_Discipline", "Statistic_Aura", "Statistic_Bonus_Aura", 
		"Skill_Bonus_Physical_Fitness", "Skill_Ranks_Physical_Fitness", "Skill_Bonus_Harness_Power", "Skill_Ranks_Harness_Power",
		"Resource_Maximum_Health", "Resource_Maximum_Mana", "Resource_Maximum_Stamina", "Resource_Maximum_Spirit",
		"Resource_Recovery_Health", "Resource_Recovery_Mana", "Resource_Recovery_Stamina", "Resource_Recovery_Spirit",
		"Resource_Recovery_Mana_Normal", "Resource_Recovery_Stamina_Normal",		
		]
		skill_names = ["Physical Fitness", "Harness Power"]
		statistic_names = ["Strength", "Constitution", "Agility", "Discipline", "Aura"]		
		race = globals.character.race.name
		profession = globals.character.profession.name

		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}
		base_bonus_arr = {}
					
		resource_names = ["Health", "Mana", "Stamina", "Spirit"]	
		spirit_value_tiers = [1, 1, 1, 2, 2, 3, 2]
		spirit_minute_tiers = [5, 4, 3, 5, 4, 5, 3]
		health_max_totals = []
		mana_max_totals = []
		stamina_max_totals = []
		spirit_max_totals = []
		health_recovery_totals = []
		mana_recovery_totals = []
		stamina_recovery_totals = []
		spirit_recovery_totals = []
		highest_mc_name = ""
		lowest_mc_name = ""
		need_max_stamina = 0
		
		# Set variables used with maximum health
		str_level0 = int(globals.character.statistics_list["Strength"].values_by_level[0].get())
		con_level0 = int(globals.character.statistics_list["Constitution"].values_by_level[0].get())		
		base_health = math.floor((str_level0 + con_level0) / 10)
		race_health_gain = int(globals.character.race.health_gain_rate)
		race_max_health = int(globals.character.race.max_health)		
		
		# Set variables used with maximum mana
		mana_stat1 = globals.character.profession.mana_statistics[0]
		mana_stat2 = globals.character.profession.mana_statistics[1]		
		stat1_level0 = int(globals.character.statistics_list[mana_stat1].bonuses_by_level[0].get())
		stat2_level0 = int(globals.character.statistics_list[mana_stat2].bonuses_by_level[0].get())	
		
		# Set variables used with resource recovery
		health_regen = globals.character.race.health_regen		
		mana_regen = 15		
		base_spirit_tier = int(globals.character.race.spirit_regen_tier) - 1
		
		# Mana recovery uses the Mana Control ranks of the profession's magic spheres. Add them to the effects list as appropriate
		if profession == "Cleric" or profession == "Paladin" or profession == "Ranger":
			effects_list.extend(("Skill_Bonus_Spiritual_Mana_Control", "Skill_Ranks_Spiritual_Mana_Control"))
			skill_names.append("Spiritual Mana Control")
			highest_mc_name = "Spiritual"
			lowest_mc_name = "Spiritual"
			
		elif profession == "Rogue" or profession == "Sorcerer" or profession == "Warrior":
			effects_list.extend(("Skill_Bonus_Elemental_Mana_Control", "Skill_Ranks_Elemental_Mana_Control", "Skill_Bonus_Spiritual_Mana_Control", "Skill_Ranks_Spiritual_Mana_Control"))
			skill_names.extend(("Elemental Mana Control", "Spiritual Mana Control"))
			highest_mc_name = "Elemental"
			lowest_mc_name = "Spiritual"
			
		elif profession == "Empath" or profession == "Monk":
			effects_list.extend(("Skill_Bonus_Mental_Mana_Control", "Skill_Ranks_Mental_Mana_Control", "Skill_Bonus_Spiritual_Mana_Control", "Skill_Ranks_Spiritual_Mana_Control"))
			skill_names.extend(("Mental Mana Control", "Spiritual Mana Control"))
			highest_mc_name = "Spiritual"
			lowest_mc_name = "Mental"
			
		elif profession == "Bard":
			effects_list.extend(("Skill_Bonus_Elemental_Mana_Control", "Skill_Ranks_Elemental_Mana_Control", "Skill_Bonus_Mental_Mana_Control", "Skill_Ranks_Mental_Mana_Control"))
			skill_names.extend(("Elemental Mana Control", "Mental Mana Control"))
			highest_mc_name = "Elemental"
			lowest_mc_name = "Mental"
			
		elif profession == "Wizard":
			effects_list.extend(("Skill_Bonus_Elemental_Mana_Control", "Skill_Ranks_Elemental_Mana_Control"))
			skill_names.append("Elemental Mana Control")
			highest_mc_name = "Elemental"
			lowest_mc_name = "Elemental"
			
		elif profession == "Savant":
			effects_list.extend(("Skill_Bonus_Mental_Mana_Control", "Skill_Ranks_Mental_Mana_Control"))
			skill_names.append("Mental Mana Control")		
			highest_mc_name = "Mental"	
			lowest_mc_name = "Mental"		

			
		override_options = self.Find_Overrides_By_Tags(effects_list)

		# Set the overrides if needed
		for option in override_options:
			if option == "Node Room":
				mana_regen = 25					
			elif option == "Discipline Bonus":
				if "Discipline" not in statistic_names:
					effects_list.extend(("Statistic_Discipline", "Statistic_Bonus_Discipline"))
					statistic_names.append("Discipline")
			elif option == "Wisdom Bonus":
				if "Wisdom" not in statistic_names:
					effects_list.extend(("Statistic_Wisdom", "Statistic_Bonus_Wisdom"))
					statistic_names.append("Wisdom")
			elif option == "Maximum Stamina":
				need_max_stamina = 1
				
				
		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)	
		loop_range = self.Set_Graph_Labels(skill_names, "Resources - Maximums & Recovery", "Resources")					
			
		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			stat_enh_bonus = 0
			spirit_stat = 0
			temp_name = ""
			
			values_dict = {}
			tooltip_dict = {}				
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Resources - Maximums & Recovery\n" % i
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()	
				
				spirit_stat = int(globals.character.statistics_list["Aura"].values_by_level[i].get())
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Resources - Maximums & Recovery\n" % ("{:,}".format(i))
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[100].get()	
					
				spirit_stat = int(globals.character.statistics_list["Aura"].values_by_level[100].get())
				
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
					


			# Calculate statistic bonuses
			for stat in statistic_names:
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, stat, 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_%s" % stat], lists_of_effects_by_tag["Statistic_%s" % stat]], 
												["Statistic_Bonus_%s" % stat, "Statistic_%s" % stat], 
												"stat_inc_to_bonus")													
				values_dict[stat] = math.floor(base_stat_arr[stat] + stat_enh_bonus)
				tooltip_dict[stat] = "".join( [ "  %s  %s bonus\n" % (("%+d" % values_dict[stat]).rjust(4), stat),
										"       %s  %s base bonus\n" % (("%+d" % base_stat_arr[stat]).rjust(4), stat),
										temp_tooltip
										])			
			
			# Spirit is based of the statistic value, not the bonus. Get the statistic value of Aura.	
			stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, "Aura", 0, 
											[lists_of_effects_by_tag["Statistic_Bonus_Aura"], lists_of_effects_by_tag["Statistic_Aura"]], 
											["Statistic_Bonus_Aura", "Statistic_Aura"], 
											"stat_bonus_to_inc")												
			values_dict["Spriit"] = math.floor(spirit_stat + min(40, stat_enh_bonus))
			tooltip_dict["Spirit"] = "".join( [ "  %s  Aura statistic value\n" % (("%+d" % values_dict["Spriit"]).rjust(4)),
									"       %s  Aura statistic value\n" % (("%+d" % spirit_stat).rjust(4)),
									temp_tooltip
									])			
									
			# Set the override variable if needed
			if "Discipline Bonus" in override_options:
				calculations.override_dict["Discipline Bonus"] = values_dict["Discipline"]
											
			if "Wisdom Bonus" in override_options:												
				calculations.override_dict["Wisdom Bonus"] = values_dict["Wisdom"]			
				
					
			# Calculate skill ranks and bonus
			for skill in skill_names:
				tagname = skill.replace(" ", "_")
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, skill, base_ranks_arr[skill], 
												[lists_of_effects_by_tag["Skill_Bonus_%s" % tagname], lists_of_effects_by_tag["Skill_Ranks_%s" % tagname]], 
												["Skill_Bonus_%s" % tagname, "Skill_Ranks_%s" % tagname], 
												"skill_bonus_to_ranks")
				values_dict[skill] = base_ranks_arr[skill] + skill_rank_count	
				tooltip_dict[skill] = "".join( [ "  %s  %s ranks\n" % (("%+d" % values_dict[skill]).rjust(4), skill),
										"       %s  %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(4), skill),
										temp_tooltip
										])			


			# In addition to needing the ranks, maximum stamina requires the bonus of Physical Fitness as well
			skill_bonus_count, temp_tooltip = self.Combine_Effects(i, "Physical Fitness", base_ranks_arr["Physical Fitness"], 
											[lists_of_effects_by_tag["Skill_Bonus_Physical_Fitness"], lists_of_effects_by_tag["Skill_Ranks_Physical_Fitness"]], 
											["Skill_Bonus_Physical_Fitness", "Skill_Ranks_Physical_Fitness"], 
											"skill_ranks_to_bonus")
			values_dict["Physical Fitness bonus"] = base_bonus_arr["Physical Fitness"] + skill_bonus_count	
			tooltip_dict["Physical Fitness bonus"] = "".join( [ 
									"  %s  Physical Fitness bonus\n" % (("%+d" % values_dict["Physical Fitness bonus"]).rjust(4)),
									temp_tooltip
									])													
			
			
			# Calculate resource maximums
			for resource in resource_names:			
				resource_value, temp_tooltip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["Resource_Maximum_%s" % resource]], ["Resource_Maximum_%s" % resource], 					"effect_display")
				values_dict["Maximum %s" % resource] = min(50, resource_value)
				tooltip_dict["Maximum %s" % resource] = "".join( [ 
											"%+d  Enhancive max %s (%+d vs +50)\n" % (values_dict["Maximum %s" % resource], resource, values_dict["Maximum %s" % resource]),
											temp_tooltip
											])			
											
											
			# "Normal" recovery is like an enhancive bonus that doesn't have an upper limit
			values_dict["Mana Recovery Normal"], temp_tooltip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["Resource_Recovery_Mana_Normal"]], ["Resource_Recovery_Mana_Normal"], "effect_display_2")			
			tooltip_dict["Mana Recovery Normal"] = "".join( [ 
										"%s  Additional Mana recovery\n" % (("%+d" % values_dict["Mana Recovery Normal"]).rjust(6)),
										temp_tooltip
										])	
										
			values_dict["Stamina Recovery Normal"], temp_tooltip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["Resource_Recovery_Stamina_Normal"]], ["Resource_Recovery_Stamina_Normal"], "effect_display_2")			
			tooltip_dict["Stamina Recovery Normal"] = "".join( [ 
										"%s  Additional Stamina recovery\n" % (("%+d" % values_dict["Stamina Recovery Normal"]).rjust(6)),
										temp_tooltip
										])	
										
													
			# Main Calculation section
			
			# Maximum Health
			health_extra = min(50, values_dict["Constitution"] + values_dict["Maximum Health"])
			health_PF = ((race_health_gain + math.floor(values_dict["Constitution"] / 10)) * values_dict["Physical Fitness"])
			health_max = min(base_health + health_PF + values_dict["Maximum Health"],  race_max_health + health_extra)  
							
							
			# Maximum Mana
			base_mana = max(0, math.floor((stat1_level0 + stat2_level0) / 4))
			if values_dict["Harness Power"] > index:
				mana_HP = (3 * index) + (values_dict["Harness Power"] - index)			
			else:
				mana_HP = 3 * values_dict["Harness Power"]				
			mana_max = base_mana + mana_HP + values_dict["Maximum Mana"]
				
				
			# Maximum Stamina
			stamina_max = values_dict["Constitution"] + math.floor((values_dict["Strength"] + values_dict["Agility"] + values_dict["Discipline"]) / 3) + math.floor(values_dict["Physical Fitness bonus"] / 3) + values_dict["Maximum Stamina"]
			if need_max_stamina:				
				calculations.override_dict["Maximum Stamina"] = stamina_max
			
			
			# Maximum Spirit
			spirit_max = math.floor(values_dict["Spriit"] / 10) + round(0.1 + (values_dict["Spriit"] % 10) / 10) + values_dict["Maximum Spirit"]
			
								
			# Calculate resource recoveries
			for resource in resource_names:			
				# Spirit has the maximum enhancive value of +3 instead of +50
				if resource == "Spirit":
					enhancive_max = 3
				else:
					enhancive_max = 50
											
				resource_value, temp_tooltip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["Resource_Recovery_%s" % resource]], ["Resource_Recovery_%s" % resource], 					"effect_display_2")
				values_dict["%s Recovery" % resource] = min(enhancive_max, resource_value)
				tooltip_dict["%s Recovery" % resource] = "".join( [ 
											"%s  Enhancive %s recovery (%+d vs +%s)\n" % (("%+d" % values_dict["%s Recovery" % resource]).rjust(6), resource, values_dict["%s Recovery" % resource], enhancive_max),
											temp_tooltip
											])							
						
			
			# Health Recovery
			health_recovery = health_regen + math.floor(values_dict["Physical Fitness"] / 20) + values_dict["Health Recovery"]
			
						
			# Mana Recovery
			base_mana_recovery = max(1, math.floor(mana_max * (mana_regen / 100)))
			
			# Find the highest mana control value
			if values_dict["%s Mana Control" % lowest_mc_name] > values_dict["%s Mana Control" % highest_mc_name]:
				temp_name = highest_mc_name
				highest_mc_name = lowest_mc_name
				lowest_mc_name = temp_name
				
			higher_mc = values_dict["%s Mana Control" % highest_mc_name]
			lower_mc = values_dict["%s Mana Control" % lowest_mc_name]			
			
			# If the mana control names match, the profession only uses one mana type. Otherwise, they use two types.
			if highest_mc_name == lowest_mc_name:
				mana_recovery = base_mana_recovery + math.floor(higher_mc / 10) + values_dict["Mana Recovery"] + values_dict["Mana Recovery Normal"]
				mana_tooltip = "%s = %s + (%s / 10) + %s + %s\n" % (mana_recovery, base_mana_recovery, higher_mc, values_dict["Mana Recovery"], values_dict["Mana Recovery Normal"])
				mana_tooltip2 = ""
			else:			
				mana_recovery = base_mana_recovery + math.floor(higher_mc / 10) + math.floor(lower_mc / 20) + values_dict["Mana Recovery"] + values_dict["Mana Recovery Normal"]
				mana_tooltip = "%s = %s + (%s / 10) + (%s / 20) + %s + %s\n" % (mana_recovery, base_mana_recovery, higher_mc, lower_mc, values_dict["Mana Recovery"], values_dict["Mana Recovery Normal"])
				mana_tooltip2 = tooltip_dict["%s Mana Control" % lowest_mc_name]
				
			
			# Stamina Recovery
			stamina_percent = 20 + math.floor(values_dict["Constitution"] / 4.5) + values_dict["Stamina Recovery"] + values_dict["Stamina Recovery Normal"]
			stamina_recovery = round(stamina_max  * (stamina_percent / 100))	
			
			
			# Spirit Recovery
			spirit_tier = min(6, base_spirit_tier + values_dict["Spirit Recovery"])
			
			if "Node Room" in override_options:
				spirit_recovery = 2 * spirit_value_tiers[spirit_tier] / spirit_minute_tiers[spirit_tier]
				spirit_recovery = math.floor(100 * spirit_recovery) / 100
				
				spirit_tooltip = "%s = %s per %s minutes (Tier %s).  Recovery tier %s vs max 7\n" % (spirit_recovery, 2 * spirit_value_tiers[spirit_tier], spirit_minute_tiers[spirit_tier], spirit_tier+1, base_spirit_tier + values_dict["Spirit Recovery"] + 1)
				spirit_node_tooltip = "     2x  Spirit recovered while on a node\n"
			else:
				spirit_recovery = round(spirit_value_tiers[spirit_tier] / spirit_minute_tiers[spirit_tier], 2)
				spirit_recovery = math.floor(100 * spirit_recovery) / 100
				
				spirit_tooltip = "%s = %s per %s minutes (Tier %s).  Recovery tier %s vs max 7\n" % (spirit_recovery, spirit_value_tiers[spirit_tier], spirit_minute_tiers[spirit_tier], spirit_tier+1, base_spirit_tier + values_dict["Spirit Recovery"] + 1)
				spirit_node_tooltip = ""			
			
			
			
			# Added the results to the totals array
			health_max_totals.append(health_max)
			mana_max_totals.append(mana_max)
			stamina_max_totals.append(stamina_max)
			spirit_max_totals.append(spirit_max)
			health_recovery_totals.append(health_recovery)
			mana_recovery_totals.append(mana_recovery)
			stamina_recovery_totals.append(stamina_recovery)
			spirit_recovery_totals.append(spirit_recovery)
			
			
			# Create Tooltip info		
			max_health_tooltip = "".join([ 
							"--Maximum Health--\n",
							"%s = (%s + %s + %s) vs max (%s + %s + %s)\n" % (health_max, base_health, health_PF, values_dict["Maximum Health"], race_max_health, values_dict["Constitution"], values_dict["Maximum Health"]),
							"%s  Base health  ((%s + %s) / 10)\n" % (("%d" % base_health).rjust(3), str_level0, con_level0),
							"        %s  Strength statistic at level 0\n" % ("%d" % str_level0).rjust(4),
							"        %s  Constitution statistic at level 0\n" % ("%d" % con_level0).rjust(4),
							"%s  Health from PF ranks ((%s + (%s / 10)) * %s)\n" % (("%d" % health_PF).rjust(3), race_health_gain, values_dict["Constitution"], values_dict["Physical Fitness"]),
							"%s  %s health gained per PF rank\n" % (("%d" % race_health_gain).rjust(7), race),
							tooltip_dict["Constitution"],
							tooltip_dict["Physical Fitness"],
							"%s  %s maximum health\n" % (("%d" % race_max_health).rjust(3), race),
							"%s  Additional maximum health (%s + %s) vs max +50\n" % (("%d" % health_extra).rjust(3), values_dict["Constitution"], values_dict["Maximum Health"]),
							tooltip_dict["Constitution"],
							tooltip_dict["Maximum Health"],
							])
				
			max_mana_tooltip = "".join([ 
							"\n--Maximum Mana--\n",	
							"%s = %s + %s + %s\n" % (mana_max, base_mana, mana_HP, values_dict["Maximum Mana"]),							
							"%s  Base mana  ((%s + %s) / 4) vs min 0\n" % (("%+d" % base_mana).rjust(3), stat1_level0, stat2_level0),
							"        %s  %s statistic at level 0\n" % (("%d" % stat1_level0).rjust(4), mana_stat1),
							"        %s  %s statistic at level 0\n" % (("%d" % stat2_level0).rjust(4), mana_stat2),
							"%s  Mana from Harness Power (3 * %s) + %s\n" % (("%+d" % mana_HP).rjust(3), min(values_dict["Harness Power"], index), max(0, values_dict["Harness Power"] - index)),
							tooltip_dict["Harness Power"],
							tooltip_dict["Maximum Mana"],
							])	
			
			max_stamina_tooltip = "".join([ 
							"\n--Maximum Stamina--\n",
							"%s = %s + (%s + %s + %s) / 3 + %s + %s\n" % (stamina_max, values_dict["Constitution"], values_dict["Strength"], values_dict["Agility"], values_dict["Discipline"], values_dict["Physical Fitness bonus"], values_dict["Maximum Stamina"]),								
							tooltip_dict["Constitution"],
							tooltip_dict["Strength"],
							tooltip_dict["Agility"],
							tooltip_dict["Discipline"],	
							tooltip_dict["Physical Fitness bonus"],	
							tooltip_dict["Maximum Stamina"],							
							])
			
			max_spirit_tooltip = "".join([ 
							"\n--Maximum Spirit--\n",
							"%s = (%s / 10) + %s\n" % (spirit_max, values_dict["Spriit"], values_dict["Maximum Spirit"]),			
							tooltip_dict["Spirit"],
							tooltip_dict["Maximum Spirit"],	
							])
							
			recovery_health_tooltip = "".join([ 
							"\n--Health Recovery--\n",
							"%s = %s + (%s / 20) + %s\n" % (health_recovery, health_regen, values_dict["Physical Fitness"], values_dict["Health Recovery"]),
							"%s  %s base health recovery\n" % (("%+d" % health_regen).rjust(7), race),
							tooltip_dict["Physical Fitness"],	
							tooltip_dict["Health Recovery"],								
							])
			
			recovery_mana_tooltip = "".join([ 
							"\n--Mana Recovery--\n",		
							mana_tooltip,
							tooltip_dict["%s Mana Control" % highest_mc_name],
							mana_tooltip2,
							tooltip_dict["Mana Recovery"],
							tooltip_dict["Mana Recovery Normal"]
							])
			
			recovery_stamina_tooltip = "".join([ 
							"\n--Stamina Recovery--\n",		
							"%s = %s * .%s\n" % (stamina_recovery, stamina_max, stamina_percent),
							" %s%% = 20 + (%s / 4.5) + %d + %s\n" % (stamina_percent, values_dict["Constitution"], values_dict["Stamina Recovery"], values_dict["Stamina Recovery Normal"]),
							tooltip_dict["Constitution"],
							tooltip_dict["Stamina Recovery"],
							tooltip_dict["Stamina Recovery Normal"],
							])
			
			recovery_spirit_tooltip = "".join([ 
							"\n--Spirit Recovery--\n",	
							spirit_tooltip,		
							"%s  %s base tier (%s per %s minutes)\n" % (("%+d" % (base_spirit_tier+1)).rjust(6), race, spirit_value_tiers[base_spirit_tier], spirit_minute_tiers[base_spirit_tier]),
							tooltip_dict["Spirit Recovery"],
							spirit_node_tooltip,
							])
			
			tooltip = "".join([ 
							tooltip,
							"%s  Maximum Health\n" % ("%s" % health_max).rjust(4),
							"%s  Maximum Mana\n" % ("%s" % mana_max).rjust(4),
							"%s  Maximum Stamina\n" % ("%s" % stamina_max).rjust(4),
							"%s  Maximum Spirit\n" % ("%s" % spirit_max).rjust(4),
							"%s  Health Recovery\n" % ("%s" % health_recovery).rjust(4),
							"%s  Mana Recovery\n" % ("%s" % mana_recovery).rjust(4),
							"%s  Stamina Recovery\n" % ("%s" % stamina_recovery).rjust(4),
							"%s  Spirit Recovery\n" % ("%s" % spirit_recovery).rjust(4),
							max_health_tooltip,
							max_mana_tooltip,
							max_stamina_tooltip,
							max_spirit_tooltip,
							recovery_health_tooltip,
							recovery_mana_tooltip,
							recovery_stamina_tooltip,
							recovery_spirit_tooltip,
							])
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(health_max_totals)		
		self.graph_information.graph_data_lists.append(health_recovery_totals)	
		self.graph_information.graph_data_lists.append(mana_max_totals)	
		self.graph_information.graph_data_lists.append(mana_recovery_totals)	
		self.graph_information.graph_data_lists.append(stamina_max_totals)	
		self.graph_information.graph_data_lists.append(stamina_recovery_totals)	
		self.graph_information.graph_data_lists.append(spirit_max_totals)	
		self.graph_information.graph_data_lists.append(spirit_recovery_totals)		
					

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = min(health_max_totals[0], mana_max_totals[0], stamina_max_totals[0], spirit_max_totals[0], health_recovery_totals[0], mana_recovery_totals[0], stamina_recovery_totals[0], spirit_recovery_totals[0]) - 5
		self.graph_information.graph_yaxis_max = max(health_max_totals[-1], mana_max_totals[-1], stamina_max_totals[-1], spirit_max_totals[-1], health_recovery_totals[-1], mana_recovery_totals[-1], stamina_recovery_totals[-1], spirit_recovery_totals[-1]) + 5
		

		# Setup the Legend
		self.graph_information.graph_num_lines = 8
		self.graph_information.graph_legend_columns = 4
		self.graph_information.graph_legend_labels.append("Max Health")
		self.graph_information.graph_legend_styles.append("ro-")			
		self.graph_information.graph_legend_labels.append("Health Regen")
		self.graph_information.graph_legend_styles.append("r^-")			
		self.graph_information.graph_legend_labels.append("Max Mana")
		self.graph_information.graph_legend_styles.append("bo-")			
		self.graph_information.graph_legend_labels.append("Mana Regen")
		self.graph_information.graph_legend_styles.append("b^-")			
		self.graph_information.graph_legend_labels.append("Max Stamina")
		self.graph_information.graph_legend_styles.append("yo-")			
		self.graph_information.graph_legend_labels.append("Stamina Regen")
		self.graph_information.graph_legend_styles.append("y^-")			
		self.graph_information.graph_legend_labels.append("Max Spirit")
		self.graph_information.graph_legend_styles.append("co-")			
		self.graph_information.graph_legend_labels.append("Spirit Regen")
		self.graph_information.graph_legend_styles.append("c^-")			

		
	# This method is used to calculate the character's wearable mana in regards to the Spellburst mechanics from level
	# 0-100 or across postcap training. It also calculates how much worn mana the character has based on the spell
	# effects they are using. Spell Research ranks are taken into consideration when determining worn mana.
	def Formula_Spellburst(self):
		effects_list = ["Skill_Ranks_Arcane_Symbols", "Skill_Ranks_Magic_Item_Use", "Skill_Ranks_Harness_Power", "Skill_Ranks_Spell_Aiming",
						"Skill_Ranks_Elemental_Mana_Control", "Skill_Ranks_Mental_Mana_Control", "Skill_Ranks_Spiritual_Mana_Control",
						"Skill_Ranks_Elemental_Lore_Air", "Skill_Ranks_Elemental_Lore_Earth", "Skill_Ranks_Elemental_Lore_Fire", "Skill_Ranks_Elemental_Lore_Water",
						"Skill_Ranks_Spiritual_Lore_Blessings", "Skill_Ranks_Spiritual_Lore_Summoning", "Skill_Ranks_Spiritual_Lore_Religion",
						"Skill_Ranks_Mental_Lore_Divination", "Skill_Ranks_Mental_Lore_Manipulation", "Skill_Ranks_Mental_Lore_Telepathy", "Skill_Ranks_Mental_Lore_Transference", "Skill_Ranks_Mental_Lore_Transformation",
						"Skill_Ranks_Sorcerous_Lore_Demonology", "Skill_Ranks_Sorcerous_Lore_Necromancy", "Skill_Ranks_Spell_Research_Minor_Spiritual", 
						"Skill_Bonus_Arcane_Symbols", "Skill_Bonus_Magic_Item_Use", "Skill_Bonus_Harness_Power", "Skill_Bonus_Spell_Aiming",
						"Skill_Bonus_Elemental_Mana_Control", "Skill_Bonus_Mental_Mana_Control", "Skill_Bonus_Spiritual_Mana_Control",
						"Skill_Bonus_Elemental_Lore_Air", "Skill_Bonus_Elemental_Lore_Earth", "Skill_Bonus_Elemental_Lore_Fire", "Skill_Bonus_Elemental_Lore_Water",
						"Skill_Bonus_Spiritual_Lore_Blessings", "Skill_Bonus_Spiritual_Lore_Summoning", "Skill_Bonus_Spiritual_Lore_Religion",
						"Skill_Bonus_Mental_Lore_Divination", "Skill_Bonus_Mental_Lore_Manipulation", "Skill_Bonus_Mental_Lore_Telepathy", "Skill_Bonus_Mental_Lore_Transference", "Skill_Bonus_Mental_Lore_Transformation",
						"Skill_Bonus_Sorcerous_Lore_Demonology", "Skill_Bonus_Sorcerous_Lore_Necromancy", "Skill_Bonus_Spell_Research_Minor_Spiritual", 
						"Spellburst"]	
		skill_names = ["Arcane Symbols", "Magic Item Use", "Harness Power", "Spell Aiming",
						"Elemental Mana Control", "Mental Mana Control", "Spiritual Mana Control", 
						"Elemental Lore, Air", "Elemental Lore, Earth", "Elemental Lore, Fire", "Elemental Lore, Water",
						"Spiritual Lore, Blessings", "Spiritual Lore, Summoning", "Spiritual Lore, Religion",
						"Mental Lore, Divination", "Mental Lore, Manipulation", "Mental Lore, Telepathy", "Mental Lore, Transference", "Mental Lore, Transformation", 
						"Sorcerous Lore, Demonology", "Sorcerous Lore, Necromancy"
						]

		index = 0
		base_ranks_arr = {}		
		wearable_totals = []
		worn_totals = []		
		
		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)		
		loop_range = self.Set_Graph_Labels(skill_names, "Spellburst wearable and worn mana", "Mana")	
			
		# Begin the big loop to calculate all the data	
		for i in loop_range:
			temp_tooltip = ""
			temp_mana1 = 0
			temp_mana2 = 0
			skill_ranks_arr = {}
			skill_tooltip_arr = {}
			wearable_tootip = ""
			worn_tootip = ""
			wearable_mana = 0
			worn_mana = 0
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Spellburst\n" % (i)					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Spellburst\n" % ("{:,}".format(i))		
		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					
			
			# Need to use the current level in the spell burst calculations but it can't be 0 or a postcap interval.
			# This check makes sure the level is accurate.
			if i > 100:
				level = 100
			elif i == 0:
				level = 1
			else:
				level = i
				
				
			# Calculate all skill ranks for wearable mana
			for skill in skill_names:				
				tagname = skill.replace(" ", "_").replace(",", "")
				skill_rank_count, temp_tooltip = self.Combine_Effects(i, skill, base_ranks_arr[skill], 
												[lists_of_effects_by_tag["Skill_Bonus_%s" % tagname], lists_of_effects_by_tag["Skill_Ranks_%s" % tagname]], 
												["Skill_Bonus_%s" % tagname, "Skill_Ranks_%s" % tagname], 
												"skill_bonus_to_ranks")

				skill_ranks_arr[skill] = base_ranks_arr[skill] + min(50, skill_rank_count)		
				skill_tooltip_arr[skill] = "".join([ 
										"    %s %s ranks\n" % (("%+d" % skill_ranks_arr["Arcane Symbols"]).rjust(4), skill),
										"       %s  %s base ranks\n" % (("%+d" % base_ranks_arr[skill]).rjust(4), skill),
										temp_tooltip
										])
				

			# Calculate mana cost for all spell effects
			worn_mana, worn_tootip = self.Combine_Effects(i, "", 0, [lists_of_effects_by_tag["Spellburst"]], ["Spellburst"], "spellburst_float_format")				
			
			
			# Calculate wearable mana
			temp_mana2 = skill_ranks_arr["Elemental Mana Control"] + skill_ranks_arr["Mental Mana Control"] + skill_ranks_arr["Spiritual Mana Control"]
			temp_mana2 += skill_ranks_arr["Elemental Lore, Air"] + skill_ranks_arr["Elemental Lore, Earth"] + skill_ranks_arr["Elemental Lore, Fire"] + skill_ranks_arr["Elemental Lore, Water"]
			temp_mana2 += skill_ranks_arr["Spiritual Lore, Blessings"] + skill_ranks_arr["Spiritual Lore, Religion"] + skill_ranks_arr["Spiritual Lore, Summoning"]
			temp_mana2 += skill_ranks_arr["Mental Lore, Divination"] + skill_ranks_arr["Mental Lore, Manipulation"] + skill_ranks_arr["Mental Lore, Telepathy"] + skill_ranks_arr["Mental Lore, Transference"] + skill_ranks_arr["Mental Lore, Transformation"]
			temp_mana2 += skill_ranks_arr["Sorcerous Lore, Demonology"] + skill_ranks_arr["Sorcerous Lore, Necromancy"]
			
			temp_mana1 = skill_ranks_arr["Arcane Symbols"] + skill_ranks_arr["Magic Item Use"] + skill_ranks_arr["Harness Power"] + skill_ranks_arr["Spell Aiming"]
			
			wearable_mana = (temp_mana1 + (0.5 * temp_mana2)) / (225/level)

			
			# Create Tooltip info			
			wearable_tootip = "".join([ 
							"--Wearable Mana--\n",
							"%.1f  Mana = (%s + (0.5 * (%s))) / (225 / %s) \n" % (wearable_mana, temp_mana1, temp_mana2, level),
							"   %s calculated with:\n" % temp_mana1,
							skill_tooltip_arr["Arcane Symbols"],
							skill_tooltip_arr["Harness Power"],
							skill_tooltip_arr["Magic Item Use"],
							skill_tooltip_arr["Spell Aiming"],
							"  %s calculated with:\n" % temp_mana2,
							skill_tooltip_arr["Elemental Mana Control"], skill_tooltip_arr["Mental Mana Control"], skill_tooltip_arr["Spiritual Mana Control"],
							skill_tooltip_arr["Elemental Lore, Air"], skill_tooltip_arr["Elemental Lore, Earth"], skill_tooltip_arr["Elemental Lore, Fire"], skill_tooltip_arr["Elemental Lore, Water"],
							skill_tooltip_arr["Spiritual Lore, Blessings"], skill_tooltip_arr["Spiritual Lore, Religion"], skill_tooltip_arr["Spiritual Lore, Summoning"],
							skill_tooltip_arr["Mental Lore, Divination"], skill_tooltip_arr["Mental Lore, Manipulation"], skill_tooltip_arr["Mental Lore, Telepathy"], skill_tooltip_arr["Mental Lore, Transference"], skill_tooltip_arr["Mental Lore, Transformation"],
							skill_tooltip_arr["Sorcerous Lore, Demonology"], skill_tooltip_arr["Sorcerous Lore, Necromancy"],
							])		
			
			if worn_mana == 0:			
				worn_tootip = "".join([ 
								"--Worn Mana--\n",
								"0 mana. No worn effects count toward spellburst\n"
								])			
			else:
				worn_tootip = "".join([ 
								"--Worn Mana--\n",
								"%.1f  mana calculated with:\n" % worn_mana,
								worn_tootip
								])		
							
			tooltip = "".join([ 
							tooltip,
							"%s  Wearable mana\n" % ("%.1f" % wearable_mana).rjust(4),
							"%s  Worn mana from spells\n" % ("%.1f" % worn_mana).rjust(4),
							wearable_tootip,
							worn_tootip
							])
			

			wearable_totals.append(wearable_mana)
			worn_totals.append(worn_mana)
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(wearable_totals)
		self.graph_information.graph_data_lists.append(worn_totals)						

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = min(wearable_totals[0], worn_totals[-1]) - 5
		self.graph_information.graph_yaxis_max = max(wearable_totals[-1], worn_totals[0]) + 5			

		# Setup the Legend
		self.graph_information.graph_num_lines = 2
		self.graph_information.graph_legend_columns = 2
		self.graph_information.graph_legend_labels.append("Wearable Mana")
		self.graph_information.graph_legend_styles.append("bo-")		
		self.graph_information.graph_legend_labels.append("Worn Mana")
		self.graph_information.graph_legend_styles.append("ro-")			
		
		
	# This method is used to calculate the duration of spellsongs used by the character from level 0-100 or across postcap training. 
	def Formula_Spellsong(self):
		effects_list = ["Skill_Ranks_Mental_Lore_Telepathy", "Skill_Bonus_Mental_Lore_Telepathy"]
		statistic_names = ["Logic", "Influence"]
		skill_names = ["Mental Lore, Telepathy"]

		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}		
			
		# Setup the effects lists and td lists	
		for stat in statistic_names:
			effects_list.append("Statistic_Bonus_%s" % stat)
			effects_list.append("Statistic_%s" % stat)

			
		time_totals = []			

#		override_options = self.Find_Overrides_By_Tags(effects_list)

		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)		
		loop_range = self.Set_Graph_Labels(skill_names, "Spellsong duration", "Duration")	


		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			stat_enh_bonus = 0
			effects_total = 0
			stat_enhancive_totals = {}
			stat_tooltip_arr = {}
			skill_tooltip_arr = {}
			effects_tooltip_text = ""
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Spellsong Duration\n" % (i)
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()	
					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Spellsong Duration\n" % ("{:,}".format(i))
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[100].get()					
		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					

			# Calculate Statistic bonus	
			for stat in statistic_names:
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, stat, 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_%s" % stat], lists_of_effects_by_tag["Statistic_%s" % stat]], 
												["Statistic_Bonus_%s" % stat, "Statistic_%s" % stat], 
												"stat_inc_to_bonus")													

				stat_enhancive_totals[stat] = int(base_stat_arr[stat] + min(50, stat_enh_bonus))
				stat_tooltip_arr[stat] = "       %s  %s base bonus\n" % (("%+d" % base_stat_arr[stat]).rjust(4), stat) + temp_tooltip		
			
				
			# Calculate Weapon Skill bonus
			lore_ranks, temp_tooltip = self.Combine_Effects(i, "Mental Lore, Telepathy", base_ranks_arr["Mental Lore, Telepathy"], 
											[lists_of_effects_by_tag["Skill_Ranks_Mental_Lore_Telepathy"], lists_of_effects_by_tag["Skill_Ranks_Mental_Lore_Telepathy"]], 
											["Skill_Ranks_Mental_Lore_Telepathy", "Skill_Ranks_Mental_Lore_Telepathy"], 
											"skill_bonus_to_ranks")

			lore_ranks_total = base_ranks_arr["Mental Lore, Telepathy"] + min(50, lore_ranks)	
			skill_tooltip_arr["Mental Lore, Telepathy"] = "       %s  Mental Lore, Telepathy base ranks\n" % (("%+d" % base_ranks_arr["Mental Lore, Telepathy"]).rjust(4)) + temp_tooltip
			
						
			# Main Calculation section
			# Base time for all spellsongs is 120 seconds
			base_time = 120
			
			# The bard's level increase the spellsong duration. Technically, this should check to see if the character is a bard
			# However, since bards are the only ones that can sing spellsongs, I didn't see the point is added another check.
			tooltip_level = i
			if i >= 100:
				lvl_time = 250
				tooltip_level = 100
			elif i > 75:
				lvl_time = 225 + (i - 75)
			elif i > 50:
				lvl_time = 175 + (i - 50) * 2
			elif i > 25:
				lvl_time = 100 + (i - 25) * 3
			else:
				lvl_time = i * 4
			
			# Find the total time. Add the above totals together + 3x influence bonus + logic bonus + 2x Telepathy ranks
			total_time = base_time + lvl_time + (3 * stat_enhancive_totals["Influence"]) + stat_enhancive_totals["Logic"] + (2 * lore_ranks_total)
			
			time_totals.append(total_time)
			
			# Create Tooltip info
			tooltip = "".join([ tooltip,
						" %s seconds\n" % total_time,
						"%s seconds calculated with:\n" % total_time,
						"+120 base duration\n",
						"%s bonus from character level (%s)\n" % (("%+d" % lvl_time).rjust(4), tooltip_level),
						"%s bonus from Logic bonus (%+d)\n" % (("%+d" % stat_enhancive_totals["Logic"]).rjust(4), stat_enhancive_totals["Logic"]),
						stat_tooltip_arr["Logic"],
						"%s bonus from Influence bonus (%+d * 3)\n" % (("%+d" % (3 * stat_enhancive_totals["Influence"])).rjust(4), stat_enhancive_totals["Influence"]),
						stat_tooltip_arr["Influence"],
						"%s bonus from Mental Lore, Telepathy ranks (%s * 2)\n" % (("%+d" % (2 * lore_ranks_total)).rjust(4), lore_ranks_total),
						skill_tooltip_arr["Mental Lore, Telepathy"],
						])
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(time_totals)			
					

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = time_totals[0] - 10
		self.graph_information.graph_yaxis_max = time_totals[-1] + 10		
		

		# Setup the Legend
		self.graph_information.graph_num_lines = 1
		self.graph_information.graph_legend_columns = 1
		self.graph_information.graph_legend_labels.append("Spellsong Duration")
		self.graph_information.graph_legend_styles.append("r^-")		


		
	'''	
	# Formula Template
	def Formula_TEMPLATE(self, ...):
		effects_list = ["TD_All", "TD_Elemental", "TD_Mental", "TD_Spiritual", "TD_Sorcerer"]
		statistic_names = ["Strength", "Agility"]
		skill_names = ["Brawling", "Combat Maneuvers"]

		index = 0
		base_stat_arr = {}
		base_ranks_arr = {}
		base_bonus_arr = {}		
			
		# Setup the effects lists and td lists	
		for stat in statistic_names:
			effects_list.append("Statistic_Bonus_%s" % stat)
			effects_list.append("Statistic_%s" % stat)

			
		gloves_totals = []
		boots_totals = []		
		

#		override_options = self.Find_Overrides_By_Tags(effects_list)

		lists_of_effects_by_tag = self.Find_Effects_By_Tags(effects_list)		
		loop_range = self.Set_Graph_Labels(skill_names, "Spellburst wearable and worn mana", "Mana")	


		# Begin the big loop to calculate all the data	
		for i in loop_range:	
			stat_enh_bonus = 0
			effects_total = 0
			stat_enhancive_totals = {}
			stat_tooltip_arr = {}
			skill_tooltip_arr = {}
			effects_tooltip_text = ""
		
			# Only a minor change depending on self.calc_style
			if self.calc_style == 1:
				tooltip = "Level %s: Target Defense\n" % (i)
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[i].get()	
					
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[i].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[i].get()		
					
			elif self.calc_style == 2:	
				tooltip = "Postcap Experience Interval %s: Target Defense\n" % ("{:,}".format(i))
				for stat in statistic_names:				
					base_stat_arr[stat] = globals.character.statistics_list[stat].bonuses_by_level[100].get()					
		
				for skill in skill_names:
					base_ranks_arr[skill] = globals.character.skills_list[skill].total_ranks_by_level[100].get()
					base_bonus_arr[skill] = globals.character.skills_list[skill].bonus_by_level[100].get()
					
					base_ranks_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Total_Ranks_Closest_To_Interval(i)
					base_bonus_arr[skill] += globals.character.skills_list[skill].Postcap_Get_Bonus_Closest_To_Interval(i)	
					

			# Calculate Statistic bonus	
			for stat in statistic_names:
				stat_enh_bonus, temp_tooltip = self.Combine_Effects(i, stat, 0, 
												[lists_of_effects_by_tag["Statistic_Bonus_%s" % stat], lists_of_effects_by_tag["Statistic_%s" % stat]], 
												["Statistic_Bonus_%s" % stat, "Statistic_%s" % stat], 
												"stat_inc_to_bonus")													

				stat_enhancive_totals[stat] = int(base_stat_arr[stat] + min(50, stat_enh_bonus))
				stat_tooltip_arr[stat] = "       %s  %s base bonus\n" % (("%+d" % base_stat_arr[stat]).rjust(4), stat) + temp_tooltip		
				stat_tooltip_arr[stat] = "  %s  %s bonus (%+d / 2)\n" % (("%+d" % (stat_enhancive_totals[stat]/2)).rjust(4), stat, stat_enhancive_totals[stat]) + stat_tooltip_arr[stat]						
			
				
			# Calculate Weapon Skill bonus. 
			weapon_inc_bonus, temp_tooltip = self.Combine_Effects(i, "Brawling", base_bonus_arr["Brawling"], 
											[lists_of_effects_by_tag["Skill_Bonus_Brawling"], lists_of_effects_by_tag["Skill_Ranks_Brawling"]], 
											["Skill_Bonus_Brawling", "Skill_Ranks_Brawling"], 
											"skill_bonus_to_ranks")

			brawling_total = base_ranks_arr["Brawling"] + min(50, weapon_inc_bonus)	
			skill_tooltip_arr["Brawling"] = "  %s  Brawling ranks  (%s * 2)\n" % (("%+d" % (brawling_total*2)).rjust(4), brawling_total) 	
			skill_tooltip_arr["Brawling"] += "       %s  Brawling base ranks\n" % (("%+d" % base_ranks_arr["Brawling"]).rjust(4)) 	
			skill_tooltip_arr["Brawling"] += temp_tooltip
			
			
			# Calculate Combat Maneuver ranks
			skill_rank_count, temp_tooltip = self.Combine_Effects(i, "Combat Maneuvers", base_ranks_arr["Combat Maneuvers"], 
											[lists_of_effects_by_tag["Skill_Bonus_Combat_Maneuvers"], lists_of_effects_by_tag["Skill_Ranks_Combat_Maneuvers"], lists_of_effects_by_tag["Skill_Phantom_Ranks_Combat_Maneuvers"]], 
											["Skill_Bonus_Combat_Maneuvers", "Skill_Ranks_Combat_Maneuvers", "Skill_Phantom_Ranks_Combat_Maneuvers"], 
											"skill_bonus_to_ranks")

			cman_total = base_ranks_arr["Combat Maneuvers"] + skill_rank_count		
			skill_tooltip_arr["Combat Maneuvers"] = "  %s  Combat Maneuver ranks  (%s / 2)\n" % (("%+d" % (cman_total/2)).rjust(4), cman_total) 		
			skill_tooltip_arr["Combat Maneuvers"] += "       %s  Combat Maneuvers base ranks\n" % (("%+d" % base_ranks_arr["Combat Maneuvers"]).rjust(4)) 				
			skill_tooltip_arr["Combat Maneuvers"] += temp_tooltip				
						
			
			
			# Main Calculation section

			
			
			gloves_totals.append(gloves_value)
			boots_totals.append(boots_value)
			
			# Create Tooltip info
			tooltip = "".join([ tooltip,
						])
			
			self.graph_information.tooltip_array.append(tooltip[:-1])	

			index += 1
					
		
		# Loop is done, set up the graph_infomation object		

		# Append the completed lists to graph_infomation object
		self.graph_information.graph_data_lists.append(gloves_totals)
		self.graph_information.graph_data_lists.append(boots_totals)					
					

		# Set the minimum height for the graph
		self.graph_information.graph_yaxis_min = min(gloves_totals[0], boots_totals[0]) - 5
		self.graph_information.graph_yaxis_max = max(gloves_totals[-1], boots_totals[-1]) + 5		
		

		# Setup the Legend
		self.graph_information.graph_num_lines = 1
		self.graph_information.graph_legend_columns = 1
		self.graph_information.graph_legend_labels.append("Elemental TD")
		self.graph_information.graph_legend_styles.append("r^-")			
	'''	
		





# This class is used with Formula_Summations to categorize and keep track of information needed to display
# correct summation values
class Summation:
	def __init__(self, arr, spell_circles):	
		self.effect_name = arr["effect_name"]
		self.lore_skill = arr["lore_skill"].split("|")
		self.category = arr["category"]
		self.bonus_style = arr["bonus_style"]
		self.default_bonus = float(arr["default_bonus"]) if "." in arr["default_bonus"] else int(arr["default_bonus"])
		self.info_string = arr["info_string"]
		self.custom_seed = arr["custom_seed"]
		self.rank_cap = int(arr["rank_cap"])
		self.summation_seed = arr["summation_seed"]
		self.multiplier = float(arr["multiplier"]) if "." in arr["multiplier"] else int(arr["multiplier"])
		self.value_format = "float" if "." in arr["multiplier"] else "int"
		self.index_to_rank_cap = 0
		self.last_index = 0
		self.circle_divisor = 1		
		self.summation_bonus_list = ""
		
		if self.category.replace(" Base", "") not in spell_circles:
			if "Base" in self.category:
				self.circle_divisor = 3
			elif "Major" in self.category:
				self.circle_divisor = 2
		
		if self.summation_seed != "CUSTOM":
			self.summation_seed = int(self.summation_seed)
			self.summation_bonus_list = globals.summation_bonuses[self.summation_seed]
		else:
			split_parts = self.custom_seed.split("|")
			if "~" not in split_parts[0]:
				self.custom_seed = [int(i) for i in split_parts]
			else:
				self.custom_seed = split_parts
			self.summation_bonus_list = self.custom_seed		

#		if spell_circles == 1:
		length = len(self.summation_bonus_list)
		for k in range(0, length):
			if self.rank_cap <= self.summation_bonus_list[k]:
				self.index_to_rank_cap = k
				break
					
			
	# With useable_ranks, find out the correspoding value and insert it into a string to be 
	# returned and displayed in the tooltip
	def Get_Summation_Info_String(self, skill_names, ranks_dict):			
#		print(self.effect_name)
		info = ""
		current_bonus = ""	
		next_bonus = ""	
		summation_message = ""
		useable_ranks = 0
		multiple_useable_ranks = []
		multiple_index = []
		multi_message = ""
		
#		if self.bonus_style == "Number" or (self.bonus_style == "Text" and len(self.lore_skill) == 1):
		if self.rank_cap != 0:			
			for skill in self.lore_skill:				
				useable_ranks += ranks_dict[skill]			

			if useable_ranks < self.summation_bonus_list[0]:
				return ""
			
			
			while useable_ranks >= self.summation_bonus_list[self.last_index] and useable_ranks < self.rank_cap:				
				self.last_index += 1
			
			if useable_ranks < self.rank_cap:
				self.last_index = max(0, self.last_index - 1)
			elif useable_ranks >= self.rank_cap:
				self.last_index = self.index_to_rank_cap
						
			
			if self.bonus_style == "Text":
				info = self.info_string.split("|")[self.last_index]
			elif self.bonus_style == "Number": 
				value = self.default_bonus + ((self.last_index + 1) * self.multiplier)
				if self.value_format == "float":
					value = round(value, 3)
				info = self.info_string.replace("??", str(value))
			
			if useable_ranks < self.rank_cap:
				current_bonus = "Current %s, " % self.summation_bonus_list[self.last_index]
				next_bonus = " Next %s,  " % self.summation_bonus_list[self.last_index + 1]
			
			if len(skill_names) > 1:
				for skill in self.lore_skill:		
					multi_message += "%s, " % (globals.LdP_effect_display_scaling["%s ranks" % skill])
				multi_message = "%sUsing Lores: %s\n" % (("%s" % "").rjust(12), multi_message[:-2])
			
			cap_text = self.summation_bonus_list[-1]
		
		# This one is only for Text summations that use more than one lore skill
#		elif self.bonus_style == "Text":		
		else:
			failed = 0
			list_length = len(self.summation_bonus_list)
			
			for i in range(self.last_index, list_length):
				j = 0
				bonus_parts = self.summation_bonus_list[i].split("~")
			
				for skill in self.lore_skill:	
					if int(bonus_parts[j]) > ranks_dict[skill]:
						failed = 1
						break
					j += 1
					
				if failed:
					break
					
				self.last_index += 1				
					
			if failed:
				if self.last_index == 0:
					return ""
				else:
					self.last_index -= 1
					current_bonus = "Current %s, " % self.summation_bonus_list[self.last_index]
					next_bonus = " Next %s,  " % self.summation_bonus_list[self.last_index + 1]
			else:
				self.last_index -= 1

			if self.bonus_style == "Text":
				info = self.info_string.split("|")[self.last_index]
			elif self.bonus_style == "Number": 
				value = self.default_bonus + ((self.last_index + 1) * self.multiplier)
				if self.value_format == "float":
					value = round(value, 3)
				info = self.info_string.replace("??", str(value))
			

			for skill in self.lore_skill:		
				multi_message += "%s, " % (globals.LdP_effect_display_scaling["%s ranks" % skill])
				
			multi_message = "%sUsing Lores: %s\n" % (("%s" % "").rjust(12), multi_message[:-2])
#			cap_text = self.summation_bonus_list[-1].replace("~", ", ")
			cap_text = self.summation_bonus_list[-1]
		
		
		summation_message = "      %s\n%s%sSummation Bonus: %s%sMax %s\n" % (info, multi_message, ("%s" % "").rjust(12), current_bonus, next_bonus, cap_text)
		return summation_message


# This class is used in a single global object that tracks ALL that data needed to be graphed on the Figure
# The Formula methods will populate the object as the data calculated
class Graph_Data_Line_Container:	
	def __init__(self):		
		self.graph_num_lines = 0   				# How many lines do we need to graph?	
		
		self.graph_xlabel = ""					# Vertical left label
		self.graph_xlabel_size = 12
		self.graph_ylabel = ""					# Horizonal bottom label
		self.graph_yaxis_min = 0				# x-axis always has a set range. y will need to specified
		self.graph_yaxis_max = 0
		self.graph_xaxis_tick_range = []		
		self.graph_xaxis_tick_labels = []
		self.graph_xaxis_rotation = 0			# This is changed
		self.graph_xaxis_size = 12
		
		self.graph_legend_columns = 1
		self.graph_legend_labels = []
		self.graph_legend_styles = []
		
		self.graph_data_lists = []				# Where the calculated information is stored in a 100 sized array for precap or variable sized for postcap
		self.tooltip_array = []					# Tooltip text detailing how the above data was calculated. Same size as graph_data_lists
	
	# Resets the object back to default so it can be reused by a new Formula method
	def Reset_Graph_Data(self):	
		self.graph_num_lines = 0   		
		
		self.graph_xlabel = ""
		self.graph_xlabel_size = 12
		self.graph_ylabel = ""	
		self.graph_yaxis_min = 0
		self.graph_yaxis_max = 0
		self.graph_xaxis_tick_range = []
		self.graph_xaxis_tick_labels = []
		self.graph_xaxis_rotation = 0
		self.graph_xaxis_size = 12
		
		self.graph_legend_columns = 1
		self.graph_legend_labels = []
		self.graph_legend_styles = []
		
		self.graph_data_lists = []	
		self.tooltip_array = []	
	
