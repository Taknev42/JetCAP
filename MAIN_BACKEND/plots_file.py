"""This file is used to get engine results during multi point analysis and plot them"""


import os,sys
#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from tkinter import messagebox
import numpy as np
from initialisingComponents_file import initialisingComponents
# sys.path.insert(0,"\\".join(os.path.abspath(__file__).split("\\")[:-2])+"\\MAIN_GUI\\symbols")
sys.path.insert(0,resource_path("MAIN_GUI\\symbols"))
from symbols import get_fullform                     #type:ignore


class plots:
    def __init__(self):
        pass

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
    
    def get_tabulated_engines(self,parameters,indp_var1_iterlst,indp_var2_iterlst= None):

        if indp_var2_iterlst == None:         #That means we have to plot one x_var_list against y_var

            x_axis= indp_var1_iterlst[0]
            x_axis_arr= np.linspace(indp_var1_iterlst[1],indp_var1_iterlst[3],num=int(indp_var1_iterlst[2]))

            return self.foo1(parameters,x_axis,x_axis_arr)

        else:                                      #That means we have two independent variables where we have to plot x_axis against y_axis

            ind_var1= indp_var1_iterlst[0]
            ind_var1_arr= np.linspace(indp_var1_iterlst[1],indp_var1_iterlst[3],num=int(indp_var1_iterlst[2]))

            ind_var2= indp_var2_iterlst[0]
            ind_var2_arr= np.linspace(indp_var2_iterlst[1],indp_var2_iterlst[3],num=int(indp_var2_iterlst[2]))

            return self.foo2(parameters,ind_var1,ind_var1_arr,ind_var2,ind_var2_arr)

    def foo1(self,parameters,x_axis, x_axis_arr):
        global engineType,AB,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType
        engineType= parameters["engineType"]
        AB= parameters["AB"]
        T0=parameters["T0"]
        P0=parameters["P0"]
        M0=parameters["M0"]
        M6= parameters["M6"]
        alp=parameters["alp"]
        gam_c=parameters["gam_c"]
        gam_t=parameters["gam_t"]
        gam_ab=parameters["gam_ab"]
        Rc=parameters["Rc"]
        Rt=parameters["Rt"]
        Rab= parameters["Rab"]
        Cpc=parameters["Cpc"]
        Cpt=parameters["Cpt"]
        Cpab=parameters["Cpab"]
        Tt4=parameters["Tt4"]
        Tt7=parameters["Tt7"]
        Hpr=parameters["Hpr"]
        eta_b=parameters["eta_b"]
        eta_m=parameters["eta_m"]
        eta_ab=parameters["eta_ab"]
        pi_d_max=parameters["pi_d_max"]
        pi_f=parameters["pi_f"]
        pi_c=parameters["pi_c"]
        pi_cL=parameters["pi_cL"]
        pi_cH=parameters["pi_cH"]
        pi_b=parameters["pi_b"]
        pi_m_max= parameters["pi_m_max"]
        pi_ab=parameters["pi_ab"]
        pi_n=parameters["pi_n"]
        pi_fn=parameters["pi_fn"]
        peta_f=parameters["peta_f"]
        peta_c=parameters["peta_c"]
        peta_t=parameters["peta_t"]
        P0_P9= parameters["P0_P9"]
        P0_P19= parameters["P0_P19"]
        sep_mixed_flow= parameters["sep_mixed_flow"]
        nozzleType= parameters["nozzleType"]

        engine_lst_dict= dict() #dictionary to store the engines results for each engine number as its key value and the value stored is a array of the results
        engine_num= 0

        try:
            for x_val in x_axis_arr:
                globals()[x_axis]= x_val

                if x_axis =="pi_c":
                    if pi_cH==1:                   #i.e the engine inputted into plots() is a single-spool
                        pi_cL= pi_c                #we vary pi_lpc
                    else:
                        pi_cH= pi_c/pi_cL          #we vary pi_hpc 
                elif x_axis=="alt":                  #bcz when we vary alt as an itertaion, we had given T0,P0 to be "NA" in the input
                    (T0,P0)= self.get_T0_P0_from_alt(x_val)
                
                engine1= initialisingComponents(engineType,AB,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType).get_engine()
                [f,ST,TSFC]= engine1.get_engineDetails() 
                engine_lst_dict[engine_num]= [engine_num,x_val,None,f,ST,TSFC]
                engine_num= engine_num+1

            return engine_lst_dict

        except:
            messagebox.showerror("Error","Math Domain error encountered during PCA calculation at "+x_axis+"="+str(x_val))
            return None
        
    def foo2(self,parameters,ind_var1,ind_var1_arr,ind_var2,ind_var2_arr):
        global engineType,AB,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType
        engineType= parameters["engineType"]
        AB= parameters["AB"]
        T0=parameters["T0"]
        P0=parameters["P0"]
        M0=parameters["M0"]
        M6= parameters["M6"]
        alp=parameters["alp"]
        gam_c=parameters["gam_c"]
        gam_t=parameters["gam_t"]
        gam_ab=parameters["gam_ab"]
        Rc=parameters["Rc"]
        Rt=parameters["Rt"]
        Rab= parameters["Rab"]
        Cpc=parameters["Cpc"]
        Cpt=parameters["Cpt"]
        Cpab=parameters["Cpab"]
        Tt4=parameters["Tt4"]
        Tt7=parameters["Tt7"]
        Hpr=parameters["Hpr"]
        eta_b=parameters["eta_b"]
        eta_m=parameters["eta_m"]
        eta_ab=parameters["eta_ab"]
        pi_d_max=parameters["pi_d_max"]
        pi_f=parameters["pi_f"]
        pi_c=parameters["pi_c"]
        pi_cL=parameters["pi_cL"]
        pi_cH=parameters["pi_cH"]
        pi_b=parameters["pi_b"]
        pi_m_max= parameters["pi_m_max"]
        pi_ab=parameters["pi_ab"]
        pi_n=parameters["pi_n"]
        pi_fn=parameters["pi_fn"]
        peta_f=parameters["peta_f"]
        peta_c=parameters["peta_c"]
        peta_t=parameters["peta_t"]
        P0_P9= parameters["P0_P9"]
        P0_P19= parameters["P0_P19"]
        sep_mixed_flow= parameters["sep_mixed_flow"]
        nozzleType= parameters["nozzleType"]
    
        # if engineType =="turbojet":
        #     if ind_var1 in ["pi_f","alp"] or ind_var2 in ["pi_f","alp"]:
        #         print(f"Can't plot for pi_f, alp in {engineType}")
        #         exit()
        # elif engineType=="ramjet":
        #     if ind_var1 in ["pi_c","pi_f","alp"] or ind_var2 in ["pi_c","pi_f","alp"]:
        #         print(f"Can't plot for pi_f,pi_c, alp in {engineType}")
        #         exit()

        engine_lst_dict= dict() #dictionary to store the engines results for each engine number as its key value and the value stored is a array of the results
        engine_num= 0

        try:
            for ind_var1_val in ind_var1_arr:
                for ind_var2_val in ind_var2_arr:
                    
                    globals()[ind_var1]= ind_var1_val
                    globals()[ind_var2]= ind_var2_val 

                    if "pi_c" in (ind_var1,ind_var2):
                        if pi_cH==1: 
                            pi_cL= pi_c
                        else:
                            pi_cH = pi_c/pi_cL

                    if "alt" in (ind_var1,ind_var2):
                        (globals()["T0"],globals()["P0"])= self.get_T0_P0_from_alt(globals()["alt"])

                    engine1=initialisingComponents(engineType,AB,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType).get_engine()
                    [f,ST,TSFC]= engine1.get_engineDetails()

                    engine_lst_dict[engine_num]= [engine_num,ind_var1_val,ind_var2_val,f,ST,TSFC]
                    engine_num= engine_num+1

            for ind_var2_val in ind_var2_arr:
                for ind_var1_val in ind_var1_arr:
                    globals()[ind_var1]= ind_var1_val
                    globals()[ind_var2]= ind_var2_val

                    if "pi_c" in (ind_var1,ind_var2):
                        if pi_cH==1: 
                            pi_cL= pi_c
                        else:
                            pi_cH = pi_c/pi_cL

                    if "alt" in (ind_var1,ind_var2):
                        (globals()["T0"],globals()["P0"])= self.get_T0_P0_from_alt(globals()["alt"])
                        
                    engine1=initialisingComponents(engineType,AB,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType).get_engine()
                    [f,ST,TSFC]= engine1.get_engineDetails()
                    
                    engine_lst_dict[engine_num]= [engine_num,ind_var1_val,ind_var2_val,f,ST,TSFC]
                    engine_num= engine_num+1

            return engine_lst_dict
        except:
            messagebox.showerror("Error","Math Domain error encountered during PCA calculation at "+ind_var1+"="+str(ind_var1_val)+" and "+ind_var2+"="+str(ind_var2_val))
            return None

    def show_plots(self,engine_lst_dict,x_var_name,y_var_name,indp_var1_iterlst,indp_var2_iterlst= None):
        plt.close('all')     #close all previous plots

        if indp_var2_iterlst ==None:    #That means we have to plot one x_var_list against y_var   #Here x_axis_name is None
            X= []
            Y= []

            x_axis_name= indp_var1_iterlst[0]
            X= np.linspace(indp_var1_iterlst[1],indp_var1_iterlst[3],num=int(indp_var1_iterlst[2]))
            
            f_index= 3
            ST_index= 4
            TSFC_index= 5
            Y_index= locals()[y_var_name+"_index"]
            Y= [engine_lst_dict[i][Y_index] for i in range(len(engine_lst_dict))]

            plt.plot(X,Y,marker='o')
            plt.xlabel(get_fullform(x_axis_name))
            plt.ylabel(get_fullform(y_var_name))
            plt.show()

        else:

            ind_var1_name= indp_var1_iterlst[0]
            ind_var1_arr= np.linspace(indp_var1_iterlst[1],indp_var1_iterlst[3],num=int(indp_var1_iterlst[2]))
            size1= indp_var1_iterlst[2]
            ind_var2_name= indp_var2_iterlst[0]
            ind_var2_arr= np.linspace(indp_var2_iterlst[1],indp_var2_iterlst[3],num=int(indp_var2_iterlst[2]))
            size2= indp_var2_iterlst[2]

            engine_num= 0
            line_num= 0
            f_index= 3
            ST_index= 4
            TSFC_index= 5
            X_index= locals()[x_var_name+"_index"]
            Y_index= locals()[y_var_name+"_index"]

            colors= iter(cm.hsv(np.linspace(0,1,size1))) #new colormap
            for ind_var1_val in ind_var1_arr:
                X= []
                Y= []
                for ind_var2_val in ind_var2_arr:
                    X.append(engine_lst_dict[engine_num][X_index])                   
                    Y.append(engine_lst_dict[engine_num][Y_index])
                    engine_num=engine_num+1

                lab= "L"+str(line_num)+":  "+ind_var1_name+"="+str(round(ind_var1_val,4))
                plt.plot(X,Y,label=lab,color= next(colors))
                plt.annotate(xy=(X[-1],Y[-1]), xytext=(10,0), textcoords='offset points', text=f"L{line_num}", va='center')
                line_num=line_num+1
            

            colors= iter(cm.viridis(np.linspace(0,1,size2)))
            for ind_var2_val in ind_var2_arr:
                X= []
                Y= []
                for ind_var1_val in ind_var1_arr:
                    X.append(engine_lst_dict[engine_num][X_index])
                    Y.append(engine_lst_dict[engine_num][Y_index])
                    engine_num=engine_num+1

                lab= "L"+str(line_num)+":  "+ind_var2_name+"="+str(round(ind_var2_val,4))
                plt.plot(X,Y,label=lab,color= next(colors))
                plt.annotate(xy=(X[-1],Y[-1]), xytext=(5,0), textcoords='offset points', text=f"L{line_num}", va='center')
                line_num=line_num+1

            x_axis_name= x_var_name
            y_axis_name= y_var_name
            plt.legend()
            plt.xlabel(get_fullform(x_axis_name))
            plt.ylabel(get_fullform(y_axis_name))
            plt.show()






