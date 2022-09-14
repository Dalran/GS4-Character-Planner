# INDEX OF CLASSES AND METHODS
'''
class Planner
    def _init__(self, parent)
    def Create_Top_Menubar(self):
    def Menubar_Option_New_Character(self):
    def Menubar_Option_Load_Character(self):
    def Menubar_Option_Save_Character(self):
    def Create_Notebook(self, parent):
    def Notebook_OnShowPage(self, caller):
    def Notebook_OnHidePage(self, caller):
'''

# !/usr/bin/python
try:
    import sys

    import traceback
    import os
    import sqlite3
    import tkinter
    import Pmw
    import Globals as globals
    import Statistics_Panel as StP
    import Misc_Panel as MiP
    import Skills_Panel as SkP
    import Maneuvers_Panel as ManP
    import PostCap_Panel as PcP
    import Loadout_Panel as LdP
    import Progression_Panel as ProgP
    from time import sleep
    # import Summary_Panel as SumP
    from tkinter import messagebox
except:
    error_file = open('error log.txt', 'a')
    traceback.print_exc()
    traceback.print_exc(file=error_file)
    error_file.close()


# Planner is the primary window in the program that holds everything else.
# Planner is responsible for creating top Menubar and the Notebook used to store each Panel
class Planner:
    def __init__(self, parent):
        self.parent = parent
        self.pages = {}
        self.panels_loaded = 0

        # Create top Menubar used to Save and Load character builds
        self.Create_Top_Menubar()

        # Create the Notebook used to hold all the Panels and then create each Panel to be held in the Notebook
        self.Create_Notebook(self)

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
                                        raisecommand=self.Notebook_OnShowPage,
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
        page7 = globals.notebook.add('Progression')
        #		page8 = globals.notebook.add('Summary')
        self.pages['Statistics'] = tkinter.Frame(page1, background="white")
        self.pages['Misc'] = tkinter.Frame(page2, background="white")
        self.pages['Skills'] = tkinter.Frame(page3, background="white")
        self.pages['Maneuvers'] = tkinter.Frame(page4, background="white")
        self.pages['Post Cap'] = tkinter.Frame(page5, background="white")
        self.pages['Loadout'] = tkinter.Frame(page6, background="white")
        self.pages['Progression'] = tkinter.Frame(page7, background="white")
        #		self.pages['Summary'] = tkinter.Frame(page8, background="white")
        self.pages['Statistics'].grid(row=0, column=0)
        self.pages['Misc'].grid(row=0, column=2)
        self.pages['Skills'].grid(row=0, column=3)
        self.pages['Maneuvers'].grid(row=0, column=4)
        self.pages['Post Cap'].grid(row=0, column=5)
        self.pages['Loadout'].grid(row=0, column=6)
        self.pages['Progression'].grid(row=0, column=7)
        #		self.pages['Summary'].grid(row=0, column=8)

        # Create each Panel. Each is added to the a global list so they can be referenced later
        globals.panels['Statistics'] = StP.Statistics_Panel(self.pages['Statistics'])
        globals.panels['Misc'] = MiP.Misc_Panel(self.pages['Misc'])
        globals.panels['Skills'] = SkP.Skills_Panel(self.pages['Skills'])
        globals.panels['Maneuvers'] = ManP.Maneuvers_Panel(self.pages['Maneuvers'])
        globals.panels['Post Cap'] = PcP.PostCap_Panel(self.pages['Post Cap'])
        globals.panels['Loadout'] = LdP.Loadout_Panel(self.pages['Loadout'])
        globals.panels['Progression'] = ProgP.Progression_Panel(self.pages['Progression'])
        #		globals.panels['Summary'] = SumP.Summary_Panel(self.pages['Summary'])

        # Set up defaults
        globals.panels['Statistics'].Change_Race("Human")
        globals.panels['Statistics'].Change_Profession("Warrior")
        self.panels_loaded = 1

    # At this time, this function is used to clear the Progression panel if the Loadout panel
    # had it's data changed.
    def Notebook_OnShowPage(self, caller):
        if self.panels_loaded == 1:
            if caller == "Progression":
                if globals.LdP_Gear_List_Updated == 1:
                    globals.panels['Progression'].Plot_Graph_Clear()
                    globals.panels['Progression'].Gear_List_Populate_Lists()
                    globals.panels['Progression'].graph_option_category.set("Physical Combat")
                    globals.panels['Progression'].Graph_Option_Category_OnChange("Physical Combat")
                    globals.LdP_Gear_List_Updated = 0
                if globals.LdP_Effects_List_Updated == 1:
                    globals.panels['Progression'].Plot_Graph_Clear()
                    globals.panels['Progression'].Effects_List_Populate_List()
                    globals.panels['Progression'].graph_option_category.set("Physical Combat")
                    globals.panels['Progression'].Graph_Option_Category_OnChange("Physical Combat")
                    globals.LdP_Effects_List_Updated = 0

    # Temporary. This might be used to quickly hide or erase data from a Panel when it is hidden
    def Notebook_OnHidePage(self, caller):
        if self.panels_loaded == 1:
            print("hide")
            self.pages[caller].grid_remove()

    def Planner_Onclose(self):
        if tkinter.messagebox.askokcancel("Quit", "Are you sure you want to quit? All unsaved data will be lost."):
            globals.root.destroy()


def on_configure(e):
    if e.widget == globals.root:
        sleep(0.015)


# Start of the program. Unless the SQLite database exist it will exit. Otherwise, setup the database and create the Planner.

if __name__ == "__main__":
    try:
        if not os.path.isfile(globals.db_file):
            globals.root.title("It seems you have died, my friend.")
            tkinter.messagebox.showerror("Error",
                                         "GS4_Planner.db file not found.\nPlease make sure GS4_Planner.db is in the same directory as Planner.exe")
        else:
            globals.db_con = sqlite3.connect(globals.db_file)
            globals.db_con.row_factory = sqlite3.Row
            globals.db_cur = globals.db_con.cursor()
            globals.root.title("%s %s - %s" % (globals.title, globals.version, globals.char_name))
            planner = Planner(globals.root)
            globals.root.bind("<Configure>", on_configure)
            globals.root.protocol("WM_DELETE_WINDOW", planner.Planner_Onclose)

            globals.root.mainloop()
    except:
        error_file = open('error log.txt', 'a')
        traceback.print_exc()
        traceback.print_exc(file=error_file)
        error_file.close()
