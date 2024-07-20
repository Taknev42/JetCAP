"""This class is used to store the code for the EPA window pop-up of the PCA-EPA software."""


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
from tkinter import ttk #package used to import themes
# sys.path.insert(0,"\\".join(os.path.abspath(__file__).split("\\")[:-2])+"\\MAIN_BACKEND")
sys.path.insert(0,resource_path("MAIN_BACKEND"))
from EPAtesting import EPAtesting_class                                           #type: ignore
from tkinter import messagebox
# sys.path.insert(0,"\\".join(os.path.abspath(__file__).split("\\")[:-1])+"\\symbols")
sys.path.insert(0,resource_path("MAIN_GUI\\symbols"))
from symbols import get_symbol as syb                                       #type: ignore

class EPA_window_class:
    def __init__(self,selected_theme,refEngine):
        self.selected_theme= selected_theme
        self.refEngine= refEngine

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

    def set_pca_result_ref(self,event):
        
        try:
            m_dot= float(self.m_dot_entry.get())
        except:
            messagebox.showerror("Error","Please enter valid parameter values")
            return
        
        try:
            refEngine= self.refEngine
            lst,lst0= refEngine.print_get_details()

            #clearing the pca_results_tree_view
            for item in self.refPoint_tree_view.get_children():
                self.refPoint_tree_view.delete(item)
            #displaying the PCA results
            for i in lst:
                val= i[1]
                if type(i[1]) != str:
                    val= round(val,4)
                self.refPoint_tree_view.insert("",tk.END,values=(syb(i[0]),val))
            
            refPointThrust= refEngine.ST*m_dot
            self.refPoint_thrust_text.config(state="normal")
            self.refPoint_thrust_text.delete("0",'end')
            self.refPoint_thrust_text.insert(0,round(refPointThrust/1e+3,4))
            self.refPoint_thrust_text.config(state="disabled")
        except:
            messagebox.showerror("Error","Error encountered during PCA calculation for reference point")
            return


    def set_pca_result_test(self,event):
        
        if (self.m_dot_entry.get()=="" or self.m_dot_entry.get()==syb("m_dot")) or (self.temperature_entry.get()=="" or self.temperature_entry.get()=="Temperature (K)") or (self.pressure_entry.get()=="" or self.pressure_entry.get()=="Pressure (KPa)") or (self.M0_entry.get()=="" or self.M0_entry.get()=="Mach Number") or (self.Tt4_entry.get()=="" or self.Tt4_entry.get()=="Turbine Inlet Temperature"):
            return  #do nothing
        
        try:
            m_dot= float(self.m_dot_entry.get())
            T0= float(self.temperature_entry.get())
            P0= float(self.pressure_entry.get())*1e+3
            M0= float(self.M0_entry.get())
            Tt4= float(self.Tt4_entry.get())
        except:
            messagebox.showerror("Error","Please enter valid parameter values")
            return 
        
        try:
            self.testEngine,m_dot_test= EPAtesting_class(self.refEngine,m_dot,[T0,P0,M0,Tt4]).get_testEngine_m_dot_T()
            testEngine= self.testEngine
            [f,ST,TSFC]= testEngine.get_engineDetails()
            lst,lst0= testEngine.print_get_details()

            #clearing the pca_results_tree_view
            for item in self.testPoint_tree_view.get_children():
                self.testPoint_tree_view.delete(item)
            #displaying the PCA results
            for i in lst:
                val= i[1]
                if type(i[1]) != str:
                    val= round(val,4)
                self.testPoint_tree_view.insert("",tk.END,values=(syb(i[0]),val))
            
            testPointThrust= self.testEngine.ST*m_dot_test
            self.testPoint_thrust_text.config(state="normal")
            self.testPoint_thrust_text.delete("0","end")
            self.testPoint_thrust_text.insert(0,round(testPointThrust/1e+3,4)) 
            self.testPoint_thrust_text.config(state="disabled")
        except:
            messagebox.showerror("Error","Error encountered during EPA calculation")
            return 


    def create_EPA_window(self):
        self.root3= tk.Tk()
        root3= self.root3
        self.screen_width= 850
        self.screen_height= 350
        root3.geometry(f"{self.screen_width}x{self.screen_height}")
        root3.resizable(True,True)
        root3.title("EPA Testing")

        #set the theme of the previous window
        style = ttk.Style(root3)
        # root3.tk.call('source', "\\".join(os.path.abspath(__file__).split("\\")[0:-1]) +"\\themes\\forest-light.tcl")
        # root3.tk.call('source',  "\\".join(os.path.abspath(__file__).split("\\")[0:-1]) +"\\themes\\forest-dark.tcl")
        root3.tk.call('source', resource_path("MAIN_GUI\\themes\\forest-light.tcl"))
        root3.tk.call('source', resource_path("MAIN_GUI\\themes\\forest-dark.tcl"))
        style.theme_use(self.selected_theme)
        if self.selected_theme=="forest-dark":
            root3.config(bg='#313131')    
        else:
            root3.config(bg='#ffffff')

    #creating a root_frame
        self.root_frame= ttk.Frame(root3)       #root_frame all the root window
        root_frame= self.root_frame
        root_frame.pack()

    #column0_frame
        column0_frame= ttk.Frame(root_frame)
        column0_frame.grid(row=0,column=0,padx=10,pady=10)

    #Engine Sizing label frame 
        engine_sizing_widgets_frame= ttk.LabelFrame(column0_frame,text="Engine Sizing @ Reference Point")
        engine_sizing_widgets_frame.grid(column=0,row=0)   

        #m_dot_entry widget
        m_dot_label= ttk.Label(engine_sizing_widgets_frame,text= "Mass Flow Rate (kg/s)")
        m_dot_label.grid(row=0,column=0,padx=5,pady=(0,5))
        self.m_dot_entry= ttk.Entry(engine_sizing_widgets_frame)
        m_dot_entry= self.m_dot_entry
        m_dot_entry.grid(row=0,column=1,padx=(0,5),pady=(0,5))
        m_dot_entry.insert(0,syb("m_dot"))
        m_dot_entry.bind("<FocusIn>",lambda args: m_dot_entry.delete('0','end'))
        m_dot_entry.bind('<Return>',self.set_pca_result_ref)


    #Test conditions widget frame
        test_conditions_widget_frame= ttk.LabelFrame(column0_frame,text="Test Conditions")
        test_conditions_widget_frame.grid(column=0,row=1,pady=5)
        row_num=0  

        #altitude alt entry widget
        alt_label= ttk.Label(test_conditions_widget_frame,text= "Altitude (m)")
        alt_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="nsew")
        self.alt_entry= ttk.Entry(test_conditions_widget_frame)
        alt_entry= self.alt_entry
        alt_entry.insert(0,"Altitude (m)")
        alt_entry.bind("<FocusIn>",lambda args: alt_entry.delete('0','end'))
        alt_entry.bind('<Return>',self.on_enter_alt_entry)
        alt_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="nsew")
        row_num+=1
        
        #Temperature T0 entry widget
        temperature_label= ttk.Label(test_conditions_widget_frame,text= "Temperature T0 (K)")
        temperature_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="nsew")
        self.temperature_entry= ttk.Entry(test_conditions_widget_frame)
        temperature_entry= self.temperature_entry 
        temperature_entry.insert(0,"Temperature (K)")
        temperature_entry.bind("<FocusIn>",lambda args: temperature_entry.delete('0','end'))
        temperature_entry.bind('<Return>',self.set_pca_result_test)
        temperature_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="nsew")
        row_num+=1          

        #Pressure P0 entry widget
        pressure_label= ttk.Label(test_conditions_widget_frame,text= "Pressure P0 (KPa)")
        pressure_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="nsew")
        self.pressure_entry= ttk.Entry(test_conditions_widget_frame)
        pressure_entry= self.pressure_entry 
        pressure_entry.insert(0,"Pressure (KPa)")
        pressure_entry.bind("<FocusIn>",lambda args: pressure_entry.delete('0','end'))
        pressure_entry.bind('<Return>',self.set_pca_result_test)
        pressure_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="nsew")
        row_num+=1


        #Mach Number M0 entry widget
        M0_label= ttk.Label(test_conditions_widget_frame,text= "Mach Number M0")
        M0_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="nsew")
        self.M0_entry= ttk.Entry(test_conditions_widget_frame)
        M0_entry= self.M0_entry 
        M0_entry.insert(0,"Mach Number")
        M0_entry.bind("<FocusIn>",lambda args: M0_entry.delete('0','end'))
        M0_entry.bind('<Return>',self.set_pca_result_test)
        M0_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="nsew")
        row_num+=1

        #Tt4 entry widget
        Tt4_label= ttk.Label(test_conditions_widget_frame,text= "Tt4 (K)")
        Tt4_label.grid(row=row_num,column=0,padx= 5,pady=(0,5),sticky="nsew")
        self.Tt4_entry= ttk.Entry(test_conditions_widget_frame)
        Tt4_entry= self.Tt4_entry 
        Tt4_entry.insert(0,"Turbine Inlet Temperature")
        Tt4_entry.bind("<FocusIn>",lambda args: Tt4_entry.delete('0','end'))
        Tt4_entry.bind('<Return>',self.set_pca_result_test)
        Tt4_entry.grid(row=row_num,column=1,padx= 5,pady=(0,5),sticky="nsew") 
        row_num+=1       

    #column1 frame
        column1_frame= ttk.Frame(root_frame)
        column1_frame.grid(row=0,column=1,pady=10)

        #refPoint_results_frame 
        refPoint_results_frame= ttk.LabelFrame(column1_frame,text="Reference Point")
        refPoint_results_frame.grid(row=0,column=0,padx=(0,5),pady=10,sticky="w")

        treeframe= ttk.Frame(refPoint_results_frame)
        treeframe.grid(row=0,column=0,columnspan=2,sticky=tk.E+tk.W)
        #scrollbar widget
        scrollbar= ttk.Scrollbar(treeframe,orient="vertical")
        scrollbar.pack(side="right",fill="y")            #filling the scrollbar in the y direction
        cols= ["Parameter","Value"]
        #tree view widget
        self.refPoint_tree_view= ttk.Treeview(treeframe,columns=cols,show="headings",height=10, yscrollcommand=scrollbar.set)
        refPoint_tree_view= self.refPoint_tree_view
        refPoint_tree_view.pack()
        for col_name in cols:                                         #initialising the coloumns in the tree_view
            refPoint_tree_view.column(col_name,width= 100,anchor="center")
        scrollbar.config(command=refPoint_tree_view.yview)         #configuring the scrollbar to the tree_view
        refPoint_tree_view.heading('Parameter',text='Parameter')
        refPoint_tree_view.heading('Value',text='Value')

        label= ttk.Label(refPoint_results_frame,text="Thrust (KN)")
        label.grid(row=1,column=0)
        # self.refPoint_thrust_text= tk.Text(refPoint_results_frame)
        # refPoint_thrust_text= self.refPoint_thrust_text
        # refPoint_thrust_text.grid(row=1,column=1)
        self.refPoint_thrust_text= ttk.Entry(refPoint_results_frame)
        refPoint_thrust_text= self.refPoint_thrust_text
        refPoint_thrust_text.grid(row=1,column=1)
        refPoint_thrust_text.config(state="disabled")


        #testPoint_results_frame 
        testPoint_results_frame= ttk.LabelFrame(column1_frame,text="Test Point")
        testPoint_results_frame.grid(row=0,column=1,padx=(0,5),pady=10)

        treeframe= ttk.Frame(testPoint_results_frame)
        treeframe.grid(row=0,column=0,columnspan=2,sticky=tk.W+tk.E)
        #scrollbar widget
        scrollbar= ttk.Scrollbar(treeframe,orient="vertical")
        scrollbar.pack(side="right",fill="y")            #filling the scrollbar in the y direction
        cols= ["Parameter","Value"]
        #tree view widget
        self.testPoint_tree_view= ttk.Treeview(treeframe,columns=cols,show="headings",height=10, yscrollcommand=scrollbar.set)
        testPoint_tree_view= self.testPoint_tree_view
        testPoint_tree_view.pack()
        for col_name in cols:                                         #initialising the coloumns in the tree_view
            testPoint_tree_view.column(col_name,width= 100,anchor="center")
        scrollbar.config(command=testPoint_tree_view.yview)         #configuring the scrollbar to the tree_view
        testPoint_tree_view.heading('Parameter',text='Parameter')
        testPoint_tree_view.heading('Value',text='Value')

        label= ttk.Label(testPoint_results_frame,text="Thrust (KN)")
        label.grid(row=1,column=0)
        # self.testPoint_thrust_text= tk.Text(testPoint_results_frame)
        # testPoint_thrust_text= self.testPoint_thrust_text
        # testPoint_thrust_text.grid(row=1,column=1)
        self.testPoint_thrust_text= ttk.Entry(testPoint_results_frame)
        testPoint_thrust_text= self.testPoint_thrust_text
        testPoint_thrust_text.grid(row=1,column=1)
        testPoint_thrust_text.config(state="disabled")

        root3.mainloop()