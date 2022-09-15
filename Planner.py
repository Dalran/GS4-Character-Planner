# INDEX OF CLASSES AND METHODS
"""
class Planner
    def _init__(self, parent)
    def Create_Top_Menubar(self):
    def Menubar_Option_New_Character(self):
    def Menubar_Option_Load_Character(self):
    def Menubar_Option_Save_Character(self):
    def Create_Notebook(self, parent):
    def Notebook_OnShowPage(self, caller):
    def Notebook_OnHidePage(self, caller):
"""

# !/usr/bin/python
import sys

import traceback
import os
import sqlite3
import tkinter
import Pmw
import Globals as globals
import StatisticsPanel as StP
import Misc_Panel as MiP
import Skills_Panel as SkP
import Maneuvers_Panel as ManP
import PostCap_Panel as PcP
import Loadout_Panel as LdP

from time import sleep

# import Summary_Panel as SumP
from tkinter import messagebox


def handle_unhandled_exception(e_type, e_value, e_traceback):
    error_file = open('error.log', 'a')
    #traceback.print_exc()
    #traceback.print_exc(file=error_file)
    print(e_value)
    error_file.close()


sys.excepthook = handle_unhandled_exception


# Planner is the primary window in the program that holds everything else.
# Planner is responsible for creating top Menubar and the Notebook used to store each Panel
class Planner:
    def __init__(self, parent):
        self.parent = parent
        self.pages = {}
        self.panels_loaded = 0

        self.fetch_data()

        # Create top Menubar used to Save and Load character builds
        self.Create_Top_Menubar()

        # Create the Notebook used to hold all the Panels and then create each Panel to be held in the Notebook
        self.Create_Notebook(self)

    def fetch_data(self):
        # Initialize the race list
        globals.db_cur.execute("SELECT * FROM Races")
        globals.db_con.commit()
        data = globals.db_cur.fetchall()

        for race in data:
            globals.character.race_list[race[0]] = globals.Race(race)

        # Initialize the profession list
        globals.db_cur.execute("SELECT * FROM Professions")
        globals.db_con.commit()
        data = globals.db_cur.fetchall()
        for prof in data:
            globals.character.profession_list[prof[0]] = globals.Profession(prof)
    # Makes the top menu that appears horizontally across the top of the planner
    def Create_Top_Menubar(self):
        menubar = tkinter.Menu(self.parent)
        self.parent.config(menu=menubar)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Character",
                             command=self.Menubar_Option_New_Character)  # Reset planner to default
        filemenu.add_command(label="Load Character",
                             command=self.Menubar_Option_Load_Character)  # Open and load a character save file into the planner
        filemenu.add_command(label="Save Character as...",
                             command=self.Menubar_Option_Save_Character)  # Save an existing build to file
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.Planner_Onclose)

    # Choosing to make a new charcter is the same thing as resetting every panel back to default.
    # Have each panel call their Clear methods and change the panel back to Statistics.
    def Menubar_Option_New_Character(self):
        if not tkinter.messagebox.askyesno("New Character",
                                           "Are you sure you want to start a new character?\nAll unsaved data will be lost."):
            return

        globals.char_name = "New Character"
        for stat, obj in globals.character.statistics_list.items():
            obj.Set_To_Default()
        globals.panels['Misc'].Reset_Panel()
        globals.panels['Skills'].ClearAll_Button_Onclick()
        globals.panels['Maneuvers'].Clear_Button_Onclick("All")
        globals.panels['Post Cap'].Clear_Button_Onclick("All")
        globals.panels['Loadout'].Gear_ClearAll_Button_Onclick()
        globals.panels['Loadout'].Effects_ClearAll_Button_Onclick()

        globals.root.title("%s %s - %s" % (globals.title, globals.version, globals.char_name))
        globals.notebook.selectpage("Statistics")

    # Load a character plan from a character file
    def Menubar_Option_Load_Character(self):
        #		if not tkinter.messagebox.askyesno("Load Character", "Are you sure you want to load a character? All unsaved data will be lost."):
        #			return
        globals.character.Load_Character()

    # Save the current character plan in a character file
    def Menubar_Option_Save_Character(self):
        globals.character.Save_Character()

    # Method uses a Python megawidget, Notebook, to create and hold all the Panels
    def Create_Notebook(self, parent):
        globals.notebook = Pmw.NoteBook(self.parent,
                                        tabpos='n',
                                        #       createcommand = PrintOne('Create'),
                                        #       lowercommand = self.Notebook_OnHidePage,
                                        hull_width=300,
                                        hull_height=300,
                                        )
        globals.notebook.pack(fill='both', expand=1, padx=5, pady=5)

        # Create the pages (tabs) for each panel and add them to the notebook
        page1 = globals.notebook.add('Statistics')
        page2 = globals.notebook.add('Misc')
        page3 = globals.notebook.add('Skills')
        page4 = globals.notebook.add('Maneuvers')
        page5 = globals.notebook.add('Post Cap')
        page6 = globals.notebook.add('Loadout')

        #		page8 = globals.notebook.add('Summary')
        self.pages['Statistics'] = tkinter.Frame(page1, background="white")
        self.pages['Misc'] = tkinter.Frame(page2, background="white")
        self.pages['Skills'] = tkinter.Frame(page3, background="white")
        self.pages['Maneuvers'] = tkinter.Frame(page4, background="white")
        self.pages['Post Cap'] = tkinter.Frame(page5, background="white")
        self.pages['Loadout'] = tkinter.Frame(page6, background="white")

        #		self.pages['Summary'] = tkinter.Frame(page8, background="white")
        self.pages['Statistics'].grid(row=0, column=0)
        self.pages['Misc'].grid(row=0, column=2)
        self.pages['Skills'].grid(row=0, column=3)
        self.pages['Maneuvers'].grid(row=0, column=4)
        self.pages['Post Cap'].grid(row=0, column=5)
        self.pages['Loadout'].grid(row=0, column=6)
        #		self.pages['Summary'].grid(row=0, column=8)

        # Create each Panel. Each is added to the a global list so they can be referenced later
        globals.panels['Statistics'] = StP.StatisticsPanel(self.pages['Statistics'])
        globals.panels['Misc'] = MiP.Misc_Panel(self.pages['Misc'])
        globals.panels['Skills'] = SkP.Skills_Panel(self.pages['Skills'])
        globals.panels['Maneuvers'] = ManP.Maneuvers_Panel(self.pages['Maneuvers'])
        globals.panels['Post Cap'] = PcP.PostCap_Panel(self.pages['Post Cap'])
        globals.panels['Loadout'] = LdP.Loadout_Panel(self.pages['Loadout'])

        #		globals.panels['Summary'] = SumP.Summary_Panel(self.pages['Summary'])

        # Set up defaults
        globals.panels['Statistics'].change_race("Human")
        globals.panels['Statistics'].change_profession("Warrior")
        self.panels_loaded = 1

    # Temporary. This might be used to quickly hide or erase data from a Panel when it is hidden
    def Notebook_OnHidePage(self, caller):
        if self.panels_loaded == 1:
            print("hide")
            #self.pages[caller].grid_remove()

    def Planner_Onclose(self):
        if tkinter.messagebox.askokcancel("Quit", "Are you sure you want to quit? All unsaved data will be lost."):
            globals.root.withdraw()
            globals.root.after(1, globals.root.destroy())


# Monkey hack for High-DPI mice
def on_configure(e):
    if e.widget == globals.root:
        sleep(0.015)


# Start of the program. Unless the SQLite database exist it will exit. Otherwise, setup the database and create the Planner.

if __name__ == "__main__":
    if not os.path.isfile(globals.db_file):
        globals.root.title("It seems you have died, my friend.")
        tkinter.messagebox.showerror("Error",
                                     "GS4_Planner.db file not found.\n"
                                     "Please make sure GS4_Planner.db is in the same directory as Planner.exe")
    else:

        globals.db_con = sqlite3.connect(globals.db_file)
        globals.db_con.row_factory = sqlite3.Row
        globals.db_cur = globals.db_con.cursor()
        globals.root.title("%s %s - %s" % (globals.title, globals.version, globals.char_name))
        planner = Planner(globals.root)
        globals.root.bind("<Configure>", on_configure)
        globals.root.protocol("WM_DELETE_WINDOW", planner.Planner_Onclose)

        globals.root.mainloop()
