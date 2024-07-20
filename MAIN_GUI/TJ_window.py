"""This class is used to store the code for the TurboJet window of the PCA-EPA software."""

import os,sys
#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from math import e,pow
import tkinter as tk
from tkinter import ttk                 #package used to import themes
from tkinter.font import Font
from PIL import Image, ImageTk          #PIL is Python Imaging Library also called Pillow          
from tkinter import messagebox
# from ..MAIN_BACKEND import initialisingComponents_file, plots_file   #'..' is used to refer to the folder which is in one level above the current directory. Since MAIN_BACKEND is with MAIN_GUI which is one level above the current directory, we use '..' to refer to MAIN_BACKEND
# sys.path.insert(0,"\\".join(os.path.abspath(__file__).split("\\")[:-2])+"\\MAIN_BACKEND")
sys.path.insert(0,resource_path("MAIN_BACKEND"))
from plots_file import plots                                         #type: ignore
from initialisingComponents_file import initialisingComponents       #type: ignore
from EPA_window import EPA_window_class                              #type: ignore
from tkinter import messagebox
# from .symbols import symbols                                   #type: ignore              #'.' is used to refer to children directory inside the current directory. Here from .symbols means refer to the symbols folder inside the current directory
# sys.path.insert(0,"\\".join(os.path.abspath(__file__).split("\\")[:-1])+"\\symbols")
sys.path.insert(0,resource_path("MAIN_GUI\\symbols"))
from symbols import get_symbol as syb                          #type: ignore


