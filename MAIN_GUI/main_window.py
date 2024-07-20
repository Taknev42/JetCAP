"Later also try to add comments to the buttons in root2 window"

import os,sys
#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

import tkinter as tk
from tkinter.font import Font
from tkinter import ttk #package used to import themes
from TJ_window import TJ_window_class
from RJ_window import RJ_window_class
from TF_window import TF_window_class

class main_window_class:
    def __init__(self,selected_theme):
        self.selected_theme= selected_theme
    
    def toggle_mode(self):
        if self.selected_theme== "forest-light":  #exisiting theme is light
            self.style.theme_use('forest-dark')
            self.root1.configure(bg= '#313131')
            self.selected_theme= "forest-dark"
        else:
            self.style.theme_use('forest-light')
            self.root1.configure(bg= '#ffffff')
            self.selected_theme= "forest-light"
        self.style.configure("Custom.TButton", font=self.customFont)

    def open_TJ_window(self):
        self.root1.destroy()
        selected_theme= self.style.theme_use()
        TJ_window= TJ_window_class(selected_theme)
        TJ_window.create_TJ_window()

    def open_TF_window(self):
        self.root1.destroy()
        selected_theme= self.style.theme_use()
        TF_window= TF_window_class(selected_theme)
        TF_window.create_TF_window()

    def open_RJ_window(self):
        self.root1.destroy()
        selected_theme= self.style.theme_use()
        RJ_window= RJ_window_class(selected_theme)
        RJ_window.create_RJ_window()

    def create_window(self):
        #root1 window has three buttons side-by-side for the TJ,TF,RMJ along with a mode button in the bottom right corner
        self.root1= tk.Tk()    
        root1= self.root1
        #sizing the window
        root1.geometry("700x700")

        root1.resizable(True,True) #to prevent resizing of the window

        self.style = ttk.Style(root1)
        style= self.style
        # root1.tk.call('source', "\\".join(os.path.abspath(__file__).split("\\")[0:-1]) +"\\themes\\forest-light.tcl")  #basically we are taking the real path of this file and by "/" splitting we take the fornt part of its path and insert "/MAIN_BACKEND" to turn it into the MAIN_BACKEND directory 
        # root1.tk.call('source', "\\".join(os.path.abspath(__file__).split("\\")[0:-1]) +"\\themes\\forest-dark.tcl")
        root1.tk.call('source', resource_path("MAIN_GUI\\themes\\forest-light.tcl"))
        root1.tk.call('source', resource_path("MAIN_GUI\\themes\\forest-dark.tcl"))

        if self.selected_theme== "forest-light":
            style.theme_use('forest-light')
            root1.configure(bg= '#ffffff')   #background color of the window
        else:
            style.theme_use('forest-dark')
            root1.configure(bg= '#313131')

        #creating a frame
        frame= ttk.Frame(root1)
        frame.pack()

        # Step 1: Create a Font Object
        self.customFont = Font(family="Segoe Script", size=12, weight="bold")
        customFont= self.customFont

        # Step 2: Define a Custom Style
        style = ttk.Style()
        style.configure("Custom.TButton", font=customFont)

        #mode_switch widget
        self.mode_switch= ttk.Checkbutton(frame,text="Mode",style="Switch",command= self.toggle_mode)
        mode_switch= self.mode_switch
        mode_switch.grid(row=0,column=0,padx= 5, pady= 5,sticky=tk.E)

        #widgets_frame
        widgets_frame= ttk.LabelFrame(frame,text="Select engine")
        widgets_frame.grid(row=1,column= 0,padx= 20, pady= 10) 

        #turbojet button widget
        # turbojet_img= tk.PhotoImage(file="\\".join(os.path.abspath(__file__).split("\\")[0:-1]) +"\\images\\turbojet_img.png")
        turbojet_img= tk.PhotoImage(file=resource_path("MAIN_GUI\\images\\turbojet_img.png"))
        turbojet_img= turbojet_img.subsample(5,5)
        turbojet_button= ttk.Button(widgets_frame,text="TurboJet", style="Custom.TButton",image=turbojet_img,compound="top",command= self.open_TJ_window)
        turbojet_button.grid(row=0,column=0,padx= 5, pady= 5,sticky="ew")

        #Turbofan button widget
        # turbofan_img= tk.PhotoImage(file="\\".join(os.path.abspath(__file__).split("\\")[0:-1]) +"\\images\\turbofan_img.png")
        turbofan_img= tk.PhotoImage(file=resource_path("MAIN_GUI\\images\\turbofan_img.png"))
        turbofan_img= turbofan_img.subsample(5,5)
        turbofan_button= ttk.Button(widgets_frame,text="TurboFan", style="Custom.TButton",image=turbofan_img,compound='top',command= self.open_TF_window)    #,style="TButton"
        turbofan_button.grid(row=1,column=0,padx= 5, pady= 5,sticky="ew")

        #Ramjet button widget
        # ramjet_img= tk.PhotoImage(file="\\".join(os.path.abspath(__file__).split("\\")[0:-1]) +"\\images\\ramjet_img.png")
        ramjet_img= tk.PhotoImage(file=resource_path("MAIN_GUI\\images\\ramjet_img.png"))
        ramjet_img= ramjet_img.subsample(4,5)
        ramjet_button= ttk.Button(widgets_frame,text="RamJet", style="Custom.TButton",image=ramjet_img,compound="top",command= self.open_RJ_window)
        ramjet_button.grid(row=2,column=0,padx= 5, pady= 5,sticky="ew")


        root1.title("JetCAP")

        root1.mainloop()