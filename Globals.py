# This file contains variables used by all the other planner files.

# INDEX OF CLASSES AND METHODS
'''	
class Character:
	def __init__(self):
	def Load_Character(self):
	def Save_Character(self):
	def Update_Statistics(self):	
	def Update_Resources(self, level):
	def Is_Prime_Stat(self, stat):
	def Update_Skills(self):
	def Calculate_Subskill_Regained_TP(self, level, subskill_group):
	def Get_Total_Ranks_Of_Subskill(self, name, level, subskill_group):
	def Update_Maneuvers(self):
	def Meets_Maneuver_Prerequisites(self, level, name, type):
	def Get_Last_Training_Interval(self, exp, type, subtype):	

class Race:
	def __init__(self, arr):

class Profession:
	def __init__(self, arr):
	
class Statistic:	
	def __init__(self, parent, name):	
	def Set_To_Default(self):	
	def Create_Statistic_Row_Frame(self, panel, stat):
	def Create_Growth_Row_Frame(self, parent):
	def Update_Growth_Frame(self):		
	def Entrybox_Validate(self, d, S, s, P):	
	def Entrybox_On_Move(self, event):
	def Set_Stat_Importance(self, action):
	
class Skill:
	def __init__(self, arr):
	def Set_To_Default(self):
	def Set_To_Default_Postcap(self):	
	def Update_Skill_Information(self, arr):
	def Create_SkP_schedule_row(self, parent):	
	def Create_PcP_schedule_row(self, parent):
	def Train_New_Ranks(self, level, subskill_ranks, ranks):
	def Get_Skill_Bonus(self, ranks):
	def Calculate_TP_Regain(self, start, end):
	def Get_Total_Skill_Cost(self, subskill_ranks, ranks, current_level):
	def Get_Next_Ranks_Cost(self, level, subskill_ranks, new_ranks):
	def Postcap_Get_Total_Ranks_Closest_To_Interval(self, interval):
	def Postcap_Get_Total_Bonus_Closest_To_Interval(self, interval):
	def Train_Postcap_Ranks(self, ranks, subskill_ranks, exp):	
	
class Maneuver:
	def __init__(self, schedule_parent, arr):
	def Set_To_Default(self):
	def Set_To_Default_Postcap(self):	
	def Button_Onclick(self, result):
	def Create_ManP_schedule_row(self, parent):
	def Create_PcP_schedule_row(self, parent):
	def Get_Cost_At_Rank(self, rank, prof_type):	
	def Get_Total_Cost_At_Rank(self, start_rank, new_ranks, prof_type):			
	def Train_New_Ranks(self, level, ranks, prof_type):	
	def Train_Postcap_Ranks(self, exp, ranks, prof_type):	
	def Postcap_Get_Total_Ranks_Closest_To_Interval(self, interval):	

class Gear:
	def __init__(self, order, name, enchantment, weight, skill_names, type):
	def Create_LdP_row(self, parent):
	def Set_Gear_Traits(self, name):
	def Update_Display_Details(self):
	def Update_Progression_Name(self):	

class Effect:
	def __init__(self, order, name, type, display_type, details, effect_tags, scaling_arr, function, options, hidden):
	def Create_ProgP_row(self, parent):
	def Create_LdP_row(self, parent):
	def Update_Row_Heights(self):
	def Calculate_Tag_Bonus(self, effect_tag, level):
	def Scroll_Details_Frame(self, event):
	def Scroll_Scaling_Frame(self, event):

class Information_Dialog:
	def __init__(self):
	def Set_To_Default(self):
	def Show_Message(self, msg):
	def Scroll_Inner_Frame(self, event):	
'''

#!/usr/bin/python
import sys
import tkinter
import tkinter.filedialog
import tkinter.font
import math
import Pmw
import re
import collections
if sys.version_info[1] >- 10:
	collections.Callable = collections.abc.Callable
import Calculations as calculations

# The Character object holds all the values and objects related to the character from across all the panels.
# These values can be easily accessed by all other panels and allows the planner to save and load character build file with minimum effort.
class Character:
	def __init__(self):
		global statistics
		
		# Statistics Panel variables
		self.race = ""
		self.profession = ""
		
		self.race_list = {}					# Contains a list of Race objects using the name of each race name as a key
		self.profession_list = {}			# Contains a list of Profession objects using the name of each profession name as a key
		self.statistics_list = {}         	# Contains a list of Statistic objects using the name of each statistic as a key
		self.racial_stat_bonus = {}         # Contains a list of bonuses for each statistic (calculted by race) using the name of each statistic as a key
		self.stat_adj = {}					# Contains a list of statistic adjustments (combination of race and profession growths) using the name of each statistic as a key
		
		# Initialize the above variables
		for stat in statistics:
			self.statistics_list[stat] = Statistic(self, stat)
			self.racial_stat_bonus[stat] = tkinter.IntVar()
			self.stat_adj[stat] = tkinter.IntVar()
			
		# People like seeing the decimal form of their starting Training Point values when determining their starting stats. The rounded down value of each is using for the by_level variables
		self.ptp_base = tkinter.DoubleVar()
		self.mtp_base = tkinter.DoubleVar()
		self.statistic_totals_by_level = [tkinter.IntVar() for i in range(101)]
		self.ptp_by_level = [tkinter.IntVar() for i in range(101)]		
		self.mtp_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_ptp_by_level = [tkinter.IntVar() for i in range(101)]		
		self.total_mtp_by_level = [tkinter.IntVar() for i in range(101)]
		
		# Resources are shown on the Statistics Panel but all of them need Skill build information to be calculated correctly.
		self.health_by_level = [tkinter.IntVar() for i in range(101)]
		self.mana_by_level = [tkinter.IntVar() for i in range(101)]
		self.stamina_by_level = [tkinter.IntVar() for i in range(101)]
		self.spirit_by_level = [tkinter.IntVar() for i in range(101)]
					
		
		# Misc Panel variables
		self.deity = tkinter.StringVar()
		self.elemental_attunement = tkinter.StringVar()
		self.society = tkinter.StringVar()
		self.society_rank = tkinter.StringVar()
		self.guild_skills_ranks = [tkinter.StringVar() for i in range(6)]    # Let the profession object handle what the guild skills are. This hold the vars the for the Misc rows		
		
		# Skills Panel variables		
		self.build_skills_list = []           # A list of Build_List_Skill objects that represent what the character wants to train in.
		self.skills_list = {}                 # Hash of skill name -> Skill objects
		
		
		# Maneuvers Panel variables			
		# Lists of Build_List_Skill objects that represent what the character wants to train in for each maneuver type
		self.combat_maneuvers_list = {}
		self.shield_maneuvers_list = {}
		self.armor_maneuvers_list = {}		
		# Because their are different types of maneuvers, a seperate set of variables must be kept for each type: Combat, Shield, Armor		
		self.build_combat_maneuvers_list = []
		self.build_armor_maneuvers_list = []
		self.build_shield_maneuvers_list = []	
		# Points for training in maneuvers are calculated as 1 point per rank in a specific skill. Combat -> Comabat Manevuers, Shield -> Shield Use, Armor -> Armor Use
		self.combat_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.shield_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.armor_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_combat_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_shield_points_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_armor_points_by_level = [tkinter.IntVar() for i in range(101)]
		
		
		# Post Cap Panel variables
		# variables for build list
		self.postcap_build_skills_list = []
		self.postcap_build_combat_maneuvers_list = []
		self.postcap_build_armor_maneuvers_list = []
		self.postcap_build_shield_maneuvers_list = []		 
		self.postcap_skill_training_by_interval = collections.OrderedDict()		
		self.postcap_total_skill_cost_by_interval = collections.OrderedDict()    # Includes both the PTP/MTP cost at a specific interval and the cumulative PTP/MTP cost for all intervals 	up to (and including) a specific interval
		self.postcap_TP_conversions_by_interval = collections.OrderedDict()      # Format A/B|C/D   A=PTP converted this interval, B=same as A but for MTP, C=Cumulative PTP converted at this interval including this interval, D=same as C but for MTP		
		self.postcap_combat_training_by_interval = collections.OrderedDict()		
		self.postcap_total_combat_cost_by_interval = collections.OrderedDict()    
		self.postcap_shield_training_by_interval = collections.OrderedDict()		
		self.postcap_total_shield_cost_by_interval = collections.OrderedDict()    
		self.postcap_armor_training_by_interval = collections.OrderedDict()		
		self.postcap_total_armor_cost_by_interval = collections.OrderedDict()    


		# Loadout Panel variables
		self.loadout_gear_build_list = []
		self.loadout_effects_build_list = []
		
		
		# Progression Panel variables
		self.LdP_Gear_List_Updated = 0
		self.LdP_Effects_List_Updated = 0
		
		
	# This method will prompt the user for a .txt file and will populate the Character class with the information saved in the file
	def Load_Character(self):
		global statistics, panels, char_name, title, version, root, notebook, db_cur, db_con, LdP_Gear_List_Updated, LdP_Effects_List_Updated
		char_file = tkinter.filedialog.askopenfile(initialdir="Characters", filetypes=[("Text files","*.txt")], mode='r', title="Load GS4 Character")
		stat_panel = panels["Statistics"]
		skills_panel = panels["Skills"]
		man_panel = panels["Maneuvers"]
		postcap_panel = panels["Post Cap"]
		loadout_panel = panels["Loadout"]
		progression_panel = panels["Progression"]