class TJ_window_class:

    def __init__(self,selected_theme):
        self.selected_theme= selected_theme
        self.var_bool= False
        self.inpt_outpt_selected_button= "input"      #/"output"  It helps us to know which button is selected
        self.single_multi_selected_button= "single"   #/"multi"  It helps us to know which button is selected



    def back_button_command(self):                              #used to go back to the main window
        self.root2.destroy()
        # Lazy import to avoid circular dependency
        from main_window import main_window_class
        main_gui= main_window_class(self.selected_theme)
        main_gui.create_window()



    def CD_C_switch_command(self):                                      #bcz we cant have two commands for the same switch
        if self.var_ConDiv_Con.get()=="C":
            self.CD_C_switch.invoke()                                   #Bcz we dont have Conv nozzle option for turbojet
            self.var_ConDiv_Con.set("CD")                                
            # self.CD_C_switch.config(text="Conv-Div")                  #uncomment them later
        else:
            pass
            # self.CD_C_switch.config(text="Conv")

    def epa_test_button_command(self):
        epa_test_window= EPA_window_class(self.selected_theme,self.engine)  #we also provide the ref Engine
        epa_test_window.create_EPA_window() 

    def get_T0_P0_from_alt(self,altitude):                  
            # Constants
            To = 288.16  # Standard temperature at sea level in K
            Po = 101325  # Standard pressure at sea level in Pa
            L = 0.0065   # Temperature lapse rate in K/m
            R = 287.05   # Specific gas constant for dry air in J/(kg·K)
            g = 9.80665  # gravity
            M = 0.02896968 # Molar mass of dry air (kg/mol)
            Lo = 0.00976 # temperature lapse rate used for pressure (K/m)
            Ro = 8.314462618 # universal gas constant (J/(mol.K))

            if altitude < 0:
                altitude= 0

            if altitude < 11000:
                T = To - L * altitude
            elif altitude > 11000 and altitude < 25000:
                T = 216.67
            else:
                T = 216.7    
            P = Po*((1 - Lo*altitude/To)**(g*M/(Ro*Lo)))

            return (T,P)
    
    def on_enter_alt_entry(self,event):                                 #command when the user presses enter after entering the altitude
        # Constants
        To = 288.16  # Standard temperature at sea level in K
        Po = 101325  # Standard pressure at sea level in Pa
        L = 0.0065   # Temperature lapse rate in K/m
        R = 287.05   # Specific gas constant for dry air in J/(kg·K)
        g = 9.80665  # gravity
        M = 0.02896968 # Molar mass of dry air (kg/mol)
        Lo = 0.00976 # temperature lapse rate used for pressure (K/m)
        Ro = 8.314462618 # universal gas constant (J/(mol.K))


        altitude= float(self.alt_entry.get())
        if altitude < 0:
            messagebox.showerror("Error","Altitude cannot be negative")
            return
        if altitude < 11000:
            T = To - L * altitude
        elif altitude > 11000 and altitude < 25000:
            T = 216.67
        else:
            T = 216.7       #we set a constant temperature for altitudes above 25000m indicating the limitations of our temperature altitude predictor
        P = Po*((1 - Lo*altitude/To)**(g*M/(Ro*Lo)))

        self.temperature_entry.delete(0,'end')  
        self.temperature_entry.insert(0,round(T,4))
        self.pressure_entry.delete(0,'end')
        self.pressure_entry.insert(0,round(P/1e+3,4))


    def reset_parameters_widgets_frame(self,event=None):        #event=None is added bcz when we call this function from bind it will pass an event argument
        """This function is used to reset the widgets of the parameters_widgets_frame everytime there is a change in the widgets of the main widgets frame."""
        for item in self.parameters_widgets_frame.winfo_children():
            item.destroy()

        parameters_widgets_frame= self.parameters_widgets_frame

        new_width= 5 #width of the entry widgets

    #atmosphere conditions widgets frame  inside parameters_widgets_frame
        atmosphere_widgets_frame= ttk.LabelFrame(parameters_widgets_frame,text="Atmospheric Conditions")
        atmosphere_widgets_frame.grid(column=0,row=0,padx= 5, pady= 5,sticky='new')
        row_num=0

        set_T0_P0_to_None= False         #when alt is selected as independent variable then we set T0 and P0 to None

        #altitude_entry widget inside atmsophere_widgets_frame
        if self.single_multi_selected_button=="multi" and ((self.onetwo_indp_var.get()=="one" and "alt" in [self.indep_var_entry_combobox.get()]) or (self.onetwo_indp_var.get()=="two" and "alt" in [self.indep_var1_entry_combobox.get(),self.indep_var2_entry_combobox.get()])) :
            alt_label= ttk.Label(atmosphere_widgets_frame,text= "Altitude (m)")
            alt_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")

            self.alt_iter_frame= ttk.Frame(atmosphere_widgets_frame)
            alt_iter_frame= self.alt_iter_frame
            alt_iter_frame.grid(row=row_num,column=1,padx= 0,pady=0,sticky="ew")
            self.min_alt_entry= ttk.Entry(alt_iter_frame)
            min_alt_entry= self.min_alt_entry
            min_alt_entry.grid(row=0,column=0,padx= 0,pady=(0,5),sticky="w")
            if self.var_bool:
                min_alt_entry.insert(0,min_alt_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                min_alt_entry.insert(0,min_alt)
            else:
                min_alt_entry.insert(0,"Min")
            min_alt_entry.bind("<FocusIn>",lambda args: min_alt_entry.delete('0','end'))
            min_alt_entry.config(width=new_width)
            self.steps_alt_entry= ttk.Spinbox(alt_iter_frame,from_= 0,to= 1000)
            steps_alt_entry= self.steps_alt_entry
            steps_alt_entry.grid(row=0,column=1,padx= 0,pady=(0,5),sticky="ew")
            if self.var_bool:
                steps_alt_entry.insert(0,steps_alt_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                steps_alt_entry.insert(0,steps_alt)
            else:
                steps_alt_entry.insert(0,"Steps")
            steps_alt_entry.bind("<FocusIn>",lambda args: steps_alt_entry.delete('0','end'))
            steps_alt_entry.config(width=new_width)
            self.max_alt_entry= ttk.Entry(alt_iter_frame)
            max_alt_entry= self.max_alt_entry
            max_alt_entry.grid(row=0,column=2,padx= 0,pady=(0,5),sticky="e")
            if self.var_bool:
                max_alt_entry.insert(0,max_alt_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                max_alt_entry.insert(0,max_alt)
            else:
                max_alt_entry.insert(0,"Max")
            max_alt_entry.bind("<FocusIn>",lambda args: max_alt_entry.delete('0','end'))
            max_alt_entry.config(width=new_width)
            row_num+=1  

            set_T0_P0_to_None= True

        else :    #if single point calculation is selected or if multi point then user has not selected alt as independent variable
            alt_label= ttk.Label(atmosphere_widgets_frame,text= "Altitude (m)")
            alt_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="nsew")
            self.alt_entry= ttk.Entry(atmosphere_widgets_frame)
            alt_entry= self.alt_entry
            if self.var_bool:
                alt_entry.insert(0,alt_default)
            elif self.inpt_outpt_selected_button=="output" and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):  #hasattr(self,"engine") is also added bcz user may enter incorrect inputs and click outputs and then try to come back to inputs
                alt_entry.insert(0,alt)
            else: 
                alt_entry.insert(0,"Altitude (m)")
            alt_entry.bind("<FocusIn>",lambda args: alt_entry.delete('0','end'))
            alt_entry.bind('<Return>',self.on_enter_alt_entry)
            alt_entry.grid(row=0,column=1,padx= 5,pady=(0,5),sticky="nsew")
            row_num+=1


        #atmosphere_temperature_entry widget inside atmsophere_widgets_frame
        temperature_label= ttk.Label(atmosphere_widgets_frame,text= "Temperature T0 (K)")
        temperature_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="nsew")
        self.temperature_entry= ttk.Entry(atmosphere_widgets_frame)
        temperature_entry= self.temperature_entry
        if set_T0_P0_to_None:
            temperature_entry.insert(0,"NA")
        elif self.var_bool:
            temperature_entry.insert(0,T0_default)
        elif self.inpt_outpt_selected_button=="output" and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):   #hasattr(self,"engine") is also added bcz user may enter incorrect inputs and click outputs and then try to come back to inputs
            temperature_entry.insert(0,T0)
        else: 
            temperature_entry.insert(0,"Temperature (K)")
        temperature_entry.bind("<FocusIn>",lambda args: temperature_entry.delete('0','end'))
        temperature_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="nsew")
        row_num+=1

        #atmosphere_pressure_entry widget inside atmsophere_widgets_frame
        pressure_label= ttk.Label(atmosphere_widgets_frame,text= "Pressure P0 (kPa)")
        pressure_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="nsew")
        self.pressure_entry= ttk.Entry(atmosphere_widgets_frame)
        pressure_entry= self.pressure_entry
        if set_T0_P0_to_None:
            pressure_entry.insert(0,"NA")
        elif self.var_bool:
            pressure_entry.insert(0,P0_default)
        elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
            if type(P0)==float:
                pressure_entry.insert(0,P0/1e+3)
            else:
                pressure_entry.insert(0,'-')
        else:
            pressure_entry.insert(0,"Pressure (Pa)")
        pressure_entry.bind("<FocusIn>",lambda args: pressure_entry.delete('0','end'))
        pressure_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="nsew")
        row_num+=1


        #machnumber_entry widget inside atmsophere_widgets_frame
        if self.single_multi_selected_button=="multi" and ((self.onetwo_indp_var.get()=="one" and "M0" in [self.indep_var_entry_combobox.get()]) or (self.onetwo_indp_var.get()=="two" and "M0" in [self.indep_var1_entry_combobox.get(),self.indep_var2_entry_combobox.get()])) :
            M0_label= ttk.Label(atmosphere_widgets_frame,text= "Mach Number M0")
            M0_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")

            self.M0_iter_frame= ttk.Frame(atmosphere_widgets_frame)
            M0_iter_frame= self.M0_iter_frame
            M0_iter_frame.grid(row=row_num,column=1,padx= 0,pady=0,sticky="ew")
            self.min_M0_entry= ttk.Entry(M0_iter_frame)
            min_M0_entry= self.min_M0_entry
            min_M0_entry.grid(row=0,column=0,padx= 0,pady=(0,5),sticky="w")
            if self.var_bool:
                min_M0_entry.insert(0,min_M0_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                min_M0_entry.insert(0,min_M0)
            else:
                min_M0_entry.insert(0,"Min")
            min_M0_entry.bind("<FocusIn>",lambda args: min_M0_entry.delete('0','end'))
            min_M0_entry.config(width=new_width)
            self.steps_M0_entry= ttk.Spinbox(M0_iter_frame,from_= 0,to= 1000)
            steps_M0_entry= self.steps_M0_entry
            steps_M0_entry.grid(row=0,column=1,padx= 0,pady=(0,5),sticky="ew")
            if self.var_bool:
                steps_M0_entry.insert(0,steps_M0_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                steps_M0_entry.insert(0,steps_M0)
            else:
                steps_M0_entry.insert(0,"Steps")
            steps_M0_entry.bind("<FocusIn>",lambda args: steps_M0_entry.delete('0','end'))
            steps_M0_entry.config(width=new_width)
            self.max_M0_entry= ttk.Entry(M0_iter_frame)
            max_M0_entry= self.max_M0_entry
            max_M0_entry.grid(row=0,column=2,padx= 0,pady=(0,5),sticky="e")
            if self.var_bool:
                max_M0_entry.insert(0,max_M0_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                max_M0_entry.insert(0,max_M0)
            else:
                max_M0_entry.insert(0,"Max")
            max_M0_entry.bind("<FocusIn>",lambda args: max_M0_entry.delete('0','end'))
            max_M0_entry.config(width=new_width)
            row_num+=1  

        else :    #if single point calculation is selected or if multi point then user has not selected Tt4 as independent variable
            M0_label= ttk.Label(atmosphere_widgets_frame,text= "Mach Number M0")
            M0_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="nsew")
            self.M0_entry= ttk.Entry(atmosphere_widgets_frame)
            M0_entry= self.M0_entry
            if self.var_bool:
                M0_entry.insert(0,M0_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                M0_entry.insert(0,M0)
            else:
                M0_entry.insert(0,"Mach Number")
            M0_entry.bind("<FocusIn>",lambda args: M0_entry.delete('0','end'))
            M0_entry.grid(row=row_num, column=1, padx= 5,pady=(0,5),sticky="nsew")
            row_num+=1


    #fuel/air properties widgets frame inside parameters_widgets_frame
        fuel_air_widgets_frame= ttk.LabelFrame(parameters_widgets_frame,text="Fuel/Air Properties")
        fuel_air_widgets_frame.grid(column=0,row=1,padx= 5, pady= 5,sticky='new')
        row_num= 0

        #gam_c_entry widget inside fuel_air_widgets_frame
        gam_c_label= ttk.Label(fuel_air_widgets_frame,text= syb("gam_c"))
        gam_c_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
        self.gam_c_entry= ttk.Entry(fuel_air_widgets_frame)
        gam_c_entry= self.gam_c_entry
        if self.var_bool:
            gam_c_entry.insert(0,gam_c_default)
        elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
            gam_c_entry.insert(0,gam_c)
        else:
            gam_c_entry.insert(0,syb("gam_c"))
        gam_c_entry.bind("<FocusIn>",lambda args: gam_c_entry.delete('0','end'))
        gam_c_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
        row_num+=1

        if self.var_ideal_real.get()=="real":
            #gam_t_entry widget inside fuel_air_widgets_frame
            gam_t_label= ttk.Label(fuel_air_widgets_frame,text= syb("gam_t"))
            gam_t_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.gam_t_entry= ttk.Entry(fuel_air_widgets_frame)
            gam_t_entry= self.gam_t_entry
            if self.var_bool:
                gam_t_entry.insert(0,gam_t_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                gam_t_entry.insert(0,gam_t)
            else:
                gam_t_entry.insert(0,syb("gam_t"))
            gam_t_entry.bind("<FocusIn>",lambda args: gam_t_entry.delete('0','end'))
            gam_t_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1
            
            if self.var_AB.get()=="Y":
                #gam_ab_entry widget inside fuel_air_widgets_frame
                gam_ab_label= ttk.Label(fuel_air_widgets_frame,text= syb("gam_ab"))
                gam_ab_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
                self.gam_ab_entry= ttk.Entry(fuel_air_widgets_frame)
                gam_ab_entry= self.gam_ab_entry
                if self.var_bool:
                    gam_ab_entry.insert(0,gam_ab_default)
                elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                    gam_ab_entry.insert(0,gam_ab)
                else:
                    gam_ab_entry.insert(0,syb("gam_ab"))
                gam_ab_entry.bind("<FocusIn>",lambda args: gam_ab_entry.delete('0','end'))
                gam_ab_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
                row_num+=1


        #Cpc_entry widget inside fuel_air_widgets_frame
        Cpc_label= ttk.Label(fuel_air_widgets_frame,text= syb("Cpc")+ " (J/kg-K)")
        Cpc_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
        self.Cpc_entry= ttk.Entry(fuel_air_widgets_frame)
        Cpc_entry= self.Cpc_entry
        if self.var_bool:
            Cpc_entry.insert(0,Cpc_default)
        elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
            Cpc_entry.insert(0,Cpc)
        else:
            Cpc_entry.insert(0,syb("Sp. Heat Cap. Compressor"))
        Cpc_entry.bind("<FocusIn>",lambda args: Cpc_entry.delete('0','end'))
        Cpc_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
        row_num+=1

        if self.var_ideal_real.get()=="real":
            #Cpt_entry widget inside fuel_air_widgets_frame
            Cpt_label= ttk.Label(fuel_air_widgets_frame,text= syb("Cpt")+" (J/kg-K)")
            Cpt_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.Cpt_entry= ttk.Entry(fuel_air_widgets_frame)
            Cpt_entry= self.Cpt_entry
            if self.var_bool:
                Cpt_entry.insert(0,Cpt_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                Cpt_entry.insert(0,Cpt)
            else:
                Cpt_entry.insert(0,syb("Sp. Heat Cap. Turbine"))
            Cpt_entry.bind("<FocusIn>",lambda args: Cpt_entry.delete('0','end'))
            Cpt_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew") 
            row_num+=1

            if self.var_AB.get()=="Y":
                #Cpab_entry widget inside fuel_air_widgets_frame
                Cpab_label= ttk.Label(fuel_air_widgets_frame,text= syb("Cpab")+ " (J/kg-K)")
                Cpab_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
                self.Cpab_entry= ttk.Entry(fuel_air_widgets_frame)
                Cpab_entry= self.Cpab_entry
                if self.var_bool:
                    Cpab_entry.insert(0,Cpab_default)
                elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                    Cpab_entry.insert(0,Cpab)
                else:
                    Cpab_entry.insert(0,syb("Sp. Heat Cap. Afterburner"))
                Cpab_entry.bind("<FocusIn>",lambda args: Cpab_entry.delete('0','end'))
                Cpab_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
                row_num+=1

        #Hpr_entry widget inside fuel_air_widgets_frame
        Hpr_label= ttk.Label(fuel_air_widgets_frame,text= syb("Hpr")+ " (kJ/kg)")
        Hpr_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
        self.Hpr_entry= ttk.Entry(fuel_air_widgets_frame)
        Hpr_entry= self.Hpr_entry
        if self.var_bool:
            Hpr_entry.insert(0,Hpr_default)
        elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
            if type(Hpr)==float:
                Hpr_entry.insert(0,Hpr/1e+3)
            else:
                Hpr_entry.insert(0,'-')
        else:
            Hpr_entry.insert(0,"Sp. Heat of Reaction")
        Hpr_entry.bind("<FocusIn>",lambda args: Hpr_entry.delete('0','end'))
        Hpr_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
        row_num+=1

    #Total temperature widget frame
        Total_temp_widgets_frame= ttk.LabelFrame(parameters_widgets_frame,text="Total Temperature Limits")
        Total_temp_widgets_frame.grid(column=0,row=2,padx= 5, pady= 5,sticky='new')
        row_num= 0

        #Tt4_entry widget inside Total_temp_widgets_frame
        if self.single_multi_selected_button=="multi" and ((self.onetwo_indp_var.get()=="one" and "Tt4" in [self.indep_var_entry_combobox.get()]) or (self.onetwo_indp_var.get()=="two" and "Tt4" in [self.indep_var1_entry_combobox.get(),self.indep_var2_entry_combobox.get()])) :
            Tt4_label= ttk.Label(Total_temp_widgets_frame,text= "Tt4 (K)")
            Tt4_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")

            self.Tt4_iter_frame= ttk.Frame(Total_temp_widgets_frame)
            Tt4_iter_frame= self.Tt4_iter_frame
            Tt4_iter_frame.grid(row=row_num,column=1,padx= 0,pady=0,sticky="ew")
            self.min_Tt4_entry= ttk.Entry(Tt4_iter_frame)
            min_Tt4_entry= self.min_Tt4_entry
            min_Tt4_entry.grid(row=0,column=0,padx= 0,pady=(0,5),sticky="w")
            if self.var_bool:
                min_Tt4_entry.insert(0,min_Tt4_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                min_Tt4_entry.insert(0,min_Tt4)
            else:
                min_Tt4_entry.insert(0,"Min")
            min_Tt4_entry.bind("<FocusIn>",lambda args: min_Tt4_entry.delete('0','end'))
            min_Tt4_entry.config(width=new_width)
            self.steps_Tt4_entry= ttk.Spinbox(Tt4_iter_frame,from_= 0,to= 1000)
            steps_Tt4_entry= self.steps_Tt4_entry
            steps_Tt4_entry.grid(row=0,column=1,padx= 0,pady=(0,5),sticky="ew")
            if self.var_bool:
                steps_Tt4_entry.insert(0,steps_Tt4_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                steps_Tt4_entry.insert(0,steps_Tt4)
            else:
                steps_Tt4_entry.insert(0,"Steps")
            steps_Tt4_entry.bind("<FocusIn>",lambda args: steps_Tt4_entry.delete('0','end'))
            steps_Tt4_entry.config(width=new_width)
            self.max_Tt4_entry= ttk.Entry(Tt4_iter_frame)
            max_Tt4_entry= self.max_Tt4_entry
            max_Tt4_entry.grid(row=0,column=2,padx= 0,pady=(0,5),sticky="e")
            if self.var_bool:
                max_Tt4_entry.insert(0,max_Tt4_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                max_Tt4_entry.insert(0,max_Tt4)
            else:
                max_Tt4_entry.insert(0,"Max")
            max_Tt4_entry.bind("<FocusIn>",lambda args: max_Tt4_entry.delete('0','end'))
            max_Tt4_entry.config(width=new_width)

            row_num+=1  
        else :    #if single point calculation is selected or if multi point then user has not selected Tt4 as independent variable
            Tt4_label= ttk.Label(Total_temp_widgets_frame,text= "Tt4 (K)")
            Tt4_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.Tt4_entry= ttk.Entry(Total_temp_widgets_frame)
            Tt4_entry= self.Tt4_entry
            if self.var_bool:
                Tt4_entry.insert(0,Tt4_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                Tt4_entry.insert(0,Tt4)
            else:
                Tt4_entry.insert(0,"Turbine inlet temperature")
            Tt4_entry.bind("<FocusIn>",lambda args: Tt4_entry.delete('0','end'))
            Tt4_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1
        
        if self.var_AB.get()=="Y":
            #Tt7_entry widget inside Total_temp_widgets_frame
            Tt7_label= ttk.Label(Total_temp_widgets_frame,text= "Tt7 (K)")
            Tt7_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.Tt7_entry= ttk.Entry(Total_temp_widgets_frame)
            Tt7_entry= self.Tt7_entry
            if self.var_bool:
                Tt7_entry.insert(0,Tt7_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                Tt7_entry.insert(0,Tt7)
            else:
                Tt7_entry.insert(0,"Afterburner exit temperature")
            Tt7_entry.bind("<FocusIn>",lambda args: Tt7_entry.delete('0','end'))
            Tt7_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1

        widget_frame_row_num=0
        if self.var_ideal_real.get()=="real":
        #efficiencies widgets frame inside parameters_widgets_frame
            efficiencies_widgets_frame= ttk.LabelFrame(parameters_widgets_frame,text="Efficiencies")
            efficiencies_widgets_frame.grid(column=1,row=widget_frame_row_num,padx= 5, pady= 5,sticky='new')
            widget_frame_row_num+=1
            row_num= 0

            #eta_b_entry widget inside efficiencies_widgets_frame
            eta_b_label= ttk.Label(efficiencies_widgets_frame,text= syb("eta_b"))
            eta_b_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.eta_b_entry= ttk.Entry(efficiencies_widgets_frame)
            eta_b_entry= self.eta_b_entry
            if self.var_bool:
                eta_b_entry.insert(0,eta_b_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                eta_b_entry.insert(0,eta_b)
            else:
                eta_b_entry.insert(0,"Burner efficiency")
            eta_b_entry.bind("<FocusIn>",lambda args: eta_b_entry.delete('0','end'))
            eta_b_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1

            #eta_m_entry widget inside efficiencies_widgets_frame
            eta_m_label= ttk.Label(efficiencies_widgets_frame,text= syb("eta_m"))
            eta_m_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.eta_m_entry= ttk.Entry(efficiencies_widgets_frame)
            eta_m_entry= self.eta_m_entry
            if self.var_bool:
                eta_m_entry.insert(0,eta_m_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                eta_m_entry.insert(0,eta_m)
            else:
                eta_m_entry.insert(0,"Mechanical efficiency")
            eta_m_entry.bind("<FocusIn>",lambda args: eta_m_entry.delete('0','end'))
            eta_m_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1

            if self.var_AB.get()=="Y":
                #eta_ab_entry widget inside efficiencies_widgets_frame
                eta_ab_label= ttk.Label(efficiencies_widgets_frame,text= syb("eta_ab"))
                eta_ab_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
                self.eta_ab_entry= ttk.Entry(efficiencies_widgets_frame)
                eta_ab_entry= self.eta_ab_entry
                if self.var_bool:
                    eta_ab_entry.insert(0,eta_ab_default)
                elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                    eta_ab_entry.insert(0,eta_ab)
                else:
                    eta_ab_entry.insert(0,"Afterburner efficiency")
                eta_ab_entry.bind("<FocusIn>",lambda args: eta_ab_entry.delete('0','end'))
                eta_ab_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
                row_num+=1

            #polytropic eff widget inside efficiencies_widgets_frame
            peta_c_label= ttk.Label(efficiencies_widgets_frame,text= syb("peta_c"))
            peta_c_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.peta_c_entry= ttk.Entry(efficiencies_widgets_frame)
            peta_c_entry= self.peta_c_entry
            if self.var_bool:
                peta_c_entry.insert(0,peta_c_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                peta_c_entry.insert(0,peta_c)
            else:
                peta_c_entry.insert(0,"Polytropic eff compressor")
            peta_c_entry.bind("<FocusIn>",lambda args: peta_c_entry.delete('0','end'))
            peta_c_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1

            #polytropic eff widget inside efficiencies_widgets_frame
            peta_t_label= ttk.Label(efficiencies_widgets_frame,text= syb("peta_t"))
            peta_t_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.peta_t_entry= ttk.Entry(efficiencies_widgets_frame)
            peta_t_entry= self.peta_t_entry
            if self.var_bool:
                peta_t_entry.insert(0,peta_t_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                peta_t_entry.insert(0,peta_t)
            else:
                peta_t_entry.insert(0,"Polytropic eff turbine")
            peta_t_entry.bind("<FocusIn>",lambda args: peta_t_entry.delete('0','end'))
            peta_t_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1

    #Pressures ratios widgets frame inside parameters_widgets_frame
        pressures_ratios_widgets_frame= ttk.LabelFrame(parameters_widgets_frame,text="Pressures Ratios (PR)")
        pressures_ratios_widgets_frame.grid(column=1,row=widget_frame_row_num,padx= 5, pady= 5,sticky='new')
        widget_frame_row_num+=1
        row_num= 0


        #pi_c_entry widget inside pressures_ratios_widgets_frame
        if self.single_multi_selected_button=="multi" and ((self.onetwo_indp_var.get()=="one" and "pi_c" in [self.indep_var_entry_combobox.get()]) or (self.onetwo_indp_var.get()=="two" and "pi_c" in [self.indep_var1_entry_combobox.get(),self.indep_var2_entry_combobox.get()])):
            pi_c_label= ttk.Label(pressures_ratios_widgets_frame,text= syb("pi_c"))
            pi_c_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")

            self.pi_c_iter_frame= ttk.Frame(pressures_ratios_widgets_frame)
            pi_c_iter_frame= self.pi_c_iter_frame
            pi_c_iter_frame.grid(row=row_num,column=1,padx= 0,pady=0,sticky="ew")
            self.min_pi_c_entry= ttk.Entry(pi_c_iter_frame)
            min_pi_c_entry= self.min_pi_c_entry
            min_pi_c_entry.grid(row=0,column=0,padx= 0,pady=(0,5),sticky="w")
            if self.var_bool:
                min_pi_c_entry.insert(0,min_pi_c_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                min_pi_c_entry.insert(0,min_pi_c)
            else:
                min_pi_c_entry.insert(0,"Min")
            min_pi_c_entry.bind("<FocusIn>",lambda args: min_pi_c_entry.delete('0','end'))
            min_pi_c_entry.config(width=new_width)
            self.steps_pi_c_entry= ttk.Spinbox(pi_c_iter_frame,from_= 0,to= 1000)
            steps_pi_c_entry= self.steps_pi_c_entry
            steps_pi_c_entry.grid(row=0,column=1,padx= 0,pady=(0,5),sticky="ew")
            if self.var_bool:
                steps_pi_c_entry.insert(0,steps_pi_c_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                steps_pi_c_entry.insert(0,steps_pi_c)
            else:
                steps_pi_c_entry.insert(0,"Steps")
            steps_pi_c_entry.bind("<FocusIn>",lambda args: steps_pi_c_entry.delete('0','end'))
            steps_pi_c_entry.config(width=new_width)
            self.max_pi_c_entry= ttk.Entry(pi_c_iter_frame)
            max_pi_c_entry= self.max_pi_c_entry
            max_pi_c_entry.grid(row=0,column=2,padx= 0,pady=(0,5),sticky="e")
            if self.var_bool:
                max_pi_c_entry.insert(0,max_pi_c_default)
            elif self.inpt_outpt_selected_button=="output"and hasattr(self,"parameters_dict"):
                max_pi_c_entry.insert(0,max_pi_c)
            else:
                max_pi_c_entry.insert(0,"Max")
            max_pi_c_entry.bind("<FocusIn>",lambda args: max_pi_c_entry.delete('0','end'))
            max_pi_c_entry.config(width=new_width)

            row_num+=1
        else :
            pi_c_label= ttk.Label(pressures_ratios_widgets_frame,text= syb("pi_c"))
            pi_c_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.pi_c_entry= ttk.Entry(pressures_ratios_widgets_frame)
            pi_c_entry= self.pi_c_entry
            if self.var_bool:
                pi_c_entry.insert(0,pi_c_default)
            elif self.inpt_outpt_selected_button== "output" and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                pi_c_entry.insert(0,pi_c)
            else:
                pi_c_entry.insert(0,"Compressor PR")
            pi_c_entry.bind("<FocusIn>",lambda args: pi_c_entry.delete('0','end'))
            pi_c_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1

        if self.var_single_dual.get()=="dual":
            #pi_cL_entry widget inside pressures_ratios_widgets_frame
            pi_cL_label= ttk.Label(pressures_ratios_widgets_frame,text= syb("pi_cL"))
            pi_cL_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.pi_cL_entry= ttk.Entry(pressures_ratios_widgets_frame)
            pi_cL_entry= self.pi_cL_entry
            if self.var_bool:
                pi_cL_entry.insert(0,pi_cL_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                pi_cL_entry.insert(0,pi_cL)
            else:
                pi_cL_entry.insert(0,"Low compressor PR")
            pi_cL_entry.bind("<FocusIn>",lambda args: pi_cL_entry.delete('0','end'))
            pi_cL_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1

        if self.var_ideal_real.get()=="real":
            #pi_d_max_entry widget inside pressures_ratios_widgets_frame
            pi_d_max_label= ttk.Label(pressures_ratios_widgets_frame,text= syb("pi_d_max"))
            pi_d_max_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.pi_d_max_entry= ttk.Entry(pressures_ratios_widgets_frame)
            pi_d_max_entry= self.pi_d_max_entry
            if self.var_bool:
                pi_d_max_entry.insert(0,pi_d_max_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                pi_d_max_entry.insert(0,pi_d_max)
            else:
                pi_d_max_entry.insert(0,"max Diffuser PR")
            pi_d_max_entry.bind("<FocusIn>",lambda args: pi_d_max_entry.delete('0','end'))
            pi_d_max_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1

            #pi_b_entry widget inside pressures_ratios_widgets_frame
            pi_b_label= ttk.Label(pressures_ratios_widgets_frame,text= syb("pi_b"))
            pi_b_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.pi_b_entry= ttk.Entry(pressures_ratios_widgets_frame)
            pi_b_entry= self.pi_b_entry
            if self.var_bool:
                pi_b_entry.insert(0,pi_b_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                pi_b_entry.insert(0,pi_b)
            else:
                pi_b_entry.insert(0,"Burner PR")
            pi_b_entry.bind("<FocusIn>",lambda args: pi_b_entry.delete('0','end'))
            pi_b_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1

            if self.var_AB.get()=="Y":
                #pi_ab_entry widget inside pressures_ratios_widgets_frame
                pi_ab_label= ttk.Label(pressures_ratios_widgets_frame,text= syb("pi_ab"))
                pi_ab_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
                self.pi_ab_entry= ttk.Entry(pressures_ratios_widgets_frame)
                pi_ab_entry= self.pi_ab_entry
                if self.var_bool:
                    pi_ab_entry.insert(0,pi_ab_default)
                elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                    pi_ab_entry.insert(0,pi_ab)
                else:
                    pi_ab_entry.insert(0,"Afterburner PR")
                pi_ab_entry.bind("<FocusIn>",lambda args: pi_ab_entry.delete('0','end'))
                pi_ab_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
                row_num+=1

            #pi_n_entry widget inside pressures_ratios_widgets_frame
            pi_n_label= ttk.Label(pressures_ratios_widgets_frame,text= syb("pi_n"))
            pi_n_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.pi_n_entry= ttk.Entry(pressures_ratios_widgets_frame)
            pi_n_entry= self.pi_n_entry
            if self.var_bool:
                pi_n_entry.insert(0,pi_n_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                pi_n_entry.insert(0,pi_n)
            else:
                pi_n_entry.insert(0,"Nozzle PR")
            pi_n_entry.bind("<FocusIn>",lambda args: pi_n_entry.delete('0','end'))
            pi_n_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="ew")
            row_num+=1

        
        if self.var_ConDiv_Con.get() == "CD":
        #nozzle_properties widgets frame inside parameters_widgets_frame
            nozzle_properties_widgets_frame= ttk.LabelFrame(parameters_widgets_frame,text="Nozzle Properties")
            nozzle_properties_widgets_frame.grid(column=1,row=widget_frame_row_num,padx= 5, pady= 5,sticky='new')
            widget_frame_row_num+=1

            #P0/P9_entry widget inside nozzle_properties_widgets_frame
            P0_P9_label= ttk.Label(nozzle_properties_widgets_frame,text= "P0/P9")
            P0_P9_label.grid(row=0,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.P0_P9_entry= ttk.Entry(nozzle_properties_widgets_frame)
            P0_P9_entry= self.P0_P9_entry
            if self.var_bool:
                P0_P9_entry.insert(0,P0_P9_default)
            elif self.inpt_outpt_selected_button=="output"and (hasattr(self,"engine") or hasattr(self,"parameters_dict")):
                P0_P9_entry.insert(0,P0_P9)
            else:
                P0_P9_entry.insert(0,"P0/P9")
            P0_P9_entry.bind("<FocusIn>",lambda args: P0_P9_entry.delete('0','end'))
            P0_P9_entry.grid(row=0,column=1,padx= 5,pady=(0,5),sticky="ew") 



    def set_default_values(self):

        #setting the default values
        global engineType_default,AB_default,alt_default,T0_default,P0_default,M0_default,M6_default,alp_default,gam_c_default,gam_t_default,gam_ab_default,Rc_default,Rt_default,Rab_default,Cpc_default,Cpt_default,Cpab_default,Tt4_default,Tt7_default,Hpr_default,eta_b_default,eta_m_default,eta_ab_default,pi_d_max_default,pi_f_default,pi_c_default,pi_cL_default,pi_cH_default,pi_b_default,pi_m_max_default,pi_ab_default,pi_n_default,pi_fn_default,peta_f_default,peta_c_default,peta_t_default,P0_P9_default,P0_P19_default,sep_mixed_flow_default,nozzleType_default
        global min_Tt4_default,steps_Tt4_default,max_Tt4_default
        global min_pi_c_default,steps_pi_c_default,max_pi_c_default
        global min_alt_default,steps_alt_default,max_alt_default
        global min_M0_default,steps_M0_default,max_M0_default

        engineType_default= "turbojet"
        AB_default= "N"
        if self.single_multi_selected_button=="single":
            alt_default= 11000
        else:
            alt_default= 11000  #bcz what if it is not selected as independent variable
            min_alt_default= 0
            steps_alt_default= 5
            max_alt_default= 11000
        T0_default= 216.7
        P0_default= 19.8157
        if self.single_multi_selected_button=="single":
            M0_default= 1.6
        else:
            M0_default= 1.6   #bcz what if it is not selected as independent variable
            min_M0_default= 0.5
            steps_M0_default= 5
            max_M0_default= 1.5
        M6_default= "NA"
        alp_default= 0
        gam_c_default= 1.4
        gam_t_default= 1.3
        gam_ab_default= 1.3
        Rc_default= 287.094
        Rt_default= 285.024
        Rab_default= 285.024
        Cpc_default= 1004.832
        Cpt_default= 1235.106
        Cpab_default= 1235.106
        if self.single_multi_selected_button=="single":
            Tt4_default= 1800
        else:
            Tt4_default= 1800   #bcz what if it is not selected as independent variable
            min_Tt4_default= 1500
            steps_Tt4_default= 5
            max_Tt4_default= 1900
        Tt7_default= 2000
        Hpr_default= 42800e+3/1e+3
        eta_b_default= 0.995
        eta_m_default= 0.995
        eta_ab_default= 0.97
        pi_d_max_default= 0.97
        pi_f_default= 1
        if self.single_multi_selected_button=="single":
            pi_c_default= 16
        else:
            pi_c_default= 16   #bcz what if it is not selected as independent variable
            min_pi_c_default= 15
            steps_pi_c_default= 5
            max_pi_c_default= 25
        pi_cL_default= 3.8
        pi_cH_default= 4.2105
        pi_b_default= 0.96
        pi_m_max_default= "NA"
        pi_ab_default= 0.96
        pi_n_default= 0.98
        pi_fn_default= 1
        peta_f_default= 1
        peta_c_default= 0.89
        peta_t_default= 0.89
        P0_P9_default= 1
        P0_P19_default= 1
        sep_mixed_flow_default= "S"
        nozzleType_default= "CD"

        self.var_bool= True
        self.reset_parameters_widgets_frame()
        self.var_bool= False



    def set_parameters(self):
        #Basic parameters
        global engineType,AB,alt,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType
        global min_Tt4,steps_Tt4,max_Tt4
        global min_pi_c,steps_pi_c,max_pi_c
        global min_alt,steps_alt,max_alt
        global min_M0,steps_M0,max_M0

        #contigency protocol incase for no inputs
        engineType,AB,alt,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType = ['-']*40
        min_Tt4,steps_Tt4,max_Tt4= ['-']*3
        min_pi_c,steps_pi_c,max_pi_c= ['-']*3
        min_alt,steps_alt,max_alt= ['-']*3
        min_M0,steps_M0,max_M0= ['-']*3

        engineType= "turbojet"

        try:
            if self.single_multi_selected_button=="single":
                alt=float(self.alt_entry.get())
                T0= float(self.temperature_entry.get())
                P0=float(self.pressure_entry.get())*1e+3
            elif self.single_multi_selected_button=="multi":
                if (self.onetwo_indp_var.get()=="one" and "alt" in [self.indep_var_entry_combobox.get()]) or  self.onetwo_indp_var.get()=="two" and "alt" in [self.indep_var1_entry_combobox.get(),self.indep_var2_entry_combobox.get()]:      
                    min_alt= float(self.min_alt_entry.get())
                    steps_alt= float(self.steps_alt_entry.get())
                    max_alt= float(self.max_alt_entry.get())
                    alt= '-' #Instead of None '-' is used bcz suppose user firstly goes to multi point two independent variable and selects alt as independent variable and then goes to single point calculation then alt will be None but it should be '-' bcz it is not selected as independent variable
                    T0= '-'
                    P0= '-'
                else:
                    alt= float(self.alt_entry.get())    #bcz what if alt is not selected as independent variable
                    T0= float(self.temperature_entry.get())
                    P0=float(self.pressure_entry.get())*1e+3



            if self.single_multi_selected_button=="single":
                M0=float(self.M0_entry.get())
            elif self.single_multi_selected_button=="multi":
                if (self.onetwo_indp_var.get()=="one" and "M0" in [self.indep_var_entry_combobox.get()]) or  self.onetwo_indp_var.get()=="two" and "M0" in [self.indep_var1_entry_combobox.get(),self.indep_var2_entry_combobox.get()]:      
                    min_M0= float(self.min_M0_entry.get())
                    steps_M0= float(self.steps_M0_entry.get())
                    max_M0= float(self.max_M0_entry.get())
                    M0= '-'
                else:
                    M0= float(self.M0_entry.get())    #bcz what if Tt4 is not selected as independent variable




            if self.single_multi_selected_button=="single":
                Tt4=float(self.Tt4_entry.get())
            elif self.single_multi_selected_button=="multi":
                if (self.onetwo_indp_var.get()=="one" and "Tt4" in [self.indep_var_entry_combobox.get()]) or  self.onetwo_indp_var.get()=="two" and "Tt4" in [self.indep_var1_entry_combobox.get(),self.indep_var2_entry_combobox.get()]:      
                    min_Tt4= float(self.min_Tt4_entry.get())
                    steps_Tt4= float(self.steps_Tt4_entry.get())
                    max_Tt4= float(self.max_Tt4_entry.get())
                    Tt4= '-'
                else:
                    Tt4= float(self.Tt4_entry.get())    #bcz what if Tt4 is not selected as independent variable

            Hpr=float(self.Hpr_entry.get())*1e+3

            if self.single_multi_selected_button=="single":
                pi_c=float(self.pi_c_entry.get())
            elif self.single_multi_selected_button=="multi":
                if (self.onetwo_indp_var.get()=="one" and "pi_c" in [self.indep_var_entry_combobox.get()]) or  self.onetwo_indp_var.get()=="two" and "pi_c" in [self.indep_var1_entry_combobox.get(),self.indep_var2_entry_combobox.get()]:
                    min_pi_c= float(self.min_pi_c_entry.get())
                    steps_pi_c= float(self.steps_pi_c_entry.get())
                    max_pi_c= float(self.max_pi_c_entry.get())
                    pi_c='-'
                else:
                    pi_c= float(self.pi_c_entry.get())
            
            if self.single_multi_selected_button=="single":
                if self.var_single_dual.get()=="single":
                    pi_cL= pi_c
                    pi_cH= 1
                else:
                    pi_cL=float(self.pi_cL_entry.get())
                    pi_cH=pi_c/pi_cL
            elif self.single_multi_selected_button=="multi":
                if (self.onetwo_indp_var.get()=="one" and "pi_c" in [self.indep_var_entry_combobox.get()]) or  (self.onetwo_indp_var.get()=="two" and "pi_c" in [self.indep_var1_entry_combobox.get(),self.indep_var2_entry_combobox.get()]):
                    if self.var_single_dual.get()=="single":
                        pi_cL= None
                        pi_cH= 1
                    else:
                        pi_cL= float(self.pi_cL_entry.get())
                        pi_cH= None
                else:
                    if self.var_single_dual.get()=="single":
                        pi_cL= pi_c
                        pi_cH= 1
                    else:
                        pi_cL=float(self.pi_cL_entry.get())
                        pi_cH=pi_c/pi_cL


            alp=0
            pi_f=1
            peta_f= 1
            pi_fn= 1
            M6= "NA"
            pi_m_max= "NA"
            sep_mixed_flow= "S"


            gam_c=float(self.gam_c_entry.get())
            Cpc= float(self.Cpc_entry.get())
            Rc = (gam_c-1)*Cpc/gam_c
            if self.var_ideal_real.get()=="real":
                gam_t=float(self.gam_t_entry.get())
                Cpt= float(self.Cpt_entry.get())
                Rt = (gam_t-1)*Cpt/gam_t
                if self.var_AB.get()=="Y":
                    gam_ab=float(self.gam_ab_entry.get())  
                    Cpab= float(self.Cpab_entry.get())
                    Rab = (gam_ab-1)*Cpab/gam_ab
                else:
                    gam_ab= gam_t
                    Cpab= Cpt
                    Rab= Rt
            else:
                #ideal cycle analysis
                Cpt= Cpc
                Cpab= Cpt
                gam_t= gam_c
                gam_ab= gam_t
                Rt= Rc
                Rab= Rt


            if self.var_ideal_real.get()=="real":
                eta_b=float(self.eta_b_entry.get())
                eta_m=float(self.eta_m_entry.get())
                peta_c=float(self.peta_c_entry.get())
                peta_t=float(self.peta_t_entry.get())
                if self.var_AB.get()=="Y":
                    eta_ab= float(self.eta_ab_entry.get())
                else:
                    eta_ab= 1
            else:
                #ideal cycle analysis
                eta_b=1
                eta_m=1
                eta_ab=1
                peta_c=1
                peta_t=1

            if self.var_ideal_real.get()=="real":
                pi_d_max=float(self.pi_d_max_entry.get())     
                pi_b=float(self.pi_b_entry.get())
                pi_n=float(self.pi_n_entry.get())
                if self.var_AB.get()=="Y":
                    pi_ab=float(self.pi_ab_entry.get())
                else:
                    pi_ab= 1
            else:
                pi_d_max=1
                pi_b=1
                pi_n=1
                pi_ab=1
        
            #afterburner property
            if self.var_AB.get()=="Y":
                AB= "Y"
                Tt7= float(self.Tt7_entry.get())
            else:
                AB= "N"
                Tt7= "NA"
                eta_ab= 1
                pi_ab= 1
                gam_ab= gam_t


            #nozzle property
            if self.var_ConDiv_Con.get()=="C":
                nozzleType= "C"
                P0_P9=  "NA"                        #its value will be calculated
                P0_P19= "NA"
            else:
                nozzleType="CD"
                P0_P9= float(self.P0_P9_entry.get())
                P0_P19= 1




            if self.single_multi_selected_button=="single":
                #we display the engine parameters scroll bar
                d= dict(globals().items()) 
                arr= ["engineType","AB","T0","P0","M0","M6","alp","gam_c","gam_t","gam_ab","Rc","Rt","Rab","Cpc","Cpt","Cpab","Tt4","Tt7","Hpr","eta_b","eta_m","eta_ab","pi_d_max","pi_f","pi_c","pi_cL","pi_cH","pi_b","pi_m_max","pi_ab","pi_n","pi_fn","peta_f","peta_c","peta_t","P0_P9","P0_P19","sep_mixed_flow","nozzleType"]
                            
                #first we empty the set_parameters_tree_view
                for item in self.set_parameters_tree_view.get_children():
                    self.set_parameters_tree_view.delete(item)
                for i in arr:
                    val= round(d[i],4) if type(d[i])==float else d[i]
                    self.set_parameters_tree_view.insert("",tk.END,values=(syb(i),val))


            elif self.single_multi_selected_button=="multi":
                globals_dict= dict(globals().items()) 
                arr= ["engineType","AB","T0","P0","M0","M6","alp","gam_c","gam_t","gam_ab","Rc","Rt","Rab","Cpc","Cpt","Cpab","Tt4","Tt7","Hpr","eta_b","eta_m","eta_ab","pi_d_max","pi_f","pi_c","pi_cL","pi_cH","pi_b","pi_m_max","pi_ab","pi_n","pi_fn","peta_f","peta_c","peta_t","P0_P9","P0_P19","sep_mixed_flow","nozzleType"]
                self.parameters_dict= dict()
                for i in arr:
                    self.parameters_dict[i]= globals_dict[i]
                
                if self.onetwo_indp_var.get()=="one":
                    min_indep_var= globals()["min_"+self.indep_var_entry_combobox.get()]
                    steps_indep_var= globals()["steps_"+self.indep_var_entry_combobox.get()]
                    max_indep_var= globals()["max_"+self.indep_var_entry_combobox.get()]
                    self.indep_var_iterlst= [self.indep_var_entry_combobox.get(),min_indep_var,steps_indep_var,max_indep_var]
                elif self.onetwo_indp_var.get()=="two":
                    min_indep_var1= globals()["min_"+self.indep_var1_entry_combobox.get()]
                    steps_indep_var1= globals()["steps_"+self.indep_var1_entry_combobox.get()]
                    max_indep_var1= globals()["max_"+self.indep_var1_entry_combobox.get()]
                    self.indep_var1_iterlst= [self.indep_var1_entry_combobox.get(),min_indep_var1,steps_indep_var1,max_indep_var1]

                    min_indep_var2= globals()["min_"+self.indep_var2_entry_combobox.get()]
                    steps_indep_var2= globals()["steps_"+self.indep_var2_entry_combobox.get()]
                    max_indep_var2= globals()["max_"+self.indep_var2_entry_combobox.get()]
                    self.indep_var2_iterlst= [self.indep_var2_entry_combobox.get(),min_indep_var2,steps_indep_var2,max_indep_var2]
                
                return 
            
        except ValueError:
            messagebox.showerror("Error","Please enter valid parameter values")
            return "error"



    def plot_button_command(self):
        
        #no error could come here since error will be handled in the get_PCA_results_multi_point_calculation function only
        if self.onetwo_indp_var.get()=="one":
            self.plot_object.show_plots(self.engine_lst_dict,None,self.Y_variable_combobox.get(),self.indep_var_iterlst)
        elif self.onetwo_indp_var.get()=="two":
            self.plot_object.show_plots(self.engine_lst_dict,self.X_variable_combobox.get(),self.Y_variable_combobox.get(),self.indep_var1_iterlst,self.indep_var2_iterlst)

    def set_iteration_variables_frame(self):

        for item in self.iteration_variables_frame.winfo_children():
            if item != self.indp_vars_checkbutton:
                item.destroy()
            else:
                continue

        if self.onetwo_indp_var.get()=="one":
            indep_var_label= ttk.Label(self.iteration_variables_frame,text="Iteration Variable")
            indep_var_label.grid(row=1,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.indep_var_entry_combobox= ttk.Combobox(self.iteration_variables_frame,values=["Tt4","pi_c","alt","M0"],state="readonly")
            indep_var_entry_combobox= self.indep_var_entry_combobox
            #call reset_parameters_widgets function whenever the indep_var_entry_combobox value is changed
            indep_var_entry_combobox.bind("<<ComboboxSelected>>",self.reset_parameters_widgets_frame)
            indep_var_entry_combobox.grid(row=2,column=0,padx= 5,pady=(0,5),sticky="ew")
            if self.inpt_outpt_selected_button=="output" and hasattr(self,"parameters_dict") and hasattr(self,"indep_var_iterlst"):
                if self.indep_var_iterlst[0]=="Tt4":         # indep_var_entry_combobox.get() wont return the value of the earlier defined combobox
                    indep_var_entry_combobox.set("Tt4")
                elif self.indep_var_iterlst[0]=="pi_c":
                    indep_var_entry_combobox.set("pi_c")
                elif self.indep_var_iterlst[0]=="alt":
                    indep_var_entry_combobox.set("alt")
                elif self.indep_var_iterlst[0]=="M0":
                    indep_var_entry_combobox.set("M0")
            else:
                indep_var_entry_combobox.current(0)




        elif self.onetwo_indp_var.get()=="two":
            indep_var1_label= ttk.Label(self.iteration_variables_frame,text="Iteration Variable 1")
            indep_var1_label.grid(row=1,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.indep_var1_entry_combobox= ttk.Combobox(self.iteration_variables_frame,values=["Tt4","pi_c","alt","M0"],state="readonly")
            indep_var1_entry_combobox= self.indep_var1_entry_combobox
            #call reset_parameters_widgets function whenever the indep_var_entry_combobox value is changed
            indep_var1_entry_combobox.bind("<<ComboboxSelected>>",self.reset_parameters_widgets_frame)
            indep_var1_entry_combobox.grid(row=2,column=0,padx= 5,pady=(0,5),sticky="ew")
            if self.inpt_outpt_selected_button=="output" and hasattr(self,"parameters_dict") and hasattr(self,"indep_var1_iterlst"):  #suppose user successful run on multi point with single variable has parameters_dict is there. Now he selects two variables and does some error in set parameters, now code doesnt have indep_var1_iterlst
                if self.indep_var1_iterlst[0]=="Tt4":         # indep_var_entry_combobox.get() wont return the value of the earlier defined combobox
                    indep_var1_entry_combobox.set("Tt4")
                elif self.indep_var1_iterlst[0]=="pi_c":
                    indep_var1_entry_combobox.set("pi_c")
                elif self.indep_var1_iterlst[0]=="alt":
                    indep_var1_entry_combobox.set("alt")
                elif self.indep_var1_iterlst[0]=="M0":
                    indep_var1_entry_combobox.set("M0")
            else:
                indep_var1_entry_combobox.current(0)

            indep_var2_label= ttk.Label(self.iteration_variables_frame,text="Iteration Variable 2")
            indep_var2_label.grid(row=3,column=0,padx= 5,pady=(0,5),sticky="ew")
            self.indep_var2_entry_combobox= ttk.Combobox(self.iteration_variables_frame,values=["Tt4","pi_c","alt","M0"],state="readonly")
            indep_var2_entry_combobox= self.indep_var2_entry_combobox
            #call reset_parameters_widgets function whenever the indep_var_entry_combobox value is changed
            indep_var2_entry_combobox.bind("<<ComboboxSelected>>",self.reset_parameters_widgets_frame)
            indep_var2_entry_combobox.grid(row=4,column=0,padx= 5,pady=(0,5),sticky="ew")
            if self.inpt_outpt_selected_button=="output" and hasattr(self,"parameters_dict") and hasattr(self,"indep_var2_iterlst"):
                if self.indep_var2_iterlst[0]=="Tt4":   
                    indep_var2_entry_combobox.set("Tt4")
                elif self.indep_var2_iterlst[0]=="pi_c":
                    indep_var2_entry_combobox.set("pi_c")
                elif self.indep_var2_iterlst[0]=="alt":
                    indep_var2_entry_combobox.set("alt")
                elif self.indep_var2_iterlst[0]=="M0":
                    indep_var2_entry_combobox.set("M0")
            else:
                indep_var2_entry_combobox.current(1)                

        #set_default_values button widget below the iteration variables
        set_default_values_button= ttk.Button(self.iteration_variables_frame,text="Set Default Values",command= self.set_default_values)   
        row_num= 3 if self.onetwo_indp_var.get()=="one" else 5       
        set_default_values_button.grid(row=row_num,column=0,padx=5,pady=(0,5) ,sticky=tk.E)

        self.reset_parameters_widgets_frame()


    def single_point_calculation_button_command(self):
        #just so that single point button is lighted up even after being clicked
        self.var_single_point_calculation_button.set(True)   
        self.var_multi_point_calculation_button.set(False)         

        if self.inpt_outpt_selected_button=="input" and self.single_multi_selected_button=="single" and hasattr(self,"single_point_calculation_frame"):
            pass
            return      #do nothing if single_point_calculation_frame is already present
        elif self.inpt_outpt_selected_button=="input" and self.single_multi_selected_button=="multi" and hasattr(self,"multi_point_calculation_frame"):
            for item in self.multi_point_calculation_frame.winfo_children():
                item.destroy()

    #single_point_calculation_frame to show the single point calculation widgets
        self.single_point_calculation_frame= ttk.Frame(self.inputs_frame)
        single_point_calculation_frame= self.single_point_calculation_frame
        single_point_calculation_frame.grid(row=2,column=0,columnspan=2,sticky=tk.W+tk.E)

    #parameters widget frame
        self.parameters_widgets_frame= ttk.LabelFrame(single_point_calculation_frame,text="Parameters/Properties")
        parameters_widgets_frame= self.parameters_widgets_frame
        parameters_widgets_frame.grid(row=0,column=0,padx=(0,20),pady=(5,0),sticky=tk.W+tk.E)

        self.single_multi_selected_button="single"

        self.reset_parameters_widgets_frame()

    #set_parameters_frame on the left side of the parameters_widgets_frame
        self.set_parameters_frame= ttk.LabelFrame(single_point_calculation_frame,text= "Set Parameters")
        set_parameters_frame= self.set_parameters_frame
        set_parameters_frame.grid(row=0,column=1,pady=(5,0),sticky='nsew')


        #set_parameters button inside the set_parameters_frame
        set_parameters_button= ttk.Button(set_parameters_frame,text="Set Parameters",command= self.set_parameters)
        set_parameters_button.grid(column=0,row=0,padx=5,sticky='ew')    

        #we have a set_parameter_tree_view scroll box just below the set_parameters_button
        treeframe= ttk.Frame(set_parameters_frame)
        treeframe.grid(row=1,column=0,padx= 10, pady= 10,sticky='ew')
        #scrollbar widget
        scrollbar= ttk.Scrollbar(treeframe,orient="vertical")
        scrollbar.pack(side="right",fill="y")            #filling the scrollbar in the y direction
        cols= ["Parameter","Value"]
        #tree view widget
        self.set_parameters_tree_view= ttk.Treeview(treeframe,columns=cols,show="headings",height=20, yscrollcommand=scrollbar.set)
        set_parameters_tree_view= self.set_parameters_tree_view
        set_parameters_tree_view.pack()
        for col_name in cols:                                         #initialising the coloumns in the tree_view
            set_parameters_tree_view.column(col_name,width= 100,anchor="center")
        scrollbar.config(command=set_parameters_tree_view.yview)         #configuring the scrollbar to the tree_view
        set_parameters_tree_view.heading('Parameter',text='Parameter')
        set_parameters_tree_view.heading('Value',text='Value')

        #set_default_values button widget below the set_parameters_tree_view
        set_default_values_button= ttk.Button(set_parameters_frame,text="Set Default Values",command= self.set_default_values)           
        set_default_values_button.grid(row=2,column=0,padx=5,pady=(0,5) ,sticky=tk.E)


    def multi_point_calculation_button_command(self):
        #just so that multi point button is lighted up even after being clicked
        self.var_multi_point_calculation_button.set(True)   
        self.var_single_point_calculation_button.set(False)
        

        if self.inpt_outpt_selected_button=="input" and self.single_multi_selected_button=="multi" and hasattr(self,"multi_point_calculation_frame"):
            pass
            return
        elif self.inpt_outpt_selected_button=="input" and self.single_multi_selected_button=="single" and hasattr(self,"single_point_calculation_frame"): 
            for item in self.single_point_calculation_frame.winfo_children():
                item.destroy() 

    #multi_point_calculation_frame to show the multi point calculation widgets
        self.multi_point_calculation_frame= ttk.Frame(self.inputs_frame)
        multi_point_calculation_frame= self.multi_point_calculation_frame
        multi_point_calculation_frame.grid(row=2,column=0,columnspan=2,sticky=tk.W+tk.E)

    #parameters widget frame
        self.parameters_widgets_frame= ttk.LabelFrame(multi_point_calculation_frame,text="Parameters/Properties")
        parameters_widgets_frame= self.parameters_widgets_frame
        parameters_widgets_frame.grid(row=0,column=0,padx=(0,20),pady=(5,0),sticky=tk.W+tk.E)

    #column1_frame to contain the iteration_variables_frame
        column1_frame= ttk.Frame(multi_point_calculation_frame)
        column1_frame.grid(row=0,column=1,padx=(0,20),pady=(5,0),sticky='nsew')

    #itertaion_variables_frame on the right side of the parameters_widgets_frame
        self.iteration_variables_frame= ttk.LabelFrame(column1_frame,text="Iteration Variables")
        iteration_variables_frame= self.iteration_variables_frame
        iteration_variables_frame.grid(row=0,column=0,padx=(20,0),pady=(5,0),sticky='nsew')

        #onetwo_indp_var button asking about number of independent variables
        if self.inpt_outpt_selected_button=="input" and self.single_multi_selected_button=="single":
            self.onetwo_indp_var= tk.StringVar(value="one")
        self.indp_vars_checkbutton= ttk.Checkbutton(iteration_variables_frame,text="Two",style="Switch",variable=self.onetwo_indp_var, offvalue="one",onvalue= "two",command= self.set_iteration_variables_frame)
        indp_vars_checkbutton= self.indp_vars_checkbutton
        indp_vars_checkbutton.grid(column=0,row=0,padx= 5, pady= 5,sticky='ew')

        self.single_multi_selected_button="multi"

        self.set_iteration_variables_frame()  #reset_parameters_widgets_frame is called inside this function since we want it to reset everytime user changes the number of independent variables


    def inputs_button_command(self):
        """This function is used to create the input window for the turbojet engine."""

        #Just to light up the inputs button and unlight the outputs button
        self.var_outputs_button.set(False)
        self.var_inputs_button.set(True)

        if self.inpt_outpt_selected_button== "input" and hasattr(self,"inputs_frame"):   #self.inpt_outpt_selected_button indicates the button that was selected last time
            pass
            return                                      #do nothing when the user repeatedly clicks the inputs button
        elif self.inpt_outpt_selected_button== "output":      
            for item in self.outputs_frame.winfo_children():
                item.destroy()                          #we change the value of self.selected_button later in this function
                                                        
        if hasattr(self,"inputs_frame"):
            for item in self.inputs_frame.winfo_children():
                item.destroy()

    #inputs_frame
        self.inputs_frame= ttk.Frame(self.root_frame)
        inputs_frame= self.inputs_frame
        inputs_frame.grid(row=1,column=0)

    #main_widgets_frame widget to contain the ideal/reality, single/dual, afterburner and CD/C switch buttons
        main_widgets_frame= ttk.LabelFrame(inputs_frame)
        main_widgets_frame.grid(row=0,column=0,columnspan=2,sticky= tk.W+tk.E)

        pad_x_val= 40
        #ideal_real_switchbutton widget
        if self.inpt_outpt_selected_button=="input":                       #bcz if we are coming back from the output window then we don't want to reset the values of the ideal_real_switch button
            self.var_ideal_real= tk.StringVar(value= "ideal")   #we dont need to reintialise the variable if we are coming back from the output window bcz they were made in the input window before and have not been destroyed as such
        self.ideal_real_switch= ttk.Checkbutton(main_widgets_frame,variable=self.var_ideal_real,style="Switch",offvalue="ideal",onvalue="real",text="Real Cycle",command= self.reset_parameters_widgets_frame) #,,text="Ideal/Real"
        ideal_real_switch= self.ideal_real_switch
        ideal_real_switch.grid(row=0,column=0,padx= pad_x_val, pady= 5,sticky="ew")

        #Single_dual_switchbutton widget
        if self.inpt_outpt_selected_button =="input":                  
            self.var_single_dual= tk.StringVar(value= "single")
        self.single_dual_switch= ttk.Checkbutton(main_widgets_frame,variable=self.var_single_dual,style="Switch",offvalue="single",onvalue="dual",text="Dual-Spool",command= self.reset_parameters_widgets_frame) #style="Switch",text="Single/Dual"
        single_dual_switch= self.single_dual_switch
        single_dual_switch.grid(row=0,column=2,padx= pad_x_val, pady= 5,sticky="ew")

        #afterburner_checkbutton widget
        if self.inpt_outpt_selected_button =="input":
            self.var_AB= tk.StringVar(value= "N")      
        afterburner_checkbutton= ttk.Checkbutton(main_widgets_frame,text="Afterburner",style="Switch",variable=self.var_AB,offvalue="N",onvalue="Y",command= self.reset_parameters_widgets_frame)
        afterburner_checkbutton.grid(row=0,column=3,padx= pad_x_val, pady= 5,sticky="ew")

        #CD_C_switchbutton widget   #convergingDiverging/Converging
        if self.inpt_outpt_selected_button =="input":
            self.var_ConDiv_Con= tk.StringVar(value="CD")  #setting default value
        self.CD_C_switch= ttk.Checkbutton(main_widgets_frame,variable=self.var_ConDiv_Con,style="Switch",offvalue="CD",onvalue="C",text="Convergent nozzle",command= self.CD_C_switch_command) #style="Switch",text="CD/C"
        CD_C_switch= self.CD_C_switch
        CD_C_switch.grid(row=0,column=4,padx= pad_x_val, pady= 5,sticky="ew")

    #single_multi_point_calculation_frame widget below the main_widgets_frame
        single_multi_point_calculation_frame= ttk.Frame(inputs_frame)
        single_multi_point_calculation_frame.grid(row=1,column=0,columnspan=2,sticky=tk.W+tk.E)

        #single_point_calculation_button widget
        if self.inpt_outpt_selected_button=="input":
            self.var_single_point_calculation_button= tk.BooleanVar(value=True)
        self.single_point_calculation_button= ttk.Checkbutton(single_multi_point_calculation_frame,text="Single Point Calculation",style="Toolbutton",variable=self.var_single_point_calculation_button,command= self.single_point_calculation_button_command,width= 30)    #, image=input_icon_img,compound='left'
        single_point_calculation_button= self.single_point_calculation_button 
        single_point_calculation_button.grid(row=0,column=0,padx=(175,0),pady=(5,0)) #,sticky=tk.W

        #multi_point_calculation_button widget
        if self.inpt_outpt_selected_button=="input":
            self.var_multi_point_calculation_button= tk.BooleanVar(value=False)
        self.multi_point_calculation_button= ttk.Checkbutton(single_multi_point_calculation_frame,text="Multi Point Calculation",style="Toolbutton",variable=self.var_multi_point_calculation_button,command= self.multi_point_calculation_button_command,width= 30)    #, image=input_icon_img,compound='left'
        multi_point_calculation_button= self.multi_point_calculation_button 
        multi_point_calculation_button.grid(row=0,column=1,padx=(5,0),pady=(5,0)) #,sticky=tk.W

        #invoke the single_point_calculation_button
        if self.single_multi_selected_button=="single":
            self.single_point_calculation_button.invoke()
        elif self.single_multi_selected_button=="multi":
            self.multi_point_calculation_button.invoke()


        self.inpt_outpt_selected_button = "input"



    def set_PCA_results_single_point_calculation(self):
        try:
            error_or_not= self.set_parameters() #since it has it's own try except block, it would never give an error
            if error_or_not=="error":
                return                          #if error is encountered in the set_parameters function then we return from here
            # os.system('hey')

            #calculating the PCA results
            engine= initialisingComponents(engineType,AB,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType).get_engine()
            self.engine= engine
            [f,ST,TSFC]= engine.get_engineDetails()
            lst,lst0= engine.print_get_details()
            
            # os.system("hey1")
            #clearing the pca_results_tree_view
            for item in self.PCA_results_tree_view.get_children():
                self.PCA_results_tree_view.delete(item)
            #displaying the PCA results
            for i in lst:
                val= i[1]
                if type(i[1]) != str:
                    val= round(val,4)
                self.PCA_results_tree_view.insert("",tk.END,values=(syb(i[0]),val))

            #clearing the station_properties_tree_view
            for item in self.station_properties_tree_view.get_children():
                self.station_properties_tree_view.delete(item)
            #displaying the Station properties scroll bar
            for i in lst0:
                self.station_properties_tree_view.insert("",tk.END,values=(i[0],round(i[1],4),round(i[2],4)))

        except : 
            messagebox.showerror("Error","Math Domain error encountered during PCA calculation")


    def set_PCA_results_multi_point_calculation(self):

        error_or_not= self.set_parameters()
        if error_or_not=="error":
            return                          #if error is encountered in the set_parameters function then we return from here
        
        #here we dont keep a error message bcz that is kept in the plots file itself and we dont want to show the error message twice
        if self.onetwo_indp_var.get()=="one":
            self.plot_object= plots()
            self.engine_lst_dict= self.plot_object.get_tabulated_engines(self.parameters_dict,self.indep_var_iterlst)
            if self.engine_lst_dict==None:     #when error was encountered in the get_tabulated_engines function. we dont want to go ahead in the function
                return

            engine_lst_dict= self.engine_lst_dict
            #clearing the tabulkar_results_tree_view
            for item in self.tabular_results_tree_view.get_children():
                self.tabular_results_tree_view.delete(item)
            #displaying the engine results
            for i in range(len(engine_lst_dict)):
                self.tabular_results_tree_view.insert("",tk.END,values=(engine_lst_dict[i][0],engine_lst_dict[i][1],round(engine_lst_dict[i][3],4),round(engine_lst_dict[i][4],4),round(engine_lst_dict[i][5],4)))
        
        elif self.onetwo_indp_var.get()=="two":
            self.plot_object= plots()
            self.engine_lst_dict= self.plot_object.get_tabulated_engines(self.parameters_dict,self.indep_var1_iterlst,self.indep_var2_iterlst)
            if self.engine_lst_dict==None:     #when error was encountered in the get_tabulated_engines function. we dont want to go ahead in the function
                return
            engine_lst_dict= self.engine_lst_dict
            #clearing the tabulkar_results_tree_view
            for item in self.tabular_results_tree_view.get_children():
                self.tabular_results_tree_view.delete(item)
            #displaying the engine results
            for i in range(len(engine_lst_dict)):
                self.tabular_results_tree_view.insert("",tk.END,values=(engine_lst_dict[i][0],engine_lst_dict[i][1],engine_lst_dict[i][2],round(engine_lst_dict[i][3],4),round(engine_lst_dict[i][4],4),round(engine_lst_dict[i][5],4)))

    def set_outputs_frame_single_point_calculation(self):
        """This function is used to create the output window for the turbojet engine when single point calculation is selected."""

        outputs_frame= self.outputs_frame

    #column0_frame inside the outputs_frame
        column0_frame= ttk.Frame(outputs_frame)
        column0_frame.grid(row=0,column=0,padx= 20,sticky=tk.E)

    #column1_frame inside the outputs_frame 
        column1_frame= ttk.Frame(outputs_frame)
        column1_frame.grid(row=0,column=1,padx= (0,20),sticky=tk.W)

    #PCA_results widgets frame inside the outputs_frame
        PCA_results_frame= ttk.LabelFrame(column0_frame,text="PCA Results")
        PCA_results_frame.grid(column=0,row=0,padx=(20,0),sticky='ew')

        #PCA_results_tree_view scroll box just below the PCA_results_button
        treeframe= ttk.Frame(PCA_results_frame)
        treeframe.grid(row=0,column=0,padx= 5, pady= 10,sticky='ew')
        #scrollbar widget
        scrollbar= ttk.Scrollbar(treeframe,orient="vertical")
        scrollbar.pack(side="right",fill="y")            #filling the scrollbar in the y direction
        cols= ["Variable","Value"]
        #tree view widget
        self.PCA_results_tree_view= ttk.Treeview(treeframe,columns=cols,show="headings",height=27, yscrollcommand=scrollbar.set)
        PCA_results_tree_view= self.PCA_results_tree_view
        PCA_results_tree_view.pack()
        for col_name in cols:                                         #initialising the coloumns in the tree_view
            PCA_results_tree_view.column(col_name,width= 100,anchor="center")
        scrollbar.config(command=PCA_results_tree_view.yview)         #configuring the scrollbar to the tree_view
        PCA_results_tree_view.heading('Variable',text='Variable')
        PCA_results_tree_view.heading('Value',text='Value')

    #nomenclature_img label frame 
        nomenclature_img_frame= ttk.LabelFrame(column1_frame,text="Nomenclature")
        nomenclature_img_frame.grid(column=0,row=0,padx= 5,sticky='ew')
        #nomenclature_img widget inside the nomenclature_img_frame
        # img= Image.open("\\".join(os.path.abspath(__file__).split("\\")[0:-1]) +"\\images\\turbojet_nomenclature_img.png")
        img= Image.open(resource_path("MAIN_GUI\\images\\turbojet_nomenclature_img.png"))
        img= img.resize((300,150),Image.ANTIALIAS)
        self.nomenclature_img= ImageTk.PhotoImage(img)
        nomenclature_img= self.nomenclature_img
        nomenclature_img_label= ttk.Label(nomenclature_img_frame,image=nomenclature_img,anchor="center")
        nomenclature_img_label.grid(row=0,column=0,padx= (30,0), pady= 10,sticky='ew')

    #station_properties widgets frame inside the outputs_frame
        station_properties_frame= ttk.LabelFrame(column1_frame,text="Station Properties")
        station_properties_frame.grid(column=0,row=1,padx= 5,pady= (10,0),sticky='ew')    
    
        #station_properties_tree_view scroll bar inside the station_properties_frame
        treeframe2= ttk.Frame(station_properties_frame)
        treeframe2.grid(row=0,column=0,padx= 5, pady= 10,sticky='ew')
        #scrollbar widget
        scrollbar2= ttk.Scrollbar(treeframe2,orient="vertical")
        scrollbar2.pack(side="right",fill="y")            #filling the scrollbar in the y direction
        cols= ["Station","Pressure (kPa)","Temperature (k)"]
        #tree view widget
        self.station_properties_tree_view= ttk.Treeview(treeframe2,columns=cols,show="headings",height=10, yscrollcommand=scrollbar2.set)
        station_properties_tree_view= self.station_properties_tree_view
        station_properties_tree_view.pack()
        for col_name in cols:                                         #initialising the coloumns in the tree_view
            station_properties_tree_view.column(col_name,width= 100,anchor="center")
        scrollbar2.config(command=station_properties_tree_view.yview)         #configuring the scrollbar to the tree_view
        station_properties_tree_view.heading('Station',text='Station')
        station_properties_tree_view.heading('Pressure (kPa)',text='Pressure (kPa)')
        station_properties_tree_view.heading('Temperature (k)',text='Temperature (K)')

    #EPA testing frame just below the station_properties_frame
        EPA_testing_frame= ttk.LabelFrame(column1_frame,text="EPA Testing")
        EPA_testing_frame.grid(column=0, row=2,padx= 5,pady= 10,sticky=tk.E+tk.W)

        #epa_test_button widget
        epa_test_button= ttk.Button(EPA_testing_frame,text="Test this engine",command= self.epa_test_button_command)  #lambda: messagebox.showinfo("Error","This feature is not available yet. Please wait for the next update.")
        epa_test_button.grid(row=0,column=0,columnspan=2,padx=120,pady=5,sticky=tk.W+tk.E)  

        self.set_PCA_results_single_point_calculation()


    def set_outputs_frame_multi_point_calculation(self):
        """This function is used to create the output window for the turbojet engine when multi point calculation is selected."""

        outputs_frame= self.outputs_frame
    #column0_frame inside the outputs_frame
        column0_frame= ttk.Frame(outputs_frame)
        column0_frame.grid(row=0,column=0,padx=5,sticky=tk.E)

    #column1_frame inside the outputs_frame
        column1_frame= ttk.Frame(outputs_frame)
        column1_frame.grid(row=0,column=1,padx=5,sticky=tk.W)

    #tabular_results_frame inside the outputs_frame
        tabular_results_frame= ttk.LabelFrame(column0_frame,text="Tabular Results")
        tabular_results_frame.grid(column=0,row=0,sticky=tk.N+tk.E)

        #station_properties_tree_view scroll bar inside the station_properties_frame
        tabular_results_treeframe= ttk.Frame(tabular_results_frame)
        tabular_results_treeframe.grid(row=0,column=0,padx= 5, pady= 10,sticky='ew')
        #scrollbar widget
        tabular_results_scrollbar= ttk.Scrollbar(tabular_results_treeframe,orient="vertical")
        tabular_results_scrollbar.pack(side="right",fill="y")            #filling the scrollbar in the y direction
        if self.onetwo_indp_var.get()=="one":
            cols= ["S.No.",self.indep_var_entry_combobox.get()," f "," ST "," TSFC "] #,"eta_t","eta_t","M9"
        elif self.onetwo_indp_var.get()=="two":
            cols= ["S.No.",self.indep_var1_entry_combobox.get(),self.indep_var2_entry_combobox.get(),"f "," ST "," TSFC "]  #,"eta_t","eta_t","M9"
        #tree view widget
        self.tabular_results_tree_view= ttk.Treeview(tabular_results_treeframe,columns=cols,show="headings",height=15, yscrollcommand=tabular_results_scrollbar.set)
        tabular_results_tree_view= self.tabular_results_tree_view
        tabular_results_tree_view.pack()
        for col_name in cols:                                         #initialising the coloumns in the tree_view
            tabular_results_tree_view.column(col_name,width= 70,anchor="center")
        tabular_results_scrollbar.config(command=tabular_results_tree_view.yview)         #configuring the scrollbar to the tree_view
        for i in cols:
            tabular_results_tree_view.heading(i,text=i)

    #plots_frame inside the outputs_frame below the tabular results frame
        plotting_widgets_frame= ttk.LabelFrame(column0_frame,text="Plots")
        plotting_widgets_frame.grid(column=0,row=1,pady= 10,sticky='ew')

        #X_variable inside the plotting_widgets_frame
        if self.onetwo_indp_var.get()=="one":
            x_values_list= [self.indep_var_entry_combobox.get()]        #bcz for one indep var is same as the x axis
        elif self.onetwo_indp_var.get()=="two":
            x_values_list= ["f","ST","TSFC"]
        X_variable_label= ttk.Label(plotting_widgets_frame,text="X axis")
        X_variable_label.grid(row=0,column=0,padx= 5,pady=(0,5),sticky="ew")
        self.X_variable_combobox= ttk.Combobox(plotting_widgets_frame,values=x_values_list,state="readonly")
        X_variable_combobox= self.X_variable_combobox
        X_variable_combobox.grid(row=0,column=1,padx= 5,pady=(0,5),sticky="ew")

        #Y_variable inside the plotting_widgets_frame
        Y_variable_label= ttk.Label(plotting_widgets_frame,text="Y axis")
        Y_variable_label.grid(row=0,column=2,padx= 5,pady=(0,5),sticky="ew")
        self.Y_variable_combobox= ttk.Combobox(plotting_widgets_frame,values=["f","ST","TSFC"],state="readonly")
        Y_variable_combobox= self.Y_variable_combobox
        Y_variable_combobox.grid(row=0,column=3,padx= 5,pady=(0,5),sticky="ew")
    
        #plot_button inside the plotting_widgets_frame
        plot_button= ttk.Button(plotting_widgets_frame,text="Plot",command= self.plot_button_command)
        plot_button.grid(row=1,column=0,columnspan=4,padx= 5,pady=(0,5),sticky="ew")

        self.set_PCA_results_multi_point_calculation()

    #engine_results_frame in the column 1 of the outputs_frame
        engine_results_frame= ttk.LabelFrame(column1_frame,text="Engine Results")
        engine_results_frame.grid(column=0,row=0,sticky="ew")

        #index_entry widget inside the engine_results_frame
        index_label= ttk.Label(engine_results_frame,text="Engine S.No.")
        index_label.grid(row=0,column=0,padx= 5,pady=(0,5),sticky="ew")
        self.index_entry= ttk.Entry(engine_results_frame)
        index_entry= self.index_entry
        index_entry.insert(0,0)  #by default the index is 0
        index_entry.bind('<Return>',self.pca_results_vs_station_properties_checkbutton_command)
        index_entry.grid(row=0,column=1,padx= 5,pady=(0,5),sticky="ew")

        #PCA_results_vs_station_properties_checkbutton widget inside the engine_results_frame
        self.var_pca_results_vs_station_properties_checkbutton= tk.StringVar(value="pca_results")   #True means get PCA for that engine at that index; False means get station properties for that engine at that index
        self.pca_results_vs_station_properties_checkbutton= ttk.Checkbutton(engine_results_frame,text="Station Properties",style="Switch",variable= self.var_pca_results_vs_station_properties_checkbutton,offvalue="pca_results",onvalue="station_properties",command= self.pca_results_vs_station_properties_checkbutton_command) 
        self.pca_results_vs_station_properties_checkbutton.grid(row=1,column=0,columnspan=2,padx= 5,pady=5,sticky="ew")
        
        self.wrapper_tree_frame= ttk.Frame(engine_results_frame)
        wrapper_tree_frame= self.wrapper_tree_frame
        wrapper_tree_frame.grid(row=2,column=0,columnspan=2,sticky='ew')

        self.pca_results_vs_station_properties_checkbutton_command()

    def pca_results_vs_station_properties_checkbutton_command(self,event=None):  #bcz we are calling this function from the index_entry widget hence we need 

        for item in self.wrapper_tree_frame.winfo_children():
            item.destroy()
        
        #PCA_results_tree_view scroll box just below the PCA_results_button
        treeframe= ttk.Frame(self.wrapper_tree_frame)
        treeframe.grid(row=0,column=0,padx= 5,sticky='ew')
        #scrollbar widget
        scrollbar= ttk.Scrollbar(treeframe,orient="vertical")
        scrollbar.pack(side="right",fill="y")            #filling the scrollbar in the y direction
        if self.var_pca_results_vs_station_properties_checkbutton.get()=="pca_results":        #show PCA results
            cols= ["Variable","Value"]
        elif self.var_pca_results_vs_station_properties_checkbutton.get()=="station_properties":       #show station properties
            cols= ["Station","Pressure (kPa)","Temperature (K)"]
        #tree view widget
        self.pca_results_vs_station_properties_tree_view= ttk.Treeview(treeframe,columns=cols,show="headings",height=17, yscrollcommand=scrollbar.set)
        pca_results_vs_station_properties_tree_view= self.pca_results_vs_station_properties_tree_view
        pca_results_vs_station_properties_tree_view.pack()
        for col_name in cols:                                         #initialising the coloumns in the tree_view
            pca_results_vs_station_properties_tree_view.column(col_name,width= 90,anchor="center")
        scrollbar.config(command=pca_results_vs_station_properties_tree_view.yview)         #configuring the scrollbar to the tree_view
        for i in cols:
            pca_results_vs_station_properties_tree_view.heading(i,text=i)

        #firstly remake the engine object at that index by using the parameters_dict
        parameters_dict= self.parameters_dict
        arr= ["engineType","AB","T0","P0","M0","M6","alp","gam_c","gam_t","gam_ab","Rc","Rt","Rab","Cpc","Cpt","Cpab","Tt4","Tt7","Hpr","eta_b","eta_m","eta_ab","pi_d_max","pi_f","pi_c","pi_cL","pi_cH","pi_b","pi_m_max","pi_ab","pi_n","pi_fn","peta_f","peta_c","peta_t","P0_P9","P0_P19","sep_mixed_flow","nozzleType"]
        values= [parameters_dict[i] for i in arr]
        d= dict(zip(arr,values))

        if self.onetwo_indp_var.get()=="one":
            indep_var= self.indep_var_entry_combobox.get()
            indep_var_val= self.engine_lst_dict[int(self.index_entry.get())][1]
            d[indep_var]= indep_var_val
        elif self.onetwo_indp_var.get()=="two":
            indep_var1= self.indep_var1_entry_combobox.get()
            indep_var2= self.indep_var2_entry_combobox.get()
            indep_var1_val= self.engine_lst_dict[int(self.index_entry.get())][1]
            indep_var2_val= self.engine_lst_dict[int(self.index_entry.get())][2]
            d[indep_var1]= indep_var1_val
            d[indep_var2]= indep_var2_val

 
        if (self.onetwo_indp_var.get()=="one" and indep_var=="alt") or (self.onetwo_indp_var.get()=="two" and "alt" in [indep_var1,indep_var2]):
            d["T0"],d["P0"]= self.get_T0_P0_from_alt(d["alt"])
        
        if (self.onetwo_indp_var.get()=="one" and indep_var=="pi_c") or (self.onetwo_indp_var.get()=="two" and "pi_c" in [indep_var1,indep_var2]):
            if self.var_single_dual.get()=="single":
                d["pi_cL"]= d["pi_c"]
                d["pi_cH"]= 1
            elif self.var_single_dual.get()=="dual":
                d["pi_cH"]= d["pi_c"]/d["pi_cL"]

        #basically dict d now contains all the inputs parameters with the corresponding correct values
        engine= initialisingComponents(d["engineType"],d["AB"],d["T0"],d["P0"],d["M0"],d["M6"],d["alp"],d["gam_c"],d["gam_t"],d["gam_ab"],d["Rc"],d["Rt"],d["Rab"],d["Cpc"],d["Cpt"],d["Cpab"],d["Tt4"],d["Tt7"],d["Hpr"],d["eta_b"],d["eta_m"],d["eta_ab"],d["pi_d_max"],d["pi_f"],d["pi_c"],d["pi_cL"],d["pi_cH"],d["pi_b"],d["pi_m_max"],d["pi_ab"],d["pi_n"],d["pi_fn"],d["peta_f"],d["peta_c"],d["peta_t"],d["P0_P9"],d["P0_P19"],d["sep_mixed_flow"],d["nozzleType"]).get_engine()
        self.engine= engine
        [f,ST,TSFC]= engine.get_engineDetails()
        lst,lst0= engine.print_get_details()

        #display the values in the tree_view 
        if self.var_pca_results_vs_station_properties_checkbutton.get()=="pca_results":   #show PCA results
            for i in lst:
                val= i[1]
                if type(i[1]) != str:
                    val= round(val,4)
                pca_results_vs_station_properties_tree_view.insert("",tk.END,values=(syb(i[0]),val))
        elif self.var_pca_results_vs_station_properties_checkbutton.get()=="station_properties":  #show station properties
            for i in lst0:
                pca_results_vs_station_properties_tree_view.insert("",tk.END,values=(i[0],round(i[1],4),round(i[2],4)))

        
        #epa_test_button widget
        epa_test_button= ttk.Button(self.wrapper_tree_frame,text="Test this engine",command= self.epa_test_button_command ) #lambda: messagebox.showinfo("Error","This feature is not available yet. Please wait for the next update.")
        epa_test_button.grid(row=1,column=0,columnspan=2,padx=(10,5),pady=(5,0))


    def outputs_button_command(self):
        """This function is used to create the output window for the turbojet engine."""

        self.var_inputs_button.set(False)
        self.var_outputs_button.set(True)

        if self.inpt_outpt_selected_button=="input":
            self.inputs_frame.grid_forget()      #now we can .grid() to make the earlier inputs_frame reapper  #we cant destroy it bcz when the person goes from outputs to inputs, then he wants to see the main_widgets in their original selected states
            self.inpt_outpt_selected_button="output"
        elif self.inpt_outpt_selected_button=="output" and hasattr(self,"outputs_frame"):
            pass                #do nothing when the user repeatedly clicks the outputs button
            return   

        if hasattr(self,"outputs_frame"):
            for item in self.outputs_frame.winfo_children():
                item.destroy()                

    #outputs_frame which contains three labelframes inside it for PCA_results, station_properties and plots
        self.outputs_frame= ttk.Frame(self.root_frame)
        outputs_frame= self.outputs_frame
        outputs_frame.grid(row=1,column=0,columnspan=2,padx= 5, pady= 5,sticky=tk.W+tk.E)
    
        if self.single_multi_selected_button=="single":
            self.set_outputs_frame_single_point_calculation()
        elif self.single_multi_selected_button=="multi":
            self.set_outputs_frame_multi_point_calculation()

        self.inpt_outpt_selected_button="output"


    def create_TJ_window(self):
        self.root2= tk.Tk()
        root2= self.root2
        self.screen_width= 850
        root2.geometry(f"{self.screen_width}x{self.screen_width-60}")
        root2.resizable(True,True)
        root2.title("TurboJet Engine")

        #set the theme of the previous window
        style = ttk.Style(root2)
        # root2.tk.call('source', "\\".join(os.path.abspath(__file__).split("\\")[0:-1]) +"\\themes\\forest-light.tcl")  
        # root2.tk.call('source', "\\".join(os.path.abspath(__file__).split("\\")[0:-1]) +"\\themes\\forest-dark.tcl") 
        root2.tk.call('source', resource_path("MAIN_GUI\\themes\\forest-light.tcl"))
        root2.tk.call('source', resource_path("MAIN_GUI\\themes\\forest-dark.tcl")) 
        style.theme_use(self.selected_theme)
        if self.selected_theme=="forest-dark":
            root2.config(bg='#313131')    
        else:
            root2.config(bg='#ffffff')

        # Step 1: Create a Font Object
        customFont = Font(family="Helvetica", size=10, weight="bold")

        # Step 2: Define a Custom Style
        style = ttk.Style()
        style.configure("Custom.Toolbutton", font=customFont)

    #creating a root_frame
        self.root_frame= ttk.Frame(root2)       #root_frame all the root window
        root_frame= self.root_frame
        root_frame.pack()

    #top_frame to hold the back_button and test button and other possible optionality for mode and all
    #Its row=1 holds the Input and Output button widgets
        self.top_frame= ttk.Frame(root_frame)       
        top_frame= self.top_frame
        top_frame.grid(row=0,column=0,sticky=tk.W+tk.E)

        #back button widget
        back_button= ttk.Button(top_frame,text="Back",command= self.back_button_command)
        back_button.grid(row=0,column=0,padx=(5,0),pady=(5,0),sticky=tk.W)

        #inputs_button widget
        # input_icon_img= tk.PhotoImage(file=r"C:\Users\ADITI\Downloads\Aditya\PropulsionsSrip\VERSION1.0\MAIN_GUI\themes_images\input_icon.png")
        # input_icon_img= input_icon_img.subsample(8,8)
        self.var_inputs_button= tk.BooleanVar(value=False)
        self.inputs_button= ttk.Checkbutton(top_frame,text="Inputs",style= "Custom.Toolbutton",variable=self.var_inputs_button,command= self.inputs_button_command,width= 55)    #, image=input_icon_img,compound='left'
        inputs_button= self.inputs_button  
        inputs_button.grid(row=1,column=0,padx=(5,0),pady=(5,0)) #,sticky=tk.W

        #outputs_button widget
        # output_icon_img= tk.PhotoImage(file=r"C:\Users\ADITI\Downloads\Aditya\PropulsionsSrip\VERSION1.0\MAIN_GUI\themes_images\output_icon.png")
        # output_icon_img= output_icon_img.subsample(15,15)
        self.var_outputs_button= tk.BooleanVar(value=False)
        self.outputs_button= ttk.Checkbutton(top_frame,text="Outputs",style= "Custom.Toolbutton",variable=self.var_outputs_button,command= self.outputs_button_command,width=55)  #,state="disabled" #,image=output_icon_img,compound='left'
        outputs_button= self.outputs_button
        outputs_button.grid(row=1,column=1,padx= (0,5),pady= (5,0))  #,sticky=tk.E

        self.inputs_button.invoke() #invoke the inputs_button_command function

        root2.mainloop()


    