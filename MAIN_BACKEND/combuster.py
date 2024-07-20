import os,sys
#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


import pandas as pd
import numpy as np
file_path =  resource_path("MAIN_BACKEND\\data_files\\SM 06_Mattingly_AppL.xlsx")


class combustor:
    def __init__(self,pi_b,eta_b,Tt4,aircraft,combuster=None,type="CC"):  #default is CC combustion chamber
        self.pi_b= pi_b
        self.eta_b= eta_b
        self.Tt4= Tt4
        self.aircraft= aircraft
        self.combuster= combuster                 # !=None if type="AB"
        self.type=type

    def get_tau_L(self):
        if hasattr(self,"tau_L"):
            return self.tau_L
        
        if self.type=="CC":
            Cpt= self.aircraft.fuel.Cpt
            Cpc= self.aircraft.fuel.Cpc
        elif self.type=="AB":
            Cpt= self.aircraft.fuel.Cpab
            Cpc= self.aircraft.fuel.Cpt
        Tt4= self.Tt4
        T0= self.aircraft.atm.T0

        Num= Cpt*Tt4
        Deno= Cpc*T0
        self.tau_L= Num/Deno
        return self.tau_L

    def get_PnT(self,Pt_in, Tt_in):
        self.Tt3= Tt_in
        Pt_out= self.pi_b*Pt_in
        Tt_out= self.Tt4

        return (Pt_out,Tt_out)
    
    def get_f(self):
        if hasattr(self,"f"):
            return self.f
        
        if self.type=="CC":
            self.f= self.get_f_CC()
            return self.f
        else:
            self.f= self.get_f_ab()
            return self.f   
        
    def get_f_CC(self):
        Tt4= self.Tt4
        Tt3= self.Tt3

        if (Tt3 >170 and Tt4 < 2220):     #To check if the input and output temperature is in the range of the data table
            alp = self.aircraft.alp
            eta_b = self.eta_b
            hpr = self.aircraft.fuel.Hpr/1e+3

            df = pd.read_excel(file_path)

            f_g = 0.0338                        #random guess fuel air ratio
            df = df.rename(columns={'f = 0': 0, 'f = 0.0169': 0.0169, 'f = 0.0338': 0.0338, 'f = 0.0507': 0.0507, 'f = 0.0676': 0.0676})
            lst = list(df.columns[1:])

            if type(Tt3) != str:
                Tt3 = float(round(Tt3,-1))
            if type(Tt4) != str:
                Tt4 = float(round(Tt4,-1))

            ht3 = df.loc[df['T'] == Tt3, 0].iloc[0]
            ht4 = df.loc[df['T'] == Tt4, f_g].iloc[0]

            f_new = (ht4 - ht3)/(eta_b*hpr - ht4)
            f_old= np.Inf

            er= 1e-6                         #error tolerance
            while abs(f_old - f_new) > er:
                for i in lst:
                    if i<f_new:
                        left_f= i
                    else:
                        right_f= i
                        break
                beta = (f_new - right_f)/(left_f-right_f)

                ht4_left_f = df.loc[df['T'] == Tt4, left_f].iloc[0]
                ht4_right_f = df.loc[df['T'] == Tt4, right_f].iloc[0]
                ht4_new = beta*(ht4_left_f) + (1-beta)*ht4_right_f

                f_old= f_new                                        #storing the old value of f
                
                f_new = (ht4_new - ht3)/(eta_b*hpr - ht4_new)

            f= f_new/(1+alp)                #bcz the data table if for m_fuel/m_dot_core

            return f                        #m_fuel/m_dot_net

        else:
            Cpc= self.aircraft.fuel.Cpc
            Cpt= self.aircraft.fuel.Cpt
            Hpr = self.aircraft.fuel.Hpr
            eta_b= self.eta_b
            alp= self.aircraft.alp

            temp1= Cpt*Tt4 - Cpc*Tt3
            temp2= (eta_b*Hpr -Cpt*Tt4)*(1+alp)               # Accurate formula
            # temp2= (eta_b*Hpr )*(1+alp)                     # PARA Assumption
            f= temp1/temp2                                    #m_dot_fuel/m_dot_net_air_inflow

            return f


    def get_f_ab(self):                             #To be used only for AB of turbofan and turbojet engines
        Tt7= self.Tt4
        Tt6A= self.Tt3                              #Always call get_PnT() before get_f()

        Cpab= self.aircraft.fuel.Cpab
        Cpt= self.aircraft.fuel.Cpt
        Hpr= self.aircraft.fuel.Hpr
        eta_ab= self.eta_b

        f_CC= self.combuster.get_f()

        num= (1+f_CC)*(Cpab*Tt7 - Cpt*Tt6A)
        deno= eta_ab*Hpr - Cpab*Tt7

        f= num/deno                                 #m_dot_fuel_AB/m_dot_net_air_inflow
        return f