#		summary_panel = panels["Summary"]
		read_mode = ""
		
		# If the user cancelled out of the file prompt, end the method immediately
		if char_file == None:
			return
		
		char_name = char_file.name.split("/")[-1].split("\\")[-1].split(".")[0]
		root.title("%s %s - %s" % (title, version, char_name))
		
		# Clear all the panels so we have a clean slate
		for stat, obj in self.statistics_list.items():
			obj.Set_To_Default()
		skills_panel.ClearAll_Button_Onclick()
		man_panel.Clear_Button_Onclick("All")
		postcap_panel.Clear_Button_Onclick("All")		
		loadout_panel.Gear_ClearAll_Button_Onclick()
		loadout_panel.Effects_ClearAll_Button_Onclick()
		LdP_Gear_List_Updated = 1				
		LdP_Effects_List_Updated = 1
		
		# Read the file line by line and remove the end of line character "\n" at the end of each line if it is present
		line = char_file.readline()
		while line:
			if line[-1] == "\n":
				line = line[:-1]
							
			# Sets the "read mode" of the method. Read mode determines what the method will do when it read in a line from the file.
			# Each header in the character file marks the begining of a new type of information in the save file and will change the read mode accordingly.
			# The rest of the loop is skipped when the read mode is changed.
			if line == "==CHARACTER INFORMATION==":
				read_mode = "character"
				line = char_file.readline()
				continue
			elif line == "==STATISTICS INFORMATION==":
				read_mode = "statistics"
				line = char_file.readline()
				continue
			elif line == "==GUILD SKILLS RANKS==":
				read_mode = "guild skills"
				line = char_file.readline()
				continue
			elif line == "==SKILLS BUILD LIST==":
				read_mode = "skill"
				line = char_file.readline()
				continue
			elif line == "==COMBAT MANEUVERS BUILD LIST==":
				read_mode = "combat"
				line = char_file.readline()
				continue
			elif line == "==SHIELD MANEUVERS BUILD LIST==":
				read_mode = "shield"
				line = char_file.readline()
				continue
			elif line == "==ARMOR MANEUVERS BUILD LIST==":
				read_mode = "armor"
				line = char_file.readline()
				continue
			elif line == "==SKILLS POSTCAP BUILD LIST==":
				read_mode = "skill postcap"
				line = char_file.readline()
				continue
			elif line == "==COMBAT MANEUVERS POSTCAP BUILD LIST==":
				read_mode = "combat postcap"
				line = char_file.readline()
				continue
			elif line == "==SHIELD MANEUVERS POSTCAP BUILD LIST==":
				read_mode = "shield postcap"
				line = char_file.readline()
				continue
			elif line == "==ARMOR MANEUVERS POSTCAP BUILD LIST==":
				read_mode = "armor postcap"
				line = char_file.readline()
				continue
			elif line == "==GEAR BUILD LIST==":
				read_mode = "gear"
				line = char_file.readline()
				continue
			elif line == "==EFFECTS BUILD LIST==":
				read_mode = "effects"
				line = char_file.readline()
				continue
			
			parts = line.split(":")            # Every field in the save file line is divided by semi-colons. Splitting on the semi-colon will give us the individual parts of the line.
			
			# Character is for the profession and race. Since the profession determines skill costs of build_list_skill objects, it needs be set immediately.
			if read_mode == "character":
				if parts[0] == "Profession":
					stat_panel.profession_dd.set(parts[1])
					stat_panel.Change_Profession(panels["Statistics"].profession_dd.get())  
				elif parts[0] == "Race":
					stat_panel.race_dd.set(parts[1])		
					stat_panel.Change_Race(panels["Statistics"].race_dd.get())		
				elif parts[0] == "Deity":
					self.deity.set(parts[1])
				elif parts[0] == "Attunement":
					self.elemental_attunement.set(parts[1])
				elif parts[0] == "Society":
					self.society.set(parts[1])
					self.society_rank.set(parts[2])	
					
			# For statistics, update the appropriate statistic with the listed value. All statistics will be recalculated later
			elif read_mode == "statistics":
				self.statistics_list[parts[0]].values_by_level[0].set(parts[1])		
				
			elif read_mode == "guild skills":
				if( parts[0] not in self.profession.guild_skills ):
					continue
				position = self.profession.guild_skills.index(parts[0])
				self.guild_skills_ranks[position].set(parts[1])
				
			elif read_mode == "skill":
				skill = self.skills_list[parts[0]]
				location = len(self.build_skills_list)
				self.build_skills_list.insert(location, skills_panel.Create_Build_List_Skill(skills_panel.ML_Frame.interior(), parts[0], parts[1], location, 
				"%s / %s (%s)" % (skill.ptp_cost,skill.mtp_cost, skill.max_ranks), parts[3], parts[4], parts[2]) )		
				self.build_skills_list[location].Set_Training_Rate(skill.max_ranks)
				
			# Each of the maneuver types will read in the line and use the information to create a Build_List_Maneuver and add it to a manevuer list.
			# The order of the build is determined by the order the maneuvers are listed in the file
			elif read_mode == "combat":
				man = self.combat_maneuvers_list[parts[0]]
				location = len(self.build_combat_maneuvers_list)
				self.build_combat_maneuvers_list.insert(location, man_panel.Create_Build_List_Maneuver(man_panel.ML_Frame.interior(), parts[0], 
				"Combat", parts[1], location, parts[3], parts[4], parts[2], (man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ))	
			elif read_mode == "shield":
				man = self.shield_maneuvers_list[parts[0]]
				location = len(self.build_shield_maneuvers_list)
				self.build_shield_maneuvers_list.insert(location, man_panel.Create_Build_List_Maneuver(man_panel.ML_Frame.interior(), parts[0], 
				"Shield", parts[1], location, parts[3], parts[4], parts[2],	(man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ))	
			elif read_mode == "armor":
				man = self.armor_maneuvers_list[parts[0]]
				location = len(self.build_armor_maneuvers_list)
				self.build_armor_maneuvers_list.insert(location, man_panel.Create_Build_List_Maneuver(man_panel.ML_Frame.interior(), parts[0], 
				"Armor", parts[1], location, parts[3], parts[4], parts[2], (man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ))		
			

			# Post cap lines are treated almost the same as the precap lines.
			elif read_mode == "skill postcap":
				skill = self.skills_list[parts[0]]
				location = len(self.postcap_build_skills_list)
				self.postcap_build_skills_list.insert(location, postcap_panel.Create_Postcap_Build_List_Skill(postcap_panel.ML_Frame.interior(), parts[0], parts[1], location,
				"%s / %s (%s)" % (skill.ptp_cost,skill.mtp_cost, skill.max_ranks), parts[2]) )						
				self.postcap_build_skills_list[location].PcP_Edit_Button.config(command=lambda v=location: postcap_panel.Add_Edit_Button_Onclick(v))				
			elif read_mode == "combat postcap":
				man = self.combat_maneuvers_list[parts[0]]
				location = len(self.postcap_build_combat_maneuvers_list)
				self.postcap_build_combat_maneuvers_list.insert(location, postcap_panel.Create_Postcap_Build_List_Maneuver(postcap_panel.ML_Frame.interior(), parts[0], 
				"Combat", parts[1], location, parts[2], (man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ) )						
			elif read_mode == "shield postcap":
				man = self.shield_maneuvers_list[parts[0]]
				location = len(self.postcap_build_shield_maneuvers_list)
				self.postcap_build_shield_maneuvers_list.insert(location, postcap_panel.Create_Postcap_Build_List_Maneuver(postcap_panel.ML_Frame.interior(), parts[0], 
				"Shield", parts[1], location, parts[2], (man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ) )		
			elif read_mode == "armor postcap":
				man = self.armor_maneuvers_list[parts[0]]
				location = len(self.postcap_build_armor_maneuvers_list)
				self.postcap_build_armor_maneuvers_list.insert(location, postcap_panel.Create_Postcap_Build_List_Maneuver(postcap_panel.ML_Frame.interior(), parts[0], 
				"Armor", parts[1], location, parts[2], (man.cost_by_rank[0], man.cost_by_rank[1], man.cost_by_rank[2], man.cost_by_rank[3], man.cost_by_rank[4]) ) )

			
			# Loadout lines for gear items and effects
			elif read_mode == "gear":			
				location = len(self.loadout_gear_build_list)
				gear = Gear(location+1, parts[0], parts[3], parts[4], parts[2], parts[1])	
				gear.Create_LdP_row(loadout_panel.Gear_List_Frame.interior())		
				gear.LdP_Row.grid(row=location, column=0)					
				gear.Update_Display_Details()
				gear.Set_Gear_Traits("")
				
				self.loadout_gear_build_list.insert(location, gear)			
				
			elif read_mode == "effects":
				location = len(self.loadout_effects_build_list)
				length = len(parts)
				scaling_arr = collections.OrderedDict()
				
				if length == 3 and parts[2] == "NONE":
					pass
				else:
					for i in range(2, length):
						data = parts[i].split("=")
						scaling_arr[data[0]] = data[1]
						
						
				db_cur.execute("SELECT type, details, effect_tags, scaling_tags, function, override_options FROM Effects WHERE name = \"%s\" " % (parts[0]))
				db_con.commit()		
				data = db_cur.fetchone()		
			
				type = ""
				for key, val in LdP_effect_display_types.items():
					if val == data["type"]:
						type = key
						break
				self.loadout_effects_build_list.insert(location, Effect(location, parts[0], type, data["type"], data["details"], data["effect_tags"], scaling_arr, data["function"], data["override_options"], parts[1] ) )
				
				self.loadout_effects_build_list[location].Create_LdP_row(loadout_panel.Effects_List_Frame.interior())	
				
				
			# End of the loop, read the next line.		
			line = char_file.readline()
	
		# Post file reading Planner setup
		# Calculate the statistics' growths and make sure the skills and maneuvers have the correct order
		for stat in statistics:
			self.statistics_list[stat].Calculate_Growth()
			self.statistics_list[stat].Update_Growth_Frame()
	
		# Make sure the added Skills are displayed in the build frame in the Skills Panel
		i = 0 
		for skill in self.build_skills_list:
			skill.order.set(i+1)
			skill.SkP_Edit_Button.config(command=lambda v=i: skills_panel.Add_Edit_Button_Onclick(v))
			skill.SkP_Build_Row.grid(row=i, column=0)					
			i += 1		
			
		# Make sure the order drop down menues are setup correctly
		skills_panel.menu_size = i+1
		if skills_panel.menu_size > 1:
			for j in range(2, skills_panel.menu_size+1):
				if j > 2:
					skills_panel.edit_order_menu["menu"].insert_command("end", label=j-1, command=lambda v=j-1: skills_panel.vars_dialog_order.set(v))	
				skills_panel.add_order_menu["menu"].insert_command("end", label=j, command=lambda v=j: skills_panel.vars_dialog_order.set(v))	
			
			
		# Maneuvers are set up the same way as skills but Combat Maneuvers are shown by default instead of every maneuver
		i = 0 
		for man in self.build_combat_maneuvers_list:
			man.order.set(i+1)
			man.ManP_Edit_Button.config(command=lambda v=i: man_panel.Add_Edit_Button_Onclick(v))
			i += 1					
		man_panel.combat_menu_size = i+1
		if man_panel.combat_menu_size > 1:
			for j in range(2, man_panel.combat_menu_size+1):
				if j > 2:
					man_panel.edit_combat_order_menu["menu"].insert_command("end", label=j-1, command=lambda v=j-1: man_panel.vars_dialog_order.set(v))	
				man_panel.add_combat_order_menu["menu"].insert_command("end", label=j, command=lambda v=j: man_panel.vars_dialog_order.set(v))	
				
		i = 0 
		for man in self.build_shield_maneuvers_list:
			man.order.set(i+1)
			man.ManP_Edit_Button.config(command=lambda v=i: man_panel.Add_Edit_Button_Onclick(v))
			i += 1					
		man_panel.shield_menu_size = i+1
		if man_panel.shield_menu_size > 1:
			for j in range(2, man_panel.shield_menu_size+1):
				if j > 2:
					man_panel.edit_shield_order_menu["menu"].insert_command("end", label=j-1, command=lambda v=j-1: man_panel.vars_dialog_order.set(v))	
				man_panel.add_shield_order_menu["menu"].insert_command("end", label=j, command=lambda v=j: man_panel.vars_dialog_order.set(v))	
				
		i = 0 
		for man in self.build_armor_maneuvers_list:
			man.order.set(i+1)
			man.ManP_Edit_Button.config(command=lambda v=i: man_panel.Add_Edit_Button_Onclick(v))
			i += 1			
		man_panel.armor_menu_size = i+1
		if man_panel.armor_menu_size > 1:
			for j in range(2, man_panel.armor_menu_size+1):
				if j > 2:
					man_panel.edit_armor_order_menu["menu"].insert_command("end", label=j-1, command=lambda v=j-1: man_panel.vars_dialog_order.set(v))	
				man_panel.add_armor_order_menu["menu"].insert_command("end", label=j, command=lambda v=j: man_panel.vars_dialog_order.set(v))			
			
		man_panel.maneuver_mode.set("")
		man_panel.Maneuver_Style_Onchange("Combat")
			
			
		# Postcap panel works mostly the same as the Skills and Maneuvers panels
		i = 0 
		for skill in self.postcap_build_skills_list:
			skill.order.set(i+1)
			skill.PcP_Edit_Button.config(command=lambda v=i: postcap_panel.Add_Edit_Button_Onclick(v))
			skill.PcP_Build_Row.grid(row=i, column=0)					
			i += 1					
		postcap_panel.skills_menu_size = i+1
		if postcap_panel.skills_menu_size > 1:
			for j in range(2, postcap_panel.skills_menu_size+1):
				if j > 2:
					postcap_panel.edit_skill_order_menu["menu"].insert_command("end", label=j-1, command=lambda v=j-1: postcap_panel.vars_dialog_order.set(v))	
				postcap_panel.add_skill_order_menu["menu"].insert_command("end", label=j, command=lambda v=j: postcap_panel.vars_dialog_order.set(v))	
				
		i = 0 
		for man in self.postcap_build_combat_maneuvers_list:
			man.order.set(i+1)
			man.PcP_Edit_Button.config(command=lambda v=i: postcap_panel.Add_Edit_Button_Onclick(v))
			i += 1					
		postcap_panel.combat_menu_size = i+1
		if postcap_panel.combat_menu_size > 1:
			for j in range(2, postcap_panel.combat_menu_size+1):
				if j > 2:
					postcap_panel.edit_combat_order_menu["menu"].insert_command("end", label=j-1, command=lambda v=j-1: postcap_panel.vars_dialog_order.set(v))	
				postcap_panel.add_combat_order_menu["menu"].insert_command("end", label=j, command=lambda v=j: postcap_panel.vars_dialog_order.set(v))	
				
		i = 0 
		for man in self.postcap_build_shield_maneuvers_list:
			man.order.set(i+1)
			man.PcP_Edit_Button.config(command=lambda v=i: postcap_panel.Add_Edit_Button_Onclick(v))
			i += 1					
		postcap_panel.shield_menu_size = i+1
		if postcap_panel.shield_menu_size > 1:
			for j in range(2, postcap_panel.shield_menu_size+1):
				if j > 2:
					postcap_panel.edit_shield_order_menu["menu"].insert_command("end", label=j-1, command=lambda v=j-1: postcap_panel.vars_dialog_order.set(v))	
				postcap_panel.add_shield_order_menu["menu"].insert_command("end", label=j, command=lambda v=j: postcap_panel.vars_dialog_order.set(v))	
				
		i = 0 
		for man in self.postcap_build_armor_maneuvers_list:
			man.order.set(i+1)
			man.PcP_Edit_Button.config(command=lambda v=i: postcap_panel.Add_Edit_Button_Onclick(v))
			i += 1			
		postcap_panel.armor_menu_size = i+1
		if postcap_panel.armor_menu_size > 1:
			for j in range(2, postcap_panel.armor_menu_size+1):
				if j > 2:
					postcap_panel.edit_armor_order_menu["menu"].insert_command("end", label=j-1, command=lambda v=j-1: postcap_panel.vars_dialog_order.set(v))	
				postcap_panel.add_armor_order_menu["menu"].insert_command("end", label=j, command=lambda v=j: postcap_panel.vars_dialog_order.set(v))			
			
		postcap_panel.goal_mode.set("Skills")
		postcap_panel.PostCap_Style_Onchange("Skills")		
		
		# Loadout panel. Load the gear list and effects list
		i = 0 
		for gear in self.loadout_gear_build_list:
			gear.order.set(i+1)
			gear.LdP_Edit_Button.config(command=lambda v=i: loadout_panel.Gear_Add_Edit_Button_Onclick(v))
			i += 1					
		loadout_panel.gear_menu_size = i+1
		if loadout_panel.gear_menu_size > 1:
			for j in range(2, loadout_panel.gear_menu_size+1):
				if j < loadout_panel.gear_menu_size+1:						
					loadout_panel.dialog_gear_edit_order_menu["menu"].insert_command("end", label=j-1, command=lambda v=j-1: loadout_panel.vars_dialog_order.set(v))				
				loadout_panel.dialog_gear_add_order_menu["menu"].insert_command("end", label=j, command=lambda v=j: loadout_panel.vars_dialog_order.set(v))	
		
		i = 0 
		for effect in self.loadout_effects_build_list:	
			effect.order.set(i+1)
			effect.LdP_Build_Row.grid(row=i, column=0)
			effect.LdP_Edit_Button.config(command=lambda v=i: loadout_panel.Effects_Add_Edit_Button_Onclick(v))
			i += 1					
		loadout_panel.effects_menu_size = i+1
		if loadout_panel.effects_menu_size > 1:
			for j in range(2, loadout_panel.effects_menu_size+1):
				if j < loadout_panel.effects_menu_size+1:				
					loadout_panel.dialog_effect_edit_order_menu["menu"].insert_command("end", label=j-1, command=lambda v=j-1: loadout_panel.vars_dialog_order.set(v))	
				loadout_panel.dialog_effect_add_order_menu["menu"].insert_command("end", label=j, command=lambda v=j: loadout_panel.vars_dialog_order.set(v))				
		
		
		
		# We are done. Change to the first panel.
		notebook.selectpage("Statistics")

		
	# Opens a .txt file and reads in information one line at a time and populates the planner with the new information
	def Save_Character(self):
		global statistics, char_name, version, root
		char_file = tkinter.filedialog.asksaveasfile(initialdir="Characters", defaultextension=".txt", mode='w', title="Save GS4 Character As ...")
		society_rank = self.society_rank.get()
		if( society_rank == ""):
			society_rank = 0 
			self.society_rank.set(0)
			
		if char_file == None:
			return		
			
		char_name = char_file.name.split("/")[-1].split("\\")[-1].split(".")[0]
		root.title("Gemstone IV Character Planner %s - %s" % (version, char_name))
			
		char_file.write("==CHARACTER INFORMATION==\n")	
		char_file.write("Profession:%s\n" % self.profession.name)	
		char_file.write("Race:%s\n" % self.race.name)	
		char_file.write("Deity:%s\n" % self.deity.get())	
		char_file.write("Attunement:%s\n" % self.elemental_attunement.get())	
		char_file.write("Society:%s:%s\n" % (self.society.get(), society_rank))	
		
		char_file.write("==STATISTICS INFORMATION==\n")	
		for stat in statistics:
			val = self.statistics_list[stat].values_by_level[0].get()
			if( val == "" ):
				val = 0
			char_file.write("%s:%s\n" % (self.statistics_list[stat].name, val))
			
		char_file.write("==GUILD SKILLS RANKS==\n")			
		for i in range(6):
			if( self.profession.guild_skills[i] == "NONE" ):
				continue
			ranks = self.guild_skills_ranks[i].get()
			if( ranks == "" ):
				ranks = 0
			char_file.write("%s:%s\n" % (self.profession.guild_skills[i], ranks))							
			
		if self.build_skills_list:
			char_file.write("==SKILLS BUILD LIST==\n")	
			for skill in self.build_skills_list:			
				char_file.write("%s:%s:%s:%s:%s\n" % (skill.name.get(), skill.hide.get(), skill.goal.get(), skill.slvl.get(), skill.tlvl.get()) )
				
		if self.build_combat_maneuvers_list:
			char_file.write("==COMBAT MANEUVERS BUILD LIST==\n")	
			for man in self.build_combat_maneuvers_list:			
				char_file.write("%s:%s:%s:%s:%s\n" % (man.name.get(), man.hide.get(), man.goal.get(), man.slvl.get(), man.tlvl.get()) )		
			
		if self.build_shield_maneuvers_list:
			char_file.write("==SHIELD MANEUVERS BUILD LIST==\n")	
			for man in self.build_shield_maneuvers_list:			
				char_file.write("%s:%s:%s:%s:%s\n" % (man.name.get(), man.hide.get(), man.goal.get(), man.slvl.get(), man.tlvl.get()) )
			
		if self.build_armor_maneuvers_list:
			char_file.write("==ARMOR MANEUVERS BUILD LIST==\n")	
			for man in self.build_armor_maneuvers_list:			
				char_file.write("%s:%s:%s:%s:%s\n" % (man.name.get(), man.hide.get(), man.goal.get(), man.slvl.get(), man.tlvl.get()) )

				
		if self.postcap_build_skills_list:
			char_file.write("==SKILLS POSTCAP BUILD LIST==\n")	
			for skill in self.postcap_build_skills_list:			
				char_file.write("%s:%s:%s\n" % (skill.name.get(), skill.hide.get(), skill.goal.get()) )	
				
		if self.postcap_build_combat_maneuvers_list:
			char_file.write("==COMBAT MANEUVERS POSTCAP BUILD LIST==\n")	
			for man in self.postcap_build_combat_maneuvers_list:			
				char_file.write("%s:%s:%s\n" % (man.name.get(), man.hide.get(), man.goal.get()) )		
			
		if self.postcap_build_shield_maneuvers_list:
			char_file.write("==SHIELD MANEUVERS POSTCAP BUILD LIST==\n")	
			for man in self.postcap_build_shield_maneuvers_list:			
				char_file.write("%s:%s:%s\n" % (man.name.get(), man.hide.get(), man.goal.get()) )
			
		if self.postcap_build_armor_maneuvers_list:
			char_file.write("==ARMOR MANEUVERS POSTCAP BUILD LIST==\n")	
			for man in self.postcap_build_armor_maneuvers_list:			
				char_file.write("%s:%s:%s\n" % (man.name.get(), man.hide.get(), man.goal.get()) )				

				
		if self.loadout_gear_build_list:
			char_file.write("==GEAR BUILD LIST==\n")	
			for gear in self.loadout_gear_build_list:			
				char_file.write("%s:%s:%s:%s:%s\n" % (gear.name.get(), gear.dialog_type, gear.skills, gear.enchantment, gear.weight) )	
		
		if self.loadout_effects_build_list:
			char_file.write("==EFFECTS BUILD LIST==\n")	
			for effect in self.loadout_effects_build_list:		
				scaling_info = ":"
				if len(effect.scaling_arr) > 0:
					for key, value in effect.scaling_arr.items():
						scaling_info += "%s=%s:" % (key, value)
					scaling_info = scaling_info[:-1]
				else:
					scaling_info = ":NONE"
				char_file.write("%s:%s%s\n" % (effect.name.get(), effect.hide.get(), scaling_info) )	
						
				
	# Calculate the PTP, MTP, Health, Mana, Stamina, Spirit over 100 levels. This is called after the statistics growth method has been called.
	def Update_Statistics(self):	
		global panels
	
		# Calculate everything using the 10 statistic values for this level.
		for i in range(101):
			STR = float(0) if self.statistics_list["Strength"].values_by_level[i].get() == "" else float(self.statistics_list["Strength"].values_by_level[i].get())
			CON = float(0) if self.statistics_list["Constitution"].values_by_level[i].get() == "" else float(self.statistics_list["Constitution"].values_by_level[i].get())
			DEX = float(0) if self.statistics_list["Dexterity"].values_by_level[i].get() == "" else float(self.statistics_list["Dexterity"].values_by_level[i].get())
			AGI = float(0) if self.statistics_list["Agility"].values_by_level[i].get() == "" else float(self.statistics_list["Agility"].values_by_level[i].get())
			DIS = float(0) if self.statistics_list["Discipline"].values_by_level[i].get() == "" else float(self.statistics_list["Discipline"].values_by_level[i].get())
			AUR = float(0) if self.statistics_list["Aura"].values_by_level[i].get() == "" else float(self.statistics_list["Aura"].values_by_level[i].get())
			LOG = float(0) if self.statistics_list["Logic"].values_by_level[i].get() == "" else float(self.statistics_list["Logic"].values_by_level[i].get())
			INT = float(0) if self.statistics_list["Intuition"].values_by_level[i].get() == "" else float(self.statistics_list["Intuition"].values_by_level[i].get())
			WIS = float(0) if self.statistics_list["Wisdom"].values_by_level[i].get() == "" else float(self.statistics_list["Wisdom"].values_by_level[i].get())
			INF = float(0) if self.statistics_list["Influence"].values_by_level[i].get() == "" else float(self.statistics_list["Influence"].values_by_level[i].get())
			
			# The sum of the 10 statistics is the statistic total for this level.
			self.statistic_totals_by_level[i].set(int(STR+CON+DEX+AGI+DIS+AUR+LOG+INT+WIS+INF))			
			
			# Calculate PTP/MTP. This formula is (STR + CON + DEX + AGI) + (AUR + DIS) / 2  for PTP and (LOG + INT + WIS + INF) + (AUR + DIS) / 2 for MTP. 
			# Prime statistics count as double for these calculations
			PTP_sum = (AUR * self.Is_Prime_Stat("Aura") + DIS * self.Is_Prime_Stat("Discipline")) / 2
			PTP_sum = (PTP_sum + STR * self.Is_Prime_Stat("Strength") + CON * self.Is_Prime_Stat("Constitution") + DEX * self.Is_Prime_Stat("Dexterity") + AGI * self.Is_Prime_Stat("Agility")) / 20 
			PTP_sum += 25
						
			MTP_sum = (AUR * self.Is_Prime_Stat("Aura") + DIS * self.Is_Prime_Stat("Discipline")) / 2
			MTP_sum = (MTP_sum + LOG * self.Is_Prime_Stat("Logic") + INT * self.Is_Prime_Stat("Intuition") + WIS * self.Is_Prime_Stat("Wisdom") + INF * self.Is_Prime_Stat("Influence")) / 20 
			MTP_sum += 25
							
			self.ptp_by_level[i].set(math.floor(PTP_sum))
			self.mtp_by_level[i].set(math.floor(MTP_sum))	
						
			# Only use the statistic values given at level 0 to determine starting mana			
			if i == 0:
				self.total_ptp_by_level[0].set(math.floor(PTP_sum))
				self.total_mtp_by_level[0].set(math.floor(MTP_sum))		
				
				self.ptp_base.set(PTP_sum)
				self.mtp_base.set(MTP_sum)				
			# Beyond level 0, sum the total PTP/MTP and color the panels if the value for last level is less than the value for this level.
			else:
				self.total_ptp_by_level[i].set( math.floor(PTP_sum) + self.total_ptp_by_level[i-1].get() )
				self.total_mtp_by_level[i].set( math.floor(MTP_sum) + self.total_mtp_by_level[i-1].get() )	
				
				if self.ptp_by_level[i].get() > self.ptp_by_level[i-1].get():
					panels['Statistics'].ptp_bgs[i] = "#00FF00"
				else:
					panels['Statistics'].ptp_bgs[i] = "lightgrey"
					
				if self.mtp_by_level[i].get() > self.mtp_by_level[i-1].get():
					panels['Statistics'].mtp_bgs[i] = "#00FF00"
				else:
					panels['Statistics'].mtp_bgs[i] = "lightgrey"
				
			# Calculate the resources values for this level
			self.Update_Resources(i)


		# Sets the background colors of the cells.	
		i = 0
		for cell in panels['Statistics'].ptp_frame.winfo_children():	
			cell["bg"] = panels['Statistics'].ptp_bgs[i]
			i += 1
	
		i = 0
		for cell in panels['Statistics'].mtp_frame.winfo_children():
			cell["bg"] = panels['Statistics'].mtp_bgs[i]
			i += 1	

			
	# Used to calculate the character's health, mana, stamina, and spirit from level 0 to 100.
	# Called by Update Statistics method but also called manually by the Skills and Maneuver panels to update without calling Update Statistics directory
	def Update_Resources(self, level):
		i = level
		postcap_mode = 0		
		
		# Handle Postcap calculations later
		if level > 100:
			i == 100
			postcap_mode = 1	
			
		STR = float(0) if self.statistics_list["Strength"].values_by_level[i].get() == "" else float(self.statistics_list["Strength"].values_by_level[i].get())
		CON = float(0) if self.statistics_list["Constitution"].values_by_level[i].get() == "" else float(self.statistics_list["Constitution"].values_by_level[i].get())
#		DEX = float(0) if self.statistics_list["Dexterity"].values_by_level[i].get() == "" else float(self.statistics_list["Dexterity"].values_by_level[i].get())
		AGI = float(0) if self.statistics_list["Agility"].values_by_level[i].get() == "" else float(self.statistics_list["Agility"].values_by_level[i].get())
		DIS = float(0) if self.statistics_list["Discipline"].values_by_level[i].get() == "" else float(self.statistics_list["Discipline"].values_by_level[i].get())
		AUR = float(0) if self.statistics_list["Aura"].values_by_level[i].get() == "" else float(self.statistics_list["Aura"].values_by_level[i].get())
#		LOG = float(0) if self.statistics_list["Logic"].values_by_level[i].get() == "" else float(self.statistics_list["Logic"].values_by_level[i].get())
#		INT = float(0) if self.statistics_list["Intuition"].values_by_level[i].get() == "" else float(self.statistics_list["Intuition"].values_by_level[i].get())
#		WIS = float(0) if self.statistics_list["Wisdom"].values_by_level[i].get() == "" else float(self.statistics_list["Wisdom"].values_by_level[i].get())
#		INF = float(0) if self.statistics_list["Influence"].values_by_level[i].get() == "" else float(self.statistics_list["Influence"].values_by_level[i].get())
			
		
		# Health calculation. Combines stats and Physical Training ranks
		health_gain_rate = int(self.race.health_gain_rate)
		PF_ranks = 0 if not "Physical Fitness" in self.skills_list else	self.skills_list["Physical Fitness"].total_ranks_by_level[i].get() 
		H_str = float(0) if self.statistics_list["Strength"].values_by_level[0].get() == "" else float(self.statistics_list["Strength"].values_by_level[0].get())
		H_con = float(0) if self.statistics_list["Constitution"].values_by_level[0].get() == "" else float(self.statistics_list["Constitution"].values_by_level[0].get())
		base_con = math.floor((H_str + H_con) / 10)
		con_bonus = float(0) if self.statistics_list["Constitution"].values_by_level[i].get() == "" else float(self.statistics_list["Constitution"].values_by_level[i].get())
		con_bonus = int(math.floor((con_bonus - 50) / 2 + self.racial_stat_bonus["Constitution"].get()))
		self.health_by_level[i].set(max(0, min(base_con +  PF_ranks * (health_gain_rate + math.floor(con_bonus /10)), self.race.max_health + con_bonus)))
	
		# Mana calculation. Just factor in the Harness power ranks at this level
		M_bonus1 = self.statistics_list[self.profession.mana_statistics[0]].values_by_level[0].get()
		M_bonus2 = self.statistics_list[self.profession.mana_statistics[1]].values_by_level[0].get()
		M_bonus1 = 0 if M_bonus1 == "" else int(M_bonus1)
		M_bonus2 = 0 if M_bonus2 == "" else int(M_bonus2)
		M_bonus1 = (M_bonus1 - 50) / 2 + self.racial_stat_bonus[self.profession.mana_statistics[0]].get()
		M_bonus2 = (M_bonus2 - 50) / 2 + self.racial_stat_bonus[self.profession.mana_statistics[1]].get()	
		HP_ranks = 0 if not "Harness Power" in self.skills_list else self.skills_list["Harness Power"].total_ranks_by_level[i].get() 		
		HP_mana = i*3 + HP_ranks-i if HP_ranks > i else HP_ranks*3
		self.mana_by_level[i].set(max(int(math.floor(M_bonus1 + M_bonus2) / 4), 0) + HP_mana)

		# Stamina calculation.
		PF_bonus = 0 if not "Physical Fitness" in self.skills_list else	self.skills_list["Physical Fitness"].bonus_by_level[i].get() 
		S_str = (STR - 50) / 2 + self.racial_stat_bonus["Strength"].get()
		S_con = (CON - 50) / 2 + self.racial_stat_bonus["Constitution"].get()
		S_agi = (AGI - 50) / 2 + self.racial_stat_bonus["Agility"].get()
		S_dis = (DIS - 50) / 2 + self.racial_stat_bonus["Discipline"].get()
		
		self.stamina_by_level[i].set(int(max(S_con + (S_str + S_agi + S_dis) / 3 + math.floor(PF_bonus / 3), 0)))
				
		# Spirit calculation
		spirit = math.floor(AUR/10)
		if (AUR - (spirit * 10)) >= 5:
			spirit += 1
		self.spirit_by_level[i].set(int(round(spirit))) 		
		
		
	# Small function that determines if the profession considers stat a prime statistic. The multiplier for determining TP is returned. 2 if yes, 1 if no
	def Is_Prime_Stat(self, stat):
		try:
			self.profession.prime_statistics.index(stat)
			return 2
		except ValueError:
			return 1		
	
	
	# This method is called when the Profession is changed. It makes a database call using the new profession and gets the new skill costs and max ranks for that skill.
	def Update_Skills(self):
		global db_cur, db_con, skill_names, panels, Skill
		skill_panel = panels['Skills']
		postcap_panel = panels['Post Cap']
		
		name = self.profession.name.lower()
		db_cur.execute("SELECT name, %s_ptp, %s_mtp, %s_max_ranks FROM Skills" % (name, name, name))		
		db_con.commit()		
		data = db_cur.fetchall()	
			
		# Update all the skills with new costs
		for skill in data:
			character.skills_list[skill[0]].Update_Skill_Information(skill)		
				
		# Reset the scrolling on the schedule and build frames		
		skill_panel.dialog_menu_skill_names['menu'].delete(0, "end")
		skill_panel.ML_Frame.yview("moveto", 0, "units")
		skill_panel.MR_Frame.yview("moveto", 0, "units")	
		postcap_panel.dialog_skill_names_menu['menu'].delete(0, "end")
		postcap_panel.ML_Frame.yview("moveto", 0, "units")
		postcap_panel.MR_Frame.yview("moveto", 0, "units")
		
		# Remove all the skills 
		for key, row in self.skills_list.items():
			if row.SkP_schedule_row == "" or row.PcP_schedule_row == "":
				break
			row.SkP_schedule_row.grid_remove()
			row.PcP_schedule_row.grid_remove()
		
		# Add all the skills from the skills_list to the schedule frame that the profession can use (ie: spell research)
		i = 0
		for name in skill_names:				
			if self.skills_list[name].active_skill:
				skill_panel.dialog_menu_skill_names['menu'].add_command(label=name, command=lambda s=name: skill_panel.Skills_Menu_Onchange(s))
				postcap_panel.dialog_skill_names_menu['menu'].add_command(label=name, command=lambda s=name: postcap_panel.Dialog_Menu_Onchange(s))
				self.skills_list[name].SkP_schedule_row.grid(row=i, column=0)
				i += 1
			
		# Reset the skills panel and make sure the schedule frame looks right	
		skill_panel.level_counter.setvalue(0)
		skill_panel.ML_Frame.yview("moveto", 0, "units")
		skill_panel.MR_Frame.yview("moveto", 0, "units")
		skill_panel.Update_Schedule_Frames()
		
		postcap_panel.PcP_radio_var.set(1)
		postcap_panel.goal_mode.set("Skills")
		postcap_panel.experience_counter.setvalue(7572500)
		postcap_panel.ML_Frame.yview("moveto", 0, "units")
		postcap_panel.MR_Frame.yview("moveto", 0, "units")
		postcap_panel.Update_Schedule_Frames()

		
	# Because Skills with the same subgroup need to be taken into account when calculating cost and max ranks, this method will determine how much TP to refund for each subgroup.
	def Calculate_Subskill_Regained_TP(self, level, subskill_group):
		global skill_names		
		
		# Abort if there is no subgroup or the level is not 1-100
		if subskill_group == "NONE" or level < 1 or level > 100:
			return (0,0)

		pcost = 0; mcost = 0; tranks = 0; prev_tranks = 0; prev_pcost = 0; prev_mcost = 0; 
		skill_ptp = 0; skill_mtp = 0		
		
		# Get the total ranks taken this level and the previous level for all the skills 
		for s in skill_names:
			skill = self.skills_list[s]
			if skill.subskill_group == subskill_group and skill.active_skill == 1:			
				skill_ptp = skill.ptp_cost
				skill_mtp = skill.mtp_cost
				prev_tranks += skill.total_ranks_by_level[level-1].get()
				tranks += skill.total_ranks_by_level[level].get()
				
		# No ranks were taken? Abort method.
		if tranks == 0:
			return (0,0)
				
		# Otherwise calculate the cost for both levels and return the different or 0 if it is a negative amount
		triple_train = max(0, tranks - 2 * (level + 1))
		double_train = max(0, tranks - triple_train - (level + 1))
		single_train = max(0, tranks - triple_train - double_train)		
		prev_triple_train = max(0, prev_tranks - 2 * (level))
		prev_double_train = max(0, prev_tranks - prev_triple_train - (level))
		prev_single_train = max(0, prev_tranks - prev_triple_train - prev_double_train)		
						
		pcost = skill_ptp * single_train  +  2 * skill_ptp * double_train  +  4 * skill_ptp * triple_train
		mcost = skill_mtp * single_train  +  2 * skill_mtp * double_train  +  4 * skill_mtp * triple_train	
		prev_pcost = skill_ptp * prev_single_train  +  2 * skill_ptp * prev_double_train  +  4 * skill_ptp * prev_triple_train
		prev_mcost = skill_mtp * prev_single_train  +  2 * skill_mtp * prev_double_train  +  4 * skill_mtp * prev_triple_train	
				
		return ( max(0, prev_pcost - pcost), max(0, prev_mcost - mcost) )
			
	
	# Given a subskill group and a skill name, find all the skills that have that subskills EXCEPT for "skill name" and return the combined total ranks for those skills
	def Get_Total_Ranks_Of_Subskill(self, name, level, subskill_group):
		global skill_names
		total = 0
		
		if subskill_group == "NONE" or level < 0:
			return 0
		
		for s in skill_names:
			skill = self.skills_list[s]
			if s == name or skill.subskill_group != subskill_group:
				continue
				
			total += skill.total_ranks_by_level[level].get()
			
		return total


	# Given a subskill group and a skill name, find all the skills that have that subskills EXCEPT for "skill name" and return the combined total ranks for those skills for precap levels and up to and including the given interval
	def Get_Total_Postcap_Ranks_Of_Subskill(self, name, interval, subskill_group):
		global skill_names
		total = 0
		exp = 0
		
		if subskill_group == "NONE":
			return 0
				
		for s in skill_names:
			skill = self.skills_list[s]
			if s == name or skill.subskill_group != subskill_group:
				continue
				
			total += skill.total_ranks_by_level[100].get()
			
			if len(skill.postcap_exp_intervals) == 0:
				continue
				
			if interval in skill.postcap_exp_intervals:
				exp = interval
			else:
				exp = self.Get_Last_Training_Interval(interval-1, "skills", s)
				if exp == 0:
					continue
			 
			total += int(skill.postcap_total_ranks_at_interval[exp])
		return total
		
		
	# This method is called when the Profession is changed. Using the new profession, it determines what maneuver that profession can learn and adds them the manevuer lists.
	def Update_Maneuvers(self):
		global combat_maneuver_names, shield_maneuver_names, armor_maneuver_names, panels
		man_panel = panels['Maneuvers']		
		postcap_panel = panels['Post Cap']		
		prof = self.profession.name
		
		# Clear the maneuvers before adding the new maneuvers
		man_panel.dialog_combat_names_menu['menu'].delete(0, "end")
		man_panel.dialog_armor_names_menu['menu'].delete(0, "end")
		man_panel.dialog_shield_names_menu['menu'].delete(0, "end")
		postcap_panel.dialog_combat_names_menu['menu'].delete(0, "end")
		postcap_panel.dialog_armor_names_menu['menu'].delete(0, "end")
		postcap_panel.dialog_shield_names_menu['menu'].delete(0, "end")
		
		if man_panel.armor_menu_size > 1:
			man_panel.add_armor_order_menu['menu'].delete(1, "end")
			if man_panel.armor_menu_size > 2:
				man_panel.edit_armor_order_menu['menu'].delete(1, "end")
			man_panel.armor_menu_size = 1	
		if man_panel.combat_menu_size > 1:
			man_panel.add_combat_order_menu['menu'].delete(1, "end")
			if man_panel.combat_menu_size > 2:
				man_panel.edit_combat_order_menu['menu'].delete(1, "end")
			man_panel.combat_menu_size = 1	
		if man_panel.shield_menu_size > 1:		
			man_panel.add_shield_order_menu['menu'].delete(1, "end")
			if man_panel.shield_menu_size > 1:		
				man_panel.edit_shield_order_menu['menu'].delete(1, "end")
			man_panel.shield_menu_size = 1			
		
		if postcap_panel.armor_menu_size > 1:
			postcap_panel.add_armor_order_menu['menu'].delete(1, "end")
			if postcap_panel.armor_menu_size > 2:
				postcap_panel.edit_armor_order_menu['menu'].delete(1, "end")
			postcap_panel.armor_menu_size = 1	
		if postcap_panel.combat_menu_size > 1:
			postcap_panel.add_combat_order_menu['menu'].delete(1, "end")
			if postcap_panel.combat_menu_size > 2:
				postcap_panel.edit_combat_order_menu['menu'].delete(1, "end")
			postcap_panel.combat_menu_size = 1	
		if postcap_panel.shield_menu_size > 1:		
			postcap_panel.add_shield_order_menu['menu'].delete(1, "end")
			if postcap_panel.shield_menu_size > 1:		
				postcap_panel.edit_shield_order_menu['menu'].delete(1, "end")
			postcap_panel.shield_menu_size = 1			
		
		postcap_panel.man_select_menu['menu'].delete(1, "end")	
		postcap_panel.ML_Frame.yview("moveto", 0, "units")
		postcap_panel.MR_Frame.yview("moveto", 0, "units")	
		
		man_panel.man_select_menu['menu'].delete(0, "end")	
		man_panel.ML_Frame.yview("moveto", 0, "units")
		man_panel.MR_Frame.yview("moveto", 0, "units")		

		# Remove all Build Rows from the build frame
		for man in self.build_combat_maneuvers_list:
			man.ManP_Build_Row.grid_remove()
		for man in self.build_shield_maneuvers_list:	
			man.ManP_Build_Row.grid_remove()
		for man in self.build_armor_maneuvers_list:	
			man.ManP_Build_Row.grid_remove()
		
		# Clear the build lists
		self.build_combat_maneuvers_list = []
		self.build_shield_maneuvers_list = []
		self.build_armor_maneuvers_list = []
		
		# Add each maneuver to the appropriate list if it can learn that manevuer.
		for name in combat_maneuver_names:	
			man = self.combat_maneuvers_list[name]
			man.Set_To_Default()	
			if man.availability[prof]:
				man_panel.dialog_combat_names_menu['menu'].add_command(label=name, command=lambda s=name: man_panel.Dialog_Menu_Onchange(s))
				postcap_panel.dialog_combat_names_menu['menu'].add_command(label=name, command=lambda s=name: postcap_panel.Dialog_Menu_Onchange(s))
		for name in shield_maneuver_names:
			man = self.shield_maneuvers_list[name]
			man.Set_To_Default()	
			if man.availability[prof]:
				man_panel.dialog_shield_names_menu['menu'].add_command(label=name, command=lambda s=name: man_panel.Dialog_Menu_Onchange(s))
				postcap_panel.dialog_shield_names_menu['menu'].add_command(label=name, command=lambda s=name: postcap_panel.Dialog_Menu_Onchange(s))
		for name in armor_maneuver_names:
			man = self.armor_maneuvers_list[name]
			man.Set_To_Default()	
			if man.availability[prof]:
				man_panel.dialog_armor_names_menu['menu'].add_command(label=name, command=lambda s=name: man_panel.Dialog_Menu_Onchange(s))
				postcap_panel.dialog_armor_names_menu['menu'].add_command(label=name, command=lambda s=name: postcap_panel.Dialog_Menu_Onchange(s))
						
		# Remove/Add the Shield and Armor options to the maneuver style menue and show the Shield and Armor footers 
		if prof == "Warrior" or prof == "Rogue" or prof == "Paladin":
			man_panel.sfooter_shield_row.grid(row=2, column=0, padx="1")
			man_panel.sfooter_armor_row.grid(row=3, column=0, padx="1")
			man_panel.man_select_menu["menu"].insert_command("end", label="Combat", command=lambda s="Combat": man_panel.Maneuver_Style_Onchange(s))
			man_panel.man_select_menu["menu"].insert_command("end", label="Shield", command=lambda s="Shield": man_panel.Maneuver_Style_Onchange(s))
			man_panel.man_select_menu["menu"].insert_command("end", label="Armor", command=lambda s="Armor": man_panel.Maneuver_Style_Onchange(s))
			postcap_panel.man_select_menu["menu"].insert_command("end", label="Combat", command=lambda s="Combat": postcap_panel.PostCap_Style_Onchange(s))
			postcap_panel.man_select_menu["menu"].insert_command("end", label="Shield", command=lambda s="Shield": postcap_panel.PostCap_Style_Onchange(s))
			postcap_panel.man_select_menu["menu"].insert_command("end", label="Armor", command=lambda s="Armor": postcap_panel.PostCap_Style_Onchange(s))
		else:		
			man_panel.man_select_menu["menu"].insert_command("end", label="Combat", command=lambda s="Combat": man_panel.Maneuver_Style_Onchange(s))
			postcap_panel.man_select_menu["menu"].insert_command("end", label="Combat", command=lambda s="Combat": postcap_panel.PostCap_Style_Onchange(s))
			man_panel.sfooter_shield_row.grid_remove()
			man_panel.sfooter_armor_row.grid_remove()		
			
		# Finally reset the maneuvers and post cap panel
		man_panel.ManP_radio_var.set(1)
		man_panel.level_counter.setvalue(0)		
		man_panel.maneuver_mode.set("")
		man_panel.Maneuver_Style_Onchange("Combat")	
		postcap_panel.PcP_radio_var.set(1)
		postcap_panel.experience_counter.setvalue(7572500)	
		postcap_panel.goal_mode.set("Skills")	
		postcap_panel.PostCap_Style_Onchange("Skills")	

	
	# Checks to see if the character meets the prerequisites to train in a maneuver at a given level.
	def Meets_Maneuver_Prerequisites(self, level, name, type):
		if type == "combat":
			man = self.combat_maneuvers_list[name]
		elif type == "shield":
			man = self.shield_maneuvers_list[name]
		elif type == "armor":		
			man = self.armor_maneuvers_list[name]
			
		requirements = man.prerequisites
		postcap_mode = 0
		or_valid = 0
		and_valid = 0
		true_valid = 1
		
		if level > 100:
			level = 100
			postcap_mode = 1
		
		if requirements == "NONE":
			return True
			
		# Maneuver prerequisites are stored in the format in the database TYPE:NAME:RANKS
		# TYPE is what kind of prerequisite it is. Skill, CM, SM are the values 
		# NAME is the name of Skill, Combat Maneuver, Shield Maneuver.
		# RANKS is a number indicating how many ranks the character must have to gain a rank in the maneuver
		# Each prerequisite can be followed by another prerequisite with the seperator "|" for OR or "&" for AND
		and_parts = requirements.split("&")
		for apart in and_parts:
			or_parts = apart.split("|")
			or_valid = 0
			for opart in or_parts:
				semi_parts = opart.split(":")
				if semi_parts[0] == "CM":
					val = self.combat_maneuvers_list[semi_parts[1]].total_ranks_by_level[level].get()
					if postcap_mode:
						man = self.combat_maneuvers_list[semi_parts[1]]
						if len(man.postcap_exp_intervals) > 1:
							val += man.postcap_total_ranks_at_interval[man.postcap_exp_intervals[-1]]
				elif semi_parts[0] == "SM":
					val = self.shield_maneuvers_list[semi_parts[1]].total_ranks_by_level[level].get()
					if postcap_mode:
						man = self.shield_maneuvers_list[semi_parts[1]]
						if len(man.postcap_exp_intervals) > 1:
							val += man.postcap_total_ranks_at_interval[man.postcap_exp_intervals[-1]]
				elif semi_parts[0] == "Skill":
					val = self.skills_list[semi_parts[1]].total_ranks_by_level[level].get()		
					if postcap_mode:
						man = self.skills_list[semi_parts[1]]
						if len(man.postcap_exp_intervals) > 1:
							val += man.postcap_total_ranks_at_interval[man.postcap_exp_intervals[-1]]	
				elif semi_parts[0] == "GS":
					if not semi_parts[1] in self.profession.guild_skills:
						val = 0
					else:						
						val = self.guild_skills_ranks[self.profession.guild_skills.index(semi_parts[1])].get()
						if val == "":
							val = 0
						val = int(val)
			
				if val >= int(semi_parts[2]):
					or_valid = 1
					break
			
			if or_valid == 0:
				true_valid = 0
				break
		
		if true_valid == 1:
			return True
		else:
			return False

			
	# Used by the Post Cap panel to find the nearest exp interval that the character has trained in a skill, combat, shield, armor maneuver	
	def Get_Last_Training_Interval(self, exp, type, subtype):	
		global character
		if exp % 2500 != 0:
			exp -= exp % 2500
		
		intervals = []
		
		if type == "skills":
			if subtype == "":
				search_list = self.postcap_skill_training_by_interval
			else:
				search_list = character.skills_list[subtype].postcap_ranks_at_interval
		elif type == "combat":
			if subtype == "":
				search_list = self.postcap_combat_training_by_interval
			else:
				search_list = character.combat_maneuvers_list[subtype].postcap_ranks_at_interval
		elif type == "shield":
			if subtype == "":
				search_list = self.postcap_shield_training_by_interval
			else:
				search_list = character.shield_maneuvers_list[subtype].postcap_ranks_at_interval
		elif type == "armor":
			if subtype == "":
				search_list = self.postcap_armor_training_by_interval
			else:
				search_list = character.armor_maneuvers_list[subtype].postcap_ranks_at_interval
				
		
		for key in search_list.keys():
			intervals.append(key)
		
#		if exp < 7572500 or len(intervals) == 0:
#			return 7572500		
		if len(intervals) == 0:
			return 0		
		elif exp in search_list:
			return exp
			
		# If it ...
		if exp < intervals[0]:
			return intervals[0]
		elif exp > intervals[-1]:
			return intervals[-1]
		
		prev = intervals[0]
		for val in intervals:
			if prev == val or exp > val:
				prev = val	
			else:
				return prev 
			
			
# The Race object hold all the information for the character's current race. 	
class Race:
	def __init__(self, arr):	
		self.name = arr['name']
		self.manauever_bonus = arr['manauever_bonus']
		self.max_health = arr['max_health']
		self.health_regen = arr['health_regen']
		self.health_gain_rate = arr['health_gain_rate']
		self.spirit_regen_tier = arr['spirit_regen_tier']
		self.decay_timer = arr['decay_timer']
		self.encumbrance_factor = arr['encumbrance_factor']
		self.weight_factor = arr['weight_factor']
		self.elemental_td = arr['elemental_td']
		self.spiritual_td = arr['spiritual_td']
		self.mental_td = arr['mental_td']
		self.sorc_td = arr['sorc_td']
		self.poison_td = arr['poison_td']
		self.disease_td = arr['disease_td']
		self.statistic_bonus = { "Strength": arr['strength_bonus'], "Constitution": arr['constitution_bonus'], "Dexterity": arr['dexterity_bonus'], "Agility": arr['agility_bonus'], "Discipline": arr['discipline_bonus'], "Aura": arr['aura_bonus'], "Logic": arr['logic_bonus'], "Intuition": arr['intuition_bonus'], "Wisdom": arr['wisdom_bonus'], "Influence": arr['influence_bonus'] }
		self.statistic_adj = { "Strength": arr['strength_adj'], "Constitution": arr['constitution_adj'], "Dexterity": arr['dexterity_adj'], "Agility": arr['agility_adj'], "Discipline": arr['discipline_adj'], "Aura": arr['aura_adj'], "Logic": arr['logic_adj'], "Intuition": arr['intuition_adj'], "Wisdom": arr['wisdom_adj'], "Influence": arr['influence_adj'] }
			

# The Profession object hold all the information for the character's current profession. This does not include skill costs or max ranks
class Profession:
	def __init__(self, arr):
		self.name = arr['name']
		self.type = arr['type']
		self.prime_statistics = [ arr['prime_statistics1'], arr['prime_statistics2'] ]
		self.mana_statistics = [ arr['mana_statistic1'], arr['mana_statistic2'] ]
		self.spell_circles = [ arr['spell_circle1'], arr['spell_circle2'] ]
		if arr['spell_circle3'] != "NONE":
			self.spell_circles.append(arr['spell_circle3'])			
		self.guild_skills = [ arr['guild_skill1'], arr['guild_skill2'], arr['guild_skill3'], arr['guild_skill4'], arr['guild_skill5'], arr['guild_skill6'] ]		
		self.statistic_growth = { "Strength": arr['strength_growth'], "Constitution": arr['constitution_growth'], "Dexterity": arr['dexterity_growth'], "Agility": arr['agility_growth'], "Discipline": arr['discipline_growth'], "Aura": arr['aura_growth'], "Logic": arr['logic_growth'], "Intuition": arr['intuition_growth'], "Wisdom": arr['wisdom_growth'], "Influence": arr['influence_growth'] }
			

# Statistic objects are responsible for mantaining the growth for their specific statistic.
# They are also responsible for the growth and statistics rows in the Statistics Panel. Including the values, bonuses, the Entry box and colors.
class Statistic:
	def __init__(self, parent, name):
		self.name = name
		self.parent = parent                   # Character object
		self.adj = 0;
		self.values_by_level = [tkinter.StringVar() for i in range(101)]
		self.bonuses_by_level = [tkinter.IntVar() for i in range(101)]
		self.values_bgs = ["lightgray" for i in range(101)]
		self.bonuses_bgs = ["lightgray" for i in range(101)]
		self.StP_display_values = [tkinter.StringVar() for i in range(101)]
		self.StP_display_bgs = ["lightgray" for i in range(101)]
		self.StP_statistic_row = ""
		self.StP_growth_row = ""
		self.entrybox = ""
		self.display_label = ""
		self.display_var = tkinter.StringVar()

		self.values_by_level[0].set("20")		
		self.display_var.set(self.name)

		
	# Returns the statistic to 20 and calculates it's growth
	def Set_To_Default(self):
		self.values_by_level[0].set("20")	
		self.Calculate_Growth()
		
		
	# Part of the Statistics panel, this Frame will show the statistic's name, bonus/penalty provided by race, growth index, and Entry Box to edit the starting statistic value.
	def Create_Statistic_Row_Frame(self, panel, stat):
		frame = tkinter.Frame(panel)
		var = self.parent.statistics_list[stat].values_by_level[0]
		mycmd = (root.register(self.Entrybox_Validate), '%d', '%S', '%s', '%P')
		var.trace_variable("w", self.Entrybox_On_Update)
		
		self.display_label = tkinter.Label(frame, width="20", anchor="w", bg="lightgray", textvar=self.display_var)
		tkinter.Label(frame, width="10", bg="lightgray", textvar=self.parent.racial_stat_bonus[stat]).grid(row=0, column=1, padx="1", pady="1")
		tkinter.Label(frame, width="10", bg="lightgray", textvar=self.parent.stat_adj[stat]).grid(row=0, column=2, padx="1", pady="1")
		self.entrybox = tkinter.Entry(frame, width="6", justify="center", validate="key", validatecommand=mycmd, textvariable=var)
		
		self.entrybox.bind("<Down>", self.Entrybox_On_Move)
		self.entrybox.bind("<Up>", self.Entrybox_On_Move)	
		self.display_label.grid(row=0, column=0, sticky="w", padx="1", pady="1")		
		self.entrybox.grid(row=0, column=3, padx="1")
						
		return frame

		
	# This frame show the growth of a statistic or the growth of a statistic's bonus. Depends on the setting in the Statistics Panel.
	def Create_Growth_Row_Frame(self, parent):
		frame = tkinter.Frame(parent)	
	
		for i in range(101):
			tkinter.Label(frame, width=6, bg=self.StP_display_bgs[i], textvar=self.StP_display_values[i]).grid(row=0, column=i, padx="1", pady="1")	
			
		return frame		
	
	
	# Places either the value or bonus for each level in the display values to be shown in the frame. It will also color the background of each frame.
	def Update_Growth_Frame(self):	
		global panels
		radio = panels['Statistics'].StP_radio_var.get()
		for i in range(101):			
			if radio == 2:			
				self.StP_display_values[i].set(self.bonuses_by_level[i].get())
				self.StP_display_bgs[i] = self.bonuses_bgs[i]	
			else:
				self.StP_display_values[i].set(self.values_by_level[i].get())
				self.StP_display_bgs[i] = self.values_bgs[i]
		
		i = 0		
		for cell in self.StP_growth_row.winfo_children():	
			cell["bg"] = self.StP_display_bgs[i]
			i += 1

			
	# Calculates the growth of the statistics and sets the value and bonus by level variables from 0-100. Also sets the cell background colors for when an increase happens
	def Calculate_Growth(self):		
		if self.StP_growth_row == "":           #ignore the call if the training frame has not been created yet
			return 0
			
		try:				
			S = int(self.values_by_level[0].get())	
		except ValueError:
			S = 0			
		
		R = self.adj
		GI = max(math.floor(S/R),1);
		prev_stat = S;
	  
		for i in range(101):
			if i > 0 and S < 100 and (i % GI) == 0:
				S += 1
				GI = max(math.floor(S/R),1);
				
			if i != 0:	
				self.values_by_level[i].set(S)	
				
			self.bonuses_by_level[i].set(int((S - 50) / 2) + self.parent.racial_stat_bonus[self.name].get())
									

			if i > 0 and self.bonuses_by_level[i].get() > self.bonuses_by_level[i-1].get():
				self.bonuses_bgs[i] = "#00FF00"
			else:
				self.bonuses_bgs[i] = "lightgray"									
									
			if S > prev_stat:
				self.values_bgs[i] = "#00FF00"
			else:
				self.values_bgs[i] = "lightgray"
				
			prev_stat = S

			
	# Makes sure that the character placed in the Entry box doesn't make the length greater than 3 and that the value is less than or equal to 100. False results prevent the edit from occuring.
	def Entrybox_Validate(self, d, S, s, P):		
	#	print("event %s" % ( d))
	#	print("%s was added/deleted to entry box. Was previously %s" % (S, s))
		if( d == "1"):
			if( (len(s) + len(S)) > 3 ):
				return False
			try:				
				if( float(P) <= 100 ):	
					return True
				else:
					return False
			except ValueError:
				return False
		
		return True
	
	
	# When something in the Entrybox changes, recalculate the statistic growth and update all the things related to statistics
	def Entrybox_On_Update(self, *args):
		self.Calculate_Growth()
		self.Update_Growth_Frame()
		self.parent.Update_Statistics()

		
	# This event files when any key is pressed while the Entrybox has focus. This method will allow a user to move up and down between Entryboxes using the Arrow keys
	def Entrybox_On_Move(self, event):
		global statistics
		new_stat = ""; found = 0
		
		if event.keysym == "Up":
			for stat in statistics:				
				if stat == self.name:
					break
				new_stat = stat
					
		elif event.keysym == "Down":
			for stat in statistics:
				if found == 1:
					new_stat = stat
					break
				elif stat == self.name:
					found = 1
			
		if new_stat == "":
			return
			
		self.parent.statistics_list[new_stat].entrybox.focus()
		self.parent.statistics_list[new_stat].entrybox.icursor("end")
		
	
	# Stat Important is a method that updates the display label for the statistic name with extra tags to indicate if the stat is a prime statistic and/or a mana statistic
	def Set_Stat_Importance(self, action):
		if action == "none":
			self.display_var.set(self.name)
		elif action == "prime":			
			self.display_var.set("%s    (P)" % self.name)
		elif action == "mana":
			self.display_var.set("%s     (M)" % self.name)
		elif action == "prime/mana":
			self.display_var.set("%s     (P,M)" % self.name)


# Each Skill object contains all the information about a skill as well as methods to update, reset, and train ranks in the skill
class Skill:
	def __init__(self, arr):
		self.name = arr[0]
		self.type = arr[1]
		self.subskill_group = arr[2]
		self.redux = arr[3]
		self.ptp_cost = ""
		self.mtp_cost = ""
		self.max_ranks = ""

		self.active_skill = 0
		self.calculated_subskill = 0
		self.cost = tkinter.StringVar()
		self.ranks = tkinter.IntVar()
		self.total_ranks = tkinter.IntVar()
		self.bonus = tkinter.IntVar()		
		self.sum_cost = tkinter.IntVar()		
		self.SkP_schedule_row = ""			
		self.postcap_cost = tkinter.StringVar()
		self.postcap_ranks = tkinter.IntVar()
		self.postcap_total_ranks = tkinter.IntVar()
		self.postcap_bonus = tkinter.IntVar()		
		self.postcap_sum_cost = tkinter.StringVar()			
		self.PcP_schedule_row = ""		
		
		self.ranks_by_level = [tkinter.IntVar() for i in range(101)]
		self.total_ranks_by_level = [tkinter.IntVar() for i in range(101)]
		self.bonus_by_level = [tkinter.IntVar() for i in range(101)]
		self.ptp_cost_at_level = [tkinter.IntVar() for i in range(101)]
		self.mtp_cost_at_level = [tkinter.IntVar() for i in range(101)]
		self.total_ptp_cost_at_level = [tkinter.IntVar() for i in range(101)]
		self.total_mtp_cost_at_level = [tkinter.IntVar() for i in range(101)]
		self.ptp_regained_at_level = [tkinter.IntVar() for i in range(101)]
		self.mtp_regained_at_level = [tkinter.IntVar() for i in range(101)]
		
		# Used by Postcap panel
		self.postcap_exp_intervals = []
		self.postcap_ranks_at_interval = collections.OrderedDict()
		self.postcap_total_ranks_at_interval = collections.OrderedDict()
		self.postcap_bonus_at_interval = collections.OrderedDict()
		self.postcap_cost_at_interval = collections.OrderedDict()		
			
		self.Set_To_Default()
		

	# Resets the Skill object for the Skills panel
	def Set_To_Default(self):
		for i in range(101):
			self.ranks_by_level[i].set(0)
			self.total_ranks_by_level[i].set(0)
			self.bonus_by_level[i].set(0)
			self.ptp_cost_at_level[i].set(0)
			self.mtp_cost_at_level[i].set(0)
			self.total_ptp_cost_at_level[i].set(0)
			self.total_mtp_cost_at_level[i].set(0)
			self.ptp_regained_at_level[i].set(0)
			self.mtp_regained_at_level[i].set(0)

			
	# Resets the Skill object for the Postcap panel	
	def Set_To_Default_Postcap(self):
		self.postcap_exp_intervals = []
		self.postcap_ranks_at_interval.clear()
		self.postcap_total_ranks_at_interval.clear()
		self.postcap_cost_at_interval.clear()		

			
	# When a new Profession is chosen, this method will be called for each Skill to change the costs and max ranks.
	# If the profession can use the skill, active_skill is set to 1 which lets it appear in the Add/Edit Dialog box and schedule array. In short, it lets the user train in it.
	def Update_Skill_Information(self, arr):
		self.name = arr[0]
		self.ptp_cost = arr[1]
		self.mtp_cost = arr[2]
		self.max_ranks = arr[3]
		
		if arr[3] > 0:
			self.active_skill = 1
		else:
			self.active_skill = 0
		
		self.Set_To_Default()

		
	# The schedule row shows the training for the current level in the skill, the cost of that training and the training and bonus for the total ranks the character has in the skill
	def Create_SkP_schedule_row(self, parent):		
		if self.SkP_schedule_row != "":
			return
			
		self.SkP_schedule_row = tkinter.Frame(parent)	
		self.SkP_schedule_row.bindtags("SkP_schedule")
		
		L1 = tkinter.Label(self.SkP_schedule_row, width="26", bg="lightgray", anchor="w", text=self.name)
		L1.grid(row=0, column=0, padx="1", pady="1")
		L1.bindtags("SkP_schedule")
		L2 = tkinter.Label(self.SkP_schedule_row, width="6", bg="lightgray", textvariable=self.ranks)	 
		L2.grid(row=0, column=1, padx="1", pady="1")	
		L2.bindtags("SkP_schedule")
		L3 = tkinter.Label(self.SkP_schedule_row, width="8", bg="lightgray", textvariable=self.cost) 		
		L3.grid(row=0, column=2, padx="1", pady="1")	
		L3.bindtags("SkP_schedule")
		L4 = tkinter.Label(self.SkP_schedule_row, width="10", bg="lightgray", textvariable=self.total_ranks)
		L4.bindtags("SkP_schedule")		
		L4.grid(row=0, column=3, padx="1", pady="1")	
		L5 = tkinter.Label(self.SkP_schedule_row, width="6", bg="lightgray", textvariable=self.bonus)	
		L5.grid(row=0, column=4, padx="1", pady="1")
		L5.bindtags("SkP_schedule")		
		L6 = tkinter.Label(self.SkP_schedule_row, width="10", bg="lightgray", textvariable=self.sum_cost)	
		L6.grid(row=0, column=5, padx="1", pady="1")
		L6.bindtags("SkP_schedule")		
	

	# The schedule row shows the training for the current level in the skill, the cost of that training and the training and bonus for the total ranks the character has in the skill
	def Create_PcP_schedule_row(self, parent):		
		if self.PcP_schedule_row != "":
			return
			
		self.PcP_schedule_row = tkinter.Frame(parent)	
		self.PcP_schedule_row.bindtags("PcP_schedule")
		
		L1 = tkinter.Label(self.PcP_schedule_row, width="25", bg="lightgray", anchor="w", text=self.name)
		L1.grid(row=0, column=0, padx="1", pady="1")
		L1.bindtags("PcP_schedule")
		L2 = tkinter.Label(self.PcP_schedule_row, width="4", bg="lightgray", textvariable=self.postcap_ranks)	 
		L2.grid(row=0, column=1, padx="1", pady="1")	
		L2.bindtags("PcP_schedule")
		L3 = tkinter.Label(self.PcP_schedule_row, width="7", bg="lightgray", textvariable=self.postcap_cost) 		
		L3.grid(row=0, column=2, padx="1", pady="1")	
		L3.bindtags("PcP_schedule")
		L4 = tkinter.Label(self.PcP_schedule_row, width="8", bg="lightgray", textvariable=self.postcap_total_ranks)
		L4.bindtags("PcP_schedule")		
		L4.grid(row=0, column=3, padx="1", pady="1")	
		L5 = tkinter.Label(self.PcP_schedule_row, width="4", bg="lightgray", textvariable=self.postcap_bonus)	
		L5.grid(row=0, column=4, padx="1", pady="1")
		L5.bindtags("PcP_schedule")		
		L6 = tkinter.Label(self.PcP_schedule_row, width="9", bg="lightgray", textvariable=self.postcap_sum_cost)	
		L6.grid(row=0, column=5, padx="1", pady="1")
		L6.bindtags("PcP_schedule")	

		
	# This method will calculate the cost of training "ranks" ranks in this skill at "level". This cost is based on the current level and the total number of ranks + subskill_ranks.
	# The cost is returned at the end of the method after the new ranks are added to the ranks_this_level and total_ranks_by_level variables.
	def Train_New_Ranks(self, level, subskill_ranks, ranks):
		pcost = 0	
		mcost = 0	
		pregain = 0
		mregain = 0
		tpcost = 0
		tmpcost = 0
		prev_total_ranks = self.total_ranks_by_level[level].get()	
		prev_ranks = self.ranks_by_level[level].get()	
		self.ranks_by_level[level].set(prev_ranks + ranks)	
		ranks_this_level = self.ranks_by_level[level].get()
		max = prev_total_ranks - prev_ranks
		
		# Calculate the PTP and MTP cost for training in the skill. Takes triple trains and double trains into consideration as well
		for x in range(1, ranks_this_level+1):
			if x + max + subskill_ranks > 2 * (level + 2):
				pcost += self.ptp_cost * 4
				mcost += self.mtp_cost * 4
			elif x + max + subskill_ranks > (level + 2):
				pcost += self.ptp_cost * 2
				mcost += self.mtp_cost * 2
			else:
				pcost += self.ptp_cost
				mcost += self.mtp_cost	
				
		self.ptp_cost_at_level[level].set(pcost)
		self.mtp_cost_at_level[level].set(mcost)	
		
		pcost = 0	
		mcost = 0
		# Set Total Ranks and Bonus for each level
		for i in range(level, 101):
			if i > level:
				ranks = self.ranks_by_level[i].get()					
						
			self.total_ranks_by_level[i].set(ranks + prev_total_ranks)			
			self.bonus_by_level[i].set(self.Get_Skill_Bonus(ranks + prev_total_ranks))
			prev_total_ranks = self.total_ranks_by_level[i].get()
			
			# This will calculate the cost a skill using all existing ranks relative to a specific level.
			if i == level or (self.total_ranks_by_level[i].get() > prev_total_ranks):				
				(tpcost, tmcost) = self.Get_Total_Skill_Cost(subskill_ranks, self.total_ranks_by_level[i].get(), i)					
				
			self.total_ptp_cost_at_level[i].set(tpcost)
			self.total_mtp_cost_at_level[i].set(tmcost)
			
				
	# A short method that takes the number of ranks and converts it's bonus counterpart
	def Get_Skill_Bonus(self, ranks):
		if ranks >= 50:
			return 100 + ranks	
		elif ranks >= 40:
			return (ranks - 40) + 140
		elif ranks >= 30:
			return 2 * (ranks - 30) + 120
		elif ranks >= 20:
			return 3 * (ranks - 20) + 90
		elif ranks >= 10:
			return 4 * (ranks - 10) + 50
		else:
			return ranks * 5
			
			
	# When the character gains a level, any skills above the level+1 are converted down a level. IE triple trains become double trains and double trains become single trains.
	# The result of this is a TP refund to the character for the shift down. This method will calculate out all the refunds from start to end
	def Calculate_TP_Regain(self, start, end):
		if start < 1 or end > 100:
			return			
				
		for i in range(start, end+1):		
			(total_ptp_cost, total_mtp_cost) = self.Get_Total_Skill_Cost(0, self.total_ranks_by_level[i-1].get(), i)		
#			print("PTP/MTP this cost at lvl %s: %s/%s" % ( i, max(0, total_ptp_cost), max(0, total_mtp_cost)))		
#			print("PTP/MTP last cost at lvl %s: %s/%s" % ( i-1, max(0, self.total_ptp_cost_at_level[i-1].get()), max(0, self.total_mtp_cost_at_level[i-1].get())))		
#			print("PTP/MTP total cost - cost from %s at lvl %s: %s/%s" % (self.name, i, max(0, self.total_ptp_cost_at_level[i-1].get() - total_ptp_cost), max(0, self.total_mtp_cost_at_level[i-1].get() - total_mtp_cost)))	
			
			
			if self.total_ptp_cost_at_level[i].get() != total_ptp_cost:
				self.total_ptp_cost_at_level[i].set(total_ptp_cost)
			
			if self.total_mtp_cost_at_level[i].get() != total_mtp_cost:
				self.total_mtp_cost_at_level[i].set(total_mtp_cost)
				

			self.ptp_regained_at_level[i].set(max(0, self.total_ptp_cost_at_level[i-1].get() - total_ptp_cost))
			self.mtp_regained_at_level[i].set(max(0, self.total_mtp_cost_at_level[i-1].get() - total_mtp_cost))	
			
			if self.total_ranks_by_level[i].get() == self.total_ranks_by_level[100].get() and (self.ptp_regained_at_level[i].get() == 0 and self.mtp_regained_at_level[i].get() == 0):
				break		
				
				
	# Figures out the skill cost using the existing ranks and any subskill ranks.
	def Get_Total_Skill_Cost(self, subskill_ranks, ranks, current_level):
		pcost = 0; mcost = 0		
		
		triple_train = max(0, ranks + subskill_ranks - 2 * (current_level + 2))
		double_train = max(0, ranks + subskill_ranks - triple_train - (current_level + 2))
		single_train = max(0, ranks + subskill_ranks - triple_train - double_train)		
				
		pcost = self.ptp_cost * single_train  +  2 * self.ptp_cost * double_train  +  4 * self.ptp_cost * triple_train
		mcost = self.mtp_cost * single_train  +  2 * self.mtp_cost * double_train  +  4 * self.mtp_cost * triple_train	

		return (pcost, mcost)
		
		
	# Figures out how much it would cost to take "new_ranks" number of ranks in this skill given level, total ranks, and subskill ranks
	def Get_Next_Ranks_Cost(self, level, subskill_ranks, new_ranks):
		total_ranks = 0
		postcap_ranks = 0
		pcost = 0; mcost = 0; end = new_ranks+1

		# Calculate the ranks using the post cap ranks
		if level > 100:
			level = 100
			total_ranks = self.total_ranks_by_level[100].get()
			for key, val in self.postcap_ranks_at_interval.items():
				total_ranks += val
		else:						
			total_ranks = self.total_ranks_by_level[level].get()
		
		if total_ranks + new_ranks + subskill_ranks > self.max_ranks * (level+2):
			return (9999, 9999)
		
		for i in range(1, end):
			if total_ranks + i + subskill_ranks > 2 * (level + 2):
				pcost += 4 * self.ptp_cost
				mcost += 4 * self.mtp_cost
			elif total_ranks + i + subskill_ranks > level + 2:
				pcost += 2 * self.ptp_cost
				mcost += 2 * self.mtp_cost
			else:
				pcost += self.ptp_cost
				mcost += self.mtp_cost		
		
		return (pcost, mcost)			
		

	# Used in postcap graph ploting by the Progression panel. 
	# Get total skill ranks at an interval based on the last time a rank was trained.
	def Postcap_Get_Total_Ranks_Closest_To_Interval(self, interval):
		ranks = 0
		
		if interval in self.postcap_total_ranks_at_interval:
			return self.postcap_total_ranks_at_interval[interval]
			
		for key, value in self.postcap_total_ranks_at_interval.items():
			if key > interval:
				break
			ranks = value
			
		return ranks
	

	# Used in postcap graph ploting by the Progression panel. 
	# Get total skill bonus at an interval based on the last time a rank was trained.	
	def Postcap_Get_Bonus_Closest_To_Interval(self, interval):
		bonus = 0
		
		if interval in self.postcap_bonus_at_interval:
			return self.postcap_bonus_at_interval[interval]
			
		for key, value in self.postcap_bonus_at_interval.items():
			if key > interval:
				break				
			bonus = value
		
		return bonus
				
	
	# Train addition ranks past level 100. "exp" is the experience interval these ranks will be trained in		
	def Train_Postcap_Ranks(self, ranks, subskill_ranks, exp):
		global character

		(pcost, mcost) = self.Get_Next_Ranks_Cost(101, subskill_ranks, ranks)	

		# If training at this experience interval already exists, append this new training cost on the end
		if exp in self.postcap_cost_at_interval:
			self.postcap_cost_at_interval[exp] = "%s|%s/%s" % (self.postcap_cost_at_interval[exp], pcost, mcost)
		else:
			self.postcap_cost_at_interval[exp] = "%s/%s" % (pcost, mcost)			

		# Add the new ranks to the ranks at this interval or set them to the new ranks if no training has happened at this level before		
		if exp not in self.postcap_ranks_at_interval:		
			self.postcap_exp_intervals.append(exp)			
			self.postcap_ranks_at_interval[exp] = ranks
		else:
			self.postcap_ranks_at_interval[exp] += ranks			

		# Update the training by interval for the character object		
		if exp in character.postcap_skill_training_by_interval.keys():
			if self.name in character.postcap_skill_training_by_interval[exp]:
				new_training = character.postcap_skill_training_by_interval[exp].replace("%s:%s" % (self.name, self.postcap_ranks_at_interval[exp]-ranks), "%s:%s" % (self.name, self.postcap_ranks_at_interval[exp]))
				character.postcap_skill_training_by_interval.update( {exp : new_training })
			else:
				character.postcap_skill_training_by_interval.update({ exp : "%s|%s:%s" % (character.postcap_skill_training_by_interval[exp], self.name, ranks) })
		else:
			character.postcap_skill_training_by_interval.update( {exp : "%s:%s" % (self.name, ranks) })
						
				
# Each maneuver object contains all the information about a maneuver as well as methods to update, reset, and train ranks in the maneuver
class Maneuver:
	def __init__(self, schedule_parent, arr):
		global professions
		
		self.name = arr[0]
		self.mnemonic = arr[1]
		self.type = arr[2]
		self.max_ranks = arr[3]	
		self.cost_by_rank = [arr[4], arr[5], arr[6], arr[7], arr[8]]
		self.availability = {}
		self.prerequisites = arr['prerequisites']	
		# Stupid back reference error! Makes me need to deal with the fact that None comes back instead of an empty string.
		self.prerequisites_displayed = re.sub("(CM:)|(SM:)|(GS:)|(Skill:)", lambda m: "%s " %m.group(0) or '', self.prerequisites)
		self.prerequisites_displayed = re.sub(":([0-9]+)", ": \g<1> ranks", self.prerequisites_displayed)
		self.prerequisites_displayed = re.sub("&", " AND\n", self.prerequisites_displayed)
		self.prerequisites_displayed = re.sub("\|", " OR\n", self.prerequisites_displayed)
		self.ManP_schedule_row = ""		
		self.PcP_schedule_row = ""		
	
		self.ranks_by_level = [tkinter.IntVar() for i in range(101)]
		self.cost_at_level = [tkinter.IntVar() for i in range(101)]
		self.total_ranks_by_level = [tkinter.IntVar() for i in range(101)]
		self.combined_cost_by_level = [tkinter.IntVar() for i in range(101)]	
		
		self.cost = tkinter.StringVar()
		self.ranks = tkinter.IntVar()
		self.total_ranks = tkinter.IntVar()
		self.combined_cost = tkinter.IntVar()	
		self.postcap_cost = tkinter.StringVar()
		self.postcap_ranks = tkinter.IntVar()
		self.postcap_total_ranks = tkinter.IntVar()
		self.postcap_sum_cost = tkinter.StringVar()	
	
		# Used by Postcap panel
		self.postcap_exp_intervals = []
		self.postcap_ranks_at_interval = collections.OrderedDict()
		self.postcap_total_ranks_at_interval = collections.OrderedDict()
		self.postcap_cost_at_interval = collections.OrderedDict()
		
	
		for prof in professions:
			self.availability[prof] = arr['available_'+prof.lower()]
	
		for i in range(0,5):
			if self.cost_by_rank[i] == "NONE":
				self.cost_by_rank[i] = "-"
				
		self.Create_ManP_schedule_row(schedule_parent)		
		self.Set_To_Default()


	# Resets the Maneuver object for the Maneuver panel
	def Set_To_Default(self):
		self.cost.set("")
		self.ranks.set(0)
		self.total_ranks.set(0)
		self.combined_cost.set(0)
		
		for i in range(101):
			self.ranks_by_level[i].set(0)
			self.cost_at_level[i].set(0)
			self.total_ranks_by_level[i].set(0)
			self.combined_cost_by_level[i].set(0)			

		self.ManP_schedule_row.grid_remove()

		
	# Resets the Maneuver object for the Postcap panel
	def Set_To_Default_Postcap(self):
		self.postcap_exp_intervals = []
		self.postcap_ranks_at_interval.clear()
		self.postcap_total_ranks_at_interval.clear()
		self.postcap_cost_at_interval.clear()	
		

	# The schedule row shows the training for the current level in the maneuver, the cost of that training and the training for the total ranks the character has in the maneuver	
	def Create_ManP_schedule_row(self, parent):
		self.ManP_schedule_row = tkinter.Frame(parent)	
		self.ManP_schedule_row.bindtags("ManP_schedule")
		
		L1 = tkinter.Label(self.ManP_schedule_row, width="26", bg="lightgray", anchor="w", text=self.name)
		L1.grid(row=0, column=0, padx="1", pady="1")
		L1.bindtags("ManP_schedule")
		L2 = tkinter.Label(self.ManP_schedule_row, width="8", bg="lightgray", textvariable=self.ranks)	 
		L2.grid(row=0, column=1, padx="1", pady="1")	
		L2.bindtags("ManP_schedule")
		L3 = tkinter.Label(self.ManP_schedule_row, width="6", bg="lightgray", textvariable=self.cost) 		
		L3.grid(row=0, column=2, padx="1", pady="1")	
		L3.bindtags("ManP_schedule")
		L4 = tkinter.Label(self.ManP_schedule_row, width="10", bg="lightgray", textvariable=self.total_ranks)
		L4.bindtags("ManP_schedule")		
		L4.grid(row=0, column=3, padx="1", pady="1")	
		L5 = tkinter.Label(self.ManP_schedule_row, width="8", bg="lightgray", textvariable=self.combined_cost)	
		L5.grid(row=0, column=4, padx="1", pady="1")
		L5.bindtags("ManP_schedule")		

		
	# The schedule row shows the training for the current experience interval in the maneuver, the cost of that training and the training for the total ranks the character has in the maneuver	
	def Create_PcP_schedule_row(self, parent):
		self.PcP_schedule_row = tkinter.Frame(parent)	
		self.PcP_schedule_row.bindtags("PcP_schedule")
		
		L1 = tkinter.Label(self.PcP_schedule_row, width="26", bg="lightgray", anchor="w", text=self.name)
		L1.grid(row=0, column=0, padx="1", pady="1")
		L1.bindtags("PcP_schedule")
		L2 = tkinter.Label(self.PcP_schedule_row, width="8", bg="lightgray", textvariable=self.postcap_ranks)	 
		L2.grid(row=0, column=1, padx="1", pady="1")	
		L2.bindtags("PcP_schedule")
		L3 = tkinter.Label(self.PcP_schedule_row, width="6", bg="lightgray", textvariable=self.postcap_cost) 		
		L3.grid(row=0, column=2, padx="1", pady="1")	
		L3.bindtags("PcP_schedule")
		L4 = tkinter.Label(self.PcP_schedule_row, width="10", bg="lightgray", textvariable=self.postcap_total_ranks)
		L4.bindtags("PcP_schedule")		
		L4.grid(row=0, column=3, padx="1", pady="1")	
		L5 = tkinter.Label(self.PcP_schedule_row, width="8", bg="lightgray", textvariable=self.postcap_sum_cost)	
		L5.grid(row=0, column=4, padx="1", pady="1")
		L5.bindtags("PcP_schedule")	

		
	# Figures out how much it cost to train in the maneuver at "rank" rank. 
	# "prof_type" will determine if there is an additional cost to train in the skill. Only "combat" maneuvers have an extra cost.
	def Get_Cost_At_Rank(self, rank, prof_type):
		if rank > len(self.cost_by_rank):
			return 9999
			
		if self.cost_by_rank[rank-1] == "-":
			return "-"
			
		if prof_type == "square" or self.type != "combat":
			modifier = 1
		elif prof_type == "semi":
			modifier = 1.5
		elif prof_type == "pure":
			modifier = 2	

		return math.floor(int(self.cost_by_rank[rank-1]) * modifier)				
	

	# Similar to Get_Cost_At_Rank, this method will figure out the CUMULATIVE cost to train "new_ranks" ranks in this manevuer starting at "start_rank" ranks.
	# "prof_type" will determine if there is an additional cost to train in the skill. Only "combat" maneuvers have an extra cost.
	# "armor" maneuvers just return their current rank cost
	def Get_Total_Cost_At_Rank(self, start_rank, new_ranks, prof_type):	
		total = 0
		end_rank = start_rank + new_ranks
		
#		if self.type == "armor":
#			return self.cost_by_rank[end_rank - 1]
				
		if prof_type == "square" or self.type != "combat":
			modifier = 1
		elif prof_type == "semi":
			modifier = 1.5
		elif prof_type == "pure":
			modifier = 2	
				
		if end_rank > 5 or self.cost_by_rank[end_rank - 1] == "-":
			return -1
			
		for i in range(start_rank, end_rank):
			total += math.floor(int(self.cost_by_rank[i]) * modifier)
			
		return total


	# This method will calculate the cost of training "ranks" ranks in this maneuver at "level". This cost is based on the existing skill ranks and what "prof_type" the characters profession is.	
	def Train_New_Ranks(self, level, ranks, prof_type):
		tcost = 0				
		new_total_ranks = self.ranks_by_level[level].get() + ranks		
		
		if level > 0:
			new_total_ranks += self.total_ranks_by_level[level-1].get()
		
		tcost =	self.Get_Total_Cost_At_Rank(0, new_total_ranks, prof_type)
		diff = self.total_ranks_by_level[level].get() - self.ranks_by_level[level].get()
		ncost = self.Get_Total_Cost_At_Rank(diff, self.ranks_by_level[level].get() + ranks, prof_type)
		
		self.cost_at_level[level].set(ncost)
		self.ranks_by_level[level].set(ranks + self.ranks_by_level[level].get())
		
		# Set Total Ranks and Bonus for each level
		for i in range(level, 101):
			self.total_ranks_by_level[i].set(new_total_ranks)				
			self.combined_cost_by_level[i].set(tcost)	

 		
	# Train addition ranks past level 100. "exp" is the experience interval these ranks will be trained in
	def Train_Postcap_Ranks(self, exp, ranks, prof_type):
		global character
		training_by_interval = ""
		total_ranks = self.total_ranks_by_level[100].get()
		
		# Find out what kind of maneuver we are training
		if self.type == "combat":
			training_by_interval = character.postcap_combat_training_by_interval 
		elif self.type == "shield":
			training_by_interval = character.postcap_shield_training_by_interval 
		elif self.type == "armor":
			training_by_interval = character.postcap_armor_training_by_interval 
		
		# Get the total postcap ranks in this maneuver
		for key, val in self.postcap_ranks_at_interval.items():
			total_ranks += val
			
		# If the new ranks would go beyond the max ranks, send back an error number
		cost = self.Get_Cost_At_Rank(total_ranks + 1, prof_type)			
		if cost == "-":
			return 9999

		# If training at this experience interval already exists, append this new training cost on the end
		if exp in self.postcap_cost_at_interval:
			self.postcap_cost_at_interval[exp] = "%s|%s" % (self.postcap_cost_at_interval[exp], cost)
		else:
			self.postcap_cost_at_interval[exp] = "%s" % cost

		
		self.postcap_exp_intervals.append(exp)				
		
		# Add the new ranks to the ranks at this interval or set them to the new ranks if no training has happened at this level before
		if exp not in self.postcap_ranks_at_interval:
			self.postcap_ranks_at_interval[exp] = ranks
		else:
			self.postcap_ranks_at_interval[exp] += ranks
			
		# Update the training by interval for the character object
		if exp in training_by_interval.keys():
			if self.name in training_by_interval[exp]:
				new_training = training_by_interval[exp].replace("%s:%s" % (self.name, self.postcap_ranks_at_interval[exp]-ranks), "%s:%s" % (self.name, self.postcap_ranks_at_interval[exp]))
				training_by_interval.update( {exp : new_training })
			else:
				training_by_interval.update({ exp : "%s|%s:%s" % (training_by_interval[exp], self.name, ranks) })
		else:
			training_by_interval.update( {exp : "%s:%s" % (self.name, ranks) })		


	# Used in postcap graph ploting by the Progression panel. 
	# Get total skill ranks at an interval based on the last time a rank was trained.			
	def Postcap_Get_Total_Ranks_Closest_To_Interval(self, interval):
		ranks = 0
		
		if interval in self.postcap_total_ranks_at_interval:
			return self.postcap_total_ranks_at_interval[interval]
			
		for key, value in self.postcap_total_ranks_at_interval.items():
			if key > interval:
				break
				
			ranks = value			
			
		return ranks
			

# "Gear" is any in game item that can be equipped and used in combat such as weapons, shields, and armor
# Gear objects are used in the Loadout panel
class Gear:
	def __init__(self, order, name, enchantment, weight, skill_names, type):
		global LdP_gear_display_types
		
		self.name = tkinter.StringVar()	
		self.order = tkinter.StringVar()	
		self.display_type = tkinter.StringVar()		
		self.display_details = tkinter.StringVar()	
		self.dialog_type = type
		self.skills = skill_names
		self.enchantment = enchantment
		self.weight = int(weight)
		self.ProgP_display_name = ""
		
		self.gear_traits = {}  	# Gear is a generic class that needs to hold any item of equipment, this dictionary will hold it's values. I.e armor hindrance or weapon base speed		
					
		self.LdP_Row = ""
		self.LdP_Edit_Button = ""		
		
		# Initialize defaults				
		self.name.set(name)		
		self.order.set(order)
		self.display_details.set("")
		self.display_type.set(LdP_gear_display_types[skill_names])
		
		self.Update_Progression_Name()
	
		
	# Create the build list row used in the Loadout panel
	def Create_LdP_row(self, parent):
		self.LdP_Row = tkinter.Frame(parent)	
		self.LdP_Row.bindtags("LdP_gear")
		
		L1 = tkinter.Label(self.LdP_Row, width=5, bg="lightgray", textvariable=self.order)
		L1.grid(row=0, column=0, padx="1", pady="1")
		L1.bindtags("LdP_gear")
		L2 = tkinter.Label(self.LdP_Row, width="22", anchor="w", bg="lightgray", textvariable=self.name)
		L2.grid(row=0, column=1, padx="1", pady="1")
		L2.bindtags("LdP_gear")
		L3 = tkinter.Label(self.LdP_Row, width="8", anchor="w", bg="lightgray", textvariable=self.display_type)
		L3.grid(row=0, column=2, padx="1", pady="1")
		L3.bindtags("LdP_gear")
		L4 = tkinter.Label(self.LdP_Row, width=20, anchor="w", bg="lightgray", textvariable=self.display_details)
		L4.grid(row=0, column=3, padx="1")
		L4.bindtags("LdP_gear")
		self.LdP_Edit_Button = tkinter.Button(self.LdP_Row, text="Edit", command="")
		self.LdP_Edit_Button.grid(row=0, column=7, padx="3")			
	
	# Because gear is generic, it doesn't have a specific fields for traits unique to a certain type of gear 
	# such as action penalty, this funtion is used to create a dictionary for those traits.
	def Set_Gear_Traits(self, name):
		global db_cur, db_con
		self.gear_traits = {}
		if self.dialog_type == "Armor":
			table = "Armor"
			fields = "roundtime, action_penalty, base_weight, minor_spiritual_spell_hindrance, major_spiritual_spell_hindrance, cleric_spell_hindrance, minor_elemental_spell_hindrance, minor_mental_spell_hindrance, major_elemental_spell_hindrance, major_mental_spell_hindrance, savant_spell_hindrance, ranger_spell_hindrance, sorcerer_spell_hindrance, wizard_spell_hindrance, bard_spell_hindrance, empath_spell_hindrance, paladin_spell_hindrance, max_spell_hindrance, roundtime_train_off_ranks, AG"	
		elif self.dialog_type == "Shields":
			table = "Shields"
			fields = "size, melee_size_modifer, ranged_size_modifer, ranged_size_bonus, dodging_shield_factor, dodging_size_penalty"	
		else:
			table = "Weapons"
			fields = "base_speed, minimum_speed"
		
		if name == "":
			name = self.name.get()
		query = "SELECT %s FROM %s WHERE name = '%s'" % (fields, table, name)
		trait_arr = fields.split(", ")
		
		db_cur.execute(query)
		db_con.commit()		
		data = db_cur.fetchall()		
		
		for item in data:
			for trait in trait_arr:
				self.gear_traits[trait] = item[trait]
						
		
	# This method updates the details section of the LdP_row found on the Loadout panel
	# Details will show the enchantment value, enchantment time (ie 3x) and weight
	def Update_Display_Details(self):
		whole_bonus = int(int(self.enchantment) / 5)
		faction_bonus = int(int(self.enchantment) % 5)
		
		if( faction_bonus > 0):
			faction_text = ".5"
		else:
			faction_text = ""	
		
		weight_text = ", %s lb" % self.weight
		
		self.display_details.set("%+d (%s%sx)%s" %(int(self.enchantment), whole_bonus, faction_text, weight_text))	
	
	# Updates the way the gear is represented in the Progression panel gear menus
	def Update_Progression_Name(self):	
		self.ProgP_display_name = "%s. %s (%+d)" % (self.order.get(), self.name.get(), int(self.enchantment))
		
		
		
# An "Effect" is a spell, enhancive or really any kind of buff/debuff that can affect the characters attributes
# Effects are created on the Loadout panel, factored into the calculations made on the Progresson panel, and
# stored as part of the global character object
class Effect:
	def __init__(self, order, name, type, display_type, details, effect_tags, scaling_arr, function, options, hidden):
		self.name = tkinter.StringVar()
		self.type = tkinter.StringVar()		
		self.display_type = tkinter.StringVar()	
		self.order = tkinter.StringVar()			
		self.scaling = tkinter.StringVar()		
		self.details = tkinter.StringVar()
		self.effect_tags = effect_tags
		self.scaling_arr = scaling_arr
		self.function = function
		self.options = options		
		self.LdP_Build_Row = ""
		self.LdP_Edit_Button = ""	
		self.LdP_details_frame_label = ""
		self.LdP_scaling_frame_label = ""
		self.hide = tkinter.StringVar()
		self.ProgP_Build_Row = ""
		self.ProgP_scaling_frame_label = ""

		scaling = ""		
		
		# Initialize defaults	
		self.name.set(name)
		self.type.set(type)
		self.display_type.set(display_type)
		self.order.set(order)
		self.details.set(details)
		self.hide.set(hidden)
		
		if len(scaling_arr) == 0:
			scaling = "NONE"			
		else:
			for key, value in scaling_arr.items():
				scaling += "%s: %s\n" % (key, value)
			scaling = scaling[:-1]				
		self.scaling.set(scaling)		
				
		
	# Create the build list row used in the Loadout panel
	def Create_LdP_row(self, parent):
		self.LdP_Build_Row = tkinter.Frame(parent)
		
		self.details_frame = Pmw.ScrolledFrame(self.LdP_Build_Row, usehullsize = 1, hull_width = 196, hull_height = 36)
		self.details_frame.component("borderframe").config(borderwidth=0)
		self.details_frame.configure(hscrollmode = "none", vscrollmode = "static")	
		
		self.scaling_frame = Pmw.ScrolledFrame(self.LdP_Build_Row, usehullsize = 1, hull_width = 146, hull_height = 36)
		self.scaling_frame.component("borderframe").config(borderwidth=0)
		self.scaling_frame.configure(hscrollmode = "none", vscrollmode = "static")	
		
		# Creates the order, name, and type fields
		L1 = tkinter.Label(self.LdP_Build_Row, width=5, height=2, bg="lightgray", textvariable=self.order)
		L1.grid(row=0, column=0, padx="1", pady="1")
		L1.bindtags("LdP_effects")
		L2 = tkinter.Label(self.LdP_Build_Row, width="15", height=2, anchor="c", wraplength=100, bg="lightgray", textvariable=self.name)
		L2.grid(row=0, column=1, padx="1", pady="1")
		L2.bindtags("LdP_effects")
		L3 = tkinter.Label(self.LdP_Build_Row, width="8", height=2, anchor="c", wraplength=70, bg="lightgray", textvariable=self.display_type)
		L3.grid(row=0, column=2, padx="1", pady="1")
		L3.bindtags("LdP_effects")
		
		# The detail and scaling frames can have more that 2 lines of text. They are setup to perform word wrapping and dynamic height adjustments
		self.details_frame.grid(row=0, column=3, sticky="nw", padx="1", pady="1")
		self.LdP_details_frame_label = tkinter.Label(self.details_frame.interior(), width=27, justify="left", anchor="nw", wraplength=175, bg="lightgray", textvariable=self.details)
		self.LdP_details_frame_label.bind("<MouseWheel>", self.Scroll_Details_Frame)
		self.LdP_details_frame_label.grid(row=0, column=0)			

		self.scaling_frame.grid(row=0, column=4, sticky="nw")
		self.LdP_scaling_frame_label = tkinter.Label(self.scaling_frame.interior(), width="20", anchor="nw", justify="left", bg="lightgray", textvariable=self.scaling)
		self.LdP_scaling_frame_label.bind("<MouseWheel>", self.Scroll_Scaling_Frame)
		self.LdP_scaling_frame_label.grid(row=0, column=0)

		self.LdP_Edit_Button = tkinter.Button(self.LdP_Build_Row, text="Edit", command="")
		self.LdP_Edit_Button.grid(row=0, column=7, padx="3")	
		
		self.Update_Row_Heights()
		
	
	# Create the build list row used in the Loadout panel
	def Create_ProgP_row(self, parent):
		self.ProgP_Build_Row = tkinter.Frame(parent)	
		self.scaling_frame = Pmw.ScrolledFrame(self.ProgP_Build_Row, usehullsize = 1, hull_width = 136, hull_height = 36)
		self.scaling_frame.component("borderframe").config(borderwidth=0)
		self.scaling_frame.configure(hscrollmode = "none", vscrollmode = "static")	
		
		tkinter.Checkbutton(self.ProgP_Build_Row, variable=self.hide).grid(row=0, column=0, sticky="w")	
		L2 = tkinter.Label(self.ProgP_Build_Row, width="15", height="2", anchor="c", wraplength=100, bg="lightgray", textvariable=self.name)
		L2.grid(row=0, column=1, padx="3", pady="2")
		L2.bindtags("ProgP_effects")
		L3 = tkinter.Label(self.ProgP_Build_Row, width="8", height=2, anchor="c", wraplength=70, bg="lightgray", textvariable=self.display_type)
		L3.grid(row=0, column=2, padx="1", pady="1")
		L3.bindtags("ProgP_effects")
		self.scaling_frame.grid(row=0, column=3, padx="1", pady="1")
		self.LdP_scaling_frame_label = tkinter.Label(self.scaling_frame.interior(), width="16", anchor="nw", justify="left", bg="lightgray", textvariable=self.scaling)
		self.LdP_scaling_frame_label.bind("<MouseWheel>", self.Scroll_Scaling_Frame)
		self.LdP_scaling_frame_label.grid(row=0, column=0)		
		
		self.Update_Row_Heights()
		

	# If the height of the details or scaling frames are 0, the frame will automatically adjust it's height to the correct number in regard to the text in it.
	# However, the height has to be atleast 2 in order to match the general size effect row. To fix this issue, count the number of text lines and if it is 
	# 2 lines or less (only 1 "\n") set the height to 2 manually
	def Update_Row_Heights(self):
		if(self.details.get().count("\n") > 0):
			self.LdP_details_frame_label.config(height = "0")
		else:
			self.LdP_details_frame_label.config(height = "2")	
			
		if(self.scaling.get().count("\n") > 0):
			self.LdP_scaling_frame_label.config(height = "0")
			self.LdP_scaling_frame_label.config(height = "0")
		else:	
			self.LdP_scaling_frame_label.config(height = "2")	
			self.LdP_scaling_frame_label.config(height = "2")			
			
	# Every effect is linked to a coresponding method in Calculations.py that calculates
	# a bonus/penalty depending on what effect tag is sent to it. Using eval and storing
	# the method names in a field in the planners database was the best way I could figure
	# out how to find the bonuses with as little bloating as possible.
	def Calculate_Tag_Bonus(self, effect_tag, level):
		return eval("calculations.%s" % self.function)(self, effect_tag, level)
	
	# Allows the Detail Frame of the LdP_row to be scrollable with the mouse wheel
	def Scroll_Details_Frame(self, event):
		self.details_frame.yview("scroll", -1*(event.delta/120), "units")	

		
	# Allows the Detail Frame of the LdP_row to be scrollable with the mouse wheel
	def Scroll_Scaling_Frame(self, event):
		self.scaling_frame.yview("scroll", -1*(event.delta/120), "units")	


		
# The Planner's "Error Box". This dialog box will appear when an error or warning is triggered by the user.
class Information_Dialog:
	def __init__(self):
		global root	
		self.width = 400; self.height = 250; self.xpos = 450; self.ypos = 300		
		self.error_font = tkinter.font.Font(family="Helvetica", size=10)
		self.dialogbox = Pmw.Dialog(root, buttons = ("Okay", ), title = "Information", command = self.Button_Onclick)
		self.message = tkinter.StringVar()
		self.myframe = Pmw.ScrolledFrame(self.dialogbox.interior(), usehullsize = 1, hull_width = self.width, hull_height = self.height-35)
		self.myframe_inner = self.myframe.interior()			
			
		self.dialogbox.transient(root)	
		self.dialogbox.resizable(width=0, height=0)		
		self.dialogbox.geometry('%sx%s+%s+%s' % (self.width, self.height, self.xpos, self.ypos))

		self.myframe.configure(hscrollmode = "none")		
		self.myframe.grid(row=0, column=0, sticky="nw")	
#		tkinter.Label(self.myframe_inner, anchor="w", font="-weight bold", wraplength=self.width-10, justify="left", textvariable=self.message).grid(row=0, column=0, sticky="w")
		tkinter.Label(self.myframe_inner, anchor="w", font=self.error_font, wraplength=self.width-10, justify="left", textvariable=self.message).grid(row=0, column=0, sticky="w")
		self.dialogbox.bind("<MouseWheel>", self.Scroll_Inner_Frame)
		self.dialogbox.withdraw()

		
	# Clicking the Okay button hides the dialog box. Also, cancelling the box does this too.
	def Button_Onclick(self, result):
		self.dialogbox.grab_release()
		self.dialogbox.withdraw()
		self.message.set("")	

		
	# Makes the dialog appear with a message.
	def Show_Message(self, msg):
		self.message.set(msg)
		self.dialogbox.show()
		self.dialogbox.grab_set()

		
	# Allows the inner frame of the Dialog box to be mouse scrollable	
	def Scroll_Inner_Frame(self, event):
		self.myframe.yview("scroll", -1*(event.delta/120), "units")
		
	
#Planner globals	
title = "Hymore Character Planner"
version = "v2.6.5"
char_name = "New Character"	
root = tkinter.Tk()
root.geometry("1140x600")
root.resizable(0,0)
notebook = ""
db_file = "GS4_Planner.db"
db_con = ""
db_cur = ""
panels = {}
info_dialog = Information_Dialog()
		
		
# Statistics Panel globals		
statistics = ["Strength", "Constitution", "Dexterity", "Agility", "Discipline", "Aura", "Logic", "Intuition", "Wisdom", "Influence"]
professions = ["Bard", "Cleric", "Empath", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warrior", "Wizard"]
races = ["Aelotoi", "Burghal Gnome", "Dark Elf", "Dwarf", "Elf", "Erithian", "Forest Gnome", "Giantman", "Half Elf", "Half Krolvin", "Halfling", "Human", "Sylvankind"]	

# Calculate the experience needed and total earned from levels 0 - 100
next_exp = [tkinter.StringVar() for i in range(101)]
total_exp = [tkinter.StringVar() for i in range(101)]	
next_exp[0].set(2500); next_exp[1].set(2500); next_exp[100].set("-")
total_exp[0].set(0); total_exp[100].set(7572500)	
for i in range(0, 100):		
	if i > 49:
		val = 500
	elif i > 39:
		val = 1000
	elif i > 24:
		val = 1500
	elif i > 14:
		val = 2000
	else:
		val = 2500	
	
	if i < 2:
		next_exp[i].set( val )	
	else:
		next_exp[i].set( int(next_exp[i-1].get()) + val )
	
	if i > 0:
		total_exp[i].set( int(total_exp[i-1].get()) + int(next_exp[i].get()) )
	
	
# Skills Panel globals	
skill_names = []


# Maneuvers Panel globals
combat_maneuver_names = []
shield_maneuver_names = []
armor_maneuver_names = []


# Loadout Panel globals
LdP_Gear_List_Updated = 0				# Indicates that a change has been made to the Loadout Panel's gear list. Progression Panel needs this to have an accurate loadout lists
LdP_Effects_List_Updated = 0			# Indicates that a change has been made to the Loadout Panel's effects list. Progression Panel needs this to have an accurate loadout lists

LdP_gear_display_types = { 'None':'None', 'Brawling':'Brawling', 'Edged Weapons':'OHE', 'Blunt Weapons':'OHB', 'Two-Handed Weapons':'THW', 'Polearm Weapons':'Polearm', 'Ranged Weapons':'Ranged', 'Thrown Weapons':'Thrown', 'UAC Weapons':'UAC', 'Armor':'Armor', 'Shields':'Shield', 'Edged Weapons/Brawling':'OHE/BRW', 'Edged Weapons/Two-Handed Weapons':'OHE/THW', "Spell Aiming":'Spell' }

LdP_effect_display_types = collections.OrderedDict()
LdP_effect_display_types['Minor Spiritual (100s)'] = 'MnS Spell'
LdP_effect_display_types['Major Spiritual (200s)'] = 'MjS Spell'
LdP_effect_display_types['Cleric Base (300s)'] = 'Clrc Spell'
LdP_effect_display_types['Minor Elemental (400s)'] = 'MnE Spell'
LdP_effect_display_types['Major Elemental (500s)'] = 'MjE Spell'
LdP_effect_display_types['Ranger Base (600s)'] = 'Rngr Spell'
LdP_effect_display_types['Sorcerer Base (700s)'] = 'Sorc Spell'
LdP_effect_display_types['Wizard Base (900s)'] = 'Wiz Spell'
LdP_effect_display_types['Bard Base (1000s)'] = 'Spellsong'
LdP_effect_display_types['Empath Base (1100s)'] = 'Emp Spell'
LdP_effect_display_types['Minor Mental (1200s)'] = 'MnM Spell'
# LdP_effect_display_types['Major Mental (1300s)'] = 'MjM Spell'
# LdP_effect_display_types['Savant Base (1400s)'] = 'Svnt Spell'
LdP_effect_display_types['Paladin Base (1600s)'] = 'Pala Spell'
LdP_effect_display_types['Arcane (1700s)'] = 'Arc Spell'
LdP_effect_display_types['Maneuvers'] = 'Maneuver'
LdP_effect_display_types['Society Powers'] = 'Society'
LdP_effect_display_types['Special Abilities'] = 'Special Ability'
LdP_effect_display_types['Enhancives (Resources)'] = 'Enhancive Resource'
LdP_effect_display_types['Enhancives (Skills)'] = 'Enhancive Skill'
LdP_effect_display_types['Enhancives (Statistics)'] = 'Enhancive Statistic'
LdP_effect_display_types['Generic Bonus'] = 'Generic Bonus'
LdP_effect_display_types['Status Effects'] = 'Status'
LdP_effect_display_types['Room Effects'] = 'Room\nEffect'
LdP_effect_display_types['Flares'] = 'Flare'
LdP_effect_display_types['Items'] = 'Item'
# LdP_effect_display_types['Other'] = 'Other'

					
LdP_effect_display_scaling = { 'Spell Research, Minor Spiritual ranks':'Minor Spiritual', 'Spell Research, Major Spiritual ranks':'Major Spiritual', 'Spell Research, Cleric ranks':					  'Cleric', 'Spell Research, Minor Elemental ranks':'Minor Elemental', 'Spell Research, Major Elemental ranks':'Major Elemental', 
					  'Spell Research, Ranger ranks':'Ranger', 'Spell Research, Sorcerer ranks':'Sorcerer', 'Spell Research, Wizard ranks':'Wizard', 'Spell Research, Bard ranks':'Bard', 'Spell Research, Empath ranks':'Empath', 'Spell Research, Minor Mental ranks':'Minor Mental', 
#					  'Spell Research, Major Mental ranks':'Major Mental', 'Spell Research, Savant ranks':'Savant', 
					  'Spell Research, Paladin ranks':'Paladin', 
					  'Elemental Lore, Air ranks':'Air', 'Elemental Lore, Earth ranks':'Earth', 'Elemental Lore, Fire ranks':'Fire', 'Elemental Lore, Water ranks':'Water', 
					  'Mental Lore, Divination ranks':'Divination', 'Mental Lore, Manipulation ranks':'Manipulation', 'Mental Lore, Telepathy ranks':'Telepathy', 'Mental Lore, Transference ranks':'Transference', 'Mental Lore, Transformation ranks':'Transformation',
					  'Spiritual Lore, Blessings ranks':'Blessings', 'Spiritual Lore, Religion ranks':'Religion', 'Spiritual Lore, Summoning ranks':'Summoning', 
					  'Sorcerous Lore, Demonology ranks':'Demonology', 'Sorcerous Lore, Necromancy ranks':'Necromancy',					
					  'Elemental Mana Control ranks':'Elemental MC', 'Mental Mana Control ranks':'Mental MC', 'Spiritual Mana Control ranks':'Spiritual MC',  
					  'Multi-Opponent Combat ranks':'MOC',
					  'Maneuver ranks':'Maneuver ranks', "Guild skill ranks":"Guild skill ranks",
					  'Council of Light rank':'COL rank', 'Guardians of Sunfist rank':'GoS rank', 'Order of Voln rank':'Voln rank',
					  # The effects below do not have dynamic scaling
					  'Health recovery bonus':'Health recovery', 'Health maximum bonus':'Maximum health', 
					  'Mana recovery bonus':'Mana recovery', 'Mana maximum bonus':'Maximum mana', 
					  'Stamina recovery bonus':'Stam recovery', 'Stamina maximum bonus':'Maximum stam', 
					  'Spirit recovery bonus':'Spirit recovery', 'Spirit maximum bonus':'Maximum spirit', 
					  'Statistic increase':'Statistic increase', 'Statistic bonus':'Statistic bonus', 'Skill ranks':'Skill ranks', 'Skill bonus':'Skill bonus', 
					  'All AS bonus':'All AS bonus', 'Melee AS bonus':'Melee AS bonus', 'Ranged AS bonus':'Ranged AS bonus', 'Bolt AS bonus':'Bolt AS bonus', 'UAF bonus':'UAF bonus', 
					  'All DS bonus':'All DS bonus', 'Melee DS bonus':'Melee DS bonus', 'Ranged DS bonus':'Ranged DS bonus', 'Bolt DS bonus':'Bolt DS bonus', 
					  'All CS bonus':'All CS bonus', 'Elemental CS bonus':'Ele CS bonus', 'Mental CS bonus':'Mental CS bonus', 'Spiritual CS bonus':'Spirit CS bonus', 'Sorcerer CS bonus':'Sorc CS bonus',
					  'All TD bonus':'All TD bonus', 'Elemental TD bonus':'Ele TD bonus', 'Mental TD bonus':'Mental TD bonus', 'Spiritual TD bonus':'Spirit TD bonus', 'Sorcerer TD bonus':'Sorc TD bonus',
					  'Tier':'Tier' }

# Progression Panel globals
summation_bonuses =[ [0],
						[1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153, 171, 190, 210, 231, 253, 276, 300],
						[2, 5, 9, 14, 20, 27, 35, 44, 54, 65, 77, 90, 104, 119, 135, 152, 170, 189, 209, 230, 252, 275, 299],
						[3, 7, 12, 18, 25, 33, 42, 52, 63, 75, 88, 102, 117, 133, 150, 168, 187, 207, 228, 250, 273, 297],
						[4, 9, 15, 22, 30, 39, 49, 60, 72, 85, 99, 114, 130, 147, 165, 184, 204, 225, 247, 270, 294],
						[5, 11, 18, 26, 35, 45, 56, 68, 81, 95, 110, 126, 143, 161, 180, 200, 221, 243, 266, 290],
						[6, 13, 21, 30, 40, 51, 63, 76, 90, 105, 121, 138, 156, 175, 195, 216, 238, 261, 285],
						[7, 15, 24, 34, 45, 57, 70, 84, 99, 115, 132, 150, 169, 189, 210, 232, 255, 279],
						[8, 17, 27, 38, 50, 63, 77, 92, 108, 125, 143, 162, 182, 203, 225, 248, 272, 297],
						[9, 19, 30, 42, 55, 69, 84, 100, 117, 135, 154, 174, 195, 217, 240, 264, 289],
						[10, 21, 33, 46, 60, 75, 91, 108, 126, 145, 165, 186, 208, 231, 255, 280]
					]					  
					  

# Character global needs to be declared last since it uses all the globals decalared above
character = Character();
